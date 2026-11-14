# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kiss-symbolic-minimization/. The authors are listed in prov/QRSANA.jsonl.

"""KISS: symbolic minimization, face constraints, and a face embedding.

The machine format and the exact minimizer come from fsmlogic. The
embedding step here is an exact search for the shortest codes that meet
every face constraint, which fits only small machines; De Micheli, Brayton
and Sangiovanni-Vincentelli used a heuristic for it.
"""

from fsmlogic import minimize, symbolic_function


def symbolic_cover(fsm):
    """A minimum symbolic cover: (input mask tuple, state group, next states, outputs)."""
    ni, no, states, rows = fsm
    n = len(states)
    domains, on, dc = symbolic_function(fsm)  # @line L1
    cover = []
    for cube, outs in minimize(domains, on, dc):  # @line L2
        group = frozenset(states[v] for v in range(n) if cube[ni] >> v & 1)
        nexts = frozenset(states[j] for j in outs if j < n)
        outputs = frozenset(j - n for j in outs if j >= n)
        cover.append((cube[:ni], group, nexts, outputs))
    return cover


def face_constraints(cover, states):
    """The groups of present states with more than one and fewer than all states."""
    seen = []
    for _, group, _, _ in cover:
        if 1 < len(group) < len(states) and group not in seen:  # @line L3
            seen.append(group)
    return seen


def face(codes, group, k):
    """(fixed mask, fixed value) of the least cube that holds the codes of group."""
    vals = [codes[s] for s in group]
    full = (1 << k) - 1
    agree = full
    for v in vals[1:]:
        agree &= ~(v ^ vals[0]) & full
    return agree, vals[0] & agree


def satisfies(codes, group, k, states):
    mask, val = face(codes, group, k)
    return all(codes[t] & mask != val for t in states if t not in group)


def embed(states, constraints, k):
    """Injective codes of k bits that meet every constraint, or None.

    Backtracking over the states in order. A partial assignment fails as
    soon as the face of the placed members of a group holds the code of a
    placed state outside the group; faces only grow, so this is safe.
    """
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


def kiss_encode(fsm):
    """Return (k, codes, symbolic cover, constraints) with the least k that meets all."""
    ni, no, states, rows = fsm
    cover = symbolic_cover(fsm)
    cons = face_constraints(cover, states)
    k = max(1, (len(states) - 1).bit_length())  # @line L4
    while True:
        codes = embed(states, cons, k)  # @line L5 L6
        if codes is not None:
            return k, codes, cover, cons  # @line L8
        k += 1


def encoded_cover(fsm, codes, k, cover):
    """Map each symbolic cube to one encoded cube (the KISS construction).

    The state part is the face of the group; the output part sets the bits
    of the code of the next state and the outputs. A cube whose output part
    is empty is dropped. Variables and outputs follow fsmlogic.
    """
    ni, no, states, rows = fsm
    result = []
    for inp, group, nexts, outputs in cover:  # @line L7
        mask, val = face(codes, group, k)
        state_part = []
        for b in range(k - 1, -1, -1):
            if mask >> b & 1:
                state_part.append(2 if val >> b & 1 else 1)
            else:
                state_part.append(3)
        outs = set(k + j for j in outputs)
        for s in nexts:
            outs.update(k - 1 - b for b in range(k) if codes[s] >> b & 1)
        if outs:
            result.append((tuple(inp) + tuple(state_part), frozenset(outs)))
    return result
