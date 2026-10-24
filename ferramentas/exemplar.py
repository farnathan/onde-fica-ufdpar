"""Inpainting por exemplares (Criminisi et al., 2004), recortado por região.

Em vez de espalhar a cor da borda (TELEA/NS, que borram), copia pedaços reais da
própria imagem que combinam com o entorno: telhas, cumeeira e grama continuam com
textura. Cada região apagada é tratada num recorte com margem, para ser rápido.
"""
import cv2
import numpy as np


def _fill_region(img, mask, patch=13, search=None, forbid=None, mode="cross", ignore=None):
    """img: BGR uint8 (recorte). mask: uint8, 255 = preencher. Retorna img preenchida."""
    h = patch // 2
    img = img.astype(np.float32).copy()
    unk = mask > 0
    H, W = unk.shape
    conf = (~unk).astype(np.float32)

    gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    box = np.ones((patch, patch), np.float32)

    while unk.any():
        # frente de preenchimento: pixels desconhecidos vizinhos de conhecidos
        known_u8 = (~unk).astype(np.uint8)
        front = unk & (cv2.dilate(known_u8, np.ones((3, 3), np.uint8)) > 0)
        ys, xs = np.nonzero(front)

        # termo de confiança (média do patch)
        c_sum = cv2.filter2D(conf, -1, box, borderType=cv2.BORDER_CONSTANT) / (patch * patch)
        # termo de dados: isófota x normal da frente
        g = gray.copy()
        g[unk] = 0
        gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
        gx[unk] = 0
        gy[unk] = 0
        # gradiente máximo na vizinhança (evita borda falsa do buraco)
        gxm = cv2.dilate(np.abs(gx), np.ones((3, 3), np.uint8))
        gym = cv2.dilate(np.abs(gy), np.ones((3, 3), np.uint8))
        mf = unk.astype(np.float32)
        nx = cv2.Sobel(mf, cv2.CV_32F, 1, 0, ksize=3)
        ny = cv2.Sobel(mf, cv2.CV_32F, 0, 1, ksize=3)
        nn = np.sqrt(nx ** 2 + ny ** 2) + 1e-6
        data = np.abs(-gym * nx / nn + gxm * ny / nn) / 255.0 + 0.001

        pr = c_sum[ys, xs] * data[ys, xs]
        i = int(np.argmax(pr))
        py, px = int(ys[i]), int(xs[i])

        y0, y1 = max(py - h, 0), min(py + h + 1, H)
        x0, x1 = max(px - h, 0), min(px + h + 1, W)
        tpl = img[y0:y1, x0:x1]
        tk = (~unk[y0:y1, x0:x1]).astype(np.float32)
        if ignore is not None:
            tk = tk * (~ignore[y0:y1, x0:x1])
        th, tw = tpl.shape[:2]

        # janelas de busca: "free" = quadrado; "vertical" = mesmas colunas;
        # "cross" = mesmas colunas OU mesmas linhas (preserva linhas retas nos dois sentidos)
        def janelas(sr):
            if not sr:
                return [(0, H, 0, W)]
            vy = (max(py - sr, 0), min(py + sr + 1, H))
            vx = (max(px - sr, 0), min(px + sr + 1, W))
            if mode == "vertical":
                return [(vy[0], vy[1], x0, x1)]
            if mode == "cross":
                return [(vy[0], vy[1], x0, x1), (y0, y1, vx[0], vx[1])]
            return [(vy[0], vy[1], vx[0], vx[1])]

        best = None
        m3 = np.dstack([tk] * 3)
        for sy0, sy1, sx0, sx1 in janelas(search):
            src = img[sy0:sy1, sx0:sx1]
            if src.shape[0] < th or src.shape[1] < tw:
                continue
            unk_src = unk[sy0:sy1, sx0:sx1].astype(np.float32)
            if forbid is not None:
                unk_src = np.maximum(unk_src, forbid[sy0:sy1, sx0:sx1].astype(np.float32))
            if ignore is not None:
                unk_src = np.maximum(unk_src, ignore[sy0:sy1, sx0:sx1].astype(np.float32))
            bad = cv2.filter2D(unk_src, -1, np.ones((th, tw), np.float32),
                               anchor=(0, 0), borderType=cv2.BORDER_CONSTANT)
            bad = bad[: src.shape[0] - th + 1, : src.shape[1] - tw + 1] > 0
            ssd = cv2.matchTemplate(src, tpl, cv2.TM_SQDIFF, mask=m3)
            ssd[bad] = np.inf
            ssd[~np.isfinite(ssd)] = np.inf
            if not np.isfinite(ssd).any():
                continue
            by, bx = np.unravel_index(int(np.argmin(ssd)), ssd.shape)
            if best is None or ssd[by, bx] < best[0]:
                best = (ssd[by, bx], src[by:by + th, bx:bx + tw])
        if best is None:
            if search:
                search = None  # sem origem válida: amplia para o recorte todo
                continue
            break
        patch_src = best[1]

        fill = unk[y0:y1, x0:x1]
        img[y0:y1, x0:x1][fill] = patch_src[fill]
        gray[y0:y1, x0:x1][fill] = cv2.cvtColor(
            patch_src.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)[fill]
        conf[y0:y1, x0:x1][fill] = c_sum[py, px]
        unk[y0:y1, x0:x1][fill] = False

    return np.clip(img, 0, 255).astype(np.uint8)


def inpaint_exemplar(img, mask, patch=15, margin=150, search=150, mode="cross"):
    """Aplica _fill_region em cada região conectada da máscara, num recorte com margem."""
    out = img.copy()
    n, lab, st, _ = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8))
    H, W = mask.shape
    for i in range(1, n):
        x, y, w, h, _a = st[i]
        x0, y0 = max(x - margin, 0), max(y - margin, 0)
        x1, y1 = min(x + w + margin, W), min(y + h + margin, H)
        sub_mask = ((lab[y0:y1, x0:x1] == i) * 255).astype(np.uint8)
        other = (lab[y0:y1, x0:x1] > i)  # regiões ainda não preenchidas
        out[y0:y1, x0:x1] = _fill_region(out[y0:y1, x0:x1], sub_mask, patch, search, other, mode)
    return out
