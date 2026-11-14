# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-covering-technology-mapping/. The authors are listed in prov/QGBZ88.jsonl.

"""Tree covering technology mapping in the style of DAGON (Keutzer, 1987).

The subject graph is a network of two-input NAND gates and inverters,
given as `kinds` and `fanins` in topological order: kinds[v] is "in",
"inv" or "nand", and every fanin of v is smaller than v. `outputs` lists
the nodes that drive primary outputs.

Each library gate has an area and a pattern, a tree over the same base
gates. A pattern is "x" (an input of the gate), ("inv", p) or
("nand", p, q). A pattern matches at a node when the subject graph has
the same shape below the node, with the two inputs of a NAND in either
order.

The subject graph is cut into trees at every node with more than one
fanout and at every output. Inside one tree, dynamic programming from
the leaves to the root gives the least area cover of every node:
cost(v) is the least area(g) + sum of cost(l) over a match of gate g at
v with inputs l, where cost(l) = 0 for a primary input or the root of
another tree. The total area is the sum of the costs of the tree roots.
"""

from typing import Sequence

# A toy library. The areas are made up for the examples of the page.
LIBRARY = [
    ("INV", 2, ("inv", "x")),
    ("NAND2", 3, ("nand", "x", "x")),
    ("AND2", 4, ("inv", ("nand", "x", "x"))),
    ("NOR2", 3, ("inv", ("nand", ("inv", "x"), ("inv", "x")))),
    ("OR2", 4, ("nand", ("inv", "x"), ("inv", "x"))),
    ("NAND3", 4, ("nand", "x", ("inv", ("nand", "x", "x")))),
    ("AOI21", 4, ("inv", ("nand", ("nand", "x", "x"), ("inv", "x")))),
    ("OAI21", 4, ("nand", ("nand", ("inv", "x"), ("inv", "x")), "x")),
    ("NAND4", 5, ("nand", ("inv", ("nand", "x", "x")), ("inv", ("nand", "x", "x")))),
    ("AOI22", 5, ("inv", ("nand", ("nand", "x", "x"), ("nand", "x", "x")))),
]


def live_nodes(fanins, outputs) -> set:
    """The nodes from which an output can be reached; other nodes are dead logic."""
    seen, stack = set(), list(outputs)
    while stack:
        w = stack.pop()
        if w not in seen:
            seen.add(w)
            stack.extend(fanins[w])
    return seen


def tree_roots(kinds, fanins, outputs) -> set:
    """Live gates where the subject graph is cut: more than one fanout, or an output."""
    live = live_nodes(fanins, outputs)
    cnt = [0] * len(fanins)
    for v in live:
        for u in fanins[v]:
            cnt[u] += 1
    outs = set(outputs)
    return {v for v in live if kinds[v] != "in" and (cnt[v] > 1 or v in outs)}


def matches(kinds, fanins, pat, v, inner_ok) -> list:
    """Every list of subject nodes that the inputs of pattern pat bind to at v.

    The root of the pattern is v. A node that an inner node of the
    pattern (not its root, not an input) covers must pass inner_ok.
    """
    if pat == "x":
        return [[v]]
    if kinds[v] != pat[0]:
        return []

    def sub(p, u):
        if p == "x":
            return [[u]]
        if not inner_ok(u):
            return []
        return matches(kinds, fanins, p, u, inner_ok)

    if pat[0] == "inv":
        return sub(pat[1], fanins[v][0])
    a, b = fanins[v]
    out = []
    for x, y in ((a, b), (b, a)):
        for la in sub(pat[1], x):
            for lb in sub(pat[2], y):
                out.append(la + lb)
    return out


def tree_cover(kinds: Sequence[str], fanins: Sequence[Sequence[int]], outputs: Sequence[int],
               library=LIBRARY):
    """Return (total area, cover). The cover maps a gate root to (gate name, inputs)."""
    for v, fi in enumerate(fanins):
        need = {"in": 0, "inv": 1, "nand": 2}[kinds[v]]
        if len(fi) != need or any(u >= v for u in fi):
            raise ValueError("bad subject graph at node %d" % v)
    roots = tree_roots(kinds, fanins, outputs)  # @line L1

    def inner_ok(u):  # inside the current tree: a gate that is not a tree root
        return kinds[u] != "in" and u not in roots

    def leaf_cost(u):  # @line L7
        return 0 if kinds[u] == "in" or u in roots else cost[u]

    cost: list = [0] * len(kinds)
    choice: list = [None] * len(kinds)
    for v in range(len(kinds)):  # @line L2
        if kinds[v] == "in":
            continue
        best = None  # @line L3: no match yet, cost infinite
        for name, area, pat in library:  # @line L4
            for leaves in matches(kinds, fanins, pat, v, inner_ok):
                c = area + sum(leaf_cost(u) for u in leaves)  # @line L5
                if best is None or c < best[0]:  # @line L6
                    best = (c, name, leaves)
        if best is None:
            raise ValueError("the library cannot cover node %d" % v)
        cost[v], choice[v] = best[0], (best[1], best[2])

    cover: dict = {}
    todo = [v for v in outputs if kinds[v] != "in"]  # @line L8
    while todo:  # @line L9
        v = todo.pop()  # @line L10
        if v in cover:
            continue
        cover[v] = choice[v]
        todo.extend(u for u in choice[v][1] if kinds[u] != "in")
    total = sum(area for name, area, _ in library for v in cover if cover[v][0] == name)
    return total, cover  # @line L11


def evaluate_pattern(pat, values) -> int:
    """Value of a pattern; values is an iterator over its inputs, left to right."""
    if pat == "x":
        return next(values)
    if pat[0] == "inv":
        return 1 - evaluate_pattern(pat[1], values)
    a = evaluate_pattern(pat[1], values)
    b = evaluate_pattern(pat[2], values)
    return 1 - (a & b)
