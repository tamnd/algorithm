# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dulmage-mendelsohn-decomposition/. The authors are listed in prov/7KYG8D.jsonl.

import random
import unittest

from dulmage_mendelsohn_decomposition import dulmage_mendelsohn


def all_maximum_matchings(n_left, n_right, edges):
    """Every maximum matching, as a frozenset of edge indices, by enumeration."""
    best: list[frozenset[int]] = []
    best_size = -1

    def rec(i, used_l, used_r, chosen):
        nonlocal best, best_size
        if i == len(edges):
            if len(chosen) > best_size:
                best_size = len(chosen)
                best = []
            if len(chosen) == best_size:
                best.append(frozenset(chosen))
            return
        rec(i + 1, used_l, used_r, chosen)
        x, y = edges[i]
        if not used_l >> x & 1 and not used_r >> y & 1:
            chosen.append(i)
            rec(i + 1, used_l | 1 << x, used_r | 1 << y, chosen)
            chosen.pop()

    rec(0, 0, 0, [])
    return best_size, best


def oracle(n_left, n_right, edges):
    """The canonical parts, computed from all maximum matchings."""
    nu, mms = all_maximum_matchings(n_left, n_right, edges)
    missed_l = set()
    missed_r = set()
    allowed = set()
    for mm in mms:
        cov_l = {edges[i][0] for i in mm}
        cov_r = {edges[i][1] for i in mm}
        missed_l |= set(range(n_left)) - cov_l
        missed_r |= set(range(n_right)) - cov_r
        allowed |= mm
    xs_r = {y for (x, y) in edges if x in missed_l}
    ys_l = {x for (x, y) in edges if y in missed_r}
    sq_l = set(range(n_left)) - missed_l - ys_l
    sq_r = set(range(n_right)) - missed_r - xs_r
    # Blocks: components of the allowed edges inside the square part.
    parent = {("l", x): ("l", x) for x in sq_l}
    parent.update({("r", y): ("r", y) for y in sq_r})

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    for i in allowed:
        x, y = edges[i]
        if x in sq_l and y in sq_r:
            parent[find(("l", x))] = find(("r", y))
    groups: dict = {}
    for v in parent:
        groups.setdefault(find(v), set()).add(v)
    blocks = set()
    for g in groups.values():
        blocks.add(
            (
                tuple(sorted(v for s, v in g if s == "l")),
                tuple(sorted(v for s, v in g if s == "r")),
            )
        )
    return nu, (missed_l, xs_r), blocks, (ys_l, missed_r), allowed


def check(tc, n_left, n_right, edges, res):
    nu, xs, blocks, ys, allowed = oracle(n_left, n_right, edges)
    tc.assertEqual(res.size, nu)
    tc.assertEqual(sum(1 for y in res.mate_left if y >= 0), nu)
    for x, y in enumerate(res.mate_left):
        if y >= 0:
            tc.assertIn((x, y), set(edges))
            tc.assertEqual(res.mate_right[y], x)
    tc.assertEqual((set(res.x_surplus.left), set(res.x_surplus.right)), xs)
    tc.assertEqual((set(res.y_surplus.left), set(res.y_surplus.right)), ys)
    got_blocks = {(tuple(b.left), tuple(b.right)) for b in res.blocks}
    tc.assertEqual(got_blocks, blocks)
    for b in res.blocks:
        tc.assertEqual(len(b.left), len(b.right))
        tc.assertGreater(len(b.left), 0)
    # Surplus parts are strictly unbalanced when they are not empty.
    if res.x_surplus.left:
        tc.assertGreater(len(res.x_surplus.left), len(res.x_surplus.right))
    if res.y_surplus.right:
        tc.assertGreater(len(res.y_surplus.right), len(res.y_surplus.left))
    # Topological order: edges between blocks go from a left end in an
    # earlier block to a right end in a later one.
    where_l = {x: i for i, b in enumerate(res.blocks) for x in b.left}
    where_r = {y: i for i, b in enumerate(res.blocks) for y in b.right}
    for x, y in edges:
        if x in where_l and y in where_r:
            tc.assertLessEqual(where_l[x], where_r[y])
    # Allowed edges are exactly those inside one part or one block.
    for i, (x, y) in enumerate(edges):
        inside = (
            (x in xs[0] and y in xs[1])
            or (x in ys[0] and y in ys[1])
            or (x in where_l and y in where_r and where_l[x] == where_r[y])
        )
        tc.assertEqual(inside, i in allowed, (edges, x, y))


class TestDulmageMendelsohn(unittest.TestCase):
    def test_worked_example(self):
        # Left 1..6 -> 0..5, right a..f -> 0..5.
        edges = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 1), (3, 2),
                 (2, 3), (4, 3), (5, 3), (5, 4), (5, 5)]
        res = dulmage_mendelsohn(6, 6, edges)
        self.assertEqual(res.size, 5)
        self.assertEqual(res.x_surplus, ([0, 1], [0]))
        self.assertEqual(res.y_surplus, ([5], [4, 5]))
        self.assertEqual(res.blocks, [([2, 3], [1, 2]), ([4], [3])])
        check(self, 6, 6, edges, res)

    def test_empty_graph(self):
        res = dulmage_mendelsohn(0, 0, [])
        self.assertEqual((res.size, res.blocks), (0, []))
        res = dulmage_mendelsohn(3, 2, [])
        self.assertEqual(res.x_surplus, ([0, 1, 2], []))
        self.assertEqual(res.y_surplus, ([], [0, 1]))
        self.assertEqual(res.blocks, [])

    def test_perfect_matching_graphs(self):
        # An even cycle is one block; a perfect matching alone is n blocks.
        c6 = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 0)]
        res = dulmage_mendelsohn(3, 3, c6)
        self.assertEqual(res.blocks, [([0, 1, 2], [0, 1, 2])])
        check(self, 3, 3, c6, res)
        pm = [(0, 0), (1, 1), (2, 2)]
        res = dulmage_mendelsohn(3, 3, pm)
        self.assertEqual(len(res.blocks), 3)
        check(self, 3, 3, pm, res)

    def test_upper_triangular(self):
        # Edges (i, j) for i <= j: a chain of n one-by-one blocks in order.
        n = 6
        edges = [(i, j) for i in range(n) for j in range(i, n)]
        res = dulmage_mendelsohn(n, n, edges)
        self.assertEqual(res.blocks, [([i], [i]) for i in range(n)])
        check(self, n, n, edges, res)

    def test_no_perfect_matching(self):
        # Three left vertices share two right vertices: Hall's condition fails.
        edges = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 2)]
        res = dulmage_mendelsohn(4, 3, edges)
        self.assertEqual(res.size, 3)
        self.assertEqual(res.x_surplus, ([0, 1, 2], [0, 1]))
        check(self, 4, 3, edges, res)

    def test_star_and_long_path(self):
        star = [(0, j) for j in range(4)]
        res = dulmage_mendelsohn(1, 4, star)
        self.assertEqual(res.y_surplus, ([0], [0, 1, 2, 3]))
        check(self, 1, 4, star, res)
        n = 2000  # path x0 y0 x1 y1 ..., deep searches must not recurse
        path = [(i, i) for i in range(n)] + [(i + 1, i) for i in range(n - 1)]
        res = dulmage_mendelsohn(n, n, path)
        self.assertEqual(res.size, n)
        self.assertEqual(len(res.blocks), n)

    def test_bad_edge(self):
        with self.assertRaises(ValueError):
            dulmage_mendelsohn(1, 1, [(0, 1)])

    def test_random_against_brute_force(self):
        rng = random.Random(1958)
        for _ in range(600):
            nl = rng.randint(0, 6)
            nr = rng.randint(0, 6)
            p = rng.random()
            edges = [(x, y) for x in range(nl) for y in range(nr) if rng.random() < p]
            edges = edges[:14]
            rng.shuffle(edges)
            check(self, nl, nr, edges, dulmage_mendelsohn(nl, nr, edges))


if __name__ == "__main__":
    unittest.main()
