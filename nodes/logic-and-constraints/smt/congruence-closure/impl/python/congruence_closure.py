# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/congruence-closure/. The authors are listed in prov/QSSXKY.jsonl.
"""Congruence closure over ground terms, with explanations.

A term is a string (a constant) or a tuple (f, t1, ..., tk) with k >= 1, the
application of the function symbol f to the terms t1, ..., tk.

The merge loop follows Downey, Sethi and Tarjan (1980): the smaller class is
relabelled, and the parents of the smaller class are looked up again in a
signature table. Each node is relabelled at most lg n times, so a run does
O(N log N) steps and table operations, where N is the number of nodes plus
the total number of argument positions. The proof forest and the explain
operation follow Nieuwenhuis and Oliveras (2005).
"""

from typing import Hashable, Union

Term = Union[str, tuple]


class CongruenceClosure:
    """Incremental congruence closure with a proof forest."""

    def __init__(self) -> None:
        self.ids: dict[Term, int] = {}
        self.terms: list[Term] = []
        self.head: list[str] = []
        self.args: list[tuple[int, ...]] = []
        self.rep: list[int] = []  # the representative of the class of each node
        self.members: list[list[int]] = []  # the nodes of each class, at its representative
        self.uses: list[list[int]] = []  # the applications with an argument in the class
        self.table: dict[tuple, int] = {}  # signature -> a node with that signature
        self.pparent: list[int] = []  # proof forest parent, or -1 at a root
        self.plabel: list[tuple] = []  # the reason of the edge to the parent
        self.pending: list[tuple[int, int, tuple]] = []

    # ------------------------------------------------------------ terms
    def _signature(self, p: int) -> tuple:
        return (self.head[p], tuple(self.rep[c] for c in self.args[p]))

    def add_term(self, t: Term) -> int:
        """Register t and all its subterms. Return the node id of t."""
        if t in self.ids:
            return self.ids[t]
        stack: list[tuple[Term, bool]] = [(t, False)]
        while stack:
            u, ready = stack.pop()
            if u in self.ids:
                continue
            if isinstance(u, tuple) and not ready:
                stack.append((u, True))
                for a in u[1:]:
                    if a not in self.ids:
                        stack.append((a, False))
                continue
            i = len(self.terms)
            self.ids[u] = i
            self.terms.append(u)
            if isinstance(u, tuple):
                self.head.append(u[0])
                self.args.append(tuple(self.ids[a] for a in u[1:]))
            else:
                self.head.append(u)
                self.args.append(())
            self.rep.append(i)  # @line L1
            self.members.append([i])
            self.uses.append([])
            self.pparent.append(-1)
            self.plabel.append(())
            if isinstance(u, tuple):  # @line L3
                for c in self.args[i]:
                    self.uses[self.rep[c]].append(i)  # @line L4
                sig = self._signature(i)
                q = self.table.get(sig)
                if q is None:
                    self.table[sig] = i  # @line L6
                else:
                    self.pending.append((i, q, ("cong", i, q)))  # @line L5
        self._propagate()
        return self.ids[t]

    # ------------------------------------------------------------ merging
    def merge(self, s: Term, t: Term, label: Hashable) -> None:
        """Assert s = t, with the given label as its reason."""
        a, b = self.add_term(s), self.add_term(t)
        self.pending.append((a, b, ("input", label)))  # @line L2
        self._propagate()

    def _make_root(self, a: int) -> None:
        """Reverse the proof forest path from a to its root."""
        prev, prev_label, x = -1, (), a
        while x != -1:
            nxt, nxt_label = self.pparent[x], self.plabel[x]
            self.pparent[x], self.plabel[x] = prev, prev_label
            prev, prev_label, x = x, nxt_label, nxt

    def _propagate(self) -> None:
        while self.pending:  # @line L7
            a, b, why = self.pending.pop()  # @line L8
            ra, rb = self.rep[a], self.rep[b]
            if ra == rb:  # @line L9
                continue
            if len(self.members[ra]) > len(self.members[rb]):  # @line L10
                a, b, ra, rb = b, a, rb, ra
            ra, rb = self.rep[a], self.rep[b]  # @line L11
            self._make_root(a)
            self.pparent[a], self.plabel[a] = b, why
            for x in self.members[ra]:  # @line L12
                self.rep[x] = rb
            self.members[rb].extend(self.members[ra])  # @line L13
            self.members[ra] = []
            moved, self.uses[ra] = self.uses[ra], []
            for p in moved:  # @line L14
                sig = self._signature(p)
                q = self.table.get(sig)
                if q is None:
                    self.table[sig] = p  # @line L15
                elif self.rep[q] != self.rep[p]:
                    self.pending.append((p, q, ("cong", p, q)))  # @line L16
            self.uses[rb].extend(moved)  # @line L17

    # ------------------------------------------------------------ queries
    def find(self, t: Term) -> int:
        return self.rep[self.add_term(t)]

    def are_equal(self, s: Term, t: Term) -> bool:
        return self.find(s) == self.find(t)

    def classes(self) -> list[list[Term]]:
        return [[self.terms[x] for x in m] for m in self.members if m]

    def explain(self, s: Term, t: Term) -> set:
        """Return a set of input labels whose equations entail s = t.

        Precondition: are_equal(s, t). The set need not be minimal.
        """
        a, b = self.ids[s], self.ids[t]
        if self.rep[a] != self.rep[b]:
            raise ValueError("the terms are not equal")
        out: set = set()
        done: set[int] = set()  # nodes whose edge to the parent is explained
        todo = [(a, b)]
        while todo:
            u, v = todo.pop()
            if u == v:
                continue
            anc: dict[int, int] = {}
            x, d = u, 0
            while x != -1:
                anc[x] = d
                x, d = self.pparent[x], d + 1
            y = v
            while y not in anc:
                y = self.pparent[y]
            for start in (u, v):
                x = start
                while x != y:
                    if x not in done:
                        done.add(x)
                        why = self.plabel[x]
                        if why[0] == "input":
                            out.add(why[1])
                        else:
                            p, q = why[1], why[2]
                            todo.extend(zip(self.args[p], self.args[q]))
                    x = self.pparent[x]
        return out


def euf_satisfiable(eqs: list[tuple[Term, Term]], diseqs: list[tuple[Term, Term]]) -> bool:
    """Decide a conjunction of equalities and disequalities of ground terms."""
    cc = CongruenceClosure()
    for t in [x for e in eqs + diseqs for x in e]:
        cc.add_term(t)
    for i, (s, t) in enumerate(eqs):
        cc.merge(s, t, i)
    return all(not cc.are_equal(s, t) for s, t in diseqs)  # @line L18
