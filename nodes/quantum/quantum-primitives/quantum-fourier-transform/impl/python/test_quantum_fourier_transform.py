# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-fourier-transform/. The authors are listed in prov/9X30GG.jsonl.

import cmath
import math
import random

from qsim import basis_state, dagger, matmul, matrix_of, norm
from quantum_fourier_transform import (
    aqft_error_bound,
    apply_circuit,
    gate_counts,
    inverse_circuit,
    qft,
    qft_circuit,
)

TOL = 1e-9


def qft_reference(n: int) -> list[list[complex]]:
    """The matrix with entries omega^(jk) / sqrt(N), omega = e^(2 pi i / N)."""
    size = 1 << n
    return [[cmath.exp(2j * math.pi * j * k / size) / math.sqrt(size) for k in range(size)] for j in range(size)]


def max_diff(a, b) -> float:
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_circuit_equals_the_fourier_matrix() -> None:
    for n in range(1, 7):
        got = matrix_of(n, lambda s: qft(s, n))
        assert max_diff(got, qft_reference(n)) < TOL


def test_relation_to_the_classical_dft_matrix() -> None:
    # The classical DFT matrix uses omega = e^(-2 pi i / N), so QFT = conj(F_N) / sqrt(N).
    for n in range(1, 6):
        size = 1 << n
        f = [[cmath.exp(-2j * math.pi * j * k / size) for k in range(size)] for j in range(size)]
        got = matrix_of(n, lambda s: qft(s, n))
        want = [[x.conjugate() / math.sqrt(size) for x in row] for row in f]
        assert max_diff(got, want) < TOL


def test_inverse_and_unitarity() -> None:
    for n in range(1, 6):
        g = qft_circuit(n)
        u = matrix_of(n, lambda s: apply_circuit(s, g))
        v = matrix_of(n, lambda s: apply_circuit(s, inverse_circuit(g)))
        ident = [[1.0 if i == j else 0.0 for j in range(1 << n)] for i in range(1 << n)]
        assert max_diff(matmul(u, v), ident) < TOL
        assert max_diff(matmul(dagger(u), u), ident) < TOL


def test_gate_counts() -> None:
    for n in range(1, 13):
        c = gate_counts(qft_circuit(n))
        assert c == {"h": n, "cr": n * (n - 1) // 2, "swap": n // 2}
        for m in range(1, n + 1):
            # Rotations R_2 .. R_m: the rotation R_k occurs n - k + 1 times.
            want = sum(n - k + 1 for k in range(2, min(m, n) + 1))
            assert gate_counts(qft_circuit(n, m))["cr"] == want
            assert want <= (m - 1) * n


def test_product_form() -> None:
    # QFT|j> = tensor over qubits l of (|0> + e^(2 pi i j / 2^(n - l)) |1>) / sqrt(2).
    rng = random.Random(1)
    for n in range(1, 7):
        for _ in range(5):
            j = rng.randrange(1 << n)
            s = basis_state(n, j)
            qft(s, n)
            for k in range(1 << n):
                want = 1.0 + 0j
                for l in range(n):
                    if (k >> l) & 1:
                        want *= cmath.exp(2j * math.pi * j / 2 ** (n - l))
                want /= math.sqrt(1 << n)
                assert abs(s[k] - want) < TOL


def operator_norm(m: list[list[complex]], rng: random.Random, iters: int = 200) -> float:
    """The largest singular value, by power iteration on M^dagger M (a lower estimate)."""
    size = len(m)
    md = dagger(m)
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(size)]
    for _ in range(iters):
        w = [sum(m[i][j] * v[j] for j in range(size)) for i in range(size)]
        v = [sum(md[i][j] * w[j] for j in range(size)) for i in range(size)]
        nv = norm(v)
        v = [x / nv for x in v]
    w = [sum(m[i][j] * v[j] for j in range(size)) for i in range(size)]
    return norm(w)


def test_approximate_qft_error_is_below_the_bound() -> None:
    rng = random.Random(2)
    for n in range(3, 7):
        exact = qft_reference(n)
        for m in range(1, n):
            approx = matrix_of(n, lambda s: qft(s, n, m))
            diff = [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(approx, exact)]
            bound = aqft_error_bound(n, m)
            # Each column error is at most the operator norm, which is at most the bound.
            col = max(norm([diff[i][j] for i in range(len(diff))]) for j in range(len(diff)))
            op = operator_norm(diff, rng)
            assert col <= op + 1e-6
            assert op <= bound + 1e-9
            assert bound <= 2 * math.pi * n / 2 ** m


def test_periodic_state() -> None:
    # A state with period r = 4 on n = 4 qubits goes to the multiples of N / r = 4.
    n, r = 4, 4
    s = [0j] * 16
    for x in range(1, 16, r):
        s[x] = 0.5
    qft(s, n)
    for k in range(16):
        p = abs(s[k]) ** 2
        assert abs(p - (0.25 if k % 4 == 0 else 0.0)) < TOL
