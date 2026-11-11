# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dolev-strong-algorithm/. The authors are listed in prov/EHN65V.jsonl.

from itertools import combinations

import pytest

from dolev_strong_algorithm import (
    DEFAULT,
    STRATEGIES,
    VALUES,
    Adversary,
    Signatures,
    agreement_and_validity,
    dolev_strong,
    late,
    message_bound,
)


def faulty_sets(n: int, k: int):
    for size in range(1, k + 1):
        yield from (frozenset(c) for c in combinations(range(n), size))


def test_signatures_cannot_be_forged() -> None:
    adv = Adversary(4, frozenset({2}), Signatures(), None)
    with pytest.raises(PermissionError):
        adv.sign_as(0, (1, ()))


def test_failure_free() -> None:
    for n, t in [(3, 1), (4, 2), (5, 3), (7, 2)]:
        res = dolev_strong(n, t, 2)
        assert set(res["decisions"].values()) == {2}
        assert res["rounds"] == t + 1
        assert res["correct_messages"] == (n - 1) ** 2
        assert res["max_signatures"] == 2


def test_page_example() -> None:
    # n = 5, t = 3, faulty sender 0 and faulty 3, 4: the late attack.
    res = dolev_strong(5, 3, None, frozenset({0, 3, 4}), late, seed=0)
    assert res["extracted"] == {1: [1, 2], 2: [1, 2]}
    assert res["decisions"] == {1: DEFAULT, 2: DEFAULT}
    short = dolev_strong(5, 3, None, frozenset({0, 3, 4}), late, seed=0, rounds=3)
    assert short["extracted"] == {1: [1, 2], 2: [1]}
    assert short["decisions"] == {1: DEFAULT, 2: 1}


def test_agreement_validity_and_costs_up_to_n_minus_2() -> None:
    for n in (3, 4, 5, 6):
        t = n - 2
        for faulty in faulty_sets(n, t):
            for name, strategy in STRATEGIES.items():
                for value in VALUES:
                    for seed in range(3 if name in ("random", "forge") else 1):
                        res = dolev_strong(n, t, value, faulty, strategy, seed)
                        assert agreement_and_validity(res, value, 0 not in faulty), (n, faulty, name)
                        assert res["rounds"] == t + 1
                        assert res["correct_messages"] <= message_bound(n)
                        assert res["max_signatures"] <= t + 1
                        for ex in res["extracted"].values():
                            assert len(ex) <= len(VALUES)


def test_t_rounds_are_not_enough() -> None:
    for n, t in [(3, 1), (4, 2), (5, 3), (6, 2), (8, 5)]:
        faulty = frozenset([0] + list(range(n - t + 1, n)))
        assert len(faulty) == t
        full = dolev_strong(n, t, None, faulty, late)
        assert len(set(full["decisions"].values())) == 1
        short = dolev_strong(n, t, None, faulty, late, rounds=t)
        assert len(set(short["decisions"].values())) == 2


def test_larger_seeded() -> None:
    n, t = 9, 6
    for seed in range(5):
        for faulty in [frozenset({0, 1, 2, 3, 4, 5}), frozenset({2, 4, 6, 8}), frozenset({0, 8})]:
            for name in ("random", "forge", "equivocate", "late"):
                res = dolev_strong(n, t, 1, faulty, STRATEGIES[name], seed)
                assert agreement_and_validity(res, 1, 0 not in faulty)
                assert res["correct_messages"] <= message_bound(n)
