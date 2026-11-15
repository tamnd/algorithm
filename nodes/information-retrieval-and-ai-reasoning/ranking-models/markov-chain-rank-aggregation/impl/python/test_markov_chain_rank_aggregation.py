# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-chain-rank-aggregation/. The authors are listed in prov/DF298Z.jsonl.

import itertools
import random
from fractions import Fraction

from markov_chain_rank_aggregation import (
    aggregate,
    local_kemenize,
    prefers,
    stationary,
    teleport,
    transition_matrix,
)

CHAINS = ("MC1", "MC2", "MC3", "MC4")


def exact_stationary(m):
    """Solve pi M = pi with sum(pi) = 1 by Gaussian elimination over Fractions. None if not unique."""
    n = len(m)
    # Equations: for each j, sum_i pi_i (M[i][j] - [i == j]) = 0; replace the last by sum pi = 1.
    a = [[m[i][j] - (1 if i == j else 0) for i in range(n)] + [Fraction(0)] for j in range(n)]
    a[n - 1] = [Fraction(1)] * n + [Fraction(1)]
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c] != 0), None)
        if p is None:
            return None
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def random_profile(rng, n, k, partial):
    items = list(range(1, n + 1))
    out = []
    for _ in range(k):
        r = items[:]
        rng.shuffle(r)
        if partial:
            r = r[: rng.randint(1, n)]
        out.append(r)
    return out


def kendall(sigma, tau):
    """Pairs ranked by both lists in opposite orders."""
    ps = {x: i for i, x in enumerate(sigma)}
    pt = {x: i for i, x in enumerate(tau)}
    common = [x for x in sigma if x in pt]
    return sum(1 for x, y in itertools.combinations(common, 2) if (ps[x] - ps[y]) * (pt[x] - pt[y]) < 0)


def footrule(sigma, tau):
    pt = {x: i for i, x in enumerate(tau)}
    return sum(abs(i - pt[x]) for i, x in enumerate(sigma))


def total(dist, sigma, profile):
    return sum(dist(sigma, t) for t in profile)


def test_rows_are_distributions():
    rng = random.Random(1)
    for _ in range(200):
        prof = random_profile(rng, rng.randint(1, 6), rng.randint(1, 4), partial=True)
        for c in CHAINS:
            _, m = transition_matrix(prof, c, exact=True)
            for row in m:
                assert sum(row) == 1 and min(row) >= 0


def test_power_iteration_matches_exact_solve():
    rng = random.Random(2)
    eps = Fraction(3, 20)
    for _ in range(120):
        prof = random_profile(rng, rng.randint(2, 5), rng.randint(1, 4), partial=rng.random() < 0.5)
        for c in CHAINS:
            _, mx = transition_matrix(prof, c, exact=True)
            _, mf = transition_matrix(prof, c)
            pi_exact = exact_stationary(teleport(mx, eps))
            pi_float = stationary(teleport(mf, 0.15))
            assert pi_exact is not None
            assert sum(pi_exact) == 1
            for a, b in zip(pi_exact, pi_float):
                assert abs(float(a) - b) < 1e-9


def test_mc4_condorcet_winner_takes_all_mass():
    rng = random.Random(3)
    seen = 0
    for _ in range(300):
        n = rng.randint(2, 5)
        prof = random_profile(rng, n, rng.choice([1, 3, 5]), partial=False)
        items = sorted(prof[0])
        winners = [w for w in items if all(prefers(prof, w, y) for y in items if y != w)]
        if not winners:
            continue
        seen += 1
        w = winners[0]
        its, m = transition_matrix(prof, "MC4", exact=True)
        i = its.index(w)
        assert m[i][i] == 1
        pi = exact_stationary(m)
        assert pi == [Fraction(1) if j == i else Fraction(0) for j in range(n)]
    assert seen > 100


def test_mc3_one_step_from_uniform_is_borda_order():
    rng = random.Random(4)
    for _ in range(200):
        n, k = rng.randint(2, 6), rng.randint(1, 5)
        prof = random_profile(rng, n, k, partial=False)
        items, m = transition_matrix(prof, "MC3", exact=True)
        step = [sum(Fraction(1, n) * m[i][j] for i in range(n)) for j in range(n)]
        for j, x in enumerate(items):
            rank_sum = sum(r.index(x) + 1 for r in prof)
            assert step[j] == Fraction(1, n) * (1 + Fraction(k * (n + 1) - 2 * rank_sum, k * n))


def kemeny_costs(prof, perms):
    """Total Kendall distance of each permutation to the full lists of prof."""
    pos = [{x: i for i, x in enumerate(r)} for r in prof]
    items = sorted(prof[0])
    w = {(x, y): sum(1 for t in pos if t[x] < t[y]) for x in items for y in items}
    n = len(items)
    return [sum(w[p[j], p[i]] for i in range(n) for j in range(i + 1, n)) for p in perms]


def footrule_costs(prof, perms):
    pos = [{x: i for i, x in enumerate(r)} for r in prof]
    return [sum(abs(i - t[x]) for t in pos for i, x in enumerate(p)) for p in perms]


def test_kemeny_costs_agree_with_kendall():
    rng = random.Random(8)
    for _ in range(20):
        prof = random_profile(rng, rng.randint(1, 5), rng.randint(1, 4), partial=False)
        perms = list(itertools.permutations(sorted(prof[0])))
        assert kemeny_costs(prof, perms) == [total(kendall, p, prof) for p in perms]
        assert footrule_costs(prof, perms) == [total(footrule, p, prof) for p in perms]


def test_condorcet_ranking_is_the_unique_kemeny_ranking():
    rng = random.Random(5)
    seen = 0
    for _ in range(150):
        n = rng.randint(2, 6)
        prof = random_profile(rng, n, rng.choice([1, 3, 5, 7]), partial=False)
        items = sorted(prof[0])
        beats = {(x, y): prefers(prof, x, y) for x in items for y in items}
        perms = list(itertools.permutations(items))
        cond = [p for p in perms if all(beats[p[i], p[j]] for i in range(n) for j in range(i + 1, n))]
        if not cond:
            continue
        seen += 1
        cost = kemeny_costs(prof, perms)
        best = min(cost)
        assert [p for p, c in zip(perms, cost) if c == best] == cond
    assert seen > 30


def test_footrule_optimum_is_a_two_approximation_of_kemeny():
    rng = random.Random(6)
    for _ in range(60):
        n = rng.randint(2, 6)
        prof = random_profile(rng, n, rng.randint(1, 5), partial=False)
        perms = list(itertools.permutations(sorted(prof[0])))
        kc, fc = kemeny_costs(prof, perms), footrule_costs(prof, perms)
        kem, fbest = min(kc), min(fc)
        for k_cost, f_cost in zip(kc, fc):
            assert k_cost <= f_cost <= 2 * k_cost  # Diaconis and Graham, summed over the lists
            if f_cost == fbest:
                assert k_cost <= 2 * kem


def test_local_kemenization():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 7)
        prof = random_profile(rng, n, rng.randint(1, 5), partial=rng.random() < 0.5)
        start = sorted({x for r in prof for x in r})
        rng.shuffle(start)
        out = local_kemenize(start, prof)
        assert sorted(out) == sorted(start)
        # Locally Kemeny optimal: no adjacent swap lowers the total Kendall distance.
        for i in range(len(out) - 1):
            assert not prefers(prof, out[i + 1], out[i])
        assert total(kendall, out, prof) <= total(kendall, start, prof)
        # Extended Condorcet: if every item of a top set beats every other item, the set comes first.
        for size in range(1, len(out)):
            for top in itertools.combinations(sorted(out), size):
                rest = [y for y in out if y not in top]
                if all(prefers(prof, x, y) for x in top for y in rest):
                    assert set(out[:size]) == set(top)


def test_extended_procedure_on_the_page_example():
    prof = [list("abc")] * 3 + [list("bca")] * 2
    assert aggregate(prof, "MC4", eps=0.0)[0] == "a"
    assert aggregate(prof, "MC4", eps=0.15) == list("abc")
    assert aggregate([list("bc")] * 3 + [list("bc")] * 2, "MC4", eps=0.0) == list("bc")
    assert local_kemenize(list("bac"), prof) == list("abc")


def test_toy_runs():
    bm25 = [1, 2, 8, 7, 4]
    run = [1, 6, 8, 2, 4]
    # Document 6 is in one list only, so it beats 2, 8 and 4 by a "majority" of one list.
    assert aggregate([bm25, run], "MC4", eps=0.15) == [1, 6, 2, 8, 7, 4]
    items, m = transition_matrix([bm25, run], "MC4", exact=True)
    pi = exact_stationary(teleport(m, Fraction(3, 20)))
    assert dict(zip(items, pi)) == {1: Fraction(4, 7), 2: Fraction(2580, 30797), 4: Fraction(3, 103), 6: Fraction(39072, 215579), 7: Fraction(120, 2369), 8: Fraction(2580, 30797)}
    # With no teleport, document 1 is a Condorcet winner and holds all the mass.
    assert aggregate([bm25, run], "MC4", eps=0.0) == [1, 2, 4, 6, 7, 8]


def test_five_voter_profile_mc3_against_mc4():
    prof = [list("abc")] * 3 + [list("bca")] * 2
    assert aggregate(prof, "MC3", eps=0.0) == list("bac")
    _, m = transition_matrix(prof, "MC3", exact=True)
    assert exact_stationary(m) == [Fraction(3, 7), Fraction(13, 28), Fraction(3, 28)]
    _, m = transition_matrix(prof, "MC4", exact=True)
    assert exact_stationary(teleport(m, Fraction(3, 20))) == [Fraction(10, 13), Fraction(90, 559), Fraction(3, 43)]
