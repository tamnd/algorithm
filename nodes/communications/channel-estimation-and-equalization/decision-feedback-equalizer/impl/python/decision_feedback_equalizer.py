# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-feedback-equalizer/. The authors are listed in prov/K3EMZX.jsonl.

"""The finite-length MMSE decision feedback equalizer.

The channel is y[k] = sum_{l=0}^{L-1} h[l] x[k-l] + w[k] at one sample per
symbol, with independent symbols of mean zero and E|x|^2 = Es, and noise
CN(0, N0). The feedforward filter c has Nf taps and its output
z[k] = sum_i c[i] y[k-i] estimates x[k - D]. The feedback filter b has Nb taps
and subtracts sum_j b[j] xhat[k - D - j], j = 1..Nb, built from past decisions.

The design assumes correct past decisions (ideal feedback). With the regressor
u = H s + w, H[i][j] = h[j - i], the feedback removes the columns D + 1, ...,
D + Nb of H. The feedforward taps are the Wiener solution against the rest:
R f = r with R = Es H_K H_K^H + N0 I and r = Es H e_D, c = conj(f). The
feedback taps are the postcursors of the combined response g = c * h:
b[j] = g[D + j]. The minimum mean squared error is J = Es - r^H f.
"""

import cbb


def channel_matrix(h: list[complex], nf: int) -> list[list[complex]]:
    """The Nf by Nf + L - 1 matrix H with H[i][j] = h[j - i]."""
    taps = len(h)
    if taps < 1 or nf < 1:
        raise ValueError("need L >= 1 and Nf >= 1")
    return [[complex(h[j - i]) if 0 <= j - i < taps else 0j for j in range(nf + taps - 1)] for i in range(nf)]


def dfe_design(h: list[complex], nf: int, nb: int, delay: int, n0: float, es: float = 1.0) -> tuple[list[complex], list[complex], float]:
    """The MMSE-DFE taps (c, b) and the mean squared error J, under ideal feedback.

    b[0] is the tap of the decision xhat[k - D - 1], b[1] that of xhat[k - D - 2], and so on.
    """
    if n0 < 0 or es <= 0 or nb < 0:
        raise ValueError("need N0 >= 0, Es > 0 and Nb >= 0")
    if not 0 <= delay <= nf + len(h) - 2:
        raise ValueError("need 0 <= delay <= Nf + L - 2")
    hm = channel_matrix(h, nf)  # @line L1
    m = len(hm[0])
    keep = [j for j in range(m) if not delay < j <= delay + nb]  # @line L2
    big_r = [[es * sum(hm[i][t] * hm[k][t].conjugate() for t in keep) + (n0 if i == k else 0) for k in range(nf)] for i in range(nf)]  # @line L3
    r = [es * hm[i][delay] for i in range(nf)]  # @line L4
    try:
        f = cbb.solve(big_r, r)  # @line L5
    except ValueError:
        raise ValueError("R is singular: N0 = 0 and the kept columns of H do not span") from None
    c = [v.conjugate() for v in f]
    j = es - cbb.dot(r, f).real  # @line L6
    g = cbb.conv(c, [complex(v) for v in h])  # @line L7
    b = [g[delay + t] if delay + t < len(g) else 0j for t in range(1, nb + 1)]
    return c, b, j  # @line L8


def combined_response(c: list[complex], h: list[complex]) -> list[complex]:
    """g = c * h, the response from the symbols to the feedforward output."""
    return cbb.conv(c, [complex(v) for v in h])


def mse(c: list[complex], b: list[complex], h: list[complex], delay: int, n0: float, es: float = 1.0) -> float:
    """E|z[k] - feedback - x[k - D]|^2 for any taps, with ideal feedback.

    It is Es times the squared error of the combined response after the feedback,
    plus N0 ||c||^2.
    """
    g = combined_response(c, h)
    e = 0.0
    for t, v in enumerate(g):
        want = 1.0 if t == delay else 0.0
        if delay < t <= delay + len(b):
            v = v - b[t - delay - 1]
        e += abs(v - want) ** 2
    return es * e + n0 * cbb.norm2(c)


def nearest(q: complex, alphabet: list[complex]) -> complex:
    """The point of the alphabet closest to q."""
    return min(alphabet, key=lambda a: abs(q - a))


def dfe_run(c: list[complex], b: list[complex], delay: int, y: list[complex], count: int, alphabet: list[complex], gain: float = 1.0, known: list[complex] | None = None) -> list[complex]:
    """Equalize y and return the decisions on x[0], ..., x[count - 1].

    The symbols before x[0] are taken as 0. gain is the bias factor 1 - J / Es that
    the slicer divides by. If known is given, the feedback uses the true symbols
    (ideal feedback, a genie) instead of the decisions.
    """
    dec = []
    nb = len(b)
    for k in range(count):  # @line L9
        n = k + delay
        z = sum(c[i] * y[n - i] for i in range(len(c)) if 0 <= n - i < len(y))  # @line L10
        past = known if known is not None else dec
        fb = sum(b[t] * past[k - 1 - t] for t in range(nb) if k - 1 - t >= 0)
        q = z - fb  # @line L11
        dec.append(nearest(q / gain, alphabet))  # @line L12
    return dec  # @line L13


def soft_outputs(c: list[complex], b: list[complex], delay: int, y: list[complex], count: int, known: list[complex]) -> list[complex]:
    """The slicer inputs q[k] with ideal feedback from the known symbols."""
    out = []
    for k in range(count):
        n = k + delay
        z = sum(c[i] * y[n - i] for i in range(len(c)) if 0 <= n - i < len(y))
        fb = sum(b[t] * known[k - 1 - t] for t in range(len(b)) if k - 1 - t >= 0)
        out.append(z - fb)
    return out
