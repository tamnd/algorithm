# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elastic-bands/. The authors are listed in prov/32ZJAX.jsonl.
import random
import unittest

from elastic_bands import (
    disc_world,
    elastic_band,
    is_valid,
    length,
    overlap,
    polyline,
    segment_clearance,
    update,
)

START = polyline([(-1.0, 0.0), (-0.8, 0.9), (0.8, 0.9), (1.0, 0.0)], 0.2)


class TestWorkedExample(unittest.TestCase):
    def test_band_around_a_disc(self):
        rho = disc_world([(0.0, 0.0, 0.5)])
        self.assertTrue(is_valid(START, rho))
        self.assertAlmostEqual(length(START), 3.4439, places=4)
        band = START
        for _ in range(20):
            band = update(band, rho)
            self.assertTrue(is_valid(band, rho))
        self.assertAlmostEqual(length(band), 2.5579, places=3)
        self.assertEqual(len(band), 10)
        self.assertAlmostEqual(segment_clearance(band, rho), 0.2069, places=3)
        self.assertAlmostEqual(max(p[1] for p in band), 0.7268, places=3)
        self.assertEqual((band[0], band[-1]), (START[0], START[-1]))

    def test_slow_obstacle_keeps_the_band_valid(self):
        rho = disc_world([(0.0, 0.0, 0.5)])
        band, _ = elastic_band(START, rho, sweeps=20)
        y = 1.5
        for _ in range(25):
            y -= 0.03
            world = disc_world([(0.0, 0.0, 0.5), (-0.4, y, 0.15)])
            self.assertTrue(is_valid(band, world))
            band = update(band, world)
            self.assertTrue(is_valid(band, world))
            self.assertGreater(segment_clearance(band, world), 0.05)


class TestEdgeCases(unittest.TestCase):
    def test_free_space_gives_the_segment(self):
        rho = disc_world([(0.0, 5.0, 0.1)])
        band, lengths = elastic_band(START, rho, sweeps=10)
        self.assertAlmostEqual(lengths[-1], 2.0, places=9)
        self.assertEqual(band, [(-1.0, 0.0), (1.0, 0.0)])

    def test_fast_obstacle_can_break_the_band(self):
        # The guarantee is for a fixed scene: an obstacle that jumps can cut the band.
        rho = disc_world([(0.0, 0.0, 0.5)])
        band, _ = elastic_band(START, rho, sweeps=20)
        broken = False
        y = 1.5
        while y > 0.75 and not broken:
            y -= 0.1
            world = disc_world([(0.0, 0.0, 0.5), (-0.4, y, 0.15)])
            if not is_valid(band, world):
                broken = True
            else:
                band = update(band, world)
        self.assertTrue(broken)

    def test_midpoint_of_overlapping_bubbles_overlaps_both(self):
        rng = random.Random(1993)
        checked = 0
        while checked < 300:
            discs = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0.05, 0.3)) for _ in range(3)]
            rho = disc_world(discs)
            a = (rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
            b = (a[0] + rng.uniform(-0.5, 0.5), a[1] + rng.uniform(-0.5, 0.5))
            ra, rb = rho(a)[0], rho(b)[0]
            if ra <= 0 or rb <= 0 or not overlap(a, b, ra, rb):
                continue
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            rm = rho(m)[0]
            self.assertGreater(rm, 0.0)
            self.assertTrue(overlap(a, m, ra, rm))
            self.assertTrue(overlap(m, b, rm, rb))
            checked += 1


class TestRandomized(unittest.TestCase):
    def test_invariant_on_random_scenes(self):
        rng = random.Random(7)
        done = 0
        while done < 4:
            discs = [(rng.uniform(-0.7, 0.7), rng.uniform(-0.6, 0.4), rng.uniform(0.1, 0.3)) for _ in range(4)]
            rho = disc_world(discs)
            start = polyline([(-1.5, 0.0), (-1.5, 1.2), (1.5, 1.2), (1.5, 0.0)], 0.1)
            if not is_valid(start, rho):
                continue
            band = start
            for _ in range(30):
                band = update(band, rho)
                self.assertTrue(is_valid(band, rho))
            self.assertGreater(segment_clearance(band, rho), 0.0)
            self.assertLess(length(band), length(start))
            done += 1


if __name__ == "__main__":
    unittest.main()
