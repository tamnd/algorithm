# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-dawg-matching/. The authors are listed in prov/YJ949P.jsonl.

from collections.abc import Hashable, Sequence


def suffix_automaton(w: Sequence[Hashable]) -> tuple[list[dict], list[bool]]:
    """Suffix automaton of w: transitions (state 0 is initial) and terminal flags.

    It accepts exactly the suffixes of w, and every factor of w labels a path from state 0.
    """
    trans: list[dict] = [{}]
    link = [-1]
    length = [0]
    last = 0
    for c in w:
        cur = len(trans)
        trans.append({})
        link.append(-1)
        length.append(length[last] + 1)
        p = last
        while p != -1 and c not in trans[p]:
            trans[p][c] = cur
            p = link[p]
        if p == -1:
            link[cur] = 0
        else:
            q = trans[p][c]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(trans)
                trans.append(dict(trans[q]))
                link.append(link[q])
                length.append(length[p] + 1)
                while p != -1 and trans[p].get(c) == q:
                    trans[p][c] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur
    terminal = [False] * len(trans)
    p = last
    while p != -1:
        terminal[p] = True
        p = link[p]
    return trans, terminal


def backward_dawg_matching(text: Sequence[Hashable], pattern: Sequence[Hashable], stats: dict | None = None) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order.

    If stats is a dict, stats["inspections"] receives the number of text characters read.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        if stats is not None:
            stats["inspections"] = 0
        return list(range(n + 1))
    trans, terminal = suffix_automaton(pattern[::-1])  # @line L3
    out, inspections = [], 0
    s = 0  # @line L4
    while s <= n - m:  # @line L5
        q, j, shift = 0, m, m  # @line L6
        while j > 0 and q is not None:  # @line L7
            inspections += 1
            q = trans[q].get(text[s + j - 1])  # @line L8
            j -= 1
            if q is not None and terminal[q]:  # @line L9
                if j > 0:  # @line L10
                    shift = j
                else:
                    out.append(s)
        s += shift  # @line L11
    if stats is not None:
        stats["inspections"] = inspections
    return out
