# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fractionally-spaced-equalizer/. The authors are listed in prov/SDKX4V.jsonl.

"""The MMSE fractionally spaced equalizer (FSE) at L_s samples per symbol.

The receiver samples at L_s samples per symbol (L_s = 2 on the page, a
T/2-spaced equalizer). The sampled pulse p[0..L_p-1] includes the transmit
filter, the channel and the sampling phase, and is normalized so that
sum |p|^2 = 1. The samples are y[m] = sum_k x[k] p[m - L_s k] + w[m], with
symbols of energy Es and noise CN(0, N0) on each sample. The equalizer has
N_f taps spaced T/L_s apart and gives one output per symbol:
z[k] = sum_{i=0}^{N_f-1} c[i] y[L_s k - i], an estimate of x[k - D].

The regressor u = (y[L_s k], ..., y[L_s k - N_f + 1]) is u = H s + w with
H[i][j] = p[L_s j - i] and s = (x[k], x[k-1], ..., x[k-Q+1]), where
Q = floor((L_p + N_f - 2) / L_s) + 1. The MMSE taps solve the Wiener-Hopf
equations R f = r with R = Es H H^H + N0 I and r = Es H e_D, and c = conj(f).
With L_s = 1 this is the symbol-spaced MMSE linear equalizer.
"""

import cbb


def fse_matrix(p: list[complex], ls: int, nf: int) -> list[list[complex]]:
    """The N_f by Q matrix H with H[i][j] = p[L_s j - i], so that u = H s + w."""
    if not p or ls < 1 or nf < 1:
        raise ValueError("need a pulse, L_s >= 1 and N_f >= 1")
    q = (len(p) + nf - 2) // ls + 1
    pp = lambda t: complex(p[t]) if 0 <= t < len(p) else 0j
    return [[pp(ls * j - i) for j in range(q)] for i in range(nf)]


def fse_mmse(p: list[complex], ls: int, nf: int, delay: int, n0: float, es: float = 1.0) -> tuple[list[complex], float]:
    """The N_f taps c, spaced T / L_s, that minimize E|z[k] - x[k - delay]|^2, and that minimum J."""
    if n0 < 0 or es <= 0:
        raise ValueError("need N0 >= 0 and Es > 0")
    if not p or ls < 1 or nf < 1:
        raise ValueError("need a pulse, L_s >= 1 and N_f >= 1")
    q = (len(p) + nf - 2) // ls + 1  # @line L1
    if not 0 <= delay < q:
        raise ValueError("need 0 <= delay < Q")
    hm = fse_matrix(p, ls, nf)  # @line L2
    big_r = [[es * sum(hm[i][t] * hm[k][t].conjugate() for t in range(q)) + (n0 if i == k else 0) for k in range(nf)] for i in range(nf)]  # @line L3
    r = [es * hm[i][delay] for i in range(nf)]  # @line L4
    try:
        f = cbb.solve(big_r, r)  # @line L5
    except ValueError:
        raise ValueError("R is singular: N0 = 0 and the phases of the pulse have a common zero, or N_f is too small") from None
    c = [v.conjugate() for v in f]  # @line L6
    j = es - cbb.dot(r, f).real  # @line L7
    return c, j  # @line L8


def mmse_by_delay(p: list[complex], ls: int, nf: int, n0: float, es: float = 1.0) -> list[float]:
    """J for every delay 0..Q-1 at once, as N0 Es times the diagonal of (Es H^H H + N0 I)^(-1); needs N0 > 0."""
    if n0 <= 0:
        raise ValueError("need N0 > 0")
    hm = fse_matrix(p, ls, nf)
    q = len(hm[0])
    m = [[es * sum(hm[t][i].conjugate() * hm[t][k] for t in range(nf)) + (n0 if i == k else 0) for k in range(q)] for i in range(q)]
    mi = cbb.inv(m)
    return [n0 * es * mi[d][d].real for d in range(q)]


def best_delay(p: list[complex], ls: int, nf: int, n0: float, es: float = 1.0) -> tuple[int, list[complex], float]:
    """The delay with the smallest J, with its taps and J."""
    js = mmse_by_delay(p, ls, nf, n0, es)
    d = min(range(len(js)), key=lambda t: js[t])
    c, j = fse_mmse(p, ls, nf, d, n0, es)
    return d, c, j


def mse(c: list[complex], p: list[complex], ls: int, delay: int, n0: float, es: float = 1.0) -> float:
    """E|z[k] - x[k - delay]|^2 for any taps c: Es ||H^T c - e_delay||^2 + N0 ||c||^2."""
    hm = fse_matrix(p, ls, len(c))
    g = [sum(hm[i][j] * c[i] for i in range(len(c))) for j in range(len(hm[0]))]
    if not 0 <= delay < len(g):
        raise ValueError("need 0 <= delay < Q")
    return es * sum(abs(v - (1 if j == delay else 0)) ** 2 for j, v in enumerate(g)) + n0 * cbb.norm2(c)


def received(x: list[complex], p: list[complex], ls: int) -> list[complex]:
    """The noiseless samples y[m] = sum_k x[k] p[m - L_s k], for m = 0 .. L_s (K - 1) + L_p - 1."""
    up = [0j] * (ls * (len(x) - 1) + 1)
    for k, v in enumerate(x):
        up[ls * k] = complex(v)
    return cbb.conv(up, p)


def equalize(c: list[complex], y: list[complex], ls: int, delay: int, count: int) -> list[complex]:
    """The outputs z[k] = sum_i c[i] y[L_s k - i] for k = delay .. delay + count - 1: the estimates of x[0 .. count - 1]."""
    out = []
    for k in range(delay, delay + count):
        acc = 0j
        for i, ci in enumerate(c):
            m = ls * k - i
            if 0 <= m < len(y):
                acc += ci * y[m]
        out.append(acc)
    return out
