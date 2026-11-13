# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-number-search/. The authors are listed in prov/8X9ESA.jsonl.

import random
import unittest

from proof_number_search import (
    INF,
    and_or_value,
    is_most_proving,
    nim_problem,
    proof_number_search,
    proof_tree_is_valid,
    random_tree,
    rules_hold,
    tic_tac_toe_problem,
    tree_problem,
)

PAGE_TREE = [[True, [False, False]], [[False, True], True], [False]]


def nim_sum(heaps):
    x = 0
    for h in heaps:
        x ^= h
    return x


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        state, children, terminal = tree_problem(PAGE_TREE)
        log = []
        r = proof_number_search(state, children, terminal, on_select=lambda root, n: log.append((n.state[0], root.pn, root.dn)))
        self.assertTrue(r.value)
        self.assertEqual(r.expansions, 5)
        # the node chosen at each step, with the root numbers before the step
        self.assertEqual(log, [((), 1, 1), ((0,), 1, 3), ((0, 1), 1, 2 + 1), ((1,), 1, 2), ((1, 0), 1, 2)])
        self.assertEqual((r.root.pn, r.root.dn), (0, INF))
        # the third child is never expanded
        self.assertIsNone(r.root.children[2].children)


class TestAgainstFullSearch(unittest.TestCase):
    def test_random_trees(self):
        rng = random.Random(1994)
        proved = disproved = 0
        for _ in range(300):
            tree = random_tree(rng, rng.randint(1, 7), (1, 4), rng.choice([0.3, 0.5, 0.7]))
            state, children, terminal = tree_problem(tree)
            for root_is_or in (True, False):
                r = proof_number_search(state, children, terminal, root_is_or)
                want = and_or_value(state, children, terminal, root_is_or)
                self.assertEqual(r.value, want)
                self.assertTrue(rules_hold(r.root))
                if r.value:
                    self.assertTrue(proof_tree_is_valid(r.root))
                proved += want
                disproved += not want
        self.assertGreater(proved, 100)
        self.assertGreater(disproved, 100)

    def test_nim(self):
        for heaps in [(1,), (1, 1), (1, 2), (1, 2, 3), (2, 3, 4), (1, 2, 4), (3, 3), (2, 2, 3), (1, 3, 5), (4, 4)]:
            state, children, terminal = nim_problem(heaps)
            r = proof_number_search(state, children, terminal)
            self.assertEqual(r.value, nim_sum(heaps) != 0, heaps)
            self.assertEqual(r.value, and_or_value(state, children, terminal))
            self.assertTrue(rules_hold(r.root))

    def test_tic_tac_toe(self):
        state, children, terminal = tic_tac_toe_problem("win")
        r = proof_number_search(state, children, terminal)
        self.assertFalse(r.value)  # X cannot force a win
        self.assertTrue(rules_hold(r.root))
        state, children, terminal = tic_tac_toe_problem("not lose")
        r = proof_number_search(state, children, terminal)
        self.assertTrue(r.value)  # but X cannot lose
        self.assertTrue(proof_tree_is_valid(r.root))
        # the proof needs far fewer expansions than the 549,946 nodes of the full tree
        self.assertLess(r.expansions, 1000)
        # X to move after X took a corner and O the center: X still cannot lose
        state, children, terminal = tic_tac_toe_problem("not lose", "X...O....")
        self.assertTrue(proof_number_search(state, children, terminal).value)


class TestMostProvingNode(unittest.TestCase):
    def test_selected_nodes_are_most_proving(self):
        rng = random.Random(42)
        checked = 0
        for _ in range(150):
            tree = random_tree(rng, rng.randint(2, 6), (1, 4), 0.5)
            state, children, terminal = tree_problem(tree)

            def check(root, node):
                nonlocal checked
                self.assertTrue(rules_hold(root))
                self.assertTrue(0 < root.pn < INF and 0 < root.dn < INF)
                self.assertIsNone(node.children)
                self.assertIsNone(node.value)
                self.assertTrue(is_most_proving(root, node))
                checked += 1

            proof_number_search(state, children, terminal, rng.random() < 0.5, on_select=check)
        self.assertGreater(checked, 500)

    def test_budget(self):
        state, children, terminal = tic_tac_toe_problem("win")
        r = proof_number_search(state, children, terminal, max_expansions=10)
        self.assertIsNone(r.value)
        self.assertEqual(r.expansions, 10)


if __name__ == "__main__":
    unittest.main()
