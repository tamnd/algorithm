# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-gcd/. The authors are listed in prov/K6XYGK.jsonl.
"""Exhaustive tests of the reversible binary GCD circuit on small registers."""

import math
import random

import pytest

from qsim import get_reg, run, set_reg
from quantum_gcd import classical_rounds, gcd_circuit, gcd_counts, gcd_rounds, make_layout, rounds, run_gcd


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_all_inputs(n):
    gates, L = gcd_circuit(n)
    for u in range(1, 1 << n, 2):
        for v in range(1 << n):
            assert run_gcd(gates, L, u, v) == {"u": u, "v": v, "g": math.gcd(u, v), "ancillas": 0}


def test_random_inputs_eight_bits():
    rng = random.Random(31)
    gates, L = gcd_circuit(8)
    for _ in range(60):
        u = rng.randrange(1, 256, 2)
        v = rng.randrange(256)
        assert run_gcd(gates, L, u, v) == {"u": u, "v": v, "g": math.gcd(u, v), "ancillas": 0}


@pytest.mark.parametrize("n", range(1, 9))
def test_round_bound_is_enough_and_tight(n):
    worst = max(classical_rounds(u, v) for u in range(1, 1 << n, 2) for v in range(1 << n))
    assert worst == rounds(n) == max(1, 2 * n - 1)
    if n >= 2:
        assert classical_rounds((1 << (n - 1)) + 1, 1 << (n - 1)) == 2 * n - 1


def test_forward_part_leaves_gcd_and_zero():
    n = 4
    L = make_layout(n)
    fwd = gcd_rounds(L)
    for u in range(1, 16, 2):
        for v in range(16):
            s = run(fwd, set_reg(set_reg(0, L.u, u), L.v, v))
            assert get_reg(s, L.u) == math.gcd(u, v)
            assert get_reg(s, L.v) == 0  # in some wire order; the value 0 is the same
            assert get_reg(s, L.tmp + [L.d, L.c0]) == 0


def test_superposition_keeps_ancillas_clean():
    # A uniform superposition over all inputs, stored sparsely: the circuit is a permutation of
    # basis states, so each amplitude moves to the image of its basis state.
    n = 3
    gates, L = gcd_circuit(n)
    amp = 1 / math.sqrt(4 * 8)
    state = {set_reg(set_reg(0, L.u, u), L.v, v): amp for u in range(1, 8, 2) for v in range(8)}
    out = {}
    for x, a in state.items():
        y = run(gates, x)
        assert y not in out  # no two inputs collide
        out[y] = a
    assert abs(sum(a * a for a in out.values()) - 1) < 1e-12
    for y in out:
        u, v = get_reg(y, L.u), get_reg(y, L.v)
        assert get_reg(y, L.g) == math.gcd(u, v)
        assert get_reg(y, L.ancillas()) == 0  # the ancillas factor out as |0>, not entangled with u, v


@pytest.mark.parametrize("n", [1, 4, 8])
def test_counts(n):
    c = gcd_counts(n)
    k = rounds(n)
    assert c["larger"] == 0 and c["not"] == 0
    assert c["toffoli"] == 2 * k * (13 * n + 1) == 52 * n * n - 22 * n - 2
    assert c["data_qubits"] == 3 * n
    assert c["ancilla_qubits"] == n + 2 + 2 * k  # 5n when n >= 1


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        classical_rounds(4, 6)
    with pytest.raises(ValueError):
        gcd_circuit(0)
