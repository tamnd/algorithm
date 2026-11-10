# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-cover-inapproximability/. The authors are listed in prov/H4FSRY.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

from set_cover_inapproximability import (
    cover_from_labeling,
    decode,
    expected_value,
    has_property,
    hypercube_system,
    is_cover,
    min_cover,
    random_system,
    reduce,
    regularize,
    value,
)


def random_game(rng, nu, nw, su, sw, m):
    edges = [(rng.randrange(nu), rng.randrange(nw), tuple(rng.randrange(sw) for _ in range(su))) for _ in range(m)]
    return nu, nw, su, sw, edges


def planted_game(rng, nu, nw, su, sw, m):
    """A game of value 1: fix labels, then make each projection agree with them."""
    left = [rng.randrange(su) for _ in range(nu)]
    right = [rng.randrange(sw) for _ in range(nw)]
    edges = []
    for _ in range(m):
        u, w = rng.randrange(nu), rng.randrange(nw)
        proj = [rng.randrange(sw) for _ in range(su)]
        proj[left[u]] = right[w]
        edges.append((u, w, tuple(proj)))
    return (nu, nw, su, sw, edges), left, right


def biregular_game(rng, nu, du, nw, dw, su, sw):
    assert nu * du == nw * dw
    lstubs = [u for u in range(nu) for _ in range(du)]
    rstubs = [w for w in range(nw) for _ in range(dw)]
    rng.shuffle(rstubs)
    edges = [(u, w, tuple(rng.randrange(sw) for _ in range(su))) for u, w in zip(lstubs, rstubs)]
    return nu, nw, su, sw, edges


def test_partition_systems() -> None:
    for labels in range(1, 5):
        m, cs = hypercube_system(labels)
        assert m == 2**labels
        assert has_property(m, cs, labels)
    for labels, h in ((3, 2), (4, 2), (3, 3)):
        m, cs = random_system(labels, h, seed=labels + h)
        assert m == math.ceil(2**h * h * math.log(2 * labels)) + 1
        assert has_property(m, cs, h)


def test_completeness_and_size() -> None:
    rng = random.Random(1)
    for _ in range(40):
        game, left, right = planted_game(rng, 3, 3, 3, 2, rng.randint(2, 6))
        n, sets, names = reduce(game, hypercube_system(2))
        assert n == len(game[4]) * 4
        assert len(sets) == 3 * 3 + 3 * 2
        cover = cover_from_labeling(game, left, right)
        assert len(cover) == 3 + 3 and is_cover(n, sets, cover)


def test_optimum_is_vertex_count_exactly_for_value_one() -> None:
    rng = random.Random(2)
    for trial in range(60):
        if trial % 2:
            game, _, _ = planted_game(rng, 2, 2, 2, 2, rng.randint(2, 4))
        else:
            game = random_game(rng, 2, 2, 2, 2, rng.randint(2, 4))
        used = {u for u, _, _ in game[4]}, {w for _, w, _ in game[4]}
        vertices = len(used[0]) + len(used[1])
        n, sets, _ = reduce(game, hypercube_system(2))
        opt = min_cover(n, sets)
        assert opt >= vertices
        assert (opt == vertices) == (value(game) == 1)


def test_decoding_bound() -> None:
    rng = random.Random(3)
    for _ in range(40):
        game = random_game(rng, 2, 2, 3, 2, rng.randint(2, 5))
        n, sets, names = reduce(game, hypercube_system(2))
        val = value(game)
        for size in range(1, 6):
            for chosen in combinations(range(len(sets)), size):
                if is_cover(n, sets, list(chosen)):
                    lu, lw = decode(game, names, list(chosen))
                    ev = expected_value(game, lu, lw)
                    bound = sum(Fraction(1, len(lu[u]) * len(lw[w])) for u, w, _ in game[4]) / len(game[4])
                    assert val >= ev >= bound


def test_regularize_keeps_value() -> None:
    rng = random.Random(4)
    for _ in range(20):
        game = biregular_game(rng, 2, 3, 3, 2, 2, 2)
        reg = regularize(game)
        assert reg[0] == reg[1] == 6
        assert len(reg[4]) == len(game[4]) * 6
        du = [sum(e[0] == u for e in reg[4]) for u in range(6)]
        dw = [sum(e[1] == w for e in reg[4]) for w in range(6)]
        assert len(set(du + dw)) == 1
        assert value(reg) == value(game)
