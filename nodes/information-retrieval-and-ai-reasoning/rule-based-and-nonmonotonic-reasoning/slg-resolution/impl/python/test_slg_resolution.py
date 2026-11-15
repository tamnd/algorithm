# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slg-resolution/. The authors are listed in prov/N2VDR9.jsonl.

import random
import unittest
from itertools import combinations

import lp
from slg_resolution import SLG, slg


def wfm_alternating(program):
    """The well-founded model by the alternating fixpoint, written with the plain definitions of lp.py."""

    def s(j):
        return lp.least_model(lp.reduct(program, j))

    k = frozenset()
    while True:
        u = s(k)
        k_next = s(u)
        if k_next == k:
            return k, frozenset(lp.atoms(program)) - u
        k = k_next


def wfm_unfounded(program):
    """The well-founded model as the least fixpoint of W_P, with the greatest unfounded set found by brute force."""
    universe = lp.atoms(program)
    true, false = frozenset(), frozenset()
    while True:
        new_true = frozenset(h for h, pos, neg in program if all(b in true for b in pos) and all(c in false for c in neg))
        gus = set()
        for k in range(1, len(universe) + 1):
            for u in combinations(universe, k):
                u = set(u)
                if all(h not in u or any(b in false or b in u for b in pos) or any(c in true for c in neg) for h, pos, neg in program):
                    gus |= u
        if (new_true, frozenset(gus)) == (true, false):
            return true, false
        true, false = new_true, frozenset(gus)


def value_in(model, atom):
    true, false = model
    return "true" if atom in true else "false" if atom in false else "undefined"


def reachable(program, query):
    seen, todo = {query}, [query]
    while todo:
        a = todo.pop()
        for h, pos, neg in program:
            if h == a:
                for b in pos + neg:
                    if b not in seen:
                        seen.add(b)
                        todo.append(b)
    return seen


class TestSLG(unittest.TestCase):
    def check_program(self, p, model):
        for q in lp.atoms(p):
            got = slg(p, q)
            self.assertIn(q, got)
            self.assertTrue(set(got) <= reachable(p, q), "only atoms that the query reaches are tabled")
            for a, v in got.items():
                self.assertEqual(v, value_in(model, a), (p, q, a))

    def test_matches_unfounded_set_definition(self):
        rng = random.Random(11)
        for _ in range(150):
            p = lp.random_program(rng, rng.randint(1, 6), rng.randint(0, 10))
            self.check_program(p, wfm_unfounded(p))

    def test_matches_alternating_fixpoint(self):
        rng = random.Random(12)
        for _ in range(500):
            n = rng.randint(1, 12)
            p = lp.random_program(rng, n, rng.randint(0, 2 * n + 2), max_pos=rng.randint(0, 3), max_neg=rng.randint(0, 2))
            self.check_program(p, wfm_alternating(p))

    def test_rule_order_does_not_matter(self):
        rng = random.Random(13)
        for _ in range(200):
            p = lp.random_program(rng, 8, 14)
            model = wfm_alternating(p)
            shuffled = [(h, tuple(rng.sample(pos, len(pos))), tuple(rng.sample(neg, len(neg)))) for h, pos, neg in p]
            rng.shuffle(shuffled)
            self.check_program(shuffled, model)

    def test_delaying_and_answer_completion_are_used(self):
        rng = random.Random(14)
        totals = {"delayed": 0, "answer_completion": 0}
        for _ in range(400):
            p = lp.random_program(rng, 6, 10, max_pos=2, max_neg=1)
            for q in lp.atoms(p):
                e = SLG(p)
                e.run(q)
                for key in totals:
                    totals[key] += e.stats[key]
        self.assertGreater(totals["delayed"], 0)
        self.assertGreater(totals["answer_completion"], 0)

    def test_answer_completion_example(self):
        # a <- not b.  b <- c, b.  c <- not a.  c <- c, not c.
        # After completion, c keeps the answer c | {c, not c}, which only a positive loop supports.
        p = [("a", (), ("b",)), ("b", ("c", "b"), ()), ("c", (), ("a",)), ("c", ("c",), ("c",))]
        e = SLG(p)
        self.assertEqual(e.run("a"), {"a": "true", "b": "false", "c": "false"})
        self.assertEqual(e.stats["answer_completion"], 1)
        self.assertEqual(wfm_alternating(p), (frozenset("a"), frozenset("bc")))

    def test_page_example(self):
        # p <- not q.  q <- not p.  q <- r.  r <- r.
        p = [("p", (), ("q",)), ("q", (), ("p",)), ("q", ("r",), ()), ("r", ("r",), ())]
        e = SLG(p)
        self.assertEqual(e.run("p"), {"p": "undefined", "q": "undefined", "r": "false"})
        self.assertEqual(e.stats["delayed"], 2)
        self.assertEqual(e.tables["p"].answers, {frozenset({("-", "q")})})

    def test_loop_on_positive_recursion(self):
        # SLDNF resolution loops on these programs; SLG terminates.
        self.assertEqual(slg([("p", ("p",), ())], "p"), {"p": "false"})
        p = [("p", ("q",), ()), ("p", (), ("q",)), ("q", ("q",), ())]
        self.assertEqual(slg(p, "p"), {"p": "true", "q": "false"})
        self.assertEqual(slg([("p", (), ("p",))], "p"), {"p": "undefined"})

    def test_win_move_game(self):
        moves = [(1, 2), (2, 3), (3, 4), (5, 6), (6, 5)]
        p = [(x, (), (y,)) for x, y in moves]
        self.assertEqual(slg(p, 1), {1: "true", 2: "false", 3: "true", 4: "false"})
        self.assertEqual(slg(p, 5), {5: "undefined", 6: "undefined"})

    def test_atom_without_rules(self):
        self.assertEqual(slg([], "a"), {"a": "false"})


if __name__ == "__main__":
    unittest.main()
