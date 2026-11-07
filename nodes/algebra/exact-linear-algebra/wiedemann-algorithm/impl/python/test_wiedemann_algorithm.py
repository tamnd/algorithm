# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiedemann-algorithm/. The authors are listed in prov/HAH02Z.jsonl.

import itertools
import random

import pytest

from wiedemann_algorithm import (SingularMatrix, berlekamp_massey, dense_black_box, sequence_minpoly,
                                 sparse_black_box, wiedemann_solve)


def gauss_solve(a, b, p):
    """Return the unique solution of a x = b mod p, or None if a is singular mod p."""
    n = len(a)
    m = [[v % p for v in row] + [bi % p] for row, bi in zip(a, b)]
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][k]), None)
        if piv is None:
            return None
        m[k], m[piv] = m[piv], m[k]
        inv = pow(m[k][k], -1, p)
        m[k] = [v * inv % p for v in m[k]]
        for i in range(n):
            if i != k and m[i][k]:
                f = m[i][k]
                m[i] = [(v - f * w) % p for v, w in zip(m[i], m[k])]
    return [m[i][n] for i in range(n)]


def brute_minpoly(s, p):
    """Smallest monic recurrence of s, by trying every coefficient tuple."""
    for big_l in range(len(s) + 1):
        for coef in itertools.product(range(p), repeat=big_l):
            f = list(coef) + [1]
            if all(sum(f[j] * s[i + j] for j in range(big_l + 1)) % p == 0 for i in range(len(s) - big_l)):
                return f
    raise AssertionError


def random_sparse(rng, n, p, per_row):
    rows = []
    for i in range(n):
        r = {i: rng.randrange(1, p)}
        for _ in range(per_row - 1):
            r[rng.randrange(n)] = rng.randrange(p)
        rows.append({j: v for j, v in r.items() if v})
    return rows


def to_dense(rows, n):
    return [[r.get(j, 0) for j in range(n)] for r in rows]


def test_berlekamp_massey_examples():
    # s_i = 1 + 3^i mod 101 has minimal polynomial (x - 1)(x - 3) = x^2 - 4x + 3
    s = [(1 + pow(3, i, 101)) % 101 for i in range(8)]
    assert berlekamp_massey(s, 101) == [3, 101 - 4, 1]
    assert berlekamp_massey([0, 0, 0], 7) == [1]
    assert berlekamp_massey([], 7) == [1]
    assert len(berlekamp_massey([0, 0, 5], 7)) == 4  # degree 3; not unique, since 3 terms < 2 * 3
    assert berlekamp_massey([0, 0, 5, 0, 0, 0], 7) == [0, 0, 0, 1]  # x^3, unique with 2L terms


def test_berlekamp_massey_vs_brute_force():
    rng = random.Random(1)
    for p in (2, 3):
        for _ in range(300):
            s = [rng.randrange(p) for _ in range(rng.randrange(0, 9))]
            f, g = berlekamp_massey(s, p), brute_minpoly(s, p)
            big_l = len(f) - 1
            assert big_l == len(g) - 1 and f[-1] == 1
            assert all(sum(f[j] * s[i + j] for j in range(big_l + 1)) % p == 0 for i in range(len(s) - big_l))
            if len(s) >= 2 * big_l:  # then the minimal polynomial is unique
                assert f == g


def test_worked_example():
    p = 7
    a = [[2, 1, 0], [0, 3, 1], [1, 0, 2]]
    apply = dense_black_box(a, p)
    b = apply([1, 1, 1])
    assert b == [3, 4, 3]
    seq, v = [], b
    for _ in range(6):
        seq.append(v[0])
        v = apply(v)
    assert seq == [3, 3, 0, 5, 4, 4]
    assert sequence_minpoly(apply, b, [1, 0, 0], p) == [1, 2, 0, 1]  # x^3 + 2x + 1, irreducible mod 7
    assert wiedemann_solve(apply, b, p, random.Random(3)) == [1, 1, 1]
    assert count_good_projections(a, b, p, 3) == 7**3 - 1  # only u = 0 fails


def test_bad_projection():
    p = 5
    apply = dense_black_box([[1, 0, 0], [0, 2, 0], [0, 0, 3]], p)
    f = sequence_minpoly(apply, [1, 1, 1], [1, 1, 0], p)
    assert f == [2, 2, 1]  # (x - 1)(x - 2), a proper divisor of mu_{A,b}
    x = [1, 3, 0]  # what line L7 gives from f
    assert apply(x) == [1, 1, 0] != [1, 1, 1]


def test_edges():
    p = 101
    assert wiedemann_solve(dense_black_box([], p), [], p) == []
    assert wiedemann_solve(dense_black_box([[5]], p), [10], p) == [2]
    assert wiedemann_solve(dense_black_box([[0, 1], [1, 0]], p), [3, 4], p) == [4, 3]  # zero diagonal
    assert wiedemann_solve(dense_black_box([[1, 2], [3, 4]], p), [0, 0], p) == [0, 0]
    with pytest.raises(SingularMatrix):  # a zero row and b with a component outside the range
        wiedemann_solve(dense_black_box([[1, 2], [0, 0]], p), [1, 1], p)
    with pytest.raises((SingularMatrix, RuntimeError)):
        wiedemann_solve(dense_black_box([[0, 0], [0, 0]], p), [1, 0], p)
    big = 2**61 - 1
    x = wiedemann_solve(dense_black_box([[3, 1], [1, 2]], big), [4, 3], big)
    assert x == [1, 1]


def count_good_projections(a, b, p, d):
    apply = dense_black_box(a, p)
    n = len(b)
    return sum(1 for u in itertools.product(range(p), repeat=n) if len(sequence_minpoly(apply, b, list(u), p)) - 1 == d)


def test_success_probability_exact():
    # The fraction of good u is Phi(mu)/p^d, the polynomial Euler function, and it is at least 1 - d/p.
    p, d = 5, 3
    diag = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]  # mu = (x-1)(x-2)(x-3), Phi = 4^3
    companion = [[0, 0, 4], [1, 0, 4], [0, 1, 0]]  # mu = x^3 + x + 1, irreducible mod 5, Phi = 5^3 - 1
    jordan = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]  # mu = (x-1)^3, Phi = 5^3 - 5^2
    for a, b, good in ((diag, [1, 1, 1], 64), (companion, [1, 0, 0], 124), (jordan, [0, 0, 1], 100)):
        assert count_good_projections(a, b, p, d) == good
        assert good >= (1 - d / p) * p**3


def test_success_rate_against_bound():
    # Over Z/101Z one try fails with probability at most deg(mu_{A,b})/101 <= n/101.
    p, n, trials = 101, 8, 400
    rng = random.Random(42)
    first_try = 0
    for _ in range(trials):
        while True:
            rows = random_sparse(rng, n, p, 3)
            if gauss_solve(to_dense(rows, n), [0] * n, p) is not None:
                break
        b = [rng.randrange(p) for _ in range(n)]
        stats = {}
        x = wiedemann_solve(sparse_black_box(rows, p), b, p, rng, stats=stats)
        assert x == gauss_solve(to_dense(rows, n), b, p)
        first_try += stats["tries"] == 1
    expected_failures = trials * n / p  # 31.7, an upper bound on the mean
    assert trials - first_try <= expected_failures + 3 * expected_failures**0.5


@pytest.mark.parametrize("p", [2, 3, 7, 101, 65537])
def test_random_vs_gauss(p):
    rng = random.Random(p)
    for _ in range(150):
        n = rng.randrange(1, 9)
        a = [[rng.randrange(p) if rng.random() < 0.5 else 0 for _ in range(n)] for _ in range(n)]
        b = [rng.randrange(p) for _ in range(n)]
        ref = gauss_solve(a, b, p)
        apply = dense_black_box(a, p)
        if ref is not None:
            assert wiedemann_solve(apply, b, p, rng) == ref
        else:
            try:
                x = wiedemann_solve(apply, b, p, rng, max_tries=8)
            except (SingularMatrix, RuntimeError):
                continue
            assert apply(x) == [v % p for v in b]  # a singular system can still be solved, and x is checked


def test_large_sparse():
    p = 1_000_003
    rng = random.Random(5)
    n = 60
    rows = random_sparse(rng, n, p, 4)
    x_true = [rng.randrange(p) for _ in range(n)]
    apply = sparse_black_box(rows, p)
    b = apply(x_true)
    if gauss_solve(to_dense(rows, n), [0] * n, p) is not None:
        assert wiedemann_solve(apply, b, p, rng) == x_true
