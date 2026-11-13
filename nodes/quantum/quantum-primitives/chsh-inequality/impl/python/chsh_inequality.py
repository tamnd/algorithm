# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chsh-inequality/. The authors are listed in prov/9NC848.jsonl.

"""The CHSH quantity S for local strategies and for measurements on a shared state.

A measurement setting is an angle t in the X-Z plane: the observable
A(t) = cos(t) Z + sin(t) X, with outcomes +1 and -1. Alice measures qubit 1
and Bob measures qubit 0 of a two-qubit state.
"""

import itertools
import math

from qsim import X, Z, inner, kron_mat, matvec, project_qubit, apply_1q


def observable(t):
    c, s = math.cos(t), math.sin(t)
    return [[c * Z[i][j] + s * X[i][j] for j in range(2)] for i in range(2)]


def correlation(state, a, b):
    """E(a, b) = <state| A(a) (x) A(b) |state>."""
    return inner(state, matvec(kron_mat(observable(a), observable(b)), state)).real


def chsh_value(state, a0, a1, b0, b1):
    """S = E(a0, b0) + E(a0, b1) + E(a1, b0) - E(a1, b1)."""
    return correlation(state, a0, b0) + correlation(state, a0, b1) + correlation(state, a1, b0) - correlation(state, a1, b1)


OPTIMAL_ANGLES = (0.0, math.pi / 2, math.pi / 4, -math.pi / 4)


def deterministic_strategies():
    """Every local deterministic strategy: outcomes (A0, A1, B0, B1) in {-1, +1}^4."""
    return itertools.product((-1, 1), repeat=4)


def classical_chsh_max():
    """The largest |S| over all local deterministic strategies (brute force)."""
    return max(abs(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1) for a0, a1, b0, b1 in deterministic_strategies())


def classical_game_value():
    """The best win probability of the CHSH game over deterministic strategies.

    The referee draws x, y uniformly from {0, 1}; the players win when a xor b = x and y.
    A strategy is a pair of functions a(x), b(y), each given by two bits.
    """
    best = 0
    for a0, a1, b0, b1 in itertools.product((0, 1), repeat=4):
        wins = sum(((a0, a1)[x] ^ (b0, b1)[y]) == (x & y) for x in (0, 1) for y in (0, 1))
        best = max(best, wins)
    return best / 4


def _rotate_to_z(t):
    """A unitary that maps the +1 eigenvector of A(t) to |0>: the rotation by -t about the Y axis."""
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[c, s], [-s, c]]


def play_chsh_game(state, rng, rounds, angles=OPTIMAL_ANGLES):
    """Play the CHSH game on fresh copies of state. Returns the number of wins.

    Output bit 0 means outcome +1 and bit 1 means outcome -1.
    """
    a_angles, b_angles = angles[:2], angles[2:]
    wins = 0
    for _ in range(rounds):
        x, y = rng.randrange(2), rng.randrange(2)
        s = apply_1q(apply_1q(state, _rotate_to_z(a_angles[x]), 1), _rotate_to_z(b_angles[y]), 0)
        p1, post1 = project_qubit(s, 1, 1)
        if rng.random() < p1:
            a, s = 1, post1
        else:
            a, s = 0, project_qubit(s, 1, 0)[1]
        p1b, _ = project_qubit(s, 0, 1)
        b = 1 if rng.random() < p1b else 0
        wins += (a ^ b) == (x & y)
    return wins
