# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fft-ocean-synthesis/. The authors are listed in prov/6YE8FD.jsonl.
"""FFT ocean synthesis in the style of Tessendorf (2001), on an N by N grid.

The patch has the side length L (m) and is periodic. The wave vector of the
index (n, m) is k = (2 pi n' / L, 2 pi m' / L), where n' = n for n < N/2 and
n' = n - N otherwise (the order of the FFT). The height is

    h(x, t) = sum_k H(k, t) exp(i k . x),
    H(k, t) = h0(k) exp(i w(k) t) + conj(h0(-k)) exp(-i w(k) t),

with the deep water dispersion w(k) = (g |k|)^(1/2) and the initial
amplitudes h0(k) = (xi_r + i xi_i) (P(k) / 2)^(1/2) from two standard normal
numbers and the Phillips spectrum P. Because H(-k) = conj(H(k)), the height is
real. The sum has no factor 1/N^2, as in the notes of Tessendorf.

This file sets h0 to 0 on the Nyquist row and column (n = N/2 or m = N/2),
so that the choppy displacement is real too. This is a choice of this file.
"""

import cmath
import math

G = 9.81


def fft(a, inverse=False):
    """The radix-2 DFT of a list of complex numbers whose length is a power of 2.

    Forward: A_k = sum_n a_n exp(-2 pi i n k / N). Inverse: the same with
    exp(+2 pi i n k / N), with no factor 1/N. Returns a new list.
    """
    n = len(a)
    if n & (n - 1):
        raise ValueError("the length must be a power of 2")
    out = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    sign = 1.0 if inverse else -1.0
    size = 2
    while size <= n:
        w_step = cmath.exp(sign * 2j * math.pi / size)
        half = size // 2
        for start in range(0, n, size):
            w = 1.0 + 0.0j
            for k in range(start, start + half):
                t = w * out[k + half]
                out[k + half] = out[k] - t
                out[k] = out[k] + t
                w *= w_step
        size *= 2
    return out


def fft2(grid, inverse=False):
    """The 2D DFT of an N by N list of lists, by 1D transforms of the rows and then of the columns."""
    rows = [fft(row, inverse) for row in grid]
    cols = [fft([rows[i][j] for i in range(len(rows))], inverse) for j in range(len(rows[0]))]
    return [[cols[j][i] for j in range(len(cols))] for i in range(len(rows))]


def wave_index(n, size):
    """The signed index n' of the FFT order."""
    return n if n < size // 2 else n - size


def wave_vector(n, m, size, length):
    return (2.0 * math.pi * wave_index(n, size) / length, 2.0 * math.pi * wave_index(m, size) / length)


def dispersion(k, g=G, depth=None):
    """The angular frequency w of a wave with the wave number k: (g k)^(1/2) in deep water, (g k tanh(k d))^(1/2) at depth d."""
    if depth is None:
        return math.sqrt(g * k)
    return math.sqrt(g * k * math.tanh(k * depth))


def phillips(kx, ky, amplitude, wind, speed, g=G, small=0.0):
    """The Phillips spectrum A exp(-1 / (k L)^2) / k^4 |k_hat . w_hat|^2, with L = V^2 / g.

    wind is the wind direction (any length), speed the wind speed V (m/s).
    small > 0 multiplies by exp(-k^2 small^2) to remove waves much shorter than small.
    P(0) = 0.
    """
    k2 = kx * kx + ky * ky
    if k2 == 0.0:
        return 0.0
    big_l = speed * speed / g
    wn = math.hypot(wind[0], wind[1])
    cos = (kx * wind[0] + ky * wind[1]) / (math.sqrt(k2) * wn)
    return amplitude * math.exp(-1.0 / (k2 * big_l * big_l)) / (k2 * k2) * cos * cos * math.exp(-k2 * small * small)


def initial_amplitudes(rng, size, length, amplitude, wind, speed, g=G, small=0.0):
    """h0(k) = (xi_r + i xi_i) (P(k) / 2)^(1/2) for each index, with standard normal xi from rng.gauss."""
    h0 = [[0j] * size for _ in range(size)]
    for n in range(size):
        for m in range(size):
            xr, xi = rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)
            if n == size // 2 or m == size // 2:
                continue
            kx, ky = wave_vector(n, m, size, length)
            p = phillips(kx, ky, amplitude, wind, speed, g, small)
            h0[n][m] = complex(xr, xi) * math.sqrt(p / 2.0)
    return h0


def spectrum_at(h0, size, length, t, g=G):
    """H(k, t) = h0(k) exp(i w t) + conj(h0(-k)) exp(-i w t) for each index."""
    out = [[0j] * size for _ in range(size)]
    for n in range(size):
        for m in range(size):
            kx, ky = wave_vector(n, m, size, length)
            w = dispersion(math.hypot(kx, ky), g)
            e = cmath.exp(1j * w * t)
            out[n][m] = h0[n][m] * e + h0[(-n) % size][(-m) % size].conjugate() * e.conjugate()
    return out


def height_field(h0, size, length, t, g=G):
    """The complex heights at the grid points x = (a L / N, b L / N). The imaginary part is 0 up to rounding."""
    spec = spectrum_at(h0, size, length, t, g)  # @line L3
    return fft2(spec, inverse=True)  # @line L4


def choppy_displacement(h0, size, length, t, lam=1.0, g=G):
    """The horizontal displacement D(x) = sum_k -i lam (k / |k|) H(k, t) exp(i k . x), as two complex grids."""
    spec = spectrum_at(h0, size, length, t, g)
    sx = [[0j] * size for _ in range(size)]
    sy = [[0j] * size for _ in range(size)]
    for n in range(size):
        for m in range(size):
            kx, ky = wave_vector(n, m, size, length)
            k = math.hypot(kx, ky)
            if k > 0.0:
                sx[n][m] = -1j * lam * kx / k * spec[n][m]
                sy[n][m] = -1j * lam * ky / k * spec[n][m]
    return fft2(sx, inverse=True), fft2(sy, inverse=True)  # @line L5


def synthesize(rng, size, length, amplitude, wind, speed, times, lam=1.0, g=G):
    """The ocean patch at each time in times: a list of (height, dx, dy) real grids."""
    h0 = initial_amplitudes(rng, size, length, amplitude, wind, speed, g)  # @line L1
    frames = []
    for t in times:  # @line L2
        h = height_field(h0, size, length, t, g)
        dx, dy = choppy_displacement(h0, size, length, t, lam, g)
        frames.append(([[z.real for z in row] for row in h], [[z.real for z in row] for row in dx],
                       [[z.real for z in row] for row in dy]))  # @line L6
    return frames
