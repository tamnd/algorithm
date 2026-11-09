# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plotkin-lgg/. The authors are listed in prov/F51B82.jsonl.

"""Plotkin's least general generalization (anti-unification) of two terms.

A term is a variable (a Python str) or a tuple (symbol, arg1, ..., argk).
A constant is a tuple with one item, for example ("a",).
"""

from typing import Union

Term = Union[str, tuple]


def _head(t: Term) -> tuple:
    """The symbol and arity of t. A variable is its own head, with arity 0."""
    return ("var", t) if isinstance(t, str) else ("fun", t[0], len(t) - 1)


def _all_variables(*terms: Term) -> set[str]:
    acc: set[str] = set()
    stack = list(terms)
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            acc.add(u)
        else:
            stack.extend(u[1:])
    return acc


def plotkin_lgg(s: Term, t: Term, prefix: str = "Z") -> tuple[Term, dict[str, Term], dict[str, Term]]:
    """Return (g, theta1, theta2) with g theta1 = s and g theta2 = t.

    g is a least general generalization of s and t: each term h that has
    both s and t as instances also has g as an instance. The variables of s
    and t are treated like constants. The new variables are prefix0,
    prefix1, ... (skipping names that already occur), and the same pair of
    subterms always gets the same new variable. Subterms are numbered by
    hash consing, so a pair key costs O(1), and the whole run takes
    O(|s| + |t|) expected time.
    """
    ids: dict[tuple, int] = {}
    node_term: list[Term] = []
    node_kids: list[tuple[int, ...]] = []
    node_head: list[tuple] = []

    def intern(term: Term) -> int:
        out: list[int] = []
        stack: list[tuple[Term, bool]] = [(term, False)]
        while stack:
            u, done = stack.pop()
            if not isinstance(u, str) and not done:
                stack.append((u, True))
                for a in reversed(u[1:]):
                    stack.append((a, False))
                continue
            k = 0 if isinstance(u, str) else len(u) - 1
            kids = tuple(out[len(out) - k:]) if k else ()
            del out[len(out) - k:]
            key = (_head(u), kids)
            if key not in ids:
                ids[key] = len(node_term)
                node_term.append(u)
                node_kids.append(kids)
                node_head.append(_head(u))
            out.append(ids[key])
        return out[0]

    used = _all_variables(s, t)
    counter = [0]

    def fresh() -> str:
        while f"{prefix}{counter[0]}" in used:
            counter[0] += 1
        name = f"{prefix}{counter[0]}"
        counter[0] += 1
        return name

    memo: dict[tuple[int, int], str] = {}  # @line L1
    theta1: dict[str, Term] = {}
    theta2: dict[str, Term] = {}
    out: list[Term] = []
    stack: list[tuple[int, int, bool]] = [(intern(s), intern(t), False)]  # @line L2
    while stack:
        a, b, done = stack.pop()
        if node_head[a] == node_head[b]:  # @line L3
            k = len(node_kids[a])
            if k == 0:
                out.append(node_term[a])
            elif not done:
                stack.append((a, b, True))
                for x, y in zip(reversed(node_kids[a]), reversed(node_kids[b])):
                    stack.append((x, y, False))
            else:
                args = out[len(out) - k:]
                del out[len(out) - k:]
                out.append((node_head[a][1], *args))  # @line L4
            continue
        z = memo.get((a, b))  # @line L5
        if z is None:
            z = fresh()  # @line L6
            memo[(a, b)] = z
            theta1[z], theta2[z] = node_term[a], node_term[b]
        out.append(z)  # @line L7
    return out[0], theta1, theta2
