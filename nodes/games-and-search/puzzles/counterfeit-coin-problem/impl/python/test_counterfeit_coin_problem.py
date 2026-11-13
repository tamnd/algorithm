# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counterfeit-coin-problem/. The authors are listed in prov/ASZJ2T.jsonl.

from counterfeit_coin_problem import (dyson_labels, nonadaptive_decode, nonadaptive_plan, solvable,
                                      solvable_counts, twelve_adaptive, weigh)

CASES = [(coin, heavy) for coin in range(12) for heavy in (True, False)]


def test_adaptive_twelve_all_24_cases() -> None:
    for fake, heavy in CASES:
        calls = []

        def scale(left, right):
            calls.append((left, right))
            return weigh(left, right, fake, heavy)

        assert twelve_adaptive(scale) == (fake, heavy)
        assert len(calls) == 3


def test_nonadaptive_twelve_all_24_cases() -> None:
    labels = dyson_labels(12, 3)
    plan = nonadaptive_plan(labels)
    assert all(len(left) == len(right) == 4 for left, right in plan)
    outcomes = set()
    for fake, heavy in CASES:
        results = [weigh(left, right, fake, heavy) for left, right in plan]
        outcomes.add(tuple(results))
        assert nonadaptive_decode(labels, results) == (fake, heavy)
    assert len(outcomes) == 24


def test_bound_by_exhaustive_search() -> None:
    for w in range(1, 5):
        top = (3 ** w - 3) // 2
        assert solvable_counts(w) == list(range(3, top + 1)), w
        assert solvable_counts(w, extra_genuine=1) == list(range(1, (3 ** w - 1) // 2 + 1)), w
    assert solvable(12, 3) and not solvable(13, 3) and solvable(13, 3, extra_genuine=1)


def test_known_heavy() -> None:
    for w in range(0, 5):
        assert solvable(3 ** w, w, heavy_only=True)
        assert not solvable(3 ** w + 1, w, heavy_only=True)


def test_small_cases_fail() -> None:
    # one or two coins with no reference coin: the type can never be found
    for w in range(1, 5):
        assert not solvable(1, w) and not solvable(2, w)
