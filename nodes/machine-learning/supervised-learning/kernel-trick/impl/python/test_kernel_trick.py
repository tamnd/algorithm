# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-trick/. The authors are listed in prov/4044MK.jsonl.

import math
import random
from fractions import Fraction

from kernel_trick import (
    dot,
    gaussian_features_1d,
    gaussian_kernel,
    gram,
    is_psd,
    is_psd_exact,
    kernel_exp,
    kernel_perceptron,
    kernel_predict,
    kernel_product,
    kernel_scale,
    kernel_sum,
    kernel_warp,
    polynomial_features,
    polynomial_kernel,
    rank_exact,
)


def test_polynomial_feature_map_matches_the_kernel() -> None:
    rng = random.Random(11)
    for d in (1, 2, 3):
        for p in (1, 2, 3, 4):
            for c in (0.0, 1.0, 2.5):
                k = polynomial_kernel(p, c)
                for _ in range(20):
                    x = [rng.uniform(-2, 2) for _ in range(d)]
                    z = [rng.uniform(-2, 2) for _ in range(d)]
                    lhs = dot(polynomial_features(x, p, c), polynomial_features(z, p, c))
                    assert math.isclose(lhs, k(x, z), rel_tol=1e-10, abs_tol=1e-10)


def test_polynomial_feature_dimension() -> None:
    x = [0.3, -1.1, 2.0]
    for p in (1, 2, 3, 4):
        assert len(polynomial_features(x, p, 1.0)) == math.comb(3 + p, p)
        assert len(polynomial_features(x, p, 0.0)) == math.comb(3 + p - 1, p)


def test_degree_two_map_in_the_plane() -> None:
    # (x . z + 1)^2 = phi(x) . phi(z) with the six coordinates
    # (1, sqrt2 x1, sqrt2 x2, x1^2, sqrt2 x1 x2, x2^2) in some order.
    phi = sorted(round(v, 12) for v in polynomial_features([2.0, 3.0], 2, 1.0))
    r2 = math.sqrt(2)
    want = sorted(round(v, 12) for v in [1, r2 * 2, r2 * 3, 4, r2 * 6, 9])
    assert phi == want


def test_gaussian_truncated_features_converge() -> None:
    sigma = 1.3
    k = gaussian_kernel(sigma)
    for x, z in ((0.4, -0.7), (1.5, 1.2), (-2.0, 0.9)):
        errs = []
        for m in (2, 5, 10, 20, 40):
            approx = dot(gaussian_features_1d(x, sigma, m), gaussian_features_1d(z, sigma, m))
            errs.append(abs(approx - k([x], [z])))
        assert all(e2 <= e1 + 1e-15 for e1, e2 in zip(errs, errs[1:]))
        assert errs[-1] < 1e-12


def test_gaussian_gram_is_nonsingular_but_polynomial_gram_has_low_rank() -> None:
    # Distinct points: the Gaussian Gram matrix is positive definite for every n,
    # so no finite feature map works. The degree 2 polynomial kernel in 1D has a
    # 3 dimensional feature map, so its Gram matrix has rank at most 3.
    pts = [[Fraction(v)] for v in (-3, -1, 0, 2, 5, 7)]
    poly = [[(a[0] * b[0] + 1) ** 2 for b in pts] for a in pts]
    assert rank_exact(poly) == 3
    assert is_psd_exact(poly)
    k = gaussian_kernel(1.0)
    for n in range(1, 9):
        xs = [[0.5 * i] for i in range(n)]
        assert is_psd(gram(xs, k), tol=0.0)  # Cholesky with no shift succeeds


def test_closure_rules_give_psd_grams() -> None:
    rng = random.Random(3)
    xs = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(12)]
    lin = lambda x, z: dot(x, z)  # noqa: E731
    poly = polynomial_kernel(3, 1.0)
    built = [
        kernel_sum(lin, poly),
        kernel_product(lin, poly),
        kernel_scale(2.5, poly),
        kernel_exp(lin),
        kernel_warp(lambda x: math.sin(3 * x[0]) - 0.2, poly),
        # The Gaussian from the rules: exp(x.z/s^2) warped by exp(-|x|^2/2s^2).
        kernel_warp(lambda x: math.exp(-dot(x, x) / 2), kernel_exp(lin)),
    ]
    for k in built:
        assert is_psd(gram(xs, k))
    g1, g2 = gram(xs, built[-1]), gram(xs, gaussian_kernel(1.0))
    assert all(math.isclose(a, b, rel_tol=1e-12) for r1, r2 in zip(g1, g2) for a, b in zip(r1, r2))


def test_exact_psd_for_rational_polynomial_kernels() -> None:
    rng = random.Random(5)
    for _ in range(10):
        pts = [[Fraction(rng.randint(-4, 4)) for _ in range(2)] for _ in range(6)]
        for p in (1, 2, 3):
            g = [[(a[0] * b[0] + a[1] * b[1] + 1) ** p for b in pts] for a in pts]
            assert is_psd_exact(g)


def test_functions_that_are_not_kernels() -> None:
    # |x - z| has Gram [[0, 1], [1, 0]] on two points, with eigenvalue -1.
    dist = [[Fraction(abs(a - b)) for b in (0, 1)] for a in (0, 1)]
    assert not is_psd_exact(dist)
    # tanh(x . z - 1) has a negative diagonal entry at x = 0.
    xs = [[0.0], [1.0], [2.0]]
    assert not is_psd(gram(xs, lambda x, z: math.tanh(dot(x, z) - 1)))
    # A difference of kernels need not be a kernel.
    lin = lambda x, z: dot(x, z)  # noqa: E731
    assert not is_psd(gram([[1.0], [2.0]], lambda x, z: lin(x, z) - 2 * lin(x, z)))


def test_kernel_perceptron_learns_xor_only_with_a_nonlinear_kernel() -> None:
    xs = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    ys = [-1, 1, 1, -1]
    lin1 = lambda x, z: dot(x, z) + 1  # noqa: E731  (linear with a bias feature)
    _, ok = kernel_perceptron(xs, ys, lin1, max_epochs=200)
    assert not ok
    k = polynomial_kernel(2, 1.0)
    a, ok = kernel_perceptron(xs, ys, k)
    assert ok
    assert [kernel_predict(xs, ys, a, k, x) for x in xs] == ys
