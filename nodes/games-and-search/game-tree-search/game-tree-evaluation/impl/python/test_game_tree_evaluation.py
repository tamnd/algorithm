# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/game-tree-evaluation/. The authors are listed in prov/1ZVZRX.jsonl.

import math
import random
import unittest
from fractions import Fraction

from game_tree_evaluation import (
    Adversary,
    LeafCounter,
    adversary_tree,
    expected_reads,
    left_first_eval,
    nand_value,
    r_eval,
    root_known,
    run_query_algorithm,
    uniform_trees,
    worst_case_recurrence,
)


def random_tree(rng, depth, root=True):
    if depth == 0 or (not root and rng.random() < 0.2):
        return rng.randint(0, 1)
    return tuple(random_tree(rng, depth - 1, False) for _ in range(rng.randint(1, 3)))


def negamax01(t):
    """Brute force negamax with values 0 and 1: win if some move leads to a loss."""
    if not isinstance(t, tuple):
        return t
    return max(1 - negamax01(c) for c in t)


class TestValues(unittest.TestCase):
    def test_nand_is_negamax(self):
        rng = random.Random(2024)
        for _ in range(500):
            t = random_tree(rng, rng.randint(1, 6))
            self.assertEqual(nand_value(t), negamax01(t))

    def test_randomized_and_deterministic_are_always_right(self):
        rng = random.Random(77)
        for _ in range(500):
            t = random_tree(rng, rng.randint(1, 6))
            self.assertEqual(r_eval(t, rng, LeafCounter()), nand_value(t))
            self.assertEqual(left_first_eval(t, LeafCounter()), nand_value(t))


class TestRandomizedCost(unittest.TestCase):
    def test_worst_case_matches_the_recurrence(self):
        # Every uniform binary tree of height h <= 4 (65,536 trees at h = 4).
        for h in range(0, 5):
            worst = {0: Fraction(0), 1: Fraction(0)}
            for t in uniform_trees(h):
                v = nand_value(t)
                worst[v] = max(worst[v], expected_reads(t))
            c0, c1 = worst_case_recurrence(h)
            self.assertEqual((worst[0], worst[1]), (c0, c1), h)

    def test_page_table(self):
        table = [worst_case_recurrence(h) for h in range(7)]
        self.assertEqual(
            table,
            [
                (1, 1),
                (2, Fraction(3, 2)),
                (3, Fraction(11, 4)),
                (Fraction(11, 2), Fraction(35, 8)),
                (Fraction(35, 4), Fraction(123, 16)),
                (Fraction(123, 8), Fraction(403, 32)),
                (Fraction(403, 16), Fraction(1387, 64)),
            ],
        )
        # The ratio of successive terms tends to (1 + sqrt 33) / 4.
        lam = (1 + math.sqrt(33)) / 4
        c0, c1 = worst_case_recurrence(200)
        d0, d1 = worst_case_recurrence(201)
        self.assertAlmostEqual(float(max(d0, d1) / max(c0, c1)), lam, places=9)
        self.assertAlmostEqual(math.log2(lam), 0.7537, places=4)

    def test_simulation_agrees_with_the_exact_expectation(self):
        rng = random.Random(5)
        t = adversary_tree(4, 1)
        runs = 20000
        total = 0
        for _ in range(runs):
            c = LeafCounter()
            r_eval(t, rng, c)
            total += c.reads
        self.assertLess(abs(total / runs - float(expected_reads(t))), 0.1)

    def test_irregular_trees_never_cost_more_than_all_leaves(self):
        rng = random.Random(99)
        for _ in range(300):
            t = random_tree(rng, rng.randint(1, 5))
            leaves = [0]

            def count(u):
                if isinstance(u, tuple):
                    for c in u:
                        count(c)
                else:
                    leaves[0] += 1

            count(t)
            self.assertLessEqual(expected_reads(t), leaves[0])


class TestDeterministicLowerBound(unittest.TestCase):
    def test_left_first_reads_every_leaf_on_the_adversary_tree(self):
        for h in range(0, 9):
            for v in (0, 1):
                t = adversary_tree(h, v)
                c = LeafCounter()
                self.assertEqual(left_first_eval(t, c), v)
                self.assertEqual(c.reads, 2**h)

    def test_adversary_forces_every_deterministic_strategy_to_read_all_leaves(self):
        # Strategies that pick the next leaf by any fixed rule, also out of
        # depth-first order. Each one is deterministic once its seed is fixed.
        for h in range(1, 5):
            for seed in range(30):
                pick = random.Random(seed)

                def choose(known, unread, pick=pick):
                    return unread[pick.randrange(len(unread))]

                adv = Adversary(h)
                value, reads = run_query_algorithm(h, choose, adv.query)
                self.assertEqual(reads, 2**h)
                self.assertEqual(value, root_known(h, {i: adv.value[(0, i)] for i in range(2**h)}))

    def test_without_the_adversary_fewer_reads_can_suffice(self):
        # On a tree with a 0 leaf first, left-first reading stops early.
        c = LeafCounter()
        left_first_eval(((0, 1), (1, 1)), c)
        self.assertEqual(c.reads, 3)


if __name__ == "__main__":
    unittest.main()
