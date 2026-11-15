# SPDX-License-Identifier: MIT
import math
import random
import unittest
from collections import Counter
from itertools import product

import stochastic_superoptimization as st

K = ("k", 1)

# x + y written with xor, and, a shift and an add: four instructions.
ADD4 = [("op", 2, "^", 0, 1), ("op", 3, "&", 0, 1), ("op", 3, "<<", 3, K), ("op", 0, "+", 2, 3)]
# 2x + 2y in three instructions; the shortest has two.
DOUBLE3 = [("op", 2, "+", 0, 0), ("op", 3, "+", 1, 1), ("op", 0, "+", 2, 3)]
# (x | y) - (x & y), which is x ^ y.
XOR3 = [("op", 2, "|", 0, 1), ("op", 3, "&", 0, 1), ("op", 0, "-", 2, 3)]
TESTS = [(0, 0), (1, 2), (3, 5), (7, 9)]


def reference_run(prog, x, y, w=4):
    """An independent 4-bit evaluator, written from the definition."""
    mask = (1 << w) - 1
    r = [x, y, 0, 0]

    def val(a):
        return a[1] if isinstance(a, tuple) else r[a]

    for ins in prog:
        if ins is None:
            continue
        if ins[0] == "copy":
            r[ins[1]] = val(ins[2])
            continue
        a, b = val(ins[3]), val(ins[4])
        r[ins[1]] = {
            "+": (a + b) % (mask + 1),
            "-": (a - b) % (mask + 1),
            "&": a & b, "|": a | b, "^": a ^ b,
            "<<": (a * 2 ** b) % (mask + 1) if b < w else 0,
            ">>": a // 2 ** b if b < w else 0,
        }[ins[2]]
    return r[0]


def equivalent(p, q):
    return all(reference_run(p, x, y) == reference_run(q, x, y) for x in range(16) for y in range(16))


class SearchTest(unittest.TestCase):
    def test_finds_the_known_shorter_program(self):
        m = st.Machine()
        r = st.search(m, ADD4, TESTS, L=4, steps=50000, seed=1)
        self.assertEqual([st.perf(p) for _, p in r.accepted], [3, 2, 1])
        self.assertEqual([s for s, _ in r.accepted], [1535, 2563, 30250])
        self.assertEqual(st.show(r.best), "r0 = r1 + r0")
        # Massalin's enumeration agrees that one instruction is the least.
        self.assertEqual(st.shortest_by_enumeration(m, ADD4, 2), [("op", 0, "+", 0, 1)])

    def test_every_accepted_rewrite_is_equivalent(self):
        m = st.Machine()
        count = 0
        for target, L in ((ADD4, 4), (DOUBLE3, 3), (XOR3, 3)):
            for seed in range(4):
                r = st.search(m, target, TESTS, L=L, steps=15000, seed=seed)
                self.assertTrue(equivalent(r.best, target))
                for _, p in r.accepted:
                    self.assertTrue(equivalent(p, target), st.show(p))
                    count += 1
                lengths = [st.perf(p) for _, p in r.accepted]
                self.assertEqual(lengths, sorted(lengths, reverse=True))
                self.assertEqual(len(set(lengths)), len(lengths))
        self.assertGreater(count, 15)

    def test_shortest_for_the_other_targets(self):
        m = st.Machine()
        self.assertEqual(len(st.shortest_by_enumeration(m, DOUBLE3, 2)), 2)
        self.assertEqual(len(st.shortest_by_enumeration(m, XOR3, 2)), 1)
        r = st.search(m, XOR3, TESTS, L=3, steps=20000, seed=0)
        self.assertEqual(st.perf(r.best), 1)


class CheckTest(unittest.TestCase):
    def test_tests_alone_are_not_enough(self):
        m = st.Machine()
        bad = [("op", 0, "|", 0, 1)]
        few = [((0, 0), 0), ((1, 2), 3)]
        self.assertEqual(st.eq(m, bad, few), 0)
        self.assertEqual(st.counterexample(m, bad, ADD4), (1, 1))
        self.assertFalse(equivalent(bad, ADD4))

    def test_refuted_candidates_become_tests(self):
        m = st.Machine()
        r = st.search(m, ADD4, TESTS, L=4, steps=50000, seed=1)
        self.assertEqual(r.verified, 4)
        self.assertEqual(len(r.counterexamples), 1)
        step, x, p = r.counterexamples[0]
        self.assertEqual((step, x), (1120, (0, 1)))
        self.assertEqual(st.show(p), "r3 = 1 ^ r0\nr2 = r0 ^ r1\nr0 = r2 << r3")
        # It was right on the four tests, and wrong on the input it gave.
        for t in TESTS:
            self.assertEqual(reference_run(p, *t), reference_run(ADD4, *t))
        self.assertEqual((reference_run(p, 0, 1), reference_run(ADD4, 0, 1)), (2, 1))
        self.assertIn(((0, 1), 1), r.tests)

    def test_counterexample_none_iff_equivalent(self):
        m = st.Machine()
        rng = random.Random(3)
        agree = 0
        for _ in range(300):
            p = [rng.choice(m.instrs) for _ in range(rng.randint(1, 3))]
            q = [rng.choice(m.instrs) for _ in range(rng.randint(1, 3))]
            same = equivalent(p, q)
            self.assertEqual(st.counterexample(m, p, q) is None, same)
            agree += same
        self.assertGreater(agree, 0)


class ChainTest(unittest.TestCase):
    def test_acceptance_rule(self):
        self.assertEqual(st.acceptance(4, 10, 9), 1.0)
        self.assertEqual(st.acceptance(4, 10, 10), 1.0)
        self.assertAlmostEqual(st.acceptance(4, 10, 11), math.exp(-4))
        self.assertAlmostEqual(st.acceptance(4, 10, 12, 2.0), 2 * math.exp(-8))
        self.assertAlmostEqual(st.acceptance(4, 10, 10, 0.5), 0.5)
        self.assertEqual(st.acceptance(4, 10, 5, 0.5), 1.0)

    def stationary_tv(self, hastings):
        m = st.Machine(w=1, nregs=2, ninputs=1, ops=("^", "&"), consts=())
        target = [("op", 0, "^", 0, 0)]
        tests = [((x,), st.run(m, target, (x,))) for x in (0, 1)]
        beta, L, n = 1.0, 2, 200000
        states = list(product([None] + m.instrs, repeat=L))
        weight = {s: math.exp(-beta * st.cost(m, list(s), tests)) for s in states}
        z = sum(weight.values())
        rng = random.Random(7)
        R = [None] * L
        c = st.cost(m, R, tests)
        seen = Counter()
        for _ in range(n):
            R, c = st.mh_step(m, R, c, tests, beta, rng, 0.5, hastings=hastings)
            seen[tuple(R)] += 1
        return 0.5 * sum(abs(seen[s] / n - weight[s] / z) for s in states)

    def test_chain_samples_exp_minus_beta_cost(self):
        # 19 * 19 = 361 programs: the visit frequencies are close to
        # exp(-beta cost) / Z with the Hastings factor, and far from it
        # without, because the unused slot is proposed half of the time.
        self.assertLess(self.stationary_tv(True), 0.05)
        self.assertGreater(self.stationary_tv(False), 0.5)

    def test_moves_keep_programs_valid(self):
        m = st.Machine()
        rng = random.Random(5)
        R = list(ADD4)
        allowed = set(m.instrs)
        for _ in range(3000):
            R, _, h = st.propose(m, R, rng, 0.2)
            self.assertEqual(len(R), 4)
            self.assertGreater(h, 0)
            for ins in R:
                self.assertTrue(ins is None or ins in allowed, ins)


if __name__ == "__main__":
    unittest.main()
