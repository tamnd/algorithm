# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-modular-inversion/. The authors are listed in prov/JXGTEC.jsonl.
"""A reversible circuit for |x>|0> -> |x>|x^-1 mod N>, for a classical odd modulus N.

The circuit runs a binary extended Euclidean algorithm for a fixed number 2n - 1
of rounds. It keeps u, v and two coefficients A, B with A x = u and B x = v
(mod N), starting from (u, v, A, B) = (N, x, 0, 1). At the end u = gcd(x, N),
so A = x^-1 mod N when x is a unit. The result is copied out, and the rounds
are run backward to clear the history (Bennett's method).

A circuit is a list of (controls, target) gates as in qsim, made of NOT, CNOT
and Toffoli gates only. Registers are lists of qubit indices, least significant
bit first.
"""

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from qsim import Allocator, Gate, copy_reg, cswap, gate_counts, get_reg, inverse, less_than, load_constant, ripple_add, run, set_reg


@dataclass
class Layout:
    x: List[int]  # data, n qubits: the input, used as v during the rounds
    out: List[int]  # data, n qubits: the result
    u: List[int]  # ancilla, n qubits, holds N during the rounds
    A: List[int]  # ancilla, n + 1 qubits
    B: List[int]  # ancilla, n + 1 qubits
    tmp: List[int]  # ancilla, n + 1 qubits: copies of u or A
    cst: List[int]  # ancilla, n + 1 qubits: classical constants
    c0: int  # ancilla: carry qubit of the adder
    d: int  # ancilla: the comparison bit [v < u]
    f: int  # ancilla: flag of the modular subtraction
    p: int  # ancilla: parity bit of the modular halving
    odd: List[int]  # history: v was odd in round i
    swp: List[int]  # history: the registers were swapped in round i

    def ancillas(self) -> List[int]:
        return self.u + self.A + self.B + self.tmp + self.cst + [self.c0, self.d, self.f, self.p] + self.odd + self.swp


def rounds(n: int) -> int:
    return max(1, 2 * n - 1)


def make_layout(N: int) -> Layout:
    n = N.bit_length()
    al = Allocator()
    x, out, u = al.reg(n), al.reg(n), al.reg(n)
    A, B, tmp, cst = al.reg(n + 1), al.reg(n + 1), al.reg(n + 1), al.reg(n + 1)
    c0, d, f, p = al.qubit(), al.qubit(), al.qubit(), al.qubit()
    k = rounds(n)
    return Layout(x=x, out=out, u=u, A=A, B=B, tmp=tmp, cst=cst, c0=c0, d=d, f=f, p=p, odd=al.reg(k), swp=al.reg(k))


def add_const(k: int, b: Sequence[int], L: Layout, controls: Sequence[int] = ()) -> List[Gate]:
    """b <- b + k mod 2^(n+1) when all controls are 1."""
    load = load_constant(k, L.cst, controls)
    return load + ripple_add(L.cst, b, L.c0) + load


def mod_add_reg(a: Sequence[int], b: Sequence[int], N: int, L: Layout) -> List[Gate]:
    """b <- (b + a) mod N for 0 <= a, b < N (registers of n + 1 qubits); the flag f stays 0."""
    top = b[-1]
    g = ripple_add(a, b, L.c0)
    g += inverse(add_const(N, b, L))
    g.append(((top,), L.f))  # f = 1 when b + a < N
    g += add_const(N, b, L, (L.f,))
    g += inverse(ripple_add(a, b, L.c0))  # now top = 0 exactly when f = 1
    g += [((), top), ((top,), L.f), ((), top)]
    g += ripple_add(a, b, L.c0)
    return g


def halve_mod(b: List[int], N: int, L: Layout) -> Tuple[List[Gate], List[int]]:
    """b <- b / 2 mod N for 0 <= b < N, N odd. Returns the gates and the new wire order of b."""
    g: List[Gate] = [((b[0],), L.p)]  # p = b mod 2
    g += add_const(N, b, L, (L.p,))  # b + p N is even and below 2N
    b = b[1:] + b[:1]  # halve by relabeling the wires
    h = (N + 1) // 2  # p = 1 exactly when b >= (N + 1)/2
    load = load_constant(h, L.cst)
    g += [((), L.p)] + load + less_than(L.cst, b, L.c0, L.p) + load
    return g, b


def inversion_rounds(N: int, L: Layout) -> List[Gate]:
    """The forward part: 2n - 1 rounds of the extended binary GCD on (u, v, A, B)."""
    n = len(L.u)
    g: List[Gate] = []
    v, B = list(L.x), list(L.B)
    for i in range(len(L.odd)):  # @line L2
        e, h = L.odd[i], L.swp[i]
        g.append(((v[0],), e))
        cmp = less_than(L.u, v, L.c0, L.d)
        g += cmp + [((e, L.d), h)] + cmp  # @line L3: e = v odd, h = e and [v < u]
        g += cswap(h, L.u, v) + cswap(h, L.A, B)  # @line L4
        cu = copy_reg(L.u, L.tmp[:n], (e,))
        g += cu + inverse(ripple_add(L.tmp[:n], v, L.c0)) + cu  # @line L5: v = v - e u
        ca = copy_reg(L.A, L.tmp, (e,))
        g += ca + inverse(mod_add_reg(L.tmp, B, N, L)) + ca  # B = B - e A mod N
        v = v[1:] + v[:1]  # @line L6
        hg, B = halve_mod(B, N, L)  # @line L7
        g += hg
    return g


def inversion_circuit(N: int) -> Tuple[List[Gate], Layout]:
    """The full circuit: load (N, 0, 1), rounds, copy A, rounds backward, unload."""
    if N < 3 or N % 2 == 0:
        raise ValueError("need an odd modulus N >= 3")
    L = make_layout(N)
    n = len(L.u)
    init = load_constant(N, L.u) + load_constant(1, L.B)  # @line L1
    fwd = inversion_rounds(N, L)
    copy = copy_reg(L.A[:n], L.out)  # @line L8
    return init + fwd + copy + inverse(fwd) + init, L  # @line L9


def run_inversion(gates: List[Gate], L: Layout, x: int) -> Dict[str, int]:
    s = run(gates, set_reg(0, L.x, x))
    return {"x": get_reg(s, L.x), "out": get_reg(s, L.out), "ancillas": get_reg(s, L.ancillas())}


def inversion_counts(N: int) -> Dict[str, int]:
    gates, L = inversion_circuit(N)
    out = gate_counts(gates)
    out["data_qubits"] = len(L.x) + len(L.out)
    out["ancilla_qubits"] = len(L.ancillas())
    return out
