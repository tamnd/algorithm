# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-modular-exponentiation/. The authors are listed in prov/S5NABE.jsonl.
"""A reversible circuit for |x>|1> -> |x>|a^x mod N>, from NOT, CNOT and Toffoli gates.

The construction follows Vedral, Barenco and Ekert, with the ripple-carry adder of
Cuccaro, Draper, Kutin and Moulton (qsim.ripple_add) as the only adder:

    MODADD(k)  b <- b + k mod N           (doubly controlled, k a classical constant)
    CMULT(a)   b <- b + a y mod N         (controlled, one MODADD per bit of y)
    CU(a)      y <- a y mod N             (controlled, CMULT(a), swap, CMULT(a^-1) backward)
    MODEXP     y <- y a^x mod N           (one CU(a^(2^j)) per exponent qubit x_j)

A circuit is a list of (controls, target) gates as in qsim. Registers are lists of
qubit indices, least significant bit first.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from qsim import Allocator, Gate, cswap, gate_counts, get_reg, inverse, load_constant, ripple_add, run, set_reg


@dataclass
class Layout:
    """The registers of the circuit. n = N.bit_length()."""

    x: List[int]  # exponent register, t qubits (data)
    y: List[int]  # work register, n qubits (data)
    b: List[int]  # accumulator, n + 1 qubits (ancilla, 0 before and after)
    tmp: List[int]  # constant register, n + 1 qubits (ancilla)
    c0: int  # carry qubit of the adder (ancilla)
    anc: int  # flag of the modular adder (ancilla)

    @property
    def num_qubits(self) -> int:
        return len(self.x) + len(self.y) + len(self.b) + len(self.tmp) + 2

    def ancillas(self) -> List[int]:
        return self.b + self.tmp + [self.c0, self.anc]


def make_layout(N: int, t: int) -> Layout:
    n = N.bit_length()
    al = Allocator()
    return Layout(x=al.reg(t), y=al.reg(n), b=al.reg(n + 1), tmp=al.reg(n + 1), c0=al.qubit(), anc=al.qubit())


def add_constant(k: int, L: Layout, controls: Sequence[int] = ()) -> List[Gate]:
    """b <- b + k mod 2^(n+1) when all controls are 1: load k into tmp, add, unload."""
    load = load_constant(k, L.tmp, controls)
    return load + ripple_add(L.tmp, L.b, L.c0) + load


def sub_constant(k: int, L: Layout, controls: Sequence[int] = ()) -> List[Gate]:
    """b <- b - k mod 2^(n+1) when all controls are 1."""
    return inverse(add_constant(k, L, controls))


def modular_adder(k: int, N: int, L: Layout, controls: Sequence[int]) -> List[Gate]:
    """MODADD: b <- (b + k) mod N when all controls are 1, for 0 <= b < N and 0 <= k < N.

    The flag anc is 0 before and after. The top qubit of b is the sign of b in
    two's complement on n + 1 qubits.
    """
    top = L.b[-1]
    g: List[Gate] = []
    g += add_constant(k, L, controls)  # @line L1
    g += sub_constant(N, L)  # @line L2
    g.append(((top,), L.anc))  # @line L3: anc = 1 when b + k < N
    g += add_constant(N, L, (L.anc,))  # @line L4
    g += sub_constant(k, L, controls)  # @line L5: now top = 0 exactly when anc = 1
    g += [((), top), ((top,), L.anc), ((), top)]  # @line L6
    g += add_constant(k, L, controls)  # @line L7
    return g


def controlled_multiplier(a: int, N: int, L: Layout, ctrl: int) -> List[Gate]:
    """CMULT: b <- (b + a y) mod N when ctrl is 1, for y < N and b < N."""
    g: List[Gate] = []
    for i, q in enumerate(L.y):  # @line L8
        g += modular_adder((a << i) % N, N, L, (ctrl, q))  # @line L9
    return g


def controlled_mult_inplace(a: int, N: int, L: Layout, ctrl: int) -> List[Gate]:
    """CU: y <- a y mod N when ctrl is 1, with b = 0 before and after. Needs gcd(a, N) = 1."""
    a_inv = pow(a, -1, N)
    g = controlled_multiplier(a, N, L, ctrl)  # @line L10: b = a y
    g += cswap(ctrl, L.y, L.b[: len(L.y)])  # @line L11: y = a y, b = y
    g += inverse(controlled_multiplier(a_inv, N, L, ctrl))  # @line L12: b = y - a^-1 (a y) = 0
    return g


def modexp_circuit(a: int, N: int, t: int) -> Tuple[List[Gate], Layout]:
    """MODEXP: |x>|y> -> |x>|y a^x mod N> for y < N, with all ancillas 0 before and after."""
    if N < 3 or math.gcd(a, N) != 1:
        raise ValueError("need N >= 3 and gcd(a, N) = 1")
    L = make_layout(N, t)
    g: List[Gate] = []
    c = a % N
    for j in range(t):  # @line L13
        g += controlled_mult_inplace(c, N, L, L.x[j])  # @line L14
        c = c * c % N  # @line L15: a^(2^(j+1)) mod N, computed classically
    return g, L


def run_modexp(gates: List[Gate], L: Layout, x: int, y: int) -> Dict[str, int]:
    """Run the circuit on the basis state |x>|y>|0...0> and read the registers back."""
    s = set_reg(set_reg(0, L.x, x), L.y, y)
    s = run(gates, s)
    return {
        "x": get_reg(s, L.x),
        "y": get_reg(s, L.y),
        "ancillas": get_reg(s, L.ancillas()),
    }


def modexp_counts(a: int, N: int, t: int) -> Dict[str, int]:
    """The gate counts and qubit counts of the circuit."""
    g, L = modexp_circuit(a, N, t)
    out = gate_counts(g)
    out["data_qubits"] = len(L.x) + len(L.y)
    out["ancilla_qubits"] = len(L.ancillas())
    return out
