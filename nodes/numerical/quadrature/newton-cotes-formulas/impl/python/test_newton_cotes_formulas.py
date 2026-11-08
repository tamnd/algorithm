# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-cotes-formulas/. The authors are listed in prov/BB06D0.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from newton_cotes_formulas import degree_of_exactness, newton_cotes, newton_cotes_weights

CLOSED = list(range(2, 12))
OPEN = list(range(1, 8))


def counted(f):
    calls = [0]

    def g(x):
        calls[0] += 1
        return f(x)

    return g, calls


def test_known_weights() -> None:
    assert newton_cotes_weights(2)[1] == [F(1, 2), F(1, 2)]
    assert newton_cotes_weights(3)[1] == [F(1, 6), F(2, 3), F(1, 6)]
    assert newton_cotes_weights(4)[1] == [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
    assert newton_cotes_weights(5)[1] == [F(7, 90), F(16, 45), F(2, 15), F(16, 45), F(7, 90)]
    assert newton_cotes_weights(1, True)[1] == [F(1)]
    assert newton_cotes_weights(3, True)[1] == [F(2, 3), F(-1, 3), F(2, 3)]


def test_weights_sum_symmetry_and_signs() -> None:
    for n in CLOSED:
        _, w = newton_cotes_weights(n)
        assert sum(w) == 1 and w == w[::-1]
        # closed rules: negative weights first at 9 points, none at 10, again at 11
        assert (min(w) < 0) == (n in (9, 11))
    for n in OPEN:
        _, w = newton_cotes_weights(n, True)
        assert sum(w) == 1 and w == w[::-1]
        assert (min(w) < 0) == (n in (3, 5, 6, 7))


def test_degree_of_exactness_exact_arithmetic() -> None:
    for open_, ns in ((False, CLOSED), (True, OPEN)):
        for n in ns:
            d = degree_of_exactness(n, open_)
            for a, b, m in ((F(0), F(1), 1), (F(-2, 3), F(7, 5), 3)):
                for k in range(d + 2):
                    exact = (b ** (k + 1) - a ** (k + 1)) / (k + 1)
                    q = newton_cotes(lambda x, k=k: x**k, a, b, n, open_, m)
                    if k <= d:
                        assert q == exact, (n, open_, k)
                    else:
                        assert q != exact, (n, open_, k)


def test_error_constants() -> None:
    # E(x^(d+1)) = C h^(d+2) (d+1)! on one panel, with the classical constants
    table = {
        (2, False): F(-1, 12), (3, False): F(-1, 90), (4, False): F(-3, 80),
        (5, False): F(-8, 945), (1, True): F(1, 3), (2, True): F(3, 4),
        (3, True): F(14, 45),
    }
    for (n, open_), c in table.items():
        d = degree_of_exactness(n, open_)
        h = F(1, n + 1) if open_ else F(1, n - 1)
        if open_ and n == 1:
            h = F(1, 2)
        e = F(1, d + 2) - newton_cotes(lambda x: x ** (d + 1), F(0), F(1), n, open_)
        assert e == c * h ** (d + 2) * math.factorial(d + 1)


def test_random_polynomials_against_exact_integral() -> None:
    rng = random.Random(20261108)
    for _ in range(600):
        open_ = rng.random() < 0.4
        n = rng.choice(OPEN if open_ else CLOSED)
        d = degree_of_exactness(n, open_)
        c = [F(rng.randint(-9, 9), rng.randint(1, 6)) for _ in range(d + 1)]
        a = F(rng.randint(-10, 10), rng.randint(1, 4))
        b = a + F(rng.randint(-10, 10), rng.randint(1, 4))
        m = rng.randint(1, 4)

        def p(x):
            return sum(ck * x**k for k, ck in enumerate(c))

        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        assert newton_cotes(p, a, b, n, open_, m) == exact


def test_evaluation_count() -> None:
    for n in (2, 3, 5, 8):
        for m in (1, 2, 7):
            g, calls = counted(math.exp)
            newton_cotes(g, 0.0, 1.0, n, False, m)
            assert calls[0] == m * (n - 1) + 1
    for n in (1, 2, 4):
        g, calls = counted(math.exp)
        newton_cotes(g, 0.0, 1.0, n, True, 5)
        assert calls[0] == 5 * n


def test_open_rules_never_touch_the_ends() -> None:
    seen = []
    newton_cotes(lambda x: seen.append(x) or 0.0, 0.0, 1.0, 4, True, 3)
    assert all(0.0 < x < 1.0 for x in seen)
    q = newton_cotes(lambda x: 1 / math.sqrt(x), 0.0, 1.0, 2, True, 4096)
    assert abs(q - 2.0) < 0.05


def test_composite_convergence_rates() -> None:
    exact = math.e - 1
    for n, p in ((2, 2), (3, 4), (4, 4), (5, 6)):
        errs = [exact - newton_cotes(math.exp, 0.0, 1.0, n, False, m) for m in (2, 4, 8)]
        rates = [math.log2(abs(e1 / e2)) for e1, e2 in zip(errs, errs[1:])]
        assert all(abs(r - p) < 0.1 for r in rates), (n, rates)


def test_single_panel_on_exp() -> None:
    q = newton_cotes(math.exp, 0.0, 1.0, 5)
    assert abs((math.e - 1 - q) - (-8.594657e-07)) < 1e-12
    q = newton_cotes(math.exp, 0.0, 1.0, 11)
    assert abs(math.e - 1 - q) < 1e-14


def test_runge_divergence() -> None:
    f = lambda x: 1 / (1 + 25 * x * x)
    exact = 0.4 * math.atan(5)
    errs = [abs(exact - newton_cotes(f, -1.0, 1.0, n)) for n in (5, 9, 13, 17, 21)]
    assert errs == sorted(errs) and errs[-1] > 5
    # the composite rule with a fixed n converges instead
    assert abs(exact - newton_cotes(f, -1.0, 1.0, 5, False, 64)) < 1e-9


def test_edge_cases() -> None:
    assert newton_cotes(math.exp, 1.0, 1.0, 4) == 0.0
    q1 = newton_cotes(math.exp, 0.0, 1.0, 3, False, 4)
    q2 = newton_cotes(math.exp, 1.0, 0.0, 3, False, 4)
    assert abs(q1 + q2) < 1e-15
    with pytest.raises(ValueError):
        newton_cotes(math.exp, 0.0, 1.0, 1)
    with pytest.raises(ValueError):
        newton_cotes(math.exp, 0.0, 1.0, 0, True)
    with pytest.raises(ValueError):
        newton_cotes(math.exp, 0.0, 1.0, 3, False, 0)
    # a kink at a panel end is harmless, inside a panel it costs order
    kink = lambda x: abs(x - 0.5)
    assert abs(newton_cotes(kink, 0.0, 1.0, 3, False, 2) - 0.25) < 1e-15
    e1 = abs(newton_cotes(kink, 0.0, 1.0, 3, False, 3) - 0.25)
    e2 = abs(newton_cotes(kink, 0.0, 1.0, 3, False, 9) - 0.25)
    assert 5 < e1 / e2 < 12
