# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qdrift/. The authors are listed in prov/D4KBEW.jsonl.

import itertools
import math
import random

from qdrift import (
    apply_sequence,
    conjugate,
    outer,
    qdrift_bound,
    qdrift_channel,
    qdrift_sequence,
    rotation_matrix,
    samples_for_error,
    trace_distance,
)
from qsim import (
    all_pauli_strings,
    basis_state,
    expm_hermitian,
    expm_taylor,
    inner,
    mat_add,
    mat_mul,
    mat_scale,
    mat_vec,
    max_abs_diff,
    pauli_matrix,
    pauli_sum_apply,
    pauli_sum_matrix,
    random_state,
    trace,
)

CHAIN = [(1.0, "ZZ"), (0.5, "XI"), (0.5, "IX")]


def choi_state(n):
    """The maximally entangled state of an n-qubit system (low qubits) and an n-qubit ancilla (high qubits)."""
    d = 1 << n
    phi = [0j] * (d * d)
    for x in range(d):
        phi[x * d + x] = 1 / math.sqrt(d)
    return outer(phi)


def test_bound_holds_on_basis_random_and_choi_inputs():
    rng = random.Random(31)
    strings = [s for s in all_pauli_strings(2) if s != "II"]
    for _ in range(6):
        terms = [(rng.uniform(-1, 1), s) for s in rng.sample(strings, 3)]
        lam = sum(abs(c) for c, _ in terms)
        t = rng.uniform(0.2, 1.0)
        big_n = rng.choice((4, 8, 16))
        u = expm_hermitian(pauli_sum_matrix(terms), t)
        bound = qdrift_bound(lam, t, big_n)
        for rho in (outer(basis_state(2, rng.randrange(4))), outer(random_state(2, rng))):
            err = trace_distance(qdrift_channel(terms, t, big_n, rho), conjugate(u, rho))
            assert err <= bound
        # with an ancilla: the Choi state gives the largest error for many channels
        ext = [(c, "II" + s) for c, s in terms]
        ue = expm_hermitian(pauli_sum_matrix(ext), t)
        rho = choi_state(2)
        err = trace_distance(qdrift_channel(ext, t, big_n, rho), conjugate(ue, rho))
        assert err <= bound


def test_channel_is_the_average_over_all_sequences():
    terms = [(0.7, "X"), (-0.2, "Z"), (0.4, "Y")]
    lam = sum(abs(c) for c, _ in terms)
    t, big_n = 0.9, 3
    tau = lam * t / big_n
    rho = outer(random_state(1, random.Random(2)))
    avg = [[0j, 0j], [0j, 0j]]
    for picks in itertools.product(range(3), repeat=big_n):
        w = 1.0
        out = rho
        for j in picks:
            c, p = terms[j]
            w *= abs(c) / lam
            out = conjugate(rotation_matrix(p, math.copysign(tau, c)), out)
        avg = mat_add(avg, out, w)
    assert max_abs_diff(avg, qdrift_channel(terms, t, big_n, rho)) < 1e-12
    assert abs(trace(avg) - 1) < 1e-12


def test_error_of_the_channel_falls_as_one_over_n():
    ext = [(c, "II" + s) for c, s in CHAIN]
    t = 0.25
    rho = choi_state(2)
    want = conjugate(expm_hermitian(pauli_sum_matrix(ext), t), rho)
    e40 = trace_distance(qdrift_channel(ext, t, 40, rho), want)
    e80 = trace_distance(qdrift_channel(ext, t, 80, rho), want)
    assert abs(e40 / e80 - 2.0) < 0.05


def test_sampled_average_matches_the_channel():
    # Hoeffding: S samples in [-1, 1] give P(|mean - mu| >= delta) <= 2 exp(-S delta^2 / 2).
    # S = 2000 and delta = 0.1 give a failure chance below 1e-4 for a random seed; the seed is fixed.
    rng = random.Random(2019)
    t, big_n, samples, delta = 0.8, 20, 2000, 0.1
    psi = basis_state(2, 0)
    obs = pauli_matrix("XI")
    total = 0.0
    for _ in range(samples):
        out = apply_sequence(psi, qdrift_sequence(CHAIN, t, big_n, rng))
        total += inner(out, mat_vec(obs, out)).real
    mean = total / samples
    mu = trace(mat_mul(obs, qdrift_channel(CHAIN, t, big_n, outer(psi)))).real
    assert abs(mean - mu) < delta
    # and the channel is close to the exact evolution: |mu - exact| <= 2 * trace distance
    phi = mat_vec(expm_hermitian(pauli_sum_matrix(CHAIN), t), psi)
    exact = inner(phi, mat_vec(obs, phi)).real
    assert abs(mu - exact) <= 2 * qdrift_bound(2.0, t, big_n)


def test_single_sequences_have_larger_error():
    rng = random.Random(7)
    psi = basis_state(2, 0)
    t = 0.5
    phi = mat_vec(expm_hermitian(pauli_sum_matrix(CHAIN), t), psi)
    mean_single = {}
    for big_n in (10, 40):
        ds = []
        for _ in range(200):
            out = apply_sequence(psi, qdrift_sequence(CHAIN, t, big_n, rng))
            ds.append(math.sqrt(max(0.0, 1 - abs(inner(phi, out)) ** 2)))
        mean_single[big_n] = sum(ds) / len(ds)
        channel = trace_distance(qdrift_channel(CHAIN, t, big_n, outer(psi)), outer(phi))
        assert mean_single[big_n] > 2 * channel
    # one sequence drifts like a random walk: error ~ 1 / sqrt(N), so 4 times N halves it
    assert 1.6 < mean_single[10] / mean_single[40] < 2.4


def test_sequence_shape_and_frequencies():
    rng = random.Random(5)
    terms = [(2.0, "ZZI"), (-1.0, "XII"), (0.5, "IXI"), (0.5, "IIX")]
    lam = 4.0
    big_n = 4000
    seq = qdrift_sequence(terms, 1.5, big_n, rng)
    assert len(seq) == big_n
    tau = lam * 1.5 / big_n
    count = {}
    for p, th in seq:
        want_sign = -1 if p == "XII" else 1
        assert th == want_sign * tau
        count[p] = count.get(p, 0) + 1
    # each frequency is within 0.03 of |c_j| / lambda (Hoeffding: failure chance below 2 exp(-7.2))
    for c, p in terms:
        assert abs(count.get(p, 0) / big_n - abs(c) / lam) < 0.03
    # the number of rotations does not depend on the number of terms
    more = terms + [(0.001 * k, "ZII") for k in range(1, 50)]
    assert len(qdrift_sequence(more, 1.5, 100, rng)) == 100


def test_samples_for_error_is_least():
    for lam, t in ((2.0, 1.0), (5.0, 0.3)):
        for eps in (1e-1, 1e-2, 1e-3):
            big_n = samples_for_error(lam, t, eps)
            assert qdrift_bound(lam, t, big_n) <= eps
            assert big_n == 1 or qdrift_bound(lam, t, big_n - 1) > eps
            assert big_n >= math.ceil(2 * lam * lam * t * t / eps)


def test_one_term_is_exact():
    terms = [(-0.6, "XZ")]
    rng = random.Random(1)
    psi = random_state(2, rng)
    out = apply_sequence(psi, qdrift_sequence(terms, 1.1, 7, rng))
    ref = mat_vec(expm_hermitian(pauli_sum_matrix(terms), 1.1), psi)
    assert max(abs(a - b) for a, b in zip(out, ref)) < 1e-12


def test_exact_references_agree():
    h = pauli_sum_matrix([(c, "II" + s) for c, s in CHAIN])
    assert max_abs_diff(expm_hermitian(h, 0.7), expm_taylor(mat_scale(h, -0.7j))) < 1e-12
    psi = random_state(2, random.Random(3))
    hv = pauli_sum_apply(CHAIN, psi)
    assert max(abs(a - b) for a, b in zip(hv, mat_vec(pauli_sum_matrix(CHAIN), psi))) < 1e-12
