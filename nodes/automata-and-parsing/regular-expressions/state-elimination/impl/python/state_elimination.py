# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-elimination/. The authors are listed in prov/GVY1JV.jsonl.

"""State elimination: a finite automaton to a regular expression.

Expressions are tuples: ("empty",) for ∅, ("eps",) for ε, ("sym", a),
("alt", r, s) for r|s, ("cat", r, s) for rs and ("star", r) for r*.
Subexpressions are shared, not copied, so each update of a label costs O(1)
even when the written-out expression is long. No function recurses, so deep
expressions are safe.
"""

EMPTY = ("empty",)
EPS = ("eps",)


def alt(r, s):
    """r | s, with ∅ as the unit."""
    if r is EMPTY:
        return s
    if s is EMPTY or s is r:
        return r
    return ("alt", r, s)


def cat(r, s):
    """r s, with ∅ as zero and ε as the unit."""
    if r is EMPTY or s is EMPTY:
        return EMPTY
    if r is EPS:
        return s
    if s is EPS:
        return r
    return ("cat", r, s)


def star(r):
    """r*, with ∅* = ε* = ε and (r*)* = r*."""
    if r is EMPTY or r is EPS:
        return EPS
    if r[0] == "star":
        return r
    return ("star", r)


def sym(a):
    return EPS if a == "" else ("sym", a)


def eliminate(n, start, accepting, moves, order=None):
    """Return a regular expression for the language of an NFA.

    The states are 0..n-1; moves is a list of (p, a, q), where a is a symbol
    or "" for an ε-move. order lists the states in the order of removal
    (default 0, 1, ..., n-1).
    """
    s, f = n, n + 1
    out = [dict() for _ in range(n + 2)]  # out[p][q] = label of p -> q
    inn = [dict() for _ in range(n + 2)]  # inn[q][p] = the same label

    def put(p, q, r):
        out[p][q] = inn[q][p] = alt(out[p].get(q, EMPTY), r)

    put(s, start, EPS)  # @line L1
    for q in accepting:
        put(q, f, EPS)
    for p, a, q in moves:  # @line L2
        put(p, q, sym(a))
    for k in order if order is not None else range(n):  # @line L3
        loop = star(out[k].pop(k, EMPTY))  # @line L4
        inn[k].pop(k, None)
        for p, rpk in inn[k].items():  # @line L5
            head = cat(rpk, loop)
            for q, rkq in out[k].items():  # @line L6
                put(p, q, cat(head, rkq))  # @line L7
        for p in inn[k]:  # @line L8
            del out[p][k]
        for q in out[k]:
            del inn[q][k]
        out[k].clear()
        inn[k].clear()
    return out[s].get(f, EMPTY)  # @line L9


def to_string(r):
    """Write r with | for union, * for star, ε and ∅, using few parentheses."""
    prec = {"alt": 0, "cat": 1, "star": 2}
    parts = []
    stack = [r]
    while stack:
        x = stack.pop()
        if isinstance(x, str):
            parts.append(x)
        elif x[0] == "empty":
            parts.append("∅")
        elif x[0] == "eps":
            parts.append("ε")
        elif x[0] == "sym":
            parts.append(x[1])
        else:
            kids = x[1:]
            items = []
            for i, y in enumerate(kids):
                need = y[0] in prec and prec[y[0]] < prec[x[0]]
                if i == 1 and x[0] == "alt":
                    items.append("|")
                items += ["(", y, ")"] if need else [y]
            if x[0] == "star":
                items.append("*")
            stack.extend(reversed(items))
    return "".join(parts)


def size(r):
    """The number of nodes of r written out as a tree, without writing it out."""
    memo = {}
    stack = [r]
    while stack:
        x = stack[-1]
        if id(x) in memo:
            stack.pop()
            continue
        kids = [y for y in x[1:] if isinstance(y, tuple)]
        todo = [y for y in kids if id(y) not in memo]
        if todo:
            stack.extend(todo)
        else:
            memo[id(x)] = 1 + sum(memo[id(y)] for y in kids)
            stack.pop()
    return memo[id(r)]
