# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift/. The authors are listed in prov/P9C537.jsonl.

"""A compact SIFT after Lowe (2004), for small images and for teaching.

Model: one channel, values in [0, 1] taken as given (no gamma step), pixel
(x, y) is img[y][x] with its center at integer coordinates, clamp border
rule for the blur. Octave o uses every 2^o th pixel, so octave coordinate x
is image coordinate x 2^o. The input image is not doubled here.

Parameters from the paper: s = 3 scales per octave, sigma0 = 1.6, an assumed
input blur of 0.5, contrast threshold 0.03, edge ratio r = 10, 36 orientation
bins with a window of 1.5 sigma, peaks within 80% of the highest, a 4 x 4 x 8
descriptor clipped at 0.2, and the ratio test 0.8. Implementation choices
that the paper leaves open: a descriptor cell width of 3 sigma, linear
spreading of each sample over two orientation bins, and a pre-filter
|D| > 0.5 * contrast / s before the quadratic fit.
"""

import math

TWO_PI = 2 * math.pi


# ---------------------------------------------------------------- blur and pyramid

def gaussian_kernel(sigma):
    r = max(1, int(math.ceil(3 * sigma)))
    k = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-r, r + 1)]
    s = sum(k)
    return [v / s for v in k]


def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def blur(img, sigma):
    """Separable Gaussian blur with the clamp border rule."""
    if sigma <= 0:
        return [list(r) for r in img]
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    h, w = len(img), len(img[0])
    tmp = [[sum(k[i] * row[_clamp(x + i - r, 0, w - 1)] for i in range(len(k))) for x in range(w)]
           for row in img]
    return [[sum(k[j] * tmp[_clamp(y + j - r, 0, h - 1)][x] for j in range(len(k))) for x in range(w)]
            for y in range(h)]


def downsample(img):
    """Every second pixel in each direction: out[y][x] = img[2 y][2 x]."""
    return [row[::2] for row in img[::2]]


def build_pyramid(img, n_octaves=2, s=3, sigma0=1.6, input_blur=0.5):
    """Return (gauss, dog): s + 3 Gaussian images and s + 2 differences per octave."""
    k = 2 ** (1.0 / s)
    sig = [sigma0 * k ** i for i in range(s + 3)]
    base = blur(img, math.sqrt(sigma0 * sigma0 - input_blur * input_blur))
    gauss, dog = [], []
    for o in range(n_octaves):
        if o > 0:
            base = downsample(gauss[-1][s])
        if len(base) < 3 or len(base[0]) < 3:
            break
        levels = [base]
        for i in range(1, s + 3):
            levels.append(blur(levels[-1], math.sqrt(sig[i] ** 2 - sig[i - 1] ** 2)))  # @line L1
        gauss.append(levels)
        dog.append([[[b - a for a, b in zip(ra, rb)] for ra, rb in zip(levels[i], levels[i + 1])]  # @line L2
                    for i in range(s + 2)])
    return gauss, dog


# ---------------------------------------------------------------- extrema and localization

def is_extremum(d, i, y, x):
    """True if d[i][y][x] is greater than all 26 neighbours or less than all 26."""
    v = d[i][y][x]
    bigger = smaller = True
    for di in (-1, 0, 1):
        plane = d[i + di]
        for dy in (-1, 0, 1):
            row = plane[y + dy]
            for dx in (-1, 0, 1):
                if di == 0 and dy == 0 and dx == 0:
                    continue
                u = row[x + dx]
                if u >= v:
                    bigger = False
                if u <= v:
                    smaller = False
                if not bigger and not smaller:
                    return False
    return True


def scan_extrema(d, min_abs=0.0):
    """All (i, y, x) with 1 <= i <= len(d) - 2, away from the border, that are 26-neighbour extrema."""
    out = []
    h, w = len(d[0]), len(d[0][0])
    for i in range(1, len(d) - 1):  # @line L3
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if abs(d[i][y][x]) > min_abs and is_extremum(d, i, y, x):  # @line L4
                    out.append((i, y, x))
    return out


def derivatives(d, i, y, x):
    """Central-difference gradient g and Hessian H of d in (x, y, i). Exact on a quadratic."""
    c = d[i][y][x]
    dx = (d[i][y][x + 1] - d[i][y][x - 1]) / 2
    dy = (d[i][y + 1][x] - d[i][y - 1][x]) / 2
    ds = (d[i + 1][y][x] - d[i - 1][y][x]) / 2
    dxx = d[i][y][x + 1] - 2 * c + d[i][y][x - 1]
    dyy = d[i][y + 1][x] - 2 * c + d[i][y - 1][x]
    dss = d[i + 1][y][x] - 2 * c + d[i - 1][y][x]
    dxy = (d[i][y + 1][x + 1] - d[i][y + 1][x - 1] - d[i][y - 1][x + 1] + d[i][y - 1][x - 1]) / 4
    dxs = (d[i + 1][y][x + 1] - d[i + 1][y][x - 1] - d[i - 1][y][x + 1] + d[i - 1][y][x - 1]) / 4
    dys = (d[i + 1][y + 1][x] - d[i + 1][y - 1][x] - d[i - 1][y + 1][x] + d[i - 1][y - 1][x]) / 4
    return [dx, dy, ds], [[dxx, dxy, dxs], [dxy, dyy, dys], [dxs, dys, dss]]


def _det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def solve3(m, b):
    """Solve m z = b by Cramer's rule. Exact with Fraction input. None if m is singular."""
    det = _det3(m)
    if det == 0:
        return None
    out = []
    for col in range(3):
        mc = [[b[r] if c == col else m[r][c] for c in range(3)] for r in range(3)]
        out.append(_det3(mc) / det)
    return out


def quadratic_offset(d, i, y, x):
    """Return (offset, value): offset = -H^-1 g and D(offset) = D + g . offset / 2. None if H is singular."""
    g, hm = derivatives(d, i, y, x)
    z = solve3(hm, [-g[0], -g[1], -g[2]])
    if z is None:
        return None
    return z, d[i][y][x] + (g[0] * z[0] + g[1] * z[1] + g[2] * z[2]) / 2


def passes_edge_test(dxx, dyy, dxy, r=10):
    """Lowe's test tr^2 / det < (r + 1)^2 / r, written without division. Rejects det <= 0."""
    tr = dxx + dyy
    det = dxx * dyy - dxy * dxy
    return det > 0 and tr * tr * r < (r + 1) ** 2 * det


def _step(v):
    return 1 if v > 0.5 else -1 if v < -0.5 else 0


def localize(d, i, y, x, contrast=0.03, edge_r=10, max_moves=5):
    """Refine an extremum. Return (i, y, x, offset, value) or None if it is rejected."""
    h, w = len(d[0]), len(d[0][0])
    for _ in range(max_moves):
        res = quadratic_offset(d, i, y, x)  # @line L5
        if res is None:
            return None
        z, val = res
        sx, sy, si = _step(z[0]), _step(z[1]), _step(z[2])
        if sx == sy == si == 0:
            break
        x, y, i = x + sx, y + sy, i + si
        if not (1 <= x <= w - 2 and 1 <= y <= h - 2 and 1 <= i <= len(d) - 2):
            return None
    else:
        return None
    if abs(val) < contrast:  # @line L6
        return None
    _, hm = derivatives(d, i, y, x)
    if not passes_edge_test(hm[0][0], hm[1][1], hm[0][1], edge_r):
        return None
    return i, y, x, z, val


# ---------------------------------------------------------------- orientation and descriptor

def _grad(img, x, y):
    gx = img[y][x + 1] - img[y][x - 1]
    gy = img[y + 1][x] - img[y - 1][x]
    return math.hypot(gx, gy), math.atan2(gy, gx) % TWO_PI


def orientation_histogram(img, x, y, sigma, bins=36):
    """Gradient magnitudes weighted by a Gaussian with 1.5 sigma, spread linearly over two bins."""
    hist = [0.0] * bins
    sw = 1.5 * sigma
    rad = int(round(3 * sw))
    h, w = len(img), len(img[0])
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            px, py = x + dx, y + dy
            if not (1 <= px <= w - 2 and 1 <= py <= h - 2):
                continue
            m, a = _grad(img, px, py)
            wt = m * math.exp(-(dx * dx + dy * dy) / (2 * sw * sw))
            b = a * bins / TWO_PI - 0.5
            b0 = math.floor(b)
            f = b - b0
            hist[b0 % bins] += wt * (1 - f)
            hist[(b0 + 1) % bins] += wt * f
    return hist


def dominant_orientations(hist, ratio=0.8):
    """Angles of the local peaks within ratio of the highest peak, refined by a parabola through 3 bins."""
    n = len(hist)
    top = max(hist)
    out = []
    if top <= 0:
        return out
    for b in range(n):
        l, c, r = hist[(b - 1) % n], hist[b], hist[(b + 1) % n]
        if c > l and c > r and c >= ratio * top:
            off = 0.5 * (l - r) / (l - 2 * c + r)
            out.append(((b + 0.5 + off) * TWO_PI / n) % TWO_PI)
    return out


def descriptor(img, x, y, xf, yf, sigma, theta, width=4, obins=8, cell=3.0, clip=0.2):
    """The 4 x 4 x 8 descriptor of the keypoint at (xf, yf), sampled around the pixel (x, y)."""
    cw = cell * sigma
    rad = int(round(cw * math.sqrt(2) * (width + 1) / 2))
    h, w = len(img), len(img[0])
    ct, st = math.cos(theta), math.sin(theta)
    hist = [0.0] * (width * width * obins)
    half = width / 2
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            px, py = x + dx, y + dy
            if not (1 <= px <= w - 2 and 1 <= py <= h - 2):
                continue
            ox, oy = px - xf, py - yf
            u = (ct * ox + st * oy) / cw
            v = (-st * ox + ct * oy) / cw
            cu, cv = u + half - 0.5, v + half - 0.5
            if not (-1 < cu < width and -1 < cv < width):
                continue
            m, a = _grad(img, px, py)
            wt = m * math.exp(-(u * u + v * v) / (2 * half * half))
            ob = ((a - theta) % TWO_PI) * obins / TWO_PI
            iu, iv, io = math.floor(cu), math.floor(cv), math.floor(ob)
            fu, fv, fo = cu - iu, cv - iv, ob - io
            for jv, wv in ((iv, 1 - fv), (iv + 1, fv)):
                if not 0 <= jv < width:
                    continue
                for ju, wu in ((iu, 1 - fu), (iu + 1, fu)):
                    if not 0 <= ju < width:
                        continue
                    for jo, wo in ((io, 1 - fo), (io + 1, fo)):
                        hist[(jv * width + ju) * obins + jo % obins] += wt * wv * wu * wo
    return normalize_clip(hist, clip)  # @line L10


def normalize_clip(vec, clip=0.2):
    """Scale to unit length, cap each entry at clip, and scale to unit length again."""
    n = math.sqrt(sum(v * v for v in vec))
    if n == 0:
        return vec
    vec = [min(v / n, clip) for v in vec]
    n = math.sqrt(sum(v * v for v in vec))
    return [v / n for v in vec]


# ---------------------------------------------------------------- full pipeline and matching

def detect_and_describe(img, n_octaves=2, s=3, sigma0=1.6, contrast=0.03, edge_r=10):
    """Return keypoints as dicts with x, y, sigma (image units), theta and desc."""
    gauss, dog = build_pyramid(img, n_octaves, s, sigma0)
    kps = []
    for o, d in enumerate(dog):
        scale = 2 ** o
        for i, y, x in scan_extrema(d, 0.5 * contrast / s):
            res = localize(d, i, y, x, contrast, edge_r)
            if res is None:
                continue
            i, y, x, z, _ = res
            sig = sigma0 * 2 ** ((i + z[2]) / s)
            xf, yf = x + z[0], y + z[1]
            g = gauss[o][i]
            hist = orientation_histogram(g, x, y, sig)  # @line L7
            for th in dominant_orientations(hist):  # @line L8
                desc = descriptor(g, x, y, xf, yf, sig, th)  # @line L9
                kps.append({"x": xf * scale, "y": yf * scale, "sigma": sig * scale, "theta": th, "desc": desc})
    return kps


def match(desc_a, desc_b, ratio=0.8):
    """Pairs (i, j) where b[j] is the nearest neighbour of a[i] and d1 < ratio d2.

    Exact search with early abandoning: a partial sum stops once it passes the
    second-best squared distance so far.
    """
    out = []
    r2 = ratio * ratio
    for i, a in enumerate(desc_a):  # @line L11
        best, second, arg = math.inf, math.inf, -1
        for j, b in enumerate(desc_b):  # @line L12
            acc = 0.0
            for p, q in zip(a, b):
                acc += (p - q) * (p - q)
                if acc >= second:
                    break
            if acc < best:
                best, second, arg = acc, best, j
            elif acc < second:
                second = acc
        if arg >= 0 and second < math.inf and best < r2 * second:  # @line L13
            out.append((i, arg))
    return out
