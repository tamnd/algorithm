# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lstar-algorithm/. The authors are listed in prov/2BJ5ME.jsonl.

from collections.abc import Callable

Word = tuple[int, ...]
DFA = tuple[list[list[int]], int, set[int]]


def _fill(
    table: dict[Word, bool],
    member: Callable[[Word], bool],
    prefixes: list[Word],
    suffixes: list[Word],
    sigma: int,
) -> None:
    """Ask a membership query for each string of (S + S.Sigma).E that is not yet known."""
    for s in prefixes:
        for x in [s] + [s + (a,) for a in range(sigma)]:
            for e in suffixes:
                w = x + e
                if w not in table:
                    table[w] = member(w)


def _row(table: dict[Word, bool], s: Word, suffixes: list[Word]) -> tuple[bool, ...]:
    return tuple(table[s + e] for e in suffixes)


def lstar(
    sigma: int,
    member: Callable[[Word], bool],
    equivalent: Callable[[DFA], Word | None],
) -> DFA:
    """Learn the minimal complete DFA of an unknown regular language over symbols 0..sigma-1.

    member(w) answers whether w is in the language. equivalent(H) returns None if the
    DFA H = (delta, start, finals) accepts the language, and otherwise a string on which
    H is wrong. With n states in the minimal DFA and counterexamples of length at most
    m, it asks at most n equivalence queries and at most (sigma + 1)(n + m(n - 1))n
    distinct membership queries, and runs in O(sigma m n^3 (m + n)) time besides the
    queries.
    """
    S: list[Word] = [()]  # @line L1
    E: list[Word] = [()]
    in_s: set[Word] = {()}
    table: dict[Word, bool] = {}
    _fill(table, member, S, E, sigma)
    while True:  # @line L2
        rep: dict[tuple[bool, ...], Word] = {}
        for s in S:
            rep.setdefault(_row(table, s, E), s)
        # consistency: strings of S with equal rows must have equal rows after each symbol
        new_suffix: Word | None = None
        for s in S:  # @line L3
            r = rep[_row(table, s, E)]
            if r == s:
                continue
            for a in range(sigma):
                for e in E:
                    if table[s + (a,) + e] != table[r + (a,) + e]:
                        new_suffix = (a,) + e
                        break
                if new_suffix is not None:
                    break
            if new_suffix is not None:
                break
        if new_suffix is not None:
            E.append(new_suffix)  # @line L4
            _fill(table, member, S, [new_suffix], sigma)
            continue
        # closedness: the row of each one-symbol extension must be a row of S
        gap: Word | None = None
        for s in S:  # @line L5
            for a in range(sigma):
                if _row(table, s + (a,), E) not in rep:
                    gap = s + (a,)
                    break
            if gap is not None:
                break
        if gap is not None:
            S.append(gap)  # @line L6
            in_s.add(gap)
            _fill(table, member, [gap], E, sigma)
            continue
        rows = list(rep)  # @line L7
        index = {row: i for i, row in enumerate(rows)}
        delta = [[index[_row(table, rep[row] + (a,), E)] for a in range(sigma)] for row in rows]
        finals = {i for i, row in enumerate(rows) if row[0]}
        hypothesis: DFA = (delta, index[_row(table, (), E)], finals)
        c = equivalent(hypothesis)  # @line L8
        if c is None:  # @line L9
            return hypothesis
        added = [c[:k] for k in range(len(c) + 1) if c[:k] not in in_s]  # @line L10
        S.extend(added)
        in_s.update(added)
        _fill(table, member, added, E, sigma)
