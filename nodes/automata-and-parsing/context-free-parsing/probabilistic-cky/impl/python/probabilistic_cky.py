# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-cky/. The authors are listed in prov/W4N6QS.jsonl.

"""Probabilistic (Viterbi) CKY for a probabilistic grammar in Chomsky normal form.

A grammar is a list of rules (A, rhs, q), where rhs is a tuple of symbols and q
is a nonnegative number, the probability of the production A -> rhs. The
nonterminals are the left sides. Every rule must be A -> B C with B, C
nonterminals, A -> a with a terminal, or start -> () when the start symbol is on
no right side. A parse tree is (A, children), where each child is a tree or a
terminal symbol.

The probabilities can be Fractions (exact), floats, or, with log_space=True,
floats that are added as logarithms so that long inputs do not underflow.
"""

import math
from typing import Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Rule = tuple[str, tuple[str, ...], object]


def check_cnf(rules: Sequence[Rule], start: str) -> set[str]:
    """Raise ValueError unless the rules are a weighted grammar in Chomsky normal form."""
    nts = {a for a, _, _ in rules}
    has_empty = False
    for a, rhs, q in rules:
        if q < 0:
            raise ValueError(f"negative probability for {a} -> {rhs}")
        if len(rhs) == 2 and rhs[0] in nts and rhs[1] in nts:
            continue
        if len(rhs) == 1 and rhs[0] not in nts:
            continue
        if len(rhs) == 0 and a == start:
            has_empty = True
            continue
        raise ValueError(f"not in Chomsky normal form: {a} -> {rhs}")
    if has_empty and any(start in rhs for _, rhs, _ in rules):
        raise ValueError("the start symbol has an empty production and is on a right side")
    return nts


def _chart(rules, w, log_space):
    """Fill the Viterbi chart. best[i][j] maps A to the largest probability of a
    tree with root A and yield w[i..j] (0-based, both ends included); back holds
    the split (k, B, C), or the terminal for j = i, of one best tree."""
    if log_space:
        lift = [(a, rhs, math.log(q)) for a, rhs, q in rules if q > 0]
    else:
        lift = list(rules)
    n = len(w)
    lexical: dict[str, list[tuple[str, object]]] = {}
    binary = []
    for a, rhs, q in lift:
        if len(rhs) == 1:
            lexical.setdefault(rhs[0], []).append((a, q))
        elif len(rhs) == 2:
            binary.append((a, rhs[0], rhs[1], q))
    best: list[list[dict[str, object]]] = [[{} for _ in range(n)] for _ in range(n)]
    back: dict[tuple[int, int, str], object] = {}
    for i in range(n):  # @line L2
        cell = best[i][i]
        for a, q in lexical.get(w[i], ()):
            if a not in cell or q > cell[a]:
                cell[a] = q  # @line L3
                back[(i, i, a)] = w[i]
    for length in range(2, n + 1):  # @line L4
        for i in range(n - length + 1):  # @line L5
            j = i + length - 1  # @line L6
            cell = best[i][j]
            for k in range(i, j):  # @line L7
                left, right = best[i][k], best[k + 1][j]
                if not left or not right:
                    continue
                for a, b, c, q in binary:  # @line L8
                    if b in left and c in right:
                        if log_space:
                            p = q + left[b] + right[c]  # @line L9
                        else:
                            p = q * left[b] * right[c]  # @line L9
                        if a not in cell or p > cell[a]:  # @line L10
                            cell[a] = p
                            back[(i, j, a)] = (k, b, c)
    return best, back


def _build_tree(back, start: str, n: int) -> Tree:
    """Follow the back pointers from (0, n - 1, start) with an explicit stack."""
    done: dict[tuple[int, int, str], Tree] = {}
    stack = [(0, n - 1, start, False)]
    while stack:
        i, j, a, expanded = stack.pop()
        b = back[(i, j, a)]
        if i == j:
            done[(i, j, a)] = (a, (b,))
            continue
        k, left, right = b
        kids = ((i, k, left), (k + 1, j, right))
        if expanded:
            done[(i, j, a)] = (a, (done[kids[0]], done[kids[1]]))
        else:
            stack.append((i, j, a, True))
            for key in kids:
                stack.append((key[0], key[1], key[2], False))
    return done[(0, n - 1, start)]


def viterbi_cky(rules: Sequence[Rule], start: str, w: Sequence[str], log_space: bool = False):
    """Return (p, tree): the largest probability p of a parse tree of w and one tree
    that has it. When w has no parse tree, return (0, None), or (-inf, None) when
    log_space is True, in which case p is the natural logarithm of the probability.

    Time Theta(n^3 g) for n = len(w) and g rules, space Theta(n^2 v).
    """
    check_cnf(rules, start)
    zero = -math.inf if log_space else 0
    if len(w) == 0:  # @line L1
        empty = [q for a, rhs, q in rules if a == start and len(rhs) == 0 and q > 0]
        if not empty:
            return zero, None
        q = max(empty)
        return (math.log(q) if log_space else q), (start, ())
    best, back = _chart(rules, w, log_space)
    top = best[0][len(w) - 1]
    if start not in top:
        return zero, None
    return top[start], _build_tree(back, start, len(w))  # @line L11


def best_chart(rules: Sequence[Rule], start: str, w: Sequence[str]) -> list[list[dict[str, object]]]:
    """Return the chart: entry [i][j][A] is the best probability of A over w[i..j]."""
    check_cnf(rules, start)
    return _chart(rules, w, False)[0]


def inside_probability(rules: Sequence[Rule], start: str, w: Sequence[str]):
    """Return P(w), the sum of the probabilities of all parse trees of w.

    The same loops as viterbi_cky, with the maximum replaced by a sum.
    """
    check_cnf(rules, start)
    n = len(w)
    if n == 0:
        return sum((q for a, rhs, q in rules if a == start and len(rhs) == 0), 0)
    inside: list[list[dict[str, object]]] = [[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        cell = inside[i][i]
        for a, rhs, q in rules:
            if len(rhs) == 1 and rhs[0] == w[i]:
                cell[a] = cell.get(a, 0) + q
    binary = [(a, rhs[0], rhs[1], q) for a, rhs, q in rules if len(rhs) == 2]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cell = inside[i][j]
            for k in range(i, j):
                left, right = inside[i][k], inside[k + 1][j]
                if not left or not right:
                    continue
                for a, b, c, q in binary:
                    if b in left and c in right:
                        cell[a] = cell.get(a, 0) + q * left[b] * right[c]
    return inside[0][n - 1].get(start, 0)


def tree_probability(rules: Sequence[Rule], tree: Tree):
    """Return the product of the probabilities of the rules used in the tree.

    If a production appears several times in the list, its largest probability is used.
    """
    q: dict[tuple[str, tuple[str, ...]], object] = {}
    for a, rhs, p in rules:
        if (a, rhs) not in q or p > q[(a, rhs)]:
            q[(a, rhs)] = p
    total = 1
    stack = [tree]
    while stack:
        a, kids = stack.pop()
        rhs = tuple(k if isinstance(k, str) else k[0] for k in kids)
        total = total * q[(a, rhs)]
        stack.extend(k for k in kids if not isinstance(k, str))
    return total


def tree_yield(tree: Tree) -> list[str]:
    """Return the terminal symbols at the leaves of the tree, from left to right."""
    out = []
    stack: list[object] = [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            out.append(t)
        else:
            stack.extend(reversed(t[1]))
    return out
