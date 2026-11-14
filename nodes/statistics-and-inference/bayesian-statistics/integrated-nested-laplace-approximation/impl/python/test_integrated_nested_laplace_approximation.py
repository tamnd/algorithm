# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integrated-nested-laplace-approximation/. The authors are listed in prov/VKP2D8.jsonl.
"""Tests for INLA: exactness for a Gaussian likelihood, the inner Newton mode, and a
comparison with brute-force numerical integration on a tiny Poisson model with one
hyperparameter on a grid."""

import math
import random
import unittest

from integrated_nested_laplace_approximation import (
    chol_solve,
    cholesky,
    inla,
    inner_mode,
    log_det,
    poisson_log_link,
    gaussian,
    rw_precision,
)


def log_prior(th):
    # tau = exp(th) ~ Gamma(1, 1), so pi(th) = exp(th) exp(-exp(th)).
    return th - math.exp(th)


def brute_force(q_of, lik, thetas, grid1, grid2):
    """pi(theta | y) on the grid, pi(x_1 | y) on grid1, and log p(y), by the trapezoid rule
    over a box in (x_1, x_2) for each theta (two latent values only)."""
    l1 = [lik(0, v)[0] for v in grid1]
    l2 = [lik(1, v)[0] for v in grid2]
    h1, h2 = grid1[1] - grid1[0], grid2[1] - grid2[0]
    logs, margs = [], []
    for th in thetas:
        q = q_of(th)
        base = log_prior(th) + 0.5 * log_det(cholesky(q)) - math.log(2 * math.pi)
        cells = [[base + l1[a] + l2[b] - 0.5 * (q[0][0] * u * u + 2 * q[0][1] * u * v + q[1][1] * v * v)
                  for b, v in enumerate(grid2)] for a, u in enumerate(grid1)]
        top = max(max(r) for r in cells)
        rows = [math.fsum(math.exp(c - top) for c in r) * h2 for r in cells]
        tot = math.fsum(rows) * h1
        logs.append(math.log(tot) + top)
        margs.append([r / tot for r in rows])
    top = max(logs)
    w = [math.exp(v - top) for v in logs]
    s = math.fsum(w)
    w = [v / s for v in w]
    mix = [math.fsum(w[k] * margs[k][g] for k in range(len(thetas))) for g in range(len(grid1))]
    mean = math.fsum(z * f for z, f in zip(grid1, mix)) * h1
    sd = math.sqrt(math.fsum((z - mean) ** 2 * f for z, f in zip(grid1, mix)) * h1)
    log_evidence = top + math.log(s * (thetas[1] - thetas[0]))
    return w, mix, mean, sd, log_evidence


class TestGaussianLikelihoodIsExact(unittest.TestCase):
    def test_hyperparameter_posterior_and_marginals_are_exact(self):
        rng = random.Random(5)
        n, s2 = 4, 0.5
        ys = [rng.gauss(1.0, 1.0) for _ in range(n)]
        lik = gaussian(ys, s2)
        thetas = [-2 + 0.25 * k for k in range(17)]
        zs = [-4 + 0.02 * a for a in range(451)]

        def q_of(th):
            return rw_precision(n, math.exp(th), 0.5)

        def exact_log_marginal(th):
            # y ~ N(0, Q^-1 + s2 I)
            q = q_of(th)
            low = cholesky(q)
            cov = [chol_solve(low, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
            for i in range(n):
                cov[i][i] += s2
            lc = cholesky(cov)
            return -0.5 * log_det(lc) - 0.5 * math.fsum(a * b for a, b in zip(ys, chol_solve(lc, ys))) - 0.5 * n * math.log(2 * math.pi)

        exact = [log_prior(t) + exact_log_marginal(t) for t in thetas]
        for strategy in ("gaussian", "laplace"):
            r = inla(q_of, log_prior, lik, thetas, 1, zs, strategy=strategy)
            for k in range(len(thetas)):
                self.assertAlmostEqual(r["log_post"][k] - r["log_post"][0], exact[k] - exact[0], places=9)
            # the marginal of x_1 is the exact mixture of normals
            top = max(exact)
            w = [math.exp(v - top) for v in exact]
            w = [v / math.fsum(w) for v in w]
            for g in range(0, len(zs), 25):
                z = zs[g]
                d = 0.0
                for k, t in enumerate(thetas):
                    q = q_of(t)
                    p = [[q[i][j] + (1 / s2 if i == j else 0.0) for j in range(n)] for i in range(n)]
                    lp = cholesky(p)
                    m = chol_solve(lp, [v / s2 for v in ys])[1]
                    v = chol_solve(lp, [0.0, 1.0, 0.0, 0.0])[1]
                    d += w[k] * math.exp(-0.5 * (z - m) ** 2 / v) / math.sqrt(2 * math.pi * v)
                self.assertAlmostEqual(r["density"][g], d, delta=1e-6)


class TestInnerMode(unittest.TestCase):
    def test_gradient_vanishes_at_the_mode(self):
        rng = random.Random(6)
        for _ in range(100):
            n = rng.randint(1, 6)
            ys = [rng.randint(0, 12) for _ in range(n)]
            lik = poisson_log_link(ys)
            q = rw_precision(n, math.exp(rng.uniform(-3, 3)), rng.uniform(0.1, 2))
            fixed = {rng.randrange(n): rng.uniform(-2, 3)} if n > 1 and rng.random() < 0.5 else None
            x, _ = inner_mode(q, lik, [0.0] * n, fixed=fixed)
            for i in range(n):
                if fixed and i in fixed:
                    self.assertEqual(x[i], fixed[i])
                    continue
                grad = lik(i, x[i])[1] - math.fsum(q[i][j] * x[j] for j in range(n))
                self.assertLess(abs(grad), 1e-8)


class TestAgainstBruteForce(unittest.TestCase):
    def test_tiny_poisson_model(self):
        # y = (3, 7), y_j ~ Poisson(exp(x_j)), Q = tau [[2, -1], [-1, 2]], tau ~ Gamma(1, 1).
        lik = poisson_log_link((3, 7))

        def q_of(th):
            return rw_precision(2, math.exp(th))

        thetas = [-6 + 0.1 * k for k in range(101)]
        grid = [-4 + 0.05 * a for a in range(181)]
        wb, mb, mean_b, sd_b, log_ev = brute_force(q_of, lik, thetas, grid, grid)
        lap = inla(q_of, log_prior, lik, thetas, 0, grid, strategy="laplace")
        gau = inla(q_of, log_prior, lik, thetas, 0, grid, strategy="gaussian")
        h = grid[1] - grid[0]
        self.assertLess(0.5 * sum(abs(a - b) for a, b in zip(wb, lap["weights"])), 0.01)
        # the log evidence from the weights of L4
        top = max(lap["log_post"])
        log_ev_inla = top + math.log(math.fsum(math.exp(v - top) for v in lap["log_post"]) * 0.1)
        self.assertLess(abs(log_ev_inla - log_ev), 0.03)
        # full Laplace marginal of x_1 is close; the Gaussian one misses the skewness
        self.assertLess(abs(lap["mean"] - mean_b), 0.002)
        self.assertLess(abs(lap["sd"] - sd_b), 0.002)
        self.assertLess(0.5 * h * sum(abs(a - b) for a, b in zip(mb, lap["density"])), 0.002)
        self.assertGreater(gau["mean"] - mean_b, 0.05)
        self.assertGreater(0.5 * h * sum(abs(a - b) for a, b in zip(mb, gau["density"])), 0.03)


if __name__ == "__main__":
    unittest.main()
