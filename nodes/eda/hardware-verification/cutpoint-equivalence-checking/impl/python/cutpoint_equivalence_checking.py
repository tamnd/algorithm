# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutpoint-equivalence-checking/. The authors are listed in prov/MX8Z1M.jsonl.
"""Cutpoint-based combinational equivalence checking (Kuehlmann and Krohm 1997), with BDDs.

Internal nodes of the two circuits that have the same simulation values are
candidates. When a candidate pair is proved equal, the pair gets a fresh cut
variable, and later BDDs use that variable in place of the function of the pair.
A difference that still depends on a cut variable may be a false negative, so
the cut variables in it are composed back (the cut moves toward the inputs)
until the difference is 0 or depends on primary inputs only.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from bdd import BDD
from netlist import Netlist, bdd_op, product, simulate


@dataclass
class Result:
    equivalent: bool
    counterexample: Optional[dict[str, int]]
    merges: int
    false_negatives: int


def resolve(bdd: BDD, g: int, definition: dict[int, int]) -> tuple[int, bool]:
    """Compose cut variables back into g until g is 0 or has no cut variable.

    definition maps each cut variable to its function over smaller variables.
    Returns the final g and True if g was nonzero over a cut variable and became 0.
    """
    start_nonzero = g != 0
    while g != 0:  # @line L14
        cuts = [v for v in bdd.support(g) if v in definition]
        if not cuts:
            break
        v = max(cuts)  # @line L15
        g = bdd.compose(g, v, definition[v])  # @line L16
    return g, start_nonzero and g == 0  # @line L17


def cutpoint_equivalence(a: Netlist, b: Netlist, width: int = 64, seed: int = 1) -> Result:
    """Decide whether the combinational circuits a and b compute the same outputs.

    Precondition: a and b have the same primary inputs, the same number of outputs and no latches.
    Returns equivalent, a distinguishing input vector when they differ, the number of
    proved merges and the number of differences that were false negatives of a cut.
    Cost: O(N + P C) BDD operations for N gates, P compared pairs and C cut variables;
    each operation is polynomial in the BDD sizes, which can be exponential in the inputs.
    """
    p, pairs = product(a, b)
    bdd = BDD()
    cut_var = {x: i for i, x in enumerate(p.inputs)}  # @line L1
    f = {x: bdd.var(i) for x, i in cut_var.items()}
    raw = dict(f)
    definition: dict[int, int] = {}
    next_var = len(p.inputs)
    rng = random.Random(seed)
    mask = (1 << width) - 1
    sig = simulate(p, {x: rng.getrandbits(width) for x in p.inputs}, mask)  # @line L2
    first: dict[int, str] = {}
    for x in p.inputs:
        first.setdefault(sig[x], x)
    merges = 0
    false_negatives = 0
    for name, op, fanins in p.gates:  # @line L3
        raw[name] = bdd_op(bdd, op, [f[x] for x in fanins])  # @line L4
        f[name] = raw[name]  # @line L5
        r = first.setdefault(sig[name], name)
        if r == name:  # @line L6
            continue
        g, was_false = resolve(bdd, bdd.xor(raw[name], raw[r]), definition)  # @line L7
        false_negatives += was_false
        if g != 0:
            continue
        if r not in cut_var:  # @line L8
            cut_var[r] = next_var
            definition[next_var] = raw[r]
            f[r] = bdd.var(next_var)
            next_var += 1
        f[name] = bdd.var(cut_var[r])  # @line L9
        merges += 1
    for o, o2 in pairs:  # @line L10
        g, was_false = resolve(bdd, bdd.xor(f[o], f[o2]), definition)  # @line L11
        false_negatives += was_false
        if g != 0:  # @line L12
            point = bdd.sat_one(g) or {}
            cex = {x: point.get(i, 0) for i, x in enumerate(p.inputs)}
            return Result(False, cex, merges, false_negatives)
    return Result(True, None, merges, false_negatives)  # @line L13
