# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-median-voter-rule/. The authors are listed in prov/N9KT39.jsonl.

import itertools
import random

import pytest

from agtprefs import (
    all_rankings,
    check_anonymity,
    check_pareto,
    condorcet_winner,
    find_manipulation,
    is_single_peaked_on,
    margins,
    weak_condorcet_winners,
)
from generalized_median_voter_rule import generalized_median, median_rule, plain_median_phantoms


def sp_rankings(m):
    axis = tuple(range(m))
    return [r for r in all_rankings(m) if is_single_peaked_on((r,), axis)]


def sp_profiles(m, n):
    return list(itertools.product(sp_rankings(m), repeat=n))


def test_agrees_with_sorting():
    rng = random.Random(1)
    for _ in range(500):
        m = rng.randint(1, 8)
        n = rng.randint(0, 7)
        peaks = [rng.randrange(m) for _ in range(n)]
        k = n + 1 if n == 0 or rng.random() < 0.5 else n - 1
        phantoms = [rng.randrange(m) for _ in range(k)]
        values = sorted(peaks + phantoms)
        assert generalized_median(peaks, phantoms, m) == values[len(values) // 2]


def test_even_total_is_rejected():
    with pytest.raises(ValueError):
        generalized_median([0, 1], [0, 1], 3)


def test_strategyproof_for_every_phantom_choice():
    m, n = 4, 2
    P = sp_profiles(m, n)
    for phantoms in itertools.combinations_with_replacement(range(m), n + 1):
        assert find_manipulation(median_rule(phantoms), m, n, profiles=P) is None


def test_strategyproof_with_three_voters():
    m, n = 4, 3
    P = sp_profiles(m, n)
    rng = random.Random(2)
    for _ in range(2):
        phantoms = sorted(rng.randrange(m) for _ in range(n + 1))
        assert find_manipulation(median_rule(phantoms), m, n, profiles=P) is None


def test_anonymous():
    m, n = 4, 3
    P = sp_profiles(m, n)
    assert check_anonymity(median_rule([0, 1, 1, 3]), m, n, profiles=P) is None


def test_pareto_with_n_minus_one_phantoms_and_not_in_general():
    m, n = 4, 3
    P = sp_profiles(m, n)
    for phantoms in itertools.combinations_with_replacement(range(m), n - 1):
        assert check_pareto(median_rule(phantoms), m, n, profiles=P) is None
    # n + 1 phantoms that leave out the end 0: all voters at 0 still get 1
    rule = median_rule([1, 1, 2, 3])
    assert rule(((0, 1, 2, 3),) * 3, m) == 1
    assert check_pareto(rule, m, n, profiles=P) is not None


def peak_rule_from_table(table):
    return lambda profile, m: table[tuple(sorted(r[0] for r in profile))]


def test_characterization_three_candidates_two_voters():
    """Every anonymous peak-only rule that is strategyproof on the single-peaked domain is a
    median with n + 1 phantoms, and with Pareto it is a median with n - 1 phantoms."""
    m, n = 3, 2
    P = sp_profiles(m, n)
    keys = list(itertools.combinations_with_replacement(range(m), n))
    sp_rules, sp_pareto_rules = set(), set()
    for values in itertools.product(range(m), repeat=len(keys)):
        table = dict(zip(keys, values))
        rule = peak_rule_from_table(table)
        if find_manipulation(rule, m, n, profiles=P) is None:
            sp_rules.add(values)
            if check_pareto(rule, m, n, profiles=P) is None:
                sp_pareto_rules.add(values)

    def medians(k):
        return {tuple(generalized_median(key, ph, m) for key in keys)
                for ph in itertools.combinations_with_replacement(range(m), k)}

    assert sp_rules == medians(n + 1)
    assert sp_pareto_rules == medians(n - 1)
    assert len(sp_rules) == 10 and len(sp_pareto_rules) == 3


def test_plain_median_is_the_condorcet_winner():
    for m in range(2, 5):
        for n in (1, 3):
            rule = median_rule(plain_median_phantoms(n, m))
            for prof in sp_profiles(m, n):
                assert rule(prof, m) == condorcet_winner(prof, m)


def test_median_voter_theorem_by_brute_force():
    for m in range(2, 6):
        R = sp_rankings(m)
        for n in range(1, 5 if m < 5 else 4):
            for prof in itertools.combinations_with_replacement(R, n):
                peaks = sorted(r[0] for r in prof)
                M = margins(prof, m)
                if n % 2 == 1:
                    order = sorted(range(m), key=lambda a: -sum(1 for b in range(m) if M[a][b] > 0))
                    assert all(M[order[i]][order[j]] > 0 for i in range(m) for j in range(i + 1, m))
                    assert is_single_peaked_on((tuple(order),), tuple(range(m)))
                else:
                    lo, hi = peaks[n // 2 - 1], peaks[n // 2]
                    assert weak_condorcet_winners(prof, m) == frozenset(range(lo, hi + 1))


def test_no_voters():
    assert generalized_median([], [2], 5) == 2
