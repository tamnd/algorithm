# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-setup-times/. The authors are listed in prov/KEC6PH.jsonl.

import itertools
import random

import pytest

from scheduling_with_setup_times import held_karp_setup, makespan, nearest_neighbor

P = [3, 2, 4, 1]
S0 = [2, 5, 1, 4]
S = [[0, 1, 6, 3], [4, 0, 2, 7], [5, 3, 0, 1], [9, 6, 4, 0]]


def brute(p, s0, s):
    return min((makespan(p, s0, s, o) for o in itertools.permutations(range(len(p)))), default=0)


def test_page_example() -> None:
    order, value = held_karp_setup(P, S0, S)
    assert order == [0, 1, 2, 3] and value == 16 == brute(P, S0, S)
    order, value = nearest_neighbor(P, S0, S)
    assert order == [2, 3, 1, 0] and value == 22


def test_held_karp_matches_brute_force() -> None:
    rng = random.Random(111)
    for _ in range(150):
        n = rng.randint(0, 7)
        p = [rng.randint(0, 9) for _ in range(n)]
        s0 = [rng.randint(0, 9) for _ in range(n)]
        s = [[0 if i == j else rng.randint(0, 9) for j in range(n)] for i in range(n)]
        order, value = held_karp_setup(p, s0, s)
        assert sorted(order) == list(range(n))
        assert value == makespan(p, s0, s, order) == brute(p, s0, s)
        assert nearest_neighbor(p, s0, s)[1] >= value


def test_sequence_independent_setups_do_not_matter() -> None:
    # s[i][j] = t[j]: every order costs sum p + sum t
    rng = random.Random(112)
    for _ in range(50):
        n = rng.randint(1, 6)
        p = [rng.randint(0, 9) for _ in range(n)]
        t = [rng.randint(0, 9) for _ in range(n)]
        s = [[t[j] for j in range(n)] for _ in range(n)]
        assert held_karp_setup(p, t, s)[1] == sum(p) + sum(t)


def test_family_setups_batch_each_family() -> None:
    # setup f[c] when the machine switches to family c, 0 inside a family
    rng = random.Random(113)
    for _ in range(50):
        n = rng.randint(1, 7)
        fam = [rng.randint(0, 2) for _ in range(n)]
        f = [rng.randint(1, 9) for _ in range(3)]
        p = [rng.randint(0, 9) for _ in range(n)]
        s0 = [f[fam[j]] for j in range(n)]
        s = [[0 if fam[i] == fam[j] else f[fam[j]] for j in range(n)] for i in range(n)]
        assert held_karp_setup(p, s0, s)[1] == sum(p) + sum(f[c] for c in set(fam))


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        held_karp_setup([1, 2], [0], [[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        held_karp_setup([1, 2], [0, 0], [[0, 1]])
