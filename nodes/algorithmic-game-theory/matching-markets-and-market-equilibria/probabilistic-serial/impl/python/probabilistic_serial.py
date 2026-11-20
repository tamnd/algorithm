# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-serial/. The authors are listed in prov/VY2D6A.jsonl.

from fractions import Fraction
from typing import Optional, Sequence


def probabilistic_serial(
    prefs: Sequence[Sequence[int]], m: Optional[int] = None
) -> list[list[Fraction]]:
    """Probabilistic serial (the eating algorithm) of Bogomolnaia and Moulin.

    prefs[i] lists the objects acceptable to agent i, best first, without repeats; the
    objects are 0, ..., m - 1 (by default m is one more than the largest listed object).
    Each object is one unit of probability. All agents eat at speed 1 from time 0 to time 1,
    each from its best acceptable object that is not used up. Returns the n by m matrix P
    of Fractions, where P[i][o] is the amount of o that agent i ate: the probability that
    i gets o.
    The loop runs once per event: at each event an object is used up or the time reaches 1,
    so there are at most m + 1 rounds of O(n + m) work, plus O(total list length) for the
    pointers. That is O(m (n + m) + n m) = O(m (n + m)) time, and O(n m) space for P.
    """
    n = len(prefs)
    if m is None:
        m = 1 + max((o for lst in prefs for o in lst), default=-1)
    for lst in prefs:
        if len(set(lst)) != len(lst) or any(not 0 <= o < m for o in lst):
            raise ValueError("a preference list repeats an object or is out of range")
    left = [Fraction(1)] * m  # @line L1
    P = [[Fraction(0)] * m for _ in range(n)]  # @line L2
    t = Fraction(0)  # @line L3
    ptr = [0] * n  # position of the current object in each list; it only moves forward
    while t < 1:  # @line L4
        top = []
        for i in range(n):  # @line L5
            lst = prefs[i]
            while ptr[i] < len(lst) and left[lst[ptr[i]]] == 0:
                ptr[i] += 1
            top.append(lst[ptr[i]] if ptr[i] < len(lst) else -1)
        if all(o == -1 for o in top):  # @line L6
            break
        eaters = [0] * m  # @line L7
        for o in top:
            if o != -1:
                eaters[o] += 1
        delta = 1 - t  # @line L8
        for o in range(m):
            if eaters[o] > 0:
                delta = min(delta, left[o] / eaters[o])
        for i in range(n):  # @line L9
            o = top[i]
            if o != -1:
                P[i][o] += delta
                left[o] -= delta
        t += delta  # @line L10
    return P  # @line L11
