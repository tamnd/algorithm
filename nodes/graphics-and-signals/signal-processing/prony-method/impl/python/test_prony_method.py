# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prony-method/. The authors are listed in prov/ATNC9Z.jsonl.

import cmath
import random
from fractions import Fraction

import pytest

from prony_method import evaluate, least_squares, polynomial_roots, prediction_polynomial, prony, solve


def poly_from_roots(roots):
    """Coefficients (1, c[1], ..., c[p]) of the product of (z - r) over the roots."""
    c = [Fraction(1)] if roots and isinstance(roots[0], Fraction) else [1]
    for r in roots:
        c = [a - r * b for a, b in zip(c + [0], [0] + c)]
    return c


def samples(z, h, n):
    return [sum(hj * zj ** t for hj, zj in zip(h, z)) for t in range(n)]


def match_error(found, true):
    """Largest distance after pairing each true root with its nearest unused found root."""
    left = list(found)
    worst = 0.0
    for r in true:
        i = min(range(len(left)), key=lambda j: abs(left[j] - r))
        worst = max(worst, abs(left.pop(i) - r))
    return worst


def test_page_example() -> None:
    z = [Fraction(1, 2), Fraction(-1, 3)]
    x = samples(z, [Fraction(2), Fraction(1)], 4)
    assert x == [3, Fraction(2, 3), Fraction(11, 18), Fraction(23, 108)]
    c = prediction_polynomial(x, 2)
    assert c == [1, Fraction(-1, 6), Fraction(-1, 6)]
    assert c == poly_from_roots(z)
    rows = [[zj ** t for zj in z] for t in range(4)]
    assert least_squares(rows, x) == [2, 1]
    zf, hf = prony(x, 2)
    assert match_error(zf, [0.5, -1 / 3]) < 1e-12
    assert max(abs(a - b) for a, b in zip(evaluate(zf, hf, 4), [float(v) for v in x])) < 1e-12


def test_edges() -> None:
    with pytest.raises(ValueError):
        prediction_polynomial([1.0, 2.0, 3.0], 2)
    with pytest.raises(ValueError):
        prediction_polynomial([1.0, 2.0], 0)
    with pytest.raises(ValueError):
        solve([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]], [Fraction(1), Fraction(2)])
    # One exponential: c[1] = -x[1]/x[0].
    assert prediction_polynomial([Fraction(5), Fraction(15)], 1) == [1, -3]
    z, h = prony([4.0, 2.0, 1.0, 0.5], 1)
    assert abs(z[0] - 0.5) < 1e-12 and abs(h[0] - 4) < 1e-12


def test_exact_recovery_of_rational_exponentials() -> None:
    rng = random.Random(4701)
    pool = [Fraction(a, b) for a in range(-7, 8) for b in range(1, 6) if a != 0]
    pool = sorted(set(pool))
    for _ in range(500):
        p = rng.randint(1, 3)
        z = rng.sample(pool, p)
        h = [Fraction(rng.choice([-1, 1]) * rng.randint(1, 9), rng.randint(1, 4)) for _ in range(p)]
        n = 2 * p + rng.randint(0, 4)
        x = samples(z, h, n)
        c = prediction_polynomial(x, p)
        assert c == poly_from_roots(z)
        rows = [[zj ** t for zj in z] for t in range(n)]
        assert least_squares(rows, x) == h


def test_the_three_rationals_of_the_page() -> None:
    z = [Fraction(1, 2), Fraction(-1, 3), Fraction(3, 4)]
    h = [Fraction(1), Fraction(-2), Fraction(3, 2)]
    x = samples(z, h, 6)
    assert prediction_polynomial(x, 3) == poly_from_roots(z)
    zf, hf = prony(x, 3)
    assert match_error(zf, [0.5, -1 / 3, 0.75]) < 1e-9


def test_floating_point_recovery_of_damped_sinusoids() -> None:
    rng = random.Random(4702)
    for _ in range(500):
        p = rng.randint(1, 4)
        while True:
            z = [cmath.rect(rng.uniform(0.7, 1.0), rng.uniform(-3.0, 3.0)) for _ in range(p)]
            if min((abs(a - b) for i, a in enumerate(z) for b in z[i + 1:]), default=1) > 0.3:
                break
        h = [cmath.rect(rng.uniform(0.5, 2.0), rng.uniform(-3.0, 3.0)) for _ in range(p)]
        n = 2 * p + rng.randint(0, 6)
        x = samples(z, h, n)
        zf, hf = prony(x, p)
        assert match_error(zf, z) < 1e-6
        assert max(abs(a - b) for a, b in zip(evaluate(zf, hf, n), x)) < 1e-6


def test_roots_of_known_polynomial() -> None:
    roots = [2.0, -1.0, 0.5j, -0.5j]
    found = polynomial_roots(poly_from_roots(roots))
    assert match_error(found, roots) < 1e-10


def test_error_grows_with_noise() -> None:
    # Two damped complex exponentials, N = 24, p = 2, 200 noise draws per level (seed 4703).
    z = [cmath.rect(0.95, 0.5), cmath.rect(0.9, 1.3)]
    h = [1.0, 0.8]
    clean = samples(z, h, 24)
    rng = random.Random(4703)
    medians = []
    for sigma in (0.0, 1e-6, 1e-4, 1e-2):
        errs = []
        for _ in range(200):
            x = [v + complex(rng.gauss(0, sigma), rng.gauss(0, sigma)) for v in clean]
            errs.append(match_error(prony(x, 2)[0], z))
        errs.sort()
        medians.append(errs[len(errs) // 2])
    assert medians[0] < 1e-9
    assert medians[0] < medians[1] < medians[2] < medians[3]
    # Roughly linear in sigma for small noise.
    assert 10 < medians[2] / medians[1] < 1000
