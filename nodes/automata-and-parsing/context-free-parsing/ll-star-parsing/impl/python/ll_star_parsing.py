# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-star-parsing/. The authors are listed in prov/DGJMDA.jsonl.

"""Top-down parsing with adaptive LL(*) prediction, in the style of ALL(*).

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. A parse tree is
a pair (A, children) for a nonterminal node and a plain string for a token leaf.

At a nonterminal with several productions the parser runs all of them in parallel
on the coming tokens, as sets of configurations (alternative, stack), until only
one alternative is left. It first uses only the stack inside the decision rule
(SLL prediction, cached as a DFA for each nonterminal); when that stack runs out
while several alternatives remain, it repeats the prediction with the real parser
stack (LL prediction). When the alternatives can no longer be told apart, the
grammar is ambiguous there and the lowest-numbered alternative wins.

The grammar must not be left-recursive. Productions that use a nonterminal that
derives no terminal string are dropped; they cannot occur in any parse tree.
"""

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


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


def _left_recursive(productions: list[Production], nts: set[str]) -> bool:
    """True if some A derives A gamma in one or more steps."""
    nullable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
    edges: dict[str, set[str]] = {a: set() for a in nts}
    for a, rhs in productions:
        for x in rhs:
            if x not in nts:
                break
            edges[a].add(x)
            if x not in nullable:
                break
    color = dict.fromkeys(nts, 0)
    for root in nts:
        if color[root]:
            continue
        color[root] = 1
        work = [(root, iter(edges[root]))]
        while work:
            a, it = work[-1]
            b = next(it, None)
            if b is None:
                color[a] = 2
                work.pop()
            elif color[b] == 1:
                return True
            elif color[b] == 0:
                color[b] = 1
                work.append((b, iter(edges[b])))
    return False


def _starts_nt(st: tuple[str, ...], nts: set[str]) -> bool:
    return bool(st) and st[0] in nts


class AllStarParser:
    """An LL(*) parser for one grammar; the SLL DFA cache persists across inputs."""

    def __init__(self, productions: list[Production], start: str) -> None:
        self.productions = _productive(list(productions))
        self.start = start
        self.nts = {a for a, _ in productions} | {start}
        if _left_recursive(self.productions, self.nts):
            raise ValueError("the grammar is left-recursive")
        self.alts: dict[str, list[int]] = {a: [] for a in self.nts}
        for p, (a, _) in enumerate(self.productions):
            self.alts[a].append(p)
        # SLL DFA: for each nonterminal, its start state, and for each state its edges.
        self.dfa_start: dict[str, frozenset] = {}
        self.dfa_edges: dict[frozenset, dict[str, frozenset]] = {}
        self.stats = {"decisions": 0, "ll_fallbacks": 0, "max_lookahead": 0}

    # Configurations of SLL prediction are (alt, stack); of LL prediction
    # (alt, stack, d), where the entries below[d - 1], ..., below[0] of the parser
    # stack (pairs whose first part is the symbol) follow the stack. The parser
    # stack is read during a prediction, never copied or changed.

    def _closure_sll(self, configs) -> frozenset:
        out, todo = set(), list(configs)
        while todo:  # @line L26
            c = todo.pop()
            if c in out:
                continue
            out.add(c)
            alt, st = c
            if st and st[0] in self.nts:
                for q in self.alts[st[0]]:  # @line L28
                    todo.append((alt, self.productions[q][1] + st[1:]))
        return frozenset(c for c in out if not _starts_nt(c[1], self.nts))  # @line L29

    def _closure_ll(self, configs, below: list) -> frozenset:
        out, todo = set(), list(configs)
        while todo:
            alt, st, d = todo.pop()
            while not st and d > 0:  # @line L27
                st, d = (below[d - 1][0],), d - 1
            c = (alt, st, d)
            if c in out:
                continue
            out.add(c)
            if st and st[0] in self.nts:
                for q in self.alts[st[0]]:
                    todo.append((alt, self.productions[q][1] + st[1:], d))
        return frozenset(c for c in out if not _starts_nt(c[1], self.nts))

    def _predict(self, a: str, tokens: list[str], i: int, below: list) -> int:
        """The production to use for nonterminal a at token i (SLL with LL fallback)."""
        n = len(tokens)
        s = self.dfa_start.get(a)
        if s is None:
            s = self._closure_sll((q, self.productions[q][1]) for q in self.alts[a])  # @line L12
            self.dfa_start[a] = s
        t = i
        while True:  # @line L13
            self.stats["max_lookahead"] = max(self.stats["max_lookahead"], t - i)
            alts = {c[0] for c in s}
            if len(alts) == 1:  # @line L14
                return alts.pop()
            if any(not st for _, st in s):  # @line L15
                self.stats["ll_fallbacks"] += 1
                return self._predict_ll(a, tokens, i, below)
            by_alt = {q: frozenset(st for p, st in s if p == q) for q in alts}
            if len(set(by_alt.values())) == 1:  # @line L16
                return min(alts)
            if t == n:  # @line L17
                raise ParseError(n, f"input ends inside {a}")
            edges = self.dfa_edges.setdefault(s, {})
            nxt = edges.get(tokens[t])
            if nxt is None:  # @line L18
                nxt = self._closure_sll((p, st[1:]) for p, st in s if st[0] == tokens[t])
                edges[tokens[t]] = nxt
            if not nxt:  # @line L19
                raise ParseError(t, f"no alternative of {a} fits")
            s, t = nxt, t + 1

    def _predict_ll(self, a: str, tokens: list[str], i: int, below: list) -> int:
        n = len(tokens)
        c = self._closure_ll(((q, self.productions[q][1], len(below)) for q in self.alts[a]), below)  # @line L20
        t = i
        while True:  # @line L21
            self.stats["max_lookahead"] = max(self.stats["max_lookahead"], t - i)
            alts = {x[0] for x in c}
            if len(alts) == 1:  # @line L22
                return alts.pop()
            by_alt = {q: frozenset((st, d) for p, st, d in c if p == q) for q in alts}
            if len(set(by_alt.values())) == 1:  # @line L23
                return min(alts)
            if t == n:  # @line L24
                done = [p for p, st, d in c if not st and d == 0]
                if not done:
                    raise ParseError(n, f"input ends inside {a}")
                return min(done)
            c = self._closure_ll(((p, st[1:], d) for p, st, d in c if st and st[0] == tokens[t]), below)  # @line L25
            if not c:
                raise ParseError(t, f"no alternative of {a} fits")
            t += 1

    def parse(self, tokens: list[str]) -> Tree:
        tokens = list(tokens)
        n = len(tokens)
        holder: list = []
        stack: list[tuple[str, list]] = [(self.start, holder)]  # @line L1
        i = 0
        while stack:  # @line L2
            x, out = stack.pop()  # @line L3
            if x not in self.nts:  # @line L4
                if i < n and tokens[i] == x:  # @line L5
                    out.append(x)
                    i += 1
                    continue
                raise ParseError(i, f"expected {x}")  # @line L6
            alts = self.alts[x]  # @line L7
            if len(alts) == 1:
                p = alts[0]
            elif not alts:
                raise ParseError(i, f"{x} derives nothing")
            else:
                self.stats["decisions"] += 1
                p = self._predict(x, tokens, i, stack)  # @line L8
            node: tuple[str, list] = (x, [])
            out.append(node)
            rhs = self.productions[p][1]
            for y in reversed(rhs):  # @line L9
                stack.append((y, node[1]))
        if i < n:  # @line L10
            raise ParseError(i, "input left over")
        return holder[0]  # @line L11


def ll_star_parse(productions: list[Production], start: str, tokens: list[str]) -> Tree:
    """Parse tokens with a fresh parser for the grammar; see AllStarParser."""
    return AllStarParser(productions, start).parse(tokens)
