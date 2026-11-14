# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daomap/. The authors are listed in prov/HAXQH6.jsonl.

"""DAOmap: depth-optimal LUT mapping with area flow, slack and iterative cut selection.

A network is a dict that maps a gate name to (op, fanins). op is one of
"AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT", "BUF". A signal that is not
a gate is a primary input.

This is a simplified DAOmap. It keeps the parts of the paper that decide the
depth and most of the area:
  - cut enumeration with the minimum arrival time of each node;
  - area flow A_C = sum A_i / f(i) + U_C + duplication cost, with U_C = 1;
  - the duplication cost N_f / |C| for each multi-fanout fanin f whose cone
    the cut covers;
  - required times from the optimal depth, and the slack of a cut;
  - for a non-critical node, the cost A_C / share - 0.3 * slack_C, where
    share counts the inputs of C that are LUT roots (1.15 for one input);
  - a few iterations of cut selection, where each iteration uses the
    multi-fanout roots of the last one as tentative roots.
It leaves out the U_C formula of the paper (cut size, covered nodes, root
fanout and reconvergent paths) and the cut probing step.
"""

from itertools import product

GATE_OPS = {"AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT", "BUF"}
SLACK_WEIGHT = 0.3
ONE_SHARE = 1.15


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


def fanouts(net: dict, outputs: list) -> dict:
    count = {}
    for _, (_, fanins) in net.items():
        for f in set(fanins):
            count[f] = count.get(f, 0) + 1
    for o in outputs:
        count[o] = count.get(o, 0) + 1
    return count


def enumerate_cuts(net: dict, k: int) -> dict:
    """The K-feasible cuts of each gate without the trivial cut, with
    dominated cuts removed."""
    cuts = {p: [frozenset([p])] for p in primary_inputs(net)}
    for g in topo_order(net):
        choices = []
        for f in net[g][1]:
            opts = [frozenset([f])]
            if f in net:
                opts = opts + cuts[f]
            choices.append(opts)
        found = set()
        for combo in product(*choices):
            c = frozenset().union(*combo)
            if len(c) <= k:
                found.add(c)
        minimal = [c for c in found if not any(o < c for o in found)]
        cuts[g] = sorted(minimal, key=lambda c: (len(c), sorted(c)))
    return cuts


def cone(net: dict, v: str, cut) -> set:
    """The gates computed inside the LUT of v over cut, v included."""
    seen, stack = set(), [v]
    while stack:
        s = stack.pop()
        if s in cut or s in seen or s not in net:
            continue
        seen.add(s)
        stack.extend(net[s][1])
    return seen


def arrival_and_area(net: dict, outputs: list, cuts: dict):
    """Minimum arrival time arr(v), and area flow A(v) taken over the cuts
    that give arr(v). Returns (arr, area, cut_area)."""
    fo = fanouts(net, outputs)
    arr = {p: 0 for p in primary_inputs(net)}
    area = {p: 0.0 for p in primary_inputs(net)}
    cut_area = {}
    for v in topo_order(net):
        arr[v] = min(1 + max(arr[u] for u in c) for c in cuts[v])
        for c in cuts[v]:
            a = sum(area[u] / max(1, fo.get(u, 1)) for u in c) + 1.0
            for f in set(net[v][1]):
                if f in net and f not in c and fo.get(f, 0) > 1:
                    a += len(cone(net, f, c)) / len(c)
            cut_area[(v, c)] = a
        area[v] = min(cut_area[(v, c)] for c in cuts[v] if 1 + max(arr[u] for u in c) == arr[v])
    return arr, area, cut_area


def select_cuts(net, outputs, cuts, arr, cut_area, d, tentative):
    """One pass of cut selection from the outputs. Returns the LUTs."""
    gate_outs = [o for o in outputs if o in net]
    required = {o: d for o in gate_outs}  # @line L4
    roots = set(gate_outs)
    luts = {}
    for v in reversed(topo_order(net)):  # @line L5
        if v not in roots:
            continue

        def slack(c):
            return required[v] - 1 - max(arr[u] for u in c)

        if required[v] == arr[v]:  # @line L6
            crit = [c for c in cuts[v] if slack(c) == 0]
            best = min(crit, key=lambda c: (cut_area[(v, c)], sorted(c)))
        else:

            def cost(c):  # @line L7
                shared = sum(1 for u in c if u in roots or u in tentative)
                share = 1.0 if shared == 0 else ONE_SHARE if shared == 1 else float(shared)
                return (cut_area[(v, c)] / share - SLACK_WEIGHT * slack(c), sorted(c))

            best = min((c for c in cuts[v] if slack(c) >= 0), key=cost)
        luts[v] = best  # @line L8
        for u in best:
            if u in net:
                roots.add(u)
                required[u] = min(required.get(u, d), required[v] - 1)
    return luts


def daomap(net: dict, outputs: list, k: int, iterations: int = 3):
    """Returns (luts, depth). luts maps each LUT root to its cut."""
    for g, (op, fanins) in net.items():
        if op not in GATE_OPS or not fanins or len(fanins) > k:
            raise ValueError(f"gate {g} is not K-bounded or has a bad op")
    cuts = enumerate_cuts(net, k)  # @line L1
    arr, _, cut_area = arrival_and_area(net, outputs, cuts)
    fo = fanouts(net, outputs)
    d = max((arr[o] for o in outputs if o in net), default=0)  # @line L2
    tentative = {g for g in net if fo.get(g, 0) > 3}
    best = None
    for _ in range(iterations):  # @line L3
        luts = select_cuts(net, outputs, cuts, arr, cut_area, d, tentative)
        if best is None or len(luts) < len(best):  # @line L9
            best = luts
        tentative = {g for g in luts if fo.get(g, 0) > 1}
    return best, d  # @line L10


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
    example = {
        "g0": ("OR", ["c", "d"]),
        "g1": ("AND", ["b", "d"]),
        "g2": ("AND", ["g1", "g0"]),
        "g3": ("OR", ["g1", "a"]),
        "g4": ("XOR", ["a", "g2"]),
    }
    luts, d = daomap(example, ["g3", "g4"], 3)
    print(d, {v: sorted(c) for v, c in sorted(luts.items())})
