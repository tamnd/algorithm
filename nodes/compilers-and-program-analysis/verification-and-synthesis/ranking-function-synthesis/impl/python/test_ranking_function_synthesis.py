# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-function-synthesis/. The authors are listed in prov/HA12CT.jsonl.

import itertools
import random
import unittest
from fractions import Fraction

from fraclp import lp_solve
from ranking_function_synthesis import linear_ranking, loop_rows, value


def dot(a, x):
    return sum(Fraction(ai) * xi for ai, xi in zip(a, x))


def step(guard, update, x):
    """The successor of x, or None when the guard is false."""
    if not all(dot(a, x) <= b for a, b in guard):
        return None
    return tuple(dot(uk, x) + ck for uk, ck in update)


def primal_is_ranking(n, rows, rho):
    """The oracle: with exact linear programs over the relation, is
    x -> rho . x bounded below and decreasing by some delta > 0? Returns
    (bound, delta) or None."""
    a_ub = [a for a, _ in rows]
    b_ub = [b for _, b in rows]
    st, _, low = lp_solve(list(rho) + [0] * n, a_ub=a_ub, b_ub=b_ub, free=range(2 * n))
    if st == "infeasible":
        return (0, 1)
    if st == "unbounded":
        return None
    st, _, dec = lp_solve(list(rho) + [-r for r in rho], a_ub=a_ub, b_ub=b_ub, free=range(2 * n))
    if st != "optimal" or dec <= 0:
        return None
    return (low, dec)


def check_samples(test, guard, update, res, points):
    rho, bound, dec = res
    test.assertGreaterEqual(dec, 1)
    for x in points:
        y = step(guard, update, x)
        if y is None:
            continue
        test.assertGreaterEqual(value(rho, x), bound)
        test.assertGreaterEqual(value(rho, x) - value(rho, y), dec)


BOX = list(itertools.product(range(-5, 6), repeat=2))


class TestPage(unittest.TestCase):
    def test_page_example(self):
        # while x >= y + 1: (x, y) := (x - 1, y + 1)
        guard = [([-1, 1], -1)]
        update = [([1, 0], -1), ([0, 1], 1)]
        res = linear_ranking(2, loop_rows(2, guard, update))
        self.assertEqual(res, ((Fraction(1, 2), Fraction(-1, 2)), Fraction(1, 2), Fraction(1)))
        check_samples(self, guard, update, res, BOX)

    def test_terminating_without_linear_ranking(self):
        # x >= 0: (x, y) := (x + y, y - 1). Every run stops, but no linear
        # function decreases on every step.
        guard = [([-1, 0], 0)]
        update = [([1, 1], 0), ([0, 1], -1)]
        rows = loop_rows(2, guard, update)
        self.assertIsNone(linear_ranking(2, rows))
        for x in BOX:
            for _ in range(60):
                y = step(guard, update, x)
                if y is None:
                    break
                x = y
            self.assertIsNone(step(guard, update, x))
        for rho in itertools.product(range(-3, 4), repeat=2):
            self.assertIsNone(primal_is_ranking(2, rows, rho))

    def test_nonterminating(self):
        # x >= 0: x := x has a fixed point; x >= 0: x := x + 1 runs away.
        for update in ([([1], 0)], [([1], 1)]):
            self.assertIsNone(linear_ranking(1, loop_rows(1, [([-1], 0)], update)))

    def test_integer_trap(self):
        # 2x >= 1 and 2x <= 1: x := x. No integer state enters the loop, so
        # every integer run stops at once. Over the rationals x = 1/2 loops
        # for ever, so there is no rational ranking function.
        guard = [([-2], -1), ([2], 1)]
        rows = loop_rows(1, guard, [([1], 0)])
        self.assertIsNone(linear_ranking(1, rows))
        self.assertTrue(all(step(guard, [([1], 0)], (x,)) is None for x in range(-20, 21)))
        self.assertEqual(step(guard, [([1], 0)], (Fraction(1, 2),)), (Fraction(1, 2),))

    def test_rational_fixed_point(self):
        # x >= 0: x := 10 - 2x. Integer runs stop, since |x - 10/3| doubles,
        # but the rational state 10/3 is a fixed point.
        guard, update = [([-1], 0)], [([-2], 10)]
        self.assertIsNone(linear_ranking(1, loop_rows(1, guard, update)))
        self.assertEqual(step(guard, update, (Fraction(10, 3),)), (Fraction(10, 3),))

    def test_nondeterministic_relation(self):
        # x >= 0 and x' <= x - 1: any smaller value.
        res = linear_ranking(1, [([-1, 0], 0), ([-1, 1], -1)])
        self.assertEqual(res, ((Fraction(1),), Fraction(0), Fraction(1)))

    def test_empty_relation(self):
        rows = loop_rows(1, [([-1], -1), ([1], 0)], [([1], 1)])
        rho, _, dec = linear_ranking(1, rows)
        self.assertEqual((rho, dec), ((Fraction(0),), Fraction(1)))


def rand_loop(rng):
    guard = []
    for _ in range(rng.randint(1, 2)):
        guard.append(([rng.randint(-2, 2), rng.randint(-2, 2)], rng.randint(-3, 3)))
    update = []
    for k in range(2):
        u = [0, 0]
        u[k] = rng.choice([1, 1, 1, 0, -1, 2])
        if rng.random() < 0.4:
            u[1 - k] = rng.choice([-1, 1])
        update.append((u, rng.randint(-2, 2)))
    return guard, update


def rational_points(rng, count=40):
    return [(Fraction(rng.randint(-15, 15), rng.randint(1, 3)), Fraction(rng.randint(-15, 15), rng.randint(1, 3))) for _ in range(count)]


def cycles(guard, update, x, limit=40):
    """True if the integer run from x repeats a state within limit steps."""
    seen = {x}
    for _ in range(limit):
        x = step(guard, update, x)
        if x is None:
            return False
        if x in seen:
            return True
        seen.add(x)
    return False


GRID = [rho for rho in itertools.product(range(-2, 3), repeat=2) if rho != (0, 0)]


class TestRandom(unittest.TestCase):
    def test_random_loops(self):
        rng = random.Random(77)
        found = looping = 0
        for _ in range(500):
            guard, update = rand_loop(rng)
            rows = loop_rows(2, guard, update)
            res = linear_ranking(2, rows)
            if any(cycles(guard, update, x) for x in BOX[::7]):
                # A loop that does not terminate has no ranking function.
                looping += 1
                self.assertIsNone(res)
            if res is None:
                # The oracle: no small integer direction is a ranking function.
                for rho in GRID:
                    self.assertIsNone(primal_is_ranking(2, rows, rho))
                continue
            found += 1
            rho, bound, dec = res
            exact = primal_is_ranking(2, rows, rho)
            self.assertIsNotNone(exact)
            self.assertGreaterEqual(exact[0], bound)
            self.assertGreaterEqual(exact[1], dec)
            check_samples(self, guard, update, res, BOX + rational_points(rng))
            # Each integer run is at most (rho . x0 - bound) / dec + 1 steps.
            for x in BOX[::5]:
                limit = max(0, (value(rho, x) - bound) / dec) + 1
                steps = 0
                while True:
                    y = step(guard, update, x)
                    if y is None:
                        break
                    x, steps = y, steps + 1
                    self.assertLessEqual(steps, limit)
        self.assertGreater(found, 100)
        self.assertGreater(looping, 50)


if __name__ == "__main__":
    unittest.main()
