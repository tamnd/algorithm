# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-geography/. The authors are listed in prov/261S19.jsonl.

import random
import unittest

from generalized_geography import (
    edge_geography_first_wins,
    qbf_to_geography,
    qbf_true,
    random_graph,
    undirected_vertex_geography_by_matching,
    vertex_geography_first_wins,
    vertex_geography_plain,
)


class TestVertexGeography(unittest.TestCase):
    def test_page_example(self):
        # a=0, b=1, c=2, d=3, e=4
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 1)]
        got = [vertex_geography_first_wins(5, edges, s) for s in range(5)]
        self.assertEqual(got, [True, False, True, False, False])
        # after a -> c (a is used), the player to move at c wins, so a -> c loses
        self.assertTrue(vertex_geography_first_wins(5, [(2, 3), (3, 4), (4, 1), (1, 3)], 2))

    def test_memo_matches_plain_search(self):
        rng = random.Random(1978)
        for _ in range(300):
            n = rng.randint(1, 8)
            edges = random_graph(rng, n, rng.choice([0.2, 0.35, 0.5]))
            s = rng.randrange(n)
            self.assertEqual(vertex_geography_first_wins(n, edges, s), vertex_geography_plain(n, edges, s))

    def test_cycle_of_length_n(self):
        for n in range(2, 12):
            edges = [(i, (i + 1) % n) for i in range(n)]
            # the play visits every vertex once: n - 1 moves
            self.assertEqual(vertex_geography_first_wins(n, edges, 0), (n - 1) % 2 == 1)


class TestUndirected(unittest.TestCase):
    def test_matching_criterion(self):
        rng = random.Random(1993)
        for _ in range(400):
            n = rng.randint(1, 9)
            edges = random_graph(rng, n, rng.choice([0.2, 0.35, 0.5]), undirected=True)
            s = rng.randrange(n)
            self.assertEqual(
                vertex_geography_first_wins(n, edges, s, undirected=True),
                undirected_vertex_geography_by_matching(n, edges, s),
                (n, edges, s),
            )


class TestEdgeGeography(unittest.TestCase):
    def test_small_cases(self):
        # one directed edge: first player moves and wins
        self.assertTrue(edge_geography_first_wins(2, [(0, 1)], 0))
        # a directed triangle: three moves, first player makes the last one
        self.assertTrue(edge_geography_first_wins(3, [(0, 1), (1, 2), (2, 0)], 0))
        # two parallel paths of length two from 0
        self.assertFalse(edge_geography_first_wins(5, [(0, 1), (1, 2), (0, 3), (3, 4)], 0))

    def test_edges_may_revisit_vertices(self):
        # a figure eight through vertex 0: four moves, second player wins
        edges = [(0, 1), (1, 0), (0, 2), (2, 0)]
        self.assertFalse(edge_geography_first_wins(3, edges, 0))
        self.assertTrue(vertex_geography_first_wins(3, edges, 0))


class TestReduction(unittest.TestCase):
    def test_random_formulas(self):
        rng = random.Random(1980)
        trues = falses = 0
        for _ in range(250):
            nv = rng.randint(1, 5)
            clauses = []
            for _ in range(rng.randint(1, 5)):
                vs = rng.sample(range(1, nv + 1), rng.randint(1, min(3, nv)))
                clauses.append([v if rng.random() < 0.5 else -v for v in vs])
            n, edges, start = qbf_to_geography(nv, clauses)
            got = vertex_geography_first_wins(n, edges, start)
            want = qbf_true(nv, clauses)
            self.assertEqual(got, want, (nv, clauses))
            trues += want
            falses += not want
        self.assertGreater(trues, 20)
        self.assertGreater(falses, 20)

    def test_page_formula(self):
        # exists x1 forall x2 exists x3: (x1 or x2) and (not x2 or x3) and (not x1 or not x3)
        clauses = [[1, 2], [-2, 3], [-1, -3]]
        self.assertFalse(qbf_true(3, clauses))
        n, edges, start = qbf_to_geography(3, clauses)
        self.assertEqual((n, len(edges)), (16, 24))
        self.assertFalse(vertex_geography_first_wins(n, edges, start))


if __name__ == "__main__":
    unittest.main()
