# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/little-algorithm/. The authors are listed in prov/10HFCT.jsonl.

import itertools
import random

from little_algorithm import INF, little, penalty_choice, reduce_matrix, tour_length

EXAMPLE = [
    [0, 13, 14, 2, 9],
    [17, 0, 16, 13, 10],
    [16, 12, 0, 19, 7],
    [17, 5, 10, 0, 5],
    [4, 20, 9, 18, 0],
]


def brute(cost):
    n = len(cost)
    best = INF
    for p in itertools.permutations(range(1, n)):
        best = min(best, tour_length(cost, (0,) + p))
    return best


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    trace: list = []
    z, tour = little(EXAMPLE, stats, trace)
    assert z == 34 and tour == [0, 3, 1, 2, 4]
    assert stats == {"nodes": 9, "expanded": 5}
    assert [v for _, v in trace] == [33, 33, 33, 34, 34, 34, 38]


def test_root_reduction_and_choice() -> None:
    n = len(EXAMPLE)
    m = [[INF if i == j else float(EXAMPLE[i][j]) for j in range(n)] for i in range(n)]
    assert reduce_matrix(m, range(n), range(n)) == 33
    assert penalty_choice(m, range(n), range(n)) == (0, 3, 10)


def test_small_sizes() -> None:
    assert little([]) == (0.0, [])
    assert little([[5]]) == (0.0, [0])
    assert little([[0, 3], [4, 0]]) == (7, [0, 1])
    assert little([[0, INF], [4, 0]]) == (INF, None)


def test_no_tour() -> None:
    # City 2 has no way out.
    c = [[0, 1, 1], [1, 0, 1], [INF, INF, 0]]
    assert little(c) == (INF, None)


def test_symmetric_square() -> None:
    # Four corners of a unit square, with distances 1 on the sides and 2 on the diagonals.
    c = [[0, 1, 2, 1], [1, 0, 1, 2], [2, 1, 0, 1], [1, 2, 1, 0]]
    z, tour = little(c)
    assert z == 4 and tour_length(c, tour) == 4


def test_zero_costs() -> None:
    z, tour = little([[0] * 6 for _ in range(6)])
    assert z == 0 and sorted(tour) == list(range(6))


def test_random_against_brute_force() -> None:
    rng = random.Random(20240611)
    for _ in range(700):
        n = rng.randint(2, 7)
        p = rng.choice([0.0, 0.1, 0.3])
        hi = rng.choice([3, 30, 1000])
        c = [[INF if rng.random() < p else rng.randint(0, hi) for _ in range(n)] for _ in range(n)]
        z, tour = little(c)
        assert z == brute(c)
        if tour is not None:
            assert sorted(tour) == list(range(n)) and tour[0] == 0
            assert tour_length(c, tour) == z


def test_larger_instance() -> None:
    rng = random.Random(7)
    n = 9
    c = [[rng.randint(1, 100) for _ in range(n)] for _ in range(n)]
    z, tour = little(c)
    assert z == brute(c) and tour_length(c, tour) == z
