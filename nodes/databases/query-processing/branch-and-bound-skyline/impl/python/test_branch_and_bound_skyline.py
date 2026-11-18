# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-bound-skyline/. The authors are listed in prov/G5JMTR.jsonl.

import random
from collections import Counter

from branch_and_bound_skyline import Node, all_nodes, bbs, build_rtree, dominates, skyline_bruteforce

NAMES = "abcdefghijkl"
P_EX = [(1, 9), (2, 10), (4, 8), (3, 6), (6, 7), (9, 10), (7, 5), (5, 4), (8, 3), (9, 1), (10, 4), (8, 8)]


def check_tree(points, root, cap):
    seen = Counter()
    for nd in all_nodes(root):
        assert 1 <= len(nd.children) <= cap
        for c in nd.children:
            lo, hi = (c.lo, c.hi) if isinstance(c, Node) else (points[c], points[c])
            assert all(a <= b for a, b in zip(nd.lo, lo)) and all(a >= b for a, b in zip(nd.hi, hi))
            if nd.leaf:
                seen[c] += 1
    assert seen == Counter(range(len(points)))


def test_example() -> None:
    root = build_rtree(P_EX, 3)
    check_tree(P_EX, root, 3)
    leaves = sorted("".join(sorted(NAMES[i] for i in nd.children)) for nd in all_nodes(root) if nd.leaf)
    assert leaves == ["abc", "deh", "fgl", "ijk"]
    sky, stats = bbs(P_EX, root)
    assert "".join(NAMES[i] for i in sky) == "hdaji"
    assert stats["nodes_read"] == 6 and len(all_nodes(root)) == 7


def test_dominance() -> None:
    assert dominates((1, 2), (1, 3)) and not dominates((1, 3), (1, 3))
    assert not dominates((0, 4), (1, 3)) and dominates((0, 0, 0), (0, 0, 1))


def test_random_against_bruteforce() -> None:
    rng = random.Random(8)
    for trial in range(120):
        dims = rng.choice([2, 3, 4])
        dom = rng.choice([3, 4, 5])
        n = rng.randrange(0, 200)
        pts = [tuple(rng.randrange(dom) for _ in range(dims)) for _ in range(n)]
        cap = rng.choice([2, 3, 4, 6])
        root = build_rtree(pts, cap)
        if pts:
            check_tree(pts, root, cap)
        sky, stats = bbs(pts, root)
        assert Counter(sky) == Counter(skyline_bruteforce(pts))
        keys = [sum(pts[i]) for i in sky]
        assert keys == sorted(keys)  # progressive: output in order of mindist
        # BBS reads exactly the nodes whose lower corner no point dominates.
        need = sum(1 for nd in all_nodes(root) if not any(dominates(p, nd.lo) for p in pts))
        assert stats["nodes_read"] == need


def test_edges_and_anticorrelated() -> None:
    assert bbs([], build_rtree([], 4)) == ([], {"nodes_read": 0, "max_heap": 0})
    assert bbs([(2, 3)], build_rtree([(2, 3)], 4))[0] == [0]
    same = [(1, 1, 1)] * 9
    assert sorted(bbs(same, build_rtree(same, 2))[0]) == list(range(9))
    diag = [(i, 49 - i) for i in range(50)]
    sky, stats = bbs(diag, build_rtree(diag, 4))
    assert sorted(sky) == list(range(50))
    assert stats["nodes_read"] == len(all_nodes(build_rtree(diag, 4)))
