# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-combination-of-unitaries/. The authors are listed in prov/XGJBQG.jsonl.

import cmath
import math
import random

from linear_combination_of_unitaries import apply_w, implement_exactly, lcu_oaa, pad_to, prep_matrix, rounds_for
from qsim import (
    add,
    basis_state,
    dagger,
    matmul,
    matvec,
    max_abs_diff,
    norm,
    pauli_matrix,
    random_state,
    random_unitary,
    scale,
    trace,
)

TOL = 1e-10


def pauli_expansion(v):
    """V = sum_P c_P P with c_P = Tr(P V)/2^n, as positive weights |c_P| and unitaries e^(i arg c_P) P."""
    n = len(v).bit_length() - 1
    strings = [""]
    for _ in range(n):
        strings = [s + ch for s in strings for ch in "IXYZ"]
    betas, us = [], []
    for s in strings:
        p = pauli_matrix(s)
        c = trace(matmul(p, v)) / len(v)
        if abs(c) > 1e-14:
            betas.append(abs(c))
            us.append(scale(cmath.exp(1j * cmath.phase(c)), p))
    return betas, us


def block_of_w(betas, us):
    """The matrix <0| W |0> on the system, column by column."""
    d = len(us[0])
    b = prep_matrix(betas)
    cols = []
    for x in range(d):
        parts = [basis_state(d.bit_length() - 1, x)] + [[0j] * d for _ in range(len(b) - 1)]
        cols.append(apply_w(b, us, parts)[0])
    return [[cols[x][y] for x in range(d)] for y in range(d)]


def test_block_of_w_is_the_sum_over_s():
    rng = random.Random(21)
    for d, m in [(2, 3), (4, 5)]:
        us = [random_unitary(d, rng) for _ in range(m)]
        betas = [rng.uniform(0.1, 1) for _ in range(m)]
        s = sum(betas)
        target = [[0j] * d for _ in range(d)]
        for b, u in zip(betas, us):
            target = add(target, scale(b / s, u))
        assert max_abs_diff(block_of_w(betas, us), target) < TOL


def test_hand_example_rotation_needs_padding():
    # V = cos(pi/6) I - i sin(pi/6) X as the sum of I and -iX with weights 0.866 and 0.5.
    th = math.pi / 6
    eye, x = pauli_matrix("I"), pauli_matrix("X")
    betas, us = [math.cos(th), math.sin(th)], [eye, scale(-1j, x)]
    s = sum(betas)
    assert abs(s - 1.3660254037844386) < 1e-12
    psi = basis_state(1, 0)
    _, p_before = lcu_oaa(betas, us, psi, 0)
    _, p_one_round = lcu_oaa(betas, us, psi, 1)
    assert abs(p_before - 1 / s ** 2) < TOL  # 0.5359
    assert abs(p_one_round - math.sin(3 * math.asin(1 / s)) ** 2) < TOL  # 0.3930: one round overshoots
    out, p, rounds = implement_exactly(betas, us, psi)
    assert rounds == 1 and abs(p - 1) < TOL
    v = add(scale(math.cos(th), eye), scale(-1j * math.sin(th), x))
    assert max(abs(a - b) for a, b in zip(out, matvec(v, psi))) < TOL


def test_success_probability_after_l_rounds():
    rng = random.Random(22)
    v = random_unitary(4, rng)
    betas, us = pauli_expansion(v)
    s = sum(betas)
    theta = math.asin(1 / s)
    for rounds in range(4):
        psi = random_state(2, rng)
        parts, p0 = lcu_oaa(betas, us, psi, rounds)
        assert abs(p0 - math.sin((2 * rounds + 1) * theta) ** 2) < TOL
        # The good part is sin((2l + 1) theta) V|psi>: the same direction for every number of rounds.
        vpsi = matvec(v, psi)
        amp = math.sin((2 * rounds + 1) * theta)
        assert max(abs(a - amp * b) for a, b in zip(parts[0], vpsi)) < TOL


def test_padding_makes_amplification_exact_for_random_unitaries():
    rng = random.Random(23)
    for d in [2, 4, 4]:
        v = random_unitary(d, rng)
        betas, us = pauli_expansion(v)
        rounds, s_target = rounds_for(sum(betas))
        bp, up = pad_to(betas, us, s_target)
        assert abs(sum(bp) - s_target) < 1e-12
        for _ in range(3):  # oblivious: the same circuit works for every input state
            psi = random_state(d.bit_length() - 1, rng)
            out, p, r = implement_exactly(betas, us, psi)
            assert r == rounds and abs(p - 1) < TOL
            assert max(abs(a - b) for a, b in zip(out, matvec(v, psi))) < TOL


def test_one_round_on_a_non_unitary_block_gives_3a_minus_4aaa():
    # For any block A = <0|W|0>, one round gives 3A - 4 A A^dagger A (the identity behind robust amplification).
    rng = random.Random(24)
    us = [random_unitary(2, rng) for _ in range(3)]
    betas = [0.7, 0.9, 0.4]
    a = block_of_w(betas, us)
    target = add(scale(3, a), scale(-4, matmul(a, matmul(dagger(a), a))))
    b = prep_matrix(betas)
    for x in range(2):
        psi = basis_state(1, x)
        parts, _ = lcu_oaa(betas, us, psi, 1)
        col = [target[y][x] for y in range(2)]
        assert max(abs(p - q) for p, q in zip(parts[0], col)) < TOL
    assert len(b) == 4


def test_rounds_for_thresholds():
    assert rounds_for(1.0) == (0, 1.0)
    r, s = rounds_for(1.5)
    assert r == 1 and abs(s - 2) < 1e-12
    r, s = rounds_for(3.0)
    assert r == 2 and abs(s - 1 / math.sin(math.pi / 10)) < 1e-12
    assert norm([3, 4]) == 5
