# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/df-pn/. The authors are listed in prov/PYWCCV.jsonl.

import random
import unittest

from df_pn import (
    INF,
    and_or_value,
    dfpn,
    mirror_numbers,
    nim_problem,
    numbers_from_children,
    proof_is_valid,
    random_tree,
    tic_tac_toe_problem,
    tree_problem,
)

PAGE_TREE = [[True, [False, False]], [[False, True], True], [False]]


def nim_sum(heaps):
    x = 0
    for h in heaps:
        x ^= h
    return x


def random_dag(rng, n, p_edge, p_true):
    """Vertices 0 .. n - 1 with edges from lower to higher numbers; a vertex
    without out-edges is terminal with a random value."""
    succ = {v: [w for w in range(v + 1, n) if rng.random() < p_edge] for v in range(n)}
    label = {v: rng.random() < p_true for v in range(n)}

    def children(v):
        return succ[v]

    def terminal(v, is_or):
        return label[v] if not succ[v] else None

    return 0, children, terminal


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        state, children, terminal = tree_problem(PAGE_TREE)
        log = []
        r = dfpn(state, children, terminal, on_mid=lambda s, o, a, b: log.append((s[0], o, a, b)))
        self.assertTrue(r.value)
        self.assertEqual(r.mid_calls, 5)
        self.assertEqual(
            log,
            [((), True, INF, INF), ((0,), False, 2, INF), ((0, 1), True, 2, INF), ((1,), False, 2, INF), ((1, 0), True, 2, INF)],
        )
        self.assertEqual(r.table[(state, True)], (0, INF))
        # the third child of the root is never searched
        third = ((2,), (False,))
        self.assertNotIn((third, False), r.table)


class TestTrees(unittest.TestCase):
    def test_random_trees_against_full_search(self):
        rng = random.Random(2002)
        for _ in range(300):
            tree = random_tree(rng, rng.randint(1, 7), (1, 4), rng.choice([0.3, 0.5, 0.7]))
            state, children, terminal = tree_problem(tree)
            for root_is_or in (True, False):
                for eps in (None, 0.25):
                    r = dfpn(state, children, terminal, root_is_or, epsilon=eps)
                    self.assertEqual(r.value, and_or_value(state, children, terminal, root_is_or))
                    if r.value:
                        self.assertTrue(proof_is_valid(r.table, state, root_is_or, children, terminal))
                    # on a tree, every stored interior entry obeys the rules
                    for (s, o), nums in r.table.items():
                        if terminal(s, o) is None and children(s):
                            self.assertEqual(nums, numbers_from_children(r.table, s, o, children, terminal))

    def test_expands_most_proving_nodes(self):
        rng = random.Random(5)
        checked = 0
        for _ in range(200):
            tree = random_tree(rng, rng.randint(2, 6), (1, 4), 0.5)
            state, children, terminal = tree_problem(tree)
            root_is_or = rng.random() < 0.5
            expanded = set()

            def on_expand(s, o):
                nonlocal checked
                # compare with the PNS tree that has expanded the same nodes
                base = mirror_numbers(state, root_is_or, expanded, children, terminal)
                proved = mirror_numbers(state, root_is_or, expanded, children, terminal, {(s, o): (0, INF)})
                disproved = mirror_numbers(state, root_is_or, expanded, children, terminal, {(s, o): (INF, 0)})
                self.assertEqual(proved[0], base[0] - 1)
                self.assertEqual(disproved[1], base[1] - 1)
                expanded.add((s, o))
                checked += 1

            dfpn(state, children, terminal, root_is_or, on_expand=on_expand)
        self.assertGreater(checked, 1000)


class TestGraphs(unittest.TestCase):
    def test_nim_with_transpositions(self):
        for heaps in [(1,), (1, 1), (1, 2, 3), (2, 3, 4), (1, 2, 4), (3, 3), (2, 2, 3), (3, 5, 7), (1, 4, 5), (2, 4, 6)]:
            state, children, terminal = nim_problem(heaps)
            for eps in (None, 0.25):
                r = dfpn(state, children, terminal, epsilon=eps)
                self.assertEqual(r.value, nim_sum(heaps) != 0, heaps)

    def test_tic_tac_toe(self):
        state, children, terminal = tic_tac_toe_problem("not lose")
        r = dfpn(state, children, terminal)
        self.assertTrue(r.value)
        self.assertTrue(proof_is_valid(r.table, state, True, children, terminal))
        self.assertLess(r.expanded, 5478)  # fewer than the reachable positions
        state, children, terminal = tic_tac_toe_problem("win")
        self.assertFalse(dfpn(state, children, terminal).value)
        self.assertFalse(dfpn(state, children, terminal, epsilon=0.25).value)

    def test_random_dags(self):
        rng = random.Random(2008)
        for _ in range(300):
            n = rng.randint(2, 25)
            state, children, terminal = random_dag(rng, n, rng.choice([0.15, 0.3, 0.5]), 0.5)
            for root_is_or in (True, False):
                r = dfpn(state, children, terminal, root_is_or, max_mid_calls=200000)
                self.assertIsNotNone(r.value)
                self.assertEqual(r.value, and_or_value(state, children, terminal, root_is_or))

    def test_budget(self):
        state, children, terminal = tic_tac_toe_problem("win")
        r = dfpn(state, children, terminal, max_mid_calls=20)
        self.assertIsNone(r.value)


if __name__ == "__main__":
    unittest.main()
