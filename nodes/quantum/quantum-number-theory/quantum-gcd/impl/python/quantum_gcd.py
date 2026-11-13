# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-gcd/. The authors are listed in prov/K6XYGK.jsonl.
"""A reversible binary GCD circuit: |u>|v>|0> -> |u>|v>|gcd(u, v)>, for odd u.

The circuit runs a fixed number 2n - 1 of rounds of the binary GCD of Stein, so
the gate sequence does not depend on the input. Each round keeps two history
bits (was v odd, was there a swap), the result is copied out, and the rounds are
run backward to clear the history (Bennett's method).

A circuit is a list of (controls, target) gates as in qsim, made of NOT, CNOT
and Toffoli gates only. Registers are lists of qubit indices, least significant
bit first.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from qsim import Allocator, Gate, copy_reg, cswap, gate_counts, get_reg, inverse, less_than, ripple_add, run, set_reg


@dataclass
class Layout:
    u: List[int]  # data, n qubits, u odd
    v: List[int]  # data, n qubits
    g: List[int]  # output, n qubits, 0 before
    tmp: List[int]  # ancilla, n qubits: a copy of u for the controlled subtraction
    d: int  # ancilla: the comparison bit [v < u]
    c0: int  # ancilla: carry qubit of the adder
    odd: List[int]  # history: odd[i] = 1 when v was odd in round i
    swp: List[int]  # history: swp[i] = 1 when u and v were swapped in round i

    def ancillas(self) -> List[int]:
        return self.tmp + [self.d, self.c0] + self.odd + self.swp


def rounds(n: int) -> int:
    """The number of rounds that is enough for all odd u < 2^n and all v < 2^n."""
    return max(1, 2 * n - 1)


def make_layout(n: int) -> Layout:
    al = Allocator()
    u, v, g, tmp = al.reg(n), al.reg(n), al.reg(n), al.reg(n)
    d, c0 = al.qubit(), al.qubit()
    k = rounds(n)
    return Layout(u=u, v=v, g=g, tmp=tmp, d=d, c0=c0, odd=al.reg(k), swp=al.reg(k))


def gcd_rounds(L: Layout) -> List[Gate]:
    """The forward part: 2n - 1 rounds. Afterwards u = gcd(u, v), v = 0 and the history is set."""
    g: List[Gate] = []
    v = list(L.v)
    for i in range(len(L.odd)):  # @line L1
        e, h = L.odd[i], L.swp[i]
        g.append(((v[0],), e))  # @line L2: e = v mod 2
        cmp = less_than(L.u, v, L.c0, L.d)  # d = [v < u]
        g += cmp + [((e, L.d), h)] + cmp  # @line L3: h = e and [v < u]; d back to 0
        g += cswap(h, L.u, v)  # @line L4
        sub = copy_reg(L.u, L.tmp, (e,))
        g += sub + inverse(ripple_add(L.tmp, v, L.c0)) + sub  # @line L5: v = v - e u
        v = v[1:] + v[:1]  # @line L6: v is even, so halving is a rotation of its wires
    return g


def gcd_circuit(n: int) -> Tuple[List[Gate], Layout]:
    """The full circuit: rounds, copy of u into g, rounds backward."""
    if n < 1:
        raise ValueError("need n >= 1")
    L = make_layout(n)
    fwd = gcd_rounds(L)
    return fwd + copy_reg(L.u, L.g) + inverse(fwd), L  # @line L7, L8


def run_gcd(gates: List[Gate], L: Layout, u: int, v: int) -> Dict[str, int]:
    """Run the circuit on |u>|v>|0...0> and read the registers back."""
    s = run(gates, set_reg(set_reg(0, L.u, u), L.v, v))
    return {"u": get_reg(s, L.u), "v": get_reg(s, L.v), "g": get_reg(s, L.g), "ancillas": get_reg(s, L.ancillas())}


def classical_rounds(u: int, v: int) -> int:
    """The number of rounds in which v > 0, for the same binary GCD run classically."""
    if u % 2 == 0:
        raise ValueError("u must be odd")
    k = 0
    while v:
        if v % 2 and v < u:
            u, v = v, u
        if v % 2:
            v -= u
        v //= 2
        k += 1
    return k


def gcd_counts(n: int) -> Dict[str, int]:
    gates, L = gcd_circuit(n)
    out = gate_counts(gates)
    out["data_qubits"] = 3 * n
    out["ancilla_qubits"] = len(L.ancillas())
    return out
