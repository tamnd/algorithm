# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dead-end-elimination/. The authors are listed in prov/161ER1.jsonl.

import random
from fractions import Fraction

from dead_end_elimination import (
    brute_force,
    dead_end_elimination,
    desmet,
    goldstein,
    solve,
    total_energy,
)

# The worked example of the page: three residues with 3, 2 and 2 rotamers.
EX_SELF = [[3, 4, 0], [0, 0], [1, 0]]
EX_PAIR = {
    (0, 1): [[0, 1], [0, 0], [0, 3]],
    (0, 2): [[0, 2], [0, 0], [0, 0]],
    (1, 2): [[3, 1], [0, 0]],
}


def random_instance(rng: random.Random, n: int, p_max: int, density: float):
    self_e = [[Fraction(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(rng.randint(1, p_max))] for _ in range(n)]
    pair_e = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                pair_e[(i, j)] = [[Fraction(rng.randint(-6, 6), rng.randint(1, 3)) for _ in self_e[j]] for _ in self_e[i]]
    return self_e, pair_e


def test_worked_example() -> None:
    assert dead_end_elimination(EX_SELF, EX_PAIR, "desmet") == [[0, 2], [0, 1], [0, 1]]
    assert dead_end_elimination(EX_SELF, EX_PAIR, "goldstein") == [[2], [0], [1]]
    best, argmins = brute_force(EX_SELF, EX_PAIR)
    assert best == 1 and argmins == [(2, 0, 1)]
    assert solve(EX_SELF, EX_PAIR)[:2] == (1, (2, 0, 1))
    # Rotamer 0 of residue 0 ties with rotamer 2 under Desmet (3 against 3), so it stays.
    full = [[0, 1, 2], [0, 1], [0, 1]]
    assert not desmet(EX_SELF, EX_PAIR, full, 0, 0, 2)
    assert goldstein(EX_SELF, EX_PAIR, full, 0, 0, 2)


def test_global_minimum_survives() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        n = rng.randint(1, 5)
        self_e, pair_e = random_instance(rng, n, 3, rng.choice([0.3, 0.7, 1.0]))
        best, argmins = brute_force(self_e, pair_e)
        for crit in ("desmet", "goldstein"):
            live = dead_end_elimination(self_e, pair_e, crit)
            assert all(live[i] for i in range(n))
            e, x, _ = solve(self_e, pair_e, crit)
            assert e == best and total_energy(self_e, pair_e, x) == best
            # Every global minimum, not only one of them, uses live rotamers.
            for xm in argmins:
                assert all(xm[i] in live[i] for i in range(n))


def test_goldstein_at_least_as_strong() -> None:
    rng = random.Random(7)
    strictly = 0
    for _ in range(300):
        n = rng.randint(2, 5)
        self_e, pair_e = random_instance(rng, n, 4, 0.8)
        full = [list(range(len(row))) for row in self_e]
        # On the same live sets, the Desmet test implies the Goldstein test.
        for i in range(n):
            for r in full[i]:
                for t in full[i]:
                    if t != r and desmet(self_e, pair_e, full, i, r, t):
                        assert goldstein(self_e, pair_e, full, i, r, t)
        # At the fixed points, Goldstein keeps a subset of what Desmet keeps.
        d = dead_end_elimination(self_e, pair_e, "desmet")
        g = dead_end_elimination(self_e, pair_e, "goldstein")
        assert all(set(g[i]) <= set(d[i]) for i in range(n))
        strictly += sum(len(d[i]) - len(g[i]) for i in range(n)) > 0
    assert strictly > 0


def test_order_does_not_change_the_result() -> None:
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(2, 5)
        self_e, pair_e = random_instance(rng, n, 4, 0.8)
        for crit in ("desmet", "goldstein"):
            base = dead_end_elimination(self_e, pair_e, crit)
            for _ in range(3):
                assert dead_end_elimination(self_e, pair_e, crit, rng) == base


def test_coloring_instance_has_no_dead_ends() -> None:
    # Graph 3-coloring as packing: a clash of 1 for equal colours on an edge.
    # Each rotamer then has G = -(degree) < 0 against each competitor.
    edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
    self_e = [[0, 0, 0] for _ in range(4)]
    pair_e = {e: [[1 if a == b else 0 for b in range(3)] for a in range(3)] for e in edges}
    assert dead_end_elimination(self_e, pair_e) == [[0, 1, 2]] * 4
    assert brute_force(self_e, pair_e)[0] == 0


def test_no_pairs_keeps_only_minima() -> None:
    # With no pair terms, both tests keep exactly the rotamers of least self energy.
    # The two tied rotamers both stay, because each test is a strict inequality.
    self_e = [[3, 1, 1, 4], [Fraction(1, 2), Fraction(1, 3)]]
    assert dead_end_elimination(self_e, {}, "goldstein") == [[1, 2], [1]]
    assert dead_end_elimination(self_e, {}, "desmet") == [[1, 2], [1]]
