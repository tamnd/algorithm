# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pushdown-saturation/. The authors are listed in prov/KE52MW.jsonl.

"""Saturation algorithms for pre* and post* of a pushdown system.

A pushdown system is a list of rules (p, g, p2, w): in control location p
with g on top of the stack, replace g by the word w (a tuple of length 0, 1
or 2; w[0] becomes the new top) and go to p2.

A P-automaton is a set of transitions (q, a, q2) and a set of final states.
The control locations are states of the automaton, and the automaton accepts
the configuration <p, w> when it can read w from state p and end in a final
state. In the result of post_star, a label a = EPS is an empty move.

Precondition of both algorithms: no transition of the input automaton leads
into a control location, and the input automaton has no empty moves.
"""

from collections import defaultdict

EPS = None

Rule = tuple[object, object, object, tuple]
Trans = tuple[object, object, object]


def pre_star(rules: list[Rule], trans: set[Trans]) -> set[Trans]:
    """Saturate the automaton so that it accepts pre*(C) for its language C.

    Cost: O(|Q|^2 |rules|) time for an automaton with state set Q
    (Esparza, Hansel, Rossmanith and Schwoon 2000).
    """
    by_rhs1 = defaultdict(list)  # (p2, g2) -> [(p, g)] for rules <p,g> -> <p2,g2>
    by_rhs2 = defaultdict(list)  # (p2, g1) -> [(p, g, g2)] for rules <p,g> -> <p2,g1 g2>
    for p, g, p2, w in rules:
        if len(w) == 1:
            by_rhs1[(p2, w[0])].append((p, g))
        elif len(w) == 2:
            by_rhs2[(p2, w[0])].append((p, g, w[1]))
    out = defaultdict(list)  # (q, a) -> [q2] for the transitions (q, a, q2) in rel
    rel: set[Trans] = set()  # @line L1
    work = list(trans)
    for p, g, p2, w in rules:  # @line L2
        if len(w) == 0:
            work.append((p, g, p2))
    derived = defaultdict(list)  # @line L3
    while work:  # @line L4
        t = work.pop()  # @line L5
        if t in rel:  # @line L6
            continue
        rel.add(t)  # @line L7
        q, a, q2 = t
        out[(q, a)].append(q2)
        for p1, g1 in by_rhs1[(q, a)] + derived[(q, a)]:  # @line L8
            work.append((p1, g1, q2))
        for p1, g1, g2 in by_rhs2[(q, a)]:  # @line L9
            derived[(q2, g2)].append((p1, g1))
            for q3 in out[(q2, g2)]:  # @line L10
                work.append((p1, g1, q3))
    return rel  # @line L11


def post_star(rules: list[Rule], trans: set[Trans]) -> set[Trans]:
    """Saturate the automaton so that it accepts post*(C) for its language C.

    The rules must have the normal form len(w) <= 2. New states are named
    ("mid", p2, g1), one for each push rule target (p2, g1).
    Cost: polynomial; cubic in the size of the rules and the automaton.
    """
    controls = {r[0] for r in rules} | {r[2] for r in rules}
    by_lhs = defaultdict(list)
    for p, g, p2, w in rules:
        by_lhs[(p, g)].append((p2, w))
    out = defaultdict(list)  # q -> [(a, q2)] in rel
    eps_into = defaultdict(list)  # q -> [p] with (p, EPS, q) in rel
    rel: set[Trans] = set()
    work = []
    for t in trans:
        if t[0] in controls:
            work.append(t)
        else:
            rel.add(t)
            out[t[0]].append((t[1], t[2]))
    while work:
        t = work.pop()
        if t in rel:
            continue
        rel.add(t)
        p, a, q = t
        out[p].append((a, q))
        if a is not EPS:
            for p2, w in by_lhs[(p, a)]:
                if len(w) == 0:
                    work.append((p2, EPS, q))
                elif len(w) == 1:
                    work.append((p2, w[0], q))
                else:
                    mid = ("mid", p2, w[0])
                    work.append((p2, w[0], mid))
                    t2 = (mid, w[1], q)
                    if t2 not in rel:
                        rel.add(t2)
                        out[mid].append((w[1], q))
                        for p3 in eps_into[mid]:
                            work.append((p3, w[1], q))
        else:
            eps_into[q].append(p)
            for b, q2 in list(out[q]):
                work.append((p, b, q2))
    return rel


def accepts(rel: set[Trans], finals: set, p: object, word: tuple) -> bool:
    """Does the automaton (rel, finals) accept the configuration <p, word>?"""
    out = defaultdict(list)
    for q, a, q2 in rel:
        out[q].append((a, q2))

    def closure(states: set) -> set:
        stack, seen = list(states), set(states)
        while stack:
            q = stack.pop()
            for a, q2 in out[q]:
                if a is EPS and q2 not in seen:
                    seen.add(q2)
                    stack.append(q2)
        return seen

    cur = closure({p})
    for letter in word:
        cur = closure({q2 for q in cur for a, q2 in out[q] if a == letter})
    return bool(cur & finals)
