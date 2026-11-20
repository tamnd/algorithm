# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chow-cioffi-bingham-algorithm/. The authors are listed in prov/KRYPZ8.jsonl.

"""Chow-Cioffi-Bingham loading for a multicarrier link (margin-adaptive form).

snr[i] is the SNR of subcarrier i when it gets unit energy. Each round
computes the real rate b[i] = log2(1 + snr[i] / (Gamma * margin)), rounds it
to the nearest integer, and moves the margin by the factor
2 ** ((total - target) / used), so that the next round lands closer to the
target. After at most max_count rounds, the bits are fixed one at a time with
the rounding errors diff[i] = b[i] - round(b[i]): extra bits are taken from
the subcarriers with the smallest diff, and missing bits are added where diff
is largest. Last, each used subcarrier gets the energy its bits need under the
gap model, and all energies are scaled to the budget, which gives every used
subcarrier the same margin.

Each round costs O(N). The fix-up scans all subcarriers once per bit that it
moves.
"""

import heapq
import math


def round_half_up(x: float) -> int:
    return math.floor(x + 0.5)


def chow_cioffi_bingham(snr, target_bits, gap=1.0, budget=None, max_count=10, b_max=None):
    """Return (bits, energies, margin, rounds).

    budget defaults to N (unit energy per subcarrier, as in the paper's
    initialization). margin is the common margin, a linear factor, that the
    final energies give on every used subcarrier.
    """
    n = len(snr)
    if n == 0 or any(not s > 0 for s in snr):
        raise ValueError("need at least one subcarrier and positive SNR values")
    if target_bits < 0 or (b_max is not None and target_bits > n * b_max):
        raise ValueError("the target must lie in [0, N * b_max]")
    if max_count < 1:
        raise ValueError("max_count must be at least 1")
    if budget is None:
        budget = float(n)
    margin_db, rounds = 0.0, 0  # @line L1
    while True:
        m = gap * 10 ** (margin_db / 10)
        b = [math.log2(1 + s / m) for s in snr]  # @line L2
        bh = [round_half_up(x) if b_max is None else min(round_half_up(x), b_max) for x in b]
        diff = [x - y for x, y in zip(b, bh)]
        used = sum(1 for y in bh if y > 0)
        total = sum(bh)  # @line L3
        if total == 0 and target_bits > 0 and rounds == 0:
            raise ValueError("the channel carries no bits at this gap")
        if used > 0:
            margin_db += 10 * math.log10(2 ** ((total - target_bits) / used))  # @line L4
        rounds += 1
        if total == target_bits or rounds >= max_count or used == 0:  # @line L5
            break
    while total > target_bits:  # @line L6
        i = min((d, i) for i, d in enumerate(diff) if bh[i] > 0)[1]
        bh[i], diff[i], total = bh[i] - 1, diff[i] + 1, total - 1
    while total < target_bits:
        i = -max((d, -i) for i, d in enumerate(diff) if b_max is None or bh[i] < b_max)[1]
        bh[i], diff[i], total = bh[i] + 1, diff[i] - 1, total + 1
    need = [gap * (2**y - 1) / s for y, s in zip(bh, snr)]  # @line L7
    total_need = sum(need)
    if total_need == 0:
        return bh, [0.0] * n, math.inf, rounds
    scale = budget / total_need
    return bh, [e * scale for e in need], scale, rounds  # @line L8


def loading_power(snr, bits, gap=1.0) -> float:
    """The least energy that carries the bits at margin 1: the sum of Gamma (2**b - 1) / snr."""
    return sum(gap * (2**b - 1) / s for b, s in zip(bits, snr))


def optimal_power(snr, target_bits, gap=1.0) -> float:
    """The least energy for target_bits bits, by the greedy rule; the reference optimum."""
    bits = [0] * len(snr)
    heap = [(gap / s, i) for i, s in enumerate(snr)]
    heapq.heapify(heap)
    total = 0.0
    for _ in range(target_bits):
        c, i = heapq.heappop(heap)
        total += c
        bits[i] += 1
        heapq.heappush(heap, (gap * 2 ** bits[i] / snr[i], i))
    return total
