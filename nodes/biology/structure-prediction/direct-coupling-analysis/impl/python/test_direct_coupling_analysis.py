# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-coupling-analysis/. The authors are listed in prov/4X9C5V.jsonl.

import itertools
import math
import random
from fractions import Fraction

from direct_coupling_analysis import (apc, correlation_matrix, direct_information, frequencies, invert,
                                      mean_field_couplings, mfdca, mutual_information, sequence_weights,
                                      zero_sum_gauge)


def potts(n, q, h, couplings):
    """Exact Boltzmann distribution of a Potts model by enumeration of all q^n sequences.

    P(x) is proportional to exp(sum_i h[i][x_i] + sum_(i<j) J_ij(x_i, x_j)).
    """
    states = list(itertools.product(range(q), repeat=n))
    w = []
    for s in states:
        e = sum(h[i][s[i]] for i in range(n))
        e += sum(m[s[i]][s[j]] for (i, j), m in couplings.items())
        w.append(math.exp(e))
    z = sum(w)
    return states, [x / z for x in w]


def exact_marginals(n, q, states, p):
    f1 = [[0.0] * q for _ in range(n)]
    f2 = {(i, j): [[0.0] * q for _ in range(q)] for i in range(n) for j in range(i + 1, n)}
    for s, pr in zip(states, p):
        for i in range(n):
            f1[i][s[i]] += pr
            for j in range(i + 1, n):
                f2[(i, j)][s[i]][s[j]] += pr
    return f1, f2


def zero_table(n, q):
    return {(i, j): [[0.0] * q for _ in range(q)] for i in range(n) for j in range(i + 1, n)}


def test_weights_match_the_definition() -> None:
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(3, 8)
        msa = [tuple(rng.randrange(3) for _ in range(n)) for _ in range(rng.randint(1, 12))]
        got = sequence_weights(msa, 0.8)
        for x, w in zip(msa, got):
            close = sum(1 for y in msa if Fraction(sum(a == b for a, b in zip(x, y)), n) >= Fraction(4, 5))
            assert w == 1.0 / close


def test_page_example_weights() -> None:
    a, c = 0, 1
    msa = [(a, a, a, a, a), (a, a, a, a, c), (c, c, c, c, c)]
    w = sequence_weights(msa, 0.8)
    assert w == [0.5, 0.5, 1.0] and sum(w) == 2.0


def test_frequencies_match_direct_counting() -> None:
    rng = random.Random(2)
    q, n = 3, 4
    msa = [tuple(rng.randrange(q) for _ in range(n)) for _ in range(15)]
    w = [rng.choice((0.5, 1.0)) for _ in msa]
    lam = 2.0
    f1, f2 = frequencies(msa, q, w, lam)
    z = lam + sum(w)
    for i in range(n):
        for a in range(q):
            want = (lam / q + sum(wm for x, wm in zip(msa, w) if x[i] == a)) / z
            assert abs(f1[i][a] - want) < 1e-12
        for j in range(i + 1, n):
            for a in range(q):
                for b in range(q):
                    want = (lam / q ** 2 + sum(wm for x, wm in zip(msa, w) if x[i] == a and x[j] == b)) / z
                    assert abs(f2[(i, j)][a][b] - want) < 1e-12


def test_inverse_is_an_inverse() -> None:
    rng = random.Random(3)
    msa = [tuple(rng.randrange(4) for _ in range(5)) for _ in range(20)]
    w = sequence_weights(msa)
    f1, f2 = frequencies(msa, 4, w, sum(w))
    c = correlation_matrix(f1, f2, 4)
    ci = invert(c)
    for r in range(len(c)):
        for s in range(len(c)):
            got = sum(c[r][t] * ci[t][s] for t in range(len(c)))
            assert abs(got - (1.0 if r == s else 0.0)) < 1e-9


def test_independent_columns_give_zero_couplings() -> None:
    # Every sequence once: the empirical distribution is uniform, a product over columns.
    q, n = 3, 4
    msa = list(itertools.product(range(q), repeat=n))
    w = [1.0] * len(msa)
    f1, f2 = frequencies(msa, q, w, 0.0)
    e = mean_field_couplings(f1, f2, q)
    assert max(abs(v) for m in e.values() for r in m for v in r) < 1e-10


def planted(scale, n=4, q=3):
    rng = random.Random(5)
    h = [[rng.uniform(-0.5, 0.5) for _ in range(q - 1)] + [0.0] for _ in range(n)]
    couplings = {}
    for i in range(n):
        for j in range(i + 1, n):
            couplings[(i, j)] = [[rng.uniform(-1, 1) * scale if a < q - 1 and b < q - 1 else 0.0
                                  for b in range(q)] for a in range(q)]
    return n, q, h, couplings


def test_planted_weak_couplings_are_recovered() -> None:
    # Mean field is exact to first order in J, so the error must shrink like scale^2.
    errs = []
    for scale in (0.1, 0.05):
        n, q, h, couplings = planted(scale)
        states, p = potts(n, q, h, couplings)
        f1, f2 = exact_marginals(n, q, states, p)
        e = mean_field_couplings(f1, f2, q)
        err = max(abs(e[k][a][b] - couplings[k][a][b]) for k in couplings for a in range(q) for b in range(q))
        assert err <= 0.4 * scale ** 2, (scale, err)  # tolerance: measured error is about 0.28 scale^2
        errs.append(err)
    assert errs[1] <= 0.3 * errs[0]  # halving J divides the error by about 4


def test_mutual_information_is_fooled_and_dca_is_not() -> None:
    # The page example: binary columns A-B-C coupled in a chain, D-E weakly coupled.
    n, q = 5, 2
    couplings = zero_table(n, q)
    couplings[(0, 1)][0][0] = 2.0
    couplings[(1, 2)][0][0] = 2.0
    couplings[(3, 4)][0][0] = 0.5
    h = [[-1.0, 0.0] for _ in range(n)]
    states, p = potts(n, q, h, couplings)
    f1, f2 = exact_marginals(n, q, states, p)
    mi = {k: mutual_information(f1, f2, *k) for k in f2}
    assert mi[(0, 2)] > mi[(3, 4)] > 0  # the indirect pair beats a true one
    assert round(mi[(0, 1)], 4) == 0.0880 and round(mi[(0, 2)], 4) == 0.0154 and round(mi[(3, 4)], 4) == 0.0058
    e = mean_field_couplings(f1, f2, q)
    assert abs(e[(0, 2)][0][0]) < 1e-9
    assert round(e[(0, 1)][0][0], 4) == 2.3504 and round(e[(3, 4)][0][0], 4) == 0.5216


def test_zero_sum_gauge_has_the_least_norm() -> None:
    rng = random.Random(6)
    q = 4
    m = [[rng.uniform(-1, 1) for _ in range(q)] for _ in range(q)]
    g = zero_sum_gauge(m)
    norm = sum(v * v for r in g for v in r)
    for _ in range(200):
        u = [rng.uniform(-1, 1) for _ in range(q)]
        v = [rng.uniform(-1, 1) for _ in range(q)]
        moved = [[m[a][b] + u[a] + v[b] for b in range(q)] for a in range(q)]
        g2 = zero_sum_gauge(moved)
        assert max(abs(g2[a][b] - g[a][b]) for a in range(q) for b in range(q)) < 1e-12  # gauge invariant
        assert norm <= sum(x * x for r in moved for x in r) + 1e-12


def test_apc_matches_the_formula() -> None:
    rng = random.Random(7)
    n = 6
    f = {(i, j): rng.uniform(0, 1) for i in range(n) for j in range(i + 1, n)}
    s = apc(f, n)
    full = [[f[(min(i, j), max(i, j))] if i != j else None for j in range(n)] for i in range(n)]
    mean = sum(f.values()) / len(f)
    for (i, j), v in s.items():
        fi = sum(x for x in full[i] if x is not None) / (n - 1)
        fj = sum(x for x in full[j] if x is not None) / (n - 1)
        assert abs(v - (f[(i, j)] - fi * fj / mean)) < 1e-12


def test_direct_information_fits_the_marginals() -> None:
    rng = random.Random(8)
    q = 3
    for _ in range(20):
        e = [[rng.uniform(-1, 1) if a < q - 1 and b < q - 1 else 0.0 for b in range(q)] for a in range(q)]
        fi = [rng.uniform(0.1, 1) for _ in range(q)]
        fj = [rng.uniform(0.1, 1) for _ in range(q)]
        fi = [x / sum(fi) for x in fi]
        fj = [x / sum(fj) for x in fj]
        di, p = direct_information(e, fi, fj)
        assert max(abs(sum(p[a]) - fi[a]) for a in range(q)) < 1e-10
        assert max(abs(sum(p[a][b] for a in range(q)) - fj[b]) for b in range(q)) < 1e-10
        assert di >= -1e-12
    di0, _ = direct_information([[0.0] * q for _ in range(q)], fi, fj)
    assert abs(di0) < 1e-12  # no coupling, no direct information


def test_sampled_alignment_ranks_the_planted_chain_first() -> None:
    n, q = 6, 3
    couplings = zero_table(n, q)
    chain = [(i, i + 1) for i in range(n - 1)]
    for k in chain:
        couplings[k][0][0] = couplings[k][1][1] = 1.2
        couplings[k][0][1] = couplings[k][1][0] = -0.6
    h = [[0.0] * q for _ in range(n)]
    states, p = potts(n, q, h, couplings)
    rng = random.Random(9)
    msa = rng.choices(states, weights=p, k=700)
    ranked, _, _ = mfdca(msa, q)
    assert set(ranked[:len(chain)]) == set(chain)
    # Raw MI on the same data also puts the chain first here, but ranks indirect pairs (i, i + 2) next.
    w = sequence_weights(msa)
    f1, f2 = frequencies(msa, q, w, sum(w))
    mi = {k: mutual_information(f1, f2, *k) for k in f2}
    assert max(mi[(i, i + 2)] for i in range(n - 2)) > min(mi[(i, j)] for (i, j) in f2 if j - i > 2)
