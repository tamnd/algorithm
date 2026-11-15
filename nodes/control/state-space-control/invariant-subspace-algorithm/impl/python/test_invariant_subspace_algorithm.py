# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invariant-subspace-algorithm/. The authors are listed in prov/55N3T2.jsonl.

import itertools
import random
from fractions import Fraction

from invariant_subspace_algorithm import (
    contains, ddp, friend, image, intersection, is_ab_invariant, isa,
    kernel, markov_zero, preimage, span, subspace_sum,
)


def unit(i, n):
    return [Fraction(int(i == j)) for j in range(n)]


def rank(a):
    """Rank by fraction-free elimination, written apart from the module."""
    m = [[Fraction(v) for v in row] for row in a]
    r = 0
    ncol = len(m[0]) if m else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(r + 1, len(m)):
            f = m[i][c] / m[r][c]
            m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def matmul(a, b):
    return [[sum(Fraction(a[i][t]) * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, x):
    return [sum(Fraction(v) * w for v, w in zip(row, x)) for row in a]


def rand_mat(rng, n, m, lo=-2, hi=2):
    return [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]


def toeplitz_reference(a, b, c):
    """V* as the states x0 for which inputs u_0..u_(n-1) give y_0 = ... = y_n = 0.

    For x_(k+1) = A x_k + B u_k, y_k = C x_k, stack y_0..y_n = O x0 + T u
    and return {x0 : O x0 in im T}, as the x part of ker [O, T].
    """
    n, m, p = len(a), len(b[0]), len(c)
    powers = [[[Fraction(int(i == j)) for j in range(n)] for i in range(n)]]
    for _ in range(n):
        powers.append(matmul(a, powers[-1]))
    obs = []
    for k in range(n + 1):
        obs.extend(matmul(c, powers[k]))
    big = []
    for k in range(n + 1):
        for i in range(p):
            row = list(obs[k * p + i])
            for j in range(n):
                if j < k:
                    blk = matmul(matmul(c, powers[k - 1 - j]), b)
                    row.extend(blk[i])
                else:
                    row.extend([Fraction(0)] * m)
            big.append(row)
    sols = kernel(big, n + n * m)
    return span([s[:n] for s in sols])


def test_kernel_matches_rank():
    rng = random.Random(1)
    for _ in range(60):
        n, k = rng.randint(1, 5), rng.randint(1, 5)
        a = rand_mat(rng, k, n)
        ker = kernel(a, n)
        assert len(ker) + rank(a) == n
        for x in ker:
            assert all(v == 0 for v in matvec(a, x))


def test_subspace_operations():
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(2, 5)
        u = span([[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(1, n))])
        v = span([[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(1, n))])
        s = subspace_sum(u, v)
        i = intersection(u, v, n)
        assert len(s) + len(i) == len(u) + len(v)
        assert contains(u, i) and contains(v, i)
        a = rand_mat(rng, n, n)
        pre = preimage(a, v)
        for x in pre:
            assert contains(v, [matvec(a, x)])
        # dim A^(-1) V = dim ker A + dim (V intersected with im A)
        assert len(pre) == len(kernel(a, n)) + len(intersection(v, image(a), n))


def test_chain_of_four_integrators():
    n = 4
    a = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
    b = [[0], [0], [0], [1]]
    c = [[1, 0, 0, 0]]
    vstar, dims = isa(a, b, kernel(c, n))
    assert dims == [3, 2, 1, 0, 0]
    assert vstar == []


def test_ddp_example_of_the_page():
    a = [[0, 1, 0], [0, 0, 1], [0, 0, -1]]
    b = [[0], [1], [0]]
    c = [[1, 0, 0]]
    e = [[0], [0], [1]]
    vstar, dims = isa(a, b, kernel(c, 3))
    assert dims == [2, 1, 1]
    assert vstar == [unit(2, 3)]
    k, v = ddp(a, b, c, e)
    assert k == [[0, 0, 1]]
    assert markov_zero(a, b, c, e, k)
    # Every K = [k1, k2, 1] decouples, and K = [1, 2, 1] puts all poles at -1.
    assert markov_zero(a, b, c, e, [[Fraction(1), Fraction(2), Fraction(1)]])
    assert not markov_zero(a, b, c, e, [[Fraction(1), Fraction(2), Fraction(0)]])
    # With the disturbance in the input channel, DDP has no solution.
    k2, _ = ddp(a, b, c, [[0], [1], [0]])
    assert k2 is None


def test_sum_closed_intersection_not():
    a = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
    b = [[0], [0], [1]]
    v1 = span([unit(0, 3), unit(1, 3)])
    v2 = span([unit(1, 3), [Fraction(1), Fraction(0), Fraction(1)]])
    assert is_ab_invariant(a, b, v1) and is_ab_invariant(a, b, v2)
    assert is_ab_invariant(a, b, subspace_sum(v1, v2))
    meet = intersection(v1, v2, 3)
    assert meet == [unit(1, 3)]
    assert not is_ab_invariant(a, b, meet)


def test_random_systems_against_toeplitz_reference():
    rng = random.Random(3)
    nontrivial = 0
    for trial in range(500):
        n = rng.randint(2, 5) if trial < 80 else rng.randint(1, 3)
        m = rng.randint(1, 2)
        p = rng.randint(1, 2)
        a = rand_mat(rng, n, n)
        b = rand_mat(rng, n, m)
        c = rand_mat(rng, p, n)
        if trial % 4 == 0:
            # Make C B = 0 often, so V* is not trivial.
            b = [[0] * m for _ in range(n)]
            b[n - 1] = [1] * m
            c = [[rng.randint(-2, 2) for _ in range(n - 1)] + [0] for _ in range(p)]
        ker_c = kernel(c, n)
        vstar, dims = isa(a, b, ker_c)
        # the sequence is nonincreasing, strictly until it stops, and short
        assert all(x > y for x, y in zip(dims[:-2], dims[1:-1]))
        assert dims[-1] == dims[-2]
        assert len(dims) - 1 <= len(ker_c) + 1
        assert contains(ker_c, vstar)
        assert is_ab_invariant(a, b, vstar)
        assert vstar == toeplitz_reference(a, b, c)
        if vstar:
            nontrivial += 1
            k = friend(a, b, vstar)
            acl = [[Fraction(a[i][j]) - sum(Fraction(b[i][t]) * k[t][j] for t in range(m)) for j in range(n)] for i in range(n)]
            for x in vstar:
                assert contains(vstar, [matvec(acl, x)])
    assert nontrivial >= 10


def test_ddp_random_against_brute_force_feedback():
    rng = random.Random(4)
    yes = no = 0
    for _ in range(60):
        n = rng.randint(2, 3)
        a = rand_mat(rng, n, n)
        b = rand_mat(rng, n, 1)
        c = rand_mat(rng, 1, n)
        e = rand_mat(rng, n, 1)
        k, vstar = ddp(a, b, c, e)
        if k is not None:
            yes += 1
            assert markov_zero(a, b, c, e, k)
        else:
            no += 1
            for ks in itertools.product(range(-2, 3), repeat=n):
                kk = [[Fraction(v) for v in ks]]
                assert not markov_zero(a, b, c, e, kk)
    assert yes >= 3 and no >= 10


def test_full_state_space_when_c_is_zero():
    a = [[1, 2], [3, 4]]
    b = [[1], [0]]
    vstar, dims = isa(a, b, kernel([[0, 0]], 2))
    assert len(vstar) == 2 and dims == [2, 2]
