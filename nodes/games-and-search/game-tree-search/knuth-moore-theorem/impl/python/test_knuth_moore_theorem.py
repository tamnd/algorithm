# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-moore-theorem/. The authors are listed in prov/AZCEZ2.jsonl.

import random
import unittest
from fractions import Fraction

from knuth_moore_theorem import (
    alpha_beta,
    build_uniform,
    is_critical,
    leaf_paths,
    minimal_tree_size,
    minimax,
    no_cutoff_tree,
    perfectly_ordered,
    smallest_proof,
    to_negamax,
    worst_first,
)

# The tree of the Tightness section: values 1 to 16, children sorted worst first.
WORST_FIRST_EXAMPLE = [[[[12, 9], [14, 13]], [[10, 4], [16, 5]]], [[[11, 3], [15, 7]], [[2, 1], [8, 6]]]]


def leaves_for(rng, n, kind):
    if kind == "int":
        return [rng.randint(-5, 5) for _ in range(n)]  # many ties
    return [Fraction(rng.randint(-200, 200), rng.randint(1, 7)) for _ in range(n)]


class TestKnuthMoore(unittest.TestCase):
    def test_formula_values(self):
        self.assertEqual([minimal_tree_size(2, d) for d in range(1, 7)], [2, 3, 5, 7, 11, 15])
        self.assertEqual([minimal_tree_size(3, d) for d in range(1, 7)], [3, 5, 11, 17, 35, 53])
        self.assertEqual([minimal_tree_size(4, d) for d in range(1, 7)], [4, 7, 19, 31, 79, 127])

    def test_perfect_ordering_meets_the_formula_exactly(self):
        rng = random.Random(1975)
        for b in range(2, 5):
            for d in range(1, 7):
                for kind in ("int", "frac"):
                    for _ in range(3 if b**d > 500 else 8):
                        tree = perfectly_ordered(build_uniform(leaves_for(rng, b**d, kind), b, d))
                        for fs in (True, False):
                            seen = []
                            v = alpha_beta(to_negamax(tree), fail_soft=fs, visited=seen)
                            self.assertEqual(v, minimax(tree))
                            self.assertEqual(len(seen), minimal_tree_size(b, d))
                            # Exactly the critical leaves, as in Theorem 1 of Knuth and Moore.
                            self.assertEqual(set(seen), {p for p in leaf_paths(tree) if is_critical(p)})

    def test_no_cutoff_values_visit_every_leaf(self):
        rng = random.Random(7)
        for b in range(2, 5):
            for d in range(1, 7):
                vals = rng.sample(range(-10**6, 10**6), b**d)
                tree = no_cutoff_tree(vals, b, d)
                for fs in (True, False):
                    seen = []
                    self.assertEqual(alpha_beta(to_negamax(tree), fail_soft=fs, visited=seen), minimax(tree))
                    self.assertEqual(len(seen), b**d)

    def test_worst_first_sort_is_not_enough(self):
        t = WORST_FIRST_EXAMPLE
        self.assertEqual(worst_first(t), t)  # already sorted worst first at every node
        self.assertEqual(minimax(t), 6)
        seen = []
        alpha_beta(to_negamax(t), visited=seen)
        self.assertEqual(len(seen), 15)
        self.assertEqual([p for p in leaf_paths(t) if p not in seen], [(1, 1, 0, 1)])
        # Up to depth 3 the worst-first sort does give the full tree.
        rng = random.Random(3)
        for b in range(2, 5):
            for d in range(1, 4):
                for _ in range(20):
                    t = worst_first(build_uniform(rng.sample(range(10**6), b**d), b, d))
                    seen = []
                    alpha_beta(to_negamax(t), visited=seen)
                    self.assertEqual(len(seen), b**d)

    def test_every_order_needs_at_least_the_formula(self):
        rng = random.Random(42)
        for b in range(2, 5):
            for d in range(1, 6):
                for kind in ("int", "frac"):
                    for _ in range(10):
                        tree = build_uniform(leaves_for(rng, b**d, kind), b, d)
                        seen = []
                        alpha_beta(to_negamax(tree), visited=seen)
                        self.assertGreaterEqual(len(seen), minimal_tree_size(b, d))
                        self.assertLessEqual(len(seen), b**d)

    def test_brute_force_lower_bound_is_exact(self):
        # With an unbounded value range, the smallest set of leaves that fixes
        # the value has exactly the Knuth-Moore size, for every leaf values.
        rng = random.Random(11)
        for b, d in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (4, 1), (4, 2)]:
            for kind in ("int", "frac"):
                for _ in range(4):
                    tree = build_uniform(leaves_for(rng, b**d, kind), b, d)
                    self.assertEqual(smallest_proof(tree, -10**9, 10**9), minimal_tree_size(b, d))

    def test_bounded_values_break_the_lower_bound(self):
        # If 1 is the largest possible value, two leaves prove the value 1.
        t = [[1, 1], [1, 1]]
        self.assertEqual(smallest_proof(t, -1, 1), 2)
        self.assertEqual(smallest_proof(t, -2, 2), 3)


if __name__ == "__main__":
    unittest.main()
