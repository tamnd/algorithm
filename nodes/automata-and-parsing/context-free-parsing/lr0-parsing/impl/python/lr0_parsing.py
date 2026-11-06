# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr0-parsing/. The authors are listed in prov/37Z7NT.jsonl.

"""LR(0) parsing, with the end marker shifted like a token.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. A parse tree is
a pair (A, children) for a nonterminal node, and a plain string for a token leaf.
The grammar is augmented with the production S' -> S $, and the parser accepts
after it has shifted $.
"""

END = "$"
AUG = ("S'",)  # the new start symbol; a tuple, so it cannot clash with a name

SHIFT = "shift"
ACCEPT = "accept"

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


class LR0Table:
    """The LR(0) automaton of the augmented grammar and its actions.

    prods[0] is S' -> S $. states[q] is the set of items (p, dot) of state q,
    goto[(q, X)] the successor state, and action[q] is SHIFT, ACCEPT, the index
    of the production to reduce, or None for a state without items to act on.
    """

    def __init__(self, prods, nts, states, goto, action):
        self.prods = prods
        self.nts = nts
        self.states = states
        self.goto = goto
        self.action = action


def _productive(productions: list[Production]) -> list[Production]:
    """Drop the productions that use a nonterminal deriving no terminal string."""
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


def build_lr0(productions: list[Production], start: str) -> LR0Table:
    """Build the LR(0) automaton and its action table. Raises ValueError on a conflict.

    Productions that use a nonterminal deriving no terminal string are removed
    first; they take part in no derivation of a sentence. Cost: O(N |G|^2) time
    for N states.
    """
    nts = {a for a, _ in productions} | {start}
    prods = [(AUG, (start, END))] + _productive(productions)
    nts.add(AUG)
    by_lhs: dict = {}
    for p, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(p)

    def closure(kernel):
        items = set(kernel)
        todo = list(kernel)
        seen: set = set()
        while todo:
            p, d = todo.pop()
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in nts and rhs[d] not in seen:
                seen.add(rhs[d])
                for q in by_lhs.get(rhs[d], ()):
                    if (q, 0) not in items:
                        items.add((q, 0))
                        todo.append((q, 0))
        return frozenset(items)

    states = [closure([(0, 0)])]
    index = {states[0]: 0}
    goto: dict = {}
    q = 0
    while q < len(states):
        moves: dict = {}
        for p, d in states[q]:
            rhs = prods[p][1]
            if d < len(rhs):
                moves.setdefault(rhs[d], []).append((p, d + 1))
        for x, kernel in moves.items():
            j = closure(kernel)
            if j not in index:
                index[j] = len(states)
                states.append(j)
            goto[q, x] = index[j]
        q += 1

    action: list = []
    for q, items in enumerate(states):
        complete = [p for p, d in items if d == len(prods[p][1])]
        shifts = [p for p, d in items if d < len(prods[p][1]) and prods[p][1][d] not in nts]
        if len(complete) > 1 or (complete and shifts):
            raise ValueError(f"not LR(0): conflict in state {q}")
        if complete:
            action.append(ACCEPT if complete[0] == 0 else complete[0])
        else:
            action.append(SHIFT if shifts else None)
    return LR0Table(prods, nts, states, goto, action)


def lr0_parse(productions: list[Production], start: str, tokens: list[str],
              table: LR0Table | None = None) -> Tree:
    """Parse tokens with an LR(0) grammar and return the parse tree.

    Precondition: the grammar with S' -> S $ is LR(0) (build_lr0 raises ValueError
    otherwise). Raises ParseError at the first token that cannot continue a sentence.
    Cost: O(n) time and space after the table is built.
    """
    if table is None:
        table = build_lr0(productions, start)
    prods, goto, action = table.prods, table.goto, table.action
    w = list(tokens) + [END]
    states = [0]  # @line L1
    trees: list = []
    i = 0
    while True:  # @line L2
        q = states[-1]
        act = action[q]  # @line L3
        if act == SHIFT:  # @line L4
            nxt = goto.get((q, w[i]))
            if nxt is None:  # @line L5
                raise ParseError(i, f"unexpected {w[i]!r}")
            states.append(nxt)  # @line L6
            trees.append(w[i])
            i += 1
        elif act == ACCEPT:  # @line L7
            if i != len(w):
                raise ParseError(i - 1, "unexpected end marker inside the input")
            return trees[0]
        elif act is None:
            raise ParseError(i, "the language is empty")
        else:  # @line L8
            a, rhs = prods[act]
            k = len(rhs)
            node = (a, trees[len(trees) - k:])  # @line L9
            del trees[len(trees) - k:]
            del states[len(states) - k:]
            states.append(goto[states[-1], a])  # @line L10
            trees.append(node)
