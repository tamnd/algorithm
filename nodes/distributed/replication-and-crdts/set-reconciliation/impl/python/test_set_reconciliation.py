# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-reconciliation/. The authors are listed in prov/ACGS5S.jsonl.

import random
from math import log2

from set_reconciliation import (IBLT, P, cpi_reconcile, cpi_sketch, iblt_reconcile, lower_bound_bits,
                                pmul, random_pair, roots)


def test_roots_of_a_product_of_linear_factors() -> None:
    rng = random.Random(0)
    for _ in range(20):
        xs = rng.sample(range(1, 1 << 40), rng.randint(0, 12))
        f = [1]
        for x in xs:
            f = pmul(f, [(-x) % P, 1])
        assert roots(f, rng) == sorted(xs)
    assert roots([1, 0, 1], rng) is None  # z^2 + 1 has no roots, as P = 3 mod 4


def test_cpi_page_example() -> None:
    a, b = {1, 2, 9, 12, 33}, {1, 2, 9, 10, 12, 28}
    assert cpi_reconcile(cpi_sketch(a, 3), b) == ({33}, {10, 28})


def test_cpi_recovers_the_exact_difference_when_m_is_at_least_d() -> None:
    rng = random.Random(1)
    for trial in range(120):
        d = rng.randint(0, 14)
        a, b = random_pair(rng, rng.randint(d, 80), d)
        m = d + rng.randint(0, 4)
        assert cpi_reconcile(cpi_sketch(a, m), b, seed=trial) == (a - b, b - a), trial


def test_cpi_reports_failure_when_m_is_too_small() -> None:
    rng = random.Random(2)
    for trial in range(60):
        d = rng.randint(2, 12)
        a, b = random_pair(rng, 60, d)
        assert cpi_reconcile(cpi_sketch(a, d - 2), b) is None, trial


def test_cpi_message_size_is_within_a_small_factor_of_the_lower_bound() -> None:
    u, d = 1 << 32, 10
    bound = lower_bound_bits(u, d)
    assert bound >= d * log2(u / d)
    sent_bits = (d + 2) * 61 + 32  # d + 2 field elements and |A|
    assert bound < sent_bits < 3 * bound


def test_iblt_recovers_the_exact_difference_with_room() -> None:
    rng = random.Random(3)
    fails = 0
    for _ in range(60):
        d = rng.randint(0, 120)
        a, b = random_pair(rng, d + 100, d)
        r = iblt_reconcile(a, b, cells=2 * d + 6)
        if r is None:
            fails += 1
        else:
            assert r == (a - b, b - a)
    assert fails <= 3


def test_iblt_failure_rate_depends_on_the_table_size() -> None:
    rng = random.Random(4)
    d, trials = 200, 100

    def failure_rate(ratio: float) -> float:
        bad = 0
        for _ in range(trials):
            a, b = random_pair(rng, d + 50, d)
            r = iblt_reconcile(a, b, cells=int(ratio * d))
            if r is None:
                bad += 1
            else:
                assert r == (a - b, b - a)  # a listing that finishes is exact
        return bad / trials

    assert failure_rate(1.0) == 1.0  # below the k = 3 threshold of about 1.222 d cells
    assert failure_rate(1.6) <= 0.06
    assert failure_rate(2.0) <= 0.03


def test_iblt_of_equal_sets_is_empty() -> None:
    s = set(range(1, 300))
    t = IBLT.of(s, 30).subtract(IBLT.of(s, 30))
    assert not any(t.count) and t.peel() == (set(), set())
