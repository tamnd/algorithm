# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-inverse/. The authors are listed in prov/7S6RR0.jsonl.
import math
import random
import unittest

from approximate_inverse import (apply_kernels, approximate_inverse, hat_mollifier,
                                 integration_estimate, integration_kernel_norm, kernels)
from imgla import adjoint_gap, matvec, norm2, rmatvec, solve, transpose


def cumsum_matrix(n):
    h = 1.0 / n
    return [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]


def pl_norm(e, h):
    """Exact L^2 norm of the piecewise linear function with nodal values e."""
    return math.sqrt(sum(h / 3.0 * (a * a + a * b + b * b) for a, b in zip(e, e[1:])))


class TestApproximateInverse(unittest.TestCase):
    def test_exact_data_gives_mollified_solution(self):
        n = 40
        h = 1.0 / n
        a = cumsum_matrix(n)
        grid = [(i + 0.5) * h for i in range(n)]
        moll = [hat_mollifier(grid, p, 0.1, h) for p in (0.2, 0.35, 0.5, 0.8)]
        rng = random.Random(61)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        est = approximate_inverse(a, moll, [matvec(a, x)])[0]
        for e, v in zip(moll, est):
            self.assertAlmostEqual(v, sum(p * q for p, q in zip(e, x)), places=9)

    def test_kernel_formulas_agree(self):
        rng = random.Random(62)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(6)] for _ in range(4)]
        es = [[rng.uniform(0.0, 1.0) for _ in range(6)] for _ in range(3)]
        beta = 0.05
        psis = kernels(a, es, beta)
        ata = [[sum(a[r][i] * a[r][j] for r in range(4)) + (beta if i == j else 0.0)
                for j in range(6)] for i in range(6)]
        for e, psi in zip(es, psis):
            ref = matvec(a, solve(ata, e))
            for p, q in zip(psi, ref):
                self.assertAlmostEqual(p, q, places=10)
            # psi minimizes ||A^T psi - e||^2 + beta ||psi||^2: the gradient is zero.
            g = matvec(a, [p - q for p, q in zip(rmatvec(a, psi), e)])
            g = [gi + beta * pi for gi, pi in zip(g, psi)]
            self.assertLess(norm2(g), 1e-10)

    def test_kernels_are_reused(self):
        n = 30
        h = 1.0 / n
        a = cumsum_matrix(n)
        grid = [(i + 0.5) * h for i in range(n)]
        moll = [hat_mollifier(grid, p, 0.15, h) for p in (0.3, 0.6)]
        rng = random.Random(63)
        ys = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(3)]
        psis = kernels(a, moll, 1e-6)
        both = approximate_inverse(a, moll, ys, 1e-6)
        for y, est in zip(ys, both):
            self.assertEqual(est, apply_kernels(psis, y))

    def test_shift_invariance(self):
        # A circulant blur commutes with shifts, so the kernel for a shifted
        # mollifier is the shifted kernel.
        n = 24
        w = [0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25]
        a = [[w[(i - j) % n] + (0.2 if i == j else 0.0) for j in range(n)] for i in range(n)]
        base = [max(0.0, 1.0 - abs(min(i, n - i)) / 3.0) for i in range(n)]
        moll = [[base[(i - s) % n] for i in range(n)] for s in range(n)]
        psis = kernels(a, moll)
        for s in range(n):
            for i in range(n):
                self.assertAlmostEqual(psis[s][i], psis[0][(i - s) % n], places=10)

    def test_integration_closed_form(self):
        n = 1000
        h = 1.0 / n
        ys = [(j * h) ** 2 / 2.0 for j in range(n + 1)]
        self.assertAlmostEqual(integration_estimate(ys, h, 0.3, 0.1), 0.3, places=12)
        self.assertAlmostEqual(integration_kernel_norm(0.1), math.sqrt(2.0) * 0.1 ** -1.5, places=9)

    def test_noise_bound_and_rate(self):
        n = 4000
        h = 1.0 / n
        ys = [(1.0 - math.cos(math.pi * j * h)) / math.pi for j in range(n + 1)]
        rng = random.Random(64)
        noise = [rng.gauss(0.0, 1.0) for _ in range(n + 1)]
        p, errs, deltas = 0.5, [], [1e-3, 1e-5]
        for delta in deltas:
            gamma = delta ** (2.0 / 7.0)
            scale = delta / pl_norm(noise, h)
            e = [scale * v for v in noise]
            clean = integration_estimate(ys, h, p, gamma)
            dirty = integration_estimate([u + v for u, v in zip(ys, e)], h, p, gamma)
            bound = delta * integration_kernel_norm(gamma)
            self.assertLessEqual(abs(dirty - clean), bound * (1.0 + 1e-9))
            # Worst case: the mollifier error and the full noise bound add up.
            errs.append(abs(clean - 1.0) + bound)
        slope = math.log(errs[0] / errs[1]) / math.log(deltas[0] / deltas[1])
        self.assertLess(abs(slope - 4.0 / 7.0), 0.15)

    def test_adjoint_of_integration(self):
        n = 50
        a = cumsum_matrix(n)
        at = transpose(a)
        rng = random.Random(65)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        self.assertLess(adjoint_gap(lambda v: matvec(a, v), lambda v: matvec(at, v), x, z), 1e-12)


if __name__ == "__main__":
    unittest.main()
