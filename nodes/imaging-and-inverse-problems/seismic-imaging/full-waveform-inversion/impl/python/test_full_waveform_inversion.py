# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/full-waveform-inversion/. The authors are listed in prov/H0DMN3.jsonl.
import math
import unittest

from full_waveform_inversion import forward, full_waveform_inversion, gradient, misfit, ricker

N_CELLS, H, DT, STEPS, F0 = 60, 10.0, 0.002, 300, 15.0  # v dt / h <= 0.5
SRC = 2
WAVELET = [ricker(k * DT - 1.2 / F0, F0) for k in range(STEPS)]


def v_true(i):
    base = 2000.0 if i < 25 else 2400.0
    return base + 300.0 * math.exp(-(((i - 40) / 4.0) ** 2))


M_TRUE = [1.0 / v_true(i) ** 2 for i in range(N_CELLS)]


def observed(recs):
    return forward(M_TRUE, SRC, WAVELET, recs, DT, H)[1]


class TestFullWaveformInversion(unittest.TestCase):
    def test_gradient_matches_finite_differences(self):
        recs = [2, 57]
        dobs = observed(recs)
        m0 = [1.0 / 2200.0 ** 2] * N_CELLS
        _, g = gradient(m0, SRC, WAVELET, recs, dobs, DT, H)
        for c in (10, 30, 45):
            step = 1e-3 * m0[c]
            mp, mm = list(m0), list(m0)
            mp[c] += step
            mm[c] -= step
            fd = (misfit(mp, SRC, WAVELET, recs, dobs, DT, H) - misfit(mm, SRC, WAVELET, recs, dobs, DT, H)) / (2.0 * step)
            self.assertLess(abs(fd - g[c]), 1e-5 * abs(g[c]))

    def test_misfit_decreases(self):
        recs = [2, 57]
        dobs = observed(recs)
        m0 = [1.0 / 2200.0 ** 2] * N_CELLS
        _, hist = full_waveform_inversion(m0, SRC, WAVELET, recs, dobs, DT, H, 10)
        for a, b in zip(hist, hist[1:]):
            self.assertLessEqual(b, a)
        self.assertLess(hist[-1], 0.05 * hist[0])

    def test_zero_residual_gives_zero_gradient(self):
        recs = [2, 57]
        dobs = observed(recs)
        j, g = gradient(M_TRUE, SRC, WAVELET, recs, dobs, DT, H)
        self.assertEqual(j, 0.0)
        self.assertEqual(max(abs(x) for x in g), 0.0)

    def test_cycle_skipping_local_minimum(self):
        # A constant true velocity of 2000 m/s, constant trial velocities and
        # one transmission receiver: the misfit has a local minimum near
        # 1625 m/s, where the predicted pulse is about one period late.
        recs = [57]
        dobs = forward([1.0 / 2000.0 ** 2] * N_CELLS, SRC, WAVELET, recs, DT, H)[1]

        def j_of(v):
            return misfit([1.0 / v ** 2] * N_CELLS, SRC, WAVELET, recs, dobs, DT, H)

        a, b, c = j_of(1600.0), j_of(1625.0), j_of(1650.0)
        self.assertLess(b, a)
        self.assertLess(b, c)
        self.assertGreater(j_of(1800.0), b)  # a barrier between it and the true model
        self.assertEqual(j_of(2000.0), 0.0)


if __name__ == "__main__":
    unittest.main()
