# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-step-fourier-migration/. The authors are listed in prov/C572NA.jsonl.
import cmath
import math
import unittest

from imgkit import dft, idft
from split_step_fourier_migration import kx_values, phase_error, split_step_fourier_migration

NT, DT = 64, 0.004


def ricker(t, f0):
    a = (math.pi * f0 * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def phase_shift_oracle(data, dt, dx, dz, vz):
    """Phase shift over the positive frequencies for a velocity v(z) only."""
    nt, nx = len(data), len(data[0])
    kxs = kx_values(nx, dx)
    spectra = [dft([data[k][j] for k in range(nt)]) for j in range(nx)]
    image = [[0.0] * nx for _ in vz]
    for k in range(1, (nt + 1) // 2):
        w = 2.0 * math.pi * k / (nt * dt)
        q = dft([spectra[j][k] for j in range(nx)])
        for i, v in enumerate(vz):
            p = idft(q)
            for j in range(nx):
                image[i][j] += 2.0 * p[j].real / nt
            s = 2.0 / v
            for j in range(nx):
                a = (w * s) ** 2 - kxs[j] ** 2
                q[j] = q[j] * cmath.exp(1j * math.sqrt(a) * dz) if a > 0.0 else 0j
    return image


class TestSplitStepFourierMigration(unittest.TestCase):
    def test_equals_phase_shift_when_v_depends_on_z_only(self):
        nx, dx, dz = 16, 10.0, 6.0
        data = [[0.0] * nx for _ in range(NT)]
        for j in range(nx):
            t0 = 2.0 * math.hypot(150.0, j * dx - 80.0) / 3000.0
            for k in range(NT):
                data[k][j] = ricker(k * DT - t0, 25.0)
        vz = [2500.0] * 10 + [3000.0] * 20
        a = split_step_fourier_migration(data, DT, dx, dz, [[v] * nx for v in vz])
        b = phase_shift_oracle(data, DT, dx, dz, vz)
        for i in range(len(vz)):
            for j in range(nx):
                self.assertAlmostEqual(a[i][j], b[i][j], delta=1e-9)

    def test_lateral_velocity_flat_reflector(self):
        # A flat reflector at z0 = 240 m under v(x) = 3000 + 300 cos(2 pi x / L):
        # the times 2 z0 / v(x) vary with x, and the split-step correction
        # brings every column back to row z0 / dz = 40.
        nx, dx, dz, nz = 32, 20.0, 6.0, 48
        vx = [3000.0 + 300.0 * math.cos(2.0 * math.pi * j / nx) for j in range(nx)]
        data = [[ricker(k * DT - 480.0 / vx[j], 25.0) for j in range(nx)] for k in range(NT)]
        img = split_step_fourier_migration(data, DT, dx, dz, [vx[:] for _ in range(nz)])
        for j in range(nx):
            self.assertEqual(max(range(nz), key=lambda i: img[i][j]), 40)

    def test_phase_error(self):
        w, dz = 2.0 * math.pi * 20.0, 6.0
        # Exact for vertical waves and for the reference slowness.
        self.assertAlmostEqual(phase_error(w, 1e-3, 8e-4, 0.0, dz), 0.0, places=12)
        self.assertAlmostEqual(phase_error(w, 1e-3, 1e-3, 0.05, dz), 0.0, places=12)
        # The error grows with the angle and with the slowness contrast.
        e1 = abs(phase_error(w, 1e-3, 9e-4, 0.03, dz))
        e2 = abs(phase_error(w, 1e-3, 9e-4, 0.06, dz))
        e3 = abs(phase_error(w, 1e-3, 8e-4, 0.06, dz))
        self.assertLess(e1, e2)
        self.assertLess(e2, e3)

    def test_kx_values(self):
        ks = kx_values(4, 1.0)
        self.assertEqual([round(k / (math.pi / 2.0)) for k in ks], [0, 1, -2, -1])


if __name__ == "__main__":
    unittest.main()
