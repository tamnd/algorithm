# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-oracle/. The authors are listed in prov/KDN9PQ.jsonl.

import random

from qsim import (
    H,
    TOL,
    apply_1q,
    basis_state,
    inner,
    is_unitary,
    max_abs_diff,
    probabilities,
    random_state,
    unitary_of,
)
from quantum_oracle import (
    all_functions,
    bit_from_controlled_phase_oracle,
    bit_oracle,
    bit_oracle_from_in_place,
    bit_oracle_perm,
    controlled_phase_oracle,
    in_place_oracle,
    inner_phase_oracle,
    phase_from_bit_oracle,
    phase_oracle,
)


def close(u, v) -> bool:
    return max(abs(a - b) for a, b in zip(u, v)) <= TOL


def boolean_tables():
    """All 16 Boolean functions on 2 bits, then 30 random ones on 3 and 4 bits (seed 3)."""
    rng = random.Random(3)
    tables = [(2, f) for f in all_functions(2, 1)]
    for n in (3, 4):
        tables += [(n, [rng.randrange(2) for _ in range(1 << n)]) for _ in range(15)]
    return tables


def test_bit_oracle_on_every_basis_state() -> None:
    for n, m in ((1, 1), (2, 1), (2, 2), (3, 2)):
        for f in all_functions(n, m) if n + m <= 4 else [[(5 * x + 1) % 4 for x in range(8)]]:
            perm = bit_oracle_perm(f, n, m)
            for x in range(1 << n):
                for y in range(1 << m):
                    assert perm[(x << m) | y] == (x << m) | (y ^ f[x])
            assert sorted(perm) == list(range(1 << (n + m)))       # a bijection for every f
            assert all(perm[perm[z]] == z for z in range(len(perm)))  # its own inverse


def test_bit_oracle_with_minus_gives_the_phase_oracle() -> None:
    """Phase kickback: on every basis state |x> and on random states, one bit query with |-> equals
    one phase query, and the output qubit stays |->."""
    rng = random.Random(4)
    for n, f in boolean_tables():
        for x in range(1 << n):
            out = phase_from_bit_oracle(basis_state(n, x), f, n)
            assert close(out, [(-1) ** f[x] * a for a in basis_state(n, x)])
        psi = random_state(n, rng)
        assert close(phase_from_bit_oracle(psi, f, n), phase_oracle(psi, f))


def test_controlled_phase_oracle_gives_the_bit_oracle() -> None:
    for n, f in boolean_tables():
        for z in range(1 << (n + 1)):
            e = basis_state(n + 1, z)
            assert close(bit_from_controlled_phase_oracle(e, f), bit_oracle(e, f, n, 1))


def test_uncontrolled_phase_oracle_cannot_tell_f_from_its_negation() -> None:
    """O_(1-f) = -O_f, a global phase: every measurement after any circuit has the same statistics.
    The bit oracles differ, and so do the controlled phase oracles."""
    rng = random.Random(5)
    for n, f in boolean_tables():
        g = [1 - v for v in f]
        psi = random_state(n, rng)
        assert close(phase_oracle(psi, g), [-a for a in phase_oracle(psi, f)])
        after_f = apply_1q(phase_oracle(psi, f), H, 0)
        after_g = apply_1q(phase_oracle(psi, g), H, 0)
        assert close(probabilities(after_f), probabilities(after_g))
        # the controlled versions are told apart with certainty: control in |+>, input |0...0>
        start = apply_1q(basis_state(n + 1, 0), H, 0)
        a = apply_1q(controlled_phase_oracle(start, f), H, 0)
        b = apply_1q(controlled_phase_oracle(start, g), H, 0)
        assert abs(inner(a, b)) <= TOL


def test_multi_bit_phase_form_is_the_bit_oracle_in_the_hadamard_basis() -> None:
    """(I x H^m) U_f (I x H^m) = the oracle |x>|y> -> (-1)^(y . f(x)) |x>|y>, for all 256 functions
    {0,1}^2 -> {0,1}^2."""
    n, m = 2, 2
    for f in all_functions(n, m):
        for z in range(1 << (n + m)):
            v = basis_state(n + m, z)
            w = v
            for q in range(m):
                w = apply_1q(w, H, q)
            w = bit_oracle(w, f, n, m)
            for q in range(m):
                w = apply_1q(w, H, q)
            assert close(w, inner_phase_oracle(v, f, m))


def test_oracles_are_unitary() -> None:
    f = [0, 1, 1, 0, 1, 0, 0, 0]
    assert is_unitary(unitary_of(4, lambda s: bit_oracle(s, f, 3, 1)))
    assert is_unitary(unitary_of(3, lambda s: phase_oracle(s, f)))
    u = unitary_of(3, lambda s: phase_oracle(phase_oracle(s, f), f))
    assert max_abs_diff(u, unitary_of(3, lambda s: s)) <= TOL


def test_in_place_oracle_needs_a_bijection() -> None:
    good = bad = 0
    for f in all_functions(2, 2):
        try:
            in_place_oracle(basis_state(2, 0), f)
            good += 1
        except ValueError:
            bad += 1
    assert (good, bad) == (24, 256 - 24)
    pi = [2, 0, 3, 1]
    assert is_unitary(unitary_of(2, lambda s: in_place_oracle(s, pi)))


def test_bit_oracle_from_one_in_place_query_and_its_inverse() -> None:
    """For every bijection pi of {0,1}^2 and every |x>|y> with a clean ancilla register."""
    n = 2
    for pi in all_functions(n, n):
        if sorted(pi) != list(range(4)):
            continue
        for x in range(4):
            for y in range(4):
                z = (x << 2 * n) | (y << n)
                out = bit_oracle_from_in_place(basis_state(3 * n, z), pi, n)
                assert close(out, basis_state(3 * n, (x << 2 * n) | ((y ^ pi[x]) << n)))
