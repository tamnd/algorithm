# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/search-extensions/. The authors are listed in prov/42DKME.jsonl.

import random
import unittest

from search_extensions import INF, exact, forced_tail_tree, free_forced_value, mixed_tree, one_reply, plain, search


def no_extension(n, c):
    return 0


class TestSearchExtensions(unittest.TestCase):
    def test_forced_tails(self):
        # The page states: 600 trees, seed 31, b = 3, d = 2, forced lines of k = 1 to 4 moves;
        # the depth-2 search without extensions was wrong in 556 of them.
        rng = random.Random(31)
        differ = 0
        for i in range(600):
            k = 1 + i % 4
            kids, static = forced_tail_tree(rng, 3, 2, k)
            ext = one_reply(kids)
            truth = exact(kids, static, "r")
            self.assertEqual(truth, plain(kids, static, "r", 2 + k))
            self.assertEqual(search(kids, static, "r", 2, -INF, INF, ext, k), truth)
            self.assertEqual(search(kids, static, "r", 2, -INF, INF, ext, k + 3), truth)
            for budget in range(k + 1):
                # With a smaller budget the search equals a full search budget plies deeper.
                self.assertEqual(search(kids, static, "r", 2, -INF, INF, ext, budget), plain(kids, static, "r", 2 + budget))
            differ += search(kids, static, "r", 2, -INF, INF, no_extension, 0) != truth
        self.assertEqual(differ, 556)

    def test_mixed_trees_against_reference(self):
        rng = random.Random(32)
        for i in range(500):
            kids, static = mixed_tree(rng, 6)
            ext = one_reply(kids)
            depth, budget = 1 + i % 3, i % 4
            want = free_forced_value(kids, static, "r", depth, budget)
            self.assertEqual(search(kids, static, "r", depth, -INF, INF, ext, budget), want)
            a = rng.randint(-15, 15)
            b = a + rng.randint(1, 10)
            got = search(kids, static, "r", depth, a, b, ext, budget)
            if want <= a:
                self.assertTrue(want <= got <= a)
            elif want >= b:
                self.assertTrue(b <= got <= want)
            else:
                self.assertEqual(got, want)

    def test_budget_zero_is_plain_search(self):
        rng = random.Random(33)
        for _ in range(200):
            kids, static = mixed_tree(rng, 5)
            for d in range(4):
                self.assertEqual(search(kids, static, "r", d, -INF, INF, one_reply(kids), 0), plain(kids, static, "r", d))

    def test_budget_bounds_the_path_length(self):
        # A single forced line of 50 moves: the budget stops the extensions.
        kids = {str(i): [str(i + 1)] for i in range(50)}
        static = {str(i): (-1) ** i * i for i in range(51)}
        ext = one_reply(kids)
        c = [0]
        search(kids, static, "0", 1, -INF, INF, ext, 5, c)
        self.assertEqual(c[0], 1 + 1 + 5)


if __name__ == "__main__":
    unittest.main()
