# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/class-hierarchy-analysis/. The authors are listed in prov/M6WV8Z.jsonl.
"""Class hierarchy analysis (CHA): a call graph from declared types.

class_hierarchy_analysis(prog) takes a program of the oomodel form and
returns (R, E): the methods reachable from the root, and the call edges as
pairs (site, method id). A virtual call y.m(z) may call LOOKUP(C, m) for
every class C at or below the declared class of y. The worklist holds the
methods that are reachable but not yet scanned.

Precondition: the program is well typed, so a variable of declared class D
only holds objects of a class C <= D. Cost: O(K * M) for the dispatch table
of K classes and M method names, plus O(n + S * K) for a program of size n
with S call sites.
"""

from oomodel import MAIN, call_sites, lookup, subclasses


def class_hierarchy_analysis(prog: dict) -> tuple[set, set]:
    below = subclasses(prog)
    table = {}  # (C, m) -> LOOKUP(C, m), built once
    for m, (mdecl, _, _) in prog["methods"].items():
        for c in below[mdecl]:
            table[(c, m)] = lookup(prog, c, m)  # @line L10 @line L11
    reach, work, edges = {MAIN}, [MAIN], set()  # @line L1
    while work:  # @line L2
        mid = work.pop()  # @line L3
        local = prog["bodies"][mid][0]
        for _, s, _, y, m, _ in call_sites(prog, mid):  # @line L4
            for c in below[local[y]]:  # @line L5
                t = table[(c, m)]  # @line L6
                edges.add((s, t))  # @line L7
                if t not in reach:  # @line L8
                    reach.add(t)
                    work.append(t)
    return reach, edges  # @line L9
