# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-ascent-parsing/. The authors are listed in prov/K7ZEFB.jsonl.
"""Recursive ascent parsing: an SLR(1) parser written as one procedure per LR state.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
A symbol is a nonterminal if it is the left side of some production, and a
terminal otherwise. Production k of the user's grammar is reported as k. A parse
tree is a token or (A, children).

Each state procedure is a Python generator. A shift or a goto is a call, written
`result = yield (state, value)`, and a reduction is a return. A small driver runs
the generators with an explicit stack, so the depth of the parse does not hit
Python's recursion limit; read `yield` as a call and the code is the recursive
procedure of the page.
"""

END = "$"
START = "S'"


class GrammarConflict(Exception):
    """The grammar is not SLR(1); .conflicts lists (state, token, actions)."""

    def __init__(self, conflicts):
        super().__init__(f"{len(conflicts)} SLR(1) conflicts")
        self.conflicts = conflicts


class ParseError(Exception):
    """The input is not a sentence; .position is the index of the bad token."""

    def __init__(self, position):
        super().__init__(f"syntax error at token {position}")
        self.position = position


def _useful(prods, start):
    """Indices of the productions whose symbols all derive terminal strings and
    whose left side is reachable from start through such productions."""
    nts = {a for a, _ in prods}
    productive, changed = set(), True
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


def _follow(P, nts):
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
    return follow


def slr_table(prods, start):
    """Return (action, goto, nstates): action[(q, a)] is ("shift", j),
    ("reduce", k) or ("accept",), and goto[(q, A)] is a state. Raise
    GrammarConflict if some entry would need two actions."""
    prods = [(a, tuple(r)) for a, r in prods]
    keep = _useful(prods, start)
    P = [(START, (start,))] + [prods[k] for k in keep]
    orig = [None] + keep
    nts = {START} | {a for a, _ in prods}
    by_lhs = {}
    for i, (a, _) in enumerate(P):
        by_lhs.setdefault(a, []).append(i)
    follow = _follow(P, nts)

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
                acts = [("shift", trans[q, rhs[d]])]
                keys = [rhs[d]]
            elif d == len(rhs) and i == 0:
                acts, keys = [("accept",)], [END]
            elif d == len(rhs):
                keys = sorted(follow[a])
                acts = [("reduce", orig[i])] * len(keys)
            else:
                continue
            for t, act in zip(keys, acts):
                entry = action.setdefault((q, t), [])
                if act not in entry:
                    entry.append(act)
    conflicts = sorted((q, t, acts) for (q, t), acts in action.items() if len(acts) > 1)
    if conflicts:
        raise GrammarConflict(conflicts)
    action = {key: acts[0] for key, acts in action.items()}
    goto = {(q, x): j for (q, x), j in trans.items() if x in nts}
    return action, goto, len(states)


class RecursiveAscentParser:
    """An SLR(1) parser made of one procedure per LR state."""

    def __init__(self, prods, start):
        self.prods = [(a, tuple(r)) for a, r in prods]
        action, goto, nstates = slr_table(self.prods, start)
        self.nstates = nstates
        rows = [dict() for _ in range(nstates)]
        gotos = [dict() for _ in range(nstates)]
        for (q, t), act in action.items():
            rows[q][t] = act
        for (q, a), j in goto.items():
            gotos[q][a] = j
        # The procedures: procs[q] is the procedure of state q, specialized to its row.
        self.procs = [self._make_state(rows[q], gotos[q]) for q in range(nstates)]

    def _make_state(self, row, gotos):
        prods = self.prods

        def state(v, inp):
            # inp = [tokens, position, reductions]; v is the tree that led into this state.
            a = inp[0][inp[1]]  # @line L3
            act = row.get(a)
            if act is not None and act[0] == "shift":  # @line L4
                inp[1] += 1
                r = yield (act[1], a)
            elif act is not None and act[0] == "reduce":  # @line L5
                k = act[1]
                inp[2].append(k)
                lhs, rhs = prods[k]
                if rhs:
                    return ("reduce", lhs, len(rhs) - 1, [v])  # @line L6
                r = ("reduce", lhs, 0, [])  # @line L7
            elif act is not None:
                return ("accept", v)  # @line L8
            else:
                raise ParseError(inp[1])  # @line L9
            while True:  # @line L10
                if r[0] == "accept":  # @line L11
                    return r
                _, lhs, c, kids = r
                if c > 0:  # @line L12
                    kids.append(v)  # the children are collected from right to left
                    return ("reduce", lhs, c - 1, kids)
                kids.reverse()
                r = yield (gotos[lhs], (lhs, tuple(kids)))  # @line L13

        return state

    def parse(self, tokens, trace=None):
        """Return (tree, reductions), or raise ParseError. reductions lists the
        user's production indices in the order of the reductions, a reverse
        rightmost derivation. If trace is a list, the state of every call is
        appended to it, so trace shows the procedure calls in order."""
        inp = [list(tokens) + [END], 0, []]
        calls = [self.procs[0](None, inp)]  # @line L1
        if trace is not None:
            trace.append(0)
        sent = None
        while True:
            try:
                q, value = calls[-1].send(sent)
            except StopIteration as stop:
                calls.pop()
                sent = stop.value
                if not calls:
                    return sent[1], inp[2]  # @line L2
                continue
            if trace is not None:
                trace.append(q)
            calls.append(self.procs[q](value, inp))
            sent = None
