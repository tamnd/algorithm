# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-back-projection-super-resolution/. The authors are listed in prov/KACAK6.jsonl.
"""Iterative back-projection (Irani-Peleg) super-resolution.

The high resolution (HR) unknown x is a signal of length n or an image of
n1 x n2 pixels. Frame k is y_k = D B W_k x: W_k is an integer shift of the HR
grid, (W_k x)_j = x_{(j + s_k) mod n}; B is periodic convolution with the PSF
h (center at index 0); D keeps every L-th sample, (D v)_j = v_{j L}. So a
frame has n / L samples (n1 / L x n2 / L for an image). The update is

    x <- x + (beta / K) sum_k W_k^T (p * U (y_k - D B W_k x)),

with U = D^T (zero fill) and p the back projection kernel. With p = mirror(h)
it is the Landweber iteration for the stacked operator A = (D B W_k)_k with
the step omega = beta / K. Works with float and with fractions.Fraction values.
"""


def _is_image(x):
    return bool(x) and isinstance(x[0], (list, tuple))


def _conv1(x, h):
    n = len(x)
    nz = [(j, v) for j, v in enumerate(h) if v != 0]
    return [sum(v * x[(i - j) % n] for j, v in nz) for i in range(n)]


def _conv2(x, h):
    n1, n2 = len(x), len(x[0])
    nz = [(p, q, h[p][q]) for p in range(len(h)) for q in range(len(h[0])) if h[p][q] != 0]
    return [[sum(v * x[(i - p) % n1][(j - q) % n2] for p, q, v in nz) for j in range(n2)] for i in range(n1)]


def blur(x, h):
    """The periodic convolution h * x (signal or image), kernel centered at index 0."""
    return _conv2(x, h) if _is_image(x) else _conv1(x, h)


def mirror(h):
    """The kernel h(-r), so that blur(., mirror(h)) is the adjoint of blur(., h) for real h."""
    if _is_image(h):
        n1, n2 = len(h), len(h[0])
        return [[h[(-i) % n1][(-j) % n2] for j in range(n2)] for i in range(n1)]
    n = len(h)
    return [h[(-j) % n] for j in range(n)]


def warp(x, s):
    """(W x)_j = x_{(j + s) mod n}; s is an int for a signal and a pair for an image."""
    if _is_image(x):
        n1, n2 = len(x), len(x[0])
        a, b = s
        return [[x[(i + a) % n1][(j + b) % n2] for j in range(n2)] for i in range(n1)]
    n = len(x)
    return [x[(j + s) % n] for j in range(n)]


def warp_adjoint(x, s):
    """W^T, the shift by -s."""
    if _is_image(x):
        return warp(x, (-s[0], -s[1]))
    return warp(x, -s)


def decimate(x, factor):
    """D: keep the samples with index j L (rows and columns i L, j L for an image)."""
    if _is_image(x):
        return [row[::factor] for row in x[::factor]]
    return x[::factor]


def upsample(y, factor):
    """U = D^T: put y_j at index j L and zeros elsewhere."""
    if _is_image(y):
        n2 = len(y[0]) * factor
        zero = 0 * y[0][0]
        out = []
        for row in y:
            full = [zero] * n2
            full[::factor] = row
            out.append(full)
            out.extend([zero] * n2 for _ in range(factor - 1))
        return out
    zero = 0 * y[0]
    out = [zero] * (len(y) * factor)
    out[::factor] = y
    return out


def forward(x, shift, h, factor):
    """Simulate one low resolution frame: D B W_k x."""
    return decimate(blur(warp(x, shift), h), factor)


def back_project(r, shift, p, factor):
    """W_k^T (p * U r): spread a low resolution residual back onto the HR grid."""
    return warp_adjoint(blur(upsample(r, factor), p), shift)


def _sub(a, b):
    if _is_image(a):
        return [[u - v for u, v in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [u - v for u, v in zip(a, b)]


def _axpy(x, c, g):
    if _is_image(x):
        return [[u + c * v for u, v in zip(ra, rb)] for ra, rb in zip(x, g)]
    return [u + c * v for u, v in zip(x, g)]


def _zeros_like(x):
    if _is_image(x):
        return [[0 * v for v in row] for row in x]
    return [0 * v for v in x]


def hr_zeros(frames, factor):
    """The zero HR signal or image for frames decimated by factor."""
    return _zeros_like(upsample(frames[0], factor))


def ibp(frames, shifts, h, factor, p=None, beta=1, iters=10, x0=None, callback=None):
    """Run iters steps of iterative back-projection.

    frames[k] is y_k and shifts[k] is s_k. p is the back projection kernel
    (default mirror(h), which gives Landweber). The step is beta / K.
    callback(t, x) is called after step t, if given. Returns the last x.
    """
    if p is None:
        p = mirror(h)
    big_k = len(frames)
    x = hr_zeros(frames, factor) if x0 is None else x0  # @line L1
    for t in range(iters):  # @line L2
        g = _zeros_like(x)  # @line L3
        for y, s in zip(frames, shifts):  # @line L4
            r = _sub(y, forward(x, s, h, factor))  # @line L5
            g = _axpy(g, 1, back_project(r, s, p, factor))  # @line L6
        x = _axpy(x, beta / big_k, g)  # @line L7
        if callback is not None:
            callback(t + 1, x)
    return x  # @line L8


def shift_and_add(frames, shifts, factor):
    """sum_k W_k^T U y_k divided by the number of frames that hit each HR pixel (0 where none)."""
    acc = hr_zeros(frames, factor)
    hits = hr_zeros(frames, factor)
    for y, s in zip(frames, shifts):
        acc = _axpy(acc, 1, warp_adjoint(upsample(y, factor), s))
        ones = [[1] * len(y[0]) for _ in y] if _is_image(y) else [1] * len(y)
        hits = _axpy(hits, 1, warp_adjoint(upsample(ones, factor), s))
    if _is_image(acc):
        return [[a / c if c else a for a, c in zip(ra, rc)] for ra, rc in zip(acc, hits)]
    return [a / c if c else a for a, c in zip(acc, hits)]


def residual_norm2(x, frames, shifts, h, factor):
    """sum_k ||y_k - D B W_k x||^2."""
    total = 0
    for y, s in zip(frames, shifts):
        r = _sub(y, forward(x, s, h, factor))
        vals = [v for row in r for v in row] if _is_image(r) else r
        total += sum(abs(v) ** 2 for v in vals)
    return total


def covers_all_residues(shifts, factor):
    """True when the shifts take every residue mod L (every pair of residues for an image)."""
    if shifts and isinstance(shifts[0], (list, tuple)):
        got = {(a % factor, b % factor) for a, b in shifts}
        return len(got) == factor * factor
    return len({s % factor for s in shifts}) == factor
