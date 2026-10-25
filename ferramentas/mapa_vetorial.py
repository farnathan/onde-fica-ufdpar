"""
Gera ../mapa-campus.svg: o mapa do campus redesenhado em vetor, sem a ilustração por baixo.

De onde vem cada coisa:
- Telhados: detectados na ilustração limpa pela textura (as telhas têm listras; piso e grama são lisos),
  mais os contornos do site (constante OUTLINE do index.html) onde a ilustração ainda tem mancha.
- Grama, árvores, asfalto, vias internas e a pista do Espaço de Convivência: pela cor da ilustração limpa.
- Árvores viram círculos (centro e raio pelo mapa de distâncias da copa).
- Nomes de ruas e lugares: escritos aqui, nas posições da ilustração.
Tudo em coordenadas da planta (as mesmas do site), então pinos, rotas e GPS continuam alinhados.

Uso:   python3 mapa_vetorial.py      (a partir da pasta ferramentas/, depois do limpar_planta.py)
Saída: ../mapa-campus.svg
"""
import json
import os
import re

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X0, Y0, PPU = 760, 160, 3

# ---------- paleta (identidade da UFDPar: neutros frios, verde suave, marinho nos contornos) ----------
COR = {
    "piso": "#F2F3F5", "grama": "#D3E5C2", "via": "#DCE1E7", "asfalto": "#B7C0CA",
    "arvore": "#A3CA87", "arvore_borda": "#8FBC70", "telhado": "#FFFFFF", "telhado_borda": "#8C9CB0",
    "telha": "#E2E7EE", "sombra": "#D2D9E2", "pista_a": "#E7B4A6", "pista_b": "#AEC2E4", "rotulo_rua": "#3B4A5C", "rotulo": "#55667A",
}

img = cv2.imread(os.path.join(AQUI, "dados", "planta-limpa.png"))
ilha = cv2.imread(os.path.join(AQUI, "dados", "planta-mascara.png"), 0) > 0
html = open(os.path.join(AQUI, "..", "index.html"), encoding="utf8").read()
OUTLINE = json.loads(re.search(r"const OUTLINE=(\{.*?\});", html).group(1))
H, W = ilha.shape

# ---------- classes pela cor (imagem suavizada, sem as listras) ----------
sm = cv2.bilateralFilter(cv2.medianBlur(img, 9), 9, 40, 9)
hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(int)
Hh, Ss, Vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
verde = (Hh >= 28) & (Hh <= 55) & (Ss > 70)
grama = verde & ilha
arvore = verde & (Vv < 118) & ilha
asfalto = (Ss < 70) & (Vv < 128) & (Hh >= 95) & (Hh <= 125) & ilha
via = (Ss < 40) & (Vv >= 135) & (Vv <= 172) & ilha & ~verde
pista_a = ((Hh <= 14) | (Hh >= 170)) & (Ss > 70) & (Vv > 90) & ilha
pista_b = (Hh >= 96) & (Hh <= 125) & (Ss > 110) & ilha

# ---------- telhados pela textura ----------
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
mu = cv2.blur(g, (9, 9))
sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - mu * mu, 0))
gx = cv2.blur(np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)), (15, 15))
gy = cv2.blur(np.abs(cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)), (15, 15))
aniso = np.abs(gx - gy) / (gx + gy + 1)
sat = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 1]
claro = (sat < 45) | pista_a
# telhas cinza têm brilho médio ~175-185; pátios de piso cinza ficam ~150-160 e também têm textura
telhado = (claro & ((sd > 6) | ((aniso > 0.35) & ((gx + gy) > 8))) & (mu > 166)) | ((mu > 232) & (sat < 20))
telhado &= ilha
telhado = telhado.astype(np.uint8)
telhado = cv2.morphologyEx(telhado, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
telhado = cv2.morphologyEx(telhado, cv2.MORPH_OPEN, np.ones((21, 21), np.uint8))  # tira bordas finas de calçada
for poly in OUTLINE.values():  # contornos do site: cobrem manchas que sobraram nos telhados
    cv2.fillPoly(telhado, [np.round((np.array(poly) - (X0, Y0)) * PPU).astype(np.int32)], 1)


def tira_pequenos(mk, area_min):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk.astype(np.uint8))
    out = np.zeros(mk.shape, np.uint8)
    for i in range(1, n):
        if st[i, 4] >= area_min:
            out[lab == i] = 1
    return out


def fecha_buracos(mk, area_max):
    """Preenche buracos menores que area_max (manchas dentro de telhados), mantém pátios."""
    inv = (1 - mk).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv)
    out = mk.copy()
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a <= area_max and x > 0 and y > 0 and x + w < mk.shape[1] and y + h < mk.shape[0]:
            out[lab == i] = 1
    return out


def tira_finos(mk, espessura_min):
    """Remove faixas finas (muros, meios-fios): componentes cuja maior distância à borda é pequena."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk.astype(np.uint8))
    dt = cv2.distanceTransform(mk.astype(np.uint8), cv2.DIST_L2, 5)
    mx = np.zeros(n)
    np.maximum.at(mx, lab.ravel(), dt.ravel())
    ok = mx >= espessura_min / 2
    ok[0] = False
    return ok[lab].astype(np.uint8)


telhado = fecha_buracos(tira_finos(tira_pequenos(telhado, 60 * 9), 30), 12000)
tel = telhado > 0


def limpa(mk, abrir=5, fechar=5, area=150):
    mk = mk.astype(np.uint8)
    if fechar:
        mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (fechar, fechar)))
    if abrir:
        mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (abrir, abrir)))
    return tira_pequenos(mk, area) > 0


grama = limpa(grama & ~tel, 7, 7, 400)
copa = limpa(arvore & ~tel, 5, 9, 120)
asfalto = fecha_buracos(limpa(asfalto & ~tel, 7, 7, 600).astype(np.uint8), 4000) > 0  # tira os nomes de rua da ilustração
via = limpa(via & ~tel & ~asfalto, 9, 7, 900)
# a pista colorida só existe no Espaço de Convivência; fora dali, vermelho/azul é resto de telha ou ícone
zona = np.zeros(ilha.shape, bool)
zona[int((330 - Y0) * PPU):int((585 - Y0) * PPU), int((1470 - X0) * PPU):int((1505 - X0) * PPU)] = True
pista_a = limpa(pista_a & ~tel & zona, 3, 3, 60)
pista_b = limpa(pista_b & ~tel & zona, 3, 3, 60)
# dois materiais de telhado: branco (Auditório, Biblioteca, blocos 19 a 26...) e telha cinza (blocos 2 a 17)
lisa = cv2.blur(g, (31, 31))
branco = limpa(tel & (lisa > 205), 9, 9, 900)
# onde o site tem o contorno exato do prédio (OUTLINE, telhados brancos), ele substitui a borda detectada
contorno = np.zeros(ilha.shape, np.uint8)
for poly in OUTLINE.values():
    cv2.fillPoly(contorno, [np.round((np.array(poly) - (X0, Y0)) * PPU).astype(np.int32)], 1)
perto = cv2.dilate(contorno, np.ones((19, 19), np.uint8)) > 0
branco = tira_pequenos((branco & ~perto) | (contorno > 0), 900) > 0
# a borda do telhado branco escurece no desfoque e viraria um anel de "telha": absorve esse anel
branco = branco | (cv2.dilate(branco.astype(np.uint8), np.ones((13, 13), np.uint8)) > 0) & tel & ~perto
# prédios que ainda têm mancha na ilustração: usa o retângulo do site (constante B)
RET = {}
for k, x, y, w, h in re.findall(r'\["(\w+)","\w+","[^"]*",(?:null|\[[\d,]+\]),\[.*?\]\],\[(\d+),(\d+),(\d+),(\d+)\]', html):
    RET[k] = [int(x), int(y), int(w), int(h)]
for k, alvo in (("18", "branco"), ("7", "telha")):
    x, y, w, h = RET[k]
    a0, b0, a1, b1 = [int(round(v)) for v in ((x - X0) * PPU, (y - Y0) * PPU, (x + w - X0) * PPU, (y + h - Y0) * PPU)]
    caixa = np.zeros(ilha.shape, bool)
    caixa[b0:b1, a0:a1] = True
    perto_cx = cv2.dilate(caixa.astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
    tel = (tel & ~(perto_cx & ~caixa)) | caixa
    branco = (branco & ~perto_cx) | (caixa if alvo == "branco" else False)
telha = tel & ~branco & ~perto


# ---------- vetorização ----------
def P(x, y):
    return f"{x / PPU + X0:.1f} {y / PPU + Y0:.1f}"


def caminho(mk, eps=2.5):
    cnts, hier = cv2.findContours(mk.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hier is None:
        return ""
    partes = []
    for cn in cnts:
        ap = cv2.approxPolyDP(cn, eps, True).reshape(-1, 2)
        if len(ap) < 3 or abs(cv2.contourArea(ap)) < 30:
            continue
        partes.append("M" + "L".join(P(x, y) for x, y in ap) + "Z")
    return "".join(partes)


def arvores(mk):
    dt = cv2.distanceTransform(mk.astype(np.uint8), cv2.DIST_L2, 5)
    pico = (dt == cv2.dilate(dt, np.ones((13, 13), np.uint8))) & (dt >= 6)
    ys, xs = np.nonzero(pico)
    ordem = np.argsort(-dt[ys, xs])
    aceitos = []
    for i in ordem:
        x, y, r = xs[i], ys[i], dt[ys[i], xs[i]]
        if all((x - a) ** 2 + (y - b) ** 2 > (0.75 * max(r, s)) ** 2 for a, b, s in aceitos):
            aceitos.append((x, y, r))
    return [(x / PPU + X0, y / PPU + Y0, min(r * 1.15, 40) / PPU) for x, y, r in aceitos]


d_ilha = caminho(ilha, 3)
d_grama = caminho(grama, 3)
d_via = caminho(via, 3)
d_asf = caminho(asfalto, 2.5)
d_pa = caminho(pista_a, 1.5)
d_pb = caminho(pista_b, 1.5)
d_tel = caminho(tel, 2.5)
d_branco = caminho(branco, 3.5)
d_telha = caminho(telha, 3.5)
circ = arvores(copa)

ROTULOS = [  # (texto, x, y, tamanho, rotação, cor)
    ("Av. São Sebastião", 1560, 1250, 20, 0, "rotulo_rua"),
    ("Av. Dep. Pinheiro Machado", 1754, 940, 20, -90, "rotulo_rua"),
    ("Passarela", 1386, 656, 9, 0, "rotulo"),
    ("Praça Universitária", 1392, 922, 9, 0, "rotulo"),
    ("Espaço de Convivência", 1472, 476, 8, 0, "rotulo"),
]

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0} {Y0} 1100 1140" width="1100" height="1140">',
       '<style>text{font-family:Hind,"Segoe UI",Arial,sans-serif;font-weight:700}</style>',
       f'<path d="{d_ilha}" fill="{COR["piso"]}"/>',
       f'<path d="{d_via}" fill="{COR["via"]}" fill-rule="evenodd"/>',
       f'<path d="{d_grama}" fill="{COR["grama"]}" fill-rule="evenodd"/>',
       f'<path d="{d_asf}" fill="{COR["asfalto"]}" fill-rule="evenodd"/>',
       f'<path d="{d_pa}" fill="{COR["pista_a"]}"/><path d="{d_pb}" fill="{COR["pista_b"]}"/>',
       '<g fill="{}" stroke="{}" stroke-width="0.8">{}</g>'.format(
           COR["arvore"], COR["arvore_borda"],
           "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>' for x, y, r in circ)),
       f'<path d="{d_tel}" fill="{COR["sombra"]}" fill-rule="evenodd" transform="translate(1.6 1.6)"/>',
       f'<path d="{d_telha}" fill="{COR["telha"]}" stroke="{COR["telhado_borda"]}" stroke-width="1.1" stroke-linejoin="round" fill-rule="evenodd"/>',
       f'<path d="{d_branco}" fill="{COR["telhado"]}" stroke="{COR["telhado_borda"]}" stroke-width="1.1" stroke-linejoin="round" fill-rule="evenodd"/>']
# campo de futebol da Escola de Aplicação (linhas brancas sobre a grama)
fx, fy, fw, fh = 903, 832, 97, 66
svg.append(f'<g fill="none" stroke="#FFFFFF" stroke-width="1.2"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}"/>'
           f'<line x1="{fx + fw / 2}" y1="{fy}" x2="{fx + fw / 2}" y2="{fy + fh}"/><circle cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="9"/>'
           f'<rect x="{fx}" y="{fy + fh / 2 - 14}" width="12" height="28"/><rect x="{fx + fw - 12}" y="{fy + fh / 2 - 14}" width="12" height="28"/></g>')
for t, x, y, s, rot, cor in ROTULOS:
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    svg.append(f'<text x="{x}" y="{y}" font-size="{s}" fill="{COR[cor]}" text-anchor="middle"{tr}>{t}</text>')
svg.append("</svg>")
open(os.path.join(AQUI, "..", "mapa-campus.svg"), "w", encoding="utf8").write("\n".join(svg))
print("árvores:", len(circ), "| tamanho:", sum(len(x) for x in svg) // 1024, "KB")
