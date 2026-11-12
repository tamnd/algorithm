# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitch-margoliash/. The authors are listed in prov/94EV9J.jsonl.

import random
from fractions import Fraction

import pytest

from fitch_margoliash import _attach, _nni_neighbors, _paths, fit, fitch_margoliash


def all_trees(n):
    """Every unrooted binary topology on leaves 0..n-1, (2n-5)!! of them."""
    trees = [[(0, n), (1, n), (2, n)]]
    for x in range(3, n):
        trees = [_attach(t, k, x, n + x - 2) for t in trees for k in range(len(t))]
    return trees


def splits(n, edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    out = {}
    for k, (u, v) in enumerate(edges):
        seen, stack, side = {u, v}, [v], set()
        while stack:
            x = stack.pop()
            if x < n:
                side.add(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if 0 in side:
            side = set(range(n)) - side
        out[frozenset(side)] = k
    return out


def random_tree(n, rng):
    edges, lengths = [(0, n), (1, n), (2, n)], [rng.randint(1, 9) for _ in range(3)]
    for x in range(3, n):
        k = rng.randrange(len(edges))
        edges = _attach(edges, k, x, n + x - 2)
        lengths = lengths[:k] + [rng.randint(1, 9) for _ in range(3)] + lengths[k + 1:]
    return edges, lengths


def tree_metric(n, edges, lengths):
    paths = _paths(list(range(n)), edges)
    D = [[0] * n for _ in range(n)]
    for (i, j), p in paths.items():
        D[i][j] = D[j][i] = sum(lengths[k] for k in p)
    return D


def random_matrix(n, rng):
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = D[j][i] = rng.randint(3, 20)
    return D


EXAMPLE = [[0, 2, 6, 6], [2, 0, 6, 9], [6, 6, 0, 4], [6, 9, 4, 0]]
AB_CD = [(0, 4), (1, 4), (4, 5), (2, 5), (3, 5)]


def test_example_from_page():
    b, Q = fit(EXAMPLE, AB_CD)
    assert b == [Fraction(3, 7), Fraction(11, 7), Fraction(25, 7), Fraction(10, 7), Fraction(18, 7)]
    assert Q == Fraction(1, 21)
    b0, Q0 = fit(EXAMPLE, AB_CD, power=0)
    assert b0 == [Fraction(1, 4), Fraction(7, 4), Fraction(15, 4), Fraction(5, 4), Fraction(11, 4)]
    assert Q0 == Fraction(9, 4)
    scores = sorted(fit(EXAMPLE, t)[1] for t in all_trees(4))
    assert scores == [Fraction(1, 21), Fraction(9, 23), Fraction(81, 137)]
    edges, lengths, Q = fitch_margoliash(EXAMPLE)
    assert Q == Fraction(1, 21)
    assert set(splits(4, edges)) >= {frozenset({2, 3})}


def test_three_taxa_and_errors():
    D = [[0, 3, 4], [3, 0, 5], [4, 5, 0]]
    edges, lengths, Q = fitch_margoliash(D)
    assert Q == 0
    assert dict(zip(edges, lengths)) == {(0, 3): 1, (1, 3): 2, (2, 3): 3}
    with pytest.raises(ValueError):
        fitch_margoliash([[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        fitch_margoliash([[0, 0, 1], [0, 0, 1], [1, 1, 0]])


def test_quartet_ols_closed_form():
    rng = random.Random(7)
    for _ in range(50):
        D = random_matrix(4, rng)
        b, Q = fit(D, AB_CD, power=0)
        ab, ac, ad, bc, bd, cd = D[0][1], D[0][2], D[0][3], D[1][2], D[1][3], D[2][3]
        assert b[2] == Fraction(ac + ad + bc + bd, 4) - Fraction(ab + cd, 2)
        assert b[0] == Fraction(ab, 2) + Fraction(ac + ad - bc - bd, 4)
        assert b[3] == Fraction(cd, 2) + Fraction(ac + bc - ad - bd, 4)
        assert Q == Fraction((ac + bd - ad - bc) ** 2, 4)


def test_normal_equations_hold_exactly():
    rng = random.Random(11)
    for _ in range(12):
        n = rng.randint(4, 6)
        D = random_matrix(n, rng)
        edges = rng.choice(all_trees(n))
        for power in (0, 2):
            b, Q = fit(D, edges, power=power)
            paths = _paths(list(range(n)), edges)
            grad = [Fraction(0)] * len(edges)
            for (i, j), p in paths.items():
                r = D[i][j] - sum(b[k] for k in p)
                for k in p:
                    grad[k] += r / Fraction(D[i][j]) ** power
            assert grad == [0] * len(edges)
            k = rng.randrange(len(edges))
            moved = list(b)
            moved[k] += Fraction(1, 3)
            Q2 = sum((D[i][j] - sum(moved[t] for t in p)) ** 2 / Fraction(D[i][j]) ** power for (i, j), p in paths.items())
            assert Q2 > Q


def test_recovers_additive_trees():
    rng = random.Random(13)
    for _ in range(15):
        n = rng.randint(4, 7)
        true_edges, true_len = random_tree(n, rng)
        D = tree_metric(n, true_edges, true_len)
        edges, lengths, Q = fitch_margoliash(D)
        assert Q == 0
        s_true, s_out = splits(n, true_edges), splits(n, edges)
        assert set(s_true) == set(s_out)
        assert all(lengths[s_out[s]] == true_len[k] for s, k in s_true.items())


def test_against_all_topologies():
    rng = random.Random(17)
    cases = [(5, 2)] * 6 + [(6, 0), (6, 2)]
    hits = 0
    for n, power in cases:
        D = random_matrix(n, rng)
        scores = [fit(D, t, power=power)[1] for t in all_trees(n)]
        edges, lengths, Q = fitch_margoliash(D, power=power)
        assert Q in scores
        assert Q >= min(scores)
        hits += Q == min(scores)
        assert all(fit(D, t, power=power)[1] >= Q for t in _nni_neighbors(edges, n))
    assert hits >= len(cases) // 2
    # on a tree metric the true topology is the only exact fit
    edges, lengths = random_tree(6, rng)
    D = tree_metric(6, edges, lengths)
    zero = [t for t in all_trees(6) if fit(D, t, power=0)[1] == 0]
    assert [set(splits(6, t)) for t in zero] == [set(splits(6, edges))]
