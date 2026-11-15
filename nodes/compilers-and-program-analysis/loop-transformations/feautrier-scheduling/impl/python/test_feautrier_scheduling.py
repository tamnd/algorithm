# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feautrier-scheduling/. The authors are listed in prov/7EMC3G.jsonl.
"""Tests: every schedule must order every dependence that a brute-force
search finds, and running the instances in schedule order, with ties in a
random order, must give the same memory as the original program."""

import random
import unittest

from feautrier_scheduling import (
    F, LP, Program, Stmt, brute_dependences, dependences, feautrier_schedule, form, instances,
    matvec, reverse_copy, run, running_sum, schedule_vector, show, stencil,
)


def check_legal(test, prog, sched, ns):
    pairs = 0
    for n in ns:
        env = {"N": n}
        for (a, p), (b, q) in brute_dependences(prog, env, 2 * n + 2):
            va = schedule_vector(prog, sched, a, p, env)
            vb = schedule_vector(prog, sched, b, q, env)
            test.assertLess(va, vb, f"{a}{p} -> {b}{q} at N={n}")
            pairs += 1
    return pairs


def check_runs(test, prog, sched, ns, seed):
    rng = random.Random(seed)
    for n in ns:
        env = {"N": n}
        want = run(prog, env, 2 * n + 2)
        for _ in range(3):
            got = run(prog, env, 2 * n + 2,
                      lambda name, p: schedule_vector(prog, sched, name, p, env), rng)
            test.assertEqual(got, want, f"N={n}")


def check_all(test, prog, ns, seed=0):
    sched, edges, report = feautrier_schedule(prog)
    # each dimension strongly satisfies at least one edge, each edge once
    test.assertTrue(all(report))
    seen = sorted(i for r in report for i in r)
    test.assertEqual(seen, list(range(len(edges))))
    pairs = check_legal(test, prog, sched, ns)
    check_runs(test, prog, sched, ns, seed)
    return sched, report, pairs


class Examples(unittest.TestCase):
    def test_lp(self):
        lp = LP()
        lp.var("x")
        lp.var("y")
        lp.ge({"x": -1, "y": -2}, -4)
        lp.ge({"x": -3, "y": -1}, -6)
        sol = lp.maximize({"x": 1, "y": 1})
        self.assertEqual((sol["x"], sol["y"]), (F(c=8)[""] / 5, F(c=6)[""] / 5))

    def test_running_sum_needs_two_dimensions(self):
        sched, report, pairs = check_all(self, running_sum(), range(0, 4))
        self.assertEqual(show(sched), {"S": "(i, j)"})
        self.assertGreater(pairs, 100)

    def test_matvec_is_one_dimensional(self):
        sched, report, _ = check_all(self, matvec(), range(1, 5))
        self.assertEqual(len(report), 1)
        # latency N: the last instance S2(N-1, N-1) runs at time N
        for n in range(1, 5):
            env = {"N": n}
            last = max(schedule_vector(matvec(), sched, S.name, p, env)
                       for _, S, p in instances(matvec(), env, n + 1))
            self.assertEqual(last, (n,))

    def test_reverse_copy_is_fully_parallel(self):
        sched, _, _ = check_all(self, reverse_copy(), range(0, 4))
        self.assertEqual(show(sched), {"S1": "(0)", "S2": "(1)"})

    def test_stencil_wavefront(self):
        sched, report, _ = check_all(self, stencil(), range(1, 5))
        self.assertEqual(show(sched), {"S": "(i + j)"})


def random_program(rng):
    """One or two outer loops with at most three statements at depth 1 or 2
    that write and read one-dimensional arrays A and B with affine
    subscripts."""
    stmts, k = [], 0
    for b0 in range(rng.randint(1, 2)):
        for b1 in range(rng.randint(1, 2)):
            if k == 3:
                break
            dom_i = [F(i=1), F(N=1, i=-1)]
            if rng.random() < 0.5:
                iters, betas, dom = ["i"], [b0, b1], dom_i
            else:
                lo, hi = rng.choice([(F(j=1), F(N=1, j=-1)), (F(j=1), F(i=1, j=-1)),
                                     (F(j=1, i=-1), F(N=1, j=-1))])
                iters, betas, dom = ["i", "j"], [b0, b1, 0], dom_i + [lo, hi]

            def sub():
                d = {"i": rng.choice([0, 1, 1, 2, -1])}
                if "j" in iters:
                    d["j"] = rng.choice([0, 1, 1, -1])
                if rng.random() < 0.2:
                    d["N"] = 1
                return form(d, rng.choice([-1, 0, 0, 1]))
            reads = [(rng.choice("AB"), [sub()]) for _ in range(rng.randint(1, 2))]
            stmts.append(Stmt(f"S{k}", iters, betas, dom, (rng.choice("AB"), [sub()]), reads))
            k += 1
    return Program(["N"], [F(N=1)], stmts)


class RandomPrograms(unittest.TestCase):
    def test_random(self):
        # programs with many edges make large linear programs; they are
        # skipped to keep the test fast
        rng = random.Random(1992)
        total, dims, t = 0, set(), 0
        while t < 20:
            prog = random_program(rng)
            if len(dependences(prog)) > 14:
                continue
            t += 1
            sched, report, pairs = check_all(self, prog, range(0, 4), seed=t)
            total += pairs
            dims.add(len(report))
        self.assertGreater(total, 1000)
        self.assertTrue({1, 2} <= dims)


if __name__ == "__main__":
    unittest.main()
