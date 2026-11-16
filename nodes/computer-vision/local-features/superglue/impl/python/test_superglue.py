# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superglue/. The authors are listed in prov/QBGQCK.jsonl.

import math
import random

from superglue import augment, mutual_matches, superglue_assign, transport_plan


def random_scores(rng, m, n, lo=-3.0, hi=3.0):
    return [[rng.uniform(lo, hi) for _ in range(n)] for _ in range(m)]


def sums(P):
    return [sum(r) for r in P], [sum(c) for c in zip(*P)]


def plain_sinkhorn(S, z, iters):
    """Sinkhorn in the plain domain: scale K = exp(S_bar) by row and column factors."""
    m, n = len(S), len(S[0])
    K = [[math.exp(x) for x in r] for r in augment(S, z)]
    a = [1.0] * m + [float(n)]
    b = [1.0] * n + [float(m)]
    y = [1.0] * (n + 1)
    x = [1.0] * (m + 1)
    for _ in range(iters):
        x = [a[i] / sum(K[i][j] * y[j] for j in range(n + 1)) for i in range(m + 1)]
        y = [b[j] / sum(K[i][j] * x[i] for i in range(m + 1)) for j in range(n + 1)]
    return [[x[i] * K[i][j] * y[j] for j in range(n + 1)] for i in range(m + 1)]


def partial_matchings(m, n):
    """All partial matchings of rows 0..m-1 into columns 0..n-1, as lists of pairs."""
    def rec(i, used):
        if i == m:
            yield []
            return
        for rest in rec(i + 1, used):
            yield rest
        for j in range(n):
            if j not in used:
                for rest in rec(i + 1, used | {j}):
                    yield [(i, j)] + rest
    yield from rec(0, frozenset())


def entropy(P):
    return -sum(p * (math.log(p) - 1.0) for r in P for p in r if p > 0)


def objective(Sbar, P):
    return sum(s * p for rs, rp in zip(Sbar, P) for s, p in zip(rs, rp))


def plan_of_matching(pairs, m, n):
    P = [[0.0] * (n + 1) for _ in range(m + 1)]
    for i, j in pairs:
        P[i][j] = 1.0
    for i in range(m):
        P[i][n] = 1.0 - sum(P[i][:n])
    for j in range(n):
        P[m][j] = 1.0 - sum(P[i][j] for i in range(m))
    P[m][n] = float(len(pairs))
    return P


def test_column_sums_are_exact_after_each_iteration():
    rng = random.Random(1)
    for iters in (1, 3, 10):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        P = transport_plan(random_scores(rng, m, n), rng.uniform(-1, 1), iters)
        _, cols = sums(P)
        assert all(abs(c - 1.0) < 1e-12 for c in cols[:n])
        assert abs(cols[n] - m) < 1e-12


def test_row_sums_converge_and_mass_is_m_plus_n():
    rng = random.Random(2)
    for _ in range(10):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        P = transport_plan(random_scores(rng, m, n), rng.uniform(-1, 1), 300)
        rows, _ = sums(P)
        assert all(abs(r - 1.0) < 1e-9 for r in rows[:m])
        assert abs(rows[m] - n) < 1e-9
        assert abs(sum(rows) - (m + n)) < 1e-9


def test_log_domain_equals_plain_domain():
    rng = random.Random(3)
    for _ in range(8):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        S, z = random_scores(rng, m, n), rng.uniform(-1, 1)
        P = transport_plan(S, z, 25)
        Q = plain_sinkhorn(S, z, 25)
        assert all(abs(p - q) < 1e-10 for rp, rq in zip(P, Q) for p, q in zip(rp, rq))


def test_large_scores_do_not_overflow():
    rng = random.Random(4)
    S = random_scores(rng, 4, 5, 500.0, 900.0)
    P, matches = superglue_assign(S, 700.0, iters=200)
    assert all(math.isfinite(p) for r in P for p in r)
    _, cols = sums(P)
    assert all(abs(c - 1.0) < 1e-9 for c in cols[:5])


def test_fixed_point_beats_marginal_preserving_perturbations():
    rng = random.Random(5)
    m, n = 4, 3
    S, z = random_scores(rng, m, n), 0.3
    Sbar = augment(S, z)
    P = transport_plan(S, z, 500)
    best = objective(Sbar, P) + entropy(P)
    for _ in range(200):
        i, k = rng.sample(range(m + 1), 2)
        j, l = rng.sample(range(n + 1), 2)
        d = rng.uniform(-1, 1) * 0.5 * min(P[i][j], P[k][l], P[i][l], P[k][j])
        Q = [r[:] for r in P]
        Q[i][j] += d
        Q[k][l] += d
        Q[i][l] -= d
        Q[k][j] -= d
        assert objective(Sbar, Q) + entropy(Q) <= best + 1e-12


def test_high_scale_matches_best_partial_matching():
    rng = random.Random(6)
    done = 0
    while done < 6:
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        S, z = random_scores(rng, m, n), rng.uniform(-1, 1)
        values = sorted(((sum(S[i][j] - z for i, j in pm), sorted(pm))
                         for pm in partial_matchings(m, n)), reverse=True)
        if len(values) > 1 and values[0][0] - values[1][0] < 1.0:
            continue  # skip near ties
        done += 1
        beta = 5.0
        Sb = [[beta * s for s in r] for r in S]
        P, matches = superglue_assign(Sb, beta * z, iters=2000, threshold=0.5)
        assert sorted((i, j) for i, j, _ in matches) == values[0][1]
        rows, _ = sums(P)
        assert all(abs(r - 1.0) < 1e-6 for r in rows[:m])  # converged
        # the bound of Lemma 4: LP optimum minus <S_bar, P> is at most (H(P) - H(P*)) / beta
        Sbar = augment(S, z)
        star = plan_of_matching(values[0][1], m, n)
        assert abs(objective(Sbar, star) - (values[0][0] + z * (m + n))) < 1e-9
        gap = objective(Sbar, star) - objective(Sbar, P)
        assert gap <= (entropy(P) - entropy(star)) / beta + 1e-6


def test_weak_rows_go_to_the_dustbin_and_matches_are_a_matching():
    rng = random.Random(7)
    S = random_scores(rng, 5, 4)
    S[2] = [-8.0] * 4
    P, matches = superglue_assign(S, 0.0, iters=200)
    assert all(i != 2 for i, _, _ in matches)
    assert P[2][4] > 0.99
    assert len({i for i, _, _ in matches}) == len(matches) == len({j for _, j, _ in matches})
    assert all(p > 0.2 for _, _, p in matches)
    assert mutual_matches(P, 1.0) == []
    assert superglue_assign([], 0.0) == ([], [])


def brute_mutual(P, theta):
    m, n = len(P) - 1, len(P[0]) - 1
    out = []
    for i in range(m):
        for j in range(n):
            row_ok = all(P[i][j] > P[i][k] or (P[i][j] == P[i][k] and j <= k) for k in range(n))
            col_ok = all(P[i][j] > P[k][j] or (P[i][j] == P[k][j] and i <= k) for k in range(m))
            if row_ok and col_ok and P[i][j] > theta:
                out.append((i, j, P[i][j]))
    return out


def test_many_small_inputs_against_plain_sinkhorn_and_brute_mutual():
    rng = random.Random(9)
    for trial in range(600):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        S = [[float(rng.randint(-2, 2)) for _ in range(n)] for _ in range(m)]
        z = float(rng.randint(-1, 1))
        iters = rng.randint(1, 8)
        P, matches = superglue_assign(S, z, iters=iters, threshold=0.2)
        Q = plain_sinkhorn(S, z, iters)
        assert all(abs(p - q) < 1e-9 for rp, rq in zip(P, Q) for p, q in zip(rp, rq))
        assert matches == brute_mutual(P, 0.2)


def test_transpose_gives_transposed_matches():
    rng = random.Random(8)
    for _ in range(5):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        S, z = random_scores(rng, m, n), rng.uniform(-1, 1)
        T = [list(c) for c in zip(*S)]
        _, a = superglue_assign(S, z, iters=400)
        _, b = superglue_assign(T, z, iters=400)
        assert sorted((i, j) for i, j, _ in a) == sorted((j, i) for i, j, _ in b)
