# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/auction-algorithm/. The authors are listed in prov/YB4A74.jsonl.

import itertools
import random
import unittest
from fractions import Fraction
from typing import Optional

from auction_algorithm import auction


def brute(benefit: list[list[Optional[int]]]) -> Optional[int]:
    """Largest total benefit over all feasible permutations, None if there is none."""
    n = len(benefit)
    best: Optional[int] = None
    for perm in itertools.permutations(range(n)):
        if any(benefit[i][perm[i]] is None for i in range(n)):
            continue
        total = sum(benefit[i][perm[i]] for i in range(n))  # type: ignore[misc]
        if best is None or total > best:
            best = total
    return best


def check(test: unittest.TestCase, benefit: list[list[Optional[int]]]) -> None:
    n = len(benefit)
    result = auction(benefit)
    want = brute(benefit)
    test.assertEqual(result.value, want)
    if want is None:
        test.assertIsNone(result.assignment)
        return
    a = result.assignment
    assert a is not None
    test.assertEqual(sorted(a), list(range(n)))
    test.assertEqual(sum(benefit[i][a[i]] for i in range(n)), want)  # type: ignore[misc]
    # 1-complementary slackness in scaled units: each person is within 1 of its best.
    for i in range(n):
        scaled = [
            None if x is None else (n + 1) * x for x in benefit[i]
        ]
        got = scaled[a[i]] - result.prices[a[i]]  # type: ignore[operator]
        for j in range(n):
            if scaled[j] is not None:
                test.assertGreaterEqual(got, scaled[j] - result.prices[j] - 1)


class TestAuction(unittest.TestCase):
    def test_worked_example(self) -> None:
        trace: list[tuple[int, int, int, Optional[int]]] = []
        r = auction([[10, 5, 8], [9, 2, 3], [7, 6, 4]], lambda *b: trace.append(b))
        self.assertEqual(r.assignment, [2, 0, 1])
        self.assertEqual(r.value, 23)
        self.assertEqual(r.prices, [25, 9, 18])
        self.assertEqual(trace, [(0, 0, 9, None), (1, 0, 25, 0), (2, 1, 9, None), (0, 2, 18, None)])
        # Dual value sum of prices plus profits, in original units, is within 1 of the primal.
        n = 3
        p = [Fraction(x, n + 1) for x in r.prices]
        b = [[10, 5, 8], [9, 2, 3], [7, 6, 4]]
        dual = sum(p) + sum(max(b[i][j] - p[j] for j in range(n)) for i in range(n))
        self.assertEqual(dual, Fraction(93, 4))

    def test_empty(self) -> None:
        r = auction([])
        self.assertEqual((r.assignment, r.value, r.bids), ([], 0, 0))

    def test_single(self) -> None:
        self.assertEqual(auction([[-7]]).assignment, [0])
        self.assertEqual(auction([[-7]]).value, -7)

    def test_no_perfect_matching(self) -> None:
        # Both persons may take only object 0: Hall's condition fails.
        r = auction([[5, None], [7, None]])
        self.assertIsNone(r.assignment)
        self.assertIsNone(r.value)
        self.assertIsNone(auction([[None]]).assignment)

    def test_forbidden_but_feasible(self) -> None:
        r = auction([[100, None, None], [1, 1, None], [1, 1, 1]])
        self.assertEqual(r.assignment, [0, 1, 2])
        self.assertEqual(r.value, 102)

    def test_ties_and_negative(self) -> None:
        check(self, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        check(self, [[-5, -1], [-2, -9]])

    def test_minimum_cost_by_negation(self) -> None:
        cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
        r = auction([[-c for c in row] for row in cost])
        self.assertEqual(r.value, -13)
        self.assertEqual(r.assignment, [1, 0, 2, 3])

    def test_not_square(self) -> None:
        with self.assertRaises(ValueError):
            auction([[1, 2]])

    def test_random(self) -> None:
        rng = random.Random(1988)
        for _ in range(700):
            n = rng.randint(0, 6)
            hi = rng.choice([1, 3, 10, 1000])
            density = rng.choice([0.0, 0.0, 0.2, 0.5])
            benefit = [
                [None if rng.random() < density else rng.randint(-hi, hi) for _ in range(n)]
                for _ in range(n)
            ]
            check(self, benefit)


if __name__ == "__main__":
    unittest.main()
