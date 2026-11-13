# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sprague-grundy-theorem/. The authors are listed in prov/AMWPCY.jsonl.

"""Sums of impartial games, to test the Sprague-Grundy theorem.

A component is a pair (moves, n): a heap of n tokens from which a move
removes m tokens for some m in moves. moves = None means a Nim heap, where
a move removes any positive number. A sum is a tuple of components, and a
move in the sum is a move in exactly one component."""

from functools import lru_cache, reduce
from typing import Iterator, List, Optional, Tuple

Component = Tuple[Optional[Tuple[int, ...]], int]
Sum = Tuple[Component, ...]


def component_options(c: Component) -> Iterator[Component]:
    moves, n = c
    if moves is None:
        for b in range(n):
            yield (None, b)
    else:
        for m in moves:
            if m <= n:
                yield (moves, n - m)


def sum_options(s: Sum) -> Iterator[Sum]:
    for i, c in enumerate(s):
        for d in component_options(c):
            yield s[:i] + (d,) + s[i + 1:]


def _canon(s: Sum) -> Sum:
    return tuple(sorted(s, key=lambda c: (c[0] is not None, c[0] or (), c[1])))


@lru_cache(maxsize=None)
def _mover_loses(s: Sum) -> bool:
    return all(not _mover_loses(_canon(t)) for t in sum_options(s))


def mover_loses(s: Sum) -> bool:
    """Brute force over the whole sum: True for a P-position."""
    return _mover_loses(_canon(s))


def mex(values) -> int:
    seen = set(values)
    m = 0
    while m in seen:
        m += 1
    return m


@lru_cache(maxsize=None)
def component_grundy(c: Component) -> int:
    return mex(component_grundy(d) for d in component_options(c))


@lru_cache(maxsize=None)
def _sum_grundy(s: Sum) -> int:
    return mex(_sum_grundy(_canon(t)) for t in sum_options(s))


def sum_grundy_brute(s: Sum) -> int:
    """The Grundy number of the sum, computed on the sum's own game graph."""
    return _sum_grundy(_canon(s))


def sum_grundy(s: Sum) -> int:
    """The theorem: the XOR of the component values."""
    return reduce(lambda a, b: a ^ b, (component_grundy(c) for c in s), 0)


def winning_moves(s: Sum) -> List[Tuple[int, Component]]:
    """Moves (component index, new component) that make the XOR zero."""
    x = sum_grundy(s)
    if x == 0:
        return []
    out = []
    for i, c in enumerate(s):
        target = component_grundy(c) ^ x
        for d in component_options(c):
            if component_grundy(d) == target:
                out.append((i, d))
    return out
