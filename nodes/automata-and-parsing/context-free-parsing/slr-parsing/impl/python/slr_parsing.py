# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slr-parsing/. The authors are listed in prov/7X628Y.jsonl.
"""SLR(1) parsing: the LR(0) automaton with reductions limited to FOLLOW sets.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
A symbol is a nonterminal if it is the left side of some production, and a
terminal otherwise. Production k of the user's grammar is reported as k.
"""

END = "$"
START = "S'"


class GrammarConflict(Exception):
    """The grammar is not SLR(1); .conflicts lists (state, token, actions)."""

    def __init__(self, conflicts):
        super().__init__(f"{len(conflicts)} SLR(1) conflicts")
        self.conflicts = conflicts


class ParseError(Exception):
    """The input is not a sentence; .position is the index of the bad token
    (len(tokens) for the end of the input)."""

    def __init__(self, position):
        super().__init__(f"syntax error at token {position}")
        self.position = position


def useful_productions(prods, start):
    """Indices of the productions in which every symbol derives a terminal
    string and whose left side is reachable from start through such rules."""
    nts = {a for a, _ in prods}
    productive = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in productive and all(x not in nts or x in productive for x in rhs):
                productive.add(a)
                changed = True
    ok = [k for k, (a, rhs) in enumerate(prods)
          if a in productive and all(x not in nts or x in productive for x in rhs)]
    reach, todo = {start}, [start]
    while todo:
        b = todo.pop()
        for k in ok:
            if prods[k][0] == b:
                for x in prods[k][1]:
                    if x in nts and x not in reach:
                        reach.add(x)
                        todo.append(x)
    return [k for k in ok if prods[k][0] in reach]


def follow_sets(P, nts):
    """Nullable set and FOLLOW sets of the augmented grammar P, by fixpoints."""
    nullable, first = set(), {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in P:
            for x in rhs:
                add = first[x] if x in nts else {x}
                if not add <= first[a]:
                    first[a] |= add
                    changed = True
                if x not in nullable:
                    break
            else:
                if a not in nullable:
                    nullable.add(a)
                    changed = True
    follow = {a: set() for a in nts}
    follow[START].add(END)
    changed = True
    while changed:
        changed = False
        for a, rhs in P:
            trailer = set(follow[a])
            for x in reversed(rhs):
                if x in nts:
                    if not trailer <= follow[x]:
                        follow[x] |= trailer
                        changed = True
                    trailer = trailer | first[x] if x in nullable else set(first[x])
                else:
                    trailer = {x}
    return nullable, follow


class SLRTable:
    """The LR(0) automaton of a grammar and its SLR(1) ACTION and GOTO tables.

    action[(state, terminal)] is a list of actions: ("shift", j),
    ("reduce", k) with k the index of the user's production, or ("accept",).
    """

    def __init__(self, prods, start):
        self.prods = [(a, tuple(r)) for a, r in prods]
        keep = useful_productions(self.prods, start)
        # P[0] is S' -> start; P[i] for i >= 1 is the user's production orig[i].
        P = [(START, (start,))] + [self.prods[k] for k in keep]
        orig = [None] + keep
        nts = {START} | {a for a, _ in self.prods}
        by_lhs = {}
        for i, (a, _) in enumerate(P):
            by_lhs.setdefault(a, []).append(i)
        self.nullable, self.follow = follow_sets(P, nts)

        def closure(kernel):
            items, todo = set(kernel), list(kernel)
            while todo:
                i, d = todo.pop()
                rhs = P[i][1]
                if d < len(rhs):
                    for j in by_lhs.get(rhs[d], ()):
                        if (j, 0) not in items:
                            items.add((j, 0))
                            todo.append((j, 0))
            return frozenset(items)

        states = [closure({(0, 0)})]
        index = {states[0]: 0}
        trans = {}
        q = 0
        while q < len(states):
            succ = {}
            for i, d in sorted(states[q]):
                rhs = P[i][1]
                if d < len(rhs):
                    succ.setdefault(rhs[d], set()).add((i, d + 1))
            for x, kernel in succ.items():
                target = closure(kernel)
                if target not in index:
                    index[target] = len(states)
                    states.append(target)
                trans[q, x] = index[target]
            q += 1

        action = {}
        for q, items in enumerate(states):
            for i, d in sorted(items):
                a, rhs = P[i]
                if d < len(rhs) and rhs[d] not in nts:
                    act = ("shift", trans[q, rhs[d]])
                    keyed = action.setdefault((q, rhs[d]), [])
                    if act not in keyed:
                        keyed.append(act)
                elif d == len(rhs) and i == 0:
                    action.setdefault((q, END), []).append(("accept",))
                elif d == len(rhs):
                    for t in sorted(self.follow[a]):
                        action.setdefault((q, t), []).append(("reduce", orig[i]))
        self.P, self.states, self.nts = P, states, nts
        self.action = action
        self.goto = {(q, x): j for (q, x), j in trans.items() if x in nts}
        self.conflicts = sorted((q, t, acts) for (q, t), acts in action.items() if len(acts) > 1)


def slr_table(prods, start):
    """The SLR(1) table, or GrammarConflict if the grammar is not SLR(1)."""
    table = SLRTable(prods, start)
    if table.conflicts:
        raise GrammarConflict(table.conflicts)
    return table


def parse(table, tokens, choose=None, trace=None, limit=None):
    """Parse tokens with the table. Returns (tree, reductions): a tree is a
    token or (A, children), and reductions lists the user's production
    indices in the order the parser used them. choose(acts) picks an action
    when an entry has several (only needed for tables with conflicts).
    If trace is a list, (states, symbols, remaining input, action) is appended
    for every step. limit bounds the number of moves (a RuntimeError is
    raised beyond it); a table without conflicts never needs it."""
    w = list(tokens) + [END]
    states, trees, reductions = [0], [], []  # @line L1
    i = moves = 0
    while True:  # @line L2
        moves += 1
        if limit is not None and moves > limit:
            raise RuntimeError("move limit exceeded")
        q, a = states[-1], w[i]  # @line L3
        acts = table.action.get((q, a))
        if not acts:  # @line L4
            raise ParseError(i)
        act = acts[0] if len(acts) == 1 else choose(acts)
        if trace is not None:
            symbols = [t if isinstance(t, str) else t[0] for t in trees]
            trace.append((list(states), symbols, w[i:], act))
        if act[0] == "shift":  # @line L5
            states.append(act[1])  # @line L6
            trees.append(a)
            i += 1
        elif act[0] == "reduce":  # @line L7
            lhs, rhs = table.prods[act[1]]
            k = len(rhs)
            kids = tuple(trees[len(trees) - k:])  # @line L8
            del states[len(states) - k:]
            del trees[len(trees) - k:]
            states.append(table.goto[states[-1], lhs])  # @line L9
            trees.append((lhs, kids))
            reductions.append(act[1])
        else:
            return trees[0], reductions  # @line L10
