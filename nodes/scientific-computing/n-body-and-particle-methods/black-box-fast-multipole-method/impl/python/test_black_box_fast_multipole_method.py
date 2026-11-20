# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/black-box-fast-multipole-method/. The authors are listed in prov/T616YW.jsonl.
"""Tests for the black-box FMM: Chebyshev interpolation, exact shifts and three kernels against direct summation."""

import math
import random
import unittest

from black_box_fast_multipole_method import (
    _shift_down,
    _shift_up,
    bbfmm,
    box_center,
    cheb_nodes,
    child_shift,
    direct,
    inverse_distance,
    log_kernel,
    p2m,
    s_weights,
)


def inverse_multiquadric(x, y):
    return 1.0 / math.sqrt(abs(x - y) ** 2 + 0.01)


def rel(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) / math.sqrt(sum(y * y for y in b))


def uniform(n, seed):
    rng = random.Random(seed)
    z = [complex(rng.random(), rng.random()) for _ in range(n)]
    q = [rng.uniform(-1, 1) for _ in range(n)]
    return q, z


class TestChebyshev(unittest.TestCase):
    def test_lagrange_property(self):
        n = 6
        nodes = cheb_nodes(n)
        for k, xk in enumerate(nodes):
            s = s_weights(n, nodes, xk)
            for m in range(n):
                self.assertAlmostEqual(s[m], 1.0 if m == k else 0.0, places=12)

    def test_reproduces_polynomials(self):
        n = 5
        nodes = cheb_nodes(n)

        def poly(t):
            return 3 * t ** 4 - t ** 3 + 0.5 * t - 2

        for x in (-1.0, -0.3, 0.2, 0.9):
            s = s_weights(n, nodes, x)
            self.assertAlmostEqual(sum(poly(xm) * sm for xm, sm in zip(nodes, s)), poly(x), places=12)


class TestShifts(unittest.TestCase):
    def test_upward_shift_is_exact(self):
        n = 4
        nodes = cheb_nodes(n)
        shift = child_shift(n, nodes)
        rng = random.Random(3)
        level = 3
        w = 1.0 / (1 << level)
        child = (5, 2)
        c = box_center(*child, level)
        z = [c + complex((rng.random() - 0.5) * w, (rng.random() - 0.5) * w) for _ in range(7)]
        q = [rng.uniform(-1, 1) for _ in range(7)]
        wc = p2m(q, z, range(7), c, w, n, nodes)
        up = _shift_up(wc, shift[child[0] % 2], shift[child[1] % 2], n)
        wp = p2m(q, z, range(7), box_center(2, 1, 2), 2 * w, n, nodes)
        for a, b in zip(up, wp):
            self.assertAlmostEqual(a, b, places=12)

    def test_downward_shift_is_exact(self):
        n = 4
        nodes = cheb_nodes(n)
        shift = child_shift(n, nodes)
        rng = random.Random(4)
        gp = [rng.uniform(-1, 1) for _ in range(n * n)]
        gc = _shift_down(gp, shift[1], shift[0], n)
        for _ in range(5):
            x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
            px, py = (x + 1) / 2, (y - 1) / 2
            sx, sy = s_weights(n, nodes, x), s_weights(n, nodes, y)
            tx, ty = s_weights(n, nodes, px), s_weights(n, nodes, py)
            child_val = sum(sx[a] * sy[b] * gc[a * n + b] for a in range(n) for b in range(n))
            parent_val = sum(tx[a] * ty[b] * gp[a * n + b] for a in range(n) for b in range(n))
            self.assertAlmostEqual(child_val, parent_val, places=12)


class TestBBFMM(unittest.TestCase):
    def test_log_kernel_matches_direct(self):
        q, z = uniform(400, 5)
        ud = direct(q, z)
        errs = []
        for n in (2, 4, 6, 8):
            u, st = bbfmm(q, z, n=n, levels=3)
            errs.append(rel(u, ud))
        for k in range(3):
            self.assertLess(errs[k + 1], errs[k] / 10)
        self.assertLess(errs[-1], 1e-7)
        self.assertEqual(st["m2l"], 1272)

    def test_other_kernels(self):
        q, z = uniform(300, 6)
        for kernel in (inverse_distance, inverse_multiquadric):
            ud = direct(q, z, kernel)
            u, _ = bbfmm(q, z, kernel=kernel, n=6, levels=3)
            self.assertLess(rel(u, ud), 1e-5)

    def test_leaf_level_two(self):
        q, z = uniform(200, 7)
        ud = direct(q, z)
        u, _ = bbfmm(q, z, n=6, levels=2)
        self.assertLess(rel(u, ud), 1e-5)

    def test_linear_in_the_charges(self):
        q, z = uniform(150, 8)
        rng = random.Random(9)
        r = [rng.uniform(-1, 1) for _ in range(150)]
        u1, _ = bbfmm(q, z, n=4, levels=3)
        u2, _ = bbfmm(r, z, n=4, levels=3)
        u3, _ = bbfmm([a - 2 * b for a, b in zip(q, r)], z, n=4, levels=3)
        for a, b, c in zip(u1, u2, u3):
            self.assertAlmostEqual(c, a - 2 * b, places=9)

    def test_small_inputs(self):
        self.assertEqual(bbfmm([], [])[0], [])
        self.assertEqual(bbfmm([1.0], [complex(0.4, 0.6)])[0], [0.0])
        q = [1.0, -2.0, 0.5]
        z = [complex(0.1, 0.1), complex(0.9, 0.8), complex(0.15, 0.85)]
        u, _ = bbfmm(q, z, kernel=log_kernel, n=8)
        for a, b in zip(u, direct(q, z)):
            self.assertAlmostEqual(a, b, places=5)


if __name__ == "__main__":
    unittest.main()
