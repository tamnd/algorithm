# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-job-first/. The authors are listed in prov/GK26MR.jsonl.

"""Nonpreemptive shortest-job-first scheduling on one CPU, with burst prediction."""

import heapq
from fractions import Fraction
from typing import Optional


def sjf(arrival: list, burst: list, predicted: Optional[list] = None) -> tuple:
    """Return (start, completion), two lists indexed like the input.

    Process i arrives at arrival[i] and runs for burst[i] > 0 units. Whenever the
    CPU is free, the scheduler runs the arrived process with the least predicted
    burst (predicted[i], or burst[i] when no prediction is given), ties by
    arrival time and then by index, to the end of its burst.
    Cost: O(n log n) time with a binary heap, O(n) extra space.
    """
    n = len(arrival)
    key = burst if predicted is None else predicted
    q = sorted(range(n), key=lambda i: (arrival[i], i))  # @line L1
    heap: list = []
    t = 0
    k = 0
    start = [0] * n
    completion = [0] * n
    while k < n or heap:  # @line L2
        if not heap and t < arrival[q[k]]:  # @line L3
            t = arrival[q[k]]
        while k < n and arrival[q[k]] <= t:  # @line L4
            i = q[k]
            heapq.heappush(heap, (key[i], arrival[i], i))  # @line L5
            k += 1
        _, _, i = heapq.heappop(heap)  # @line L6
        start[i] = t  # @line L7
        t = t + burst[i]
        completion[i] = t
    return start, completion  # @line L8


def predict(bursts: list, alpha: Fraction, tau0: object) -> list:
    """Exponential averages tau[j+1] = alpha * t[j] + (1 - alpha) * tau[j].

    Returns [tau0, tau1, ..., tau_m] for the m measured bursts. 0 <= alpha <= 1.
    """
    taus = [tau0]
    for t in bursts:
        taus.append(alpha * t + (1 - alpha) * taus[-1])
    return taus
