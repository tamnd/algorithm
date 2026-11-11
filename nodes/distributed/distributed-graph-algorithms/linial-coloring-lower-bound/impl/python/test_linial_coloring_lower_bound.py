# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linial-coloring-lower-bound/. The authors are listed in prov/781NR6.jsonl.

import itertools
import math
import random

from linial_coloring_lower_bound import (
    chromatic_number,
    colourable,
    is_proper_kary,
    neighbourhood_graph,
    reduce_colouring,
    shift_graph,
    tower_bound,
)


def test_zero_rounds_is_complete_graph() -> None:
    for n in range(2, 6):
        _, adj = neighbourhood_graph(0, n)
        assert chromatic_number(adj) == n


def test_shift_graph_needs_log_colours() -> None:
    for n in range(2, 10):
        _, adj = shift_graph(n, 2)
        assert chromatic_number(adj) == math.ceil(math.log2(n))


def test_one_round_neighbourhood_graph() -> None:
    expected = {4: 2, 5: 3, 6: 3}
    for n, chi in expected.items():
        _, adj = neighbourhood_graph(1, n)
        assert chromatic_number(adj) == chi
        _, sub = shift_graph(n, 3)
        assert chromatic_number(sub) <= chi
    _, sub = shift_graph(7, 3)
    assert chromatic_number(sub) == 3


def random_proper(n: int, k: int, c: int, rng: random.Random) -> dict | None:
    verts, adj = shift_graph(n, k)
    col = colourable(adj, c)
    if col is None:
        return None
    perm = list(range(c))
    rng.shuffle(perm)
    return {verts[i]: perm[col[i]] for i in range(len(verts))}


def test_reduction_step() -> None:
    rng = random.Random(5)
    for k in (2, 3):
        for n in range(k + 1, 9):
            for c in (3, 4):
                f = random_proper(n, k, c, rng)
                if f is None:
                    continue
                assert is_proper_kary(f, n, k)
                g = reduce_colouring(f, n, k)
                assert is_proper_kary(g, n, k - 1)
                assert len(set(g.values())) <= 2**c


def test_tower_bound_against_exact_values() -> None:
    for n in range(2, 10):
        chi1 = chromatic_number(shift_graph(n, 1)[1])
        assert n <= tower_bound(1, chi1)
        chi2 = chromatic_number(shift_graph(n, 2)[1])
        assert n <= tower_bound(2, chi2)
    assert tower_bound(3) == 2**8 and tower_bound(4) == 2**256


def test_views_of_consecutive_nodes() -> None:
    # Every pair of consecutive windows on a directed cycle is an edge of B(t, n).
    n, t = 6, 1
    verts, adj = neighbourhood_graph(t, n)
    index = {v: i for i, v in enumerate(verts)}
    for perm in itertools.permutations(range(n)):
        w = [tuple(perm[(j + d) % n] for d in range(-t, t + 1)) for j in range(n)]
        for j in range(n):
            assert index[w[(j + 1) % n]] in adj[index[w[j]]]
