# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-cross-correlation/. The authors are listed in prov/ZSW84C.jsonl.

"""Normalized cross-correlation (NCC) for template matching.

An image is a list of H rows, each a list of W numbers (int or Fraction).
Pixel (x, y) is img[y][x]. A template has q rows of p numbers. An offset
(u, v) puts the template corner on pixel (u, v); the valid offsets are
0 <= u <= W - p and 0 <= v <= H - q, so no border rule is needed.

For an offset, with n = p q, F = sum f, F2 = sum f^2, T = sum t,
T2 = sum t^2 and C = sum f t over the window, the exact integer parts are

    num = n C - F T,   vf = n F2 - F^2,   vt = n T2 - T^2,

and NCC = num / sqrt(vf vt). It is undefined when vf = 0 or vt = 0
(a flat window or a flat template); the score functions return None then.

The fast form of Lewis (1995) takes F and F2 from integral images of the
image and of its square, so only C depends on the template. C comes from a
direct sum (exact) or from an FFT correlation (floating point).
"""

import cmath
import math
from fractions import Fraction


def integral_image(img):
    """Return S with (H + 1) rows and (W + 1) columns, S[y][x] = sum of img[j][i] for j < y, i < x."""
    h = len(img)
    w = len(img[0]) if h else 0
    s = [[0] * (w + 1) for _ in range(h + 1)]
    for y in range(h):
        run = 0
        row = img[y]
        above = s[y]
        cur = s[y + 1]
        for x in range(w):
            run += row[x]
            cur[x + 1] = above[x + 1] + run
    return s


def rect_sum(s, x0, y0, x1, y1):
    """Sum of the pixels with x0 <= x < x1 and y0 <= y < y1, from an integral image."""
    return s[y1][x1] - s[y0][x1] - s[y1][x0] + s[y0][x0]


def _sizes(image, template):
    h, w = len(image), len(image[0])
    q, p = len(template), len(template[0])
    if p > w or q > h or p == 0 or q == 0:
        raise ValueError("the template must be non-empty and fit in the image")
    return w, h, p, q


def cross_term_direct(image, template):
    """C[v][u] = sum over the window of f(u + i, v + j) t(i, j). Exact, O(W H p q)."""
    w, h, p, q = _sizes(image, template)
    out = []
    for v in range(h - q + 1):
        row = []
        for u in range(w - p + 1):
            c = 0
            for j in range(q):
                irow = image[v + j]
                trow = template[j]
                for i in range(p):
                    c += irow[u + i] * trow[i]  # @line L7
            row.append(c)
        out.append(row)
    return out


def _fft(a, invert):
    """In-place iterative radix-2 FFT of a list of complex numbers whose length is a power of two."""
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    sign = 1 if invert else -1
    while length <= n:
        wl = cmath.exp(sign * 2j * math.pi / length)
        half = length // 2
        for start in range(0, n, length):
            wk = 1 + 0j
            for k in range(half):
                x = a[start + k]
                y = a[start + k + half] * wk
                a[start + k] = x + y
                a[start + k + half] = x - y
                wk *= wl
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n


def _fft2(grid, invert):
    rows = [list(r) for r in grid]
    for r in rows:
        _fft(r, invert)
    ncols = len(rows[0])
    for x in range(ncols):
        col = [rows[y][x] for y in range(len(rows))]
        _fft(col, invert)
        for y in range(len(rows)):
            rows[y][x] = col[y]
    return rows


def _next_pow2(n):
    m = 1
    while m < n:
        m <<= 1
    return m


def cross_term_fft(image, template):
    """The same table as cross_term_direct, by FFT correlation with zero padding. Floats, O(N log N)."""
    w, h, p, q = _sizes(image, template)
    pw, ph = _next_pow2(w), _next_pow2(h)
    a = [[complex(image[y][x]) if (y < h and x < w) else 0j for x in range(pw)] for y in range(ph)]
    b = [[complex(template[y][x]) if (y < q and x < p) else 0j for x in range(pw)] for y in range(ph)]
    fa = _fft2(a, False)
    fb = _fft2(b, False)
    prod = [[fa[y][x] * fb[y][x].conjugate() for x in range(pw)] for y in range(ph)]
    r = _fft2(prod, True)  # @line L11
    # Circular correlation: r[v][u] = sum f(u + i, v + j) t(i, j) with wrap; no wrap occurs
    # for valid offsets because the template support ends before the padding wraps.
    return [[r[v][u].real for u in range(w - p + 1)] for v in range(h - q + 1)]


def window_sums(image, p, q):
    """Return (F, F2): the sums of f and f^2 over each p by q window, from two integral images."""
    h, w = len(image), len(image[0])
    s1 = integral_image(image)
    s2 = integral_image([[val * val for val in row] for row in image])  # @line L3
    f1, f2 = [], []
    for v in range(h - q + 1):
        r1, r2 = [], []
        for u in range(w - p + 1):
            r1.append(rect_sum(s1, u, v, u + p, v + q))  # @line L6
            r2.append(rect_sum(s2, u, v, u + p, v + q))
        f1.append(r1)
        f2.append(r2)
    return f1, f2


def ncc_parts(image, template, cross=None):
    """Return a table of (num, vf, vt) per offset. Exact for int or Fraction input when cross is exact."""
    w, h, p, q = _sizes(image, template)
    n = p * q
    t1 = sum(sum(row) for row in template)
    t2 = sum(val * val for row in template for val in row)
    vt = n * t2 - t1 * t1  # @line L1
    if cross is None:
        cross = cross_term_direct(image, template)
    f1, f2 = window_sums(image, p, q)
    out = []
    for v in range(h - q + 1):  # @line L4
        row = []
        for u in range(w - p + 1):  # @line L5
            num = n * cross[v][u] - f1[v][u] * t1  # @line L8
            vf = n * f2[v][u] - f1[v][u] * f1[v][u]
            row.append((num, vf, vt))
        out.append(row)
    return out


def ncc_key(num, vf, vt):
    """An exact value with the same order as NCC: sign(num) num^2 / (vf vt). None if undefined."""
    if vt == 0:  # @line L2
        return None
    if vf == 0:  # @line L9: a flat window has no score
        return None
    return Fraction(num * abs(num)) / Fraction(vf * vt)


def ncc_map(image, template, use_fft=False):
    """NCC score per offset as floats in [-1, 1], or None where the window or template is flat."""
    cross = cross_term_fft(image, template) if use_fft else None
    parts = ncc_parts(image, template, cross)
    out = []
    for row in parts:
        r = []
        for num, vf, vt in row:
            if vf <= 0 or vt <= 0:
                # vf can come out slightly negative only with float input; exact input gives vf >= 0.
                r.append(None)
            else:
                val = float(num) / math.sqrt(float(vf) * float(vt))
                r.append(max(-1.0, min(1.0, val)))
        out.append(r)
    return out


def ssd_map(image, template):
    """Sum of squared differences per offset: F2 - 2 C + T2, with F2 from an integral image. Exact."""
    w, h, p, q = _sizes(image, template)
    t2 = sum(val * val for row in template for val in row)
    cross = cross_term_direct(image, template)
    _, f2 = window_sums(image, p, q)
    return [[f2[v][u] - 2 * cross[v][u] + t2 for u in range(w - p + 1)] for v in range(h - q + 1)]


def best_offset(table, larger_is_better=True):
    """The first offset (u, v) in row-major order with the best value; None entries are skipped."""
    best = None
    best_val = None
    for v, row in enumerate(table):
        for u, val in enumerate(row):
            if val is None:
                continue
            if best_val is None or (val > best_val if larger_is_better else val < best_val):
                best_val = val
                best = (u, v)
    return best


def match_ncc(image, template):
    """Offset of the exact NCC maximum, using ncc_key so that ties and rounding cannot change it."""
    parts = ncc_parts(image, template)
    keys = [[ncc_key(*cell) for cell in row] for row in parts]
    return best_offset(keys, True)  # @line L10


def match_ssd(image, template):
    """Offset of the SSD minimum."""
    return best_offset(ssd_map(image, template), False)
