# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-max-coverage/. The authors are listed in prov/CJWJGV.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from greedy_max_coverage import greedy_max_coverage


def brute_opt(sets, k):
    k = min(k, len(sets))
    return max(len(set().union(*[sets[i] for i in c])) for c in combinations(range(len(sets)), k))


def bound(k):
    return 1 - (1 - Fraction(1, k)) ** k


def test_example_page():
    sets = [{1, 2, 3, 4}, {5, 6, 7, 8}, {2, 3, 6, 7, 9}, {10, 11, 12}]
    chosen, covered = greedy_max_coverage(sets, 3)
    assert chosen == [2, 3, 0]
    assert len(covered) == 10
    assert brute_opt(sets, 3) == 11
    chosen2, covered2 = greedy_max_coverage(sets, 2)
    assert chosen2 == [2, 3] and len(covered2) == 8 == brute_opt(sets, 2)


def test_random_against_brute_force():
    rng = random.Random(1978)
    for trial in range(300):
        n, m, k = rng.randint(1, 12), rng.randint(1, 7), rng.randint(1, 4)
        sets = [set(e for e in range(n) if rng.random() < 0.35) for _ in range(m)]
        chosen, covered = greedy_max_coverage(sets, k)
        assert len(chosen) <= k and len(set(chosen)) == len(chosen)
        assert covered == set().union(set(), *[sets[j] for j in chosen])
        opt = brute_opt(sets, k)
        assert len(covered) >= bound(k) * opt
        # the step inequality of the proof: OPT - f(G_i+1) <= (1 - 1/k)(OPT - f(G_i))
        prev = 0
        cov = set()
        for j in chosen:
            cov |= sets[j]
            assert opt - len(cov) <= (1 - Fraction(1, k)) * (opt - prev)
            prev = len(cov)


def test_bound_below_one_minus_one_over_e():
    # 1 - (1 - 1/k)^k decreases toward 1 - 1/e = 0.632...
    vals = [bound(k) for k in range(1, 30)]
    assert all(a > b for a, b in zip(vals, vals[1:]))
    assert vals[-1] > Fraction(632, 1000)


def test_tight_family():
    for k in range(1, 5):
        size = k**k
        rows = [{(r, c) for c in range(size)} for r in range(k)]
        greedy_sets, start = [], 0
        for i in range(1, k + 1):
            a = k ** (k - i) * (k - 1) ** (i - 1)
            greedy_sets.append({(r, c) for r in range(k) for c in range(start, start + a)})
            start += a
        sets = greedy_sets + rows
        chosen, covered = greedy_max_coverage(sets, k)
        assert chosen == list(range(k))
        opt = k * size
        assert brute_opt(sets, k) == opt
        assert Fraction(len(covered), opt) == bound(k)


def test_k_zero_and_empty():
    assert greedy_max_coverage([{1}], 0) == ([], set())
    assert greedy_max_coverage([set(), set()], 2) == ([], set())
