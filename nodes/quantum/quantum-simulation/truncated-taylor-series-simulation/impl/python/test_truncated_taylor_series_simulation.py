# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-taylor-series-simulation/. The authors are listed in prov/6TQGRV.jsonl.

import math
import random

from qsim import (
    add,
    dagger,
    expm_hermitian,
    identity,
    matmul,
    matvec,
    max_abs_diff,
    norm,
    pauli_sum_matrix,
    random_state,
    scale,
)
from truncated_taylor_series_simulation import (
    error_bound,
    order_for,
    pad_to_two,
    prep_matrix,
    segment,
    segments,
    tail,
    taylor_lcu,
    taylor_simulate,
)

EXAMPLE = [(0.6, "X"), (-0.8, "Z")]


def random_terms(rng, n, big_l):
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice("IXYZ") for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def truncated_series(h, tau, big_k):
    d = len(h)
    out, power = identity(d), identity(d)
    for k in range(1, big_k + 1):
        power = scale(-1j * tau / k, matmul(power, h))
        out = add(out, power)
    return out


def test_segments_keep_the_one_norm_at_most_two():
    for lam, t in [(1.4, 2.0), (1.0, math.log(2) * 3), (3.7, 0.1), (0.2, 50.0)]:
        r, tau = segments(lam, t)
        assert r == max(1, math.ceil(lam * t / math.log(2) - 1e-12))
        assert lam * tau <= math.log(2) + 1e-12 and abs(r * tau - t) < 1e-12
    assert segments(1.4, 2.0) == (5, 0.4)


def test_the_lcu_is_the_truncated_taylor_series():
    rng = random.Random(61)
    terms = random_terms(rng, 2, 3)
    h = pauli_sum_matrix(terms)
    lam = sum(abs(c) for c, _ in terms)
    tau = math.log(2) / lam
    for big_k in range(4):
        betas, unitaries = taylor_lcu(terms, tau, big_k)
        assert len(betas) == sum(3 ** k for k in range(big_k + 1)) and min(betas) > 0
        assert abs(sum(betas) - sum((lam * tau) ** k / math.factorial(k) for k in range(big_k + 1))) < 1e-12
        v = [[0j] * 4 for _ in range(4)]
        for beta, u in zip(betas, unitaries):
            v = add(v, scale(beta, u))
        assert max_abs_diff(v, truncated_series(h, tau, big_k)) < 1e-12


def test_one_segment_applies_the_oblivious_amplification_polynomial():
    # The index-0 part of -W R W^dagger R W |0>|psi> is (3/2 V - 1/2 V V^dagger V)|psi> for s = 2 (eq. (14)).
    rng = random.Random(62)
    terms = random_terms(rng, 2, 3)
    h = pauli_sum_matrix(terms)
    lam = sum(abs(c) for c, _ in terms)
    r, tau = segments(lam, 1.0)
    for big_k in [1, 2, 3]:
        betas, unitaries = pad_to_two(*taylor_lcu(terms, tau, big_k))
        assert abs(sum(betas) - 2) < 1e-12
        v = truncated_series(h, tau, big_k)
        a = add(scale(1.5, v), scale(-0.5, matmul(v, matmul(dagger(v), v))))
        b = prep_matrix(betas)
        psi = random_state(2, rng)
        good, p = segment(b, unitaries, psi)
        assert max(abs(x - y) for x, y in zip(good, matvec(a, psi))) < 1e-12
        assert abs(p - norm(matvec(a, psi)) ** 2) < 1e-12


def test_the_error_is_below_its_bound_and_falls_with_the_order():
    h = pauli_sum_matrix(EXAMPLE)
    psi = [1 + 0j, 0j]
    exact = matvec(expm_hermitian(h, 2.0), psi)
    errors = []
    for big_k in range(1, 6):
        out, prob, r = taylor_simulate(EXAMPLE, 2.0, big_k, psi)
        err = norm([x - y for x, y in zip(out, exact)])
        assert r == 5 and err <= error_bound(1.4, 2.0, big_k)
        # prob is the squared norm of the output, so it is at least (1 - bound)^2 when the bound is below 1.
        assert abs(prob - norm(out) ** 2) < 1e-12
        assert prob >= max(0.0, 1 - error_bound(1.4, 2.0, big_k)) ** 2
        errors.append(err)
    assert errors[-1] < 1e-5 and errors[-1] < errors[0] / 1e3
    assert abs(errors[2] - 0.0016760645616600) < 1e-9


def test_random_hamiltonians_on_two_qubits():
    rng = random.Random(63)
    for _ in range(3):
        terms = random_terms(rng, 2, 3)
        h = pauli_sum_matrix(terms)
        lam = sum(abs(c) for c, _ in terms)
        t = rng.uniform(0.5, 2.0)
        psi = random_state(2, rng)
        exact = matvec(expm_hermitian(h, t), psi)
        out, prob, r = taylor_simulate(terms, t, 3, psi)
        err = norm([x - y for x, y in zip(out, exact)])
        assert err <= error_bound(lam, t, 3) and abs(prob - 1) < 0.02


def test_the_order_grows_slowly_with_time_and_precision():
    assert abs(tail(math.log(2), 3) - 0.0111222) < 1e-6
    ks = [order_for(1.4, t, 1e-3) for t in [2, 10, 100, 1000]]
    assert ks == [5, 6, 7, 8]
    assert order_for(1.4, 100, 1e-9) > order_for(1.4, 100, 1e-3)
