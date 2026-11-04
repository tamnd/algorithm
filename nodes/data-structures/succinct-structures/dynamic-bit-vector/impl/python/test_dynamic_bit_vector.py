# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-bit-vector/. The authors are listed in prov/ZZJ07J.jsonl.
"""Tests for the dynamic bit vector."""

from __future__ import annotations

import random
import unittest

from dynamic_bit_vector import DynamicBitVector


def check(t: unittest.TestCase, d: DynamicBitVector, ref: list[int]) -> None:
    t.assertEqual(d.to_list(), ref)
    t.assertEqual(len(d), len(ref))
    ones = [i for i, b in enumerate(ref) if b]
    zeros = [i for i, b in enumerate(ref) if not b]
    for i in range(len(ref) + 1):
        t.assertEqual(d.rank1(i), sum(ref[:i]))
    for j, p in enumerate(ones, 1):
        t.assertEqual(d.select1(j), p)
    for j, p in enumerate(zeros, 1):
        t.assertEqual(d.select0(j), p)


class TestDynamicBitVector(unittest.TestCase):
    def test_example(self) -> None:
        d = DynamicBitVector([0, 1, 1, 0, 1, 0, 0, 1], block=2)
        self.assertEqual(d.rank1(5), 3)
        self.assertEqual(d.select1(3), 4)
        d.insert(2, 1)
        self.assertEqual(d.to_list(), [0, 1, 1, 1, 0, 1, 0, 0, 1])
        self.assertEqual(d.rank1(5), 3)
        self.assertEqual(d.select1(4), 5)
        self.assertEqual(d.delete(0), 0)
        self.assertEqual(d.to_list(), [1, 1, 1, 0, 1, 0, 0, 1])
        self.assertEqual(d.select1(4), 4)
        self.assertEqual(d.select0(1), 3)

    def test_empty_and_errors(self) -> None:
        d = DynamicBitVector()
        self.assertEqual(len(d), 0)
        self.assertEqual(d.rank1(0), 0)
        with self.assertRaises(IndexError):
            d.select1(1)
        with self.assertRaises(IndexError):
            d.delete(0)
        d.insert(0, 1)
        self.assertEqual(d.select1(1), 0)
        self.assertEqual(d.delete(0), 1)
        self.assertEqual(len(d), 0)
        d.insert(0, 0)
        self.assertEqual(d.to_list(), [0])

    def test_random_ops(self) -> None:
        rng = random.Random(707)
        for trial in range(6):
            block = rng.choice([1, 2, 3, 4, 8])
            ref = [rng.randint(0, 1) for _ in range(rng.randint(0, 20))]
            d = DynamicBitVector(ref, block=block, seed=trial)
            for _ in range(100):
                op = rng.random()
                if op < 0.45 or not ref:
                    i, b = rng.randint(0, len(ref)), rng.randint(0, 1)
                    d.insert(i, b)
                    ref.insert(i, b)
                elif op < 0.8:
                    i = rng.randrange(len(ref))
                    self.assertEqual(d.delete(i), ref.pop(i))
                else:
                    i, b = rng.randrange(len(ref)), rng.randint(0, 1)
                    d.set(i, b)
                    ref[i] = b
                self.assertEqual(len(d), len(ref))
                if ref:
                    i = rng.randrange(len(ref))
                    self.assertEqual(d.access(i), ref[i])
                    self.assertEqual(d.rank1(i), sum(ref[:i]))
            check(self, d, ref)


if __name__ == "__main__":
    unittest.main()
