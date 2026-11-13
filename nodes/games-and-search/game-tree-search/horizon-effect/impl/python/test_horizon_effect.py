# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizon-effect/. The authors are listed in prov/86NNG4.jsonl.

import random
import unittest

from horizon_effect import (
    capture_past_horizon,
    delaying_sacrifice,
    exact_value,
    limited_value,
    quiesce_value,
    random_material_tree,
    root_choice,
    wrong_choices,
)


def with_stop_leaves(kids, static):
    """The capture-or-stop game as an explicit tree: keep the captures only, and
    give each node one more leaf child "stop" worth its static score to the mover."""
    k2, s2 = {}, dict(static)
    for n in static:
        row = [(c, True) for c, cap in kids.get(n, []) if cap]
        stop = n + "/stop"
        s2[stop] = -static[n]
        k2[n] = row + [(stop, False)]
    return k2, s2


class TestHorizonEffect(unittest.TestCase):
    def test_capture_past_horizon(self):
        kids, static = capture_past_horizon()
        self.assertEqual(exact_value(kids, static, "A"), 0)
        self.assertEqual(-exact_value(kids, static, "QxP"), -8)
        self.assertEqual(root_choice(kids, static, "A", 1, False), ("QxP", 1))
        self.assertEqual(root_choice(kids, static, "A", 1, True), ("quiet", 0))

    def test_delaying_sacrifice(self):
        kids, static = delaying_sacrifice()
        self.assertEqual(-exact_value(kids, static, "let"), -9)
        self.assertEqual(-exact_value(kids, static, "sac"), -10)
        # Depth 2, with or without quiescence, gives up the pawn and still loses the queen.
        self.assertEqual(root_choice(kids, static, "R", 2, False), ("sac", -1))
        self.assertEqual(root_choice(kids, static, "R", 2, True), ("sac", -1))
        self.assertEqual(root_choice(kids, static, "R", 3, False), ("sac", -1))
        # One more ply, with quiescence, sees the queen capture and finds the true value.
        self.assertEqual(root_choice(kids, static, "R", 3, True), ("let", -9))
        self.assertEqual(root_choice(kids, static, "R", 4, False), ("let", -9))

    def test_quiescence_equals_full_search_of_capture_subtree(self):
        rng = random.Random(11)
        checked = 0
        for _ in range(60):
            kids, static = random_material_tree(rng, 3, 4)
            k2, s2 = with_stop_leaves(kids, static)
            for n in static:
                self.assertEqual(quiesce_value(kids, static, n), exact_value(k2, s2, n))
                checked += 1
        self.assertEqual(checked, 60 * 121)

    def test_full_depth_is_exact(self):
        rng = random.Random(12)
        for _ in range(500):
            kids, static = random_material_tree(rng, 2, 5)
            for flag in (False, True):
                self.assertEqual(limited_value(kids, static, "r", 5, flag), exact_value(kids, static, "r"))

    def test_measured_wrong_choices(self):
        # The page states these counts: seed 2024, 300 trees, b = 3, height 6.
        self.assertEqual(wrong_choices(2024, 300, 3, 6, 1), (113, 58))
        self.assertEqual(wrong_choices(2024, 300, 3, 6, 2), (71, 41))


if __name__ == "__main__":
    unittest.main()
