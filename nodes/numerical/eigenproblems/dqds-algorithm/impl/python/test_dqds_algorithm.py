# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dqds-algorithm/. The authors are listed in prov/BE4Y2X.jsonl.
import math
import random
from fractions import Fraction

from dqds_algorithm import U, dqds_step, newton_shift, singular_values


def exact_singular_values(a, b):
    """Singular values from exact rational Sturm counts on B^T B, to about 2^-60 relative."""
    n = len(a)
    a = [Fraction(x) for x in a]
    b = [Fraction(x) for x in b]
    diag = [a[k] ** 2 + (b[k - 1] ** 2 if k else 0) for k in range(n)]
    off2 = [(a[k] * b[k]) ** 2 for k in range(n - 1)]

    def below(x):
        count, d = 0, diag[0] - x
        count += d < 0
        for k in range(1, n):
            if d == 0:
                d = Fraction(1, 10 ** 80)
            d = diag[k] - x - off2[k - 1] / d
            count += d < 0
        return count

    top = 2 * sum(diag) + 1
    out = []
    for i in range(n):
        lo, hi = Fraction(0), Fraction(top)
        while hi - lo > lo / 2 ** 60 and hi > Fraction(1, 10 ** 300):
            if lo > 0 and hi > 4 * lo:
                x = Fraction(math.sqrt(float(lo) * float(hi)))
            elif lo == 0:
                x = hi / 1024
            else:
                x = (lo + hi) / 2
            if below(x) > i:
                hi = x
            else:
                lo = x
        out.append(math.sqrt(float((lo + hi) / 2)))
    return sorted(out, reverse=True)


def assert_relative(got, want, c=8.0):
    n = len(want)
    for g, w in zip(got, want):
        if w == 0:
            assert g == 0
        else:
            assert abs(g - w) <= c * n * U * w, (g, w)


def test_page_example_graded():
    a, b = [1.0, 1e-4, 1e-8, 1e-12], [1.0, 1e-4, 1e-8]
    sigma, stats = singular_values(a, b)
    assert stats["steps"] == 5 and stats["failures"] == 0
    assert_relative(sigma, exact_singular_values(a, b), c=2.0)
    assert abs(sigma[3] - 4.9999999859375e-13) <= 4 * U * 5e-13
    q, e = [x * x for x in a], [x * x for x in b]
    tau = newton_shift(q, e, 4)
    assert abs(tau - 2.5e-25) <= 1e-6 * 2.5e-25
    qh, eh, _ = dqds_step(q, e, 4, tau)
    assert all(x > 0 for x in qh) and eh[2] < 1e-24  # e_3 fell from 1e-16 to 7.5e-25


def test_relative_accuracy_where_shifted_qr_is_absolute():
    a, b = [1e-12, 1e-4, 1e-8, 1.0], [1e-6, 1e-6, 1e-2]
    sigma, _ = singular_values(a, b)
    exact = exact_singular_values(a, b)
    assert_relative(sigma, exact)
    assert abs(exact[3] - 7.070714e-13) < 1e-18


def test_known_spectra():
    n = 12
    sigma, _ = singular_values([1.0] * n, [1.0] * (n - 1))
    assert_relative(sigma, [2 * math.cos(k * math.pi / (2 * n + 1)) for k in range(1, n + 1)])
    n = 40  # Cholesky factor of tridiag(-1, 2, -1): singular values sqrt(2 - 2 cos(k pi / (n + 1)))
    a = [math.sqrt((k + 1) / k) for k in range(1, n + 1)]
    b = [-math.sqrt(k / (k + 1)) for k in range(1, n)]
    sigma, _ = singular_values(a, b)
    want = sorted((2 * math.sin(k * math.pi / (2 * (n + 1))) for k in range(1, n + 1)), reverse=True)
    assert_relative(sigma, want, c=16.0)


def test_random_exact_invariants_and_rate():
    rnd = random.Random(1)
    n = 100
    a = [rnd.uniform(0.1, 1) for _ in range(n)]
    b = [rnd.uniform(0.1, 1) for _ in range(n - 1)]
    sigma, stats = singular_values(a, b)
    det = math.prod(a)
    assert abs(math.prod(sigma) / det - 1) <= 8 * n * U
    frob = float(sum(Fraction(x) ** 2 for x in a) + sum(Fraction(x) ** 2 for x in b))
    assert abs(sum(s * s for s in sigma) - frob) <= 8 * n * U * frob
    assert stats["steps"] <= 12 * n  # observed about 9 transforms per singular value
    a = [rnd.choice([-1, 1]) * 10 ** rnd.uniform(-6, 0) for _ in range(6)]
    b = [rnd.choice([-1, 1]) * 10 ** rnd.uniform(-6, 0) for _ in range(5)]
    assert_relative(singular_values(a, b)[0], exact_singular_values(a, b))


def test_trivial_and_zero_cases():
    assert singular_values([-3.0], [])[0] == [3.0]
    assert singular_values([0.0] * 3, [0.0] * 2)[0] == [0.0, 0.0, 0.0]
    sigma, _ = singular_values([2.0, -5.0, 1.0], [0.0, 0.0])  # diagonal
    assert sigma == [5.0, 2.0, 1.0]
    for a, b in (([0.0, 1.0, 2.0], [1.0, 1.0]), ([1.0, 0.0, 2.0], [1.0, 1.0]), ([1.0, 2.0, 0.0], [1.0, 1.0])):
        sigma, _ = singular_values(a, b)
        assert sigma[-1] == 0.0
        assert abs(sum(s * s for s in sigma) - (sum(x * x for x in a) + sum(x * x for x in b))) < 1e-14
    a, b, c = 3.0, 4.0, 2.0  # 2 by 2: sigma1 sigma2 = |ac|, sigma1^2 + sigma2^2 = a^2 + b^2 + c^2
    s1, s2 = singular_values([a, c], [b])[0]
    assert abs(s1 * s2 - 6.0) < 1e-14 and abs(s1 * s1 + s2 * s2 - 29.0) < 1e-13


def test_repeated_and_close_values():
    sigma, _ = singular_values([1.0] * 5, [0.0] * 4)
    assert sigma == [1.0] * 5
    sigma, _ = singular_values([1.0, 1.0], [1e-8])  # close pair 1 +- 5e-9
    assert abs(sigma[0] - (1 + 5e-9)) < 4 * U and abs(sigma[1] - (1 - 5e-9)) < 4 * U
    sigma, _ = singular_values([1.0, 1.0 + 1e-12, 1.0], [1e-300, 1e-300])
    assert abs(sigma[0] - (1 + 1e-12)) < 4 * U and sigma[1] == 1.0 and sigma[2] == 1.0
