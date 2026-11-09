# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-free-lunch-theorem/. The authors are listed in prov/MA8DGV.jsonl.

"""Exhaustive checks of the no free lunch theorem on tiny finite domains.

The search space is X = {0, ..., n-1} and the values are Y = {0, ..., k-1}.
A function f is a tuple of length n. A deterministic non-revisiting algorithm
with m steps is a dict that maps each tuple of values seen so far (of length
0 to m-1) to the next point to evaluate, which must not be a point visited
before. Its trace on f is the tuple of the m values it sees.
"""

import itertools
from collections import Counter
from typing import Iterable, Iterator

Function = tuple[int, ...]
Algorithm = dict[tuple[int, ...], int]


def all_functions(n: int, k: int) -> list[Function]:
    """All k^n functions from {0..n-1} to {0..k-1}."""
    return list(itertools.product(range(k), repeat=n))


def all_algorithms(n: int, k: int, m: int) -> Iterator[Algorithm]:
    """Every deterministic non-revisiting algorithm with m <= n steps, as a decision tree."""
    # The nodes of the tree are the value prefixes of length 0..m-1, in order.
    prefixes = [p for t in range(m) for p in itertools.product(range(k), repeat=t)]

    def build(i: int, alg: Algorithm) -> Iterator[Algorithm]:
        if i == len(prefixes):
            yield dict(alg)
            return
        p = prefixes[i]
        visited = [alg[p[:j]] for j in range(len(p))]
        for x in range(n):
            if x not in visited:
                alg[p] = x
                yield from build(i + 1, alg)
        del alg[p]

    yield from build(0, {})


def count_algorithms(n: int, k: int, m: int) -> int:
    """The number of decision trees: prod over t < m of (n - t)^(k^t)."""
    total = 1
    for t in range(m):
        total *= (n - t) ** (k**t)
    return total


def trace(alg: Algorithm, f: Function, m: int) -> tuple[int, ...]:
    """The m values that alg sees on f."""
    ys: tuple[int, ...] = ()
    for _ in range(m):
        ys += (f[alg[ys]],)
    return ys


def trace_multiset(alg: Algorithm, F: Iterable[Function], m: int) -> Counter:
    return Counter(trace(alg, f, m) for f in F)


def is_closed_under_permutation(F: Iterable[Function], n: int) -> bool:
    """True if f o sigma is in F for every f in F and every permutation sigma of X."""
    S = set(F)
    return all(tuple(f[s] for s in sigma) in S for f in S for sigma in itertools.permutations(range(n)))


def nfl_holds(F: Iterable[Function], n: int, k: int, m: int) -> bool:
    """True if all algorithms with m steps have the same multiset of traces on F."""
    F = list(F)
    first = None
    for alg in all_algorithms(n, k, m):
        ms = trace_multiset(alg, F, m)
        if first is None:
            first = ms
        elif ms != first:
            return False
    return True


def time_to_minimum(alg: Algorithm, f: Function) -> int:
    """The number of evaluations until alg first sees min(f), with m = n."""
    target = min(f)
    for t, y in enumerate(trace(alg, f, len(f)), start=1):
        if y == target:
            return t
    raise AssertionError("a full trace sees every value")
