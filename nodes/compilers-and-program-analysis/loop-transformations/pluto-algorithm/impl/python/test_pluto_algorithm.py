# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pluto-algorithm/. The authors are listed in prov/8AZ5A6.jsonl.
"""Tests: the transformation must order every dependence that a brute-force
search finds; inside each band every hyperplane must keep the dependences
that reach the band nonnegative and within the bound u N + w; and running
the instances in the new order, untiled or tiled, with ties in a random
order, must give the same memory as the original program."""

import random
import unittest

from pluto_algorithm import (
    F, LP, Program, Stmt, brute_dependences, dependences, form, ilp_lexmin, matmul,
    orthogonal_rows, pluto, producer_consumer, run, seidel, show, stencil, time_vector,
)


def check_all(test, prog, ns, seed=0):
    dims, bands, edges = pluto(prog)
    pairs = 0
    rng = random.Random(seed)
    for n in ns:
        env = {"N": n}
        box = 2 * n + 2
        for (a, p), (b, q) in brute_dependences(prog, env, box):
            va = time_vector(prog, dims, a, p, env)
            vb = time_vector(prog, dims, b, q, env)
            test.assertLess(va, vb, f"{a}{p} -> {b}{q} at N={n}")
            pairs += 1
            diff = [y - x for x, y in zip(va, vb)]
            for band in bands:
                if any(diff[:band[0]]):
                    continue        # satisfied before the band
                for k in band:
                    test.assertGreaterEqual(diff[k], 0, "band not permutable")
                    test.assertLessEqual(diff[k], dims[k]["u"] * n + dims[k]["w"], "cost bound")
        want = run(prog, env, box)
        for tile in (None, 2, 3):
            got = run(prog, env, box,
                      lambda name, pt: time_vector(prog, dims, name, pt, env, bands, tile), rng)
            test.assertEqual(got, want, f"N={n} tile={tile}")
    return dims, bands, pairs


class Pieces(unittest.TestCase):
    def test_orthogonal_rows(self):
        self.assertEqual(orthogonal_rows([[1, 0]], 2), [[0, 1]])
        self.assertEqual(orthogonal_rows([[1, 1]], 2), [[1, -1], [-1, 1]])
        self.assertEqual(orthogonal_rows([[1, 0, 0], [0, 1, 0]], 3), [[0, 0, 1]])

    def test_ilp_lexmin(self):
        # minimize x, then y, over 2x + 2y >= 3, 0 <= x, y <= 5, integers:
        # the rational optimum has x = 0, y = 3/2; the integer one y = 2
        lp = LP()
        for v in "xy":
            lp.var(v)
            lp.ge({v: -1}, -5)
        lp.ge({"x": 2, "y": 2}, 3)
        sol = ilp_lexmin(lp, [{"x": 1}, {"y": 1}], ["x", "y"])
        self.assertEqual((sol["x"], sol["y"]), (0, 2))


class Examples(unittest.TestCase):
    def test_seidel_skews_time(self):
        dims, bands, _ = check_all(self, seidel(), range(2, 5))
        self.assertEqual(show(dims), {"S": "(t, i + t)"})
        self.assertEqual(bands, [[0, 1]])
        self.assertEqual([(d["u"], d["w"]) for d in dims], [(1, 0), (1, 1)])

    def test_stencil_tiles_directly(self):
        dims, bands, _ = check_all(self, stencil(), range(1, 5))
        self.assertEqual(show(dims), {"S": "(i, j)"})
        self.assertEqual([(d["u"], d["w"]) for d in dims], [(0, 1), (0, 1)])

    def test_producer_consumer_fuses_with_a_shift(self):
        dims, bands, _ = check_all(self, producer_consumer(), range(1, 6))
        self.assertEqual(show(dims), {"S1": "(i, 0)", "S2": "(i + 1, 1)"})
        self.assertEqual((dims[0]["u"], dims[0]["w"]), (0, 2))
        self.assertEqual(dims[1]["kind"], "scalar")

    def test_matmul_band_of_three(self):
        dims, bands, _ = check_all(self, matmul(), range(0, 3))
        self.assertEqual(bands, [[0, 1, 2]])
        self.assertEqual([(d["u"], d["w"]) for d in dims[:2]], [(0, 0), (0, 0)])


def random_program(rng):
    """At most three statements at depth 1 or 2 in one or two outer loops,
    on one-dimensional arrays A and B with affine subscripts."""
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
        # programs with many edges make large integer programs; they are
        # skipped to keep the test fast
        rng = random.Random(2008)
        total, kinds, t = 0, set(), 0
        while t < 16:
            prog = random_program(rng)
            if len(dependences(prog)) > 10:
                continue
            t += 1
            dims, bands, pairs = check_all(self, prog, range(0, 4), seed=t)
            total += pairs
            kinds |= {d["kind"] for d in dims}
        self.assertGreater(total, 500)
        self.assertIn("hyperplane", kinds)


if __name__ == "__main__":
    unittest.main()
