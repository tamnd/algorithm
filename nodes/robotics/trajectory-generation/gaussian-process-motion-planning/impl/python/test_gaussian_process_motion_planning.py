# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-process-motion-planning/. The authors are listed in prov/6FK8HV.jsonl.
import random
import unittest

from gaussian_process_motion_planning import (
    Problem,
    block_tridiag_solve,
    disc_sd,
    gpmp,
    interpolation,
    min_clearance,
    phi,
    q_inv,
    solve_dense,
    straight_init,
    support_clearance,
)

Q0, Q1 = [-1.0, 0.0], [1.0, 0.0]
DISC = disc_sd(0.0, -0.15, 0.5)


def hermite(s0, s1, dt, tau):
    """Position and velocity of the cubic Hermite interpolant, one coordinate per call."""
    out = []
    for c in range(2):
        p0, v0, p1, v1 = s0[c], s0[c + 2], s1[c], s1[c + 2]
        u = tau / dt
        h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
        d00, d10, d01, d11 = 6 * u ** 2 - 6 * u, 3 * u ** 2 - 4 * u + 1, -6 * u ** 2 + 6 * u, 3 * u ** 2 - 2 * u
        out.append((h00 * p0 + h10 * dt * v0 + h01 * p1 + h11 * dt * v1,
                    (d00 * p0 + d10 * dt * v0 + d01 * p1 + d11 * dt * v1) / dt))
    return out


def dense_clearance(prob, x, per=40):
    s = prob.states(x)
    best = float("inf")
    for i in range(prob.n):
        for j in range(per + 1):
            lam, psi = interpolation(prob.dt, prob.dt * j / per, prob.qc)
            p = [sum(lam[r][k] * s[i][k] + psi[r][k] * s[i + 1][k] for k in range(4)) for r in range(2)]
            best = min(best, DISC(p)[0])
    return best


class TestWorkedExample(unittest.TestCase):
    def test_disc_with_interpolation(self):
        prob = Problem(Q0, Q1, 1.0, 5, [DISC], eps=0.1, sigma=0.02, n_ip=4)
        x, hist = gpmp(prob)
        self.assertAlmostEqual(hist[0], 1660.597, places=2)
        self.assertAlmostEqual(hist[-1], 42.7862, places=3)
        self.assertEqual(len(hist) - 1, 7)
        self.assertTrue(all(b < a for a, b in zip(hist, hist[1:])))
        self.assertAlmostEqual(min_clearance(prob, x), 0.0857, places=3)
        self.assertGreater(dense_clearance(prob, x), 0.08)

    def test_without_interpolation_the_curve_cuts_closer(self):
        prob = Problem(Q0, Q1, 1.0, 5, [DISC], eps=0.1, sigma=0.02, n_ip=0)
        x, hist = gpmp(prob)
        self.assertAlmostEqual(support_clearance(prob, x), 0.0811, places=3)
        self.assertLess(dense_clearance(prob, x), 0.03)


class TestEdgeCases(unittest.TestCase):
    def test_free_space_gives_the_minimum_acceleration_cubic(self):
        prob = Problem(Q0, Q1, 1.0, 10, [])
        x, hist = gpmp(prob)
        self.assertAlmostEqual(hist[-1], 24.0, places=6)
        for i, s in enumerate(x, start=1):
            u = i / 10.0
            self.assertAlmostEqual(s[0], -1.0 + 2.0 * (3 * u * u - 2 * u ** 3), places=5)
            self.assertAlmostEqual(s[2], 2.0 * (6 * u - 6 * u * u), places=4)
            self.assertAlmostEqual(s[1], 0.0, places=9)

    def test_interpolation_is_cubic_hermite(self):
        rng = random.Random(3)
        for _ in range(5):
            dt = rng.uniform(0.1, 1.0)
            tau = rng.uniform(0.0, dt)
            s0 = [rng.uniform(-1, 1) for _ in range(4)]
            s1 = [rng.uniform(-1, 1) for _ in range(4)]
            lam, psi = interpolation(dt, tau, rng.uniform(0.5, 2.0))
            st = [sum(lam[r][k] * s0[k] + psi[r][k] * s1[k] for k in range(4)) for r in range(4)]
            h = hermite(s0, s1, dt, tau)
            for c in range(2):
                self.assertAlmostEqual(st[c], h[c][0], places=9)
                self.assertAlmostEqual(st[c + 2], h[c][1], places=9)

    def test_prior_factor_is_the_minimum_energy(self):
        rng = random.Random(8)
        dt, qc = 0.7, 1.3
        s0 = [rng.uniform(-1, 1) for _ in range(4)]
        s1 = [rng.uniform(-1, 1) for _ in range(4)]
        e = [s1[k] - sum(phi(dt)[k][j] * s0[j] for j in range(4)) for k in range(4)]
        w = q_inv(dt, qc)
        factor = 0.5 * sum(e[a] * w[a][b] * e[b] for a in range(4) for b in range(4))
        # the Hermite cubic has a linear second derivative, so Simpson's rule is exact
        energy = 0.0
        for c in range(2):
            p0, v0, p1, v1 = s0[c], s0[c + 2], s1[c], s1[c + 2]
            a2 = (3 * (p1 - p0) - (2 * v0 + v1) * dt) / dt ** 2
            a3 = (2 * (p0 - p1) + (v0 + v1) * dt) / dt ** 3
            acc = [2 * a2 + 6 * a3 * t for t in (0.0, dt / 2, dt)]
            energy += dt / 6 * (acc[0] ** 2 + 4 * acc[1] ** 2 + acc[2] ** 2)
        self.assertAlmostEqual(factor, 0.5 * energy / qc, places=9)

    def test_block_solve_matches_dense(self):
        rng = random.Random(11)
        m = 4
        diag = [[[rng.uniform(-0.2, 0.2) for _ in range(4)] for _ in range(4)] for _ in range(m)]
        for i in range(m):
            diag[i] = [[(diag[i][p][q] + diag[i][q][p]) / 2 + (5.0 if p == q else 0.0) for q in range(4)] for p in range(4)]
        off = [[[rng.uniform(-1, 1) for _ in range(4)] for _ in range(4)] for _ in range(m - 1)]
        rhs = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(m)]
        big = [[0.0] * (4 * m) for _ in range(4 * m)]
        for i in range(m):
            for p in range(4):
                for q in range(4):
                    big[4 * i + p][4 * i + q] = diag[i][p][q]
                    if i < m - 1:
                        big[4 * i + p][4 * i + 4 + q] = off[i][p][q]
                        big[4 * i + 4 + q][4 * i + p] = off[i][p][q]
        ref = solve_dense(big, [[v] for r in rhs for v in r])
        got = block_tridiag_solve(diag, off, rhs)
        for i in range(m):
            for p in range(4):
                self.assertAlmostEqual(got[i][p], ref[4 * i + p][0], places=9)

    def test_gradient_matches_finite_differences(self):
        prob = Problem(Q0, Q1, 1.0, 4, [DISC], eps=0.1, sigma=0.05, n_ip=2)
        x = straight_init(prob)
        x[1][1] += 0.03
        _, _, g = prob.normal_equations(x)
        h = 1e-6
        for i in range(len(x)):
            for k in range(4):
                xp = [list(s) for s in x]
                xm = [list(s) for s in x]
                xp[i][k] += h
                xm[i][k] -= h
                fd = (prob.cost(xp) - prob.cost(xm)) / (2 * h)
                self.assertAlmostEqual(g[i][k], fd, delta=1e-4 * max(1.0, abs(fd)))


class TestRandomized(unittest.TestCase):
    def test_cost_decreases_on_random_scenes(self):
        rng = random.Random(2018)
        for _ in range(3):
            sds = [disc_sd(rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.2), rng.uniform(0.1, 0.3)) for _ in range(2)]
            prob = Problem(Q0, Q1, 1.0, 6, sds, eps=0.1, sigma=0.05, n_ip=2)
            x, hist = gpmp(prob, iters=30)
            self.assertTrue(all(b < a for a, b in zip(hist, hist[1:])))
            self.assertLessEqual(hist[-1], hist[0])


if __name__ == "__main__":
    unittest.main()
