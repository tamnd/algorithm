# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slg-resolution/. The authors are listed in prov/N2VDR9.jsonl.
"""A small SLG evaluator for ground normal programs (Chen and Warren 1996).

A program is a list of rules (head, pos, neg), as in lp.py. slg(program, query)
evaluates the atom query top-down with tables and returns a dict from each
tabled atom to "true", "false" or "undefined", its value in the well-founded
model.

The evaluator keeps one table per called atom. A node (h, goals, delay) is a
rule instance for h with the goals still to solve and the set of delayed
literals; a delayed literal is (POS, b) or (NEG, b). It implements the SLG
operations for ground programs: program clause resolution, answer return,
negative return, delaying, simplification, completion of a strongly connected
component of the call graph, and answer completion.

It leaves out: calls with variables (variant checks and substitutions), call
subsumption, the scheduling strategies of real engines, the incremental
completion stack (the components are recomputed from scratch), and all
efficiency work of an engine such as the SLG-WAM.
"""

POS, NEG = "+", "-"


class _Table:
    __slots__ = ("complete", "true", "answers", "consumers", "waiters")

    def __init__(self):
        self.complete = False
        self.true = False  # True once the table has an answer with no delay
        self.answers = set()  # the delay lists of the conditional answers
        self.consumers = []  # nodes waiting for the first answer of a positive call
        self.waiters = []  # nodes waiting on the negation of this atom


class SLG:
    def __init__(self, program):
        self.rules = {}
        for h, pos, neg in program:
            goals = tuple((POS, b) for b in pos) + tuple((NEG, c) for c in neg)
            self.rules.setdefault(h, []).append(goals)
        self.tables = {}
        self.calls = {}  # the call graph: atom -> dict of called atoms, used as an ordered set
        self.work = []
        self.stats = {"delayed": 0, "answer_completion": 0, "nodes": 0}

    # The truth values.

    def _is_false(self, t):
        return t.complete and not t.true and not t.answers

    def value(self, atom):
        t = self.tables[atom]
        if t.true:
            return "true"
        return "false" if not t.answers else "undefined"

    def values(self):
        return {a: self.value(a) for a in self.tables}

    # The operations.

    def _push(self, node):
        self.work.append(node)
        self.stats["nodes"] += 1

    def _call(self, b, caller):
        if caller is not None:
            self.calls[caller][b] = None  # @line L29
        if b not in self.tables:  # @line L30
            self.tables[b] = _Table()
            self.calls[b] = {}
            for goals in self.rules.get(b, ()):
                self._push((b, goals, frozenset()))
        return self.tables[b]

    def _reduce(self, delay):
        """The delay without its true literals, or None if one of its literals is false."""
        out = []
        for sign, b in delay:
            t = self.tables[b]
            if t.true:
                if sign == NEG:
                    return None
            elif self._is_false(t):
                if sign == POS:
                    return None
            else:
                out.append((sign, b))
        return frozenset(out)

    def _make_true(self, h):
        t = self.tables[h]
        t.true = True
        t.complete = True  # a true atom of a ground program is final
        t.answers = set()
        t.waiters = []

    def _wake(self, h):
        t = self.tables[h]
        consumers, t.consumers = t.consumers, []
        for head, rest, delay in consumers:
            self._push((head, rest, delay if t.true else delay | {(POS, h)}))

    def _answer(self, h, delay):
        t = self.tables[h]
        d = self._reduce(delay)  # @line L31
        if d is None or t.true or d in t.answers:
            return
        first = not t.answers
        if not d:
            self._make_true(h)  # @line L32
        else:
            t.answers.add(d)  # @line L33
        if first:
            self._wake(h)  # @line L34

    def _simplify(self):
        changed = True
        while changed:  # @line L35
            changed = False
            for h, t in self.tables.items():
                if t.true or not t.answers:
                    continue
                kept = set()
                for d in t.answers:
                    r = self._reduce(d)
                    if r is None:
                        continue
                    if not r:
                        kept = None
                        break
                    kept.add(r)
                if kept is None:
                    self._make_true(h)
                    changed = True
                elif kept != t.answers:
                    t.answers = kept
                    changed = True

    def _step(self, node):
        h, goals, delay = node  # @line L4
        if self.tables[h].true:
            return
        if not goals:
            self._answer(h, delay)  # @line L5
            return
        (sign, b), rest = goals[0], goals[1:]  # @line L6
        t = self._call(b, h)
        if sign == POS:  # @line L7
            if t.true:
                self._push((h, rest, delay))  # @line L8
            elif t.answers:
                self._push((h, rest, delay | {(POS, b)}))  # @line L9
            elif not t.complete:
                t.consumers.append((h, rest, delay))  # @line L10
        else:  # @line L11
            if t.true:
                return  # @line L12
            if t.complete and not t.answers:
                self._push((h, rest, delay))  # @line L13
            elif t.complete:
                self._push((h, rest, delay | {(NEG, b)}))  # @line L14
            else:
                t.waiters.append((h, rest, delay))  # @line L15

    def _sink_component(self, open_tables):
        """The first component found by Tarjan's algorithm on the incomplete tables, which has no edge to another component."""
        inside = set(open_tables)
        index, low, on_stack, stack = {}, {}, set(), []
        for root in open_tables:
            if root in index:
                continue
            index[root] = low[root] = len(index)
            stack.append(root)
            on_stack.add(root)
            frames = [(root, iter(self.calls[root]))]
            while frames:
                v, it = frames[-1]
                descended = False
                for w in it:
                    if w not in inside:
                        continue
                    if w not in index:
                        index[w] = low[w] = len(index)
                        stack.append(w)
                        on_stack.add(w)
                        frames.append((w, iter(self.calls[w])))
                        descended = True
                        break
                    if w in on_stack:
                        low[v] = min(low[v], index[w])
                if descended:
                    continue
                frames.pop()
                if frames:
                    u = frames[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    comp = set()
                    while True:
                        w = stack.pop()
                        on_stack.discard(w)
                        comp.add(w)
                        if w == v:
                            return comp
        raise AssertionError("no incomplete table")

    def _complete(self, comp):
        for a in comp:
            self.tables[a].complete = True  # @line L22
        while True:  # @line L23
            self._simplify()  # @line L24
            supported, grew = set(), True
            while grew:  # @line L25
                grew = False
                for a in comp:
                    t = self.tables[a]
                    if a in supported or not t.answers:
                        continue
                    if any(all(b in supported for s, b in d if s == POS and b in comp) for d in t.answers):
                        supported.add(a)
                        grew = True
            dead = [a for a in comp if self.tables[a].answers and a not in supported]
            if not dead:  # @line L27
                break
            self.stats["answer_completion"] += 1
            for a in dead:
                self.tables[a].answers = set()  # @line L26
        for a in comp:
            t = self.tables[a]
            waiters, t.waiters, t.consumers = t.waiters, [], []
            for h, rest, delay in waiters:  # @line L28
                if t.true:
                    continue
                if not t.answers:
                    self._push((h, rest, delay))
                else:
                    self._push((h, rest, delay | {(NEG, a)}))

    def run(self, query):
        self._call(query, None)  # @line L1
        while True:  # @line L2
            while self.work:  # @line L3
                self._step(self.work.pop())
            self._simplify()  # @line L16
            open_tables = [a for a, t in self.tables.items() if not t.complete]
            if not open_tables:  # @line L17
                return self.values()
            comp = self._sink_component(open_tables)  # @line L18
            inner = [(b, node) for b in comp for node in self.tables[b].waiters if node[0] in comp]
            if inner:  # @line L19
                for b in comp:
                    t = self.tables[b]
                    t.waiters = [node for node in t.waiters if node[0] not in comp]
                for b, (h, rest, delay) in inner:
                    self.stats["delayed"] += 1
                    self._push((h, rest, delay | {(NEG, b)}))  # @line L20
            else:  # @line L21
                self._complete(comp)


def slg(program, query):
    """Evaluates the atom query and returns a dict from each tabled atom to "true", "false" or "undefined"."""
    return SLG(program).run(query)
