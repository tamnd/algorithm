# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyk-algorithm/. The authors are listed in prov/0KFTGG.jsonl.

"""The CYK recognizer and parser for a grammar in Chomsky normal form.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides. Every production must be A -> B C with
B, C nonterminals, A -> a with a terminal, or start -> () when the start
symbol is on no right side. A parse tree is (A, children), where each child
is a tree or a terminal symbol.
"""

from typing import Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Production = tuple[str, tuple[str, ...]]


def _check_cnf(productions: Sequence[Production], start: str) -> set[str]:
    nts = {a for a, _ in productions}
    has_empty = False
    for a, rhs in productions:
        if len(rhs) == 2 and rhs[0] in nts and rhs[1] in nts:
            continue
        if len(rhs) == 1 and rhs[0] not in nts:
            continue
        if len(rhs) == 0 and a == start:
            has_empty = True
            continue
        raise ValueError(f"not in Chomsky normal form: {a} -> {rhs}")
    if has_empty and any(start in rhs for _, rhs in productions):
        raise ValueError("the start symbol has an empty production and is on a right side")
    return nts


def cyk_table(productions: Sequence[Production], start: str, w: Sequence[str]):
    """Fill the CYK table. Returns (T, back) with T[i][j] the set of nonterminals
    that derive w[i..j] (0-based, both ends included) and back[(i, j, A)] the first
    split (k, B, C) found for A, or the terminal for j = i.

    Time Theta(n^3 |P|), space Theta(n^2 |V|), for n = len(w).
    """
    _check_cnf(productions, start)
    n = len(w)
    binary = [(a, rhs[0], rhs[1]) for a, rhs in productions if len(rhs) == 2]
    T: list[list[set[str]]] = [[set() for _ in range(n)] for _ in range(n)]
    back: dict[tuple[int, int, str], object] = {}
    for i in range(n):  # @line L2
        for a, rhs in productions:
            if len(rhs) == 1 and rhs[0] == w[i]:
                T[i][i].add(a)  # @line L3
                back.setdefault((i, i, a), w[i])
    for length in range(2, n + 1):  # @line L4
        for i in range(n - length + 1):  # @line L5
            j = i + length - 1  # @line L6
            cell = T[i][j]
            for k in range(i, j):  # @line L7
                left, right = T[i][k], T[k + 1][j]
                if not left or not right:
                    continue
                for a, b, c in binary:  # @line L8
                    if b in left and c in right:  # @line L9
                        cell.add(a)  # @line L10
                        back.setdefault((i, j, a), (k, b, c))
    return T, back


def cyk_recognize(productions: Sequence[Production], start: str, w: Sequence[str]) -> bool:
    """Return True when start derives w. Precondition: the grammar is in CNF."""
    if len(w) == 0:  # @line L1
        _check_cnf(productions, start)
        return any(a == start and len(r) == 0 for a, r in productions)
    T, _ = cyk_table(productions, start, w)
    return start in T[0][len(w) - 1]  # @line L11


def cyk_parse(productions: Sequence[Production], start: str, w: Sequence[str]) -> Tree | None:
    """Return one parse tree of w, or None when w is not in the language.

    The tree is built from the back pointers with an explicit stack, so a long
    input does not hit the recursion limit.
    """
    n = len(w)
    if n == 0:
        return (start, ()) if cyk_recognize(productions, start, w) else None
    T, back = cyk_table(productions, start, w)
    if start not in T[0][n - 1]:
        return None
    # Build bottom-up: first list the nodes in preorder, then assemble in reverse.
    order: list[tuple[int, int, str]] = []
    stack = [(0, n - 1, start)]
    while stack:
        node = stack.pop()
        order.append(node)
        i, j, a = node
        if i < j:
            k, b, c = back[node]  # type: ignore[misc]
            stack.append((k + 1, j, c))
            stack.append((i, k, b))
    built: dict[tuple[int, int, str], Tree] = {}
    for node in reversed(order):
        i, j, a = node
        if i == j:
            built[node] = (a, (w[i],))
        else:
            k, b, c = back[node]  # type: ignore[misc]
            built[node] = (a, (built[(i, k, b)], built[(k + 1, j, c)]))
    return built[(0, n - 1, start)]
