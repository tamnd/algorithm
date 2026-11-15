# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farkas-invariant-generation/. The authors are listed in prov/K23N8A.jsonl.

import itertools
import random
import unittest
from fractions import Fraction

from farkas_invariant_generation import Loop, affine, equal, holds, invariant_for
from fraclp import lp_solve


def dot(a, x):
    return sum(Fraction(ai) * xi for ai, xi in zip(a, x))


def primal_inductive(loop, c, d):
    """The oracle: maximize c . x over Init and c . x' over each transition
    from c . x + d <= 0, exactly, and compare with -d."""
    n = loop.n
    st, _, val = lp_solve([-v for v in c], a_ub=[a for a, _ in loop.init], b_ub=[b for _, b in loop.init], free=range(n))
    if st == "unbounded" or (st == "optimal" and -val + d > 0):
        return False
    for t in loop.trans:
        a_ub = [a for a, _ in t] + [list(c) + [0] * n]
        b_ub = [b for _, b in t] + [-d]
        st, _, val = lp_solve([0] * n + [-v for v in c], a_ub=a_ub, b_ub=b_ub, free=range(2 * n))
        if st == "unbounded" or (st == "optimal" and -val + d > 0):
            return False
    return True


def certificate(loop, c, d, mus=None):
    """Whether Farkas multipliers exist for the fixed inequality (c, d).
    With mus = None the multiplier mu of consecution is a free unknown
    mu >= 0, so every condition is linear; otherwise mu is taken from mus."""
    n = loop.n
    m0 = len(loop.init)
    a_eq = [[a[k] for a, _ in loop.init] for k in range(n)]
    b_eq = [c[k] for k in range(n)]
    if lp_solve([0] * m0, a_eq, b_eq, [[b for _, b in loop.init]], [-d])[0] != "optimal":
        return False
    for t in loop.trans:
        m = len(t)
        ok = False
        options = [("cons", None), ("dis", None)] if mus is None else [("cons", mu) for mu in mus] + [("dis", None)]
        for kind, mu in options:
            # Unknowns: mu, then lambda (m). All nonnegative.
            a_eq, b_eq = [], []
            for k in range(n):
                a_eq.append([c[k] if mu is None or kind == "dis" else 0] + [a[k] for a, _ in t])
                b_eq.append(0 if mu is None or kind == "dis" else -mu * c[k])
                a_eq.append([0] + [a[n + k] for a, _ in t])
                b_eq.append(c[k] if kind == "cons" else 0)
            if kind == "cons" and mu is None:
                a_ub, b_ub = [[-d] + [b for _, b in t]], [-d]
            elif kind == "cons":
                a_ub, b_ub = [[0] + [b for _, b in t]], [(mu - 1) * d]
            else:
                a_ub, b_ub = [[-d] + [b for _, b in t]], [-1]
            if lp_solve([0] * (m + 1), a_eq, b_eq, a_ub, b_ub)[0] == "optimal":
                ok = True
                break
        if not ok:
            return False
    return True


def int_box_inductive(loop, c, d, lo, hi):
    """Initiation and consecution on the integer points of a box, for loops
    built with affine(), whose rows over x' are the update equalities."""
    n = loop.n
    pts = list(itertools.product(range(lo, hi + 1), repeat=n))
    for x in pts:
        if all(dot(a, x) <= b for a, b in loop.init) and not holds(c, d, x):
            return False
    for t in loop.trans:
        for x in pts:
            if not holds(c, d, x):
                continue
            for y in pts:
                if all(dot(a, list(x) + list(y)) <= b for a, b in t) and not holds(c, d, y):
                    return False
    return True


# The loop of Colon, Sankaranarayanan and Sipma, Fig. 1:
# (i, j) := (2, 0); loop forever: i := i + 4, or (i, j) := (i + 2, j + 1).
CSS = Loop(
    2,
    equal([1, 0], 2) + equal([0, 1], 0),
    [affine(2, [], [([1, 0], 4), ([0, 1], 0)]), affine(2, [], [([1, 0], 2), ([0, 1], 1)])],
)


class TestPage(unittest.TestCase):
    def test_css_example(self):
        self.assertEqual(invariant_for(CSS, (0, 0)), ((-1, 0), 2))
        self.assertEqual(invariant_for(CSS, (3, 1)), ((-1, 2), 2))
        self.assertEqual(invariant_for(CSS, (10, -1)), ((0, -1), 0))
        for inv in [((-1, 0), 2), ((-1, 2), 2), ((0, -1), 0)]:
            self.assertTrue(primal_inductive(CSS, *inv))
            self.assertTrue(certificate(CSS, *inv, mus=(1, 0)))

    def test_css_reachable(self):
        # Every reachable state is i = 2 + 4a + 2b, j = b with a, b >= 0.
        for a in range(6):
            for b in range(6):
                x = (2 + 4 * a + 2 * b, b)
                self.assertTrue(holds((-1, 2), 2, x))
                self.assertTrue(holds((0, -1), 0, x))
                self.assertIsNone(invariant_for(CSS, x))

    def test_integer_trap(self):
        # x := 0; while 2x <= 1: x := 2x + 1. The reachable states are 0
        # and 1, and x <= 1 is inductive over the integers, but every
        # rational inductive inequality also holds at x = 2.
        trap = Loop(1, equal([1], 0), [affine(1, [([2], 1)], [([2], 1)])])
        self.assertIsNone(invariant_for(trap, (2,)))
        self.assertTrue(int_box_inductive(trap, (1,), -1, -6, 6))
        self.assertFalse(primal_inductive(trap, (1,), -1))
        self.assertEqual(invariant_for(trap, (3,)), ((1,), -2))
        # With the guard replaced by its integer hull x <= 0, x <= 1 is found.
        hull = Loop(1, equal([1], 0), [affine(1, [([1], 0)], [([2], 1)])])
        self.assertEqual(invariant_for(hull, (2,)), ((1,), -1))

    def test_multiplier_two(self):
        # x := 1; loop forever: x := 2x. Both x >= 0 and x >= 1 are
        # inductive, but their certificates need mu = 2.
        dbl = Loop(1, equal([1], 1), [affine(1, [], [([2], 0)])])
        self.assertIsNone(invariant_for(dbl, (-1,)))
        self.assertEqual(invariant_for(dbl, (-1,), mus=(1, 0, 2)), ((-1,), 1))
        for d in (0, 1):
            self.assertTrue(primal_inductive(dbl, (-1,), d))
            self.assertTrue(certificate(dbl, (-1,), d))
            self.assertFalse(certificate(dbl, (-1,), d, mus=(1, 0)))

    def test_empty_init(self):
        empty = Loop(1, [([1], 0), ([-1], -1)], [affine(1, [], [([1], 1)])])
        self.assertEqual(invariant_for(empty, (0,)), ((0,), 1))


def rand_loop(rng):
    n = 2
    if rng.random() < 0.5:
        init = equal([1, 0], rng.randint(-2, 2)) + equal([0, 1], rng.randint(-2, 2))
    else:
        lx = rng.randint(-2, 1)
        init = [([1, 0], lx + 1), ([-1, 0], -lx)] + equal([0, 1], rng.randint(-2, 2))
    trans = []
    for _ in range(rng.randint(1, 2)):
        guard = []
        if rng.random() < 0.6:
            guard.append(([rng.randint(-1, 1), rng.randint(-1, 1)], rng.randint(-3, 3)))
        update = []
        for k in range(n):
            u = [0, 0]
            u[k] = rng.choice([1, 1, 1, 0, -1])
            if rng.random() < 0.3:
                u[1 - k] = rng.choice([-1, 1])
            update.append((u, rng.randint(-2, 2)))
        trans.append((guard, update))
    loop = Loop(n, init, [affine(n, g, u) for g, u in trans])
    return loop, trans


def runs(loop, trans, rng, walks=3, steps=12):
    """States of random runs from the integer initial states in a box."""
    starts = [x for x in itertools.product(range(-4, 5), repeat=2) if all(dot(a, x) <= b for a, b in loop.init)]
    seen = set(starts)
    for x0 in starts:
        for _ in range(walks):
            x = x0
            for _ in range(steps):
                enabled = [u for g, u in trans if all(dot(a, x) <= b for a, b in g)]
                if not enabled:
                    break
                u = rng.choice(enabled)
                x = tuple(dot(uk, x) + ck for uk, ck in u)
                seen.add(x)
    return seen


class TestRandom(unittest.TestCase):
    def test_found_invariants_are_sound(self):
        rng = random.Random(31)
        found = 0
        for _ in range(500):
            loop, trans = rand_loop(rng)
            bad = (rng.randint(-4, 4), rng.randint(-4, 4))
            inv = invariant_for(loop, bad)
            if inv is None:
                continue
            found += 1
            c, d = inv
            self.assertFalse(holds(c, d, bad))
            self.assertTrue(primal_inductive(loop, c, d))
            self.assertTrue(certificate(loop, c, d, mus=(1, 0)))
            for x in runs(loop, trans, rng):
                self.assertTrue(holds(c, d, x))
        self.assertGreater(found, 150)

    def test_complete_on_grid(self):
        # The oracle enumerates the inequalities with c in {-1, 0, 1}^2 and
        # d in {-3, ..., 3}. Rational inductiveness by the primal LP must
        # agree with the existence of a certificate with mu free (Farkas'
        # lemma), and whenever one with mu in {0, 1} excludes a bad point,
        # the algorithm must find some invariant for it.
        rng = random.Random(5)
        grid = [(c, d) for c in itertools.product((-1, 0, 1), repeat=2) if c != (0, 0) for d in range(-3, 4)]
        checked = 0
        for _ in range(15):
            loop, _ = rand_loop(rng)
            good = []
            for c, d in grid:
                ind = primal_inductive(loop, c, d)
                self.assertEqual(ind, certificate(loop, c, d))
                if ind and certificate(loop, c, d, mus=(1, 0)):
                    good.append((c, d))
            for bad in itertools.product(range(-3, 4), repeat=2):
                if any(not holds(c, d, bad) for c, d in good):
                    checked += 1
                    self.assertIsNotNone(invariant_for(loop, bad))
        self.assertGreater(checked, 100)


if __name__ == "__main__":
    unittest.main()
