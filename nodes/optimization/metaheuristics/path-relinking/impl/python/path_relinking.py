# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-relinking/. The authors are listed in prov/EFCZD2.jsonl.

from collections.abc import Callable
from dataclasses import dataclass

Bits = tuple[int, ...]


@dataclass(frozen=True)
class Step:
    """One move of the path: the flipped position, the new point and its cost."""

    flipped: int
    x: Bits
    fx: int


def path_relinking(xs: Bits, xt: Bits, f: Callable[[Bits], int]) -> tuple[Bits, int, list[Step]]:
    """Greedy path relinking from xs to xt on bit strings, minimizing f (Glover).

    Each step flips one position where the current point still differs from
    xt, the one that gives the least cost, with ties to the lowest position.
    The path has exactly as many steps as the Hamming distance of xs and xt
    and ends at xt. Returns (best point on the path, its cost, the steps).
    """
    if len(xs) != len(xt):
        raise ValueError("the two solutions must have the same length")
    x = xs  # @line L1
    best, f_best = xs, f(xs)
    delta = [i for i in range(len(xs)) if xs[i] != xt[i]]  # @line L2
    path: list[Step] = []
    while delta:  # @line L3
        options = [(f(flip(x, i)), i) for i in delta]  # @line L4
        fx, i = min(options)
        x = flip(x, i)  # @line L5
        delta.remove(i)
        path.append(Step(i, x, fx))
        if fx < f_best:  # @line L6
            best, f_best = x, fx
    return best, f_best, path  # @line L7


def flip(x: Bits, i: int) -> Bits:
    """The bit string x with position i flipped."""
    return x[:i] + (1 - x[i],) + x[i + 1 :]


def unsatisfied_weight(clauses: list[tuple[int, ...]], weights: list[int]) -> Callable[[Bits], int]:
    """The weighted MAX-SAT cost: the total weight of the clauses that x does not satisfy.

    A clause is a tuple of nonzero literals; literal v means variable v - 1 is 1,
    and literal -v means variable v - 1 is 0.
    """

    def f(x: Bits) -> int:
        return sum(w for c, w in zip(clauses, weights) if not any((x[abs(v) - 1] == 1) == (v > 0) for v in c))

    return f


def flip_descent(x: Bits, f: Callable[[Bits], int]) -> Bits:
    """Best-improvement descent with one-bit flips, ties to the lowest position."""
    while True:
        fx, i = min((f(flip(x, i)), i) for i in range(len(x)))
        if fx >= f(x):
            return x
        x = flip(x, i)
