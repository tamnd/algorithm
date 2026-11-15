# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-fixpoint/. The authors are listed in prov/8YTFM5.jsonl.

import random
import unittest
from itertools import combinations

import lp
from alternating_fixpoint import alternating_trace, least_model_of_reduct, well_founded


def is_unfounded(program, u, true, false):
    """Van Gelder, Ross and Schlipf: each rule for an atom of u has a body literal false in (true, false) or a positive body atom in u."""
    for h, pos, neg in program:
        if h not in u:
            continue
        body_false = any(b in false for b in pos) or any(c in true for c in neg)
        if not body_false and not any(b in u for b in pos):
            return False
    return True


def wfm_by_unfounded_sets(program):
    """The least fixpoint of W_P(T, F) = (T_P(T, F), the greatest unfounded set), with the greatest unfounded set found by brute force."""
    universe = lp.atoms(program)
    true, false = frozenset(), frozenset()
    while True:
        new_true = frozenset(h for h, pos, neg in program if all(b in true for b in pos) and all(c in false for c in neg))
        gus = set()
        for k in range(1, len(universe) + 1):
            for u in combinations(universe, k):
                if is_unfounded(program, set(u), true, false):
                    gus.update(u)
        new_false = frozenset(gus)
        if (new_true, new_false) == (true, false):
            return true, false
        true, false = new_true, new_false


def random_stratified(rng, n_atoms, n_rules):
    """Atom a has level a // 3; positive body atoms have a level at most that of the head, negative ones a lower level."""
    program = []
    for _ in range(n_rules):
        h = rng.randrange(n_atoms)
        same_or_lower = [a for a in range(n_atoms) if a // 3 <= h // 3]
        lower = [a for a in range(n_atoms) if a // 3 < h // 3]
        pos = tuple(rng.sample(same_or_lower, rng.randint(0, min(2, len(same_or_lower)))))
        neg = tuple(rng.sample(lower, rng.randint(0, min(2, len(lower)))))
        program.append((h, pos, neg))
    return program


class TestAlternatingFixpoint(unittest.TestCase):
    def test_least_model_of_reduct_matches_lp(self):
        rng = random.Random(1)
        for _ in range(300):
            p = lp.random_program(rng, rng.randint(1, 8), rng.randint(0, 12))
            j = frozenset(a for a in range(8) if rng.random() < 0.5)
            self.assertEqual(least_model_of_reduct(p, j), lp.least_model(lp.reduct(p, j)))

    def test_equals_unfounded_set_definition(self):
        rng = random.Random(2)
        for _ in range(300):
            p = lp.random_program(rng, rng.randint(1, 7), rng.randint(0, 11))
            self.assertEqual(well_founded(p), wfm_by_unfounded_sets(p), p)

    def test_trace_is_monotone_and_short(self):
        rng = random.Random(3)
        for _ in range(300):
            p = lp.random_program(rng, rng.randint(1, 10), rng.randint(0, 16))
            trace = alternating_trace(p)
            self.assertLessEqual(len(trace), len(lp.atoms(p)) + 1)
            for (k0, u0), (k1, u1) in zip(trace, trace[1:]):
                self.assertTrue(k0 < k1, "K grows strictly until the fixpoint")
                self.assertTrue(u1 <= u0)
            for k, u in trace:
                self.assertTrue(k <= u)

    def test_inside_every_stable_model(self):
        rng = random.Random(4)
        for _ in range(150):
            p = lp.random_program(rng, rng.randint(1, 9), rng.randint(0, 14))
            true, false = well_founded(p)
            self.assertFalse(true & false)
            models = lp.stable_models(p)
            for m in models:
                self.assertTrue(true <= m and not (false & m))
            if len(true) + len(false) == len(lp.atoms(p)):
                self.assertEqual(models, [true], "a total well-founded model is the unique stable model")

    def test_stratified_programs_are_total(self):
        rng = random.Random(5)
        for _ in range(200):
            p = random_stratified(rng, 9, rng.randint(1, 14))
            true, false = well_founded(p)
            self.assertEqual(true | false, frozenset(lp.atoms(p)))
            self.assertEqual(lp.stable_models(p), [true])

    def test_page_example(self):
        # a <- not b.  b <- not a.  c <- not c.  d <- not e.  e <- e.  f <- d, not c.  g <- a.
        a, b, c, d, e, f, g = "abcdefg"
        p = [(a, (), (b,)), (b, (), (a,)), (c, (), (c,)), (d, (), (e,)), (e, (e,), ()), (f, (d,), (c,)), (g, (a,), ())]
        trace = alternating_trace(p)
        self.assertEqual(trace[0], (frozenset(), frozenset("abcdfg")))
        self.assertEqual(trace[1], (frozenset("d"), frozenset("abcdfg")))
        self.assertEqual(len(trace), 2)
        self.assertEqual(well_founded(p), (frozenset("d"), frozenset("e")))

    def test_win_move_game(self):
        # win(x) <- move(x, y), not win(y) on the moves 1->2, 2->3, 3->4, 5->6, 6->5.
        moves = [(1, 2), (2, 3), (3, 4), (5, 6), (6, 5)]
        p = [(x, (), (y,)) for x, y in moves] + [(4, (4,), ())]
        f = frozenset
        self.assertEqual(alternating_trace(p), [(f(), f({1, 2, 3, 5, 6})), (f({3}), f({1, 3, 5, 6})), (f({1, 3}), f({1, 3, 5, 6}))])
        true, false = well_founded(p)
        self.assertEqual(true, frozenset({1, 3}))
        self.assertEqual(false, frozenset({2, 4}))

    def test_atom_in_every_stable_model_but_undefined(self):
        # a <- not b.  b <- not a.  c <- a.  c <- b.
        p = [("a", (), ("b",)), ("b", (), ("a",)), ("c", ("a",), ()), ("c", ("b",), ())]
        self.assertEqual(well_founded(p), (frozenset(), frozenset()))
        self.assertEqual(lp.stable_models(p), [frozenset("ac"), frozenset("bc")])

    def test_empty_program(self):
        self.assertEqual(well_founded([]), (frozenset(), frozenset()))


if __name__ == "__main__":
    unittest.main()
