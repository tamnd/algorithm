# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jackknife-resampling/. The authors are listed in prov/DBF7V5.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from jackknife_resampling import delete_d_variance, jackknife, mean, median, plugin_variance, pseudo_values

MOUSE_TREATMENT = [94, 197, 16, 38, 99, 141, 23]


def sample_variance(xs):
    """S^2 with divisor n - 1, by its definition."""
    m = Fraction(sum(xs), len(xs))
    return sum((Fraction(v) - m) ** 2 for v in xs) / (len(xs) - 1)


def random_fractions(rng, n):
    return [Fraction(rng.randint(-50, 50), rng.randint(1, 6)) for _ in range(n)]


def test_variance_of_the_mean_is_s2_over_n():
    rng = random.Random(1)
    for n in range(2, 12):
        x = random_fractions(rng, n)
        r = jackknife(x, mean)
        assert r.variance == sample_variance(x) / n
        assert r.bias == 0 and r.corrected == mean(x)


def test_jackknife_of_plugin_variance_is_s2():
    rng = random.Random(2)
    for n in range(2, 12):
        x = random_fractions(rng, n)
        r = jackknife(x, plugin_variance)
        assert r.corrected == sample_variance(x)
        assert r.bias == -sample_variance(x) / n  # E(plug-in) - sigma^2 = -sigma^2/n


def u_statistic_by_definition(x, kernel):
    """The average of the kernel over all 2-subsets of the sample."""
    pairs = list(itertools.combinations(range(len(x)), 2))
    return sum((kernel(x[i], x[j]) for i, j in pairs), Fraction(0)) / len(pairs)


def v_statistic(kernel):
    def v(xs):
        n = len(xs)
        return sum((kernel(a, b) for a in xs for b in xs), Fraction(0)) / (n * n)

    return v


KERNELS = [
    lambda a, b: (a - b) ** 2 / 2,  # U = S^2
    lambda a, b: abs(a - b),  # Gini mean difference
    lambda a, b: Fraction(int(a + b > 0)),  # Wilcoxon one-sample kernel
    lambda a, b: a * b,  # U estimates mu^2
]


def test_jackknifed_v_statistic_is_the_u_statistic():
    rng = random.Random(3)
    for n in range(2, 9):
        x = random_fractions(rng, n)
        for h in KERNELS:
            assert jackknife(x, v_statistic(h)).corrected == u_statistic_by_definition(x, h)
    x = random_fractions(rng, 6)
    assert u_statistic_by_definition(x, KERNELS[0]) == sample_variance(x)


def test_pseudo_values():
    rng = random.Random(4)
    for n in range(2, 10):
        x = random_fractions(rng, n)
        r = jackknife(x, plugin_variance)
        pv = pseudo_values(x, plugin_variance)
        assert sum(pv) / n == r.corrected
        assert sample_variance(pv) / n == r.variance
        assert pseudo_values(x, mean) == x  # the pseudo-values of the mean are the data


def test_median_formula_and_inconsistency():
    rng = random.Random(5)
    for m in range(1, 7):
        n = 2 * m
        x = sorted(random_fractions(rng, n))
        gap = x[m] - x[m - 1]
        assert jackknife(x, median).variance == Fraction(n - 1, 4) * gap**2
    # For odd n the leave-one-out medians take only three values.
    loo = jackknife(MOUSE_TREATMENT, median).leave_one_out
    assert sorted(set(loo)) == [66, Fraction(137, 2), Fraction(193, 2)]


def test_delete_d_reduces_to_delete_one_and_is_exact_for_the_mean():
    rng = random.Random(6)
    for n in range(3, 9):
        x = random_fractions(rng, n)
        assert delete_d_variance(x, plugin_variance, 1) == jackknife(x, plugin_variance).variance
        for d in range(1, n):
            assert delete_d_variance(x, mean, d) == sample_variance(x) / n


def test_median_variance_estimates_by_simulation():
    """Measured, not proved: the delete-1 jackknife variance of the median does not settle
    as n grows, while the delete-d version with d near sqrt(n) stays closer to the truth."""
    rng = random.Random(7)
    n, reps = 16, 60
    ratios_one, ratios_d = [], []
    for _ in range(reps):
        x = [rng.random() for _ in range(n)]
        ratios_one.append(jackknife(x, median).variance)
        ratios_d.append(delete_d_variance(x, median, 4))
    true_var = 1 / (4 * (n + 2))  # variance of the uniform median, about 1/(4n)
    spread_one = math.sqrt(sum((v / true_var - 1) ** 2 for v in ratios_one) / reps)
    spread_d = math.sqrt(sum((v / true_var - 1) ** 2 for v in ratios_d) / reps)
    assert spread_d < spread_one


def test_float_example_and_errors():
    r = jackknife([float(v) for v in MOUSE_TREATMENT], mean)
    s2 = sample_variance(MOUSE_TREATMENT)
    assert math.isclose(math.sqrt(r.variance), math.sqrt(s2 / 7), rel_tol=1e-12)
    with pytest.raises(ValueError):
        jackknife([1.0], mean)
    with pytest.raises(ValueError):
        delete_d_variance([1, 2, 3], mean, 3)
