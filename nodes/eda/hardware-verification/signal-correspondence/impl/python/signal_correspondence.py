# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-correspondence/. The authors are listed in prov/EMBMJW.jsonl.
"""Signal correspondence (van Eijk 2000): the greatest inductive set of signal equalities, with BDDs.

Random simulation from the initial state groups the latches and gates of a
product machine into candidate classes of equal signals. The classes are then
split until they hold in the initial state for every input and are preserved
by one step of the machine. Pairs of outputs in one class are then equal in
every reachable state, so the two circuits are sequentially equivalent.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from bdd import BDD
from netlist import Netlist, build_bdds, initial_state, next_state, simulate

ZERO, ONE = "#0", "#1"


@dataclass
class Result:
    proved: bool
    classes: list[list[str]]
    splits: int


def signal_nodes(p: Netlist) -> list[str]:
    """The nodes that take part: the two constants, the latches and the gates."""
    return [ZERO, ONE] + [name for name, _, _ in p.latches] + [name for name, _, _ in p.gates]


def simulation_classes(p: Netlist, cycles: int = 8, width: int = 32, seed: int = 1) -> list[list[str]]:
    """Classes of nodes with equal values on `width` random runs of `cycles` cycles from the initial state."""
    rng = random.Random(seed)
    mask = (1 << width) - 1
    state = initial_state(p, mask)
    nodes = signal_nodes(p)
    sig: dict[str, list[int]] = {n: [] for n in nodes}
    for _ in range(cycles):
        val = simulate(p, {**{x: rng.getrandbits(width) for x in p.inputs}, **state}, mask)
        val[ZERO], val[ONE] = 0, mask
        for n in nodes:
            sig[n].append(val[n])
        state = next_state(p, val)
    groups: dict[tuple[int, ...], list[str]] = {}
    for n in nodes:
        groups.setdefault(tuple(sig[n]), []).append(n)
    return list(groups.values())


def split(classes: list[list[str]], value: dict[str, int]) -> list[list[str]]:
    """Split every class by the value of its nodes at one point; the order inside a class is kept."""
    out: list[list[str]] = []
    for k in classes:
        parts: dict[int, list[str]] = {}
        for n in k:
            parts.setdefault(value[n], []).append(n)
        out.extend(parts.values())
    return out


def first_difference(bdd: BDD, classes: list[list[str]], f: dict[str, int], care: int) -> Optional[dict[int, int]]:
    """A point where care holds and some node differs from the representative of its class, or None."""
    for k in classes:
        for n in k[1:]:
            d = bdd.conj(care, bdd.xor(f[n], f[k[0]]))
            if d != 0:
                return bdd.sat_one(d)
    return None


def signal_correspondence(
    p: Netlist,
    pairs: list[tuple[str, str]],
    cycles: int = 8,
    width: int = 32,
    seed: int = 1,
    classes: Optional[list[list[str]]] = None,
) -> Result:
    """Try to prove that each pair of outputs of the product machine p is equal in every reachable state.

    Precondition: p is a netlist with latches (for example netlist.product(a, b)) and the
    pairs name its nodes. If classes is given, it replaces the simulation classes.
    Returns proved (True means equivalent; False means unknown), the final classes and
    the number of splits. Cost: at most V - 1 splits for V nodes, each after at most V
    BDD checks; a BDD can be exponential in the latches and inputs.
    """
    if classes is None:
        classes = simulation_classes(p, cycles, width, seed)  # @line L1
    classes = [list(k) for k in classes]
    n_lat, n_in = len(p.latches), len(p.inputs)
    bdd = BDD()
    s = {name: bdd.var(j) for j, (name, _, _) in enumerate(p.latches)}
    x0 = {x: bdd.var(n_lat + i) for i, x in enumerate(p.inputs)}
    x1 = {x: bdd.var(n_lat + n_in + i) for i, x in enumerate(p.inputs)}
    f0 = build_bdds(p, bdd, {**s, **x0})
    delta = {name: f0[nxt] for name, nxt, _ in p.latches}
    f1 = build_bdds(p, bdd, {**delta, **x1})
    b0 = build_bdds(p, bdd, {**{name: init for name, _, init in p.latches}, **x0})
    for f in (f0, f1, b0):
        f[ZERO], f[ONE] = 0, 1
    splits = 0
    while True:
        point = first_difference(bdd, classes, b0, 1)  # @line L2
        if point is None:
            break
        classes = split(classes, {n: bdd.evaluate(b0[n], point) for n in signal_nodes(p)})  # @line L3
        splits += 1
    while True:  # @line L4
        care = 1
        for k in classes:  # @line L5
            for n in k[1:]:
                care = bdd.conj(care, bdd.xnor(f0[n], f0[k[0]]))
        point = first_difference(bdd, classes, f1, care)  # @line L6
        if point is None:  # @line L8
            break
        classes = split(classes, {n: bdd.evaluate(f1[n], point) for n in signal_nodes(p)})  # @line L7
        splits += 1
    where = {n: i for i, k in enumerate(classes) for n in k}
    proved = all(where.get(o, o) == where.get(o2, o2) for o, o2 in pairs)  # @line L9
    return Result(proved, classes, splits)  # @line L10
