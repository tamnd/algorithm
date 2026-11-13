# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-modular-exponentiation/. The authors are listed in prov/S5NABE.jsonl.
"""Exhaustive tests of the modular arithmetic circuits on small moduli.

Every circuit is run on basis states, which is enough: the circuits are
permutations of basis states, so they act linearly on superpositions.
"""

import math
import random

import pytest

from qsim import get_reg, run, set_reg
from quantum_modular_exponentiation import (
    controlled_mult_inplace,
    controlled_multiplier,
    make_layout,
    modexp_circuit,
    modexp_counts,
    modular_adder,
    run_modexp,
)


def state(L, x=0, y=0, b=0):
    return set_reg(set_reg(set_reg(0, L.x, x), L.y, y), L.b, b)


def units(N):
    return [a for a in range(1, N) if math.gcd(a, N) == 1]


@pytest.mark.parametrize("N", range(3, 20))
def test_modular_adder_all_inputs(N):
    L = make_layout(N, 2)
    c1, c2 = L.x
    for k in range(N):
        g = modular_adder(k, N, L, (c1, c2))
        for ctl in range(4):
            for b in range(N):
                out = run(g, state(L, x=ctl, b=b))
                want = (b + k) % N if ctl == 3 else b
                assert out == state(L, x=ctl, b=want)  # ancillas and controls unchanged


@pytest.mark.parametrize("N", [5, 9, 15, 21])
def test_multiplier_all_inputs(N):
    L = make_layout(N, 1)
    for a in range(N):
        g = controlled_multiplier(a, N, L, L.x[0])
        for ctl in (0, 1):
            for y in range(N):
                for b in (0, (3 * y + 1) % N):
                    out = run(g, state(L, x=ctl, y=y, b=b))
                    want = (b + a * y) % N if ctl else b
                    assert out == state(L, x=ctl, y=y, b=want)


@pytest.mark.parametrize("N", [7, 15, 21, 35])
def test_in_place_multiplier_all_inputs(N):
    L = make_layout(N, 1)
    for a in units(N):
        g = controlled_mult_inplace(a, N, L, L.x[0])
        for ctl in (0, 1):
            for y in range(N):
                out = run(g, state(L, x=ctl, y=y))
                want = a * y % N if ctl else y
                assert out == state(L, x=ctl, y=want)  # b, tmp, c0 and anc are back to 0


@pytest.mark.parametrize("N,t", [(15, 4), (21, 4), (35, 3)])
def test_modexp_all_exponents(N, t):
    for a in units(N)[:6]:
        g, L = modexp_circuit(a, N, t)
        for x in range(1 << t):
            for y in (1, N - 1):
                assert run_modexp(g, L, x, y) == {"x": x, "y": y * pow(a, x, N) % N, "ancillas": 0}


def test_modexp_full_exponent_register():
    rng = random.Random(2024)
    for N, a in [(15, 7), (21, 2)]:
        t = (N * N - 1).bit_length()  # the register size of order finding
        g, L = modexp_circuit(a, N, t)
        for x in [0, 1, (1 << t) - 1] + [rng.randrange(1 << t) for _ in range(12)]:
            assert run_modexp(g, L, x, 1) == {"x": x, "y": pow(a, x, N), "ancillas": 0}


@pytest.mark.parametrize("N,a,t", [(15, 7, 4), (21, 2, 4), (35, 3, 3), (15, 2, 8)])
def test_gate_and_qubit_counts(N, a, t):
    n = N.bit_length()
    counts = modexp_counts(a, N, t)
    assert counts["larger"] == 0  # only NOT, CNOT and Toffoli gates
    assert counts["data_qubits"] == t + n
    assert counts["ancilla_qubits"] == 2 * n + 4
    # Toffolis: each MODADD(k) has 5 adders of 2(n+1) Toffolis and 6 popcount(k) loads,
    # each CU has 2n MODADDs and n Fredkin gates.
    pop = 0
    c = a % N
    for _ in range(t):
        for m in (c, pow(c, -1, N)):
            pop += sum(bin((m << i) % N).count("1") for i in range(n))
        c = c * c % N
    assert counts["toffoli"] == t * (20 * n * n + 21 * n) + 6 * pop


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        modexp_circuit(6, 15, 4)
    with pytest.raises(ValueError):
        modexp_circuit(1, 2, 2)
