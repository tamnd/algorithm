# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/side-chain-packing/. The authors are listed in prov/MMD1MC.jsonl.

import random
from fractions import Fraction

from side_chain_packing import brute_force, min_degree_order, pack, total_energy


def random_instance(rng: random.Random, n: int, p_max: int, edges):
    self_e = [[Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(rng.randint(1, p_max))] for _ in range(n)]
    pair_e = {}
    for i, j in edges:
        pair_e[(i, j)] = [[Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in self_e[j]] for _ in self_e[i]]
    return self_e, pair_e


def test_against_brute_force_random_graphs() -> None:
    rng = random.Random(31)
    for _ in range(250):
        n = rng.randint(1, 6)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.5]
        self_e, pair_e = random_instance(rng, n, 3, edges)
        e, x = pack(self_e, pair_e)
        best, _ = brute_force(self_e, pair_e)
        assert e == best
        assert total_energy(self_e, pair_e, x) == best


def test_chain_and_cycle() -> None:
    rng = random.Random(5)
    for n in range(2, 8):
        for edges in ([(i, i + 1) for i in range(n - 1)], [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]):
            self_e, pair_e = random_instance(rng, n, 3, edges)
            assert pack(self_e, pair_e)[0] == brute_force(self_e, pair_e)[0]


def test_widths() -> None:
    assert min_degree_order(5, [(0, 1), (1, 2), (2, 3), (3, 4)])[1] == 1
    assert min_degree_order(4, [(0, 1), (1, 2), (2, 3), (0, 3)])[1] == 2
    assert min_degree_order(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])[1] == 3


def test_page_example() -> None:
    # The example of the page: a chain of three residues with two rotamers each.
    self_e = [[0, 2], [1, 0], [0, 1]]
    pair_e = {(0, 1): [[0, 3], [0, 0]], (1, 2): [[0, 0], [2, 0]]}
    assert brute_force(self_e, pair_e) == (1, (0, 0, 0))
    assert pack(self_e, pair_e) == (1, (0, 0, 0))
