# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-from-focus/. The authors are listed in prov/09NTD3.jsonl.

import math
import random
import unittest

from shape_from_focus import (defocus_stack, gaussian_peak_offset, modified_laplacian,
                              shape_from_focus, sum_modified_laplacian, window_sum)


class ShapeFromFocusTest(unittest.TestCase):
    def test_modified_laplacian_by_hand(self):
        img = [[0, 7, 0], [4, 10, 6], [0, 9, 0]]
        self.assertEqual(modified_laplacian(img)[1][1], 14.0)
        flat = [[5.0] * 4 for _ in range(4)]
        self.assertEqual(modified_laplacian(flat), [[0.0] * 4 for _ in range(4)])

    def test_window_sum_matches_direct_sum(self):
        rng = random.Random(1)
        vals = [[rng.random() for _ in range(7)] for _ in range(5)]
        got = window_sum(vals, 2)
        for v in range(5):
            for u in range(7):
                want = sum(vals[y][x] for y in range(max(v - 2, 0), min(v + 3, 5))
                           for x in range(max(u - 2, 0), min(u + 3, 7)))
                self.assertAlmostEqual(got[v][u], want, places=9)

    def test_gaussian_fit_is_exact_for_gaussian_profiles(self):
        rng = random.Random(2)
        for _ in range(50):
            center, width, height = rng.uniform(1.0, 7.0), rng.uniform(0.7, 3.0), rng.uniform(1.0, 50.0)
            F = [height * math.exp(-(k - center) ** 2 / (2.0 * width * width)) for k in range(9)]
            m = max(range(9), key=lambda k: F[k])
            self.assertAlmostEqual(m + gaussian_peak_offset(F[m - 1], F[m], F[m + 1]), center, places=9)
        self.assertAlmostEqual(gaussian_peak_offset(40.0, 100.0, 70.0), 0.2198, places=4)
        self.assertIsNone(gaussian_peak_offset(10.0, 5.0, 10.0))
        self.assertIsNone(gaussian_peak_offset(0.0, 5.0, 1.0))

    def test_gain_and_offset_do_not_change_the_choice(self):
        rng = random.Random(3)
        tex = [[rng.randint(0, 255) for _ in range(16)] for _ in range(16)]
        d = [[1.0 + 0.4 * u for u in range(16)] for _ in range(16)]
        stack = defocus_stack(tex, d, 9, 0.8)
        _, best = shape_from_focus(stack)
        brighter = [[[3.0 * x + 40.0 for x in row] for row in img] for img in stack]
        _, best2 = shape_from_focus(brighter)
        self.assertEqual(best, best2)
        a = sum_modified_laplacian(stack[0])
        b = sum_modified_laplacian(brighter[0])
        self.assertAlmostEqual(b[5][5], 3.0 * a[5][5], places=6)

    def test_recovers_a_slanted_plane(self):
        rng = random.Random(1)
        size = 24
        tex = [[rng.randint(0, 255) for _ in range(size)] for _ in range(size)]
        truth = [[2.0 + 4.0 * u / (size - 1) for u in range(size)] for _ in range(size)]
        stack = defocus_stack(tex, truth, 9, 0.8)
        depth, best = shape_from_focus(stack, radius=2)
        frame_err = [abs(best[v][u] - truth[v][u]) for v in range(size) for u in range(size)]
        fit_err = [abs(depth[v][u] - truth[v][u]) for v in range(size) for u in range(size)]
        self.assertLessEqual(max(frame_err), 1.0)
        self.assertLess(sum(fit_err) / len(fit_err), 0.1)
        self.assertLess(sum(fit_err), 0.5 * sum(frame_err))

    def test_focus_measure_peaks_at_the_sharp_frame(self):
        rng = random.Random(4)
        tex = [[rng.randint(0, 255) for _ in range(12)] for _ in range(12)]
        d = [[4.0] * 12 for _ in range(12)]
        stack = defocus_stack(tex, d, 9, 0.8)
        totals = [sum(map(sum, sum_modified_laplacian(img))) for img in stack]
        self.assertEqual(max(range(9), key=lambda k: totals[k]), 4)
        # Near focus the measure falls on both sides. Far from focus the cut-off
        # kernel is no longer a Gaussian and the fall need not be monotone.
        for k in (2, 3):
            self.assertLess(totals[k], totals[k + 1])
            self.assertGreater(totals[8 - k - 1], totals[8 - k])


if __name__ == "__main__":
    unittest.main()
