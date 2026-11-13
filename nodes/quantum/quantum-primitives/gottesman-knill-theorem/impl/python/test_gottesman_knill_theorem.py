# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gottesman-knill-theorem/. The authors are listed in prov/V5TKK8.jsonl.

import math
import random

from gottesman_knill_theorem import Tableau, simulate
from qsim import H, S, apply_1q, apply_cnot, apply_pauli, basis_state, close, inner


def sv_gate(state, g):
    if g[0] == "H":
        return apply_1q(state, H, g[1])
    if g[0] == "S":
        return apply_1q(state, S, g[1])
    return apply_cnot(state, g[1], g[2])


def p_one(state, q):
    return sum(abs(a) ** 2 for x, a in enumerate(state) if (x >> q) & 1)


def project(state, q, b):
    """The normalized state after outcome b on qubit q."""
    kept = [a if ((x >> q) & 1) == b else 0j for x, a in enumerate(state)]
    s = math.sqrt(sum(abs(a) ** 2 for a in kept))
    return [a / s for a in kept]


def random_gate(rng, n):
    k = rng.randrange(3) if n > 1 else rng.randrange(2)
    q = rng.randrange(n)
    if k == 0:
        return ("H", q)
    if k == 1:
        return ("S", q)
    t = rng.choice([j for j in range(n) if j != q])
    return ("CNOT", q, t)


def assert_tableau_matches(t, state):
    """Every stabilizer row fixes the state, and the rows have the right commutation pattern."""
    for sign, word in t.stabilizers():
        assert close([sign * a for a in apply_pauli(state, word)], state, 1e-9)
    n = t.n
    for i in range(2 * n):
        for j in range(2 * n):
            sym = bin((t.x[i] & t.z[j]) ^ (t.z[i] & t.x[j])).count("1") % 2
            # destabilizer i anticommutes only with stabilizer i; all other pairs commute
            assert sym == (1 if abs(i - j) == n else 0)


def test_bell_and_ghz() -> None:
    t = Tableau(2)
    t.h(1)
    t.cnot(1, 0)
    assert sorted(t.stabilizers()) == [(1, "XX"), (1, "ZZ")]
    t = Tableau(3)
    t.h(2)
    t.cnot(2, 1)
    t.cnot(1, 0)
    rng = random.Random(1)
    b, det = t.measure(2, rng)
    assert not det
    assert t.measure(1, rng) == (b, True) and t.measure(0, rng) == (b, True)


def test_signs_of_single_gates() -> None:
    t = Tableau(1)
    t.h(0)
    t.s(0)
    assert t.stabilizers() == [(1, "Y")]  # S H |0> = (|0> + i|1>)/sqrt 2
    t.s(0)
    assert t.stabilizers() == [(-1, "X")]  # S^2 H |0> = Z|+> = |->
    t.h(0)
    assert t.stabilizers() == [(-1, "Z")]  # H|-> = |1>
    assert t.measure(0) == (1, True)


def test_random_circuits_against_state_vector() -> None:
    rng = random.Random(7071)
    for n in (1, 2, 3, 4):
        for _ in range(60):
            t = Tableau(n)
            state = basis_state(n, 0)
            for _ in range(rng.randrange(1, 40)):
                g = random_gate(rng, n)
                t.apply(g)
                state = sv_gate(state, g)
            assert_tableau_matches(t, state)
            # measure every qubit in a random order; compare probabilities, then collapse both
            for q in rng.sample(range(n), n):
                p = p_one(state, q)
                b, det = t.measure(q, rng)
                if det:
                    assert abs(p - b) < 1e-9
                else:
                    assert abs(p - 0.5) < 1e-9
                state = project(state, q, b)
                assert_tableau_matches(t, state)


def test_mid_circuit_measurement() -> None:
    rng = random.Random(7072)
    n = 4
    for _ in range(40):
        t = Tableau(n)
        state = basis_state(n, 0)
        for _ in range(50):
            if rng.random() < 0.15:
                q = rng.randrange(n)
                p = p_one(state, q)
                b, det = t.measure(q, rng)
                assert (abs(p - b) < 1e-9) if det else (abs(p - 0.5) < 1e-9)
                state = project(state, q, b)
            else:
                g = random_gate(rng, n)
                t.apply(g)
                state = sv_gate(state, g)
            assert_tableau_matches(t, state)


def branches(t, qs):
    """All outcome strings of measuring the qubits qs in order, with their exact probabilities."""
    if not qs:
        return {(): 1.0}
    out = {}
    first = t.copy()
    if first.is_deterministic(qs[0]):
        b, _ = first.measure(qs[0])
        for rest, p in branches(first, qs[1:]).items():
            out[(b,) + rest] = p
        return out
    for b in (0, 1):
        u = t.copy()
        u.measure(qs[0], forced=b)
        for rest, p in branches(u, qs[1:]).items():
            out[(b,) + rest] = p / 2
    return out


def test_exact_output_distribution() -> None:
    rng = random.Random(7073)
    for n in (2, 3, 4):
        for _ in range(30):
            t = Tableau(n)
            state = basis_state(n, 0)
            for _ in range(30):
                g = random_gate(rng, n)
                t.apply(g)
                state = sv_gate(state, g)
            dist = branches(t, list(range(n)))
            probs = [abs(a) ** 2 for a in state]
            for x in range(1 << n):
                key = tuple((x >> q) & 1 for q in range(n))
                assert abs(dist.get(key, 0.0) - probs[x]) < 1e-9
            # the output distribution is uniform on its support, of size a power of two
            support = [x for x in range(1 << n) if probs[x] > 1e-12]
            assert len(support) & (len(support) - 1) == 0


def test_global_phase_is_not_tracked_but_states_agree() -> None:
    # H S S H = H Z H = X, so |0> goes to |1>; the tableau sees -Z
    t = Tableau(1)
    for g in [("H", 0), ("S", 0), ("S", 0), ("H", 0)]:
        t.apply(g)
    assert t.stabilizers() == [(-1, "Z")]
    state = basis_state(1, 0)
    for g in [("H", 0), ("S", 0), ("S", 0), ("H", 0)]:
        state = sv_gate(state, g)
    assert abs(abs(inner(basis_state(1, 1), state)) - 1) < 1e-12


def test_large_ghz_is_fast() -> None:
    # 300 qubits: a state vector would need 2^300 amplitudes; the tableau needs 600 rows
    n = 300
    circuit = [("H", n - 1)] + [("CNOT", q + 1, q) for q in range(n - 2, -1, -1)] + [("M", q) for q in range(n)]
    for seed in (1, 2):
        out = simulate(n, circuit, random.Random(seed))
        assert len(set(out)) == 1


def test_rejects_non_clifford_gate() -> None:
    t = Tableau(1)
    try:
        t.apply(("T", 0))
    except ValueError:
        return
    raise AssertionError("T was accepted")
