# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-oracle/. The authors are listed in prov/KDN9PQ.jsonl.
"""Quantum oracles for a function f: {0,1}^n -> {0,1}^m given as a table (a list of 2**n integers).

Register layout: in |x>|y> the first register x holds the high qubits, as on the quantum-state page.
So the basis index of |x>|y> is x * 2**m + y, the output register y is qubits 0 .. m-1, and qubit 0
is the least significant bit.
"""

from qsim import H, apply_1q, apply_diagonal, apply_permutation


def bit_oracle_perm(f, n: int, m: int) -> list:
    """The bit oracle U_f |x>|y> = |x>|y xor f(x)> as a permutation of the 2**(n+m) basis indices."""
    mask = (1 << m) - 1
    return [((z >> m) << m) | ((z & mask) ^ f[z >> m]) for z in range(1 << (n + m))]


def bit_oracle(state, f, n: int, m: int):
    return apply_permutation(state, bit_oracle_perm(f, n, m))


def phase_oracle(state, f):
    """The phase oracle O_f |x> = (-1)^f(x) |x> for a Boolean f (values 0 or 1)."""
    return apply_diagonal(state, [(-1) ** v for v in f])


def controlled_phase_oracle(state, f):
    """|x>|c> -> (-1)^(c f(x)) |x>|c>; the control c is qubit 0."""
    return apply_diagonal(state, [(-1) ** ((z & 1) * f[z >> 1]) for z in range(len(state))])


def inner_phase_oracle(state, f, m: int):
    """The phase form of a multi-bit oracle: |x>|y> -> (-1)^(y . f(x)) |x>|y>."""
    mask = (1 << m) - 1
    return apply_diagonal(state, [(-1) ** bin((z & mask) & f[z >> m]).count("1") for z in range(len(state))])


def phase_from_bit_oracle(state, f, n: int):
    """One query to the bit oracle with the output qubit in |->: returns the n-qubit state that comes out
    on the input register, and checks that the output qubit is still exactly |->."""
    s = 2 ** -0.5
    big = [0j] * (2 * len(state))
    for x, a in enumerate(state):
        big[2 * x], big[2 * x + 1] = a * s, -a * s
    big = bit_oracle(big, f, n, 1)
    out = [big[2 * x] / s for x in range(len(state))]
    for x in range(len(state)):
        if abs(big[2 * x + 1] + big[2 * x]) > 1e-12:
            raise AssertionError("the output qubit is no longer |->")
    return out


def bit_from_controlled_phase_oracle(state, f):
    """One query to the controlled phase oracle gives the bit oracle (m = 1): H on y, then
    |x>|y> -> (-1)^(y f(x)) |x>|y>, then H on y."""
    state = apply_1q(state, H, 0)
    state = controlled_phase_oracle(state, f)
    return apply_1q(state, H, 0)


def in_place_oracle(state, f):
    """|x> -> |f(x)>. This is a unitary only when f is a bijection; otherwise qsim raises ValueError."""
    return apply_permutation(state, list(f))


def bit_oracle_from_in_place(state, pi, n: int):
    """The bit oracle for a bijection pi from one query to |x> -> |pi(x)> and one to its inverse.

    Three n-qubit registers |x>|y>|a> with index (x << 2n) | (y << n) | a, and a starts at 0:
    a ^= x, then pi on a, then y ^= a, then pi^-1 on a, then a ^= x again."""
    mask = (1 << n) - 1
    inv = [0] * len(pi)
    for x, v in enumerate(pi):
        inv[v] = x

    def on_a(g):
        return lambda z: (z & ~mask) | g(z & mask, z)

    state = apply_permutation(state, on_a(lambda a, z: a ^ (z >> 2 * n)))
    state = apply_permutation(state, on_a(lambda a, z: pi[a]))
    state = apply_permutation(state, lambda z: z ^ ((z & mask) << n))
    state = apply_permutation(state, on_a(lambda a, z: inv[a]))
    return apply_permutation(state, on_a(lambda a, z: a ^ (z >> 2 * n)))


def all_functions(n: int, m: int):
    """Every table of a function {0,1}^n -> {0,1}^m."""
    size, vals = 1 << n, 1 << m
    for code in range(vals ** size):
        table = []
        for _ in range(size):
            table.append(code % vals)
            code //= vals
        yield table
