# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neumaier-summation/. The authors are listed in prov/C00E29.jsonl.

"""Neumaier's improved Kahan summation (Kahan-Babuska summation) of binary64 floats.

Each addition s + x is followed by Fast2Sum with the larger operand first,
which gives its exact rounding error; the errors are added in a separate
sum c, and s + c is returned.
"""

from collections.abc import Iterable


def neumaier_sum(xs: Iterable[float]) -> float:
    """Compensated sum of xs. Cost: 4 floating-point operations and one comparison per term."""
    s = 0.0  # @line L1
    c = 0.0  # @line L2
    for x in xs:  # @line L3
        t = s + x  # @line L4
        if abs(s) >= abs(x):  # @line L5
            c += (s - t) + x  # @line L6
        else:
            c += (x - t) + s  # @line L7
        s = t  # @line L8
    return s + c  # @line L9


def neumaier_parts(xs: Iterable[float]) -> tuple[float, list[float], float]:
    """The final s, the list of exact errors q_i, and the accumulated c, for tests."""
    s = 0.0
    c = 0.0
    qs = []
    for x in xs:
        t = s + x
        q = (s - t) + x if abs(s) >= abs(x) else (x - t) + s
        qs.append(q)
        c += q
        s = t
    return s, qs, c
