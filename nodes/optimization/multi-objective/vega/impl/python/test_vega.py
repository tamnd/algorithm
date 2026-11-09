# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vega/. The authors are listed in prov/3S4BQF.jsonl.

import itertools
import random
from fractions import Fraction as Fr

from vega import dominates, part_sizes, proportional_shares, vega, weighted_sum_shares


def sch(x):
    """Schaffer's function: minimize x^2 and (x - 2)^2."""
    return (x[0] ** 2, (x[0] - 2) ** 2)


def test_example_shares() -> None:
    # f = A(1, 9), B(6, 6), C(9, 1), D(7, 7); fitness g = 10 - f
    g = [(9, 1), (4, 4), (1, 9), (3, 3)]
    s = proportional_shares(g, 4)
    assert s == [Fr(20, 17), Fr(16, 17), Fr(20, 17), Fr(12, 17)]
    assert s == weighted_sum_shares(g, 4)
    assert sum(s) == 4


def test_identity_random() -> None:
    rng = random.Random(11)
    for _ in range(300):
        p = rng.randint(1, 4)
        n = p * rng.randint(1, 5)
        g = [tuple(Fr(rng.randint(1, 30)) for _ in range(p)) for _ in range(n)]
        assert proportional_shares(g, n) == weighted_sum_shares(g, n)
        assert sum(proportional_shares(g, n)) == n


def test_part_sizes() -> None:
    assert part_sizes(10, 3) == [4, 3, 3]
    assert part_sizes(6, 2) == [3, 3]
    for n in range(1, 30):
        for p in range(1, 6):
            assert sum(part_sizes(n, p)) == n


def test_run_invariants() -> None:
    for seed, n in [(1, 10), (2, 7), (3, 1), (4, 12)]:
        rng = random.Random(seed)

        def hook(pop):
            assert len(pop) == n
            for x, y in pop:
                assert -5 <= x[0] <= 5 and y == sch(x)

        out = vega(sch, 2, n, [-5], [5], 30, rng, on_generation=hook)
        assert out
        for (x, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)
        assert all(-5 <= x[0] <= 5 and y == sch(x) for x, y in out)


def test_three_objectives() -> None:
    rng = random.Random(8)

    def f(x):
        return (x[0], x[1], (1 - x[0]) + (1 - x[1]))

    out = vega(f, 3, 9, [0, 0], [1, 1], 15, rng)
    for (_, a), (_, b) in itertools.permutations(out, 2):
        assert not dominates(a, b)
