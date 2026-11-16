# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loftr/. The authors are listed in prov/JB95QG.jsonl.

import math
import random

from loftr import coarse_matches, dual_softmax, loftr_match, refine


def rand_vecs(rng, n, d):
    return [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n)]


def brute_dual_softmax(FA, FB, tau):
    S = [[sum(x * y for x, y in zip(a, b)) / tau for b in FB] for a in FA]
    m, n = len(FA), len(FB)
    P = []
    for i in range(m):
        row = []
        for j in range(n):
            r = math.exp(S[i][j]) / sum(math.exp(S[i][k]) for k in range(n))
            c = math.exp(S[i][j]) / sum(math.exp(S[k][j]) for k in range(m))
            row.append(r * c)
        P.append(row)
    return P


def brute_mutual(P, theta):
    m, n = len(P), len(P[0])
    out = []
    for i in range(m):
        for j in range(n):
            row_ok = all(P[i][j] > P[i][k] or (P[i][j] == P[i][k] and j <= k) for k in range(n))
            col_ok = all(P[i][j] > P[k][j] or (P[i][j] == P[k][j] and i <= k) for k in range(m))
            if row_ok and col_ok and P[i][j] >= theta:
                out.append((i, j, P[i][j]))
    return out


def test_dual_softmax_matches_definition_and_bounds():
    rng = random.Random(1)
    for _ in range(10):
        m, n, d = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 4)
        FA, FB = rand_vecs(rng, m, d), rand_vecs(rng, n, d)
        tau = rng.choice((0.5, 1.0, 2.0))
        P, Q = dual_softmax(FA, FB, tau), brute_dual_softmax(FA, FB, tau)
        assert all(abs(p - q) < 1e-12 for rp, rq in zip(P, Q) for p, q in zip(rp, rq))
        assert all(0.0 < p <= 1.0 for r in P for p in r)
        assert all(sum(r) <= 1.0 + 1e-12 for r in P)
        assert all(sum(c) <= 1.0 + 1e-12 for c in zip(*P))


def test_coarse_matches_equal_brute_force_with_ties():
    rng = random.Random(2)
    for trial in range(30):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        P = dual_softmax(rand_vecs(rng, m, 3), rand_vecs(rng, n, 3), 0.5)
        if trial % 3 == 0:
            P = [[round(p, 1) for p in r] for r in P]
        theta = rng.choice((0.0, 0.1, 0.3))
        got = coarse_matches(P, theta)
        assert got == brute_mutual(P, theta)
        assert len({i for i, _, _ in got}) == len(got) == len({j for _, j, _ in got})


def test_many_small_inputs_against_brute_force():
    rng = random.Random(7)
    for _ in range(600):
        m, n, d = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 3)
        FA = [[float(rng.randint(-2, 2)) for _ in range(d)] for _ in range(m)]
        FB = [[float(rng.randint(-2, 2)) for _ in range(d)] for _ in range(n)]
        tau = rng.choice((0.5, 1.0))
        P, Q = dual_softmax(FA, FB, tau), brute_dual_softmax(FA, FB, tau)
        assert all(abs(p - q) < 1e-12 for rp, rq in zip(P, Q) for p, q in zip(rp, rq))
        theta = rng.choice((0.0, 0.2, 0.5))
        assert coarse_matches(Q, theta) == brute_mutual(Q, theta)


def test_above_one_half_is_always_mutual():
    rng = random.Random(3)
    for _ in range(40):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        P = dual_softmax(rand_vecs(rng, m, 3), rand_vecs(rng, n, 3), 0.2)
        high = [(i, j) for i in range(m) for j in range(n) if P[i][j] > 0.5]
        assert sorted(high) == sorted((i, j) for i, j, _ in coarse_matches(P, 0.5000001))


def test_shift_and_transpose():
    rng = random.Random(4)
    m, n, d = 4, 5, 3
    FA, FB = rand_vecs(rng, m, d), rand_vecs(rng, n, d)
    P = dual_softmax(FA, FB, 0.5)
    # a constant added to every score: append a coordinate 1 to A and c to B
    Ps = dual_softmax([a + [1.0] for a in FA], [b + [3.7] for b in FB], 0.5)
    assert all(abs(p - q) < 1e-12 for rp, rq in zip(P, Ps) for p, q in zip(rp, rq))
    Pt = dual_softmax(FB, FA, 0.5)
    assert all(abs(P[i][j] - Pt[j][i]) < 1e-12 for i in range(m) for j in range(n))
    a = sorted((i, j) for i, j, _ in coarse_matches(P, 0.0))
    b = sorted((i, j) for j, i, _ in coarse_matches(Pt, 0.0))
    assert a == b


def test_refined_position_is_in_the_window():
    rng = random.Random(5)
    G = [[[rng.gauss(0, 1) for _ in range(4)] for _ in range(12)] for _ in range(10)]
    for _ in range(30):
        fx, fy = rng.randrange(12), rng.randrange(10)
        c = [rng.gauss(0, 1) for _ in range(4)]
        x, y = refine(c, G, fx, fy, 5, rng.choice((0.5, 1.0, 4.0)))
        assert max(0, fx - 2) - 1e-12 <= x <= min(11, fx + 2) + 1e-12
        assert max(0, fy - 2) - 1e-12 <= y <= min(9, fy + 2) + 1e-12


def test_peaked_window_gives_the_peak_within_the_bound():
    d, w = 3, 5
    G = [[[0.0] * d for _ in range(9)] for _ in range(9)]
    c = [1.0, 0.0, 0.0]
    G[3][5] = [1.0, 0.0, 0.0]  # offset (+1, -1) from the center (4, 4)
    for gap in (2.0, 5.0, 10.0):
        x, y = refine(c, G, 4, 4, w, gap)
        err = math.hypot(x - 5, y - 3)
        bound = (w * w - 1) * math.exp(-gap) * (w - 1) * math.sqrt(2)
        assert err <= bound + 1e-12
    x, y = refine(c, G, 4, 4, w, 30.0)
    assert abs(x - 5) < 1e-9 and abs(y - 3) < 1e-9


def test_full_pipeline_recovers_a_shuffled_grid():
    rng = random.Random(6)
    hc, wc, d = 3, 4, 16
    FA = [[x / math.sqrt(sum(t * t for t in v)) for x in v] for v in rand_vecs(rng, hc * wc, d)]
    perm = list(range(hc * wc))
    rng.shuffle(perm)
    FB = [None] * (hc * wc)
    for i, j in enumerate(perm):
        FB[j] = [x + rng.gauss(0, 0.05) for x in FA[i]]
    GA = [[[rng.gauss(0, 1) for _ in range(d)] for _ in range(4 * wc)] for _ in range(4 * hc)]
    GB = [[[0.0] * d for _ in range(4 * wc)] for _ in range(4 * hc)]
    for i, j in enumerate(perm):  # put the fine vector of A one fine pixel right of the cell of j
        bx, by = j % wc, j // wc
        GB[4 * by][min(4 * bx + 1, 4 * wc - 1)] = GA[4 * (i // wc)][4 * (i % wc)]
    out = loftr_match(FA, FB, wc, wc, GA, GB, tau=0.1, theta=0.2, w=5, scale=20.0)
    assert len(out) == hc * wc
    for (pa, pb, conf) in out:
        i = pa[1] // 8 * wc + pa[0] // 8
        j = perm[i]
        bx, by = j % wc, j // wc
        want = (2 * min(4 * bx + 1, 4 * wc - 1), 8 * by)
        assert abs(pb[0] - want[0]) < 1e-3 and abs(pb[1] - want[1]) < 1e-3 and conf >= 0.2
