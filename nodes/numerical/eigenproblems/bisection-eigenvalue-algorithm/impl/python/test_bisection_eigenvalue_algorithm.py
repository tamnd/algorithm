# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisection-eigenvalue-algorithm/. The authors are listed in prov/SXNY4P.jsonl.

import math
import random
from fractions import Fraction

from bisection_eigenvalue_algorithm import U, eigenvalues, gershgorin_interval, kth_eigenvalue, negcount


def exact_count(a, b, x):
    """Exact number of eigenvalues < x by the Sturm sequence of leading minors in Fraction.
    Zero minors are handled by the sign rule: a zero p_i takes the sign opposite to p_(i-1)."""
    x = Fraction(x)
    a = [Fraction(t) for t in a]
    b = [Fraction(t) for t in b]
    p_prev, p = Fraction(1), a[0] - x
    signs = [1, p]
    for i in range(1, len(a)):
        p_prev, p = p, (a[i] - x) * p - b[i - 1] ** 2 * p_prev
        signs.append(p)
    # number of sign agreements of (p_0, ..., p_n) for det(xI - T) style counting:
    # eigenvalues < x equal the sign changes of p_i(x) = det(T_i - x I)
    c, last = 0, 1
    for s in signs[1:]:
        if s == 0:
            s = -last
        if (s > 0) != (last > 0):
            c += 1
        last = s
    return c


def check_bracket(a, b, lam, rel=8 * U, absol=0.0):
    """For each computed eigenvalue, exact counts show an eigenvalue in [lam - d, lam + d]."""
    n = len(a)
    for k, x in enumerate(lam, start=1):
        d = Fraction(rel) * abs(Fraction(x)) + Fraction(absol)
        assert exact_count(a, b, Fraction(x) - d) <= k - 1
        assert exact_count(a, b, Fraction(x) + d) >= k


def toeplitz(n):
    return [2.0] * n, [-1.0] * (n - 1)


def test_page_example():
    a, b = toeplitz(4)
    assert gershgorin_interval(a, b) == (0.0, 4.0)
    assert [negcount(a, b, x) for x in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5)] == [1, 1, 2, 2, 2, 3, 3]
    x, steps = kth_eigenvalue(a, b, 2)
    assert abs(x - (3 - math.sqrt(5)) / 2 - 1) < 4 * U and steps == 54


def test_float_count_matches_exact_count():
    rng = random.Random(1)
    for trial in range(40):
        n = rng.randint(1, 12)
        a = [float(rng.randint(-5, 5)) for _ in range(n)]
        b = [float(rng.randint(-3, 3)) for _ in range(n - 1)]
        for _ in range(10):
            x = rng.randint(-200, 200) / 16.0 + 1.0 / 64
            assert negcount(a, b, x) == exact_count(a, b, x)


def test_toeplitz_known_spectra():
    for n in (1, 2, 3, 7, 20, 31):
        a, b = toeplitz(n)
        got = eigenvalues(a, b)
        want = [2.0 - 2.0 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)]
        assert all(got[i] <= got[i + 1] for i in range(n - 1))
        assert max(abs(x - y) for x, y in zip(got, want)) < 8 * U * 4


def test_random_tridiagonal_bracketed_exactly():
    rng = random.Random(2026)
    for trial in range(12):
        n = rng.randint(2, 10)
        a = [rng.uniform(-4, 4) for _ in range(n)]
        b = [rng.uniform(-2, 2) for _ in range(n - 1)]
        lam = eigenvalues(a, b)
        check_bracket(a, b, lam, rel=0, absol=8 * n * U * max(abs(t) for t in gershgorin_interval(a, b)))
        assert abs(sum(lam) - sum(a)) < 1e-12 * n


def test_trivial_cases():
    assert eigenvalues([3.5], []) == [3.5]
    assert all(abs(t) < 1e-300 for t in eigenvalues([0.0, 0.0, 0.0], [0.0, 0.0]))
    got = eigenvalues([1.0, 1.0], [1.0])
    assert abs(got[0]) <= 2 * U * 2 and abs(got[1] - 2.0) < 4 * U  # absolute error of order u ||T||


def test_repeated_eigenvalues_from_split_matrix():
    a = [1.0, 3.0, 1.0, 3.0, 2.0]
    b = [1.0, 0.0, 1.0, 0.0]
    got = eigenvalues(a, b)
    want = sorted([2 - math.sqrt(2), 2 - math.sqrt(2), 2 + math.sqrt(2), 2 + math.sqrt(2), 2.0])
    assert max(abs(x - y) for x, y in zip(got, want)) < 8 * U * 4


def test_wilkinson_nearly_equal_pair():
    """W21+: the two largest eigenvalues agree to about 13 significant digits but are separated."""
    a = [float(abs(10 - i)) for i in range(21)]
    b = [1.0] * 20
    lam = eigenvalues(a, b)
    gap = lam[-1] - lam[-2]
    assert 1e-14 < gap < 1e-12
    mid = Fraction(lam[-2]) + Fraction(gap) / 2
    assert exact_count(a, b, mid) == 20


def test_relative_accuracy_zero_diagonal_graded():
    """Zero diagonal and graded off-diagonal: tiny eigenvalues to high relative accuracy."""
    b = [1.0, 1e-6, 1e-12, 1e-18]
    a = [0.0] * 5
    lam = eigenvalues(a, b)
    check_bracket(a, b, lam, rel=64 * U, absol=1e-300)
    assert min(abs(t) for t in lam if t != 0.0) < 1e-17


def test_halving_rate():
    """Each step halves the interval: steps = number of halvings from the padded Gershgorin width."""
    a, b = toeplitz(10)
    x, steps = kth_eigenvalue(a, b, 3, abstol=1e-6)
    lo, hi = gershgorin_interval(a, b)
    width = (hi - lo) * (1 + 1e-12)
    assert steps == math.ceil(math.log2(width / 1e-6))
    want = 2.0 - 2.0 * math.cos(3 * math.pi / 11)
    assert abs(x - want) <= 0.5e-6


def test_count_is_monotone():
    rng = random.Random(4)
    a = [rng.uniform(-1, 1) for _ in range(30)]
    b = [rng.uniform(-1, 1) * 10 ** rng.randint(-8, 0) for _ in range(29)]
    xs = sorted(rng.uniform(-3, 3) for _ in range(400))
    cs = [negcount(a, b, x) for x in xs]
    assert all(cs[i] <= cs[i + 1] for i in range(len(cs) - 1))
