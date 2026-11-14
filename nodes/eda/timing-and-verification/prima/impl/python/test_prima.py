# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prima/. The authors are listed in prov/KQ4G00.jsonl.

import random
from fractions import Fraction

import pytest

from prima import block_moments, lu_factor, poles, prima, transfer


def rc_tree(parent, R, C, ports):
    """Nodal G, C of an RC tree with a resistor R[root] from the root to ground.

    Port j injects a current at node ports[j] and observes its voltage (L = B)."""
    n = len(parent)
    G = [[Fraction(0)] * n for _ in range(n)]
    Cm = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        g = 1 / Fraction(R[i])
        Cm[i][i] = Fraction(C[i])
        G[i][i] += g
        if parent[i] >= 0:
            p = parent[i]
            G[p][p] += g
            G[i][p] -= g
            G[p][i] -= g
    B = [[Fraction(int(i == k)) for k in ports] for i in range(n)]
    return G, Cm, B


def rlc_ladder(g, c, r, ind, ports):
    """Modified nodal analysis of an RLC ladder.

    Node k has a conductance g[k] and a capacitor c[k] to ground. Branch j joins
    node j and node j + 1 by a resistor r[j] in series with an inductor ind[j].
    The unknowns are the n node voltages and the n - 1 branch currents, and
    G = [[N, E], [-E^T, Rb]], C = diag(c, ind), so G + G^T >= 0 and C >= 0."""
    n = len(g)
    m = n - 1
    size = n + m
    G = [[Fraction(0)] * size for _ in range(size)]
    Cm = [[Fraction(0)] * size for _ in range(size)]
    for k in range(n):
        G[k][k] = Fraction(g[k])
        Cm[k][k] = Fraction(c[k])
    for j in range(m):
        a, b, row = j, j + 1, n + j
        G[a][row] += 1
        G[b][row] -= 1
        G[row][a] -= 1
        G[row][b] += 1
        G[row][row] = Fraction(r[j])
        Cm[row][row] = Fraction(ind[j])
    B = [[Fraction(int(i == k)) for k in ports] for i in range(size)]
    return G, Cm, B


def exact_solve(A, rhs):
    n = len(A)
    M = [list(row) + [rhs[i]] for i, row in enumerate(A)]
    for col in range(n):
        p = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[p] = M[p], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def exact_moments(G, C, B, count):
    """Brute force: M_k = B^T (-G^{-1} C)^k G^{-1} B in exact arithmetic."""
    n = len(G)
    cols = [[B[i][j] for i in range(n)] for j in range(len(B[0]))]
    X = [exact_solve(G, b) for b in cols]
    out = []
    for _ in range(count):
        out.append([[sum(l[i] * x[i] for i in range(n)) for x in X] for l in cols])
        X = [exact_solve(G, [-sum(C[i][j] * v[j] for j in range(n)) for i in range(n)]) for v in X]
    return out


def close(A, B, rel):
    scale = max(abs(x) for row in B for x in row)
    return all(abs(a - b) <= rel * scale for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def reduced_moments(model, count):
    return block_moments(model.G, model.C, model.B, model.L, count)


def random_ladder(rng, n):
    return [-1] + list(range(n - 1)), [rng.randint(1, 9) for _ in range(n)], [rng.randint(1, 9) for _ in range(n)]


def test_rc_ladders_match_q_and_2q_moments():
    rng = random.Random(1)
    for n in range(3, 7):
        parent, R, C = random_ladder(rng, n)
        G, Cm, B = rc_tree(parent, R, C, [0])
        exact = exact_moments(G, Cm, B, 2 * n)
        for q in range(1, n):
            model = prima(G, Cm, B, B, q)
            got = reduced_moments(model, 2 * q + 1)
            for k in range(2 * q):  # G and C are symmetric and L = B: 2q moments
                assert close(got[k], [[float(x) for x in row] for row in exact[k]], 1e-9), (n, q, k)
            # The next moment is not matched in general.
            if q == 1:
                assert not close(got[2], [[float(x) for x in row] for row in exact[2]], 1e-6)


def pade(m, q):
    """Exact [q-1/q] Pade approximation from the moments m_0 .. m_{2q-1}: (P, Q) with Q(0) = 1."""
    hankel = [[m[k - j] for j in range(1, q + 1)] for k in range(q, 2 * q)]
    den = [Fraction(1)] + exact_solve(hankel, [-m[k] for k in range(q, 2 * q)])
    num = [sum(den[j] * m[k - j] for j in range(k + 1)) for k in range(q)]
    return num, den


def test_one_port_rc_model_is_the_pade_approximation():
    # Rational of type (q-1, q) matching 2q moments: the Pade approximation, which is unique.
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(3, 6)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        G, Cm, B = rc_tree(parent, [rng.randint(1, 9) for _ in range(n)], [rng.randint(1, 9) for _ in range(n)],
                           [rng.randrange(n)])
        m = [row[0][0] for row in exact_moments(G, Cm, B, 2 * n)]
        for q in range(1, n):
            P, Q = pade(m, q)
            model = prima(G, Cm, B, B, q)
            for s in (0.2, 1j, 1 + 1j):
                hr = transfer(model.G, model.C, model.B, model.L, s)[0][0]
                h = sum(complex(a) * s ** k for k, a in enumerate(P)) / sum(complex(b) * s ** k for k, b in enumerate(Q))
                assert abs(hr - h) <= 1e-7 * abs(h)


def test_rlc_and_multiport_match_q_block_moments():
    rng = random.Random(2)
    for n in range(3, 6):
        g = [Fraction(rng.randint(1, 5), 10) for _ in range(n)]
        c = [rng.randint(1, 5) for _ in range(n)]
        r = [Fraction(rng.randint(1, 5), 10) for _ in range(n - 1)]
        ind = [rng.randint(1, 5) for _ in range(n - 1)]
        for ports in ([0], [0, n - 1]):
            G, Cm, B = rlc_ladder(g, c, r, ind, ports)
            size = len(G)
            exact = exact_moments(G, Cm, B, 2 * size)
            for q in range(1, size // len(ports)):
                model = prima(G, Cm, B, B, q)
                assert len(model.X) == q * len(ports)
                got = reduced_moments(model, q)
                for k in range(q):
                    assert close(got[k], [[float(x) for x in row] for row in exact[k]], 1e-8), (n, ports, q, k)


def test_basis_is_orthonormal_and_deflates():
    rng = random.Random(3)
    parent, R, C = random_ladder(rng, 6)
    G, Cm, B = rc_tree(parent, R, C, [0, 5])
    model = prima(G, Cm, B, B, 3)
    X = model.X
    assert len(X) == 6
    for i in range(len(X)):
        for j in range(len(X)):
            assert abs(sum(a * b for a, b in zip(X[i], X[j])) - (i == j)) < 1e-12
    # Two equal ports span one direction only, and q p > n stops at n vectors.
    G, Cm, B = rc_tree(parent, R, C, [2, 2])
    assert len(prima(G, Cm, B, B, 1).X) == 1
    G, Cm, B = rc_tree(parent, R, C, [0])
    assert len(prima(G, Cm, B, B, 10).X) == 6


def test_full_order_gives_the_same_transfer_function():
    rng = random.Random(4)
    for _ in range(10):
        n = rng.randint(3, 6)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        G, Cm, B = rc_tree(parent, [rng.randint(1, 9) for _ in range(n)], [rng.randint(1, 9) for _ in range(n)], [0])
        model = prima(G, Cm, B, B, n)
        for s in (0.1, 1j, 0.3 + 2j, 5.0):
            h = transfer(G, Cm, B, B, s)[0][0]
            hr = transfer(model.G, model.C, model.B, model.L, s)[0][0]
            assert abs(h - hr) <= 1e-9 * abs(h)


def det(A):
    try:
        M, perm = lu_factor(A)
    except ValueError:
        return 0.0  # a zero column during elimination: exactly singular
    sign = 1
    p = list(perm)
    for i in range(len(p)):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            sign = -sign
    out = sign
    for i in range(len(M)):
        out *= M[i][i]
    return out


def test_poles_in_the_left_half_plane():
    rng = random.Random(5)
    for trial in range(40):
        n = rng.randint(3, 5)
        if trial % 2 == 0:
            parent = [-1] + [rng.randrange(i) for i in range(1, n)]
            G, Cm, B = rc_tree(parent, [rng.randint(1, 9) for _ in range(n)],
                               [rng.randint(1, 9) for _ in range(n)], [0])
        else:
            G, Cm, B = rlc_ladder([Fraction(rng.randint(1, 5), 10) for _ in range(n)],
                                  [rng.randint(1, 5) for _ in range(n)],
                                  [Fraction(rng.randint(0, 5), 10) for _ in range(n - 1)],
                                  [rng.randint(1, 5) for _ in range(n - 1)], [0])
        q = rng.randint(1, len(G) - 1)
        model = prima(G, Cm, B, B, q)
        ps = poles(model.G, model.C)
        assert len(ps) == len(model.X)  # the reduced C is non-singular here
        for p in ps:
            assert p.real < 0
            # p is a root of det(G_r + p C_r), relative to Hadamard's bound on the determinant
            k = len(model.G)
            M = [[model.G[i][j] + p * model.C[i][j] for j in range(k)] for i in range(k)]
            hadamard = 1.0
            for i in range(k):
                hadamard *= sum((abs(model.G[i][j]) + abs(p) * abs(model.C[i][j])) ** 2 for j in range(k)) ** 0.5
            assert abs(det(M)) <= 1e-10 * hadamard
            if trial % 2 == 0:
                assert abs(p.imag) <= 1e-7 * abs(p)  # symmetric RC: real poles


def test_rlc_model_is_positive_real():
    rng = random.Random(6)
    g = [Fraction(1, 10), Fraction(0), Fraction(0), Fraction(1, 20)]
    c = [1, 2, 1, 3]
    r = [Fraction(1, 10), Fraction(0), Fraction(1, 5)]
    ind = [2, 1, 3]
    G, Cm, B = rlc_ladder(g, c, r, ind, [0, 3])
    for q in (1, 2, 3):
        model = prima(G, Cm, B, B, q)
        for _ in range(200):
            s = complex(rng.uniform(0.0, 3.0), rng.uniform(-5.0, 5.0))
            H = transfer(model.G, model.C, model.B, model.L, s)
            # Hermitian part of a 2 x 2 matrix: positive semidefinite
            h11 = H[0][0].real
            h22 = H[1][1].real
            h12 = (H[0][1] + H[1][0].conjugate()) / 2
            assert h11 >= -1e-9 and h22 >= -1e-9
            assert h11 * h22 - abs(h12) ** 2 >= -1e-9


def test_reduced_g_can_be_singular_for_rlc():
    # LC ladder with one conductance: G is invertible, but X^T G X is diag(1/3, 0).
    G, Cm, B = rlc_ladder([1, 0, 0], [1, 1, 1], [0, 0], [1, 1], [0])
    assert lu_factor([[float(x) for x in row] for row in G])
    model = prima(G, Cm, B, B, 2)
    s3, s5 = 3 ** -0.5, 5 ** -0.5
    assert model.X[0] == pytest.approx([s3, s3, s3, 0, 0], abs=1e-12)
    assert model.X[1] == pytest.approx([0, 0, 0, 2 * s5, s5], abs=1e-12)
    assert model.G[0][0] == pytest.approx(1 / 3, abs=1e-12)
    assert max(abs(model.G[0][1]), abs(model.G[1][0]), abs(model.G[1][1])) < 1e-12


def test_errors():
    G, Cm, B = rc_tree([-1], [1], [1], [0])
    with pytest.raises(ValueError):
        prima(G, Cm, B, B, 0)
    with pytest.raises(ValueError):
        lu_factor([[0.0, 0.0], [0.0, 1.0]])
