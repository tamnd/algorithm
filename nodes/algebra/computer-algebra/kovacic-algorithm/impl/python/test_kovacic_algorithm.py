# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kovacic-algorithm/. The authors are listed in prov/0QX1QC.jsonl.
import random
from fractions import Fraction as Q

import pytest

from kovacic_algorithm import kovacic, rf, rf_add, rf_der, rf_mul, rf_scale, pole_term, verify


def rsum(terms):
    a = rf([])
    for n, d in terms:
        a = rf_add(a, rf(n, d))
    return a


def riccati(w):
    """r = w' + w^2."""
    return rf_add(rf_der(w), rf_mul(w, w))


def check(r, expect_case=None):
    out = kovacic(*r)
    if expect_case is None:
        assert out is None
        return out
    assert out is not None
    case, F = out
    assert case == expect_case if isinstance(expect_case, int) else case in expect_case
    assert verify(r[0], r[1], F)
    return out


def test_worked_examples():
    trace = []
    case, F = kovacic([3, 0, 1], [1], trace)  # r = x^2 + 3
    assert case == 1 and len(trace) == 1 and trace[0][1] == 1
    assert F == [rf([-1, 0, -1], [0, 1]), rf([1])]  # w = x + 1/x, y = x e^(x^2/2)
    case, F = kovacic([-3, 16], [0, 0, 16])  # r = 1/x - 3/(16 x^2)
    assert case == 2
    assert F == [rf([Q(1, 16), -1], [0, 0, 1]), rf([Q(-1, 2)], [0, 1]), rf([1])]
    assert kovacic([0, 1], [1]) is None  # Airy
    assert not verify([3, 0, 1], [1], [rf([-1, 0, -1]), rf([1])])  # w = x is wrong
    assert not verify([4, 0, 1], [1], [rf([-1, 0, -1], [0, 1]), rf([1])])  # wrong r


@pytest.mark.parametrize("lam,mu,nu,n", [
    (Q(1, 2), Q(1, 3), Q(1, 3), 4),   # tetrahedral
    (Q(1, 2), Q(1, 3), Q(1, 4), 6),   # octahedral
    (Q(1, 2), Q(1, 3), Q(1, 5), 12),  # icosahedral
])
def test_finite_primitive_groups(lam, mu, nu, n):
    # Riemann equation with exponent differences lam, mu, nu at 0, 1, infinity
    r = rsum([([-(1 - lam * lam) / 4], [0, 0, 1]), ([-(1 - mu * mu) / 4], [1, -2, 1]),
              ([-(lam * lam + mu * mu - nu * nu - 1) / 4], [0, -1, 1])])
    case, F = check(r, 3)
    assert len(F) - 1 == n


def test_weber_family():
    # y'' = (x^2 + lam) y has a Liouvillian solution exactly when lam is an odd integer
    for lam in range(-9, 10):
        check(([lam, 0, 1], [1]), 1 if lam % 2 else None)


def test_modified_bessel_family():
    # nu = k/2: Liouvillian exactly when nu + 1/2 is an integer, that is k odd
    for k in range(0, 10):
        r = rsum([([1], [1]), ([Q(k * k - 1, 4)], [0, 0, 1])])
        check(r, (1, 2) if k % 2 else None)


def test_edge_cases():
    assert kovacic([], [1])[0] == 1  # y'' = 0
    assert kovacic([0, 0, 0, 1], [1]) is None  # odd order at infinity
    assert kovacic([1], [0, 1]) is None  # y'' = y/x
    with pytest.raises(ValueError):
        kovacic([1], [-2, 0, 1])  # poles at +-sqrt(2)


def random_lin(rng):
    return Q(rng.randint(-3, 3))


def test_planted_case_one():
    rng = random.Random(1986)
    halves = [Q(k) for k in range(-2, 4)] + [Q(1, 2), Q(3, 2), Q(-1, 2)]
    for _ in range(500):
        w = rf([random_lin(rng) for _ in range(rng.randint(0, 2))])
        for c in rng.sample(range(-3, 4), rng.randint(0, 2)):
            w = rf_add(w, pole_term(rng.choice(halves), Q(c), 1))
        check(riccati(w), 1)


def test_planted_case_two():
    rng = random.Random(1981)
    for _ in range(40):
        q = [Q(1)]
        for c in rng.sample(range(-3, 4), rng.randint(1, 2)):
            q = rf_mul(rf(q), rf([-c, 1]))[0]
        B = rf([rng.choice([1, -1, 2, Q(1, 2)])])
        for c in rng.sample(range(-3, 4), rng.randint(0, 2)):
            B = rf_mul(B, rf([1], [-c, 1]) if rng.random() < 0.5 else rf([-c, 1]))
        # w = A + B sqrt(q) with A = -B'/(2B) - q'/(4q) has w' + w^2 = A' + A^2 + q B^2
        A = rf_add(rf_scale(rf_mul(rf_der(B), rf(B[1], B[0])), Q(-1, 2)),
                   rf_scale(rf_mul(rf_der(rf(q)), rf([1], q)), Q(-1, 4)))
        r = rf_add(riccati(A), rf_mul(rf(q), rf_mul(B, B)))
        check(r, (1, 2))


def test_random_inputs_are_sound():
    rng = random.Random(4096)
    found = 0
    for _ in range(500):
        t = [Q(1)]
        for _ in range(rng.randint(0, 3)):
            t = rf_mul(rf(t), rf([rng.randint(-2, 2), 1]))[0]
        s = [Q(rng.randint(-4, 4)) for _ in range(rng.randint(1, 4))]
        try:
            out = kovacic(s, t)
        except NotImplementedError:
            continue
        if out is not None:
            found += 1
            assert verify(s, t, out[1])
    assert found > 0
