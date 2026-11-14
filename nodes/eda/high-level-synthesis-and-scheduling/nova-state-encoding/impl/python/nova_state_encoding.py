# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nova-state-encoding/. The authors are listed in prov/EG491A.jsonl.

"""A NOVA-style encoder: weighted face constraints at the least code length.

Symbolic minimization gives groups of present states. The weight of a
group is the number of symbolic cubes that use it. With k fixed to the
least length ceil(log2 n), the encoder takes the groups in order of
decreasing weight and keeps a group if the kept groups can still all be
met. This follows the greedy idea of Villa and Sangiovanni-Vincentelli's
heuristic; their program has several other options that are not here.
The satisfiability test is an exact search, so it fits only small machines.
"""

from fsmlogic import minimize, symbolic_function


def weighted_constraints(fsm):
    """Groups of present states with their weights, heaviest first."""
    ni, no, states, rows = fsm
    n = len(states)
    domains, on, dc = symbolic_function(fsm)
    weight = {}
    first = {}
    for pos, (cube, outs) in enumerate(minimize(domains, on, dc)):  # @line L1
        group = frozenset(states[v] for v in range(n) if cube[ni] >> v & 1)
        if 1 < len(group) < n:
            weight[group] = weight.get(group, 0) + 1  # @line L2
            first.setdefault(group, pos)
    return sorted(weight.items(), key=lambda gw: (-gw[1], len(gw[0]), first[gw[0]]))  # @line L3


def face(codes, group, k):
    vals = [codes[s] for s in group]
    full = (1 << k) - 1
    agree = full
    for v in vals[1:]:
        agree &= ~(v ^ vals[0]) & full
    return agree, vals[0] & agree


def embed(states, constraints, k):
    """Injective codes of k bits meeting every constraint, or None (backtracking)."""
    n = len(states)
    codes = {}
    used = set()

    def ok():
        for g in constraints:
            placed = [s for s in g if s in codes]
            if len(placed) < 2:
                continue
            mask, val = face(codes, placed, k)
            if any(codes[t] & mask == val for t in codes if t not in g):
                return False
        return True

    def place(i):
        if i == n:
            return True
        for c in range(1 << k):
            if c in used:
                continue
            codes[states[i]] = c
            used.add(c)
            if ok() and place(i + 1):
                return True
            used.discard(c)
            del codes[states[i]]
        return False

    return dict(codes) if place(0) else None


def nova_encode(fsm):
    """Return (k, codes, kept groups, dropped groups)."""
    ni, no, states, rows = fsm
    k = max(1, (len(states) - 1).bit_length())  # @line L4
    kept, dropped = [], []
    for group, w in weighted_constraints(fsm):  # @line L5
        if embed(states, kept + [group], k) is not None:  # @line L6
            kept.append(group)
        else:
            dropped.append(group)  # @line L7
    return k, embed(states, kept, k), kept, dropped  # @line L8
