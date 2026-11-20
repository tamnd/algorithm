# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-campello-algorithm/. The authors are listed in prov/XEKW7B.jsonl.

"""Levin-Campello bit loading.

Subcarrier i has the gain g[i]. With the SNR gap Gamma, bit b + 1 on it
costs the power Gamma * 2**b / g[i]. The algorithm starts from any loading
and first makes it efficient: while the most expensive loaded bit costs more
than the cheapest unloaded bit, it moves that bit. Then it tightens the
loading: in the margin-adaptive (MA) form it removes the most expensive bits
or adds the cheapest bits until the total is B; in the rate-adaptive (RA)
form it removes bits while the power exceeds P and adds bits while the next
one fits. Two heaps with lazy deletion give the most expensive loaded bit and
the cheapest unloaded bit in O(log) time per move.

Ties are broken by the subcarrier index: the loaded bit with the largest
(cost, index) leaves first and the unloaded bit with the smallest
(cost, index) enters first. The arithmetic works with int, float or
fractions.Fraction values.
"""

import heapq

INF = float("inf")


class Loading:
    """The bits, bit count, total power and two lazy heaps of one loading."""

    def __init__(self, gains, bits, gap=1, b_max=None):
        self.g, self.b, self.gap, self.b_max = gains, list(bits), gap, b_max
        self.count = sum(self.b)
        self.power = sum(gap * (2**b - 1) / g for g, b in zip(gains, self.b))
        self.lasts = []  # entries (-cost, -i, bits) for the last loaded bit of i
        self.nexts = []  # entries (cost, i, bits) for the next bit of i
        for i in range(len(gains)):
            self._push(i)

    def _push(self, i):
        b = self.b[i]
        if b > 0:
            heapq.heappush(self.lasts, (-(self.gap * 2 ** (b - 1) / self.g[i]), -i, b))
        if self.b_max is None or b < self.b_max:
            heapq.heappush(self.nexts, (self.gap * 2**b / self.g[i], i, b))

    def max_last(self):
        """(cost, i) of the most expensive loaded bit, or (-inf, -1) if none."""
        while self.lasts and self.lasts[0][2] != self.b[-self.lasts[0][1]]:
            heapq.heappop(self.lasts)
        if not self.lasts:
            return -INF, -1
        return -self.lasts[0][0], -self.lasts[0][1]

    def min_next(self):
        """(cost, i) of the cheapest unloaded bit, or (inf, -1) if none."""
        while self.nexts and self.nexts[0][2] != self.b[self.nexts[0][1]]:
            heapq.heappop(self.nexts)
        if not self.nexts:
            return INF, -1
        return self.nexts[0][0], self.nexts[0][1]

    def remove_bit(self, i, cost):
        self.b[i], self.count, self.power = self.b[i] - 1, self.count - 1, self.power - cost
        self._push(i)

    def add_bit(self, i, cost):
        self.b[i], self.count, self.power = self.b[i] + 1, self.count + 1, self.power + cost
        self._push(i)


def levin_campello(gains, start, target_bits=None, budget=None, gap=1, b_max=None):
    """Optimal loading reached from the start loading.

    Give exactly one of target_bits (MA form) and budget (RA form).
    Returns (bits, total_power, number_of_swaps).
    """
    if (target_bits is None) == (budget is None):
        raise ValueError("give exactly one of target_bits and budget")
    if not gains or any(not g > 0 for g in gains) or len(start) != len(gains):
        raise ValueError("need positive gains and a start loading of the same length")
    if any(b < 0 or (b_max is not None and b > b_max) for b in start):
        raise ValueError("the start loading must lie in [0, b_max]")
    if budget is not None and budget < 0:
        raise ValueError("the budget must not be negative")
    if target_bits is not None and (target_bits < 0 or (b_max is not None and target_bits > b_max * len(gains))):
        raise ValueError("the target must lie in [0, N * b_max]")
    ma = target_bits is not None
    s = Loading(gains, start, gap, b_max)  # @line L1
    swaps = 0
    while True:
        (cl, m), (cn, n) = s.max_last(), s.min_next()
        if not cl > cn:  # @line L2
            break
        s.remove_bit(m, cl)  # @line L3
        s.add_bit(n, cn)
        swaps += 1
    while (s.count > target_bits) if ma else (s.power > budget):  # @line L4
        cl, m = s.max_last()
        s.remove_bit(m, cl)  # @line L5
    while True:
        cn, n = s.min_next()
        if n < 0 or ((s.count >= target_bits) if ma else (s.power + cn > budget)):  # @line L6
            break
        s.add_bit(n, cn)  # @line L7
    return s.b, s.power, swaps  # @line L8
