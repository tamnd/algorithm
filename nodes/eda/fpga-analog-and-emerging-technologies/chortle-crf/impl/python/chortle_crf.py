# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chortle-crf/. The authors are listed in prov/H1WBNA.jsonl.

"""Chortle-crf: map a network of AND, OR and XOR gates into K-input LUTs.

A network is a dict that maps a gate name to (op, fanins), where op is
"AND", "OR" or "XOR" and fanins is a list of signal names. A signal that is
not a gate is a primary input. The outputs are a list of gate names.

The network is cut into fanout-free trees at every gate that is an output or
has more than one reader. Each tree is mapped bottom up. At a gate, the root
LUTs of the children and the leaf inputs are packed into bins of size K by
first-fit decreasing, and then the bins are joined into one root LUT. Every
gate keeps one solution: the fewest LUTs, and among those the smallest root.

A LUT is (name, inputs, expr). expr is a signal name or (op, [expr, ...]).
"""

from itertools import product

OPS = {"AND", "OR", "XOR"}


def fanout_counts(net: dict, outputs: list) -> dict:
    count = {}
    for name, (_, fanins) in net.items():
        for f in fanins:
            count[f] = count.get(f, 0) + 1
    for o in outputs:
        count[o] = count.get(o, 0) + 1
    return count


def tree_roots(net: dict, outputs: list) -> list:
    """Gates that start a tree: the outputs and every gate with fanout above 1."""
    count = fanout_counts(net, outputs)
    roots = [g for g in net if g in outputs or count.get(g, 0) > 1]
    return roots


class _Item:
    """A packable item: a child root LUT that is still open, or a wire."""

    __slots__ = ("size", "expr", "inputs")

    def __init__(self, size, expr, inputs):
        self.size = size
        self.expr = expr
        self.inputs = inputs


def _join(op, items):
    if len(items) == 1:
        return items[0].expr
    return (op, [it.expr for it in items])


def _inputs(items):
    out = set()
    for it in items:
        out |= it.inputs
    return out


def ffd_bins(sizes: list, k: int) -> list:
    """First-fit decreasing. Returns the bins as lists of item indices, and
    the bins are in the order they were opened."""
    order = sorted(range(len(sizes)), key=lambda i: (-sizes[i], i))
    bins, room = [], []
    for i in order:
        for b in range(len(bins)):
            if room[b] >= sizes[i]:
                bins[b].append(i)
                room[b] -= sizes[i]
                break
        else:
            bins.append([i])
            room.append(k - sizes[i])
    return bins


def map_node(op, children, k, namer):
    """Decompose one gate. children is a list of _Item. Returns
    (closed_luts, root_item), where closed_luts are the new LUTs that this
    gate closes and root_item is the open root LUT of the gate."""
    sizes = [c.size for c in children]
    if any(s > k for s in sizes):
        raise ValueError("an item is larger than K")
    packed = ffd_bins(sizes, k)  # @line L5
    groups = [[children[i] for i in b] for b in packed]  # @line L6
    bins = [[sum(c.size for c in g), g] for g in groups]
    closed = []
    while len(bins) > 1:  # @line L7
        # close the fullest bin (ties: the one opened first)
        j = max(range(len(bins)), key=lambda b: (bins[b][0], -b))
        size, g = bins.pop(j)
        name = namer()
        closed.append((name, sorted(_inputs(g)), _join(op, g)))  # @line L8
        wire = _Item(1, name, {name})
        # put its output in the fullest bin that still has room
        fit = [b for b in range(len(bins)) if bins[b][0] + 1 <= k]
        if fit:  # @line L9
            b = max(fit, key=lambda b: (bins[b][0], -b))
            bins[b][0] += 1
            bins[b][1].append(wire)
        else:
            bins.append([1, [wire]])
    size, g = bins[0]
    return closed, _Item(size, _join(op, g), _inputs(g))  # @line L10


def chortle_crf(net: dict, outputs: list, k: int) -> list:
    """Map the network. Returns the list of LUTs. The LUT of a tree root has
    the name of that root, so every output keeps its name."""
    if k < 2:
        raise ValueError("K must be at least 2")
    for name, (op, fanins) in net.items():
        if op not in OPS or not fanins:
            raise ValueError(f"bad gate {name}")
    roots = set(tree_roots(net, outputs))
    luts = []
    counter = [0]

    def namer():
        counter[0] += 1
        return f"_lut{counter[0]}"

    def solve(g):
        op, fanins = net[g]
        children = []  # @line L1
        for f in fanins:  # @line L2
            if f in net and f not in roots:
                children.append(solve(f))  # @line L3
            else:
                children.append(_Item(1, f, {f}))  # @line L4
        closed, root = map_node(op, children, k, namer)
        luts.extend(closed)
        return root

    for r in sorted(roots):
        root = solve(r)
        luts.append((r, sorted(root.inputs), root.expr))
    return luts


def eval_expr(expr, values: dict) -> int:
    if isinstance(expr, str):
        return values[expr]
    op, args = expr
    vals = [eval_expr(a, values) for a in args]
    if op == "AND":
        return int(all(vals))
    if op == "OR":
        return int(any(vals))
    r = 0
    for v in vals:
        r ^= v
    return r


def eval_network(net: dict, outputs: list, values: dict) -> dict:
    memo = dict(values)

    def ev(s):
        if s not in memo:
            op, fanins = net[s]
            memo[s] = eval_expr((op, list(fanins)), {f: ev(f) for f in fanins})
        return memo[s]

    return {o: ev(o) for o in outputs}


def eval_luts(luts: list, outputs: list, values: dict) -> dict:
    by_name = {name: (inputs, expr) for name, inputs, expr in luts}
    memo = dict(values)

    def ev(s):
        if s not in memo:
            inputs, expr = by_name[s]
            memo[s] = eval_expr(expr, {i: ev(i) for i in inputs})
        return memo[s]

    return {o: ev(o) for o in outputs}


def primary_inputs(net: dict) -> list:
    pis = set()
    for _, (_, fanins) in net.items():
        for f in fanins:
            if f not in net:
                pis.add(f)
    return sorted(pis)


def equivalent(net: dict, outputs: list, luts: list, rng=None, samples: int = 512) -> bool:
    """Compare on every input vector, or on random vectors from rng when
    there are more than 12 inputs."""
    pis = primary_inputs(net)
    if len(pis) <= 12 or rng is None:
        vectors = product((0, 1), repeat=len(pis))
    else:
        vectors = (tuple(rng.randint(0, 1) for _ in pis) for _ in range(samples))
    for bits in vectors:
        values = dict(zip(pis, bits))
        if eval_network(net, outputs, values) != eval_luts(luts, outputs, values):
            return False
    return True


if __name__ == "__main__":
    # the example of the page: f = OR(AND(a, b, c), AND(d, e), g, h), K = 4
    net = {"x": ("AND", ["a", "b", "c"]), "y": ("AND", ["d", "e"]), "f": ("OR", ["x", "y", "g", "h"])}
    for lut in chortle_crf(net, ["f"], 4):
        print(lut)
