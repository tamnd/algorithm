# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-free-lunch-theorem/. The authors are listed in prov/MA8DGV.jsonl.

import itertools
import math
from fractions import Fraction

from no_free_lunch_theorem import (
    all_algorithms,
    all_functions,
    count_algorithms,
    is_closed_under_permutation,
    nfl_holds,
    time_to_minimum,
    trace,
    trace_multiset,
)


def test_algorithm_count() -> None:
    for n, k, m in ((3, 2, 3), (3, 3, 2), (4, 2, 4), (4, 2, 2)):
        algs = list(all_algorithms(n, k, m))
        assert len(algs) == count_algorithms(n, k, m)
    assert count_algorithms(4, 2, 4) == 4 * 3**2 * 2**4 == 576


def test_traces_do_not_revisit() -> None:
    for alg in all_algorithms(4, 2, 4):
        for f in all_functions(4, 2):
            ys = ()
            points = []
            for _ in range(4):
                points.append(alg[ys])
                ys += (f[alg[ys]],)
            assert sorted(points) == [0, 1, 2, 3] and ys == trace(alg, f, 4)


def test_all_functions_every_trace_equally_often() -> None:
    # Wolpert and Macready: over all of Y^X, each value sequence of length m
    # is the trace of exactly k^(n-m) functions, for every algorithm.
    for n, k, m in ((3, 3, 1), (3, 3, 2), (3, 3, 3), (4, 2, 2), (4, 2, 4)):
        F = all_functions(n, k)
        for alg in all_algorithms(n, k, m):
            ms = trace_multiset(alg, F, m)
            assert len(ms) == k**m
            assert set(ms.values()) == {k ** (n - m)}


def test_mean_time_to_minimum_is_the_same() -> None:
    F = all_functions(3, 2)
    means = {Fraction(sum(time_to_minimum(a, f) for f in F), len(F)) for a in all_algorithms(3, 2, 3)}
    assert means == {Fraction(3, 2)}


def test_sharpened_nfl_iff_closed_under_permutation() -> None:
    # Schumacher, Vose and Whitley: every subset F of Y^X, checked exhaustively.
    n, k = 3, 2
    funcs = all_functions(n, k)
    closed = 0
    for r in range(len(funcs) + 1):
        for F in itertools.combinations(funcs, r):
            cup = is_closed_under_permutation(F, n)
            closed += cup
            if cup:
                assert all(nfl_holds(F, n, k, m) for m in range(1, n + 1))
            # With full traces (m = n), NFL holds only for closed sets.
            assert nfl_holds(F, n, k, n) == cup
    # The closed sets are the unions of orbits; there are C(n+k-1, k-1) orbits.
    assert closed == 2 ** math.comb(n + k - 1, k - 1) == 16


def test_closed_class_that_is_not_all_functions() -> None:
    # The needle functions on 4 points: one point has value 0, the others 1.
    needles = [tuple(0 if i == j else 1 for i in range(4)) for j in range(4)]
    assert is_closed_under_permutation(needles, 4)
    assert nfl_holds(needles, 4, 2, 4)
    times = {sum(time_to_minimum(a, f) for f in needles) for a in all_algorithms(4, 2, 4)}
    assert times == {1 + 2 + 3 + 4}
