# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uncomputation/. The authors are listed in prov/2V47CD.jsonl.

import math
import random

from qsim import (
    H,
    TOL,
    X,
    apply_1q,
    basis_state,
    inner,
    prob_qubit,
    purity,
    random_state,
    reduced_density_matrix,
    run,
    run_classical,
)
from uncomputation import (
    N_IN,
    OUT,
    WIDTH,
    WORK,
    maj,
    maj_clean_oracle,
    maj_compute,
    maj_garbage_oracle,
    temporary_and_compute,
    temporary_and_uncompute,
    uncompute_template,
)

KEEP = [0, 1, 2, OUT]  # the input and the output; the work qubits are traced out


def work_bits(z: int) -> int:
    return sum(((z >> w) & 1) << i for i, w in enumerate(WORK))


def start_state(out_minus: bool):
    """(1/sqrt 8) sum_x |x>, work qubits |0>, output |0> or |->."""
    psi = basis_state(WIDTH, 0)
    for q in range(N_IN):
        psi = apply_1q(psi, H, q)
    if out_minus:
        psi = apply_1q(apply_1q(psi, X, OUT), H, OUT)
    return psi


def test_clean_oracle_on_every_basis_state() -> None:
    gates = maj_clean_oracle()
    for x in range(8):
        for y in range(2):
            z = run_classical(x | (y << OUT), gates)
            assert z & 7 == x
            assert work_bits(z) == 0
            assert (z >> OUT) & 1 == y ^ maj(x)


def test_garbage_oracle_leaves_values_on_the_work_qubits() -> None:
    gates = maj_garbage_oracle()
    garbage = set()
    for x in range(8):
        z = run_classical(x, gates)
        assert (z >> OUT) & 1 == maj(x)
        garbage.add(work_bits(z))
    assert len(garbage) == 5  # 000, 001, 010, 100 share one value; the other four inputs differ


def test_template_on_random_circuits() -> None:
    """C may change its own wires in any way. After C, a CNOT copy to a fresh wire and C^-1, every wire
    of C is back at its start value, and the fresh wire holds the copied value."""
    rng = random.Random(11)
    for _ in range(40):
        w = rng.randint(2, 6)
        compute = []
        for _ in range(rng.randint(1, 12)):
            kind = rng.choice(["x", "cx", "mcx"])
            if kind == "x":
                compute.append(("x", rng.randrange(w)))
            elif kind == "cx":
                c, t = rng.sample(range(w), 2)
                compute.append(("cx", c, t))
            elif w >= 3:
                c1, c2, t = rng.sample(range(w), 3)
                compute.append(("mcx", (c1, c2), t))
        src = rng.randrange(w)
        gates = uncompute_template(compute, [("cx", src, w)])
        for z in range(1 << w):
            after_c = run_classical(z, compute)
            out = run_classical(z, gates)
            assert out & ((1 << w) - 1) == z
            assert out >> w == (after_c >> src) & 1


def test_phase_with_clean_work_qubits_is_exact() -> None:
    """With the output in |->, the clean oracle gives (1/sqrt 8) sum_x (-1)^maj(x) |x> |0..0> |->."""
    psi = run(start_state(True), maj_clean_oracle())
    minus = [1 / math.sqrt(2), -1 / math.sqrt(2)]
    for z in range(1 << WIDTH):
        x, y = z & 7, (z >> OUT) & 1
        expect = 0j
        if work_bits(z) == 0:
            expect = (-1) ** maj(x) / math.sqrt(8) * minus[y]
        assert abs(psi[z] - expect) <= TOL


def test_garbage_is_entangled_with_the_output() -> None:
    clean = run(start_state(False), maj_clean_oracle())
    dirty = run(start_state(False), maj_garbage_oracle())
    assert abs(purity(reduced_density_matrix(clean, KEEP)) - 1) <= TOL
    # garbage classes: one of 4 inputs and four of 1 input, so the purity is 1/4 + 4/64 = 5/16
    assert abs(purity(reduced_density_matrix(dirty, KEEP)) - 5 / 16) <= TOL


def test_garbage_destroys_interference() -> None:
    """Phase form, then H on the input. maj is balanced, so with clean work qubits the input is never 000.
    With garbage the terms of different garbage values cannot cancel, and 000 has probability 5/16."""
    for gates, expect in ((maj_clean_oracle(), 0.0), (maj_garbage_oracle(), 5 / 16)):
        psi = run(start_state(True), gates)
        for q in range(N_IN):
            psi = apply_1q(psi, H, q)
        p000 = sum(abs(a) ** 2 for z, a in enumerate(psi) if z & 7 == 0)
        assert abs(p000 - expect) <= TOL


def test_measurement_based_uncompute_of_an_and() -> None:
    """Qubits a = 0, b = 1, a third qubit 2 entangled with them, ancilla 3. For both outcomes the state
    after the fix-up equals the start state, and each outcome has probability 1/2."""
    rng = random.Random(5)
    for _ in range(10):
        psi = random_state(3, rng) + [0j] * 8  # qubit 3 (the ancilla) is |0>
        mid = temporary_and_compute(psi, 0, 1, 3)
        anc = apply_1q(mid, H, 3)
        assert abs(prob_qubit(anc, 3, 1) - 0.5) <= TOL
        for outcome in (0, 1):
            back = temporary_and_uncompute(mid, 0, 1, 3, outcome)
            assert abs(abs(inner(psi, back)) - 1) <= TOL
            assert abs(inner(psi, back) - 1) <= TOL  # no phase left at all
