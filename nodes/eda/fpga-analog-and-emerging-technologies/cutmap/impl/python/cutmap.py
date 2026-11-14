# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutmap/. The authors are listed in prov/7KTJSE.jsonl.

"""CutMap: depth-optimal LUT mapping with fewer LUTs.

A network is a dict that maps a gate name to (op, fanins). op is one of
"AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT", "BUF". A signal that is not
a gate is a primary input. Every gate input is a signal name.

The FlowMap labels are computed from all K-feasible cuts (found by cut
enumeration, not by max-flow). Then the outputs are given the required time
D, the optimal depth, and the gates are visited in reverse topological order.
Each gate that must be a LUT root takes the K-feasible cut of least cost
among the cuts whose nodes all have label at most r(v) - 1. A cut node costs
0 if it is a primary input or already a LUT root, and 1 otherwise, so the
cost counts the new LUT roots that the cut makes.
"""

from itertools import product

GATE_OPS = {"AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT", "BUF"}


def gate_value(op: str, vals: list) -> int:
    if op in ("AND", "NAND"):
        r = int(all(vals))
    elif op in ("OR", "NOR"):
        r = int(any(vals))
    elif op in ("XOR", "XNOR"):
        r = sum(vals) % 2
    elif op in ("BUF", "NOT"):
        r = vals[0]
    else:
        raise ValueError(op)
    return 1 - r if op in ("NAND", "NOR", "XNOR", "NOT") else r


def topo_order(net: dict) -> list:
    order, state = [], {}

    def visit(s):
        if s not in net or state.get(s) == 2:
            return
        if state.get(s) == 1:
            raise ValueError("the network has a cycle")
        state[s] = 1
        for f in net[s][1]:
            visit(f)
        state[s] = 2
        order.append(s)

    for g in sorted(net):
        visit(g)
    return order


def primary_inputs(net: dict) -> list:
    return sorted({f for _, (_, fanins) in net.items() for f in fanins if f not in net})


def enumerate_cuts(net: dict, k: int) -> dict:
    """For each gate, the list of its K-feasible cuts, not counting the
    trivial cut {v}. Dominated cuts (strict supersets of another) are kept
    out."""
    cuts = {}
    for p in primary_inputs(net):
        cuts[p] = [frozenset([p])]
    for g in topo_order(net):
        fanin_choices = []
        for f in net[g][1]:
            opts = [frozenset([f])]
            if f in net:
                opts = opts + cuts[f]
            fanin_choices.append(opts)
        found = set()
        for combo in product(*fanin_choices):
            c = frozenset().union(*combo)
            if len(c) <= k:
                found.add(c)
        minimal = [c for c in found if not any(o < c for o in found)]
        cuts[g] = sorted(minimal, key=lambda c: (len(c), sorted(c)))
    return cuts


def flowmap_labels(net: dict, cuts: dict) -> dict:
    """l(PI) = 0 and l(v) = 1 + min over cuts C of v of max l(u), u in C."""
    label = {p: 0 for p in primary_inputs(net)}
    for g in topo_order(net):
        label[g] = min(1 + max(label[u] for u in c) for c in cuts[g])
    return label


def cutmap(net: dict, outputs: list, k: int, depth=None):
    """Returns (luts, depth) where luts maps a root gate to its cut."""
    for g, (op, fanins) in net.items():
        if op not in GATE_OPS or not fanins or len(fanins) > k:
            raise ValueError(f"gate {g} is not K-bounded or has a bad op")
    cuts = enumerate_cuts(net, k)
    label = flowmap_labels(net, cuts)
    gate_outs = [o for o in outputs if o in net]
    d_opt = max((label[o] for o in gate_outs), default=0)
    d = d_opt if depth is None else depth
    if d < d_opt:
        raise ValueError("the depth bound is below the optimal depth")
    required = {o: d for o in gate_outs}  # @line L1
    roots = set(gate_outs)
    luts = {}
    for v in reversed(topo_order(net)):  # @line L2
        if v not in roots:
            continue
        bound = required[v] - 1  # @line L3
        feasible = [c for c in cuts[v] if max(label[u] for u in c) <= bound]  # @line L4

        def cost(c):
            new = sum(1 for u in c if u in net and u not in roots)
            return (new, len(c), max(label[u] for u in c), sorted(c))

        best = min(feasible, key=cost)  # @line L5
        luts[v] = best  # @line L6
        for u in best:  # @line L7
            if u in net:
                roots.add(u)  # @line L8
                required[u] = min(required.get(u, d), required[v] - 1)  # @line L9
    return luts, d  # @line L10


def lut_value(net: dict, root: str, cut, values: dict) -> int:
    memo = {}

    def ev(s):
        if s in cut or s not in net:
            return values[s]
        if s not in memo:
            op, fanins = net[s]
            memo[s] = gate_value(op, [ev(f) for f in fanins])
        return memo[s]

    return ev(root)


def eval_network(net: dict, outputs: list, values: dict) -> dict:
    memo = dict(values)

    def ev(s):
        if s not in memo:
            op, fanins = net[s]
            memo[s] = gate_value(op, [ev(f) for f in fanins])
        return memo[s]

    return {o: ev(o) for o in outputs}


def eval_luts(net: dict, luts: dict, outputs: list, values: dict) -> dict:
    memo = dict(values)

    def ev(s):
        if s not in memo:
            cut = luts[s]
            memo[s] = lut_value(net, s, cut, {u: ev(u) for u in cut})
        return memo[s]

    return {o: ev(o) for o in outputs}


def lut_depth(net: dict, luts: dict, outputs: list) -> int:
    memo = {}

    def dep(s):
        if s not in net:
            return 0
        if s not in memo:
            memo[s] = 1 + max(dep(u) for u in luts[s])
        return memo[s]

    return max((dep(o) for o in outputs), default=0)


def equivalent(net: dict, luts: dict, outputs: list) -> bool:
    pis = primary_inputs(net)
    for bits in product((0, 1), repeat=len(pis)):
        values = dict(zip(pis, bits))
        if eval_network(net, outputs, values) != eval_luts(net, luts, outputs, values):
            return False
    return True


if __name__ == "__main__":
    from_page = {
        "g0": ("XOR", ["c", "b"]),
        "g1": ("OR", ["d", "b"]),
        "g2": ("OR", ["g1", "g0"]),
        "g3": ("XOR", ["g2", "a"]),
    }
    luts, d = cutmap(from_page, ["g3"], 3)
    print(d, {v: sorted(c) for v, c in luts.items()})
