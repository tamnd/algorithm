# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/take-the-stairs-strategy/. The authors are listed in prov/F0PJDM.jsonl.

from fractions import Fraction
from numbers import Rational


def wait_limit(e: Rational, s: Rational) -> Rational:
    """How long the strategy waits for the elevator: s - e, or 0 if the stairs are not slower."""
    if e < 0 or s <= 0:
        raise ValueError("need e >= 0 and s > 0")
    if e >= s:  # @line L1
        return 0
    return s - e  # @line L2


def arrival_time(t: Rational | None, e: Rational, s: Rational, w: Rational | None = None) -> Rational:
    """Time to reach the top when the elevator comes at time t (None: never) and we wait at most w."""
    if w is None:
        w = wait_limit(e, s)
    if e >= s:
        return s
    # @line L3: wait for the elevator, for at most time w
    if t is not None and t <= w:  # @line L4
        return t + e
    return w + s  # @line L5


def opt_time(t: Rational | None, e: Rational, s: Rational) -> Rational:
    """The offline optimum: ride the elevator if it is faster, else take the stairs at once."""
    if t is None:
        return s
    return min(t + e, s)


def worst_ratio(e: Rational, s: Rational, w: Rational) -> Fraction:
    """Exact supremum over all arrival times of the ratio of the rule "wait at most w", for 0 < e < s.

    For t <= w the ratio is (t + e) / min(t + e, s), at most (w + e) / min(w + e, s).
    For t > w it is (w + s) / min(t + e, s), which is largest as t tends to w from above.
    The second value is the larger one. The supremum may not be attained.
    """
    if not 0 < e < s or w < 0:
        raise ValueError("need 0 < e < s and w >= 0")
    return Fraction(w + s) / min(w + e, s)
