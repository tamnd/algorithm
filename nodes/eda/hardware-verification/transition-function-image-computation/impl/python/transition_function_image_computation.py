# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-function-image-computation/. The authors are listed in prov/H8PR83.jsonl.
"""Image computation from next-state functions (Coudert, Berthet and Madre 1989; Coudert and Madre 1990).

The image of a set S of states under next-state functions delta_1..delta_m is
the range of the vector (delta_1 constrain S, ..., delta_m constrain S). The
range is computed by splitting on one output at a time. No transition relation
is built.
"""

from __future__ import annotations

from bdd import BDD


def constrain(bdd: BDD, f: int, c: int) -> int:
    """The generalized cofactor f constrain c of Coudert and Madre, for c != 0.

    It agrees with f where c is 1. Cost O(|f| |c|) calls with a cache.
    """
    if c == 0:
        raise ValueError("constrain by the zero function")
    cache: dict[tuple[int, int], int] = {}

    def go(f: int, c: int) -> int:
        if c == 1 or f <= 1:
            return f
        if f == c:
            return 1
        key = (f, c)
        r = cache.get(key)
        if r is None:
            v = min(bdd.level(f), bdd.level(c))
            f0, f1 = bdd.cofactors(f, v)
            c0, c1 = bdd.cofactors(c, v)
            if c0 == 0:
                r = go(f1, c1)
            elif c1 == 0:
                r = go(f0, c0)
            else:
                r = bdd.mk(v, go(f0, c0), go(f1, c1))
            cache[key] = r
        return r

    return go(f, c)


def range_of(bdd: BDD, g: list[int], y: list[int]) -> int:
    """The set {g(z) : z any point}, as a BDD over the variables y (one per function).

    Precondition: the variables y do not occur in g. Cost: at most 2^len(g) - 1 calls,
    each with up to len(g) constrain operations.
    """
    if not g:  # @line L4
        return 1
    head, rest = g[0], g[1:]
    yi = bdd.var(y[0])
    if head == 1:  # @line L5
        return bdd.conj(yi, range_of(bdd, rest, y[1:]))
    if head == 0:  # @line L6
        return bdd.conj(bdd.neg(yi), range_of(bdd, rest, y[1:]))
    hi = range_of(bdd, [constrain(bdd, h, head) for h in rest], y[1:])  # @line L7
    lo = range_of(bdd, [constrain(bdd, h, bdd.neg(head)) for h in rest], y[1:])  # @line L8
    return bdd.disj(bdd.conj(yi, hi), bdd.conj(bdd.neg(yi), lo))  # @line L9


def image(bdd: BDD, delta: list[int], states: int, y: list[int]) -> int:
    """The image {delta(s, x) : states(s) = 1, x any input} as a BDD over the next-state variables y.

    Precondition: delta[i] is the next-state function of state bit i over the present-state
    and input variables; states is a BDD over the present-state variables; y are fresh
    variables, one per state bit. Cost: len(delta) constrain operations plus range_of.
    """
    if states == 0:  # @line L1
        return 0
    g = [constrain(bdd, d, states) for d in delta]  # @line L2
    return range_of(bdd, g, y)  # @line L3
