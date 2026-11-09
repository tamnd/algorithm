# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equivalent-literal-substitution/. The authors are listed in prov/5XGNFS.jsonl.

"""Equivalent literal substitution (ELS).

Literals in one strongly connected component of the binary implication
graph are equivalent in every model. Each component is replaced by one
representative literal. If x and -x share a component, the formula is
unsatisfiable. Clauses are lists of DIMACS ints.
"""


def sccs(nodes: list[int], succ: dict[int, list[int]]) -> list[list[int]]:
    """Strongly connected components by Tarjan's algorithm, without recursion."""
    index: dict[int, int] = {}
    low: dict[int, int] = {}
    on_stack: set[int] = set()
    stack: list[int] = []
    comps: list[list[int]] = []
    counter = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            v, i = work.pop()
            if i == 0:
                index[v] = low[v] = counter
                counter += 1
                stack.append(v)
                on_stack.add(v)
            out = succ.get(v, [])
            if i < len(out):
                work.append((v, i + 1))
                w = out[i]
                if w not in index:
                    work.append((w, 0))
                elif w in on_stack:
                    low[v] = min(low[v], index[w])
                continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                comps.append(comp)
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
    return comps


def els(clauses: list[list[int]]) -> tuple[list[list[int]] | None, dict[int, int]]:
    """Substitute equivalent literals until no binary clause gives a new equivalence.

    Returns (clauses, rep) where rep maps each replaced variable x to the
    literal that x equals. The clauses are None if the formula is UNSAT.
    """
    cnf = {frozenset(c) for c in clauses if not any(-a in c for a in c)}
    rep: dict[int, int] = {}
    while True:
        succ: dict[int, list[int]] = {}
        for c in cnf:  # @line L1
            if len(c) == 2:
                a, b = sorted(c)
                succ.setdefault(-a, []).append(b)
                succ.setdefault(-b, []).append(a)
        nodes = sorted(succ, key=lambda u: (abs(u), u))
        sub: dict[int, int] = {}
        for comp in sccs(nodes, succ):  # @line L2
            members = set(comp)
            if any(-a in members for a in members):  # @line L3
                return None, rep
            r = min(comp, key=abs)  # @line L4
            for a in comp:
                if a != r and a > 0:
                    sub[a] = r
                elif a != r:
                    sub[-a] = -r
        if not sub:
            return sorted(sorted(c, key=lambda a: (abs(a), a)) for c in cnf), rep
        new = set()
        for c in cnf:  # @line L5
            d = frozenset(sub.get(a, a) if a > 0 else -sub.get(-a, -a) for a in c)
            if any(-a in d for a in d):  # @line L6
                continue
            if not d:
                return None, rep
            new.add(d)  # @line L7
        cnf = new
        for x, r in sub.items():  # compose with earlier substitutions
            rep[x] = r
        for x in list(rep):
            r = rep[x]
            while abs(r) in sub:
                r = sub[abs(r)] if r > 0 else -sub[abs(r)]
            rep[x] = r


def reconstruct(model: dict[int, bool], rep: dict[int, int]) -> dict[int, bool]:
    """Give each replaced variable the value of its representative literal."""
    alpha = dict(model)
    for x, r in rep.items():  # @line L8
        alpha[x] = alpha[abs(r)] == (r > 0)
    return alpha
