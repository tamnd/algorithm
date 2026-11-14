# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-bend-sequencing/. The authors are listed in prov/0RQ6RW.jsonl.

import random
import unittest
from fractions import Fraction
from functools import lru_cache
from itertools import permutations

import a_star_bend_sequencing as m
from a_star_bend_sequencing import Tool, a_star_bends, collides, fits, heuristic, plan_cost, profile_after

STANDARD = Tool(3, 2, 1)
GOOSENECK = Tool(1, 4, 2)
LIPPED = ([1, 4, 6, 4, 1], [0, 1, 1, 1, 1])


def feasible_tools(lengths, signs, tools, done, b, cache):
    key = (frozenset(done), b)
    if key not in cache:
        cache[key] = [t for t in range(len(tools)) if fits(lengths, b, tools[t]) and not collides(lengths, signs, set(done), b, tools[t])]
    return cache[key]


def brute_force(lengths, signs, tools, flip, change):
    """Try every order of the bends. For each order, choose the tools by a small DP."""
    n = len(lengths) - 1
    cache = {}
    best = None
    count = 0
    for order in permutations(range(1, n + 1)):
        done = set()
        dp = {-1: 0}  # last tool -> least number of tool changes so far
        for b in order:
            ok = feasible_tools(lengths, signs, tools, done, b, cache)
            new = {}
            for t in ok:
                new[t] = min(c + (1 if last not in (-1, t) else 0) for last, c in dp.items())
            dp = new
            if not dp:
                break
            done.add(b)
        if not dp:
            continue
        count += 1
        flips = sum(1 for a, c in zip(order, order[1:]) if signs[a] != signs[c])
        cost = flip * flips + change * min(dp.values())
        if best is None or cost < best:
            best = cost
    return best, count


def random_instance(rng, n, alternate=0.5):
    """A random profile. Signs change with probability `alternate`; a profile
    whose signs alternate is a staircase, which is often feasible, and one
    with many equal signs curls up and often is not."""
    lengths = [rng.randint(1, 4) for _ in range(n + 1)]
    signs = [0, rng.choice((1, -1))]
    for _ in range(n - 1):
        signs.append(-signs[-1] if rng.random() < alternate else signs[-1])
    tools = [Tool(rng.randint(1, 2), rng.randint(1, 4), rng.randint(1, 2)) for _ in range(rng.randint(1, 3))]
    return lengths, signs[: n + 1], tools


class TestGeometry(unittest.TestCase):
    def test_profile_of_the_last_wall_bend(self):
        lengths, signs = LIPPED
        segs = profile_after(lengths, signs, {1, 2, 4}, 3)
        self.assertEqual(
            segs,
            [((0, 0), (4, 0)), ((4, 0), (4, 1)), ((0, 0), (0, 6)), ((0, 6), (4, 6)), ((4, 6), (4, 5))],
        )
        self.assertTrue(collides(lengths, signs, {1, 2, 4}, 3, STANDARD))
        self.assertFalse(collides(lengths, signs, {1, 2, 4}, 3, GOOSENECK))

    def test_mirror_for_a_bend_to_the_right(self):
        # The same channel with all signs flipped is the same part turned over.
        lengths, signs = LIPPED
        flipped = [0] + [-s for s in signs[1:]]
        for done in (set(), {1}, {1, 2}, {1, 2, 4}):
            for b in range(1, 5):
                if b not in done:
                    self.assertEqual(profile_after(lengths, signs, done, b), profile_after(lengths, flipped, done, b))

    def test_open_region_against_sampling(self):
        # Endpoints are integer and the region has coefficients in {-1, 0, 1},
        # so every clipping bound is a multiple of 1/L for a segment of length L.
        # A nonempty open interval then holds a multiple of 1/(2L).
        rng = random.Random(7)
        for _ in range(3000):
            p = (rng.randint(-4, 4), rng.randint(-4, 4))
            length = rng.randint(1, 5)
            d = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            q = (p[0] + length * d[0], p[1] + length * d[1])
            planes = [(rng.randint(-1, 1), rng.randint(-1, 1), rng.randint(-3, 3)) for _ in range(rng.randint(1, 4))]
            sampled = False
            for j in range(2 * length + 1):
                s = Fraction(j, 2 * length)
                x = p[0] + s * (q[0] - p[0])
                y = p[1] + s * (q[1] - p[1])
                if all(a * x + c * y < k for a, c, k in planes):
                    sampled = True
                    break
            self.assertEqual(m._meets_open((p, q), planes), sampled, (p, q, planes))


class TestSearch(unittest.TestCase):
    def test_lipped_channel(self):
        lengths, signs = LIPPED
        tools = [STANDARD, GOOSENECK]
        plan = a_star_bends(lengths, signs, tools, flip=2, change=1)
        self.assertEqual(plan.cost, 1)
        self.assertEqual(plan.steps, [(1, 0), (2, 0), (4, 0), (3, 1)])
        self.assertEqual(plan_cost(lengths, signs, tools, plan.steps, 2, 1), 1)
        self.assertEqual(brute_force(lengths, signs, tools, 2, 1), (1, 6))
        self.assertEqual(plan.expanded, 17)
        self.assertEqual(a_star_bends(lengths, signs, tools, 2, 1, use_h=False).expanded, 24)

    def test_no_plan(self):
        # With only the standard punch the last wall bend always hits a lip.
        lengths, signs = LIPPED
        self.assertIsNone(a_star_bends(lengths, signs, [STANDARD]))
        self.assertEqual(brute_force(lengths, signs, [STANDARD], 1, 1), (None, 0))

    def test_empty_and_single(self):
        self.assertEqual(a_star_bends([5], [0], [STANDARD]).cost, 0)
        self.assertEqual(a_star_bends([2, 2], [0, -1], [STANDARD]).steps, [(1, 0)])

    def test_against_brute_force(self):
        rng = random.Random(2024)
        found = 0
        found7 = 0
        for trial in range(210):
            n = 1 + trial % 7
            lengths, signs, tools = random_instance(rng, n, 0.5 if trial % 3 == 0 else 0.85)
            flip, change = rng.randint(0, 3), rng.randint(0, 3)
            want, _ = brute_force(lengths, signs, tools, flip, change)
            plan = a_star_bends(lengths, signs, tools, flip, change)
            ucs = a_star_bends(lengths, signs, tools, flip, change, use_h=False)
            if want is None:
                self.assertIsNone(plan)
                self.assertIsNone(ucs)
                continue
            found += 1
            found7 += n == 7
            self.assertEqual(plan.cost, want, (lengths, signs, tools, flip, change))
            self.assertEqual(ucs.cost, want)
            self.assertEqual(plan_cost(lengths, signs, tools, plan.steps, flip, change), want)
            self.assertLessEqual(plan.expanded, ucs.expanded)
        self.assertGreater(found, 80)
        self.assertGreater(found7, 4)

    def test_heuristic_is_consistent_and_admissible(self):
        rng = random.Random(99)
        for trial in range(40):
            n = 2 + trial % 5
            lengths, signs, tools = random_instance(rng, n, 0.85)
            flip, change = rng.randint(1, 3), rng.randint(1, 3)
            k = len(tools)
            full = sum(1 << b for b in range(1, n + 1))
            fit_mask = [0] * (n + 1)
            for b in range(1, n + 1):
                for t in range(k):
                    if fits(lengths, b, tools[t]):
                        fit_mask[b] |= 1 << t

            def moves(state):
                done, s, t0 = state
                dset = {b for b in range(1, n + 1) if done >> b & 1}
                for b in range(1, n + 1):
                    if done >> b & 1:
                        continue
                    for t in range(k):
                        if fit_mask[b] >> t & 1 and not collides(lengths, signs, dset, b, tools[t]):
                            c = (flip if s not in (0, signs[b]) else 0) + (change if t0 not in (-1, t) else 0)
                            yield (done | 1 << b, signs[b], t), c

            @lru_cache(maxsize=None)
            def to_go(state):
                if state[0] == full:
                    return 0
                best = None
                for v, c in moves(state):
                    r = to_go(v)
                    if r is not None and (best is None or c + r < best):
                        best = c + r
                return best

            seen = {(0, 0, -1)}
            stack = [(0, 0, -1)]
            while stack:
                u = stack.pop()
                hu = heuristic(n, signs, fit_mask, u, flip, change)
                exact = to_go(u)
                if exact is not None:
                    self.assertLessEqual(hu, exact)
                for v, c in moves(u):
                    self.assertLessEqual(hu, c + heuristic(n, signs, fit_mask, v, flip, change))
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)


if __name__ == "__main__":
    unittest.main()
