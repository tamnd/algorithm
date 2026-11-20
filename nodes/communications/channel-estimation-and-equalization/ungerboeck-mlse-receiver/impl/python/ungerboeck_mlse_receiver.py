# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ungerboeck-mlse-receiver/. The authors are listed in prov/REAJPJ.jsonl.

"""Ungerboeck's maximum likelihood sequence receiver on matched filter samples.

The channel is y[k] = sum_{l=0}^{L-1} h[l] x[k-l] + w[k] for k = 0..N+L-2, with
x[k] = 0 outside 0..N-1 and w white CN(0, N0). The matched filter gives
z[k] = sum_l conj(h[l]) y[k+l], and R[l] = sum_i h[i+l] conj(h[i]) is the
channel autocorrelation. Then

    ||y||^2 - ||y - h * x||^2 = sum_k ( 2 Re(conj(x[k]) z[k]) - R[0] |x[k]|^2
                                         - 2 Re(conj(x[k]) sum_{l>=1} R[l] x[k-l]) ),

so maximizing the right side is maximum likelihood. Each term depends only on
x[k] and the L-1 symbols before it, so the Viterbi algorithm on the same trellis
as the Forney receiver finds the best sequence. No whitening filter is needed.
"""

import itertools


def matched_filter(y: list[complex], h: list[complex], n: int) -> list[complex]:
    """z[k] = sum_l conj(h[l]) y[k + l] for k = 0..n-1 (samples past the end of y count as 0)."""
    return [sum(complex(h[l]).conjugate() * y[k + l] for l in range(len(h)) if k + l < len(y)) for k in range(n)]


def autocorrelation(h: list[complex]) -> list[complex]:
    """R[l] = sum_i h[i + l] conj(h[i]) for l = 0..L-1."""
    return [sum(complex(h[i + l]) * complex(h[i]).conjugate() for i in range(len(h) - l)) for l in range(len(h))]


def ungerboeck_metric(z: list[complex], r: list[complex], x: list[complex]) -> float:
    """The sum of the Ungerboeck increments for the sequence x (x[k] = 0 for k < 0)."""
    total = 0.0
    for k, a in enumerate(x):
        a = complex(a)
        isi = sum(r[l] * x[k - l] for l in range(1, len(r)) if k - l >= 0)
        total += 2 * (a.conjugate() * z[k]).real - r[0].real * abs(a) ** 2 - 2 * (a.conjugate() * isi).real
    return total


def ungerboeck_mlse(y: list[complex], h: list[complex], alphabet: list[complex], tail: list[complex] | None = None) -> list[complex]:
    """The maximum likelihood sequence from the received block y of length N + L - 1.

    The block holds N symbols. If tail is given, its symbols are the last ones
    and are known, so the result has N - len(tail) symbols.
    """
    taps = len(h)
    mem = taps - 1
    m = len(alphabet)
    tail = list(tail) if tail is not None else []
    total = len(y) - mem
    n = total - len(tail)
    if total < 1 or n < 0:
        raise ValueError("y must hold N + L - 1 samples with N > len(tail)")
    index = {complex(a): i for i, a in enumerate(alphabet)}
    for v in tail:
        if complex(v) not in index:
            raise ValueError("tail symbols must be in the alphabet")
    z = matched_filter(y, h, total)  # @line L1
    r = autocorrelation(h)  # @line L2
    states = m ** mem
    inf = float("inf")
    metric = [-inf] * states
    metric[0] = 0.0  # @line L3
    back = []
    for k in range(total):  # @line L4
        new = [-inf] * states
        ptr = [(-1, -1)] * states
        choices = range(m) if k < n else [index[complex(tail[k - n])]]
        for s in range(states):
            if metric[s] == -inf:
                continue
            # the ISI term from the past symbols in the state; before x[0] they are 0
            isi = 0j
            for l in range(1, min(mem, k) + 1):
                isi += r[l] * alphabet[(s // m ** (l - 1)) % m]
            for i0 in choices:  # @line L5
                a = complex(alphabet[i0])
                lam = 2 * (a.conjugate() * z[k]).real - r[0].real * abs(a) ** 2 - 2 * (a.conjugate() * isi).real  # @line L6
                t = i0 + m * (s % (m ** (mem - 1))) if mem > 0 else 0
                if metric[s] + lam > new[t]:  # @line L7
                    new[t] = metric[s] + lam
                    ptr[t] = (s, i0)
        metric = new
        back.append(ptr)
    s = max(range(states), key=lambda q: metric[q])  # @line L8
    path = []
    for k in range(total - 1, -1, -1):
        prev, i0 = back[k][s]
        path.append(alphabet[i0])
        s = prev
    path.reverse()
    return path[:n]  # @line L9


def convolve(h: list[complex], x: list[complex]) -> list[complex]:
    """The full convolution h * x of length len(x) + len(h) - 1."""
    out = [0j] * (len(x) + len(h) - 1)
    for i, a in enumerate(x):
        for l, v in enumerate(h):
            out[i + l] += v * a
    return out


def brute_force(y: list[complex], h: list[complex], alphabet: list[complex], tail: list[complex] | None = None) -> list[complex]:
    """The sequence that minimizes ||y - h * x||^2, by trying all M^n sequences (for tests)."""
    tail = list(tail) if tail is not None else []
    n = len(y) - (len(h) - 1) - len(tail)
    best, arg = float("inf"), None
    for cand in itertools.product(alphabet, repeat=n):
        out = convolve(h, list(cand) + tail)
        v = sum(abs(a - b) ** 2 for a, b in zip(y, out))
        if v < best:
            best, arg = v, list(cand)
    return arg
