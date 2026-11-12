# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-transform/. The authors are listed in prov/56ZDC1.jsonl.

import math
import random

from orthogonal_transform import (
    apply, dct_ii, energy, householder, inverse_apply, is_orthogonal, matmul, unitary_dft, walsh_hadamard,
)

TOL = 1e-9


def quantize(y, step):
    return [math.floor(v / step + 0.5) * step for v in y]


def test_worked_example():
    # The example of the page: 4-point Walsh-Hadamard, quantizer step 2.
    a = walsh_hadamard(4)
    x = [4.0, 2.0, -1.0, 3.0]
    y = apply(a, x)
    assert max(abs(p - q) for p, q in zip(y, [4.0, -1.0, 2.0, 3.0])) < TOL
    assert abs(energy(x) - 30.0) < TOL and abs(energy(y) - 30.0) < TOL
    y_hat = quantize(y, 2.0)
    assert y_hat == [4.0, 0.0, 2.0, 4.0]
    x_hat = inverse_apply(a, y_hat)
    assert max(abs(p - q) for p, q in zip(x_hat, [5.0, 1.0, -1.0, 3.0])) < TOL
    err_y = sum((p - q) ** 2 for p, q in zip(y, y_hat))
    err_x = sum((p - q) ** 2 for p, q in zip(x, x_hat))
    assert abs(err_y - 2.0) < TOL and abs(err_x - 2.0) < TOL


def test_standard_matrices_are_orthogonal():
    for n in [1, 2, 4, 8, 16]:
        assert is_orthogonal(walsh_hadamard(n))
        assert is_orthogonal(dct_ii(n))
        assert is_orthogonal(unitary_dft(n))
    assert is_orthogonal(householder([1.0, 2.0, 3.0]))


def test_non_examples():
    # Unnormalized sum and difference: A^T A = 2 I, not I.
    assert not is_orthogonal([[1.0, 1.0], [1.0, -1.0]])
    # Prediction (difference) matrix: invertible, not orthogonal.
    assert not is_orthogonal([[1.0, 0.0], [-1.0, 1.0]])
    # A non-square matrix is never orthogonal in this sense.
    assert not is_orthogonal([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])


def test_error_grows_for_non_orthogonal():
    # y = (x0, x1 - x0); an error (0.5, 0.5) in y gives (0.5, 1.0) in x.
    inv = [[1.0, 0.0], [1.0, 1.0]]
    e_x = apply(inv, [0.5, 0.5])
    assert e_x == [0.5, 1.0]
    assert abs(energy(e_x) - 1.25) < TOL and abs(energy([0.5, 0.5]) - 0.5) < TOL


def random_orthogonal(rng, n):
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        q = matmul(householder([rng.gauss(0, 1) for _ in range(n)]), q)
    return q


def test_parseval_and_error_identity_random():
    rng = random.Random(7)
    for trial in range(500):
        n = rng.randint(1, 6)
        kind = trial % 4
        if kind == 0:
            a = random_orthogonal(rng, n)
        elif kind == 1:
            a = dct_ii(n)
        elif kind == 2:
            a = unitary_dft(n)
        else:
            m = 1 << rng.randint(0, 3)
            n = m
            a = walsh_hadamard(m)
        assert is_orthogonal(a, 1e-10)
        x = [rng.uniform(-10, 10) for _ in range(n)]
        y = apply(a, x)
        assert abs(energy(y) - energy(x)) < 1e-9 * max(1.0, energy(x))
        back = inverse_apply(a, y)
        assert max(abs(p - q) for p, q in zip(back, x)) < 1e-9
        # Any perturbation of the coefficients gives the same squared error in the signal.
        e = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) if kind == 2 else rng.uniform(-1, 1) for _ in range(n)]
        x2 = inverse_apply(a, [p + q for p, q in zip(y, e)])
        assert abs(energy([p - q for p, q in zip(x2, x)]) - energy(e)) < 1e-9


def test_quantization_error_same_in_both_domains():
    rng = random.Random(11)
    a = dct_ii(8)
    for _ in range(200):
        x = [rng.uniform(-128, 127) for _ in range(8)]
        y = apply(a, x)
        y_hat = quantize(y, rng.choice([1.0, 4.0, 16.0]))
        x_hat = inverse_apply(a, y_hat)
        e1 = sum((p - q) ** 2 for p, q in zip(y, y_hat))
        e2 = sum((p - q) ** 2 for p, q in zip(x, x_hat))
        assert abs(e1 - e2) < 1e-8 * max(1.0, e1)
