# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-parse-table/. The authors are listed in prov/B3QKMP.jsonl.

"""LR parse tables: ACTION and GOTO, filled by the LR(0), SLR(1) or LR(1) rules.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. A parse tree is
a pair (A, children) for a nonterminal node, and a plain string for a token leaf.
The grammar is augmented with S' -> S, and the end marker $ ends the input.
"""

END = "$"
AUG = ("S'",)  # the new start symbol; a tuple, so it cannot clash with a name

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str
Action = tuple  # ("shift", state) | ("reduce", production) | ("accept",)


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


class LRParseTable:
    """ACTION[q][a] and GOTO[q][A] for the states q of an LR automaton.

    action[q] maps a terminal or $ to one action; goto[q] maps a nonterminal to a
    state; conflicts lists (q, a, actions) for every cell that got two actions.
    """

    def __init__(self, prods: list, n_states: int) -> None:
        self.prods = prods
        self.action: list[dict[str, Action]] = [{} for _ in range(n_states)]
        self.goto: list[dict[str, int]] = [{} for _ in range(n_states)]
        self.conflicts: list[tuple[int, str, set]] = []

    def set_action(self, q: int, a: str, act: Action) -> None:
        old = self.action[q].get(a)
        if old is None or old == act:  # @line L7
            self.action[q][a] = act
        else:  # @line L8
            self.conflicts.append((q, a, {old, act}))

    def lookup(self, q: int, a: str) -> Action | None:
        return self.action[q].get(a)  # @line L9


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
    return [(a, r) for a, r in productions
            if a in good and all(x in good or x not in nts for x in r)]


def _first_follow(prods, nts):
    null: set = set()
    first: dict = {a: set() for a in nts}
    follow: dict = {a: set() for a in nts}
    follow[AUG].add(END)

    def first_of(alpha):
        out: set = set()
        for x in alpha:
            if x not in nts:
                out.add(x)
                return out, False
            out |= first[x]
            if x not in null:
                return out, False
        return out, True

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            f, nul = first_of(rhs)
            if nul and a not in null:
                null.add(a)
                changed = True
            if not f <= first[a]:
                first[a] |= f
                changed = True
            for i, x in enumerate(rhs):
                if x in nts:
                    g, rest = first_of(rhs[i + 1:])
                    if rest:
                        g = g | follow[a]
                    if not g <= follow[x]:
                        follow[x] |= g
                        changed = True
    return first_of, follow


def build_table(productions: list[Production], start: str, kind: str = "slr") -> LRParseTable:
    """Build the LR automaton and fill ACTION and GOTO.

    kind is "lr0" (reduce on every terminal), "slr" (reduce on FOLLOW of the left
    side) or "lr1" (canonical LR(1) items, reduce on the item's lookahead).
    Productions that use a nonterminal deriving no terminal string are removed first.
    """
    if kind not in ("lr0", "slr", "lr1"):
        raise ValueError(f"unknown kind {kind!r}")
    prods = [(AUG, (start,))] + _productive(productions)
    nts = {a for a, _ in productions} | {start, AUG}
    terms = sorted({x for _, r in prods for x in r if x not in nts}) + [END]
    first_of, follow = _first_follow(prods, nts)
    by_lhs: dict = {}
    for p, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(p)

    def closure(kernel):
        items = set(kernel)
        todo = list(kernel)
        while todo:
            it = todo.pop()
            p, d = it[0], it[1]
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in nts:
                if kind == "lr1":
                    f, nul = first_of(rhs[d + 1:])
                    las = f | {it[2]} if nul else f
                else:
                    las = (None,)
                for q in by_lhs.get(rhs[d], ()):
                    for la in las:
                        new = (q, 0, la) if kind == "lr1" else (q, 0)
                        if new not in items:
                            items.add(new)
                            todo.append(new)
        return frozenset(items)

    start_item = (0, 0, END) if kind == "lr1" else (0, 0)
    states = [closure([start_item])]
    index = {states[0]: 0}
    trans: dict = {}
    q = 0
    while q < len(states):
        moves: dict = {}
        for it in states[q]:
            rhs = prods[it[0]][1]
            if it[1] < len(rhs):
                moves.setdefault(rhs[it[1]], []).append((it[0], it[1] + 1) + tuple(it[2:]))
        for x, kernel in moves.items():
            j = closure(kernel)
            if j not in index:
                index[j] = len(states)
                states.append(j)
            trans[q, x] = index[j]
        q += 1

    table = LRParseTable(prods, len(states))
    for q, items in enumerate(states):
        for it in sorted(items, key=repr):  # @line L1
            p, d = it[0], it[1]
            a, rhs = prods[p]
            if d < len(rhs) and rhs[d] not in nts:  # @line L2
                table.set_action(q, rhs[d], ("shift", trans[q, rhs[d]]))
            elif d == len(rhs) and p == 0:  # @line L3
                table.set_action(q, END, ("accept",))
            elif d == len(rhs):  # @line L4
                if kind == "lr0":
                    las = terms
                elif kind == "slr":
                    las = sorted(follow[a])
                else:
                    las = [it[2]]
                for b in las:  # @line L5
                    table.set_action(q, b, ("reduce", p))
    for (q, x), j in trans.items():
        if x in nts:
            table.goto[q][x] = j  # @line L6
    return table


def lr_parse(table: LRParseTable, tokens: list[str]) -> Tree:
    """Run the shift-reduce driver on tokens. Requires a table without conflicts.

    Raises ParseError at the first token whose cell is empty.
    """
    if table.conflicts:
        raise ValueError("the table has conflicts")
    prods = table.prods
    w = list(tokens) + [END]
    states = [0]
    trees: list = []
    i = 0
    while True:
        act = table.lookup(states[-1], w[i])  # @line L10
        if act is None or (w[i] == END and i != len(w) - 1):  # @line L11
            raise ParseError(i, f"unexpected {w[i]!r}")
        if act[0] == "shift":  # @line L12
            states.append(act[1])
            trees.append(w[i])
            i += 1
        elif act[0] == "reduce":  # @line L13
            a, rhs = prods[act[1]]
            k = len(rhs)
            node = (a, trees[len(trees) - k:])
            del trees[len(trees) - k:]
            del states[len(states) - k:]
            states.append(table.goto[states[-1]][a])
            trees.append(node)
        else:  # @line L14
            return trees[0]
