# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benjamini-yekutieli-procedure/. The authors are listed in prov/HW5E27.jsonl.
"""The Benjamini-Yekutieli procedure.

It is the Benjamini-Hochberg step-up procedure run at level q / c_m, where
c_m = 1 + 1/2 + ... + 1/m. Find the largest k with p_(k) <= k q / (m c_m) and
reject H_(1), ..., H_(k). Under any dependence among the p-values, with valid
null p-values, the false discovery rate is at most (m_0 / m) q.

Comparisons are done as m c_m p <= k q. With fractions.Fraction inputs, c_m is
computed exactly as a Fraction, so the decisions are exact.
"""

import math
from collections.abc import Sequence
from fractions import Fraction


def harmonic(m: int, exact: bool = False):
    """c_m = 1 + 1/2 + ... + 1/m, as a Fraction if exact, else as a correctly summed float."""
    if exact:
        return sum((Fraction(1, i) for i in range(1, m + 1)), Fraction(0))
    return math.fsum(1 / i for i in range(1, m + 1))


def by(p: Sequence, q) -> tuple[list[bool], list]:
    """Return (reject, adjusted) in the original order of p."""
    m = len(p)
    if m == 0:
        return [], []
    if any(not 0 <= v <= 1 for v in p):
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 < q <= 1:
        raise ValueError("q must lie in (0, 1]")
    exact = isinstance(q, Fraction) or any(isinstance(v, Fraction) for v in p)
    c = harmonic(m, exact)  # @line L1
    order = sorted(range(m), key=lambda i: p[i])  # @line L2
    k = m
    while k >= 1 and m * c * p[order[k - 1]] > k * q:  # @line L3
        k -= 1  # @line L4
    reject = [False] * m
    for r in range(k):  # @line L5
        reject[order[r]] = True
    adjusted = [0] * m
    running = 1
    for r in range(m - 1, -1, -1):  # @line L6
        running = min(running, m * c * p[order[r]] / (r + 1))  # @line L7
        adjusted[order[r]] = running
    return reject, adjusted  # @line L8
