# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-computation/. The authors are listed in prov/3F0WFR.jsonl.
"""Reversible computation on classical bits.

1. A Boolean circuit of AND, OR, XOR, NAND and NOT gates becomes a reversible circuit of
   NOT, CNOT and Toffoli gates that writes each gate value to a fresh work bit (this leaves garbage).
2. Bennett's construction (1973): compute, copy the outputs, uncompute. The work bits end at 0.
3. Bennett's pebble game (1989): a reversible schedule for a chain of T steps with few checkpoints.

Wire j is bit j of an integer (bit 0 is the least significant bit), as in qsim.py.
"""

from qsim import inverse_gates, run_classical


def evaluate(circuit, n: int, outputs, x: int) -> int:
    """The reference: evaluate a Boolean circuit on the input bits of x. Returns the output bits as an integer."""
    val = [(x >> i) & 1 for i in range(n)]
    for op, args in circuit:
        a = val[args[0]]
        b = val[args[1]] if len(args) > 1 else 0
        val.append({"and": a & b, "or": a | b, "xor": a ^ b, "nand": 1 - (a & b), "not": 1 - a}[op])
    return sum(val[w] << i for i, w in enumerate(outputs))


def compute_with_garbage(circuit, n: int) -> list:
    """Gate value number i goes to wire n + i, which must start at 0. Inputs are not changed."""
    gates = []
    for i, (op, args) in enumerate(circuit):
        t = n + i
        if op == "and":
            gates.append(("mcx", (args[0], args[1]), t))
        elif op == "nand":
            gates += [("mcx", (args[0], args[1]), t), ("x", t)]
        elif op == "or":
            # a or b = a xor b xor ab
            gates += [("cx", args[0], t), ("cx", args[1], t), ("mcx", (args[0], args[1]), t)]
        elif op == "xor":
            gates += [("cx", args[0], t), ("cx", args[1], t)]
        elif op == "not":
            gates += [("cx", args[0], t), ("x", t)]
        else:
            raise ValueError(f"unknown operation {op!r}")
    return gates


def bennett(circuit, n: int, outputs) -> tuple:
    """Bennett's compute, copy, uncompute. Returns (gates, width, output wires).

    Wires: 0 .. n-1 the input, n .. n+g-1 the work bits, then one fresh wire per output.
    On input x with every other wire 0 the result is x, all work bits 0, and f(x) on the output wires.
    """
    g = len(circuit)
    compute = compute_with_garbage(circuit, n)
    out_wires = [n + g + i for i in range(len(outputs))]
    copy = [("cx", w, o) for w, o in zip(outputs, out_wires)]
    return compute + copy + inverse_gates(compute), n + g + len(outputs), out_wires


def landauer_embedding(f, n: int, m: int):
    """The reversible map (x, y) -> (x, y xor f(x)) on n + m bits; y is the high m bits."""
    def perm(z: int) -> int:
        x, y = z & ((1 << n) - 1), z >> n
        return x | ((y ^ f(x)) << n)
    return perm


def pebble_schedule(k: int, m: int = 2) -> list:
    """Bennett's reversible pebbling of a chain of T = m**k steps.

    Node 0 is the input and is always pebbled. A move toggles the pebble on node i >= 1, and it is legal
    only when node i - 1 holds a pebble. The schedule starts with no pebble on 1 .. T and ends with one
    pebble on node T only. For m = 2 it has 3**k moves and uses at most k + 1 pebbles.
    """
    moves = []

    def advance(s: int, level: int) -> None:
        if level == 0:
            moves.append(s + 1)
            return
        step = m ** (level - 1)
        for j in range(m):
            advance(s + j * step, level - 1)
        for j in range(m - 2, -1, -1):
            retract(s + j * step, level - 1)

    def retract(s: int, level: int) -> None:
        start = len(moves)
        advance(s, level)
        part = moves[start:]
        del moves[start:]
        moves.extend(reversed(part))

    advance(0, k)
    return moves


def play_pebbles(moves, length: int) -> tuple:
    """Check a schedule. Returns (final set of pebbled nodes, the largest number of pebbles at one time)."""
    pebbled = {0}
    most = 0
    for i in moves:
        if not 1 <= i <= length or i - 1 not in pebbled:
            raise ValueError(f"illegal move on node {i}")
        pebbled ^= {i}
        most = max(most, len(pebbled) - 1)
    return pebbled - {0}, most


def run_bits(x: int, gates) -> int:
    return run_classical(x, gates)
