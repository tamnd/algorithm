# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/klu-solver/. The authors are listed in prov/SR6DG7.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from klu_solver import (
    SingularMatrixError,
    analyze,
    determinant,
    factor,
    klu_solve,
    max_transversal,
    minimum_degree,
    refactor,
    solve,
    tarjan_scc,
)
from sim3dense import solve as dense_solve

# Two stages joined by a voltage-controlled current source: a 1 V source at
# node 1, unit conductances 1-gnd, 1-2, 2-gnd, 3-gnd, 3-4, 4-gnd, and a VCCS
# of 2 S from node 3 to ground controlled by the voltage of node 2.
# Unknowns (e1, e2, e3, e4, j).
TWO_STAGE = [
    [2, -1, 0, 0, 1],
    [-1, 2, 0, 0, 0],
    [0, 2, 2, -1, 0],
    [0, 0, -1, 2, 0],
    [1, 0, 0, 0, 0],
]


def exact(a):
    return [[F(x) for x in row] for row in a]


def closure(adj, n):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in adj[i]:
            reach[i][j] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return reach


def brute_det(a):
    n = len(a)
    total = F(0)
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        prod = F(1)
        for i in range(n):
            prod *= a[i][perm[i]]
            if prod == 0:
                break
        total += -prod if inv % 2 else prod
    return total


def structural_rank_full(a):
    n = len(a)
    return any(all(a[i][p[i]] != 0 for i in range(n)) for p in itertools.permutations(range(n)))


def random_btf_matrix(rng, n):
    """A random sparse matrix, often reducible, with a nonzero determinant."""
    while True:
        a = [[F(0)] * n for _ in range(n)]
        perm = list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            a[i][perm[i]] = F(rng.choice([-3, -2, -1, 1, 2, 3, 5]))
        for _ in range(rng.randint(0, 2 * n)):
            a[rng.randrange(n)][rng.randrange(n)] = F(rng.randint(-4, 4))
        if brute_det(a) != 0 if n <= 6 else True:
            try:
                dense_solve(a, [F(1)] * n)
                return a
            except ValueError:
                continue


def check_btf(a, sym):
    n = len(a)
    pos_c = {c: k for k, c in enumerate(sym.pcol)}
    block_of = [0] * n
    for b, (s, e) in enumerate(sym.blocks):
        for k in range(s, e):
            block_of[k] = b
    for k, r in enumerate(sym.prow):
        for c in range(n):
            if a[r][c] != 0:
                assert block_of[k] <= block_of[pos_c[c]], "entry below the diagonal blocks"
    for k in range(n):
        assert a[sym.prow[k]][sym.pcol[k]] != 0, "zero on the permuted diagonal"
    # each diagonal block is irreducible: strongly connected
    for s, e in sym.blocks:
        m = e - s
        adj = [[t - s for t in range(s, e) if t != k and a[sym.prow[k]][sym.pcol[t]] != 0] for k in range(s, e)]
        reach = closure(adj, m)
        assert all(all(row) for row in reach)
    return block_of


def test_two_stage_example():
    a = exact(TWO_STAGE)
    sym = analyze(a)
    assert sym.prow == [2, 3, 0, 1, 4]
    assert sym.pcol == [2, 3, 4, 1, 0]
    assert sym.blocks == [(0, 2), (2, 3), (3, 4), (4, 5)]
    num = factor(a, sym)
    x = solve(num, [F(0), F(0), F(0), F(0), F(1)])
    assert x == [F(1), F(1, 2), F(-2, 3), F(-1, 3), F(-3, 2)]
    assert determinant(num) == brute_det(a) == F(-6)


def test_tarjan_against_closure():
    rng = random.Random(31)
    for _ in range(200):
        n = rng.randint(1, 9)
        adj = [sorted({rng.randrange(n) for _ in range(rng.randint(0, 3))} - {i}) for i in range(n)]
        comps = tarjan_scc(adj, n)
        reach = closure(adj, n)
        brute = {}
        for i in range(n):
            key = frozenset(j for j in range(n) if reach[i][j] and reach[j][i])
            brute[key] = True
        assert {frozenset(c) for c in comps} == set(brute)
        # emitted in reverse topological order: an edge goes to the same or an earlier component
        where = {v: k for k, c in enumerate(comps) for v in c}
        for i in range(n):
            for j in adj[i]:
                assert where[j] <= where[i]


def test_transversal_against_permutations():
    rng = random.Random(32)
    for _ in range(300):
        n = rng.randint(1, 6)
        a = [[1 if rng.random() < 0.35 else 0 for _ in range(n)] for _ in range(n)]
        rows = [{j for j in range(n) if a[i][j]} for i in range(n)]
        full = structural_rank_full(a)
        if full:
            match = max_transversal(rows, n)
            assert sorted(match) == list(range(n))
            assert all(a[match[j]][j] for j in range(n))
        else:
            with pytest.raises(SingularMatrixError):
                max_transversal(rows, n)


def test_minimum_degree_is_greedy():
    g = {0: {1, 2, 3}, 1: {0}, 2: {0}, 3: {0}}
    # leaves first; after two leaves the hub and the last leaf tie at degree 1
    assert minimum_degree(g) == [1, 2, 0, 3]
    # a path 0-1-2-3-4: ends first, never a middle node of degree 2
    path = {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2, 4}, 4: {3}}
    assert minimum_degree(path) == [0, 1, 2, 3, 4]


def test_btf_solve_det_refactor():
    rng = random.Random(33)
    for _ in range(150):
        n = rng.randint(1, 6)
        a = random_btf_matrix(rng, n)
        sym = analyze(a)
        check_btf(a, sym)
        num = factor(a, sym)
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
        assert solve(num, b) == dense_solve(a, b)
        assert determinant(num) == brute_det(a)
        # same pattern, new values: refactorization reuses the pivots
        a2 = [[x * F(rng.randint(1, 3), rng.randint(1, 3)) if x != 0 else F(0) for x in row] for row in a]
        try:
            num2 = refactor(a2, num)
        except SingularMatrixError:
            continue
        assert solve(num2, b) == dense_solve(a2, b)


def test_float_circuit_chain():
    # A chain of 40 amplifier stages, each a grounded RC-like node pair, one-way coupled.
    rng = random.Random(34)
    stages, n = 40, 80
    a = [[0.0] * n for _ in range(n)]
    for s in range(stages):
        i, j = 2 * s, 2 * s + 1
        g1, g2, g3 = (rng.uniform(0.5, 2.0) for _ in range(3))
        a[i][i] += g1 + g2
        a[j][j] += g2 + g3
        a[i][j] -= g2
        a[j][i] -= g2
        if s > 0:
            a[i][2 * s - 1] += rng.uniform(1.0, 5.0)  # transconductance from the previous stage
    b = [rng.uniform(-1, 1) for _ in range(n)]
    sym = analyze(a)
    assert len(sym.blocks) == stages
    x = klu_solve(a, b)
    r = max(abs(sum(a[i][k] * x[k] for k in range(n)) - b[i]) for i in range(n))
    assert r < 1e-9


def test_singular():
    with pytest.raises(SingularMatrixError):
        analyze([[F(1), F(1)], [F(0), F(0)]])
    with pytest.raises(SingularMatrixError):
        klu_solve([[F(1), F(2)], [F(2), F(4)]], [F(1), F(1)])
