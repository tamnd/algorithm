# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qubit/. The authors are listed in prov/YX77AF.jsonl.
"""A qubit: a unit vector a|0> + b|1> in C^2, with its global and relative phase."""

import cmath
import math
import random

from qsim import TOL, inner, measure

S2 = math.sqrt(0.5)
KET0 = [1 + 0j, 0j]
KET1 = [0j, 1 + 0j]
PLUS = [S2 + 0j, S2 + 0j]
MINUS = [S2 + 0j, -S2 + 0j]
PLUS_I = [S2 + 0j, 1j * S2]
MINUS_I = [S2 + 0j, -1j * S2]
Z_BASIS = (KET0, KET1)
X_BASIS = (PLUS, MINUS)
Y_BASIS = (PLUS_I, MINUS_I)


def qubit(a: complex, b: complex) -> list[complex]:
    """The state a|0> + b|1>. Raises ValueError unless |a|^2 + |b|^2 = 1."""
    if abs(abs(a) ** 2 + abs(b) ** 2 - 1) > TOL:
        raise ValueError("a qubit state needs |a|^2 + |b|^2 = 1")
    return [complex(a), complex(b)]


def normalize(a: complex, b: complex) -> list[complex]:
    """Scale a nonzero vector (a, b) to a unit vector."""
    r = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    if r == 0:
        raise ValueError("the zero vector is not a state")
    return [complex(a) / r, complex(b) / r]


def probabilities_in_basis(state: list[complex], basis) -> list[float]:
    """Outcome probabilities |<e_k|psi>|^2 for an orthonormal basis (e_0, e_1)."""
    return [abs(inner(e, state)) ** 2 for e in basis]


def with_global_phase(state: list[complex], gamma: float) -> list[complex]:
    """e^(i gamma) times the state."""
    w = cmath.exp(1j * gamma)
    return [w * a for a in state]


def relative_phase(state: list[complex]) -> float:
    """arg(b) - arg(a) in [0, 2 pi). Defined only when a and b are both nonzero."""
    a, b = state
    if abs(a) < TOL or abs(b) < TOL:
        raise ValueError("the relative phase needs two nonzero amplitudes")
    return (cmath.phase(b) - cmath.phase(a)) % (2 * math.pi)


def same_physical_state(u: list[complex], v: list[complex]) -> bool:
    """True when the unit vectors u and v differ only by a global phase, that is |<u|v>| = 1."""
    return abs(abs(inner(u, v)) - 1) <= TOL


def canonical(state: list[complex]) -> list[complex]:
    """The representative with a real, nonnegative amplitude on |0> (on |1> when a = 0)."""
    a, b = state
    lead = a if abs(a) > TOL else b
    w = cmath.exp(-1j * cmath.phase(lead))
    return [w * a, w * b]


def sample_counts(state: list[complex], shots: int, rng: random.Random) -> list[int]:
    """Counts of the outcomes 0 and 1 in shots measurements of fresh copies in the computational basis."""
    counts = [0, 0]
    for _ in range(shots):
        x, _post = measure(state, rng)
        counts[x] += 1
    return counts
