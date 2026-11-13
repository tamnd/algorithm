# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-modular-inversion/. The authors are listed in prov/JXGTEC.jsonl.
"""Exhaustive tests of the reversible modular inversion circuit on small odd moduli."""

import math
import random

import pytest

from qsim import get_reg, run, set_reg
from quantum_modular_inversion import (
    halve_mod,
    inversion_circuit,
    inversion_counts,
    make_layout,
    mod_add_reg,
    rounds,
    run_inversion,
)


@pytest.mark.parametrize("N", range(3, 34, 2))
def test_all_inputs(N):
    gates, L = inversion_circuit(N)
    for x in range(N):
        r = run_inversion(gates, L, x)
        assert r["x"] == x and r["ancillas"] == 0
        if math.gcd(x, N) == 1:
            assert r["out"] == pow(x, -1, N)
        else:  # the coefficient A of the extended GCD: A x = gcd(x, N) mod N
            assert r["out"] < N and (r["out"] * x - math.gcd(x, N)) % N == 0


def test_random_inputs_larger_moduli():
    rng = random.Random(77)
    for N in (127, 251):  # primes, so every x > 0 is a unit
        gates, L = inversion_circuit(N)
        for _ in range(6):
            x = rng.randrange(1, N)
            assert run_inversion(gates, L, x) == {"x": x, "out": pow(x, -1, N), "ancillas": 0}


@pytest.mark.parametrize("N", [3, 9, 15, 21])
def test_modular_subtraction_all_inputs(N):
    L = make_layout(N)
    g = mod_add_reg(L.tmp, L.B, N, L)
    sub = list(reversed(g))
    for a in range(N):
        for b in range(N):
            s = set_reg(set_reg(0, L.tmp, a), L.B, b)
            assert run(g, s) == set_reg(set_reg(0, L.tmp, a), L.B, (a + b) % N)
            assert run(sub, s) == set_reg(set_reg(0, L.tmp, a), L.B, (b - a) % N)


@pytest.mark.parametrize("N", [3, 9, 15, 21, 33])
def test_modular_halving_all_inputs(N):
    L = make_layout(N)
    g, wires = halve_mod(list(L.B), N, L)
    half = pow(2, -1, N)
    for b in range(N):
        s = run(g, set_reg(0, L.B, b))
        assert get_reg(s, wires) == b * half % N
        assert s == set_reg(0, wires, b * half % N)  # p, cst and the carry are back to 0


def test_superposition_keeps_ancillas_clean():
    N = 15
    gates, L = inversion_circuit(N)
    xs = [x for x in range(N) if math.gcd(x, N) == 1]
    amp = 1 / math.sqrt(len(xs))
    out = {}
    for x in xs:
        y = run(gates, set_reg(0, L.x, x))
        assert y not in out
        out[y] = amp
    assert abs(sum(a * a for a in out.values()) - 1) < 1e-12
    for y in out:
        x = get_reg(y, L.x)
        assert get_reg(y, L.out) == pow(x, -1, N)
        assert get_reg(y, L.ancillas()) == 0


@pytest.mark.parametrize("N", [3, 15, 31, 251])
def test_counts(N):
    n = N.bit_length()
    c = inversion_counts(N)
    assert c["larger"] == 0
    assert c["toffoli"] == 2 * rounds(n) * (32 * n + 20)
    assert c["data_qubits"] == 2 * n
    assert c["ancilla_qubits"] == 9 * n + 6


def test_rejects_bad_modulus():
    for N in (1, 2, 16):
        with pytest.raises(ValueError):
            inversion_circuit(N)
