# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-shasha-algorithm/. The authors are listed in prov/Y3PPPP.jsonl.

import random
import sys
from functools import lru_cache

sys.dont_write_bytecode = True

from zhang_shasha_algorithm import tree_edit_distance  # noqa: E402


def nested(children, labels, v=0):
    return (labels[v], tuple(nested(children, labels, c) for c in children[v]))


def size(forest):
    return sum(1 + size(t[1]) for t in forest)


@lru_cache(maxsize=None)
def forest_dist(f, g, w=1):
    """Forest edit distance by the rightmost-root recursion, with deletion
    and insertion cost w and rename cost 0 or 1."""
    if not f:
        return w * size(g)
    if not g:
        return w * size(f)
    (a, fa), (b, gb) = f[-1], g[-1]
    return min(
        forest_dist(f[:-1] + fa, g, w) + w,
        forest_dist(f, g[:-1] + gb, w) + w,
        forest_dist(f[:-1], g[:-1], w) + forest_dist(fa, gb, w) + (a != b),
    )


def oracle(c1, l1, c2, l2, w=1):
    return forest_dist((nested(c1, l1),), (nested(c2, l2),), w)


def random_tree(n, rng, alphabet):
    parent = [-1] + [rng.randrange(i) for i in range(1, n)]
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    for ch in children:
        rng.shuffle(ch)
    return children, [rng.choice(alphabet) for _ in range(n)]


# T1 = f(d(a, c(b)), e) and T2 = f(c(d(a, b)), e), nodes numbered in preorder
C1 = [[1, 5], [2, 3], [], [4], [], []]
L1 = ["f", "d", "a", "c", "b", "e"]
C2 = [[1, 5], [2], [3, 4], [], [], []]
L2 = ["f", "c", "d", "a", "b", "e"]


def test_example():
    assert tree_edit_distance(C1, L1, C2, L2) == 2
    assert tree_edit_distance(C2, L2, C1, L1) == 2
    assert tree_edit_distance(C1, L1, C1, L1) == 0


def test_weighted_costs():
    d = tree_edit_distance(C1, L1, C2, L2, delete=lambda a: 3, insert=lambda b: 3,
                           rename=lambda a, b: 0 if a == b else 1)
    assert d == oracle(C1, L1, C2, L2, 3)


def test_single_vertex():
    assert tree_edit_distance([[]], ["a"], [[]], ["a"]) == 0
    assert tree_edit_distance([[]], ["a"], [[]], ["b"]) == 1


def test_star_and_path():
    n = 6
    star = [list(range(1, n))] + [[] for _ in range(n - 1)]
    path = [[i + 1] for i in range(n - 1)] + [[]]
    lab = ["x"] * n
    assert tree_edit_distance(star, lab, path, lab) == oracle(star, lab, path, lab)
    # a star minus k leaves
    assert tree_edit_distance(star, lab, [list(range(1, 3))] + [[], []], ["x"] * 3) == 3


def test_long_path():
    n = 100_000
    path = [[i + 1] for i in range(n - 1)] + [[]]
    lab = ["a"] * n
    assert tree_edit_distance(path, lab, [[]], ["a"]) == n - 1
    assert tree_edit_distance([[]], ["b"], path, lab) == n


def test_random_against_oracle():
    rng = random.Random(20240613)
    for _ in range(600):
        n1, n2 = rng.randint(1, 7), rng.randint(1, 7)
        c1, l1 = random_tree(n1, rng, "ab")
        c2, l2 = random_tree(n2, rng, "abc")
        w = rng.choice([1, 1, 2])
        d = tree_edit_distance(c1, l1, c2, l2, delete=lambda a: w, insert=lambda b: w)
        assert d == oracle(c1, l1, c2, l2, w)
        assert d == tree_edit_distance(c2, l2, c1, l1, delete=lambda a: w, insert=lambda b: w)


if __name__ == "__main__":
    test_example()
    test_weighted_costs()
    test_single_vertex()
    test_star_and_path()
    test_long_path()
    test_random_against_oracle()
    print("ok")
