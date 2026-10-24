"""Preenchimento guiado pelo contorno real dos prédios (OpenStreetMap), usado pelo limpar_planta.py.

Onde a mancha cobre a borda de um telhado, o contorno do OpenStreetMap diz onde fica essa borda.
Cada contorno é antes encaixado na borda visível do desenho (o OpenStreetMap pode estar alguns
metros deslocado em relação à ilustração). Depois:
- dentro do prédio: preenche só com textura do mesmo telhado (e, com tons=True, de cada faixa de tom);
- fora: reconstrói as áreas (grama, calçada...) e preenche cada uma com a própria textura.
"""
import math
import re
import xml.etree.ElementTree as ET

import cv2
import numpy as np

from exemplar import _fill_region
from estrutura import _classes, _complete


def carregar_predios(osm, html, X0, Y0, PPU, shape):
    """Contornos dos prédios sem nome (os do campus) do arquivo .osm, em pixels da planta,
    usando a georreferência do site (constante GEO do index.html)."""
    M = eval(re.search(r"const GEO=\{M:(\[\[.*?\]\])", html).group(1))
    lat0 = float(re.search(r"lat0:(-?[\d.]+)", html).group(1))
    lon0 = float(re.search(r"lon0:(-?[\d.]+)", html).group(1))
    k = math.cos(lat0 * math.pi / 180) * 111320
    (a, b, c) = M
    det = a[0] * b[1] - b[0] * a[1]

    def px(lat, lon):
        mx = (lon - lon0) * k - c[0]
        my = (lat0 - lat) * 111320 - c[1]
        x, y = (mx * b[1] - b[0] * my) / det, (a[0] * my - a[1] * mx) / det
        return ((x - X0) * PPU, (y - Y0) * PPU)

    raiz = ET.parse(osm).getroot()
    nos = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in raiz.findall("node")}
    H, W = shape
    out = []
    for w in raiz.findall("way"):
        tags = {t.get("k"): t.get("v") for t in w.findall("tag")}
        if "building" not in tags or tags.get("name"):
            continue
        p = np.array([px(*nos[n.get("ref")]) for n in w.findall("nd") if n.get("ref") in nos], np.float32)
        if len(p) and (p[:, 0] >= 0).all() and (p[:, 0] < W).all() and (p[:, 1] >= 0).all() and (p[:, 1] < H).all():
            out.append(p)
    return out


def encaixar(img, poly, livre, raio=30, passo=2):
    """Desloca o contorno (px) até coincidir com a borda visível do desenho.
    livre: pixels que podem entrar na comparação (fora das manchas)."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mag = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    H, W = g.shape
    melhor = (-1.0, 0, 0)
    for dy in range(-raio, raio + 1, passo):
        for dx in range(-raio, raio + 1, passo):
            borda = np.zeros((H, W), np.uint8)
            cv2.polylines(borda, [np.round(poly + (dx, dy)).astype(np.int32)], True, 1, 3)
            sel = (borda > 0) & livre
            if sel.sum() < 50:
                continue
            sc = float(mag[sel].mean())
            if sc > melhor[0]:
                melhor = (sc, dx, dy)
    return melhor[1], melhor[2]


def preencher_osm(img, hole, outros, predios, patch=15, search=150, modo="vertical", tons=True):
    """img: recorte BGR; hole/outros: bool; predios: contornos (px, no recorte) já encaixados.
    modo: "vertical" (copia das mesmas colunas) ou "cross" (mesmas colunas ou mesmas linhas).
    tons: separa as faixas de tom dentro de cada telhado. Retorna (imagem, mapa de áreas)."""
    H, W = hole.shape
    dentro = np.zeros((H, W), np.int32)
    for j, poly in enumerate(predios, start=1):
        cv2.fillPoly(dentro, [np.round(poly).astype(np.int32)], j)
    known = ~hole & ~outros
    fora_known = known & (dentro == 0)
    L = np.full((H, W), 255, np.int32)
    # entorno: classes de cor/textura, prolongadas para dentro do buraco
    lab = _classes(img, fora_known).astype(np.int32)
    lab[outros | (dentro > 0)] = 255
    hole_fora = hole & (dentro == 0)
    if hole_fora.any() and (lab[fora_known] != 255).any():
        comp = _complete(lab.astype(np.uint8), hole_fora, outros | (dentro > 0)).astype(np.int32)
        lab[hole_fora] = comp[hole_fora]
    L[dentro == 0] = lab[dentro == 0]
    # telhados: um rótulo por prédio, ou por faixa de tom dentro dele
    for j in range(1, len(predios) + 1):
        dj = dentro == j
        kj = known & dj
        if not tons or kj.sum() < 300:
            L[dj] = 100 + 10 * j
            continue
        lj = _classes(img, kj, k=3).astype(np.int32)
        lj[~dj | outros] = 255
        hj = hole & dj
        if hj.any():
            comp = _complete(lj.astype(np.uint8), hj, (~dj) | outros).astype(np.int32)
            lj[hj] = comp[hj]
        L[dj] = 100 + 10 * j + lj[dj]
    out = img.copy()
    pend = hole.copy()
    ids, cnt = np.unique(L[hole], return_counts=True)
    for i, _n in sorted(zip(ids, cnt), key=lambda t: (t[0] < 100, -t[1])):  # telhados primeiro
        part = hole & (L == i)
        if not part.any():
            continue
        forbid = known & (L != i)
        ignore = (pend & ~part) | outros
        out = _fill_region(out, (part * 255).astype(np.uint8), patch, search, forbid, modo, ignore)
        pend &= ~part
        known = known | part
    resto = hole & np.all(out == img, axis=2)
    if resto.any():
        out = cv2.inpaint(out, (resto * 255).astype(np.uint8), 13, cv2.INPAINT_TELEA)
    return out, L
