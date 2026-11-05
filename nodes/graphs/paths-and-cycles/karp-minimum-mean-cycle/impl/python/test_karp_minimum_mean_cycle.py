# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-minimum-mean-cycle/. The authors are listed in prov/CDP661.jsonl.

import itertools
import random
from fractions import Fraction

from karp_minimum_mean_cycle import karp_minimum_mean_cycle


def brute_min_mean(n, arcs):
    """Independent oracle: minimum of weight / length over all simple cycles."""
    cheapest = {}
    for u, v, w in arcs:
        if (u, v) not in cheapest or w < cheapest[(u, v)]:
            cheapest[(u, v)] = w
    best = None
    for k in range(1, n + 1):
        for vs in itertools.combinations(range(n), k):
            for rest in itertools.permutations(vs[1:]):
                c = (vs[0],) + rest
                pairs = [(c[i], c[(i + 1) % k]) for i in range(k)]
                if all(p in cheapest for p in pairs):
                    mean = Fraction(sum(cheapest[p] for p in pairs), k)
                    best = mean if best is None or mean < best else best
    return best


def check_cycle(arcs, cycle, mean) -> bool:
    if not cycle:
        return False
    for i, a in enumerate(cycle):
        if arcs[a][1] != arcs[cycle[(i + 1) % len(cycle)]][0]:
            return False
    heads = [arcs[a][1] for a in cycle]
    if len(set(heads)) != len(heads):
        return False
    return Fraction(sum(arcs[a][2] for a in cycle), len(cycle)) == mean


EXAMPLE = [(0, 1, 2), (1, 0, 4), (1, 2, 1), (2, 3, 1), (3, 1, 4), (3, 0, 0)]


def test_example() -> None:
    mean, cycle = karp_minimum_mean_cycle(4, EXAMPLE)
    assert mean == Fraction(1)
    assert check_cycle(EXAMPLE, cycle, mean)
    assert cycle == [2, 3, 5, 0]


def test_small_cases() -> None:
    assert karp_minimum_mean_cycle(0, []) is None
    assert karp_minimum_mean_cycle(1, []) is None
    assert karp_minimum_mean_cycle(1, [(0, 0, -3)]) == (Fraction(-3), [0])
    assert karp_minimum_mean_cycle(3, [(0, 1, 5), (1, 2, -9)]) is None
    # parallel arcs: the cheaper one is used
    got = karp_minimum_mean_cycle(2, [(0, 1, 3), (0, 1, 1), (1, 0, 1)])
    assert got is not None and got[0] == 1 and sorted(got[1]) == [1, 2]
    # isolated vertices and a loop away from a 2-cycle
    arcs = [(0, 1, 1), (1, 0, 1), (3, 3, 2)]
    got = karp_minimum_mean_cycle(5, arcs)
    assert got is not None and got[0] == 1 and sorted(got[1]) == [0, 1]


def test_fractions() -> None:
    arcs = [(0, 1, Fraction(1, 3)), (1, 0, Fraction(1, 6))]
    mean, cycle = karp_minimum_mean_cycle(2, arcs)
    assert mean == Fraction(1, 4)


def test_random_against_brute_force() -> None:
    rng = random.Random(1978)
    for _ in range(700):
        n = rng.randint(1, 6)
        m = rng.randint(0, 12)
        arcs = [(rng.randrange(n), rng.randrange(n), rng.randint(-5, 9)) for _ in range(m)]
        want = brute_min_mean(n, arcs)
        got = karp_minimum_mean_cycle(n, arcs)
        if want is None:
            assert got is None
        else:
            assert got is not None and got[0] == want
            assert check_cycle(arcs, got[1], want)
