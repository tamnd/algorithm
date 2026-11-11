# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signed-messages-algorithm/. The authors are listed in prov/XR29FE.jsonl.

from itertools import combinations

import pytest

from signed_messages_algorithm import (
    RETREAT,
    STRATEGIES,
    VALUES,
    Adversary,
    Signatures,
    agreement_and_validity,
    choice,
    late,
    sm,
)


def traitor_sets(n: int, k: int):
    for size in range(1, k + 1):
        yield from (frozenset(c) for c in combinations(range(n), size))


def test_choice() -> None:
    assert choice({2}) == 2
    assert choice(set()) == RETREAT
    assert choice({1, 2}) == RETREAT


def test_no_forgery() -> None:
    sigs = Signatures()
    adv = Adversary(4, frozenset({3}), sigs, None)
    with pytest.raises(PermissionError):
        adv.sign_as(1, (1, ()))
    sigs.sign(0, (1, ()))
    assert sigs.valid(1, (0,))
    assert not sigs.valid(2, (0,))
    assert not sigs.valid(1, (0, 2))


def test_failure_free_counts() -> None:
    for n, m in [(3, 1), (4, 2), (5, 3), (6, 2)]:
        res = sm(n, m, 1)
        assert set(res["decisions"].values()) == {1}
        assert res["rounds"] == m + 1
        assert res["loyal_messages"] == (n - 1) ** 2
        assert res["loyal_signatures"] == (n - 1) + 2 * (n - 1) * (n - 2)


def test_page_example() -> None:
    # n = 4, m = 2, the commander and lieutenant 3 are traitors.
    res = sm(4, 2, None, frozenset({0, 3}), late, seed=0)
    assert res["sets"] == {1: frozenset({1, 2}), 2: frozenset({1, 2})}
    assert res["decisions"] == {1: RETREAT, 2: RETREAT}


def test_agreement_and_validity_up_to_n_minus_2() -> None:
    for n in (3, 4, 5):
        m = n - 2
        for traitors in traitor_sets(n, m):
            for name, strategy in STRATEGIES.items():
                for value in VALUES:
                    for seed in range(4 if name in ("random", "forge") else 1):
                        res = sm(n, m, value, traitors, strategy, seed)
                        assert agreement_and_validity(res, value, 0 not in traitors), (n, traitors, name)
                        assert res["rounds"] == m + 1
                        d = len({v for s in res["sets"].values() for v in s})
                        assert res["loyal_messages"] <= (n - 1) * (1 + (n - 2) * max(d, 1))


def test_larger_seeded() -> None:
    n, m = 7, 4
    for seed in range(6):
        for traitors in [frozenset({0, 2, 4, 6}), frozenset({1, 5}), frozenset({0, 1, 2, 3})]:
            for name in ("random", "forge", "equivocate", "late"):
                res = sm(n, m, 2, traitors, STRATEGIES[name], seed)
                assert agreement_and_validity(res, 2, 0 not in traitors)


def test_forgeries_are_rejected() -> None:
    res = sm(5, 3, 1, frozenset({4}), STRATEGIES["forge"], seed=1)
    assert res["rejected"] > 0
    assert set(res["decisions"].values()) == {1}


def test_one_round_short_breaks_agreement() -> None:
    # with m traitors (the commander among them), m rounds are not enough
    for n, m in [(4, 2), (5, 3), (6, 2)]:
        traitors = frozenset(range(0, n)[:1]) | frozenset(range(n - m + 1, n))
        assert len(traitors) == m
        good = sm(n, m, None, traitors, late)
        assert len(set(good["decisions"].values())) == 1
        bad = sm(n, m, None, traitors, late, rounds=m)
        assert len(set(bad["decisions"].values())) == 2
