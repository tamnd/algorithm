# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-pca/. The authors are listed in prov/V5B4MS.jsonl.

import math
import random

from kernel_pca import KernelPCA, center_gram, gram, jacobi_eigen, linear_kernel, polynomial_kernel, rbf_kernel

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def linear_pca(x):
    n, d = len(x), len(x[0])
    mu = [sum(p[j] for p in x) / n for j in range(d)]
    cov = [[sum((p[i] - mu[i]) * (p[j] - mu[j]) for p in x) / n for j in range(d)] for i in range(d)]
    vals, vecs = jacobi_eigen(cov)
    order = sorted(range(d), key=lambda j: -vals[j])
    return mu, [vals[j] for j in order], [[vecs[i][j] for i in range(d)] for j in order]


def close_up_to_sign(a, b, tol):
    return all(abs(s - t) < tol for s, t in zip(a, b)) or all(abs(s + t) < tol for s, t in zip(a, b))


def test_worked_example_linear_kernel():
    m = KernelPCA(EXAMPLE, linear_kernel, 3)
    assert all(abs(a - b) < 1e-9 for a, b in zip(m.eigenvalues, [648, 288, 72]))
    assert all(abs(a - b) < 1e-9 for a, b in zip(m.feature_variances(), [81, 36, 9]))
    for row in m.training_scores():
        assert all(abs(abs(s) - t) < 1e-9 for s, t in zip(row, (9, 6, 3)))
    # the new point mu + (1, 2, 2) has the score 3 on the first component and 0 on the others
    (s,) = m.transform([(5, 7, 8)])
    assert abs(abs(s[0]) - 3) < 1e-9 and abs(s[1]) < 1e-9 and abs(s[2]) < 1e-9


def test_centering():
    rng = random.Random(1)
    x = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(9)]
    k = gram(x, x, rbf_kernel(0.7))
    kc = center_gram(k)
    assert all(abs(sum(row)) < 1e-12 for row in kc)
    # for the linear kernel, K' is the Gram matrix of the centered points
    mu = [sum(p[j] for p in x) / 9 for j in range(3)]
    xc = [[p[j] - mu[j] for j in range(3)] for p in x]
    kl = center_gram(gram(x, x, linear_kernel))
    assert all(abs(kl[i][j] - linear_kernel(xc[i], xc[j])) < 1e-12 for i in range(9) for j in range(9))


def test_normalization():
    rng = random.Random(2)
    x = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(12)]
    m = KernelPCA(x, rbf_kernel(0.5), 4)
    for lam, alpha in zip(m.eigenvalues, m.alphas):
        assert abs(lam * sum(a * a for a in alpha) - 1) < 1e-9
        # ||V||^2 = alpha^T K' alpha = 1: the feature-space component is a unit vector
        assert abs(sum(a * sum(r * b for r, b in zip(row, alpha)) for a, row in zip(alpha, m.kc)) - 1) < 1e-9


def test_matches_linear_pca_on_random_data():
    rng = random.Random(3)
    x = [[rng.gauss(0, 1) * (j + 1) for j in range(4)] for _ in range(10)]
    mu, vals, vecs = linear_pca(x)
    m = KernelPCA(x, linear_kernel, 4)
    assert all(abs(a - b) < 1e-9 for a, b in zip(m.feature_variances(), vals))
    tests = [[rng.gauss(0, 2) for _ in range(4)] for _ in range(3)]
    for t, got in zip(tests, m.transform(tests)):
        want = [sum((t[i] - mu[i]) * v[i] for i in range(4)) for v in vecs]
        assert all(abs(abs(g) - abs(w)) < 1e-9 for g, w in zip(got, want))
    for k in range(4):
        got = [row[k] for row in m.training_scores()]
        want = [sum((p[i] - mu[i]) * vecs[k][i] for i in range(4)) for p in x]
        assert close_up_to_sign(got, want, 1e-9)


def test_transform_of_training_points_equals_scores():
    rng = random.Random(4)
    x = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(10)]
    m = KernelPCA(x, polynomial_kernel(3), 3)
    for a, b in zip(m.transform(x), m.training_scores()):
        assert all(abs(s - t) < 1e-8 * (1 + abs(t)) for s, t in zip(a, b))


def test_explicit_feature_map():
    # (x . z)^2 in the plane has the feature map (x1^2, sqrt(2) x1 x2, x2^2)
    rng = random.Random(5)
    x = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(8)]
    phi = [[p[0] ** 2, math.sqrt(2) * p[0] * p[1], p[1] ** 2] for p in x]
    m = KernelPCA(x, polynomial_kernel(2, 0.0), 3)
    _, vals, _ = linear_pca(phi)
    assert all(abs(a - b) < 1e-9 for a, b in zip(m.feature_variances(), vals))


def test_rbf_separates_two_rings():
    pts = []
    for r, off in ((1.0, 0.0), (3.0, 0.2)):
        pts += [(r * math.cos(2 * math.pi * i / 8 + off), r * math.sin(2 * math.pi * i / 8 + off)) for i in range(8)]
    first = [s[0] for s in KernelPCA(pts, rbf_kernel(0.5), 1).training_scores()]
    inner, outer = first[:8], first[8:]
    assert max(inner) - min(inner) < 1e-6 and max(outer) - min(outer) < 1e-6
    assert inner[0] * outer[0] < 0
    # linear PCA cannot: both rings are centered at the origin, so its scores mix them
    lin = [s[0] for s in KernelPCA(pts, linear_kernel, 1).training_scores()]
    assert max(lin[:8]) > min(lin[8:]) and max(lin[8:]) > min(lin[:8])


def test_preimage():
    rng = random.Random(1)
    clean = [(math.cos(2 * math.pi * i / 40), math.sin(2 * math.pi * i / 40)) for i in range(40)]
    noisy = [(x + rng.gauss(0, 0.15), y + rng.gauss(0, 0.15)) for x, y in clean]
    gamma = 0.5
    m = KernelPCA(noisy, rbf_kernel(gamma), 4)
    den = [m.preimage_rbf(s, gamma, p) for s, p in zip(m.training_scores(), noisy)]
    before = sum(abs(math.hypot(*p) - 1) for p in noisy) / 40
    after = sum(abs(math.hypot(*p) - 1) for p in den) / 40
    assert after < 0.6 * before
    # with all components a training point projects onto itself, so it is a fixed point
    full = KernelPCA(noisy[:10], rbf_kernel(gamma), 9)
    z = full.preimage_rbf(full.training_scores()[3], gamma, noisy[3])
    assert math.dist(z, noisy[3]) < 1e-6
