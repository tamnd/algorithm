# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rubiks-cube-problem/. The authors are listed in prov/CVDGSV.jsonl.
import random
import unittest

from rubiks_cube_problem import (
    HTM,
    MOVES,
    QTM,
    SOLVED,
    apply,
    assemblies,
    ball,
    distance_meet_in_middle,
    invariants,
    layer_counts,
    multiply,
    order,
    state_count,
    superflip,
)


class TestMoves(unittest.TestCase):
    def test_orders(self):
        for f in "URFDLB":
            self.assertEqual(order([f]), 4)
            self.assertEqual(order([f + "2"]), 2)
        self.assertEqual(order("R U".split()), 105)
        self.assertEqual(order("R U R' U'".split()), 6)

    def test_inverse(self):
        rnd = random.Random(1)
        seq = [rnd.choice(HTM) for _ in range(30)]
        inv = [m[0] + {"": "'", "'": "", "2": "2"}[m[1:]] for m in reversed(seq)]
        self.assertEqual(apply(apply(SOLVED, seq), inv), SOLVED)

    def test_opposite_faces_commute(self):
        for a, b in (("U", "D"), ("R", "L"), ("F", "B")):
            self.assertEqual(apply(SOLVED, [a, b]), apply(SOLVED, [b, a]))
        self.assertNotEqual(apply(SOLVED, ["U", "R"]), apply(SOLVED, ["R", "U"]))


class TestInvariants(unittest.TestCase):
    def test_random_sequences(self):
        rnd = random.Random(2)
        for _ in range(300):
            c = apply(SOLVED, [rnd.choice(HTM) for _ in range(rnd.randint(0, 40))])
            self.assertEqual(invariants(c), (0, 0, 0))

    def test_single_twist_is_unreachable(self):
        cp, co, ep, eo = SOLVED
        self.assertNotEqual(invariants((cp, (1,) + co[1:], ep, eo)), (0, 0, 0))
        self.assertNotEqual(invariants((cp, co, ep, (1,) + eo[1:])), (0, 0, 0))
        self.assertNotEqual(invariants(((1, 0) + cp[2:], co, ep, eo)), (0, 0, 0))

    def test_counts(self):
        self.assertEqual(state_count(), 43252003274489856000)
        self.assertEqual(assemblies(), 12 * state_count())

    def test_superflip_is_central(self):
        sf = superflip()
        self.assertEqual(invariants(sf), (0, 0, 0))
        for m in HTM:
            self.assertEqual(multiply(sf, MOVES[m]), multiply(MOVES[m], sf))


class TestSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.half = ball(SOLVED, 4, HTM)

    def test_layers(self):
        self.assertEqual(layer_counts(4, HTM), [1, 18, 243, 3240, 43239])
        self.assertEqual(layer_counts(4, QTM), [1, 12, 114, 1068, 10011])

    def test_meet_in_the_middle(self):
        rnd = random.Random(3)
        for length in range(0, 9):
            for _ in range(2):
                seq = [rnd.choice(HTM) for _ in range(length)]
                c = apply(SOLVED, seq)
                d = distance_meet_in_middle(c, self.half, 4, HTM)
                self.assertGreaterEqual(d, 0)
                self.assertLessEqual(d, length)
                if c in self.half:
                    self.assertEqual(d, self.half[c])
                else:
                    self.assertGreater(d, 4)
        self.assertEqual(distance_meet_in_middle(apply(SOLVED, "R U F".split()), self.half, 4, HTM), 3)
        self.assertEqual(distance_meet_in_middle(superflip(), self.half, 4, HTM), -1)


if __name__ == "__main__":
    unittest.main()
