# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-over-e-stopping-rule/. The authors are listed in prov/19FPEC.jsonl.

import itertools
import math
import random
from fractions import Fraction

from one_over_e_stopping_rule import cutoff, one_over_e_stopping_rule, optimal_cutoff, success_probability


def test_example() -> None:
    c = [6, 3, 8, 5, 9, 2, 10, 1, 7, 4]
    assert cutoff(10) == 3
    assert one_over_e_stopping_rule(c) == 4
    assert one_over_e_stopping_rule(c, 1) == 2
    assert one_over_e_stopping_rule(c, 5) == 6


def test_edges() -> None:
    assert one_over_e_stopping_rule([]) is None
    assert one_over_e_stopping_rule([5]) == 0
    assert one_over_e_stopping_rule([1, 2]) == 0
    assert one_over_e_stopping_rule([9, 1, 2, 3]) is None
    assert one_over_e_stopping_rule([2, 2, 2, 2]) is None
    assert one_over_e_stopping_rule([3, 1, 2], 3) is None
    assert [cutoff(n) for n in range(1, 12)] == [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4]


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(0, 12)
        a = [rng.randrange(8) for _ in range(n)]
        r = rng.randrange(0, n + 1)
        prefix = max(a[:r]) if r else None
        want = None
        for i in range(r, n):
            if prefix is None or a[i] > prefix:
                want = i
                break
            # prefix stays the max of a[:r]: a later item is hired as soon as it beats it
        assert one_over_e_stopping_rule(a, r) == want


def brute_success(n: int, r: int) -> Fraction:
    wins = 0
    perms = list(itertools.permutations(range(n)))
    for p in perms:
        pick = one_over_e_stopping_rule(list(p), r)
        if pick is not None and p[pick] == n - 1:
            wins += 1
    return Fraction(wins, len(perms))


def test_success_probability_exact() -> None:
    for n in range(1, 8):
        for r in range(n):
            assert success_probability(n, r) == brute_success(n, r)


def test_known_values() -> None:
    assert [optimal_cutoff(n)[1] for n in range(1, 9)] == [
        Fraction(1), Fraction(1, 2), Fraction(1, 2), Fraction(11, 24),
        Fraction(13, 30), Fraction(77, 180), Fraction(29, 70), Fraction(459, 1120)]
    assert optimal_cutoff(10) == (3, Fraction(3349, 8400))


def test_optimal_cutoff_is_the_best_cutoff() -> None:
    for n in range(1, 60):
        vals = [success_probability(n, r) for r in range(n)]
        r, p = optimal_cutoff(n)
        assert p == max(vals)
        assert r == vals.index(p)
        assert r in (cutoff(n), cutoff(n) + 1) or n <= 2


def best_over_all_rules(n: int) -> Fraction:
    """Optimal success probability over every rule that sees the relative order.

    Backward induction over the patterns (relative orders) of each prefix, by
    brute force over all permutations. It does not assume that a cutoff rule
    is optimal.
    """
    perms = list(itertools.permutations(range(n)))

    def pattern(p: tuple[int, ...], i: int) -> tuple[int, ...]:
        head = p[:i]
        s = sorted(head)
        return tuple(s.index(x) for x in head)

    value: dict[tuple[int, ...], Fraction] = {}
    for i in range(n, 0, -1):
        groups: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
        for p in perms:
            groups.setdefault(pattern(p, i), []).append(p)
        for pat, ps in groups.items():
            stop = Fraction(sum(1 for p in ps if p[i - 1] == n - 1), len(ps))
            if i == n:
                go = Fraction(0)
            else:
                nxt: dict[tuple[int, ...], int] = {}
                for p in ps:
                    q = pattern(p, i + 1)
                    nxt[q] = nxt.get(q, 0) + 1
                go = sum((Fraction(c, len(ps)) * value[q] for q, c in nxt.items()), Fraction(0))
            value[pat] = max(stop, go)
    return value[(0,)]


def test_cutoff_rules_are_optimal() -> None:
    for n in range(1, 7):
        assert best_over_all_rules(n) == optimal_cutoff(n)[1]


def test_limit_and_bounds() -> None:
    for n in (3, 10, 37, 100, 300):
        r, p = optimal_cutoff(n)
        assert p > Fraction(1, 3)
        assert float(p) <= 1 / math.e + 1 / n + 1e-12
        assert float(p) > 1 / math.e
    assert abs(float(optimal_cutoff(1000)[1]) - 1 / math.e) < 5e-4


def test_monte_carlo_matches_exact() -> None:
    rng = random.Random(11)
    n, trials, wins = 20, 20000, 0
    for _ in range(trials):
        p = list(range(n))
        rng.shuffle(p)
        pick = one_over_e_stopping_rule(p)
        wins += pick is not None and p[pick] == n - 1
    exact = float(success_probability(n, cutoff(n)))
    assert abs(wins / trials - exact) < 0.015
