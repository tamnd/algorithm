# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hughes-hartogs-algorithm/. The authors are listed in prov/YMENDP.jsonl.

"""Hughes-Hartogs greedy bit loading.

Subcarrier i has the gain g[i] (SNR per unit of power). With the SNR gap
Gamma it needs the power Gamma * (2**b - 1) / g[i] to carry b bits, so the
next bit costs Gamma * 2**b / g[i]. The algorithm adds one bit at a time to
the subcarrier whose next bit is cheapest. In the margin-adaptive form it
stops at the target number of bits; in the rate-adaptive form it stops when
the next bit does not fit in the power budget. A binary heap keeps the next
costs, so the time is O(N + B log N).

The arithmetic works with int, float or fractions.Fraction values, so the
tests can check exact optima.
"""

import heapq


def bit_power(gain, bits: int, gap=1):
    """The power Gamma * (2**b - 1) / g that carries b bits."""
    return gap * (2**bits - 1) / gain


def hughes_hartogs(gains, target_bits=None, budget=None, gap=1, b_max=None):
    """Greedy loading. Give exactly one of target_bits (MA form) or budget (RA form).

    Returns (bits, total_power). Ties go to the lowest index.
    """
    if (target_bits is None) == (budget is None):
        raise ValueError("give exactly one of target_bits and budget")
    if not gains or any(not g > 0 for g in gains):
        raise ValueError("need at least one subcarrier and positive gains")
    if b_max is not None and b_max < 0:
        raise ValueError("b_max must not be negative")
    n = len(gains)
    bits, total, count = [0] * n, 0, 0  # @line L1
    heap = [(gap / g, i) for i, g in enumerate(gains)] if b_max != 0 else []  # @line L2
    heapq.heapify(heap)
    while heap:  # @line L3
        cost, i = heap[0]  # @line L4
        if count == target_bits or (budget is not None and total + cost > budget):  # @line L5
            break
        heapq.heappop(heap)  # @line L6
        bits[i], total, count = bits[i] + 1, total + cost, count + 1
        if b_max is None or bits[i] < b_max:  # @line L7
            heapq.heappush(heap, (gap * 2 ** bits[i] / gains[i], i))
    if target_bits is not None and count < target_bits:
        raise ValueError("the target exceeds N * b_max bits")
    return bits, total  # @line L8


def greedy_from_increments(increments: list[list], target_bits: int) -> tuple[list[int], object]:
    """The same greedy rule on arbitrary tables of next-bit costs.

    increments[i][b] is the cost of bit b + 1 on subcarrier i. The result is
    optimal when every table is nondecreasing, and can be worse otherwise.
    """
    bits, total = [0] * len(increments), 0
    heap = [(t[0], i) for i, t in enumerate(increments) if t]
    heapq.heapify(heap)
    for _ in range(target_bits):
        if not heap:
            raise ValueError("not enough bits in the tables")
        cost, i = heapq.heappop(heap)
        bits[i], total = bits[i] + 1, total + cost
        if bits[i] < len(increments[i]):
            heapq.heappush(heap, (increments[i][bits[i]], i))
    return bits, total
