# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymptotic-waveform-evaluation/. The authors are listed in prov/5A3DBS.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from asymptotic_waveform_evaluation import (
    asymptotic_waveform_evaluation,
    durand_kerner,
    is_stable,
    moments,
    polyval,
    step_response,
)


def rc_tree(parent, R, C):
    """Nodal equations (G + sC) v = b for an RC tree driven by a unit source through R[root]."""
    n = len(parent)
    G = [[Fraction(0)] * n for _ in range(n)]
    Cm = [[Fraction(0)] * n for _ in range(n)]
    b = [Fraction(0)] * n
    for i in range(n):
        g = 1 / Fraction(R[i])
        Cm[i][i] = Fraction(C[i])
        G[i][i] += g
        if parent[i] < 0:
            b[i] += g
        else:
            p = parent[i]
            G[p][p] += g
            G[i][p] -= g
            G[p][i] -= g
    return G, Cm, b


def unit(n, i):
    return [1 if k == i else 0 for k in range(n)]


def random_tree(rng, n):
    parent = [-1] + [rng.randrange(i) for i in range(1, n)]
    R = [rng.randint(1, 9) for _ in range(n)]
    C = [rng.randint(1, 9) for _ in range(n)]
    return parent, R, C


def polymul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def polyadd(a, b):
    k = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(k)]


def det_poly(M):
    """det of a matrix of polynomials by the Leibniz formula."""
    n = len(M)
    total = [Fraction(0)]
    for perm in itertools.permutations(range(n)):
        sign = 1
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    sign = -sign
        p = [Fraction(sign)]
        for i in range(n):
            p = polymul(p, M[i][perm[i]])
        total = polyadd(total, p)
    return total


def exact_transfer(G, C, b, l):
    """H(s) = N(s) / D(s) by Cramer's rule, with no moments involved."""
    n = len(G)
    M = [[[G[i][j], C[i][j]] for j in range(n)] for i in range(n)]
    D = det_poly(M)
    N = [Fraction(0)]
    for i in range(n):
        if l[i] != 0:
            Mi = [[[b[r], 0] if c == i else M[r][c] for c in range(n)] for r in range(n)]
            N = polyadd(N, [l[i] * x for x in det_poly(Mi)])
    return N, D


def series(N, D, count):
    """The first count Taylor coefficients of N(s) / D(s) at s = 0."""
    out = []
    for k in range(count):
        v = N[k] if k < len(N) else Fraction(0)
        for j in range(1, min(k, len(D) - 1) + 1):
            v -= D[j] * out[k - j]
        out.append(v / D[0])
    return out


def elmore(parent, R, C, i):
    def path(v):
        out = set()
        while v >= 0:
            out.add(v)
            v = parent[v]
        return out

    pi = path(i)
    return sum(C[k] * sum(R[e] for e in pi & path(k)) for k in range(len(parent)))


def test_moments_against_cramer_expansion():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(1, 5)
        parent, R, C = random_tree(rng, n)
        G, Cm, b = rc_tree(parent, R, C)
        l = [rng.randint(-2, 2) for _ in range(n)]
        N, D = exact_transfer(G, Cm, b, l)
        assert moments(G, Cm, b, l, 7) == series(N, D, 7)


def test_ladders_of_three_to_six_sections():
    rng = random.Random(6)
    for n in range(3, 7):
        R = [rng.randint(1, 9) for _ in range(n)]
        C = [rng.randint(1, 9) for _ in range(n)]
        G, Cm, b = rc_tree([-1] + list(range(n - 1)), R, C)
        l = unit(n, n - 1)
        N, D = exact_transfer(G, Cm, b, l)
        exact = series(N, D, 2 * n)
        assert moments(G, Cm, b, l, 2 * n) == exact
        for q in range(1, n + 1):
            model = asymptotic_waveform_evaluation(G, Cm, b, l, q)
            assert series(model.numerator, model.denominator, 2 * q) == exact[:2 * q]


def test_minus_first_moment_is_the_elmore_delay():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(1, 7)
        parent, R, C = random_tree(rng, n)
        G, Cm, b = rc_tree(parent, R, C)
        for i in range(n):
            m = moments(G, Cm, b, unit(n, i), 2)
            assert m[0] == 1
            assert -m[1] == elmore(parent, R, C, i)


def test_model_matches_two_q_moments():
    rng = random.Random(3)
    checked = 0
    for _ in range(80):
        n = rng.randint(2, 6)
        parent, R, C = random_tree(rng, n)
        G, Cm, b = rc_tree(parent, R, C)
        i = rng.randrange(n)
        for q in range(1, n + 1):
            try:
                model = asymptotic_waveform_evaluation(G, Cm, b, unit(n, i), q)
            except ValueError:
                continue  # singular Hankel matrix: no q-pole model exists
            exact = moments(G, Cm, b, unit(n, i), 2 * q + 1)
            assert series(model.numerator, model.denominator, 2 * q) == exact[:2 * q]
            checked += 1
    assert checked > 200


def test_q_equal_n_gives_the_exact_transfer_function():
    rng = random.Random(4)
    for _ in range(25):
        n = rng.randint(1, 5)
        _, R, C = random_tree(rng, n)
        # Far end of a chain: the numerator is a constant, so no pole cancels.
        G, Cm, b = rc_tree([-1] + list(range(n - 1)), R, C)
        l = unit(n, n - 1)
        N, D = exact_transfer(G, Cm, b, l)
        model = asymptotic_waveform_evaluation(G, Cm, b, l, n)
        assert model.denominator == [x / D[0] for x in D]
        assert polymul(model.numerator, D) == polymul(N, model.denominator)[:len(model.numerator) + len(D) - 1]
        assert is_stable(model.denominator)
        assert all(p.real < 0 and abs(p.imag) < 1e-6 * abs(p) for p in model.poles)


def test_one_pole_model_is_the_elmore_exponential():
    G, Cm, b = rc_tree([-1, 0, 1], [1, 2, 3], [3, 1, 2])
    model = asymptotic_waveform_evaluation(G, Cm, b, unit(3, 2), 1)
    td = elmore([-1, 0, 1], [1, 2, 3], [3, 1, 2], 2)
    assert model.denominator == [1, td]
    assert model.poles[0] == pytest.approx(-1 / td)
    assert step_response(model, float(td)) == pytest.approx(1 - 1 / 2.718281828459045)


def test_unstable_two_pole_model():
    # Ladder R = (1, 1, 1), C = (1, 2, 1), output at the middle node.
    G, Cm, b = rc_tree([-1, 0, 1], [1, 1, 1], [1, 2, 1])
    model = asymptotic_waveform_evaluation(G, Cm, b, unit(3, 1), 2)
    assert model.moments == [1, -7, 48, -330]
    assert model.denominator == [1, 6, -6]
    assert not is_stable(model.denominator)
    assert max(p.real for p in model.poles) == pytest.approx((6 + 60 ** 0.5) / 12, abs=1e-12)
    # The circuit itself is stable, and so is the exact model q = 3.
    exact = asymptotic_waveform_evaluation(G, Cm, b, unit(3, 1), 3)
    assert is_stable(exact.denominator)
    assert all(p.real < 0 for p in exact.poles)


def test_exact_stability_test_agrees_with_the_roots():
    rng = random.Random(5)
    for _ in range(400):
        deg = rng.randint(1, 5)
        roots = []
        while len(roots) < deg:
            re = rng.choice([-1, 1]) * rng.randint(1, 5) / 2
            if deg - len(roots) >= 2 and rng.random() < 0.5:
                im = rng.randint(1, 4) / 2
                roots += [complex(re, im), complex(re, -im)]
            else:
                roots.append(complex(re, 0))
        poly = [Fraction(1)]
        for r in roots:
            if r.imag > 0:
                poly = polymul(poly, [Fraction(r.real ** 2 + r.imag ** 2), Fraction(-2 * r.real), Fraction(1)])
            elif r.imag == 0:
                poly = polymul(poly, [Fraction(-r.real), Fraction(1)])
        assert is_stable(poly) == all(r.real < 0 for r in roots)
        if len(set(roots)) == len(roots):  # a multiple root is found to about sqrt(eps) only
            found = durand_kerner(poly)
            for r in roots:
                assert min(abs(r - z) for z in found) < 1e-8
    assert not is_stable([1, 0, 1])  # roots +i and -i
    assert not is_stable([0, 1])     # root 0
    assert is_stable([5])


def simulate(G, C, b, l, t_end, steps):
    """Brute force: RK4 on C v' = b - G v from v = 0, for a diagonal C."""
    n = len(G)
    Gf = [[float(x) for x in row] for row in G]
    cf = [float(C[i][i]) for i in range(n)]
    bf = [float(x) for x in b]

    def f(v):
        return [(bf[i] - sum(Gf[i][j] * v[j] for j in range(n))) / cf[i] for i in range(n)]

    h = t_end / steps
    v = [0.0] * n
    for _ in range(steps):
        k1 = f(v)
        k2 = f([v[i] + h / 2 * k1[i] for i in range(n)])
        k3 = f([v[i] + h / 2 * k2[i] for i in range(n)])
        k4 = f([v[i] + h * k3[i] for i in range(n)])
        v = [v[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(n)]
    return sum(l[i] * v[i] for i in range(n))


def test_step_response_against_simulation():
    G, Cm, b = rc_tree([-1, 0, 1, 1], [1, 2, 1, 3], [1, 1, 2, 1])
    l = unit(4, 3)
    exact = asymptotic_waveform_evaluation(G, Cm, b, l, 4)
    two = asymptotic_waveform_evaluation(G, Cm, b, l, 2)
    assert step_response(exact, 0.0) == pytest.approx(0.0, abs=1e-9)
    assert step_response(two, 0.0) == pytest.approx(0.0, abs=1e-9)
    worst = 0.0
    for t in (0.5, 2.0, 5.0, 10.0, 20.0):
        y = simulate(G, Cm, b, l, t, 4000)
        assert step_response(exact, t) == pytest.approx(y, abs=1e-8)
        worst = max(worst, abs(step_response(two, t) - y))
    assert worst < 0.02  # measured for this circuit, not a bound


def test_errors():
    G, Cm, b = rc_tree([-1], [2], [3])
    with pytest.raises(ValueError):
        asymptotic_waveform_evaluation(G, Cm, b, [1], 0)
    with pytest.raises(ValueError):
        asymptotic_waveform_evaluation(G, Cm, b, [1], 2)  # one pole only: singular Hankel matrix
    assert polyval([1, 2, 3], 2) == 17
