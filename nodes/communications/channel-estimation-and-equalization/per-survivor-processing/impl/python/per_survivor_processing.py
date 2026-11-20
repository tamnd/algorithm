# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/per-survivor-processing/. The authors are listed in prov/24BB6C.jsonl.

"""Per-survivor processing: a Viterbi equalizer with one LMS channel estimate per survivor.

The received samples are y[n] = sum_k f_n[k] x[n - k] + noise, with real symbols
and channel taps f_n that may drift slowly. The trellis state is the last
L - 1 symbols, most recent first. Every state keeps its own channel estimate.
A branch from state s with the new symbol a is scored with the estimate of s,
and after the add-compare-select step, the estimate of the winning branch is
updated by one LMS step that uses the symbols of that branch. So every
estimate is driven by the decisions of its own survivor, with no decision
delay. With the step size 0, the receiver is the plain Viterbi equalizer for
the channel f0.
"""

from itertools import product


def psp_viterbi(
    y: list[float],
    f0: list[float],
    step: float,
    alphabet: tuple[float, ...] = (-1.0, 1.0),
    pre: list[float] | None = None,
) -> tuple[list[float], list[float]]:
    """Return the decisions and the final channel estimate of the best survivor.

    pre holds the L - 1 symbols sent before y[0], in time order. The default is
    alphabet[0] repeated, a known start.
    """
    m = len(f0) - 1
    if m < 0:
        raise ValueError("the channel needs at least one tap")
    if pre is None:
        pre = [alphabet[0]] * m
    if len(pre) != m:
        raise ValueError("pre must hold len(f0) - 1 symbols")
    start = tuple(reversed(pre))
    metric = {start: 0.0}  # @line L1
    est = {start: [float(v) for v in f0]}
    back = []
    for yn in y:  # @line L2
        best = {}
        for s, ms in metric.items():  # @line L3
            f = est[s]
            for a in alphabet:
                x = (a,) + s
                e = yn - sum(fk * xk for fk, xk in zip(f, x))  # @line L4
                cand = ms + e * e
                t = x[:m]
                if t not in best or cand < best[t][0]:  # @line L5
                    best[t] = (cand, s, a, e, x)
        metric, new_est, bp = {}, {}, {}
        for t, (cand, s, a, e, x) in best.items():
            metric[t] = cand
            new_est[t] = [fk + step * e * xk for fk, xk in zip(est[s], x)]  # @line L6
            bp[t] = (s, a)
        est = new_est
        back.append(bp)
    t = min(metric, key=metric.get)  # @line L7
    final = est[t]
    out = []
    for bp in reversed(back):
        s, a = bp[t]
        out.append(a)
        t = s
    out.reverse()
    return out, final


def drifting_channel(n: int, base: list[float], depth: float, period: float) -> list[list[float]]:
    """Taps that drift as base[k] + depth sin(2 pi i / period + k), for i < n."""
    import math

    return [[b + depth * math.sin(2 * math.pi * i / period + k) for k, b in enumerate(base)] for i in range(n)]


def transmit(x: list[float], taps: list[list[float]], pre: list[float]) -> list[float]:
    """Noiseless output of the time-varying channel, taps[n] used at time n."""
    full = list(pre) + list(x)
    m = len(pre)
    return [sum(f[k] * full[m + n - k] for k in range(len(f))) for n, f in enumerate(taps)]
