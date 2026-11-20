# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-propagation-detection/. The authors are listed in prov/R4B3XS.jsonl.

import itertools
import math
import random
import unittest

import cbb
import constel
from expectation_propagation_detection import ep_detect, ep_real, real_alphabet, real_model, tilted_moments


def iid(rng: random.Random, m: int, n: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0 / m) for _ in range(n)] for _ in range(m)]


def posterior_moments(y, h, points, n0):
    """Exact marginal means and variances of Re x_k and Im x_k, by summing over all M^n vectors."""
    n = len(h[0])
    ws, xs = [], []
    for xv in itertools.product(points, repeat=n):
        r = cbb.sub(y, cbb.matvec(h, list(xv)))
        ws.append(-cbb.norm2(r) / n0)
        xs.append(xv)
    top = max(ws)
    ws = [math.exp(w - top) for w in ws]
    tot = sum(ws)
    comps = [lambda v: v.real, lambda v: v.imag]
    mean, var = [], []
    for part in comps:
        for k in range(n):
            mk = sum(w * part(xv[k]) for w, xv in zip(ws, xs)) / tot
            vk = sum(w * (part(xv[k]) - mk) ** 2 for w, xv in zip(ws, xs)) / tot
            mean.append(mk)
            var.append(vk)
    return mean, var


class TestExpectationPropagationDetection(unittest.TestCase):
    def test_tilted_moments_bpsk(self):
        for t, h2 in [(0.3, 0.5), (-1.2, 0.1), (2.0, 3.0), (40.0, 0.01)]:
            mean, var = tilted_moments(t, h2, [-1.0, 1.0])
            self.assertAlmostEqual(mean, math.tanh(t / h2), delta=1e-12)
            self.assertAlmostEqual(var, 1.0 - math.tanh(t / h2) ** 2, delta=1e-12)

    def test_first_q_is_lmmse(self):
        rng = random.Random(2201)
        pts = constel.qam(4)
        n0 = 0.3
        for _ in range(5):
            h = iid(rng, 6, 4)
            y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(4)] for _ in range(4)]), n0)
            yr, hr = real_model(y, h)
            mu, _ = ep_real(yr, hr, real_alphabet(pts), n0 / 2.0, iters=0)
            a = cbb.add(cbb.matmul(cbb.herm(h), h), cbb.scale(n0, cbb.eye(4)))
            want = cbb.solve(a, cbb.matvec(cbb.herm(h), y))
            for k in range(4):
                self.assertAlmostEqual(mu[k], want[k].real, delta=1e-9)
                self.assertAlmostEqual(mu[4 + k], want[k].imag, delta=1e-9)

    def test_page_example(self):
        h = [[1.0, 0.5], [0.5, 1.0]]
        y = [0.2, 0.6]
        bpsk = constel.pam(2)
        yr, hr = real_model(y, h, True)
        mu0, var0 = ep_real(yr, hr, [-1.0, 1.0], 0.3, iters=0)
        for got, want in zip(mu0 + var0, [0.0535, 0.4171, 0.3316, 0.3316]):
            self.assertAlmostEqual(got, want, delta=1e-4)
        mu1, var1 = ep_real(yr, hr, [-1.0, 1.0], 0.3, iters=1, damping=1.0)
        for got, want in zip(mu1 + var1, [-0.2261, 0.8505, 0.3087, 0.2766]):
            self.assertAlmostEqual(got, want, delta=1e-4)
        mu5, _ = ep_real(yr, hr, [-1.0, 1.0], 0.3, iters=5, damping=1.0)
        for a, b in zip(mu1, mu5):
            self.assertAlmostEqual(a, b, delta=1e-12)
        self.assertEqual(constel.ml_vector(y, h, bpsk), [1, 0])
        self.assertEqual(ep_detect(y, h, bpsk, 0.6, damping=1.0), [1, 0])

    def test_correlated_channel_can_fail(self):
        # Columns with correlation 3 / sqrt(10): EP settles on (-1, +1), ML is (+1, -1).
        h = [[2.0, 1.0], [1.0, 1.0]]
        y = [0.5, 0.6]
        bpsk = constel.pam(2)
        self.assertEqual(constel.ml_vector(y, h, bpsk), [0, 1])
        self.assertEqual(ep_detect(y, h, bpsk, 0.25, damping=1.0), [1, 0])
        yr, hr = real_model(y, h, True)
        mu, _ = ep_real(yr, hr, [-1.0, 1.0], 0.125, iters=10, damping=1.0)
        self.assertAlmostEqual(mu[0], -1.0, delta=1e-3)
        self.assertAlmostEqual(mu[1], 1.0, delta=1e-3)

    def test_orthogonal_channel_gives_exact_marginals(self):
        # H = U diag(d) with U a rotation, so H^H H is diagonal. The gains are small enough
        # that the cavity variance s2 / |d|^2 is above 0.9 = max a^2, so every update is kept.
        rng = random.Random(2202)
        pts = constel.qam(16)
        n0 = 1.0
        for _ in range(4):
            d = [0.6 * complex(math.cos(p), math.sin(p)) for p in (rng.uniform(0, 6.3), rng.uniform(0, 6.3))]
            d[1] *= 5.0 / 6.0
            phi = rng.uniform(0, 6.3)
            c, s = math.cos(phi), math.sin(phi)
            h = [[c * d[0], -s * d[1]], [s * d[0], c * d[1]]]
            y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(16)] for _ in range(2)]), n0)
            yr, hr = real_model(y, h)
            mu, var = ep_real(yr, hr, real_alphabet(pts), n0 / 2.0, iters=40)
            mean, vexact = posterior_moments(y, h, pts, n0)
            for a, b in zip(mu, mean):
                self.assertAlmostEqual(a, b, delta=1e-6)
            for a, b in zip(var, vexact):
                self.assertAlmostEqual(a, b, delta=1e-6)

    def test_agrees_with_ml_at_high_snr(self):
        # 4-QAM, n = 4, m = 4, 15 dB, seed 2204: 97 of 100 in the reference run.
        rng = random.Random(2204)
        pts = constel.qam(4)
        n0 = cbb.undb(-15.0)
        agree = 0
        for _ in range(100):
            h = iid(rng, 4, 4)
            y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(4)] for _ in range(4)]), n0)
            agree += ep_detect(y, h, pts, n0) == constel.ml_vector(y, h, pts)
        self.assertGreaterEqual(agree, 92)

    def test_fewer_errors_than_lmmse(self):
        # 4-QAM, n = m = 8, 10 dB, seed 2206, 40 vectors (320 symbols): 19 errors against 38.
        rng = random.Random(2206)
        pts = constel.qam(4)
        n0 = cbb.undb(-10.0)
        e_ep = e_lin = 0
        for _ in range(40):
            h = iid(rng, 8, 8)
            idx = [rng.randrange(4) for _ in range(8)]
            y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), n0)
            e_ep += sum(a != b for a, b in zip(ep_detect(y, h, pts, n0), idx))
            e_lin += sum(a != b for a, b in zip(ep_detect(y, h, pts, n0, iters=0), idx))
        self.assertLessEqual(5 * e_ep, 3 * e_lin)


if __name__ == "__main__":
    unittest.main()
