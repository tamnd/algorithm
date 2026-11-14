# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rapid-type-analysis/. The authors are listed in prov/D3EG6T.jsonl.
"""Rapid type analysis (RTA): a call graph from the classes that reachable
code creates.

rapid_type_analysis(prog) takes a program of the oomodel form and returns
(R, E): the methods reachable from the root, and the call edges as pairs
(site, method id). A virtual call y.m(z) may call LOOKUP(C, m) for every class
C that is at or below the declared class of y and that a reachable method
creates with new. The graph is built on the fly: a class created late adds
edges to the sites seen before, and a site seen late uses all classes created
before.

Precondition: the program is well typed. Cost: O(K * M) for the dispatch
table, plus O(n + S * K) for a program of size n with S call sites and K
classes.
"""

from oomodel import MAIN, lookup, subclasses


def rapid_type_analysis(prog: dict) -> tuple[set, set]:
    below = subclasses(prog)
    table = {}  # (C, m) -> LOOKUP(C, m), built once
    for m, (mdecl, _, _) in prog["methods"].items():
        for c in below[mdecl]:
            table[(c, m)] = lookup(prog, c, m)
    reach, work, edges = {MAIN}, [MAIN], set()  # @line L1
    made, seen = set(), []  # I and S of the pseudocode

    def add(s, t):
        edges.add((s, t))  # @line L13
        if t not in reach:  # @line L14
            reach.add(t)
            work.append(t)

    while work:  # @line L2
        mid = work.pop()  # @line L3
        local, stmts = prog["bodies"][mid]
        for st in stmts:  # @line L4
            if st[0] == "new" and st[2] not in made:
                c = st[2]
                made.add(c)  # @line L5
                for s, m, d in seen:  # @line L6
                    if c in below[d]:
                        add(s, table[(c, m)])  # @line L7
        for st in stmts:  # @line L8
            if st[0] == "call":
                _, s, _, y, m, _ = st
                d = local[y]
                seen.append((s, m, d))  # @line L9
                for c in made:  # @line L10
                    if c in below[d]:
                        add(s, table[(c, m)])  # @line L11
    return reach, edges  # @line L12
