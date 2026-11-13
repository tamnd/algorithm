# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax/. The authors are listed in prov/4KA77P.jsonl.

import itertools
import random
import unittest
from fractions import Fraction

from minimax import minimax, minimax_tree

PAGE_TREE = [[[3, 17], [2, 12]], [[15, 25], [2, 5]]]
RN_TREE = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]


def uniform_leaves(rng: random.Random, b: int, d: int) -> list:
    return [rng.randint(-20, 20) for _ in range(b**d)]


def build_uniform(leaves: list, b: int, d: int):
    if d == 0:
        return leaves[0]
    k = len(leaves) // b
    return [build_uniform(leaves[i * k : (i + 1) * k], b, d - 1) for i in range(b)]


def levelwise(leaves: list, b: int, d: int, max_root: bool = True):
    """Oracle without recursion: reduce the leaf row level by level, from the bottom."""
    row = list(leaves)
    for depth in range(d - 1, -1, -1):
        is_max = (depth % 2 == 0) == max_root
        f = max if is_max else min
        row = [f(row[i : i + b]) for i in range(0, len(row), b)]
    return row[0]


def random_tree(rng: random.Random, depth: int, root: bool = True):
    if depth == 0 or (not root and rng.random() < 0.25):
        return rng.randint(-9, 9)
    return [random_tree(rng, depth - 1, False) for _ in range(rng.randint(1, 3))]


def strategy_value(tree, max_root: bool = True):
    """Oracle by pure strategies: max over MAX strategies of min over MIN strategies
    of the leaf reached, and the same in the other order. Returns both numbers."""
    max_nodes, min_nodes = [], []

    def walk(node, path, is_max):
        if isinstance(node, list):
            (max_nodes if is_max else min_nodes).append((path, len(node)))
            for i, c in enumerate(node):
                walk(c, path + (i,), not is_max)

    walk(tree, (), max_root)

    def strategies(nodes):
        keys = [p for p, _ in nodes]
        for choice in itertools.product(*[range(k) for _, k in nodes]):
            yield dict(zip(keys, choice))

    def play(smax, smin):
        node, path, is_max = tree, (), max_root
        while isinstance(node, list):
            i = (smax if is_max else smin)[path]
            node, path, is_max = node[i], path + (i,), not is_max
        return node

    smaxs, smins = list(strategies(max_nodes)), list(strategies(min_nodes))
    maxmin = max(min(play(a, c) for c in smins) for a in smaxs)
    minmax = min(max(play(a, c) for a in smaxs) for c in smins)
    return maxmin, minmax, len(smaxs) * len(smins)


def strategy_pairs(tree, max_root: bool = True) -> int:
    counts = [1, 1]

    def walk(node, is_max):
        if isinstance(node, list):
            counts[0 if is_max else 1] *= len(node)
            for c in node:
                walk(c, not is_max)

    walk(tree, max_root)
    return counts[0] * counts[1]


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def ttt_winner(b: str):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_children(b: str):
    if ttt_winner(b) or "." not in b:
        return []
    p = "X" if b.count("X") == b.count("O") else "O"
    return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]


def ttt_utility(b: str) -> int:
    w = ttt_winner(b)
    return 1 if w == "X" else -1 if w == "O" else 0


class TestExamples(unittest.TestCase):
    def test_page_example(self):
        self.assertEqual(minimax_tree(PAGE_TREE), 12)
        self.assertEqual(minimax_tree(PAGE_TREE, max_to_move=False), 3)

    def test_russell_norvig_tree(self):
        self.assertEqual(minimax_tree(RN_TREE), 3)

    def test_single_leaf(self):
        self.assertEqual(minimax_tree(7), 7)
        self.assertEqual(minimax_tree([7]), 7)
        self.assertEqual(minimax_tree([[7]], max_to_move=False), 7)

    def test_fractions_stay_exact(self):
        t = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(2, 3), Fraction(1)]]
        self.assertEqual(minimax_tree(t), Fraction(2, 3))

    def test_tictactoe_centre_opening_is_a_draw(self):
        # X has taken the centre and O is to move: 25,872 complete games follow.
        count = [0]
        self.assertEqual(minimax("....X....", False, ttt_children, ttt_utility, count), 0)
        self.assertEqual(count[0], 25872)
        count = [0]
        self.assertEqual(minimax("X...O....", True, ttt_children, ttt_utility, count), 0)
        self.assertEqual(count[0], 3468)

    def test_tictactoe_forced_win(self):
        # X on 0 and 4, O on 1 and 8, X to move: X plays 3 and makes two threats.
        self.assertEqual(minimax("XO..X...O", True, ttt_children, ttt_utility), 1)


class TestAgainstOracles(unittest.TestCase):
    def test_uniform_trees_levelwise(self):
        rng = random.Random(20261113)
        for b in range(2, 5):
            for d in range(1, 7):
                if b**d > 5000:
                    continue
                for _ in range(15):
                    leaves = uniform_leaves(rng, b, d)
                    tree = build_uniform(leaves, b, d)
                    for max_root in (True, False):
                        count = [0]
                        v = minimax_tree(tree, max_root, count)
                        self.assertEqual(v, levelwise(leaves, b, d, max_root))
                        self.assertEqual(count[0], b**d)

    def test_irregular_trees_against_pure_strategies(self):
        rng = random.Random(7)
        checked = 0
        while checked < 300:
            tree = random_tree(rng, rng.randint(1, 4))
            max_root = rng.random() < 0.5
            if strategy_pairs(tree, max_root) > 4000:
                continue
            maxmin, minmax, _ = strategy_value(tree, max_root)
            v = minimax_tree(tree, max_root)
            self.assertEqual(v, maxmin)
            self.assertEqual(v, minmax)
            checked += 1

    def test_monotone_transformation_keeps_the_decision(self):
        rng = random.Random(99)
        for _ in range(200):
            leaves = uniform_leaves(rng, 3, 3)
            t1 = build_uniform(leaves, 3, 3)
            t2 = build_uniform([x**3 + 5 * x for x in leaves], 3, 3)
            v1 = [minimax_tree(c, False) for c in t1]
            v2 = [minimax_tree(c, False) for c in t2]
            self.assertEqual(v1.index(max(v1)), v2.index(max(v2)))


if __name__ == "__main__":
    unittest.main()
