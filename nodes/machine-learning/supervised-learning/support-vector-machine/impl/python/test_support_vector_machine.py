# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-vector-machine/. The authors are listed in prov/3V5V6X.jsonl.

import math
import random

from support_vector_machine import SVM, gaussian_kernel, linear_kernel


def blobs(seed, n, spread):
    rng = random.Random(seed)
    xs, ys = [], []
    for i in range(n):
        y = 1 if i % 2 == 0 else -1
        xs.append((y + rng.gauss(0, spread), y + rng.gauss(0, spread)))
        ys.append(y)
    return xs, ys


def test_hard_margin_on_separable_data() -> None:
    xs = [(2, 0), (0, 2), (3, 3), (-1, 0), (0, -1), (-2, -2)]
    ys = [1, 1, 1, -1, -1, -1]
    m = SVM(linear_kernel, c=1e6, eps=1e-10).fit(xs, ys)
    w = m.weight_vector()
    assert abs(w[0] - 2 / 3) < 1e-7 and abs(w[1] - 2 / 3) < 1e-7 and abs(m.b + 1 / 3) < 1e-7
    assert abs(2 / math.hypot(*w) - 3 / math.sqrt(2)) < 1e-7  # margin 2/|w|
    # Every support vector lies on the margin (the dual is degenerate here, so
    # not every margin point needs a positive multiplier).
    assert set(m.sv) <= {0, 1, 3, 4}
    assert m.sv and all(abs(ys[i] * m.decision(xs[i]) - 1) < 1e-7 for i in m.sv)
    for x, y in zip(xs, ys):
        assert y * m.decision(x) >= 1 - 1e-7


def test_kkt_and_zero_duality_gap() -> None:
    for seed in range(5):
        for spread in (0.6, 1.5):
            xs, ys = blobs(seed, 40, spread)
            for k in (linear_kernel, gaussian_kernel(1.0)):
                for c in (0.1, 1.0, 10.0):
                    m = SVM(k, c, eps=1e-6).fit(xs, ys)
                    assert all(0 <= a <= c for a in m.alpha)
                    assert m.kkt_violation() < 1e-5
                    gap = m.primal_objective() - m.dual_objective()
                    assert -1e-7 <= gap < 1e-4 * (1 + abs(m.primal_objective()))


def test_role_of_c() -> None:
    xs, ys = blobs(7, 60, 1.2)
    norms, errors = [], []
    for c in (0.01, 0.1, 1.0, 10.0, 100.0):
        m = SVM(linear_kernel, c).fit(xs, ys)
        norms.append(m.norm_w_squared())
        errors.append(sum(1 for x, y in zip(xs, ys) if y * m.decision(x) < 1))  # margin errors
    assert all(n1 <= n2 + 1e-9 for n1, n2 in zip(norms, norms[1:]))  # larger C, narrower margin
    assert errors[0] >= errors[-1]


def test_xor_with_a_gaussian_kernel() -> None:
    xs = [(0, 0), (1, 1), (0, 1), (1, 0)]
    ys = [-1, -1, 1, 1]
    lin = SVM(linear_kernel, 10.0).fit(xs, ys)
    assert any(lin.predict(x) != y for x, y in zip(xs, ys))
    m = SVM(gaussian_kernel(0.7), 10.0).fit(xs, ys)
    assert [m.predict(x) for x in xs] == ys
    assert len(m.sv) == 4


def test_support_vectors_and_box() -> None:
    xs, ys = blobs(3, 50, 1.5)
    c = 1.0
    m = SVM(linear_kernel, c).fit(xs, ys)
    for i, (x, y) in enumerate(zip(xs, ys)):
        margin = y * m.decision(x)
        if m.alpha[i] == 0:
            assert margin >= 1 - 1e-5
        elif m.alpha[i] == c:
            assert margin <= 1 + 1e-5
        else:
            assert abs(margin - 1) < 1e-5
