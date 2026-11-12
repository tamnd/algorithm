# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contact-map/. The authors are listed in prov/3YNAR9.jsonl.

import math
import random

from contact_map import (contact_matrix, contact_pairs, distance_matrix, relative_contact_order,
                         separation_class)


def direct_pairs(points, cutoff, min_sep):
    """The O(n^2) definition: test every pair."""
    n = len(points)
    return {(i, j) for i in range(n) for j in range(i + min_sep, n) if math.dist(points[i], points[j]) < cutoff}


def hairpin():
    return [(3.8 * i, 0.0, 0.0) for i in range(4)] + [(3.8 * (7 - i), 4.8, 0.0) for i in range(4, 8)]


def test_example_of_the_page() -> None:
    pts = hairpin()
    pairs = contact_pairs(pts, 8.0, 3)
    assert sorted(pairs) == [(0, 6), (0, 7), (1, 5), (1, 6), (1, 7), (2, 5), (2, 6)]
    assert abs(relative_contact_order(pairs, 8) - 35 / 56) < 1e-12
    assert len(contact_pairs(pts, 8.0, 1)) == 20
    c = contact_matrix(8, pairs)
    assert all(c[i][j] == c[j][i] for i in range(8) for j in range(8))
    assert all(c[i][i] == 0 for i in range(8))
    d = distance_matrix(pts)
    assert abs(d[0][7] - 4.8) < 1e-12


def test_edges() -> None:
    assert contact_pairs([], 8.0) == set()
    assert contact_pairs([(1.0, 2.0, 3.0)], 8.0) == set()
    same = [(0.5, 0.5, 0.5)] * 5
    assert contact_pairs(same, 8.0) == {(i, j) for i in range(5) for j in range(i + 1, 5)}
    assert contact_pairs(same, 8.0, 3) == {(0, 3), (0, 4), (1, 4)}
    # exactly at the cutoff is not a contact; just below is
    assert contact_pairs([(0.0, 0.0, 0.0), (8.0, 0.0, 0.0)], 8.0) == set()
    assert contact_pairs([(0.0, 0.0, 0.0), (7.999, 0.0, 0.0)], 8.0) == {(0, 1)}
    # negative coordinates and points on cell borders
    assert contact_pairs([(-0.1, 0.0, 0.0), (0.1, 0.0, 0.0)], 8.0) == {(0, 1)}
    assert relative_contact_order(set(), 10) == 0.0


def test_separation_classes() -> None:
    assert separation_class(0, 5) == "local"
    assert separation_class(0, 6) == "short" and separation_class(11, 0) == "short"
    assert separation_class(0, 12) == "medium" and separation_class(0, 23) == "medium"
    assert separation_class(0, 24) == "long"


def random_chain(rng, n):
    """A random walk with steps of 3.8 A, a crude C-alpha trace."""
    p = [0.0, 0.0, 0.0]
    out = []
    for _ in range(n):
        out.append(tuple(p))
        v = [rng.gauss(0, 1) for _ in range(3)]
        s = math.sqrt(sum(c * c for c in v))
        p = [p[k] + 3.8 * v[k] / s for k in range(3)]
    return out


def test_cell_list_against_direct_check() -> None:
    rng = random.Random(8)
    for trial in range(600):
        n = rng.randint(0, 60)
        if trial % 2 == 0:
            pts = random_chain(rng, n)
        else:
            box = rng.uniform(1, 40)
            pts = [tuple(rng.uniform(-box, box) for _ in range(3)) for _ in range(n)]
        cutoff = rng.choice([4.0, 6.0, 8.0, rng.uniform(0.5, 15)])
        sep = rng.randint(1, 8)
        got = contact_pairs(pts, cutoff, sep)
        assert got == direct_pairs(pts, cutoff, sep)
        expect_co = sum(j - i for i, j in got) / (n * len(got)) if got else 0.0
        assert abs(relative_contact_order(got, n) - expect_co) < 1e-12
