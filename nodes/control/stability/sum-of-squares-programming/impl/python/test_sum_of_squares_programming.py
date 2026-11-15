# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sum-of-squares-programming/. The authors are listed in prov/501R5E.jsonl.

import math
import random
from fractions import Fraction as F

from sum_of_squares_programming import (
    SOSProgram,
    certificate_holds,
    gram_form,
    jacobi_eig,
    ldl,
    lyapunov_program,
    monomials,
    padd,
    pclean,
    pderiv,
    peval,
    pmul,
    pscale,
    solve,
    sos_terms,
)

# 2 x^4 + 2 x^3 y - x^2 y^2 + 5 y^4 in the basis z = (x^2, y^2, x y).
P = {(4, 0): 2, (3, 1): 2, (2, 2): -1, (0, 4): 5}
Z = [(2, 0), (0, 2), (1, 1)]
MOTZKIN = {(4, 2): 1, (2, 4): 1, (2, 2): -3, (0, 0): 1}
# x1' = x2, x2' = -x1 - x2 - x1^3 (a damped Duffing oscillator).
DUFFING = [{(0, 1): 1}, {(1, 0): -1, (0, 1): -1, (3, 0): -1}]


def gram_family(lam):
    return [[2, lam, 1], [lam, 5, 0], [1, 0, -1 - 2 * lam]]


def square(p):
    return pmul(p, p)


def from_terms(terms):
    s = {}
    for d, l in terms:
        s = padd(s, pscale(square(l), d))
    return s


def ldl_product(L, D):
    n = len(D)
    return [[sum(L[i][k] * D[k] * L[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def vdot(V, f):
    d = {}
    for i in range(len(f)):
        d = padd(d, pmul(pderiv(V, i), f[i]))
    return d


def test_monomial_count_is_binomial():
    for n in range(1, 4):
        for d in range(0, 4):
            assert len(monomials(n, 0, d)) == math.comb(n + d, d)


def test_every_gram_matrix_of_the_family_gives_p():
    for lam in (-3, -2, F(-1, 2), 0, 7):
        assert gram_form(Z, gram_family(lam)) == P


def test_ldl_on_the_family():
    L, D = ldl(gram_family(-3))
    assert D == [2, F(1, 2), 0]
    assert ldl_product(L, D) == gram_family(-3)
    L, D = ldl(gram_family(-2))
    assert D == [2, 3, F(13, 6)]
    assert ldl(gram_family(0)) is None


def test_hand_decomposition():
    a = {(2, 0): 2, (0, 2): -3, (1, 1): 1}
    b = {(0, 2): 1, (1, 1): 3}
    s = padd(pscale(square(a), F(1, 2)), pscale(square(b), F(1, 2)))
    assert s == P
    L, D = ldl(gram_family(-3))
    assert from_terms(sos_terms(Z, L, D)) == P


def test_solver_finds_an_exact_certificate():
    prog = SOSProgram()
    prog.add_sos(P, [], Z)
    res = solve(prog)
    assert res is not None
    assert certificate_holds(prog, res)
    L, D = res["ldl"][0]
    assert all(d > 0 for d in D)
    assert from_terms(sos_terms(Z, L, D)) == P


def test_motzkin_basis_forces_a_negative_diagonal_entry():
    basis = [(0, 0), (1, 1), (2, 1), (1, 2)]
    rng = random.Random(3)
    for _ in range(20):
        Q = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(i, 4):
                Q[i][j] = Q[j][i] = F(rng.randint(-5, 5))
        # The only product of two basis monomials equal to x^2 y^2 is (xy)(xy).
        assert gram_form(basis, Q).get((2, 2), 0) == Q[1][1]
    prog = SOSProgram()
    prog.add_sos(MOTZKIN, [], basis)
    assert solve(prog) is None


def test_motzkin_is_nonnegative_but_search_fails():
    # Grid check of nonnegativity (the proof is the AM-GM inequality).
    for i in range(41):
        for j in range(41):
            x, y = -2 + i * 0.1, -2 + j * 0.1
            assert peval(MOTZKIN, (x, y)) >= -1e-12
    prog = SOSProgram()
    prog.add_sos(MOTZKIN, [], monomials(2, 0, 3))
    assert solve(prog, iters=300) is None


def test_negative_polynomial_has_no_certificate():
    p = {(4, 0): 1, (0, 4): 1, (2, 2): -3}
    assert peval(p, (1, 1)) == -1
    prog = SOSProgram()
    prog.add_sos(p, [], [(2, 0), (1, 1), (0, 2)])
    assert solve(prog, iters=300) is None


def test_univariate_positive_polynomials():
    for p in ({(4,): 1, (0,): 1}, {(4,): 1, (3,): -2, (2,): 3, (1,): -2, (0,): 1}):
        prog = SOSProgram()
        prog.add_sos(p, [], [(0,), (1,), (2,)])
        res = solve(prog)
        assert res is not None and certificate_holds(prog, res)


def test_random_interior_sos_polynomials():
    rng = random.Random(1)
    for n, basis in ((2, monomials(2, 0, 2)), (2, monomials(2, 0, 2)), (3, monomials(3, 1, 2))):
        k = len(basis)
        G = [[rng.randint(-3, 3) for _ in range(k)] for _ in range(k)]
        Q = [[sum(G[i][t] * G[j][t] for t in range(k)) + int(i == j) for j in range(k)] for i in range(k)]
        p = gram_form(basis, Q)
        prog = SOSProgram()
        prog.add_sos(p, [], basis)
        res = solve(prog)
        assert res is not None and certificate_holds(prog, res)
        L, D = res["ldl"][0]
        assert from_terms(sos_terms(basis, L, D)) == p


def test_hand_lyapunov_function_for_duffing():
    V = {(0, 2): F(1, 2), (2, 0): F(3, 4), (1, 1): F(1, 2), (4, 0): F(1, 4)}
    assert vdot(V, DUFFING) == {(2, 0): F(-1, 2), (0, 2): F(-1, 2), (4, 0): F(-1, 2)}
    assert ldl([[F(3, 4), F(1, 4)], [F(1, 4), F(1, 2)]])[1] == [F(3, 4), F(5, 12)]


def test_solver_finds_a_quartic_lyapunov_function():
    vb = [(2, 0), (1, 1), (0, 2), (4, 0)]
    gb = [(1, 0), (0, 1), (2, 0)]
    eps = F(1, 100)
    prog = lyapunov_program(DUFFING, vb, eps, gb, gb)
    res = solve(prog)
    assert res is not None and certificate_holds(prog, res)
    V = {m: c for m, c in zip(vb, res["c"]) if c != 0}
    W = vdot(V, DUFFING)
    sq = {(2, 0): eps, (0, 2): eps}
    # Exact: V - eps|x|^2 and -V' - eps|x|^2 are the Gram forms of the certificate.
    assert pclean(padd(V, sq, -1)) == gram_form(gb, res["Q"][0])
    assert pclean(padd(pscale(W, -1), sq, -1)) == gram_form(gb, res["Q"][1])
    # Sanity: V decreases along a simulated solution (RK4, dt = 0.01, T = 10).
    Vf = {k: float(v) for k, v in V.items()}

    def f(x):
        return (x[1], -x[0] - x[1] - x[0] ** 3)

    x, dt, steps = (2.0, -1.5), 0.01, int(round(10 / 0.01))
    assert steps == 1000
    last = peval(Vf, x)
    for _ in range(steps):
        k1 = f(x)
        k2 = f((x[0] + dt / 2 * k1[0], x[1] + dt / 2 * k1[1]))
        k3 = f((x[0] + dt / 2 * k2[0], x[1] + dt / 2 * k2[1]))
        k4 = f((x[0] + dt * k3[0], x[1] + dt * k3[1]))
        x = (x[0] + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
             x[1] + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
        now = peval(Vf, x)
        assert now < last
        last = now
    # The linear part has eigenvalues -1/2 +- i sqrt(3)/2, so |x| shrinks like e^(-t/2).
    assert math.hypot(*x) < 5e-2


def test_no_quadratic_certificate_for_duffing():
    prog = lyapunov_program(DUFFING, monomials(2, 2, 2), F(1, 100),
                            [(1, 0), (0, 1)], [(1, 0), (0, 1), (2, 0), (1, 1)])
    assert solve(prog, iters=300) is None
    # The reason: for V = a x1^2 + b x1 x2 + c x2^2, the quartic part of -V'
    # is b x1^4 + 2 c x1^3 x2, which is negative somewhere unless c = 0.
    a, b, c = F(1), F(1, 3), F(2)
    W = pscale(vdot({(2, 0): a, (1, 1): b, (0, 2): c}, DUFFING), -1)
    assert {k: v for k, v in W.items() if sum(k) == 4} == {(4, 0): b, (3, 1): 2 * c}


def test_ldl_random_matrices():
    rng = random.Random(7)
    for _ in range(30):
        n = rng.randint(1, 6)
        r = rng.randint(1, n)
        G = [[F(rng.randint(-3, 3)) for _ in range(r)] for _ in range(n)]
        Q = [[sum(G[i][t] * G[j][t] for t in range(r)) for j in range(n)] for i in range(n)]
        out = ldl(Q)
        assert out is not None
        L, D = out
        assert ldl_product(L, D) == Q
        assert all(d >= 0 for d in D)
        Q[0][0] -= 1 + sum(abs(v) for v in Q[0])
        assert ldl(Q) is None


def test_jacobi_eigenvalues():
    rng = random.Random(11)
    for _ in range(20):
        n = rng.randint(2, 5)
        S = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                S[i][j] = S[j][i] = rng.uniform(-2, 2)
        w, V = jacobi_eig(S)
        assert abs(sum(w) - sum(S[i][i] for i in range(n))) < 1e-9
        for k in range(n):
            Sv = [sum(S[i][j] * V[j][k] for j in range(n)) for i in range(n)]
            assert max(abs(Sv[i] - w[k] * V[i][k]) for i in range(n)) < 1e-9
