# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iteratively-regularized-gauss-newton/. The authors are listed in prov/KK6851.jsonl.
import math
import random
import unittest
from fractions import Fraction

from imgla import adjoint_gap, matvec, norm2, rmatvec, solve
from iteratively_regularized_gauss_newton import exp_integration_problem, irgnm, irgnm_step


def smooth_truth(n):
    return [0.5 * math.sin(math.pi * (i + 0.5) / n) for i in range(n)]


def noisy(y, delta, seed):
    rng = random.Random(seed)
    e = [rng.gauss(0.0, 1.0) for _ in range(len(y))]
    ne = norm2(e)
    return [p + delta * q / ne for p, q in zip(y, e)]


class TestIRGNM(unittest.TestCase):
    def test_linear_case_is_centered_tikhonov(self):
        rng = random.Random(51)
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(4)]
        y = [Fraction(rng.randint(-5, 5)) for _ in range(4)]
        x0 = [Fraction(1), Fraction(-1), Fraction(2)]
        alpha0, q = Fraction(2), Fraction(1, 2)

        def f(x):
            return [sum(p * t for p, t in zip(row, x)) for row in a]

        res = irgnm(f, lambda x: a, y, x0, alpha0, q, kmax=4)
        r0 = [p - t for p, t in zip(y, f(x0))]
        for k in range(4):
            alpha = alpha0 * q ** k
            m = [[sum(a[r][i] * a[r][j] for r in range(4)) + (alpha if i == j else 0)
                  for j in range(3)] for i in range(3)]
            h = solve(m, [sum(a[r][i] * r0[r] for r in range(4)) for i in range(3)])
            self.assertEqual(res.iterates[k + 1], [p + t for p, t in zip(x0, h)])

    def test_jacobian_and_adjoint(self):
        n = 16
        f, jac, a = exp_integration_problem(n)
        rng = random.Random(52)
        x = [rng.uniform(-0.5, 0.5) for _ in range(n)]
        d = [rng.gauss(0.0, 1.0) for _ in range(n)]
        eps = 1e-5
        fp = f([p + eps * t for p, t in zip(x, d)])
        fm = f([p - eps * t for p, t in zip(x, d)])
        fd = [(p - t) / (2 * eps) for p, t in zip(fp, fm)]
        jd = matvec(jac(x), d)
        self.assertLess(norm2([p - t for p, t in zip(fd, jd)]), 1e-8 * norm2(jd))
        j = jac(x)
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        self.assertLess(adjoint_gap(lambda v: matvec(j, v), lambda v: rmatvec(j, v), d, z), 1e-12)

    def test_step_minimizes_linearized_tikhonov(self):
        n = 12
        f, jac, a = exp_integration_problem(n)
        rng = random.Random(53)
        x = [rng.uniform(-0.5, 0.5) for _ in range(n)]
        x0 = [0.0] * n
        y = [rng.uniform(0.0, 1.0) for _ in range(n)]
        r = [p - t for p, t in zip(y, f(x))]
        alpha = 0.01
        j = jac(x)
        xn = irgnm_step(j, r, x, x0, alpha)
        h = [p - t for p, t in zip(xn, x)]
        # Gradient of ||J h - r||^2 + alpha ||x + h - x0||^2 is zero at the step.
        g = rmatvec(j, [p - t for p, t in zip(matvec(j, h), r)])
        g = [gi + alpha * (xi + hi - x0i) for gi, xi, hi, x0i in zip(g, x, h, x0)]
        self.assertLess(norm2(g), 1e-12 * (norm2(rmatvec(j, r)) + alpha))

    def test_exact_data_converges(self):
        n = 32
        f, jac, a = exp_integration_problem(n)
        xt = smooth_truth(n)
        res = irgnm(f, jac, f(xt), [0.0] * n, 1.0, 0.5, kmax=20)
        errs = [norm2([p - q for p, q in zip(x, xt)]) / math.sqrt(n) for x in res.iterates]
        self.assertLess(errs[-1], 0.005)
        for e0, e1 in zip(errs, errs[1:]):
            self.assertLess(e1, e0)

    def test_discrepancy_stop(self):
        n = 32
        f, jac, a = exp_integration_problem(n)
        xt = smooth_truth(n)
        y = f(xt)
        final = []
        for delta in (1e-2, 1e-3):
            yd = noisy(y, delta, 2)
            res = irgnm(f, jac, yd, [0.0] * n, 1.0, 0.5, kmax=30, delta=delta, tau=2.0)
            self.assertEqual(res.stopped, "discrepancy")
            self.assertLessEqual(res.residuals[-1], 2.0 * delta)
            for rn in res.residuals[:-1]:
                self.assertGreater(rn, 2.0 * delta)
            longer = irgnm(f, jac, yd, [0.0] * n, 1.0, 0.5, kmax=res.k + 8)
            errs = [norm2([p - q for p, q in zip(x, xt)]) for x in longer.iterates]
            self.assertLess(errs[res.k], 1.5 * min(errs))
            final.append(errs[res.k])
        self.assertLess(final[1], final[0])


if __name__ == "__main__":
    unittest.main()
