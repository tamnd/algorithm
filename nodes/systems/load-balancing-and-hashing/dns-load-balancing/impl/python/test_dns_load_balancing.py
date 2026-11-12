# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dns-load-balancing/. The authors are listed in prov/1TFQQ5.jsonl.

import itertools
import random
from collections import Counter
from fractions import Fraction

import pytest

from dns_load_balancing import (
    Authority,
    rotate,
    simulate,
    srv_first_probabilities,
    srv_order,
    srv_pick_index,
)


def test_rotation_of_the_page() -> None:
    auth = Authority(["A", "B", "C"], 300)
    got = [auth.answer()[0] for _ in range(4)]
    assert got == [["A", "B", "C"], ["B", "C", "A"], ["C", "A", "B"], ["A", "B", "C"]]
    # over any n consecutive answers each address is first exactly once
    auth = Authority(list("ABCDE"), 60)
    firsts = [auth.answer()[0][0] for _ in range(50)]
    for i in range(0, 50 - 5 + 1):
        assert sorted(firsts[i:i + 5]) == list("ABCDE")
    assert rotate([], 3) == []


def test_srv_pick_matches_running_sum_reference() -> None:
    rng = random.Random(3)
    for _ in range(300):
        cands = [(0, rng.choice([0, 0, 1, 2, 5, 10]), f"t{i}") for i in range(rng.randint(1, 5))]
        total = sum(w for _, w, _ in cands)
        for r in range(total + 1):
            sums = list(itertools.accumulate(w for _, w, _ in cands))
            want = next(i for i, s in enumerate(sums) if s >= r)
            assert srv_pick_index(cands, r) == want


def test_srv_first_probabilities_of_the_page() -> None:
    cands = [(10, 0, "z"), (10, 60, "a"), (10, 30, "b"), (10, 10, "c")]
    got = [Fraction(h, d) for h, d in srv_first_probabilities(cands)]
    assert got == [Fraction(1, 101), Fraction(60, 101), Fraction(30, 101), Fraction(10, 101)]
    # without a weight-0 record, the first record also takes r = 0
    got = [Fraction(h, d) for h, d in srv_first_probabilities(cands[1:])]
    assert got == [Fraction(61, 101), Fraction(30, 101), Fraction(10, 101)]


def test_srv_order_is_by_priority_and_a_permutation() -> None:
    rng = random.Random(11)
    for _ in range(300):
        recs = [(rng.randint(0, 2), rng.choice([0, 1, 3, 7]), f"t{i}") for i in range(rng.randint(0, 7))]
        out = srv_order(recs, rng)
        assert sorted(out) == sorted(recs)
        assert [p for p, _, _ in out] == sorted(p for p, _, _ in recs)
    with pytest.raises(ValueError):
        srv_order([(0, -1, "x")], rng)


def test_srv_first_choice_frequencies() -> None:
    rng = random.Random(7)
    recs = [(10, 60, "a"), (10, 30, "b"), (10, 10, "c"), (20, 0, "backup")]
    first = Counter(srv_order(recs, rng)[0][2] for _ in range(20000))
    assert first["backup"] == 0
    assert abs(first["a"] / 20000 - 61 / 101) < 0.015
    assert abs(first["b"] / 20000 - 30 / 101) < 0.015
    assert abs(first["c"] / 20000 - 10 / 101) < 0.015


def test_resolver_skew_of_the_page() -> None:
    c = simulate([900, 100], ["S1", "S2"], ttl=60, horizon=600)
    assert c == {"S1": 900 * 600, "S2": 100 * 600, "failed": 0}
    # the same clients spread over 10 resolvers of 100
    c = simulate([100] * 10, ["S1", "S2"], ttl=60, horizon=600)
    assert c["S1"] == c["S2"] == 500 * 600


def test_failure_lasts_one_ttl() -> None:
    # S1 dies at t = 30. The resolver whose cached answer starts with S1
    # keeps it until the cache expires at t = 60.
    c = simulate([100, 100], ["S1", "S2"], ttl=60, horizon=60, dead=["S1"], dead_from=30)
    assert c["failed"] == 100 * 30
