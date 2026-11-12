# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davies-bouldin-index/. The authors are listed in prov/7PAEH8.jsonl.

import random
from math import inf, isclose, sqrt

from davies_bouldin_index import davies_bouldin, scatters_and_centroids

POINTS = [(0, 0), (2, 0), (1, 3), (8, 0), (10, 0), (9, 3), (4, 8), (6, 8), (5, 11)]
GOOD = [0, 0, 0, 1, 1, 1, 2, 2, 2]
MERGED = [0, 0, 0, 0, 0, 0, 1, 1, 1]


def test_example_by_hand() -> None:
    # Each cluster of GOOD is a copy of (0,0), (2,0), (1,3) with centroid (1,1):
    # S = (sqrt 2 + sqrt 2 + 2) / 3. The centroids (1,1), (9,1), (5,9) are at
    # distances 8, sqrt 80 and sqrt 80. The worst ratio of each cluster uses the nearest centroid.
    s = (2 * sqrt(2) + 2) / 3
    _, scat, cents = scatters_and_centroids(POINTS, GOOD)
    assert all(isclose(x, s) for x in scat)
    assert cents == [[1, 1], [9, 1], [5, 9]]
    want = (2 * s / 8 + 2 * s / 8 + 2 * s / sqrt(80)) / 3
    assert isclose(davies_bouldin(POINTS, GOOD), want)
    assert isclose(davies_bouldin(POINTS, GOOD), 0.38821, abs_tol=5e-6)
    assert isclose(davies_bouldin(POINTS, MERGED), 0.73174, abs_tol=5e-6)


def test_one_dimensional() -> None:
    # Clusters {0, 2} and {10, 14}: S = 1 and 2, M = 11, DB = 3/11.
    assert isclose(davies_bouldin([(0,), (2,), (10,), (14,)], [0, 0, 1, 1]), 3 / 11)


def test_invariances_and_symmetric_parts() -> None:
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randrange(4, 15)
        pts = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]
        lab = [i % 3 for i in range(n)]
        db = davies_bouldin(pts, lab)
        moved = [(2.5 * x + 1, 2.5 * y - 4) for x, y in pts]
        assert isclose(davies_bouldin(moved, lab), db, rel_tol=1e-9)
        assert db >= 0


def test_coincident_centroids() -> None:
    assert davies_bouldin([(0,), (2,), (1,), (1,)], [0, 0, 1, 1]) == inf


def test_other_q_and_p() -> None:
    # q = 2 uses the root mean square distance; p = 1 the city block distance between centroids.
    pts = [(0, 0), (2, 0), (10, 0), (10, 4)]
    lab = [0, 0, 1, 1]
    s0, s1 = 1.0, 2.0
    assert isclose(davies_bouldin(pts, lab, q=2, p=1), (s0 + s1) / (9 + 2))
