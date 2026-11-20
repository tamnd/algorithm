# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimum-multiuser-detector/. The authors are listed in prov/H2AQFV.jsonl.

"""Verdu's optimum (jointly maximum likelihood) multiuser detector for CDMA.

Model (real, chip level, coherent BPSK). User k = 0, ..., K-1 sends the bits
b_k[0], ..., b_k[M-1] in {-1, +1} with the amplitude A_k > 0 and the
signature s_k of N chips with unit energy. User k starts tau_k chips late,
with 0 <= tau_k < N. The receiver sees

    y[n] = sum_k A_k sum_i b_k[i] s_k[n - i N - tau_k] + w[n],

with w[n] independent N(0, sigma^2). In the complex baseband model this is
the in-phase part, with sigma^2 = N0 / 2. With all delays 0 the model is
synchronous: y = S A b + w for one symbol interval.

The detector orders the K M bits by start time, so that each bit overlaps only
the K - 1 bits before it and the K - 1 bits after it. The log-likelihood is
then a sum of branch metrics that depend on the current bit and the K - 1
bits before it, and a Viterbi search over 2^(K-1) states finds the bit
sequence that maximizes it.
"""

import math


def bit_waveforms(sigs: list[list[float]], delays: list[int], m: int) -> tuple[list[tuple[int, int]], list[int], int]:
    """The bits in order of start time.

    Returns (order, starts, length): order[t] = (user k, symbol i) of the t-th
    bit, starts[t] = i N + tau_k its first chip, and the frame length in chips.
    """
    k_users = len(sigs)
    if k_users < 1 or m < 1:
        raise ValueError("need K >= 1 and M >= 1")
    n = len(sigs[0])
    if any(len(s) != n for s in sigs) or len(delays) != k_users:
        raise ValueError("signatures must have N chips each and one delay per user")
    if any(not 0 <= d < n for d in delays):
        raise ValueError("delays must lie in 0 .. N - 1")
    bits = sorted(((i * n + delays[k], k, i) for i in range(m) for k in range(k_users)))
    order = [(k, i) for _, k, i in bits]
    starts = [st for st, _, _ in bits]
    return order, starts, m * n + max(delays)


def received(sigs, delays, amps, b, sigma=0.0, rng=None) -> list[float]:
    """The chip samples y for the bits b[k][i], plus N(0, sigma^2) noise if rng is given."""
    m = len(b[0])
    order, starts, length = bit_waveforms(sigs, delays, m)
    n = len(sigs[0])
    y = [0.0] * length
    for (k, i), st in zip(order, starts):
        a = amps[k] * b[k][i]
        for c in range(n):
            y[st + c] += a * sigs[k][c]
    if rng is not None and sigma > 0.0:
        y = [v + rng.gauss(0.0, sigma) for v in y]
    return y


def _corr(sa: list[float], st_a: int, sb: list[float], st_b: int) -> float:
    """The inner product of two shifted signatures."""
    n = len(sa)
    lo, hi = max(st_a, st_b), min(st_a, st_b) + n
    return sum(sa[c - st_a] * sb[c - st_b] for c in range(lo, hi))


def optimum_detector(y: list[float], sigs: list[list[float]], delays: list[int], amps: list[float], m: int) -> list[list[int]]:
    """The bit sequences b[k][i] that maximize the likelihood of y (ties are measure zero)."""
    k_users = len(sigs)
    order, starts, length = bit_waveforms(sigs, delays, m)  # @line L1
    if len(y) != length:
        raise ValueError("y has the wrong length")
    total = len(order)
    amp = [amps[k] for k, _ in order]
    z = []
    rho = []
    for t, (k, _) in enumerate(order):  # @line L2
        st = starts[t]
        z.append(sum(sigs[k][c] * y[st + c] for c in range(len(sigs[k]))))
        rho.append([_corr(sigs[k], st, sigs[order[t - d][0]], starts[t - d]) for d in range(1, min(t, k_users - 1) + 1)])
    # A state holds the last min(t, K - 1) bits, most recent last.
    metric = {(): 0.0}  # @line L3
    survivor: dict[tuple[int, ...], list[int]] = {(): []}
    for t in range(total):  # @line L4
        new_metric: dict[tuple[int, ...], float] = {}
        new_surv: dict[tuple[int, ...], list[int]] = {}
        for state, lam in metric.items():  # @line L5
            interf = sum(amp[t - d] * state[-d] * rho[t][d - 1] for d in range(1, len(state) + 1))
            for bt in (1, -1):
                branch = 2.0 * amp[t] * bt * (z[t] - interf)  # @line L6
                nxt = (state + (bt,))[-(k_users - 1):] if k_users > 1 else ()
                val = lam + branch  # @line L7
                if nxt not in new_metric or val > new_metric[nxt]:
                    new_metric[nxt] = val
                    new_surv[nxt] = survivor[state] + [bt]
        metric, survivor = new_metric, new_surv  # @line L8
    best = max(metric, key=lambda s: metric[s])  # @line L9
    seq = survivor[best]
    out = [[0] * m for _ in range(k_users)]
    for (k, i), bt in zip(order, seq):
        out[k][i] = bt
    return out


def optimum_synchronous(y: list[float], sigs: list[list[float]], amps: list[float]) -> list[int]:
    """The synchronous case, one symbol interval: argmin over b of ||y - S A b||^2."""
    res = optimum_detector(y, sigs, [0] * len(sigs), amps, 1)
    return [r[0] for r in res]


def log_likelihood(y, sigs, delays, amps, b) -> float:
    """-||y - signal(b)||^2, the log-likelihood up to a constant and the factor 1 / (2 sigma^2)."""
    s = received(sigs, delays, amps, b)
    return -math.fsum((u - v) ** 2 for u, v in zip(y, s))
