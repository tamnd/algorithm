# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-mechanism/. The authors are listed in prov/73DA32.jsonl.

import math
import random
from fractions import Fraction

import dpkit
from matrix_mechanism import (
    all_range_queries,
    hierarchical_strategy,
    identity,
    inverse,
    laplace_noise,
    matmul,
    matrix_mechanism,
    matvec,
    pseudoinverse,
    sensitivity,
    total_squared_error,
    transpose,
)


def _random_full_rank(rng: random.Random, p: int, n: int) -> list:
    while True:
        A = [[rng.randrange(-2, 3) for _ in range(n)] for _ in range(p)]
        try:
            inverse(matmul(transpose(A), A))
            return A
        except ValueError:
            continue


def test_pseudoinverse_meets_penrose_conditions_exactly() -> None:
    # The oracle is the four Penrose equations, checked in exact arithmetic.
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randrange(1, 4)
        p = rng.randrange(n, n + 3)
        A = _random_full_rank(rng, p, n)
        P = pseudoinverse(A)
        assert matmul(matmul(A, P), A) == [[Fraction(v) for v in row] for row in A]
        assert matmul(matmul(P, A), P) == P
        AP = matmul(A, P)
        assert AP == transpose(AP)
        PA = matmul(P, A)
        assert PA == [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        # Least squares: the residual of A^+ y is orthogonal to the columns of A.
        y = [rng.randrange(-5, 6) for _ in range(p)]
        r = [a - b for a, b in zip(matvec(A, matvec(P, y)), y)]
        assert matvec(transpose(A), r) == [0] * n


def test_noise_free_answers_are_exact() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randrange(1, 4)
        A = _random_full_rank(rng, rng.randrange(n, n + 3), n)
        W = [[rng.randrange(0, 2) for _ in range(n)] for _ in range(rng.randrange(1, 5))]
        x = [rng.randrange(0, 10) for _ in range(n)]
        assert matvec(W, matvec(pseudoinverse(A), matvec(A, x))) == matvec(W, x)


def test_rank_deficient_strategy_is_rejected() -> None:
    try:
        pseudoinverse([[1, 1], [2, 2]])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_sensitivity_is_the_largest_change_over_all_neighbors() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randrange(1, 5)
        A = [[rng.randrange(-3, 4) for _ in range(n)] for _ in range(rng.randrange(1, 6))]
        x = [rng.randrange(0, 5) for _ in range(n)]
        worst = 0
        for j in range(n):
            for sign in (1, -1):
                x2 = list(x)
                x2[j] += sign
                worst = max(worst, sum(abs(a - b) for a, b in zip(matvec(A, x), matvec(A, x2))))
        assert worst == sensitivity(A)
    assert sensitivity(hierarchical_strategy(8)) == 4


def _logpdf(point, centers, b):
    return sum(-abs(z - c) / b - math.log(2 * b) for z, c in zip(point, centers))


def test_noisy_strategy_answers_are_epsilon_dp() -> None:
    rng = random.Random(4)
    A, epsilon = hierarchical_strategy(4), 0.5
    b = sensitivity(A) / epsilon
    for _ in range(40):
        x = [rng.randrange(0, 6) for _ in range(4)]
        j = rng.randrange(4)
        x2 = list(x)
        x2[j] += 1
        cx, cy = matvec(A, x), matvec(A, x2)
        base = [rng.uniform(-10, 20) for _ in cx]
        d = [rng.uniform(-1, 1) for _ in cx]
        grid = [k / 4 for k in range(-300, 301)]
        f = lambda z, c: _logpdf([p + z * e for p, e in zip(base, d)], c, b)
        assert dpkit.log_ratio_grid(lambda z: f(z, cx), lambda z: f(z, cy), grid) <= epsilon + 1e-9
    # Tight: far below all centers, the three rows that hold cell 0 each move the ratio by 1/b.
    far = [-100.0] * 7
    x = [1, 1, 1, 1]
    assert math.isclose(_logpdf(far, matvec(A, [0, 1, 1, 1]), b) - _logpdf(far, matvec(A, x), b), epsilon)


def test_example_errors() -> None:
    W = all_range_queries(4)
    assert total_squared_error(W, identity(4), 1) == 40
    assert total_squared_error(W, hierarchical_strategy(4), 1) == Fraction(876, 7)
    assert total_squared_error(W, W, 1) == 288  # answering the workload itself
    for n in (2, 4, 8):
        # The identity strategy has total error 2 * (sum of range lengths) = n(n+1)(n+2)/3.
        assert total_squared_error(all_range_queries(n), identity(n), 1) == n * (n + 1) * (n + 2) // 3


def test_monte_carlo_error_and_bias_match_formula() -> None:
    rng = random.Random(5)
    W, x, epsilon, runs = all_range_queries(4), [3, 0, 5, 2], 1.0, 1500
    true = matvec(W, x)
    for A in (identity(4), hierarchical_strategy(4)):
        want = float(total_squared_error(W, A, epsilon))
        sq, mean = 0.0, [0.0] * len(W)
        for _ in range(runs):
            out = matrix_mechanism(W, A, x, epsilon, rng)
            sq += sum((o - t) ** 2 for o, t in zip(out, true))
            mean = [m + o / runs for m, o in zip(mean, out)]
        assert abs(sq / runs - want) <= 0.15 * want
        # Unbiased: each mean is within 6 standard errors of the true answer.
        assert all(abs(m - t) <= 6 * math.sqrt(want / runs) for m, t in zip(mean, true))


def test_laplace_tail_check_value() -> None:
    rng = random.Random(6)
    zs = [laplace_noise(2.0, rng) for _ in range(2000)]
    frac = sum(1 for z in zs if abs(z) > 2 * math.log(10)) / len(zs)
    assert abs(frac - 0.1) <= dpkit.hoeffding_margin(len(zs), 1e-6)


def test_bad_parameters() -> None:
    rng = random.Random(7)
    try:
        matrix_mechanism(identity(2), identity(2), [1, 1], 0.0, rng)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    try:
        hierarchical_strategy(6)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
