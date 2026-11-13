# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-state-tomography/. The authors are listed in prov/JWVX4D.jsonl.

import math
import random

from qsim import (
    eigvalsh,
    is_hermitian,
    matmul,
    max_abs_diff,
    outer,
    random_density,
    random_state,
    sub,
    trace,
)
from quantum_state_tomography import (
    all_labels,
    estimate_expectations,
    expectation_from_counts,
    hoeffding_radius,
    linear_inversion,
    log_likelihood,
    maximum_likelihood,
    measure_all,
    outcome_probabilities,
    pauli_matrix,
    project_to_density,
    sample_counts,
    setting_for,
)


def trace_distance(a, b):
    return 0.5 * sum(abs(x) for x in eigvalsh(sub(a, b)))


def frobenius(a, b):
    return math.sqrt(sum(abs(a[i][j] - b[i][j]) ** 2 for i in range(len(a)) for j in range(len(a))))


def is_state(rho, tol=1e-9):
    return is_hermitian(rho, tol) and abs(trace(rho) - 1) < tol and eigvalsh(rho)[0] > -tol


def exact_expectations(rho, n):
    return {label: trace(matmul(pauli_matrix(label), rho)).real for label in all_labels(n)}


def error_bound(n, shots, delta):
    """With probability >= 1 - delta, every one of the 4^n - 1 estimates is within t (union bound).

    Then ||est - rho||_2^2 = 2^-n sum_P (error_P)^2 <= (4^n - 1) t^2 / 2^n,
    and the trace distance is at most (sqrt(2^n) / 2) times the Frobenius distance.
    """
    t = hoeffding_radius(shots, delta / (4**n - 1))
    frob = math.sqrt((4**n - 1) * t * t / 2**n)
    return t, frob, 0.5 * math.sqrt(2**n) * frob


def test_setting_probabilities_match_expectations():
    rng = random.Random(61)
    for n in (1, 2, 3):
        rho = random_density(rng, 2**n)
        for label in all_labels(n):
            probs = outcome_probabilities(rho, setting_for(label))
            assert abs(sum(probs) - 1) < 1e-9
            # exact probabilities, used as counts with weight 1
            mask = sum(1 << q for q, ch in enumerate(label) if ch != "I")
            e = sum(p * (-1) ** bin(i & mask).count("1") for i, p in enumerate(probs))
            assert abs(e - trace(matmul(pauli_matrix(label), rho)).real) < 1e-9


def test_linear_inversion_is_exact_without_noise():
    rng = random.Random(62)
    for n in (1, 2, 3):
        for _ in range(3):
            rho = random_density(rng, 2**n)
            assert max_abs_diff(linear_inversion(exact_expectations(rho, n), n), rho) < 1e-9


def test_sampled_single_qubit_within_hoeffding():
    rng = random.Random(63)
    shots, delta = 20000, 1e-3
    t, frob, tdist = error_bound(1, shots, delta)
    for _ in range(5):
        rho = random_density(rng, 2)
        data = measure_all(rho, 1, shots, rng)
        est = estimate_expectations(data, 1)
        exact = exact_expectations(rho, 1)
        assert all(abs(est[k] - exact[k]) <= t for k in exact)
        lin = linear_inversion(est, 1)
        assert trace_distance(lin, rho) <= tdist
    assert t < 0.03 and tdist < 0.026  # 20000 shots: t = 0.0295 per Bloch component, D <= sqrt(3) t / 2


def test_sampled_two_qubits_and_projection():
    rng = random.Random(64)
    shots, delta = 5000, 1e-3
    t, frob, tdist = error_bound(2, shots, delta)
    psi = random_state(rng, 4)
    rho = outer(psi, psi)  # pure, so noise usually gives a negative eigenvalue
    data = measure_all(rho, 2, shots, rng)
    lin = linear_inversion(estimate_expectations(data, 2), 2)
    assert is_hermitian(lin) and abs(trace(lin) - 1) < 1e-9
    assert eigvalsh(lin)[0] < 0  # not a state
    proj = project_to_density(lin)
    assert is_state(proj)
    assert frobenius(proj, rho) <= frobenius(lin, rho) + 1e-12  # projection onto a convex set
    assert trace_distance(lin, rho) <= tdist and trace_distance(proj, rho) <= tdist


def test_projection_qubit_closed_form():
    # For a qubit, the closest state to (I + r.sigma)/2 with |r| > 1 is (I + r/|r| . sigma)/2.
    rng = random.Random(65)
    for _ in range(50):
        r = [rng.gauss(0, 1) for _ in range(3)]
        norm = math.sqrt(sum(x * x for x in r))
        r = [x * (1.0 + 2 * rng.random()) / norm for x in r]  # length between 1 and 3
        a = linear_inversion({"I": 1.0, "X": r[0], "Y": r[1], "Z": r[2]}, 1)
        unit = [x / math.sqrt(sum(y * y for y in r)) for x in r]
        expected = linear_inversion({"I": 1.0, "X": unit[0], "Y": unit[1], "Z": unit[2]}, 1)
        assert max_abs_diff(project_to_density(a), expected) < 1e-9
    good = random_density(rng, 4)
    assert max_abs_diff(project_to_density(good), good) < 1e-9


def test_maximum_likelihood():
    rng = random.Random(66)
    shots = 3000
    psi = random_state(rng, 4)
    rho = outer(psi, psi)
    data = measure_all(rho, 2, shots, rng)
    mle = maximum_likelihood(data, 2, iterations=300)
    assert is_state(mle, tol=1e-8)
    proj = project_to_density(linear_inversion(estimate_expectations(data, 2), 2))
    assert log_likelihood(data, mle) >= log_likelihood(data, proj) - 1e-6
    assert trace_distance(mle, rho) <= error_bound(2, shots, 1e-3)[2]


def test_error_shrinks_like_one_over_root_shots():
    rng = random.Random(67)
    rho = random_density(rng, 2)
    errs = {}
    for shots in (500, 32000):
        total = 0.0
        for _ in range(8):
            data = measure_all(rho, 1, shots, rng)
            total += trace_distance(linear_inversion(estimate_expectations(data, 1), 1), rho)
        errs[shots] = total / 8
    ratio = errs[500] / errs[32000]  # sqrt(64) = 8 in expectation
    assert 4 < ratio < 16


def test_counts_of_a_basis_state():
    rng = random.Random(68)
    counts = sample_counts([[1, 0], [0, 0]], "Z", 1000, rng)
    assert counts == [1000, 0]
    assert expectation_from_counts("Z", counts) == 1.0
    counts = sample_counts([[1, 0], [0, 0]], "X", 4000, rng)
    assert abs(expectation_from_counts("X", counts)) <= hoeffding_radius(4000, 1e-6)
