# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-rooting/. The authors are listed in prov/7VS8ZC.jsonl.

import itertools
import random
from fractions import Fraction

from midpoint_rooting import clusters, distances_from, leaves, midpoint, root_tree


def make(edges):
    t = {}
    for u, v, w in edges:
        t.setdefault(u, {})[v] = w
        t.setdefault(v, {})[u] = w
    return t


def canonical(tree, u, v, t):
    """One name for a point of the tree: a vertex, or (edge, distance from its first end)."""
    if t == 0:
        return ("vertex", u)
    if t == tree[u][v]:
        return ("vertex", v)
    a, b = sorted([u, v], key=repr)
    return ("edge", a, b, t if a == u else tree[u][v] - t)


def brute_midpoints(tree):
    """The diameter by all pairs of leaves, and the midpoint of each longest leaf-to-leaf path."""
    ls = leaves(tree)
    dist = {x: distances_from(tree, x) for x in ls}
    D = max(dist[x][0][y] for x, y in itertools.combinations(ls, 2))
    pts = set()
    for x, y in itertools.combinations(ls, 2):
        if dist[x][0][y] != D:
            continue
        _, parent = dist[x]
        half = Fraction(D) / 2
        w = y
        dx = dist[x][0]
        while dx[parent[w]] > half:
            w = parent[w]
        p = parent[w]
        pts.add(canonical(tree, p, w, half - dx[p]))
    return D, pts


def random_tree(rng, n, zero=False):
    """A random unrooted tree with integer branch lengths, some internal vertices of high degree."""
    t = {"L0": {}, "L1": {}}
    w = rng.randint(0 if zero else 1, 9)
    t["L0"]["L1"] = t["L1"]["L0"] = w
    k = 0
    for i in range(2, n):
        if rng.random() < 0.3 and any(isinstance(v, int) for v in t):
            p = rng.choice([v for v in t if isinstance(v, int)])
        else:
            u = rng.choice(list(t))
            v = rng.choice(list(t[u]))
            ell = t[u].pop(v)
            del t[v][u]
            p = k
            k += 1
            a = rng.randint(0, ell)
            t[p] = {u: a, v: ell - a}
            t[u][p] = a
            t[v][p] = ell - a
        x = f"L{i}"
        ell = rng.randint(0 if zero else 1, 9)
        t[x] = {p: ell}
        t[p][x] = ell
    return t


def test_example_rate_variation():
    # The rooted tree ((A:1,B:6):1,(C:1,D:1):1), unrooted: the root edge P-Q has length 2.
    tree = make([("P", "A", 1), ("P", "B", 6), ("Q", "C", 1), ("Q", "D", 1), ("P", "Q", 2)])
    u, v, t, D = midpoint(tree)
    assert D == 9
    assert canonical(tree, u, v, t) == canonical(tree, "B", "P", Fraction(9, 2))
    root, ch, _ = root_tree(tree, u, v, t)
    assert clusters(root, ch) == {frozenset("ACD"), frozenset("CD")}  # not the true {A,B}, {C,D}


def test_example_ultrametric():
    # The rooted tree ((A:2,B:2):1,(C:1,D:1):2): every leaf is at distance 3 from the root.
    tree = make([("P", "A", 2), ("P", "B", 2), ("Q", "C", 1), ("Q", "D", 1), ("P", "Q", 3)])
    u, v, t, D = midpoint(tree)
    assert D == 6
    assert canonical(tree, u, v, t) == canonical(tree, "P", "Q", 1)
    root, ch, length = root_tree(tree, u, v, t)
    assert clusters(root, ch) == {frozenset("AB"), frozenset("CD")}
    assert length["P"] == 1 and length["Q"] == 2


def test_against_brute_force():
    rng = random.Random(2017)
    for _ in range(300):
        zero = rng.random() < 0.3
        tree = random_tree(rng, rng.randint(2, 14), zero=zero)
        u, v, t, D = midpoint(tree)
        D2, pts = brute_midpoints(tree)
        assert D == D2
        if not any(w == 0 for nb in tree.values() for w in nb.values()):
            assert len(pts) == 1  # all longest paths share one midpoint
            assert canonical(tree, u, v, t) in pts
        du, _ = distances_from(tree, u)
        dv, _ = distances_from(tree, v)
        far = max(min(du[y] + t, dv[y] + tree[u].get(v, 0) - t) if u != v else du[y] for y in leaves(tree))
        assert far == Fraction(D) / 2


def random_ultrametric(rng, n):
    """A random rooted binary tree with integer heights; leaves at height 0."""
    height = {f"L{i}": 0 for i in range(n)}
    pool = list(height)
    children = {}
    now = 0
    k = 0
    while len(pool) > 1:
        now += rng.randint(1, 5)
        a, b = rng.sample(pool, 2)
        p = ("v", k)
        k += 1
        height[p] = now
        children[p] = [a, b]
        pool = [x for x in pool if x not in (a, b)] + [p]
    return pool[0], children, height


def test_ultrametric_trees_are_rooted_correctly():
    rng = random.Random(1972)
    for _ in range(200):
        n = rng.randint(3, 25)
        root, children, height = random_ultrametric(rng, n)
        tree = {}
        for p, kids in children.items():
            if p == root:
                continue
            for c in kids:
                ell = height[p] - height[c]
                tree.setdefault(p, {})[c] = ell
                tree.setdefault(c, {})[p] = ell
        a, b = children[root]
        ell = 2 * height[root] - height[a] - height[b]
        tree.setdefault(a, {})[b] = ell
        tree.setdefault(b, {})[a] = ell
        want = {frozenset(c) for c in clusters(root, {**{v: [] for v in height}, **children})}
        u, v, t, D = midpoint(tree)
        assert D == 2 * height[root]
        r2, ch2, _ = root_tree(tree, u, v, t)
        got = {frozenset(c) for c in clusters(r2, ch2)}
        assert got == want


def test_floats_and_deep_path():
    n = 5000
    edges = [(i, i + 1, 0.5) for i in range(n)]
    edges += [(i, f"x{i}", 1.0) for i in range(1, n)]
    tree = make(edges)
    u, v, t, D = midpoint(tree)
    assert D == n * 0.5 + 1.0  # from x1 to x(n - 1)
    assert canonical(tree, u, v, t) in {("vertex", n // 2), canonical(tree, n // 2, n // 2 + 1, 0.25)}
