"""Preenchimento guiado por estrutura, para pinos antigos que cobriam uma borda
(telhado com grama, calçada, outro telhado).

1. Classifica o entorno em áreas de cor e textura parecidas (telhado cinza,
   telhado branco, grama, calçada...).
2. Reconstrói o mapa de áreas dentro do buraco prolongando as bordas retas:
   se em cima e embaixo é a mesma área, ela continua; se à esquerda e à direita
   é a mesma, idem; vale o par com o vão mais curto.
3. Preenche cada área só com textura da mesma área (cópia de exemplares).
"""
import cv2
import numpy as np

from exemplar import _fill_region


def _classes(img, known, k=5):
    sm = cv2.medianBlur(img, 15)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32)
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mu = cv2.blur(g, (15, 15))
    sd = np.sqrt(np.maximum(cv2.blur(g * g, (15, 15)) - mu * mu, 0))
    feat = np.dstack([lab, sd[..., None] * 2.0])
    X = feat[known].reshape(-1, 4)
    k = min(k, max(1, len(X) // 500))
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, lbl, cen = cv2.kmeans(X, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    out = np.full(known.shape, 255, np.uint8)
    out[known] = lbl.ravel().astype(np.uint8)
    # limpa salpicos: cada pixel conhecido fica com a classe mais comum da vizinhança
    votes = np.stack([cv2.blur((out == i).astype(np.float32), (9, 9)) for i in range(k)])
    clean = votes.argmax(0).astype(np.uint8)
    out[known] = clean[known]
    return out


def _complete(lab, hole, outros=None):
    """Prolonga as áreas para dentro do buraco nas 4 direções."""
    H, W = lab.shape
    INF = 10 ** 6

    def scan(a, h):
        n, m = a.shape
        last = np.full(m, 255, np.uint8)
        dist = np.full(m, INF, np.int32)
        L = np.zeros_like(a)
        D = np.zeros((n, m), np.int32)
        for r in range(n):
            known = ~h[r]
            last = np.where(known, a[r], last)
            dist = np.where(known, 0, dist + 1)
            L[r], D[r] = last, dist
        return L, D

    hole_s = hole if outros is None else (hole | outros)
    U, dU = scan(lab, hole_s)
    Dn, dD = scan(lab[::-1], hole_s[::-1]); Dn, dD = Dn[::-1], dD[::-1]
    Lt, dL = scan(lab.T, hole_s.T); Lt, dL = Lt.T, dL.T
    Rt, dR = scan(lab.T[::-1], hole_s.T[::-1]); Rt, dR = Rt[::-1].T, dR[::-1].T

    vert_ok = (U == Dn) & (U != 255)
    hor_ok = (Lt == Rt) & (Lt != 255)
    vspan, hspan = dU + dD, dL + dR
    res = lab.copy()
    # nenhum par concorda: fica com a área conhecida mais próxima
    cand = np.stack([U, Dn, Lt, Rt]); dist = np.stack([dU, dD, dL, dR])
    near = np.take_along_axis(cand, dist.argmin(0)[None], 0)[0]
    choice = near
    choice = np.where(hor_ok, Lt, choice)
    choice = np.where(vert_ok & (~hor_ok | (vspan <= hspan)), U, choice)
    vals = lab[~hole_s]
    moda = np.bincount(vals[vals != 255]).argmax() if (vals != 255).any() else 0
    choice = np.where(choice == 255, moda, choice)
    res[hole] = choice[hole]
    # alisa o mapa reconstruído só dentro do buraco
    k = int(res[res != 255].max()) + 1
    votes = np.stack([cv2.blur((res == i).astype(np.float32), (11, 11)) for i in range(k)])
    sm = votes.argmax(0).astype(np.uint8)
    res[hole] = sm[hole]
    return res


def preencher(img, hole, outros, patch=15, search=150):
    """img: recorte BGR com o pino; hole: bool (pino a apagar); outros: bool (outras
    áreas apagadas, que não servem de origem). Retorna (imagem, mapa de áreas)."""
    known = ~hole & ~outros
    lab = _classes(img, known)
    lab[outros] = 255
    lab = _complete(lab, hole, outros)
    out = img.copy()
    pend = hole.copy()
    ids, cnt = np.unique(lab[hole], return_counts=True)
    for i in ids[np.argsort(-cnt)]:
        part = hole & (lab == i)
        if not part.any():
            continue
        forbid = known & (lab != i)
        ignore = (pend & ~part) | outros
        out = _fill_region(out, (part * 255).astype(np.uint8), patch, search,
                           forbid, "vertical", ignore)
        pend &= ~part
        known = known | part
    resto = hole & np.all(out == img, axis=2)
    if resto.any():
        out = cv2.inpaint(out, (resto * 255).astype(np.uint8), 13, cv2.INPAINT_TELEA)
    return out, lab
