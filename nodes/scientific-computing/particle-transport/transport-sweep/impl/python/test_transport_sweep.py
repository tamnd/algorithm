# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transport-sweep/. The authors are listed in prov/WZRH6P.jsonl.
import math
import random
import unittest

from transport_sweep import (cartesian_mesh, sweep_dd_2d, sweep_order, sweep_step, triangle_mesh,
                             wavefronts)

OMEGA = (math.cos(0.4), math.sin(0.4))


def exact_absorber(x, y, sigma_t=1.0):
    # constant source 1, vacuum inflow: psi = (1 - exp(-sigma_t s)) / sigma_t, s = distance to the inflow side
    s = min(x / OMEGA[0], y / OMEGA[1])
    return (1.0 - math.exp(-sigma_t * s)) / sigma_t


def avg_exp(a, b):
    return (math.exp(-a) - math.exp(-b)) / (b - a)


class TestOrder(unittest.TestCase):
    def check_upwind_order(self, n_cells, faces, omega, order):
        pos = {c: k for k, c in enumerate(order)}
        self.assertEqual(sorted(order), list(range(n_cells)))
        for a, b, nx, ny, area in faces:
            if b < 0:
                continue
            g = omega[0] * nx + omega[1] * ny
            if g > 0:
                self.assertLess(pos[a], pos[b])
            elif g < 0:
                self.assertLess(pos[b], pos[a])

    def test_orders_are_upwind_for_many_directions(self):
        rng = random.Random(3)
        meshes = [cartesian_mesh(7, 5, 1.0, 2.0), triangle_mesh(6, 6, 1.0, 1.0)]
        for _ in range(20):
            a = rng.uniform(0.0, 2.0 * math.pi)
            omega = (math.cos(a), math.sin(a))
            for n_cells, faces, _, _ in meshes:
                order, blocked = sweep_order(n_cells, faces, omega)
                self.assertEqual(blocked, [])
                self.check_upwind_order(n_cells, faces, omega, order)

    def test_cycle_is_reported(self):
        faces = [(0, 1, 1.0, 0.0, 1.0), (1, 2, 0.0, 1.0, 1.0), (2, 0, 1.0, 0.0, 1.0), (2, 3, 1.0, 0.0, 1.0),
                 (4, 0, 1.0, 0.0, 1.0)]
        order, blocked = sweep_order(5, faces, (0.8, 0.6))
        self.assertEqual(order, [4])
        self.assertEqual(blocked, [0, 1, 2, 3])
        with self.assertRaises(ValueError):
            sweep_step(5, faces, [1.0] * 5, [1.0] * 5, [1.0] * 5, (0.8, 0.6))
        # the opposite normal on the face 2-0 breaks the cycle
        faces[2] = (2, 0, -1.0, 0.0, 1.0)
        order, blocked = sweep_order(5, faces, (0.8, 0.6))
        self.assertEqual(blocked, [])

    def test_wavefronts_of_a_grid(self):
        for nx, ny in ((4, 4), (7, 3), (16, 9)):
            n_cells, faces, _, _ = cartesian_mesh(nx, ny, 1.0, 1.0)
            level, count = wavefronts(n_cells, faces, (0.6, 0.8))
            self.assertEqual(count, nx + ny - 1)
            for j in range(ny):
                for i in range(nx):
                    self.assertEqual(level[i + nx * j], i + j + 1)
            _, count = wavefronts(n_cells, faces, (1.0, 0.0))
            self.assertEqual(count, nx)


class TestStepSweep(unittest.TestCase):
    def test_two_by_two_by_hand(self):
        n_cells, faces, vol, _ = cartesian_mesh(2, 2, 2.0, 2.0)
        psi, out, inflow = sweep_step(n_cells, faces, vol, [1.0] * 4, [1.0] * 4, (0.6, 0.8))
        for got, want in zip(psi, (1 / 2.4, 1.25 / 2.4, (4 / 3) / 2.4, 1.75 / 2.4)):
            self.assertAlmostEqual(got, want, places=14)
        self.assertAlmostEqual(out, 16.0 / 9.0, places=13)
        self.assertEqual(inflow, 0.0)

    def test_balance_and_positivity(self):
        rng = random.Random(11)
        for n_cells, faces, vol, _ in (cartesian_mesh(10, 8, 3.0, 2.0), triangle_mesh(9, 9, 2.0, 2.0)):
            st = [rng.uniform(0.1, 20.0) for _ in range(n_cells)]
            q = [rng.uniform(0.0, 5.0) for _ in range(n_cells)]
            for _ in range(5):
                a = rng.uniform(0.0, 2.0 * math.pi)
                omega = (math.cos(a), math.sin(a))
                psi, out, inflow = sweep_step(n_cells, faces, vol, st, q, omega, psi_in=0.7)
                absorbed = sum(s * p * v for s, p, v in zip(st, psi, vol))
                source = sum(x * v for x, v in zip(q, vol))
                self.assertAlmostEqual(absorbed + out, source + inflow, delta=1e-11 * (source + inflow))
                self.assertGreaterEqual(min(psi), 0.0)

    def test_pure_absorber_converges_at_first_order(self):
        errors = []
        for n in (8, 16, 32):
            n_cells, faces, vol, cent = triangle_mesh(n, n, 1.0, 1.0)
            psi, _, _ = sweep_step(n_cells, faces, vol, [1.0] * n_cells, [1.0] * n_cells, OMEGA)
            errors.append(sum(abs(p - exact_absorber(*xy)) * v for p, xy, v in zip(psi, cent, vol)))
        self.assertAlmostEqual(errors[0], 2.0361e-02, delta=1e-6)
        self.assertGreater(errors[0] / errors[1], 1.6)
        self.assertGreater(errors[1] / errors[2], 1.7)
        self.assertLess(errors[1] / errors[2], 2.2)

    def test_uniform_inflow_without_source_decays(self):
        n_cells, faces, vol, _ = cartesian_mesh(1, 1, 1.0, 1.0)
        psi, out, inflow = sweep_step(n_cells, faces, vol, [2.0], [0.0], (1.0, 0.0), psi_in=1.0)
        self.assertAlmostEqual(psi[0], 1.0 / 3.0, places=15)
        self.assertAlmostEqual(inflow, 1.0, places=15)
        self.assertAlmostEqual(out, 1.0 / 3.0, places=15)


class TestDiamond2D(unittest.TestCase):
    def manufactured(self, n, mu, eta, st=2.0):
        h = 1.0 / n
        ax = [avg_exp(i * h, (i + 1) * h) for i in range(n)]
        q = [[(st - abs(mu) - abs(eta)) * ax[i] * ax[j] for j in range(n)] for i in range(n)]
        cells, out_x, out_y = sweep_dd_2d(mu, eta, [[st] * n for _ in range(n)], q, [h] * n, [h] * n, ax, ax)
        return max(abs(cells[i][j] - ax[i] * ax[j]) for i in range(n) for j in range(n))

    def test_second_order(self):
        errs = [self.manufactured(n, 0.6, 0.3) for n in (8, 16, 32, 64)]
        for a, b in zip(errs, errs[1:]):
            self.assertGreater(a / b, 3.5)
            self.assertLess(a / b, 4.1)

    def test_direction_signs_mirror(self):
        rng = random.Random(5)
        nx, ny = 6, 4
        st = [[rng.uniform(0.5, 2.0) for _ in range(ny)] for _ in range(nx)]
        q = [[rng.uniform(0.0, 1.0) for _ in range(ny)] for _ in range(nx)]
        dx = [rng.uniform(0.1, 0.5) for _ in range(nx)]
        dy = [rng.uniform(0.1, 0.5) for _ in range(ny)]
        inc_x = [rng.uniform(0, 1) for _ in range(ny)]
        inc_y = [rng.uniform(0, 1) for _ in range(nx)]
        a, ax_, ay_ = sweep_dd_2d(0.7, 0.2, st, q, dx, dy, inc_x, inc_y)
        b, bx, by = sweep_dd_2d(-0.7, 0.2, st[::-1], q[::-1], dx[::-1], dy, inc_x, inc_y[::-1])
        for i in range(nx):
            for j in range(ny):
                self.assertAlmostEqual(a[i][j], b[nx - 1 - i][j], places=13)
        self.assertEqual(ax_, bx)

    def test_negative_outgoing_value_in_a_thick_cell(self):
        cells, out_x, out_y = sweep_dd_2d(0.1, 0.1, [[1.0]], [[0.0]], [1.0], [1.0], [1.0], [1.0])
        self.assertAlmostEqual(cells[0][0], 2.0 / 7.0, places=15)
        self.assertAlmostEqual(out_x[0], -3.0 / 7.0, places=15)
        self.assertAlmostEqual(out_y[0], -3.0 / 7.0, places=15)


if __name__ == "__main__":
    unittest.main()
