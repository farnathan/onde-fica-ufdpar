"""
Ajusta dados/contornos.json depois do contornos.py, nos prédios em que o recorte pela cor falha.

- Bloco 14 (Auditório) e Biblioteca Central (BC): o telhado encosta em outros telhados claros, então o
  recorte pela cor "vaza" para o vizinho. Aqui o contorno vem dos perfis de linhas e colunas: dentro da
  caixa do prédio no OpenStreetMap (com folga), pega o trecho contínuo em que mais de 70% dos pixels são
  telhado claro. Os dois telhados são retângulos alinhados à planta.
- Escola de Aplicação (EA): tira o "calombo" no alto do contorno, resto da etiqueta apagada da ilustração.

Uso: python3 contornos.py && python3 ajustar_contornos.py   (a partir da pasta ferramentas/)
Depois, copie o conteúdo de dados/contornos.json para a constante OUTLINE do index.html.
"""
import json
import os

import cv2
import numpy as np

from contorno_osm import carregar_predios

AQUI = os.path.dirname(os.path.abspath(__file__))
X0, Y0, PPU = 760, 160, 3
CAMINHO = os.path.join(AQUI, "dados", "contornos.json")

c = cv2.imread(os.path.join(AQUI, "dados", "planta-limpa.png"))
html = open(os.path.join(AQUI, "..", "index.html"), encoding="utf8").read()
pred = carregar_predios(os.path.join(AQUI, "fontes", "campus-openstreetmap.osm"), html, X0, Y0, PPU, c.shape[:2])
hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
telha = (hsv[..., 1] < 40) & (hsv[..., 2] > 200)  # telhado branco ou azulado claro
cont = json.load(open(CAMINHO))


def predio_osm(chave):
    """Prédio do OpenStreetMap que mais se sobrepõe ao contorno atual."""
    alvo = np.zeros(telha.shape, np.uint8)
    cv2.fillPoly(alvo, [np.round((np.array(cont[chave]) - (X0, Y0)) * PPU).astype(np.int32)], 1)
    melhor, escolhido = 0, None
    for q in pred:
        m = np.zeros(telha.shape, np.uint8)
        cv2.fillPoly(m, [np.round(q).astype(np.int32)], 1)
        iou = (alvo & m).sum() / max((alvo | m).sum(), 1)
        if iou > melhor:
            melhor, escolhido = iou, q
    return escolhido


def retangulo_do_telhado(chave, folga=45, limiar=0.7):
    q = predio_osm(chave)
    x0, y0 = q.min(0)
    x1, y1 = q.max(0)
    mx, my = int((x1 - x0) * 0.25), int((y1 - y0) * 0.25)  # faixa central, longe dos vizinhos
    X = np.arange(int(x0) - folga, int(x1) + folga + 1)
    Y = np.arange(int(y0) - folga, int(y1) + folga + 1)
    col = telha[int(y0) + my:int(y1) - my, X].mean(0)
    lin = telha[Y, int(x0) + mx:int(x1) - mx].mean(1)

    def trecho(v, eixo):
        ok = np.nonzero(v > limiar)[0]
        meio = len(v) // 2
        partes = np.split(ok, np.nonzero(np.diff(ok) > 3)[0] + 1)
        p = [g for g in partes if g[0] <= meio <= g[-1]] or [max(partes, key=len)]
        return eixo[p[0][0]], eixo[p[0][-1]] + 1

    a, b = trecho(col, X)
    t, u = trecho(lin, Y)
    xa, xb = round(X0 + a / PPU, 1), round(X0 + b / PPU, 1)
    ya, yb = round(Y0 + t / PPU, 1), round(Y0 + u / PPU, 1)
    return [[xa, ya], [xb, ya], [xb, yb], [xa, yb]]


for chave in ("14", "BC"):
    cont[chave] = retangulo_do_telhado(chave)
    print(chave, cont[chave])

# EA: o alto do telhado é reto em y = 703; pontos acima disso são resto da etiqueta
cont["EA"] = [p for p in cont["EA"] if p[1] >= 702.5]
print("EA", len(cont["EA"]), "pontos")

json.dump(cont, open(CAMINHO, "w"))
