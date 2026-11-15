# SPDX-License-Identifier: MIT
"""Pettis-Hansen code positioning.

Basic block positioning: a control-flow graph is a list of blocks (the
first one is the entry) and a dict from edge (a, b) to its profile weight.
chain_blocks merges blocks into chains along the heaviest edges first,
order_chains puts the chains in a sequence, and layout gives the final
order. fallthrough_weight is the weight of the edges that become fall
throughs, the quantity the layout tries to make large.

Procedure positioning: closest_is_best orders the procedures of a call
graph by merging groups along the heaviest call edges first, and joins two
groups so that the two procedures of the edge end up as close as possible.

apply_layout puts the blocks of a toy IR program (toyir.py) in a new order.
"""

from itertools import permutations

import toyir


def chain_blocks(blocks, weight):
    """The chains of Pettis and Hansen's bottom-up block positioning.

    An edge a -> b joins the chain that ends in a to the chain that starts
    with b, when the two chains differ and b is not the entry. Edges are
    taken in order of decreasing weight, ties in the order of weight's keys.
    Returns the list of chains, each a list of blocks.
    """
    entry = blocks[0]
    chain_of = {b: [b] for b in blocks}
    order = sorted((e for e in weight if weight[e] > 0), key=lambda e: -weight[e])  # stable for ties
    for a, b in order:  # @line L2
        ca, cb = chain_of[a], chain_of[b]
        if a == b or b == entry or ca is cb:  # @line L3
            continue
        if ca[-1] != a or cb[0] != b:  # @line L4
            continue
        ca.extend(cb)  # @line L5
        for x in cb:
            chain_of[x] = ca
    seen, chains = set(), []
    for b in blocks:
        c = chain_of[b]
        if id(c) not in seen:
            seen.add(id(c))
            chains.append(c)
    return chains


def order_chains(chains, weight, entry):
    """Put the chains in a sequence: the chain of the entry first, then
    repeatedly the chain with the largest total weight of edges from the
    placed blocks into it (ties: the earlier chain in the list).
    """
    rest = [c for c in chains if c[0] != entry]
    placed = [c for c in chains if c[0] == entry]  # @line L6
    done = set(placed[0])
    while rest:  # @line L7
        def pull(c):
            members = set(c)
            return sum(w for (a, b), w in weight.items() if a in done and b in members)
        best = max(range(len(rest)), key=lambda i: (pull(rest[i]), -i))  # @line L8
        c = rest.pop(best)
        placed.append(c)  # @line L9
        done.update(c)
    return placed


def layout(blocks, weight):
    """The block order: the chains of chain_blocks, put in a sequence."""
    chains = chain_blocks(blocks, weight)  # @line L1
    order = []
    for c in order_chains(chains, weight, blocks[0]):
        order.extend(c)
    return order  # @line L10


def fallthrough_weight(order, weight):
    """The total weight of the edges a -> b where b directly follows a."""
    return sum(weight.get((a, b), 0) for a, b in zip(order, order[1:]))


def best_layout(blocks, weight):
    """An order with the entry first and the largest fall-through weight,
    by trying every order (for small graphs only)."""
    entry, rest = blocks[0], blocks[1:]
    best, best_w = None, -1
    for p in permutations(rest):
        order = [entry] + list(p)
        w = fallthrough_weight(order, weight)
        if w > best_w:
            best, best_w = order, w
    return best, best_w


def closest_is_best(procs, calls):
    """Pettis and Hansen's procedure ordering.

    calls maps a pair (f, g) to the number of calls between f and g, in
    either direction. Groups are merged along the heaviest edge between two
    groups; of the four ways to join two groups (each one forwards or
    reversed), the one that puts f and g closest wins. Returns the order of
    all procedures.
    """
    group = {p: [p] for p in procs}
    pos = {p: i for i, p in enumerate(procs)}
    w = {}
    for (f, g), c in calls.items():
        if f != g:
            key = (f, g) if pos[f] < pos[g] else (g, f)
            w[key] = w.get(key, 0) + c
    # For each pair of groups: (total weight, f, g, c), where f -- g is the
    # heaviest single edge between them, with weight c. It fixes the joining.
    while True:
        between = {}
        for (f, g), c in w.items():
            gf, gg = group[f], group[g]
            if gf is gg:
                continue
            k = frozenset((id(gf), id(gg)))
            tot, bf, bg, bc = between.get(k, (0, None, None, -1))
            if c > bc:
                bf, bg, bc = f, g, c
            between[k] = (tot + c, bf, bg, bc)
        if not between:
            break
        k = max(between, key=lambda k: (between[k][0], -pos[between[k][1]], -pos[between[k][2]]))
        _, f, g, _ = between[k]
        a, b = group[f], group[g]
        best = None
        for x in (a, a[::-1]):
            for y in (b, b[::-1]):
                joined = x + y
                d = abs(joined.index(f) - joined.index(g))
                if best is None or d < best[0]:
                    best = (d, joined)
        joined = best[1]
        for p in joined:
            group[p] = joined
    seen, order = set(), []
    for p in procs:
        if id(group[p]) not in seen:
            seen.add(id(group[p]))
            order.extend(group[p])
    return order


def apply_layout(prog, order):
    """prog with its blocks in the given order. The entry must stay first,
    because the toy IR starts at the first block."""
    if order[0] != prog.entry or sorted(order) != sorted(prog.blocks):
        raise ValueError("the order must be a permutation with the entry first")
    return toyir.Program(list(prog.params), {b: prog.blocks[b] for b in order})
