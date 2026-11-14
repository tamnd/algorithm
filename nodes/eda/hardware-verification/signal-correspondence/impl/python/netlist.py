# SPDX-License-Identifier: MIT
# Shared helper of the hv1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Gate netlists with optional latches: bit-parallel simulation, BDDs of nodes, and two-circuit products.

A gate is (name, op, fanins). The gates are in topological order. A latch is
(name, next-state node, initial value). Fanins and next-state nodes name
primary inputs, latches or gates.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from bdd import BDD

OPS = ("AND", "OR", "NAND", "NOR", "XOR", "XNOR", "NOT", "BUF", "CONST0", "CONST1")
BINARY_OPS = ("AND", "OR", "NAND", "NOR", "XOR", "XNOR")


@dataclass(frozen=True)
class Netlist:
    inputs: tuple[str, ...]
    gates: tuple[tuple[str, str, tuple[str, ...]], ...]
    outputs: tuple[str, ...]
    latches: tuple[tuple[str, str, int], ...] = ()


def eval_op(op: str, vals: list[int], mask: int) -> int:
    """The value of one gate on bit-parallel words; mask has a 1 in every used bit."""
    if op == "CONST0":
        return 0
    if op == "CONST1":
        return mask
    if op in ("BUF", "NOT"):
        r = vals[0]
    elif op in ("AND", "NAND"):
        r = mask
        for v in vals:
            r &= v
    elif op in ("OR", "NOR"):
        r = 0
        for v in vals:
            r |= v
    elif op in ("XOR", "XNOR"):
        r = 0
        for v in vals:
            r ^= v
    else:
        raise ValueError(op)
    if op in ("NOT", "NAND", "NOR", "XNOR"):
        r ^= mask
    return r & mask


def simulate(net: Netlist, values: dict[str, int], mask: int) -> dict[str, int]:
    """Values of all nodes, given words for the primary inputs and the latches. Cost O(gates + pins)."""
    val = dict(values)
    for name, op, fanins in net.gates:
        val[name] = eval_op(op, [val[f] for f in fanins], mask)
    return val


def next_state(net: Netlist, val: dict[str, int]) -> dict[str, int]:
    """The next value of every latch, from the node values of simulate."""
    return {name: val[nxt] for name, nxt, _ in net.latches}


def initial_state(net: Netlist, mask: int) -> dict[str, int]:
    """The initial value of every latch, copied into every used bit."""
    return {name: (mask if init else 0) for name, _, init in net.latches}


def bdd_op(bdd: BDD, op: str, args: list[int]) -> int:
    """The BDD of one gate applied to the BDDs of its fanins."""
    if op == "CONST0":
        return 0
    if op == "CONST1":
        return 1
    if op in ("BUF", "NOT"):
        r = args[0]
    elif op in ("AND", "NAND"):
        r = 1
        for a in args:
            r = bdd.conj(r, a)
    elif op in ("OR", "NOR"):
        r = 0
        for a in args:
            r = bdd.disj(r, a)
    elif op in ("XOR", "XNOR"):
        r = 0
        for a in args:
            r = bdd.xor(r, a)
    else:
        raise ValueError(op)
    if op in ("NOT", "NAND", "NOR", "XNOR"):
        r = bdd.neg(r)
    return r


def build_bdds(net: Netlist, bdd: BDD, leaves: dict[str, int]) -> dict[str, int]:
    """BDDs of all nodes, given the BDDs of the primary inputs and the latches."""
    f = dict(leaves)
    for name, op, fanins in net.gates:
        f[name] = bdd_op(bdd, op, [f[x] for x in fanins])
    return f


def product(a: Netlist, b: Netlist) -> tuple[Netlist, list[tuple[str, str]]]:
    """The product of a and b on shared primary inputs, and the pairs of matching outputs.

    The latches and gates of a get the prefix "a." and those of b the prefix "b.".
    """
    if a.inputs != b.inputs or len(a.outputs) != len(b.outputs):
        raise ValueError("the circuits must have the same inputs and the same number of outputs")
    ins = set(a.inputs)

    def ren(p: str, n: str) -> str:
        return n if n in ins else p + n

    gates = [(ren("a.", n), op, tuple(ren("a.", x) for x in fs)) for n, op, fs in a.gates]
    gates += [(ren("b.", n), op, tuple(ren("b.", x) for x in fs)) for n, op, fs in b.gates]
    latches = [(ren("a.", n), ren("a.", nx), i) for n, nx, i in a.latches]
    latches += [(ren("b.", n), ren("b.", nx), i) for n, nx, i in b.latches]
    oa = [ren("a.", o) for o in a.outputs]
    ob = [ren("b.", o) for o in b.outputs]
    return Netlist(a.inputs, tuple(gates), tuple(oa + ob), tuple(latches)), list(zip(oa, ob))


def random_netlist(rng: random.Random, n_inputs: int, n_latches: int, n_gates: int, n_outputs: int) -> Netlist:
    """A random netlist; every latch reads a random node and has a random initial value."""
    inputs = tuple(f"x{i}" for i in range(n_inputs))
    latches = [f"q{i}" for i in range(n_latches)]
    pool = list(inputs) + latches
    gates = []
    for k in range(n_gates):
        op = rng.choice(BINARY_OPS + ("NOT",))
        if op == "NOT":
            fanins: tuple[str, ...] = (rng.choice(pool),)
        else:
            fanins = (rng.choice(pool), rng.choice(pool))
        name = f"g{k}"
        gates.append((name, op, fanins))
        pool.append(name)
    nodes = pool[n_inputs:] or pool
    outputs = tuple(rng.choice(nodes) for _ in range(n_outputs))
    lat = tuple((q, rng.choice(nodes), rng.randrange(2)) for q in latches)
    return Netlist(inputs, tuple(gates), outputs, lat)


def rewrite(net: Netlist, rng: random.Random) -> Netlist:
    """An equivalent netlist: some gates are rewritten by De Morgan's laws, with new NOT gates."""
    gates = []
    for name, op, fanins in net.gates:
        if len(fanins) == 2 and op in ("AND", "OR", "NAND", "NOR") and rng.random() < 0.6:
            na, nb = name + "_n0", name + "_n1"
            gates.append((na, "NOT", (fanins[0],)))
            gates.append((nb, "NOT", (fanins[1],)))
            dual = {"AND": "NOR", "OR": "NAND", "NAND": "OR", "NOR": "AND"}[op]
            gates.append((name, dual, (na, nb)))
        elif op == "XOR" and rng.random() < 0.6:
            na = name + "_n0"
            gates.append((na, "NOT", (fanins[0],)))
            gates.append((name, "XNOR", (na, fanins[1])))
        else:
            gates.append((name, op, fanins))
    return Netlist(net.inputs, tuple(gates), net.outputs, net.latches)


def mutate(net: Netlist, rng: random.Random) -> Netlist:
    """A netlist with the operator of one random two-input gate changed; it may or may not be equivalent."""
    idx = [k for k, (_, _, fs) in enumerate(net.gates) if len(fs) == 2]
    if not idx:
        return net
    k = rng.choice(idx)
    name, op, fanins = net.gates[k]
    new_op = rng.choice([o for o in BINARY_OPS if o != op])
    gates = list(net.gates)
    gates[k] = (name, new_op, fanins)
    return Netlist(net.inputs, tuple(gates), net.outputs, net.latches)
