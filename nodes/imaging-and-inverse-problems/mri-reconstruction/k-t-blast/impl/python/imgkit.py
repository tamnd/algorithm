# SPDX-License-Identifier: MIT
# Shared helper of the imaging and inverse problems pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small images and signals for the imaging and inverse problems pages.

Conventions:
- A signal is a list of numbers. An image is a list of rows, img[i][j], with
  row i from the top and column j from the left.
- An n x n image covers the square [-1, 1]^2. The center of pixel (i, j) is
  x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n, so y goes up.
- DFT: X_k = sum_j x_j exp(-2 pi i j k / n), unnormalized; the inverse has
  the factor 1 / n. Index k stands for frequency k for k < n / 2 and k - n
  otherwise. fftshift moves the zero frequency to position n // 2.
- Periodic convolution kernels are stored with their center at index 0
  (wrapped around), so a delta kernel gives the identity and no shift.
"""

import cmath
import math

# ------------------------------------------------------------------ images


def new_image(n1, n2, value=0.0):
    """An n1 x n2 image (n1 rows, n2 columns) filled with value."""
    return [[value] * n2 for _ in range(n1)]


def img_add(a, b):
    """The pixelwise sum a + b."""
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def img_scale(a, c):
    """The image c a."""
    return [[c * x for x in row] for row in a]


def img_dot(a, b):
    """<a, b> = sum conj(a_ij) b_ij."""
    return sum(x.conjugate() * y for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def img_norm(a):
    """The Euclidean (Frobenius) norm of an image."""
    return math.sqrt(sum(abs(x) ** 2 for row in a for x in row))


def flatten(img):
    """Row-major vector of an image."""
    return [x for row in img for x in row]


def unflatten(v, n1, n2):
    """The n1 x n2 image of a row-major vector."""
    return [list(v[i * n2:(i + 1) * n2]) for i in range(n1)]


# ------------------------------------------------------------------ DFT


def _is_pow2(n):
    return n > 0 and n & (n - 1) == 0


def _fft_pow2(x):
    """Iterative radix-2 FFT, unnormalized forward transform."""
    n = len(x)
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        half = size // 2
        tw = [cmath.exp(-2j * math.pi * k / size) for k in range(half)]
        for start in range(0, n, size):
            for k in range(half):
                u = a[start + k]
                v = a[start + k + half] * tw[k]
                a[start + k] = u + v
                a[start + k + half] = u - v
        size *= 2
    return a


def dft(x):
    """X_k = sum_j x_j exp(-2 pi i j k / n). Radix-2 FFT when n is a power of 2."""
    n = len(x)
    if n == 0:
        return []
    if _is_pow2(n):
        return _fft_pow2(x)
    w = [cmath.exp(-2j * math.pi * t / n) for t in range(n)]
    return [sum(x[j] * w[(j * k) % n] for j in range(n)) for k in range(n)]


def idft(xf):
    """x_j = (1/n) sum_k X_k exp(2 pi i j k / n)."""
    n = len(xf)
    if n == 0:
        return []
    y = dft([complex(v).conjugate() for v in xf])
    return [v.conjugate() / n for v in y]


def _rows_then_cols(img, f):
    rows = [f(row) for row in img]
    cols = [f(list(col)) for col in zip(*rows)]
    return [list(r) for r in zip(*cols)]


def dft2(img):
    """2D DFT: X_kl = sum_jq x_jq exp(-2 pi i (j k / n1 + q l / n2))."""
    return _rows_then_cols(img, dft)


def idft2(img):
    """Inverse 2D DFT, with the factor 1 / (n1 n2)."""
    return _rows_then_cols(img, idft)


def _shift1(x, s):
    return list(x[s:]) + list(x[:s])


def fftshift(x):
    """Move the zero frequency to position n // 2 (1D, or both axes of an image)."""
    if x and isinstance(x[0], (list, tuple)):
        rows = [fftshift(r) for r in x]
        return _shift1(rows, (len(rows) + 1) // 2)
    return _shift1(x, (len(x) + 1) // 2)


def ifftshift(x):
    """The inverse of fftshift (1D, or both axes of an image)."""
    if x and isinstance(x[0], (list, tuple)):
        rows = [ifftshift(r) for r in x]
        return _shift1(rows, len(rows) // 2)
    return _shift1(x, len(x) // 2)


def circ_conv(x, h):
    """Periodic convolution y_i = sum_j h_j x_{(i - j) mod n}, kernel centered at index 0."""
    n = len(x)
    nz = [(j, hj) for j, hj in enumerate(h) if hj != 0]
    return [sum(hj * x[(i - j) % n] for j, hj in nz) for i in range(n)]


def circ_conv2(img, h):
    """Periodic 2D convolution with the kernel h centered at index (0, 0)."""
    n1, n2 = len(img), len(img[0])
    nz = [(p, q, h[p][q]) for p in range(len(h)) for q in range(len(h[0])) if h[p][q] != 0]
    out = new_image(n1, n2)
    for i in range(n1):
        for j in range(n2):
            out[i][j] = sum(v * img[(i - p) % n1][(j - q) % n2] for p, q, v in nz)
    return out


# ------------------------------------------------------------------ phantoms


def pixel_centers(n):
    """(xs, ys): xs[j] = -1 + (2 j + 1) / n and ys[i] = 1 - (2 i + 1) / n."""
    xs = [-1.0 + (2 * j + 1) / n for j in range(n)]
    ys = [1.0 - (2 * i + 1) / n for i in range(n)]
    return xs, ys


# Rows: rho, A, B, x0, y0, phi (degrees). A is the semi-axis along the
# direction phi (counterclockwise from the x axis), B the other semi-axis.
# Geometry and densities of Shepp and Logan (1974), as reproduced in Kak and
# Slaney, Principles of Computerized Tomographic Imaging, Table 3.1. The value
# at the center (0, 0) is 2 - 0.98 = 1.02.
SHEPP_LOGAN = [
    (2.0, 0.92, 0.69, 0.0, 0.0, 90.0),
    (-0.98, 0.874, 0.6624, 0.0, -0.0184, 90.0),
    (-0.02, 0.31, 0.11, 0.22, 0.0, 72.0),
    (-0.02, 0.41, 0.16, -0.22, 0.0, 108.0),
    (0.01, 0.25, 0.21, 0.0, 0.35, 90.0),
    (0.01, 0.046, 0.046, 0.0, 0.1, 0.0),
    (0.01, 0.046, 0.046, 0.0, -0.1, 0.0),
    (0.01, 0.046, 0.023, -0.08, -0.605, 0.0),
    (0.01, 0.023, 0.023, 0.0, -0.605, 0.0),
    (0.01, 0.046, 0.023, 0.06, -0.605, 90.0),
]

# The same ellipses with the gray levels of Toft (1996), which give more
# contrast. The value at the center is 1 - 0.8 = 0.2.
MODIFIED_SHEPP_LOGAN = [
    (rho, a, b, x0, y0, phi)
    for rho, (_, a, b, x0, y0, phi) in zip(
        (1.0, -0.8, -0.2, -0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1), SHEPP_LOGAN
    )
]


def ellipse_value(x, y, table):
    """The phantom value at the point (x, y): the sum of rho over the ellipses that hold it."""
    total = 0.0
    for rho, a, b, x0, y0, phi in table:
        c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
        dx, dy = x - x0, y - y0
        u = dx * c + dy * s
        v = -dx * s + dy * c
        if (u / a) ** 2 + (v / b) ** 2 <= 1.0:
            total += rho
    return total


def ellipse_phantom(n, table):
    """The n x n image of an ellipse table, sampled at the pixel centers."""
    xs, ys = pixel_centers(n)
    return [[ellipse_value(x, y, table) for x in xs] for y in ys]


def disk_phantom(n, radius):
    """1 at pixel centers with x^2 + y^2 <= radius^2, 0 elsewhere."""
    xs, ys = pixel_centers(n)
    r2 = radius * radius
    return [[1.0 if x * x + y * y <= r2 else 0.0 for x in xs] for y in ys]


def spikes_1d(n, positions, amplitudes):
    """A signal of length n with the given amplitudes at the given positions."""
    out = [0.0] * n
    for p, a in zip(positions, amplitudes):
        out[p] += a
    return out


# ------------------------------------------------------------------ projector


def parallel_beam_matrix(n, angles, nbins):
    """Pixel-driven discrete Radon transform of an n x n image on [-1, 1]^2.

    Each pixel center (x, y) projects to s = x cos(theta) + y sin(theta). Its
    value times the pixel area over the bin width is split linearly between
    the two nearest bin centers. The bins cover [-sqrt(2), sqrt(2)]. Row
    a * nbins + b holds angle a and bin b; column i * n + j holds pixel (i, j).
    Returns the sparse rows, each a list of (column, weight) pairs.
    Pixel-driven projection has a ripple: with a bin width close to the pixel
    size, a disk projection is off by up to about 10 percent in some bins. A
    bin of about twice the pixel size (nbins = 23 for n = 32) keeps it near
    1 percent.
    """
    xs, ys = pixel_centers(n)
    smax = math.sqrt(2.0)
    width = 2.0 * smax / nbins
    scale = (2.0 / n) ** 2 / width
    rows = []
    for theta in angles:
        c, s = math.cos(theta), math.sin(theta)
        acc = [dict() for _ in range(nbins)]
        for i, y in enumerate(ys):
            for j, x in enumerate(xs):
                t = (x * c + y * s + smax) / width - 0.5
                b0 = math.floor(t)
                frac = t - b0
                col = i * n + j
                for b, w in ((b0, 1.0 - frac), (b0 + 1, frac)):
                    if 0 <= b < nbins and w > 0.0:
                        acc[b][col] = acc[b].get(col, 0.0) + w * scale
        rows.extend(sorted(d.items()) for d in acc)
    return rows


def sp_matvec(rows, x):
    """y = A x for sparse rows of (column, weight) pairs."""
    return [sum(w * x[c] for c, w in row) for row in rows]


def sp_rmatvec(rows, y, ncols):
    """x = A^H y for sparse rows of (column, weight) pairs and ncols columns."""
    out = [0.0] * ncols
    for row, yi in zip(rows, y):
        if yi == 0:
            continue
        for c, w in row:
            out[c] += w.conjugate() * yi
    return out


# ------------------------------------------------------------------ noise


def gauss_noise(rng, shape, sigma):
    """Independent N(0, sigma^2) values: a list for an int shape, an image for (n1, n2)."""
    if isinstance(shape, int):
        return [rng.gauss(0.0, sigma) for _ in range(shape)]
    n1, n2 = shape
    return [[rng.gauss(0.0, sigma) for _ in range(n2)] for _ in range(n1)]


def _poisson_small(rng, lam):
    """Knuth's product method, exact for a mean lam <= 30."""
    limit = math.exp(-lam)
    k, p = 0, rng.random()
    while p > limit:
        k += 1
        p *= rng.random()
    return k


def poisson_sample(rng, lam):
    """An exact Poisson(lam) sample: a sum of Knuth samples with means at most 30."""
    if lam < 0:
        raise ValueError("negative mean")
    total = 0
    while lam > 30.0:
        total += _poisson_small(rng, 30.0)
        lam -= 30.0
    if lam > 0.0:
        total += _poisson_small(rng, lam)
    return total
