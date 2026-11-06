# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-k-parsing/. The authors are listed in prov/VNTPSZ.jsonl.

"""LL(k) parsing with the canonical LL(k) tables T(A, L).

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


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


def _cat(xs: set[Look], ys: set[Look], k: int) -> set[Look]:
    """The k-concatenation: every x + y cut to its first k tokens."""
    out = {x for x in xs if len(x) >= k}
    short = [x for x in xs if len(x) < k]
    for x in short:
        for y in ys:
            out.add((x + y)[:k])
    return out


def first_k(productions: list[Production], k: int) -> dict[str, set[Look]]:
    """FIRST_k of every nonterminal, as the least fixed point of the productions."""
    nts = {a for a, _ in productions}
    first: dict[str, set[Look]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            cur: set[Look] = {()}
            for x in rhs:
                cur = _cat(cur, first[x] if x in nts else {(x,)}, k)
                if not cur:
                    break
            if not cur <= first[a]:
                first[a] |= cur
                changed = True
    return first


class LLkTables:
    """The tables T(A, L): tables[t] maps a lookahead to (production, child tables)."""

    def __init__(self, productions: list[Production], start: str, k: int) -> None:
        self.productions = productions
        self.start = start
        self.k = k
        self.keys: list[tuple[str, frozenset[Look]]] = []
        self.tables: list[dict[Look, tuple[int, tuple[int | None, ...]]]] = []
        self.start_table = 0


def build_tables(productions: list[Production], start: str, k: int) -> LLkTables:
    """Build the LL(k) tables reachable from T(start, {()}). Raises ValueError if G is not LL(k)."""
    nts = {a for a, _ in productions}
    first = first_k(productions, k)  # @line L12
    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(productions):
        by_lhs.setdefault(a, []).append(p)

    def first_of(alpha: tuple[str, ...], tail: frozenset[Look]) -> set[Look]:
        cur: set[Look] = {()}
        for x in alpha:
            cur = _cat(cur, first[x] if x in nts else {(x,)}, k)
            if not cur:
                return cur
        return _cat(cur, set(tail), k)

    out = LLkTables(productions, start, k)
    index: dict[tuple[str, frozenset[Look]], int] = {}

    def table(a: str, look: frozenset[Look]) -> int:
        key = (a, look)
        if key not in index:
            index[key] = len(out.tables)
            out.keys.append(key)
            out.tables.append({})
            queue.append(index[key])
        return index[key]

    queue: deque[int] = deque()
    out.start_table = table(start, frozenset({()}))  # @line L13
    while queue:
        t = queue.popleft()  # @line L14
        a, look = out.keys[t]
        for p in by_lhs.get(a, []):
            rhs = productions[p][1]
            lookaheads = first_of(rhs, look)  # @line L15
            if not lookaheads:
                continue
            for u in lookaheads:
                old = out.tables[t].get(u)
                if old is not None and old[0] != p:  # @line L16
                    raise ValueError(f"not LL({k}): T({a}, ...) has two productions for {u!r}")
            kids: list[int | None] = []
            for j, y in enumerate(rhs):  # @line L17
                if y in nts:
                    kids.append(table(y, frozenset(first_of(rhs[j + 1:], look))))
                else:
                    kids.append(None)
            for u in lookaheads:  # @line L18
                out.tables[t][u] = (p, tuple(kids))
    return out


def _common(u: Look, v: Look) -> int:
    m = 0
    while m < len(u) and m < len(v) and u[m] == v[m]:
        m += 1
    return m


def llk_parse(productions: list[Production], start: str, tokens: list[str], k: int,
              tables: LLkTables | None = None) -> Tree:
    """Parse tokens with an LL(k) grammar and return the parse tree.

    Raises ValueError (from build_tables) if the grammar is not LL(k), and ParseError
    when tokens is not in the language, at the first token where the input stops being
    a prefix of a sentence. Cost: O(n + tree size) steps once the tables exist, each
    step O(k) for slicing and hashing the lookahead.
    """
    if tables is None:
        tables = build_tables(productions, start, k)
    w = list(tokens)
    n = len(w)
    i = 0  # @line L1
    root: list[Tree] = []
    stack: list[tuple[str, int | None, list]] = [(start, tables.start_table, root)]
    while stack:  # @line L2
        x, t, parent = stack.pop()  # @line L3
        if t is None:  # @line L4
            if i >= n or w[i] != x:  # @line L5
                found = w[i] if i < n else "the end of the input"
                raise ParseError(i, f"expected {x!r}, found {found!r}")
            parent.append(w[i])  # @line L6
            i += 1
            continue
        u = tuple(w[i:i + k])  # @line L7
        entry = tables.tables[t].get(u)
        if entry is None:  # @line L8
            best = max((_common(u, v) for v in tables.tables[t]), default=0)
            raise ParseError(i + best, f"no production of {x} fits the lookahead {u!r}")
        p, kids = entry  # @line L9
        node: tuple[str, list] = (x, [])
        parent.append(node)
        rhs = productions[p][1]
        for j in range(len(rhs) - 1, -1, -1):  # @line L10
            stack.append((rhs[j], kids[j], node[1]))
    if i < n:  # @line L11
        raise ParseError(i, f"expected the end of the input, found {w[i]!r}")
    return root[0]
