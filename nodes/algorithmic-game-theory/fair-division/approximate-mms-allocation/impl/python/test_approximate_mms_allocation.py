# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-mms-allocation/. The authors are listed in prov/1VB5JR.jsonl.

import random
from fractions import Fraction

import pytest

from approximate_mms_allocation import approx_mms, mms_partition

F = Fraction


def mms_brute(row, n):
    """MMS by brute force over partitions: max over a first bundle S of min(v(S), MMS of the rest with n - 1)."""
    m = len(row)
    val = [0] * (1 << m)
    for s in range(1, 1 << m):
        low = s & -s
        val[s] = val[s ^ low] + row[low.bit_length() - 1]
    memo = {}

    def best(s, k):
        if k == 1:
            return val[s]
        if (s, k) not in memo:
            r = -1
            sub = s
            while True:
                r = max(r, min(val[sub], best(s ^ sub, k - 1)))
                if sub == 0:
                    break
                sub = (sub - 1) & s
            memo[(s, k)] = r
        return memo[(s, k)]

    return best((1 << m) - 1, n)


def check(values, bundles, exact=True):
    n, m = len(values), len(values[0])
    assert sorted(g for b in bundles for g in b) == list(range(m))
    for i in range(n):
        target = mms_brute(values[i], n) if exact else mms_partition([F(x) for x in values[i]], range(m), n)[0]
        assert 4 * sum(values[i][g] for g in bundles[i]) >= 3 * target


def test_worked_example():
    values = [[1] * 10, [3, 3, 2, 2, 2, 2, 1, 1, 1, 1]]
    assert mms_brute(values[0], 2) == 5
    assert mms_brute(values[1], 2) == 9
    stats = {}
    bundles = approx_mms(values, stats)
    assert stats["rules"] == []
    assert stats["bagfill"] == [0, 1]
    assert bundles == [[1, 2, 5, 6, 7, 8, 9], [0, 3, 4]]
    assert [sum(values[i][g] for g in bundles[i]) for i in range(2)] == [7, 7]
    check(values, bundles)


def test_mms_partition_against_brute_force():
    rng = random.Random(41)
    for _ in range(300):
        n, m = rng.randint(1, 4), rng.randint(0, 8)
        row = [rng.randint(0, 12) for _ in range(m)]
        value, part = mms_partition([F(x) for x in row], range(m), n)
        assert value == mms_brute(row, n)
        assert len(part) == n
        assert sorted(g for b in part for g in b) == list(range(m))
        assert min(sum(row[g] for g in b) for b in part) == value


def test_random_instances():
    rng = random.Random(42)
    rules_seen = set()
    for _ in range(250):
        n, m = rng.randint(1, 4), rng.randint(0, 8)
        lo = rng.choice([0, 1, 5, 10])
        hi = lo + rng.choice([3, 10, 30])
        values = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]
        stats = {}
        bundles = approx_mms(values, stats)
        rules_seen.update(rule for _, rule in stats["rules"])
        check(values, bundles)
    assert {1, 2, 3} <= rules_seen


def test_rule_four():
    # Agent 0: MMS 17, so 3/4 MMS = 51/4. g1 = 9, g2 + g3 = 11 and g3 + g4 + g5 = 12 are below it,
    # and g1 + g5 = 13 is not, so only R4 applies.
    values = [[9, 7, 4, 4, 4, 4, 1, 1], [6, 3, 2, 2, 2, 2, 2, 1]]
    assert mms_brute(values[0], 2) == 17
    stats = {}
    bundles = approx_mms(values, stats)
    assert stats["rules"] == [(0, 4)]
    check(values, bundles)


def test_bag_filling_instances():
    rng = random.Random(43)
    reached = 0
    for _ in range(80):
        n = rng.choice([2, 3])
        m = rng.randint(2 * n + 1, 9)
        values = [[rng.randint(10, 14) for _ in range(m)] for _ in range(n)]
        stats = {}
        bundles = approx_mms(values, stats)
        reached += bool(stats["bagfill"])
        check(values, bundles)
    assert reached >= 10


def test_three_agents_in_bag_filling():
    values = [
        [7, 9, 6, 6, 6, 8, 6, 7, 6, 6, 9, 9, 6],
        [7, 6, 9, 6, 6, 7, 6, 9, 6, 7, 6, 7, 8],
        [9, 7, 6, 8, 7, 6, 7, 8, 6, 6, 6, 7, 9],
    ]
    stats = {}
    bundles = approx_mms(values, stats)
    assert stats["bagfill"] == [0, 1, 2]
    check(values, bundles, exact=False)


def test_rational_values_and_bad_input():
    values = [[F(1, 2), F(1, 3), F(1, 6), F(2, 3)], [F(1, 4), F(1, 4), F(1, 4), F(1, 4)]]
    check(values, approx_mms(values))
    with pytest.raises(ValueError):
        approx_mms([])
    with pytest.raises(ValueError):
        approx_mms([[1, -1]])
