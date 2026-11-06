# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-parsing/. The authors are listed in prov/R5HRV8.jsonl.

"""Knuth's canonical LR(k) parsing, for any k >= 0.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. A parse tree is
a pair (A, children) for a nonterminal node, and a plain string for a token leaf.
Lookahead strings are tuples of at most k tokens; a shorter tuple means that the
input ends there.
"""

from collections import deque

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str
Look = tuple[str, ...]
Item = tuple[int, int, Look]

AUG = "S'"
SHIFT = ("shift",)
ACCEPT = ("accept",)


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


def _cat(xs: set[Look], ys: set[Look], k: int) -> set[Look]:
    out = {x for x in xs if len(x) >= k}
    for x in xs:
        if len(x) < k:
            for y in ys:
                out.add((x + y)[:k])
    return out


def _productive(productions: list[Production]) -> list[Production]:
    nts = {a for a, _ in productions}
    good: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            if a not in good and all(x in good or x not in nts for x in rhs):
                good.add(a)
                changed = True
    return [(a, r) for a, r in productions if a in good and all(x in good or x not in nts for x in r)]


class LRkTable:
    """ACTION[state][lookahead] and GOTO[state][symbol] of the canonical LR(k) automaton."""

    def __init__(self, k: int) -> None:
        self.k = k
        self.productions: list[Production] = []
        self.states: list[frozenset[Item]] = []
        self.action: list[dict[Look, tuple]] = []
        self.goto: list[dict[str, int]] = []


def build_table(productions: list[Production], start: str, k: int) -> LRkTable:
    """Build the canonical LR(k) tables. Raises ValueError if the grammar is not LR(k).

    Productions that use a nonterminal deriving no terminal string are dropped first.
    """
    prods = [(AUG, (start,))] + _productive(productions)  # @line L12
    nts = {a for a, _ in prods} | {start}
    first: dict[str, set[Look]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            cur: set[Look] = {()}
            for x in rhs:
                cur = _cat(cur, first[x] if x in nts else {(x,)}, k)
            if not cur <= first[a]:
                first[a] |= cur
                changed = True

    def first_of(alpha: tuple[str, ...], tail: Look) -> set[Look]:
        cur: set[Look] = {()}
        for x in alpha:
            cur = _cat(cur, first[x] if x in nts else {(x,)}, k)
        return _cat(cur, {tail}, k)

    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(p)

    def closure(items: set[Item]) -> frozenset[Item]:
        out = set(items)
        todo = list(items)
        while todo:
            p, d, la = todo.pop()
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in nts:
                for v in first_of(rhs[d + 1:], la):
                    for q in by_lhs.get(rhs[d], []):
                        it = (q, 0, v)
                        if it not in out:
                            out.add(it)
                            todo.append(it)
        return frozenset(out)

    table = LRkTable(k)
    table.productions = prods
    index: dict[frozenset[Item], int] = {}
    queue: deque[int] = deque()

    def state(items: frozenset[Item]) -> int:
        if items not in index:
            index[items] = len(table.states)
            table.states.append(items)
            table.action.append({})
            table.goto.append({})
            queue.append(index[items])
        return index[items]

    state(closure({(0, 0, ())}))  # @line L13
    while queue:
        s = queue.popleft()  # @line L14
        moves: dict[str, set[Item]] = {}
        for p, d, la in table.states[s]:
            rhs = prods[p][1]
            if d < len(rhs):
                moves.setdefault(rhs[d], set()).add((p, d + 1, la))
        for x in sorted(moves):
            table.goto[s][x] = state(closure(moves[x]))  # @line L15
    for s, items in enumerate(table.states):
        act = table.action[s]
        for p, d, la in sorted(items):
            rhs = prods[p][1]
            if d < len(rhs):
                if rhs[d] in nts:
                    continue
                entries = [(v, SHIFT) for v in first_of(rhs[d:], la)]  # @line L16
            elif p == 0:
                entries = [(la, ACCEPT)]
            else:
                entries = [(la, ("reduce", p))]  # @line L17
            for v, a in entries:
                old = act.setdefault(v, a)
                if old != a:  # @line L18
                    raise ValueError(f"not LR({k}): state {s} has {old} and {a} on {v!r}")
    return table


def _common(u: Look, v: Look) -> int:
    m = 0
    while m < len(u) and m < len(v) and u[m] == v[m]:
        m += 1
    return m


def lr_parse(table: LRkTable, tokens: list[str]) -> Tree:
    """Parse tokens with the LR(k) tables and return the parse tree.

    Raises ParseError at the first token where the input stops being a prefix of a
    sentence. Cost: O(n + tree size) steps, each O(k) for the lookahead.
    """
    k = table.k
    w = list(tokens)
    n = len(w)
    states = [0]  # @line L1
    trees: list[Tree] = []
    i = 0
    while True:  # @line L2
        s = states[-1]  # @line L3
        u = tuple(w[i:i + k])
        act = table.action[s].get(u)
        if act is None:  # @line L4
            best = max((_common(u, v) for v in table.action[s]), default=0)
            raise ParseError(i + best, f"no action for the lookahead {u!r}")
        if act == SHIFT:  # @line L5
            nxt = table.goto[s].get(w[i]) if i < n else None
            if nxt is None:  # @line L6
                found = w[i] if i < n else "the end of the input"
                raise ParseError(i, f"unexpected {found!r}")
            trees.append(w[i])  # @line L7
            states.append(nxt)
            i += 1
        elif act[0] == "reduce":  # @line L8
            a, rhs = table.productions[act[1]]
            m = len(rhs)  # @line L9
            kids = trees[len(trees) - m:]
            del trees[len(trees) - m:]
            del states[len(states) - m:]
            trees.append((a, kids))  # @line L10
            states.append(table.goto[states[-1]][a])
        else:
            if i < n:  # @line L11
                raise ParseError(i, f"expected the end of the input, found {w[i]!r}")
            return trees[-1]
