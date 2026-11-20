# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friends-of-friends-algorithm/. The authors are listed in prov/HXVJ9V.jsonl.
import math
import random
from collections import deque

import pytest

from friends_of_friends_algorithm import friends_of_friends


def brute(x, b, min_size=1):
    """Reference: test all pairs, then breadth-first search for the components."""
    n = len(x)
    adj = [[j for j in range(n) if j != i and math.dist(x[i], x[j]) <= b] for i in range(n)]
    seen, out = [False] * n, []
    for s in range(n):
        if seen[s]:
            continue
        seen[s], comp, q = True, [], deque([s])
        while q:
            u = q.popleft()
            comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        if len(comp) >= min_size:
            out.append(sorted(comp))
    return sorted(out, key=lambda g: g[0])


def clustered(n, dim, seed):
    rng = random.Random(seed)
    centers = [tuple(rng.uniform(-5, 5) for _ in range(dim)) for _ in range(6)]
    pts = []
    for _ in range(n):
        if rng.random() < 0.3:
            pts.append(tuple(rng.uniform(-6, 6) for _ in range(dim)))
        else:
            c = rng.choice(centers)
            pts.append(tuple(c[k] + rng.gauss(0, 0.4) for k in range(dim)))
    return pts


def test_hand_example_on_a_line():
    x = [(0.0,), (0.15,), (0.3,), (1.0,), (1.1,), (2.5,)]
    assert friends_of_friends(x, 0.2) == [[0, 1, 2], [3, 4], [5]]
    assert friends_of_friends(x, 0.2, min_size=2) == [[0, 1, 2], [3, 4]]
    assert friends_of_friends(x, 0.12) == [[0], [1], [2], [3, 4], [5]]
    assert friends_of_friends(x, 1.5) == [[0, 1, 2, 3, 4, 5]]


@pytest.mark.parametrize("dim", [1, 2, 3])
@pytest.mark.parametrize("b", [0.2, 0.5, 1.0])
def test_against_brute_force(dim, b):
    x = clustered(250, dim, 10 * dim + int(10 * b))
    assert friends_of_friends(x, b) == brute(x, b)
    assert friends_of_friends(x, b, min_size=5) == brute(x, b, min_size=5)


def test_negative_coordinates_and_cell_boundaries():
    # Friends that sit in neighboring grid cells, including across zero.
    x = [(-0.05, 0.0), (0.05, 0.0), (0.95, 1.0), (1.05, 1.0), (-1.0, -1.0)]
    assert friends_of_friends(x, 0.2) == brute(x, 0.2) == [[0, 1], [2, 3], [4]]


def test_permutation_gives_same_partition():
    x = clustered(200, 3, 4)
    perm = list(range(200))
    random.Random(1).shuffle(perm)
    y = [x[p] for p in perm]
    a = {frozenset(g) for g in friends_of_friends(x, 0.5)}
    b = {frozenset(perm[i] for i in g) for g in friends_of_friends(y, 0.5)}
    assert a == b


def test_chaining_links_far_points():
    # Ten points 0.1 apart form one group with b = 0.1 even though the ends are 0.9 apart.
    x = [(0.1 * i + 1e-12 * i, 0.0) for i in range(10)]
    assert friends_of_friends(x, 0.1 + 1e-9) == [list(range(10))]


def test_bad_linking_length():
    with pytest.raises(ValueError):
        friends_of_friends([(0.0,)], 0.0)
