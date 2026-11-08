# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-kronrod-quadrature/. The authors are listed in prov/Q6XB94.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_kronrod_quadrature import (gauss_legendre, gk_panel, integrate, kronrod_rule, legendre_triple,
                                      stieltjes_coefficients)

U = 2.0 ** -53

# QUADPACK qk15 (Piessens et al. 1983): Kronrod nodes and weights, and the G7 weights
XGK = [0.991455371120812639206854697526329, 0.949107912342758524526189684047851,
       0.864864423359769072789712788640926, 0.741531185599394439863864773280788,
       0.586087235467691130294144845693013, 0.405845151377397166906606412076961,
       0.207784955007898467600689403773245, 0.0]
WGK = [0.022935322010529224963732008058970, 0.063092092629978553290700663189204,
       0.104790010322250183839876322541518, 0.140653259715525918745189590510238,
       0.169004726639267902826583426598550, 0.190350578064785409913256402421014,
       0.204432940075298892414161999234649, 0.209482141084727828012999174891714]
WG = [0.129484966168869693270611432679082, 0.279705391489276667901467771423780,
      0.381830050505118944950369775488975, 0.417959183673469387755102040816327]


def legendre_poly(k):
    """Exact monomial coefficients of P_k."""
    p0, p1 = [F(1)], [F(0), F(1)]
    if k == 0:
        return p0
    for j in range(1, k):
        nxt = [F(0)] * (j + 2)
        for i, c in enumerate(p1):
            nxt[i + 1] += F(2 * j + 1, j + 1) * c
        for i, c in enumerate(p0):
            nxt[i] -= F(j, j + 1) * c
        p0, p1 = p1, nxt
    return p1


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def integral(p):
    """Exact integral over [-1, 1]."""
    return sum((c * F(2, k + 1) for k, c in enumerate(p) if k % 2 == 0), F(0))


def degree(n):
    return 3 * n + 2 if n % 2 else 3 * n + 1


def test_matches_quadpack_qk15():
    y, wk, wg = kronrod_rule(7)
    assert len(y) == 15
    for i in range(8):
        assert y[i] == pytest.approx(-XGK[i], abs=2e-16) and y[14 - i] == pytest.approx(XGK[i], abs=2e-16)
        assert wk[i] == pytest.approx(WGK[i], abs=5e-16) and wk[14 - i] == pytest.approx(WGK[i], abs=5e-16)
    assert [wg[i] for i in (1, 3, 5, 7)] == pytest.approx(WG, abs=5e-16)
    assert [wg[i] for i in range(0, 15, 2)] == [0.0] * 8  # the Kronrod-only nodes


def test_worked_example_and_small_cases():
    assert stieltjes_coefficients(1) == (F(-2, 5), F(0), F(1))  # E_2 = P_2 - 2/5, zeros +-sqrt(3/5)
    assert stieltjes_coefficients(2) == (F(0), F(-9, 14), F(0), F(1))  # proportional to x^3 - 6x/7
    assert stieltjes_coefficients(3) == (F(14, 891), F(0), F(-20, 27), F(0), F(1))
    y, wk, wg = kronrod_rule(1)  # K3 extending G1 is G3
    assert y == pytest.approx((-math.sqrt(0.6), 0.0, math.sqrt(0.6))) and wk == pytest.approx((5 / 9, 8 / 9, 5 / 9))
    assert wg == (0.0, 2.0, 0.0)
    y, wk, _ = kronrod_rule(3)
    assert y[4:] == pytest.approx((0.43424374934680254, 0.7745966692414834, 0.9604912687080203), abs=2e-16)
    assert wk[3:] == pytest.approx((0.4509165386584741, 0.40139741477596225, 0.26848808986833345,
                                    0.10465622602646724), abs=5e-16)
    # the quartic factor of E_4: x^4 - 10/9 x^2 + 155/891
    for t in (y[4], y[6]):
        assert t ** 4 - 10 / 9 * t * t + 155 / 891 == pytest.approx(0.0, abs=1e-15)


def test_adams_formula_against_monomials():
    polys = [legendre_poly(k) for k in range(9)]
    for l in range(9):
        for m in range(9):
            for n in range(9):
                assert legendre_triple(l, m, n) == integral(mul(mul(polys[l], polys[m]), polys[n]))


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_stieltjes_orthogonality_exact(n):
    e = [F(0)] * (n + 2)
    for j, c in enumerate(stieltjes_coefficients(n)):
        for i, a in enumerate(legendre_poly(j)):
            e[i] += c * a
    ep = mul(e, legendre_poly(n))
    for k in range(n + 1):
        assert integral(mul(ep, [F(0)] * k + [F(1)])) == 0
    k = n + 1 if n % 2 == 0 else n + 2  # for odd n the product E P_n x^(n+1) is odd: one degree for free
    assert integral(mul(ep, [F(0)] * k + [F(1)])) != 0


@pytest.mark.parametrize("n", list(range(1, 11)))
def test_exactness_and_failure_at_next_degree(n):
    y, wk, wg = kronrod_rule(n)
    d = degree(n)
    for k in range(d + 1):
        exact = 2 / (k + 1) if k % 2 == 0 else 0.0
        assert abs(math.fsum(w * t ** k for w, t in zip(wk, y)) - exact) <= 20 * n * U
    k = d + 1  # always even
    err = 2 / (k + 1) - math.fsum(w * t ** k for w, t in zip(wk, y))
    assert abs(err) > 1e-12  # 0.046 at n = 1, 4.4e-12 at n = 10
    # the embedded Gauss rule has degree 2n - 1 and fails at 2n
    for k in range(2 * n):
        exact = 2 / (k + 1) if k % 2 == 0 else 0.0
        assert abs(math.fsum(w * t ** k for w, t in zip(wg, y)) - exact) <= 20 * n * U
    assert abs(2 / (2 * n + 1) - math.fsum(w * t ** (2 * n) for w, t in zip(wg, y))) > 1e-6


@pytest.mark.parametrize("n", [1, 2, 5, 7, 10, 15, 20, 30])
def test_interlacing_positivity_symmetry(n):
    y, wk, wg = kronrod_rule(n)
    gx, _ = gauss_legendre(n)
    assert len(y) == 2 * n + 1 and all(y[i] < y[i + 1] for i in range(2 * n))
    assert -1 < y[0] and y[-1] < 1
    assert list(y[1::2]) == gx  # Gauss nodes sit at odd positions: strict interlacing
    assert all(w > 0 for w in wk)
    assert math.fsum(wk) == pytest.approx(2.0, abs=50 * n * U) and math.fsum(wg) == pytest.approx(2.0, abs=50 * n * U)
    assert list(y) == [-t for t in reversed(y)] and list(wk) == list(reversed(wk))


def test_random_polynomial_oracle():
    rng = random.Random(1965)
    count = 0
    for _ in range(600):
        n = rng.randint(1, 8)
        c = [F(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(rng.randint(1, degree(n) + 1))]
        a = rng.uniform(-3.0, 3.0)
        b = a + rng.choice([-1, 1]) * rng.uniform(0.01, 2.0)
        fa, fb = F(a), F(b)  # exact binary values of the float endpoints
        exact = sum((ck * (fb ** (k + 1) - fa ** (k + 1)) / (k + 1) for k, ck in enumerate(c)), F(0))
        cf = [float(t) for t in c]

        def p(t):
            return math.fsum(ck * t ** k for k, ck in enumerate(cf))

        size = abs(b - a) * sum(abs(ck) * max(abs(a), abs(b)) ** k for k, ck in enumerate(cf))
        value, est, _, _ = gk_panel(p, a, b, n)
        assert abs(value - float(exact)) <= 1e-13 * size + 1e-300
        count += 1
    assert count == 600


@pytest.mark.parametrize("n,rate", [(1, 7), (2, 9)])
def test_panel_rate(n, rate):
    """The K_(2n+1) panel error on [0, h] for a smooth integrand behaves like h^(d + 2)."""
    errs = []
    for h in (0.125, 0.0625):
        value, _, _, _ = gk_panel(lambda t: math.exp(4 * t), 0.0, h, n)
        errs.append(abs(value - (math.exp(4 * h) - 1) / 4))
    assert math.log2(errs[0] / errs[1]) == pytest.approx(rate, abs=0.25)


def test_estimate_is_pessimistic_on_smooth_panels():
    # e^x on [0, 4]: Kronrod error about 1e-14, Gauss error about 5e-10, estimate about 5e-12
    k, est, g, _ = gk_panel(math.exp, 0.0, 4.0)
    exact = math.exp(4.0) - 1
    assert abs(k - exact) < 1e-13 < 1e-11 < abs(g - exact) and abs(k - exact) < est < abs(g - exact)
    # sqrt on [0, 1] is not smooth: the estimate still exceeds the true error
    k, est, g, _ = gk_panel(math.sqrt, 0.0, 1.0)
    assert abs(k - 2 / 3) < est


CLOSED = [
    ("exp", math.exp, 0.0, 1.0, math.e - 1, 15),
    ("sin", math.sin, 0.0, math.pi, 2.0, 15),
    ("runge", lambda t: 1 / (1 + t * t), -5.0, 5.0, 2 * math.atan(5.0), 225),
    ("ecos", lambda t: math.exp(math.cos(t)), 0.0, 2 * math.pi, 2 * math.pi * 1.2660658777520082, 105),
    ("sqrt", math.sqrt, 0.0, 1.0, 2 / 3, 585),
    ("log", math.log, 0.0, 1.0, -1.0, 1005),
    ("isqrt", lambda t: t ** -0.5, 0.0, 1.0, 2.0, 2025),
    ("cos100", lambda t: math.cos(100 * t), 0.0, 1.0, math.sin(100.0) / 100, 945),
    ("kink", lambda t: abs(t - 1 / 3), 0.0, 1.0, 5 / 18, 495),
    ("jump", lambda t: 0.0 if t < 0.3 else 1.0, 0.0, 1.0, 0.7, 975),
]


@pytest.mark.parametrize("name,f,a,b,exact,evals", CLOSED, ids=[c[0] for c in CLOSED])
def test_adaptive_closed_forms(name, f, a, b, exact, evals):
    value, est, used, status = integrate(f, a, b, tol=1e-10)
    assert status == "ok" and est <= 1e-10
    assert abs(value - exact) <= 1e-10  # the estimate was not fooled on any of these
    assert used == evals and used % 15 == 0


def test_evaluations_grow_slowly_with_tolerance():
    used = [integrate(math.sqrt, 0.0, 1.0, tol=t)[2] for t in (1e-6, 1e-8, 1e-10, 1e-12)]
    assert used == [315, 465, 585, 705]  # about 60 evaluations per factor 10 for a sqrt singularity
    errs = [abs(integrate(math.sqrt, 0.0, 1.0, tol=t)[0] - 2 / 3) for t in (1e-6, 1e-12)]
    assert errs[0] < 1e-6 and errs[1] < 1e-12


def test_edge_cases():
    assert integrate(math.exp, 2.0, 2.0) == (0.0, 0.0, 0, "ok")
    v, e, used, status = integrate(math.exp, 1.0, 0.0)
    assert v == pytest.approx(-(math.e - 1), rel=1e-15) and status == "ok"
    # unreachable tolerance: stops with "roundoff" instead of bisecting forever
    v, e, used, status = integrate(math.exp, 0.0, 1.0, tol=1e-20)
    assert status == "roundoff" and used == 15 and v == pytest.approx(math.e - 1, rel=1e-15)
    # a panel budget that is too small
    v, e, used, status = integrate(math.sqrt, 0.0, 1.0, tol=1e-14, limit=10)
    assert status == "limit" and e > 1e-14 and abs(v - 2 / 3) < e
    # relative tolerance
    assert integrate(math.exp, 0.0, 1.0, tol=0.0, rel=1e-6)[3] == "ok"
    # a function that is undefined at the endpoints is never evaluated there
    def strict0(t):
        if t <= 0.0:
            raise ValueError("endpoint evaluated")
        return t ** -0.5
    v, e, used, status = integrate(strict0, 0.0, 1.0, tol=1e-12)
    assert abs(v - 2.0) < 1e-12 and status == "ok"

    # a singularity at 1 instead of 0: floats near 1 are 1.1e-16 apart, so panels cannot shrink far enough
    def strict(t):
        if t <= 0.0 or t >= 1.0:
            raise ValueError("endpoint evaluated")
        return 1 / math.sqrt(t * (1 - t))
    v, e, used, status = integrate(strict, 0.0, 1.0, tol=1e-6)
    assert abs(v - math.pi) < 1e-6 and status == "ok"
    v, e, used, status = integrate(strict, 0.0, 1.0, tol=1e-10)
    assert status == "roundoff" and abs(v - math.pi) < e and e > 1e-7
    # a single panel with n = 1 is Simpson-like: G3
    v, e, _, _ = gk_panel(lambda t: t ** 5, -1.0, 1.0, 1)
    assert v == pytest.approx(0.0, abs=1e-16)
    with pytest.raises(ValueError):
        kronrod_rule(0)


def test_infinite_intervals_by_substitution():
    # x = t / (1 - t) maps [0, 1) onto [0, inf)
    def half_line(g):
        return lambda t: g(t / (1 - t)) / (1 - t) ** 2
    v, e, used, status = integrate(half_line(lambda x: math.exp(-x)), 0.0, 1.0)
    assert v == pytest.approx(1.0, abs=1e-12) and status == "ok"
    v, e, used, status = integrate(half_line(lambda x: 1 / (1 + x * x)), 0.0, 1.0)
    assert v == pytest.approx(math.pi / 2, abs=1e-12) and status == "ok"
