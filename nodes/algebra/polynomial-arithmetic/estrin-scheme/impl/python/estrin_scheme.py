# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/estrin-scheme/. The authors are listed in prov/SDH9BZ.jsonl.

"""Estrin's scheme for evaluating a polynomial with a short critical path.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. The coefficients and the point may be
int, Fraction, float, or any ring element type with + and *.

Each round combines neighbouring pairs c[2i] + c[2i+1] * p, where p is
x^(2^k) in round k, and then squares p. The products of one round do not
depend on each other, so on parallel hardware the critical path has about
2 log2(n + 1) operations, against 2n for Horner's rule.
"""

from __future__ import annotations

from typing import Any, List, Sequence, Tuple


def estrin(a: Sequence[Any], x: Any) -> Any:
    """Return a(x) by Estrin's scheme, with n + ceil(log2(n + 1)) - 1 products."""
    c = list(a)  # @line L1
    if not c:
        return x - x
    p = x  # @line L2
    while len(c) > 1:  # @line L3
        nxt = [c[2 * i] + c[2 * i + 1] * p for i in range(len(c) // 2)]  # @line L4
        if len(c) % 2 == 1:  # @line L5
            nxt.append(c[-1])
        c = nxt  # @line L6
        if len(c) > 1:  # @line L7
            p = p * p
    return c[0]  # @line L8


class Counter:
    """A ring element that counts operations and the depth of its expression."""

    stats = {"mul": 0, "add": 0}

    def __init__(self, v: Any, depth: int = 0) -> None:
        self.v = v
        self.depth = depth

    def _w(self, o: Any) -> "Counter":
        return o if isinstance(o, Counter) else Counter(o)

    def __add__(self, o: Any) -> "Counter":
        o = self._w(o)
        Counter.stats["add"] += 1
        return Counter(self.v + o.v, max(self.depth, o.depth) + 1)

    __radd__ = __add__

    def __sub__(self, o: Any) -> "Counter":
        o = self._w(o)
        return Counter(self.v - o.v, max(self.depth, o.depth))

    def __mul__(self, o: Any) -> "Counter":
        o = self._w(o)
        Counter.stats["mul"] += 1
        return Counter(self.v * o.v, max(self.depth, o.depth) + 1)

    __rmul__ = __mul__


def estrin_stats(a: Sequence[Any], x: Any) -> Tuple[Any, int, int, int]:
    """Return (value, products, additions, depth) of Estrin's scheme."""
    Counter.stats = {"mul": 0, "add": 0}
    r = estrin([Counter(c) for c in a], Counter(x))
    return r.v, Counter.stats["mul"], Counter.stats["add"], r.depth


def horner(a: Sequence[Any], x: Any) -> Any:
    """Reference: Horner's rule, n products and n additions in sequence."""
    acc = x - x
    for c in reversed(list(a)):
        acc = acc * x + c
    return acc


def horner_stats(a: Sequence[Any], x: Any) -> Tuple[Any, int, int, int]:
    """Return (value, products, additions, depth) of Horner's rule."""
    Counter.stats = {"mul": 0, "add": 0}
    a = list(a)
    if not a:
        return x - x, 0, 0, 0
    acc = Counter(a[-1])
    xc = Counter(x)
    for c in reversed(a[:-1]):
        acc = acc * xc + c
    return acc.v, Counter.stats["mul"], Counter.stats["add"], acc.depth


def levels(a: Sequence[Any], x: Any) -> List[List[Any]]:
    """The lists c after each round, for traces."""
    c = list(a)
    out = [c]
    p = x
    while len(c) > 1:
        nxt = [c[2 * i] + c[2 * i + 1] * p for i in range(len(c) // 2)]
        if len(c) % 2 == 1:
            nxt.append(c[-1])
        c = nxt
        out.append(c)
        if len(c) > 1:
            p = p * p
    return out


if __name__ == "__main__":
    print(levels([1, 2, 3, 4, 5, 6, 7, 8], 2))
    print(estrin_stats([1, 2, 3, 4, 5, 6, 7, 8], 2), horner_stats([1, 2, 3, 4, 5, 6, 7, 8], 2))
