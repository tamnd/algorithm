# SPDX-License-Identifier: MIT
# Shared helper of the qn1 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python simulator for the qn1 pages (Shor, factoring and arithmetic circuits).

Conventions:
- A state on n qubits is a list of 2**n complex amplitudes.
- Qubit 0 is the least significant bit of the basis index.
- A register is a list of qubit indices, least significant bit first.

Two parts:
1. State vectors: one-qubit gates, controlled gates, permutations of basis
   states (oracles and reversible arithmetic), diagonal phases, exact
   probabilities and sampled measurement.
2. Reversible circuits on basis states: a circuit is a list of
   multi-controlled NOT gates (controls, target). NOT, CNOT and Toffoli are
   the cases with 0, 1 and 2 controls. Basis states are Python integers, so
   circuits with many qubits run fast. A ripple-carry adder and a comparator
   are given as building blocks; the pages build their own circuits from them.

This file holds no algorithm of any page.
"""

import cmath
import math
import random
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

State = List[complex]
Matrix2 = Tuple[Tuple[complex, complex], Tuple[complex, complex]]

SQRT_HALF = 1 / math.sqrt(2)
H: Matrix2 = ((SQRT_HALF, SQRT_HALF), (SQRT_HALF, -SQRT_HALF))
X: Matrix2 = ((0, 1), (1, 0))


def phase(theta: float) -> Matrix2:
    """The gate diag(1, e^(i theta))."""
    return ((1, 0), (0, cmath.exp(1j * theta)))


# ---------------------------------------------------------------- state vectors


def basis_state(n: int, k: int = 0) -> State:
    """The basis state |k> on n qubits."""
    s = [0j] * (1 << n)
    s[k] = 1 + 0j
    return s


def apply_1q(state: State, q: int, m: Matrix2) -> None:
    """Apply the 2 x 2 matrix m to qubit q, in place."""
    bit = 1 << q
    (a, b), (c, d) = m
    for i in range(len(state)):
        if not i & bit:
            x, y = state[i], state[i | bit]
            state[i] = a * x + b * y
            state[i | bit] = c * x + d * y


def apply_controlled_1q(state: State, controls: Sequence[int], q: int, m: Matrix2) -> None:
    """Apply m to qubit q on the basis states where every control qubit is 1."""
    bit = 1 << q
    mask = 0
    for c in controls:
        mask |= 1 << c
    (a, b), (c, d) = m
    for i in range(len(state)):
        if not i & bit and i & mask == mask:
            x, y = state[i], state[i | bit]
            state[i] = a * x + b * y
            state[i | bit] = c * x + d * y


def apply_controlled_phase(state: State, c: int, q: int, theta: float) -> None:
    """Multiply the amplitude by e^(i theta) where qubits c and q are both 1 (symmetric in c and q)."""
    mask = (1 << c) | (1 << q)
    w = cmath.exp(1j * theta)
    for i in range(len(state)):
        if i & mask == mask:
            state[i] *= w


def swap_qubits(state: State, p: int, q: int) -> None:
    """Swap qubits p and q, in place."""
    bp, bq = 1 << p, 1 << q
    for i in range(len(state)):
        if i & bp and not i & bq:
            j = (i ^ bp) | bq
            state[i], state[j] = state[j], state[i]


def apply_permutation(state: State, f: Callable[[int], int]) -> State:
    """Return the state with amplitude of |i> moved to |f(i)>. f must be a bijection."""
    out = [0j] * len(state)
    seen = bytearray(len(state))
    for i, amp in enumerate(state):
        j = f(i)
        if seen[j]:
            raise ValueError("the map is not a permutation of the basis states")
        seen[j] = 1
        out[j] = amp
    return out


def apply_diagonal(state: State, theta: Callable[[int], float]) -> None:
    """Multiply the amplitude of |i> by e^(i theta(i)), in place."""
    for i in range(len(state)):
        if state[i]:
            state[i] *= cmath.exp(1j * theta(i))


def norm2(state: State) -> float:
    return sum(abs(a) ** 2 for a in state)


def probabilities(state: State) -> List[float]:
    """The exact probability of each basis state (Born rule)."""
    return [abs(a) ** 2 for a in state]


def marginal(probs: Sequence[float], qubits: Sequence[int]) -> Dict[int, float]:
    """The distribution of the value of the register `qubits` (least significant first)."""
    out: Dict[int, float] = {}
    for i, p in enumerate(probs):
        if p:
            v = get_reg(i, qubits)
            out[v] = out.get(v, 0.0) + p
    return out


def sample(dist: Dict[int, float], rng: random.Random) -> int:
    """Draw one value from a distribution given as {value: probability}."""
    u = rng.random() * sum(dist.values())
    acc = 0.0
    last = None
    for v in sorted(dist):
        acc += dist[v]
        last = v
        if u < acc:
            return v
    return last


def measure(state: State, rng: random.Random) -> int:
    """Measure all qubits in the computational basis and return the basis index."""
    return sample({i: p for i, p in enumerate(probabilities(state)) if p}, rng)


# ---------------------------------------------------------------- registers


def get_reg(x: int, reg: Sequence[int]) -> int:
    """The integer held by register reg in the basis state x."""
    v = 0
    for k, q in enumerate(reg):
        v |= ((x >> q) & 1) << k
    return v


def set_reg(x: int, reg: Sequence[int], value: int) -> int:
    """The basis state x with register reg set to value."""
    for k, q in enumerate(reg):
        if (value >> k) & 1:
            x |= 1 << q
        else:
            x &= ~(1 << q)
    return x


class Allocator:
    """Hands out fresh qubit indices, so that registers never overlap."""

    def __init__(self) -> None:
        self.n = 0

    def reg(self, size: int) -> List[int]:
        r = list(range(self.n, self.n + size))
        self.n += size
        return r

    def qubit(self) -> int:
        return self.reg(1)[0]


# ---------------------------------------------------------------- reversible circuits

Gate = Tuple[Tuple[int, ...], int]  # (controls, target): target ^= AND of the controls


def run(gates: Iterable[Gate], x: int) -> int:
    """Run a circuit of multi-controlled NOT gates on the basis state x."""
    for controls, t in gates:
        if all((x >> c) & 1 for c in controls):
            x ^= 1 << t
    return x


def inverse(gates: Sequence[Gate]) -> List[Gate]:
    """The inverse circuit. Each multi-controlled NOT is its own inverse."""
    return list(reversed(gates))


def controlled(gates: Iterable[Gate], c: int) -> List[Gate]:
    """Add the control qubit c to every gate. c must not be a target of the circuit."""
    out = []
    for controls, t in gates:
        if t == c:
            raise ValueError("the control qubit is a target of the circuit")
        out.append((tuple(controls) + (c,), t))
    return out


def gate_counts(gates: Iterable[Gate]) -> Dict[str, int]:
    """Count the gates by number of controls: NOT, CNOT, Toffoli and larger."""
    names = {0: "not", 1: "cnot", 2: "toffoli"}
    out = {"not": 0, "cnot": 0, "toffoli": 0, "larger": 0}
    for controls, _ in gates:
        out[names.get(len(controls), "larger")] += 1
    return out


def load_constant(k: int, reg: Sequence[int], controls: Sequence[int] = ()) -> List[Gate]:
    """XOR the classical constant k into reg, on the basis states where all controls are 1."""
    if k >> len(reg):
        raise ValueError("the constant does not fit in the register")
    return [(tuple(controls), q) for i, q in enumerate(reg) if (k >> i) & 1]


def copy_reg(src: Sequence[int], dst: Sequence[int], controls: Sequence[int] = ()) -> List[Gate]:
    """XOR src into dst bit by bit (CNOTs, or Toffolis with one control)."""
    return [(tuple(controls) + (s,), d) for s, d in zip(src, dst)]


def cswap(c: int, r1: Sequence[int], r2: Sequence[int]) -> List[Gate]:
    """Swap the registers r1 and r2 when qubit c is 1 (one Fredkin gate per bit)."""
    out: List[Gate] = []
    for p, q in zip(r1, r2):
        out += [((q,), p), ((c, p), q), ((q,), p)]
    return out


def ripple_add(a: Sequence[int], b: Sequence[int], c0: int, z: int = None) -> List[Gate]:
    """Ripple-carry adder of Cuccaro, Draper, Kutin and Moulton (MAJ and UMA blocks).

    Maps |a>|b>|c0 = 0>|z> to |a>|(a + b) mod 2^n>|0>|z xor carry>, where n = len(a) = len(b).
    With z = None the carry out is dropped and the map is addition mod 2^n.
    The inverse circuit maps b to (b - a) mod 2^n and toggles z exactly when b < a.
    """
    n = len(a)
    if n != len(b) or n == 0:
        raise ValueError("the registers must have the same positive length")
    g: List[Gate] = []
    carry = [c0] + list(a)  # the carry into position i sits on carry[i] after MAJ i-1

    def maj(x: int, y: int, w: int) -> None:  # x: carry in, y: b_i, w: a_i
        g.extend([((w,), y), ((w,), x), ((x, y), w)])

    def uma(x: int, y: int, w: int) -> None:
        g.extend([((x, y), w), ((w,), x), ((x,), y)])

    for i in range(n):
        maj(carry[i], b[i], a[i])
    if z is not None:
        g.append(((a[n - 1],), z))
    for i in reversed(range(n)):
        uma(carry[i], b[i], a[i])
    return g


def less_than(a: Sequence[int], b: Sequence[int], c0: int, z: int) -> List[Gate]:
    """Toggle z exactly when b < a (unsigned). a and b are unchanged afterwards."""
    return inverse(ripple_add(a, b, c0, z)) + ripple_add(a, b, c0)
