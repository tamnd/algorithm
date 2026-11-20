# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-qpsk/. The authors are listed in prov/HPEG9T.jsonl.

"""Offset QPSK at L_s samples per symbol: the modulator, the matched-filter receiver, and the
phase steps of the signal.

Bits 2k and 2k+1 give the in-phase and quadrature levels (1 - 2b)/sqrt(2), so E_s = 1 for a
pulse whose taps have unit energy. offset=False gives plain QPSK with the same pulse, for comparison.
L_s must be even, so that the offset of T/2 is L_s/2 samples.
"""

import math


def rrc_taps(beta: float, ls: int, span: int) -> list[float]:
    """Root-raised-cosine taps g(n/ls), |n| <= span*ls, T = 1, scaled to unit energy."""
    g = []
    for n in range(-span * ls, span * ls + 1):
        u = n / ls
        if u == 0:
            v = 1 - beta + 4 * beta / math.pi
        elif abs(abs(4 * beta * u) - 1) < 1e-12:
            a = math.pi / (4 * beta)
            v = beta / math.sqrt(2) * ((1 + 2 / math.pi) * math.sin(a) + (1 - 2 / math.pi) * math.cos(a))
        else:
            v = (math.sin(math.pi * (1 - beta) * u) + 4 * beta * u * math.cos(math.pi * (1 + beta) * u)) / (
                math.pi * u * (1 - (4 * beta * u) ** 2)
            )
        g.append(v)
    e = math.sqrt(sum(v * v for v in g))
    return [v / e for v in g]


def levels(bits: list[int]) -> tuple[list[float], list[float]]:
    """The in-phase and quadrature levels of each symbol."""
    if len(bits) % 2:
        raise ValueError("need an even number of bits")
    s = 1 / math.sqrt(2)
    a_i = [(1 - 2 * b) * s for b in bits[0::2]]  # @line L1
    a_q = [(1 - 2 * b) * s for b in bits[1::2]]
    return a_i, a_q


def modulate(bits: list[int], taps: list[float], ls: int, offset: bool = True) -> list[complex]:
    """sum_k a_I[k] g(t - kT) + j sum_k a_Q[k] g(t - kT - T/2), at ls samples per T."""
    if ls % 2:
        raise ValueError("ls must be even")
    a_i, a_q = levels(bits)
    off = ls // 2 if offset else 0
    out = [0j] * (len(a_i) * ls + len(taps) + off)
    for k, (x, y) in enumerate(zip(a_i, a_q)):
        for n, h in enumerate(taps):
            out[k * ls + n] += x * h  # @line L2
            out[k * ls + off + n] += 1j * y * h  # @line L3
    return out  # @line L4


def demodulate(r: list[complex], taps: list[float], ls: int, nsym: int, offset: bool = True) -> list[int]:
    """Matched filter, then I at kT and Q at kT + T/2 (after the delay of the two filters)."""
    off = ls // 2 if offset else 0
    d = len(taps) - 1

    def matched(m: int) -> complex:
        # The output at sample m of r filtered with the time-reversed taps.
        return sum(r[m - d + n] * h for n, h in enumerate(taps) if 0 <= m - d + n < len(r))  # @line L5

    bits = []
    for k in range(nsym):
        bits.append(1 if matched(k * ls + d).real < 0 else 0)  # @line L6
        bits.append(1 if matched(k * ls + off + d).imag < 0 else 0)  # @line L7
    return bits


def phase_steps(s: list[complex], ls: int, start: int, count: int) -> list[float]:
    """Phase change in degrees between the middles of consecutive half-symbol intervals."""
    half = ls // 2
    mids = [s[start + m * half + half // 2] for m in range(count)]
    steps = []
    for p, q in zip(mids, mids[1:]):
        d = math.degrees(math.atan2((q * p.conjugate()).imag, (q * p.conjugate()).real))  # @line L8
        steps.append(d)
    return steps
