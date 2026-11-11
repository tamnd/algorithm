# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-garbled-circuits/. The authors are listed in prov/7XSXVN.jsonl.
"""Yao's garbled circuits with point-and-permute, free XOR and half gates.

A circuit is a list of gates (op, a, b, c) on integer wire ids, in
topological order. op is "AND", "XOR" or "INV" (for INV, b is ignored).
Labels are KAPPA-bit integers. The global offset DELTA has lsb 1, and every
wire w has labels W_w^0 and W_w^1 = W_w^0 XOR DELTA (free XOR). The
permute bit of a wire is lsb(W_w^0).

Three ways to garble an AND gate, for comparison:
  "classic": point-and-permute, 4 ciphertexts (Beaver, Micali, Rogaway 1990)
  "grr3":    row reduction, 3 ciphertexts (Naor, Pinkas, Sumner 1999)
  "half":    half gates, 2 ciphertexts (Zahur, Rosulek, Evans 2015)
All three use free XOR (Kolesnikov and Schneider 2008), so XOR and INV
gates cost nothing.

H is SHA-256 truncated to KAPPA bits, with the gate index as a tweak. The
security proofs model H as a circular correlation robust hash or a random
oracle. The evaluator's input labels come from a local ideal OT.

For study only. The code is not constant time, uses Python's random module
for labels, and is not a secure computation library; use a maintained one
such as EMP-toolkit or MP-SPDZ for real data.
"""

import hashlib
import random
from dataclasses import dataclass, field
from typing import Sequence

KAPPA = 128
MASK = (1 << KAPPA) - 1

Gate = tuple[str, int, int, int]


@dataclass
class Circuit:
    """Wires 0..n_wires-1. Garbler inputs, evaluator inputs, outputs and gates."""

    n_wires: int
    garbler_inputs: list[int]
    evaluator_inputs: list[int]
    outputs: list[int]
    gates: list[Gate]


def H(*parts: int) -> int:
    """KAPPA-bit hash of integers (labels and a tweak)."""
    data = b"".join(p.to_bytes(KAPPA // 8 + 4, "big") for p in parts)
    return int.from_bytes(hashlib.sha256(data).digest()[: KAPPA // 8], "big")


def lsb(x: int) -> int:
    return x & 1


@dataclass
class Garbled:
    """What the garbler sends: tables for AND gates and output decoding bits."""

    tables: dict[int, tuple[int, ...]] = field(default_factory=dict)
    decode: list[int] = field(default_factory=list)


@dataclass
class GarblerSecrets:
    delta: int
    zero_labels: dict[int, int]

    def label(self, w: int, v: int) -> int:
        return self.zero_labels[w] ^ (self.delta if v else 0)


# ---------------------------------------------------------------- garbling


def garble(circ: Circuit, rng: random.Random, mode: str = "half") -> tuple[Garbled, GarblerSecrets]:
    """Garble circ. Returns the garbled circuit and the garbler's secrets."""
    delta = rng.getrandbits(KAPPA) | 1  # @line L1
    w0: dict[int, int] = {}
    for w in circ.garbler_inputs + circ.evaluator_inputs:  # @line L2
        w0[w] = rng.getrandbits(KAPPA)
    gc = Garbled()
    for j, (op, a, b, c) in enumerate(circ.gates):  # @line L3
        if op == "XOR":  # @line L4
            w0[c] = w0[a] ^ w0[b]
        elif op == "INV":  # @line L5
            w0[c] = w0[a] ^ delta
        elif op == "AND":  # @line L6
            if mode == "half":
                w0[c], gc.tables[j] = _garble_half(w0[a], w0[b], delta, j)
            elif mode == "classic":
                w0[c], gc.tables[j] = _garble_classic(w0[a], w0[b], delta, j, rng)
            elif mode == "grr3":
                w0[c], gc.tables[j] = _garble_grr3(w0[a], w0[b], delta, j)
            else:
                raise ValueError(mode)
        else:
            raise ValueError(op)
    gc.decode = [lsb(w0[w]) for w in circ.outputs]  # @line L13
    return gc, GarblerSecrets(delta, w0)  # @line L14


def _garble_half(wa0: int, wb0: int, delta: int, j: int) -> tuple[int, tuple[int, int]]:
    """Two half gates: 2 ciphertexts per AND gate."""
    wa1, wb1 = wa0 ^ delta, wb0 ^ delta
    pa, pb = lsb(wa0), lsb(wb0)  # @line L7
    tg = H(wa0, 2 * j) ^ H(wa1, 2 * j) ^ (delta if pb else 0)  # @line L8
    wg = H(wa0, 2 * j) ^ (tg if pa else 0)  # @line L9
    te = H(wb0, 2 * j + 1) ^ H(wb1, 2 * j + 1) ^ wa0  # @line L10
    we = H(wb0, 2 * j + 1) ^ ((te ^ wa0) if pb else 0)  # @line L11
    return wg ^ we, (tg, te)  # @line L12


def _garble_classic(wa0: int, wb0: int, delta: int, j: int, rng: random.Random) -> tuple[int, tuple[int, ...]]:
    """Point-and-permute: 4 rows, row 2*lsb(Wa^x) + lsb(Wb^y) holds Enc(Wc^(x AND y))."""
    wc0 = rng.getrandbits(KAPPA)
    rows = [0, 0, 0, 0]
    for x in (0, 1):
        for y in (0, 1):
            wa, wb = wa0 ^ (delta if x else 0), wb0 ^ (delta if y else 0)
            wc = wc0 ^ (delta if x & y else 0)
            rows[2 * lsb(wa) + lsb(wb)] = H(wa, wb, j) ^ wc
    return wc0, tuple(rows)


def _garble_grr3(wa0: int, wb0: int, delta: int, j: int) -> tuple[int, tuple[int, ...]]:
    """Row reduction: choose the output label so that row 0 is all zero, send rows 1..3."""
    pa, pb = lsb(wa0), lsb(wb0)
    # Row 0 is for the labels with lsb 0, that is the values x = pa and y = pb.
    wc_row0 = H(wa0 ^ (delta if pa else 0), wb0 ^ (delta if pb else 0), j)
    wc0 = wc_row0 ^ (delta if pa & pb else 0)
    rows = [0, 0, 0, 0]
    for x in (0, 1):
        for y in (0, 1):
            wa, wb = wa0 ^ (delta if x else 0), wb0 ^ (delta if y else 0)
            wc = wc0 ^ (delta if x & y else 0)
            rows[2 * lsb(wa) + lsb(wb)] = H(wa, wb, j) ^ wc
    assert rows[0] == 0
    return wc0, tuple(rows[1:])


# ---------------------------------------------------------------- evaluation


def evaluate(circ: Circuit, gc: Garbled, labels: dict[int, int], mode: str = "half") -> list[int]:
    """Evaluate with one label per input wire; return the output bits."""
    x = dict(labels)
    for j, (op, a, b, c) in enumerate(circ.gates):  # @line L15
        if op == "XOR":  # @line L16
            x[c] = x[a] ^ x[b]
        elif op == "INV":  # @line L17
            x[c] = x[a]
        elif mode == "half":
            sa, sb = lsb(x[a]), lsb(x[b])  # @line L18
            tg, te = gc.tables[j]
            x[c] = H(x[a], 2 * j) ^ (tg if sa else 0) ^ H(x[b], 2 * j + 1) ^ ((te ^ x[a]) if sb else 0)  # @line L19
        elif mode == "classic":
            x[c] = gc.tables[j][2 * lsb(x[a]) + lsb(x[b])] ^ H(x[a], x[b], j)
        else:  # grr3
            r = 2 * lsb(x[a]) + lsb(x[b])
            x[c] = H(x[a], x[b], j) ^ (gc.tables[j][r - 1] if r else 0)
    return [lsb(x[w]) ^ d for w, d in zip(circ.outputs, gc.decode)]  # @line L20


# ---------------------------------------------------------------- the protocol


def ideal_ot(m0: int, m1: int, choice: int) -> int:
    """A local ideal 1-out-of-2 OT: the receiver gets m_choice, the sender nothing."""
    return m1 if choice else m0


def yao_protocol(circ: Circuit, x: Sequence[int], y: Sequence[int], rng: random.Random,
                 mode: str = "half") -> list[int]:
    """Semi-honest two-party Yao: the garbler has bits x, the evaluator bits y."""
    gc, sec = garble(circ, rng, mode)  # @line L21
    labels = {w: sec.label(w, v) for w, v in zip(circ.garbler_inputs, x)}
    for w, v in zip(circ.evaluator_inputs, y):  # @line L22
        labels[w] = ideal_ot(sec.label(w, 0), sec.label(w, 1), v)
    return evaluate(circ, gc, labels, mode)  # @line L23


def ciphertexts_per_and(circ: Circuit, gc: Garbled) -> set[int]:
    return {len(gc.tables[j]) for j, g in enumerate(circ.gates) if g[0] == "AND"}


# ---------------------------------------------------------------- circuits


def plain_eval(circ: Circuit, x: Sequence[int], y: Sequence[int]) -> list[int]:
    """Evaluate the circuit in the clear."""
    v = dict(zip(circ.garbler_inputs, x)) | dict(zip(circ.evaluator_inputs, y))
    for op, a, b, c in circ.gates:
        v[c] = v[a] & v[b] if op == "AND" else v[a] ^ v[b] if op == "XOR" else 1 - v[a]
    return [v[w] for w in circ.outputs]


def comparator(w: int) -> Circuit:
    """Outputs [a > b] and [a <= b] for w-bit a (garbler) and b (evaluator).

    c_0 = 0 and c_{t+1} = a_t XOR ((a_t XOR c_t) AND (b_t XOR c_t)), bits
    from the least significant; one AND gate per bit."""
    a = list(range(w))
    b = list(range(w, 2 * w))
    nxt = 2 * w
    gates: list[Gate] = []

    def new() -> int:
        nonlocal nxt
        nxt += 1
        return nxt - 1

    t = new()
    gates.append(("AND", a[0], b[0], t))
    c = new()
    gates.append(("XOR", a[0], t, c))
    for i in range(1, w):
        u, v, m, c2 = new(), new(), new(), new()
        gates += [("XOR", a[i], c, u), ("XOR", b[i], c, v), ("AND", u, v, m), ("XOR", a[i], m, c2)]
        c = c2
    le = new()
    gates.append(("INV", c, 0, le))
    return Circuit(nxt, a, b, [c, le], gates)


def adder(w: int) -> Circuit:
    """Ripple-carry adder: w-bit a (garbler) plus w-bit b (evaluator), w + 1 output bits.

    s_t = a_t XOR b_t XOR c_t and c_{t+1} = c_t XOR ((a_t XOR c_t) AND (b_t XOR c_t))."""
    a = list(range(w))
    b = list(range(w, 2 * w))
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
