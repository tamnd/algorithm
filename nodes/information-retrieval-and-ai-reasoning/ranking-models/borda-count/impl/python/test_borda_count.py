# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/borda-count/. The authors are listed in prov/2CGC7D.jsonl.

import itertools
import random
from fractions import Fraction

from borda_count import borda, borda_scores


def random_profile(rng, n, k, partial):
    items = list(range(1, n + 1))
    out = []
    for _ in range(k):
        r = items[:]
        rng.shuffle(r)
        if partial:
            r = r[: rng.randint(0, n)]
        out.append(r)
    return out


def kendall(sigma, tau):
    ps = {x: i for i, x in enumerate(sigma)}
    pt = {x: i for i, x in enumerate(tau)}
    return sum(1 for x, y in itertools.combinations(sigma, 2) if (ps[x] - ps[y]) * (pt[x] - pt[y]) < 0)


def test_points_by_the_formula():
    rng = random.Random(1)
    for _ in range(300):
        prof = random_profile(rng, rng.randint(1, 7), rng.randint(1, 5), partial=True)
        union = sorted({x for r in prof for x in r})
        n = len(union)
        s = borda_scores(prof)
        assert sorted(s) == union
        for x in union:
            want = Fraction(0)
            for r in prof:
                if x in r:
                    want += n - (r.index(x) + 1) + 1
                else:
                    want += Fraction(sum(n - i + 1 for i in range(len(r) + 1, n + 1)), n - len(r))
            assert s[x] == want
        # Each list hands out 1 + 2 + ... + n points.
        assert sum(s.values()) == len(prof) * n * (n + 1) // 2


def test_score_is_one_plus_pairwise_wins_plus_half_ties():
    rng = random.Random(2)
    for _ in range(300):
        prof = random_profile(rng, rng.randint(1, 7), rng.randint(1, 5), partial=True)
        union = sorted({x for r in prof for x in r})
        s = borda_scores(prof)
        for x in union:
            want = Fraction(0)
            for r in prof:
                pos = {y: i for i, y in enumerate(r)}
                big = len(union)
                want += 1
                for y in union:
                    if y == x:
                        continue
                    px, py = pos.get(x, big), pos.get(y, big)
                    if px < py:
                        want += 1
                    elif px == py:
                        want += Fraction(1, 2)
            assert s[x] == want


def test_borda_order_minimizes_squared_rank_distance():
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(1, 6)
        prof = random_profile(rng, n, rng.randint(1, 5), partial=False)
        items = list(range(1, n + 1))

        def cost(sigma):
            p = {x: i for i, x in enumerate(sigma)}
            return sum((p[x] - r.index(x)) ** 2 for r in prof for x in items)

        best = min(cost(p) for p in itertools.permutations(items))
        assert cost(borda(prof)) == best


def test_borda_is_a_five_approximation_of_kemeny():
    rng = random.Random(4)
    worst = Fraction(1)
    for _ in range(80):
        n = rng.randint(2, 6)
        prof = random_profile(rng, n, rng.randint(1, 6), partial=False)
        perms = list(itertools.permutations(range(1, n + 1)))
        opt = min(sum(kendall(p, r) for r in prof) for p in perms)
        got = sum(kendall(borda(prof), r) for r in prof)
        if opt == 0:
            assert got == 0
        else:
            worst = max(worst, Fraction(got, opt))
            assert got <= 5 * opt
    assert worst < 2


def test_condorcet_failure():
    prof = [list("abc")] * 3 + [list("bca")] * 2
    s = borda_scores(prof)
    assert s == {"a": 11, "b": 12, "c": 7}
    assert borda(prof) == list("bac")
    # a beats b and c in a strict majority of the lists, yet b wins the Borda count.
    assert sum(r.index("a") < r.index("b") for r in prof) == 3
    assert sum(r.index("a") < r.index("c") for r in prof) == 3


def test_toy_runs():
    bm25 = [1, 2, 8, 7, 4]
    run = [1, 6, 8, 2, 4]
    s = borda_scores([bm25, run])
    assert s == {1: 12, 2: 8, 8: 8, 6: 6, 7: 4, 4: 4}
    assert borda([bm25, run]) == [1, 2, 8, 6, 4, 7]


def test_empty_and_single():
    assert borda([]) == []
    assert borda([[3, 1, 2]]) == [3, 1, 2]
    assert borda([[], [5]]) == [5]
