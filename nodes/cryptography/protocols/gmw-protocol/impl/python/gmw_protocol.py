# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmw-protocol/. The authors are listed in prov/6M8M74.jsonl.
"""Two-party GMW on XOR shares, with semi-honest security.

A circuit is a list of gates (op, a, b, c) on integer wire ids, in
topological order, with op in "AND", "XOR", "INV" (for INV, b is ignored).
Every wire value v is held as two bits [v]_1, [v]_2 with v = [v]_1 XOR [v]_2.

XOR and INV gates are local. An AND gate needs one interaction, done in one
of two ways:
  "ot":     a 1-out-of-4 OT from P1 to P2 (Goldreich, Micali, Wigderson 1987);
  "triple": a Beaver multiplication triple from a dealer, then each party
            opens two masked bits (Beaver 1991).
All AND gates of the same AND depth run in one round, so the number of
rounds for the gates equals the AND depth of the circuit.

The OT and the dealer are local ideal functionalities. For study only: the
code is not constant time, uses Python's random module, and runs both
parties in one process. Use a maintained framework such as MP-SPDZ or
ABY for real data.
"""

import random
from dataclasses import dataclass, field
from typing import Sequence

Gate = tuple[str, int, int, int]


@dataclass
class Circuit:
    n_wires: int
    inputs1: list[int]     # wires of P1's input bits
    inputs2: list[int]     # wires of P2's input bits
    outputs: list[int]
    gates: list[Gate]


@dataclass
class Stats:
    rounds: int = 0                 # communication rounds used by AND gates
    ots: int = 0                    # 1-out-of-4 OTs
    triples: int = 0                # Beaver triples used
    opened_bits: int = 0            # bits sent when opening d and e
    view2: list[int] = field(default_factory=list)  # bits P2 received during the gates


def ideal_ot_1_of_4(table: Sequence[int], choice: int) -> int:
    """Local ideal 1-out-of-4 OT: the receiver gets table[choice], the sender nothing."""
    return table[choice]


def dealer_triple(rng: random.Random) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """A random AND triple x*y = z, XOR-shared between the two parties."""
    x1, x2, y1, y2, z1 = (rng.getrandbits(1) for _ in range(5))
    z2 = z1 ^ ((x1 ^ x2) & (y1 ^ y2))
    return (x1, y1, z1), (x2, y2, z2)


def and_depths(circ: Circuit) -> dict[int, int]:
    """AND depth of every wire: inputs 0, XOR and INV keep the max, AND adds 1."""
    dep = {w: 0 for w in circ.inputs1 + circ.inputs2}
    for op, a, b, c in circ.gates:
        if op == "INV":
            dep[c] = dep[a]
        elif op == "XOR":
            dep[c] = max(dep[a], dep[b])
        else:
            dep[c] = max(dep[a], dep[b]) + 1
    return dep


def gmw(circ: Circuit, x: Sequence[int], y: Sequence[int], rng: random.Random,
        mode: str = "ot") -> tuple[list[int], Stats]:
    """Run two-party GMW; return the output bits and the cost counters."""
    s1: dict[int, int] = {}
    s2: dict[int, int] = {}
    st = Stats()
    for w, v in zip(circ.inputs1, x):  # @line L1
        r = rng.getrandbits(1)
        s1[w], s2[w] = v ^ r, r
        st.view2.append(r)
    for w, v in zip(circ.inputs2, y):
        r = rng.getrandbits(1)
        s1[w], s2[w] = r, v ^ r
    dep = and_depths(circ)
    depth = max((dep[g[3]] for g in circ.gates), default=0)
    for d in range(depth + 1):  # @line L2
        layer = [g for g in circ.gates if g[0] == "AND" and dep[g[3]] == d]
        if layer:
            st.rounds += 1
        for op, a, b, c in layer:  # @line L3
            if mode == "ot":
                r = rng.getrandbits(1)  # @line L4
                s1[c] = r
                table = [r ^ ((s1[a] ^ i) & (s1[b] ^ j)) for i in (0, 1) for j in (0, 1)]  # @line L5
                s2[c] = ideal_ot_1_of_4(table, 2 * s2[a] + s2[b])  # @line L6
                st.ots += 1
                st.view2.append(s2[c])
            else:
                s1[c], s2[c] = _and_with_triple(s1[a], s1[b], s2[a], s2[b], rng, st)
        for op, a, b, c in circ.gates:  # @line L7
            if op == "AND" or dep[c] != d:
                continue
            if op == "XOR":  # @line L8
                s1[c], s2[c] = s1[a] ^ s1[b], s2[a] ^ s2[b]
            else:  # @line L9
                s1[c], s2[c] = s1[a] ^ 1, s2[a]
    return [s1[w] ^ s2[w] for w in circ.outputs], st  # @line L10


def _and_with_triple(a1: int, b1: int, a2: int, b2: int, rng: random.Random, st: Stats) -> tuple[int, int]:
    """Beaver's method: open d = a XOR x and e = b XOR y, then compute shares of a AND b."""
    (x1, y1, z1), (x2, y2, z2) = dealer_triple(rng)
    st.triples += 1
    d = (a1 ^ x1) ^ (a2 ^ x2)        # each party sends its share of d and of e
    e = (b1 ^ y1) ^ (b2 ^ y2)
    st.opened_bits += 4
    st.view2 += [a1 ^ x1, b1 ^ y1]
    c1 = z1 ^ (d & y1) ^ (e & x1) ^ (d & e)
    c2 = z2 ^ (d & y2) ^ (e & x2)
    return c1, c2


def plain_eval(circ: Circuit, x: Sequence[int], y: Sequence[int]) -> list[int]:
    v = dict(zip(circ.inputs1, x)) | dict(zip(circ.inputs2, y))
    for op, a, b, c in circ.gates:
        v[c] = v[a] & v[b] if op == "AND" else v[a] ^ v[b] if op == "XOR" else 1 - v[a]
    return [v[w] for w in circ.outputs]


def random_circuit(n_in: int, n_gates: int, n_out: int, rng: random.Random) -> Circuit:
    """A random circuit with n_in input bits per party."""
    wires = list(range(2 * n_in))
    gates: list[Gate] = []
    for k in range(n_gates):
        op = rng.choice(["AND", "AND", "XOR", "INV"])
        c = 2 * n_in + k
        gates.append((op, rng.choice(wires), rng.choice(wires), c))
        wires.append(c)
    return Circuit(2 * n_in + n_gates, list(range(n_in)), list(range(n_in, 2 * n_in)), wires[-n_out:], gates)


def adder(w: int) -> Circuit:
    """Ripple-carry adder, w-bit plus w-bit, w + 1 output bits; AND depth w."""
    a, b = list(range(w)), list(range(w, 2 * w))
    nxt = 2 * w
    gates: list[Gate] = []
    outs: list[int] = []

    def new() -> int:
        nonlocal nxt
        nxt += 1
        return nxt - 1

    s0, c = new(), new()
    gates += [("XOR", a[0], b[0], s0), ("AND", a[0], b[0], c)]
    outs.append(s0)
    for i in range(1, w):
        u, v, s1, s, m, c2 = new(), new(), new(), new(), new(), new()
        gates += [("XOR", a[i], c, u), ("XOR", b[i], c, v), ("XOR", a[i], b[i], s1),
                  ("XOR", s1, c, s), ("AND", u, v, m), ("XOR", c, m, c2)]
        outs.append(s)
        c = c2
    outs.append(c)
    return Circuit(nxt, a, b, outs, gates)


def to_bits(v: int, w: int) -> list[int]:
    return [(v >> i) & 1 for i in range(w)]


def from_bits(bits: Sequence[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))
