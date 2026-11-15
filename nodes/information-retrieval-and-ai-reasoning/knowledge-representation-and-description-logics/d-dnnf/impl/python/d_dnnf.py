# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-dnnf/. The authors are listed in prov/FSRAPA.jsonl.
"""A compiler from CNF to d-DNNF, and the linear-time queries of d-DNNF.

A CNF is a list of clauses. A clause is a tuple of nonzero integers in the
DIMACS style: the literal 3 is x3 and the literal -3 is the negation of x3.
The variables are 1 to n.

A circuit lives in a Circuit object. Node 0 is FALSE and node 1 is TRUE.
Every other node is one of

    ("lit", l)                  a literal
    ("and", (c1, c2, ...))      a conjunction of the child nodes
    ("or", (c1, c2, ...))       a disjunction of the child nodes

Nodes are hash-consed: the same triple always gets the same id. A child
always has a smaller id than its parent, so a loop over the ids in
increasing order visits the children before the parents. Each query below is
one such loop, so its time is linear in the number of nodes plus edges.

The compiler is exhaustive DPLL with unit propagation, a split into
independent components and a cache of compiled components (the method of
Huang and Darwiche, "The language of search", JAIR 29, 2007). Its output is
a decision-DNNF: every or-node is a decision node (x and A) or (not x and B).
Decision-DNNF is a subset of d-DNNF, and this module does not produce the
other members of d-DNNF.
"""

from __future__ import annotations

FALSE, TRUE = 0, 1


class Circuit:
    """A store of hash-consed NNF nodes."""

    def __init__(self) -> None:
        self.nodes: list[tuple] = [("false",), ("true",)]
        self.unique: dict[tuple, int] = {}

    def _make(self, key: tuple) -> int:
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def lit(self, l: int) -> int:
        return self._make(("lit", l))

    def conj(self, children) -> int:
        """The and of the children, with FALSE and TRUE folded."""
        kept = set()
        for c in children:
            if c == FALSE:
                return FALSE
            if c != TRUE:
                kept.add(c)
        if not kept:
            return TRUE
        if len(kept) == 1:
            return kept.pop()
        return self._make(("and", tuple(sorted(kept))))

    def disj(self, children) -> int:
        """The or of the children, with FALSE and TRUE folded."""
        kept = set()
        for c in children:
            if c == TRUE:
                return TRUE
            if c != FALSE:
                kept.add(c)
        if not kept:
            return FALSE
        if len(kept) == 1:
            return kept.pop()
        return self._make(("or", tuple(sorted(kept))))

    # ---------------------------------------------------------------- queries

    def size(self, root: int) -> int:
        """The number of edges below the root."""
        return sum(len(self.nodes[u][1]) for u in self.reachable(root) if self.nodes[u][0] in ("and", "or"))

    def reachable(self, root: int) -> list[int]:
        """The ids of the nodes below the root (root included), in increasing order."""
        seen = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            key = self.nodes[u]
            if key[0] in ("and", "or"):
                for c in key[1]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return sorted(seen)

    def variables(self, root: int) -> dict[int, frozenset[int]]:
        """vars(u) for each node u below the root."""
        out: dict[int, frozenset[int]] = {}
        for u in self.reachable(root):
            key = self.nodes[u]
            if key[0] == "lit":
                out[u] = frozenset([abs(key[1])])
            elif key[0] in ("and", "or"):
                out[u] = frozenset().union(*(out[c] for c in key[1]))
            else:
                out[u] = frozenset()
        return out

    def evaluate(self, root: int, assignment: dict[int, bool]) -> bool:
        """The value of the circuit under a full assignment of its variables."""
        val: dict[int, bool] = {}
        for u in self.reachable(root):
            key = self.nodes[u]
            if key[0] == "lit":
                l = key[1]
                val[u] = assignment[abs(l)] == (l > 0)
            elif key[0] == "and":
                val[u] = all(val[c] for c in key[1])
            elif key[0] == "or":
                val[u] = any(val[c] for c in key[1])
            else:
                val[u] = u == TRUE
        return val[root]

    def consistent(self, root: int) -> bool:
        """CO: is the circuit satisfiable? Correct when the circuit is decomposable."""
        val: dict[int, bool] = {}
        for u in self.reachable(root):  # @line L12
            key = self.nodes[u]
            if key[0] == "lit":  # @line L13
                val[u] = True
            elif key[0] == "and":  # @line L14
                val[u] = all(val[c] for c in key[1])
            elif key[0] == "or":  # @line L15
                val[u] = any(val[c] for c in key[1])
            else:
                val[u] = u == TRUE
        return val[root]  # @line L16

    def condition(self, root: int, term: set[int]) -> int:
        """The circuit with each literal of the term set to TRUE and its negation to FALSE."""
        new: dict[int, int] = {}
        for u in self.reachable(root):  # @line L17
            key = self.nodes[u]
            if key[0] == "lit":
                l = key[1]
                new[u] = TRUE if l in term else FALSE if -l in term else u
            elif key[0] == "and":
                new[u] = self.conj(new[c] for c in key[1])
            elif key[0] == "or":
                new[u] = self.disj(new[c] for c in key[1])
            else:
                new[u] = u
        return new[root]

    def entails_clause(self, root: int, clause) -> bool:
        """CE: does the circuit entail the clause? Uses conditioning on the negated clause, then CO."""
        lits = set(clause)
        if any(-l in lits for l in lits):  # @line L18
            return True
        return not self.consistent(self.condition(root, {-l for l in lits}))  # @line L19

    def smooth(self, root: int, all_vars) -> int:
        """An equivalent smooth circuit whose root mentions every variable of all_vars."""
        vs = self.variables(root)
        new: dict[int, int] = {}

        def pad(u: int, have: frozenset[int], want: frozenset[int]) -> int:
            missing = sorted(want - have)
            return self.conj([u] + [self.disj([self.lit(v), self.lit(-v)]) for v in missing])

        for u in self.reachable(root):  # @line L20
            key = self.nodes[u]
            if key[0] == "and":
                new[u] = self.conj(new[c] for c in key[1])
            elif key[0] == "or":
                new[u] = self.disj(pad(new[c], vs[c], vs[u]) for c in key[1])  # @line L21
            else:
                new[u] = u
        return pad(new[root], vs[root], frozenset(all_vars))  # @line L22

    def is_smooth(self, root: int) -> bool:
        vs = self.variables(root)
        return all(
            len({vs[c] for c in self.nodes[u][1]}) == 1 for u in vs if self.nodes[u][0] == "or"
        )

    def count_smooth(self, root: int) -> int:
        """CT on a smooth d-DNNF: literals count 1, an and multiplies, an or adds."""
        cnt: dict[int, int] = {}
        for u in self.reachable(root):  # @line L23
            key = self.nodes[u]
            if key[0] == "lit":
                cnt[u] = 1
            elif key[0] == "and":
                p = 1
                for c in key[1]:
                    p *= cnt[c]
                cnt[u] = p
            elif key[0] == "or":
                cnt[u] = sum(cnt[c] for c in key[1])
            else:
                cnt[u] = 1 if u == TRUE else 0
        return cnt[root]  # @line L24

    def model_count(self, root: int, n: int) -> int:
        """The number of models over the variables 1 to n."""
        return self.count_smooth(self.smooth(root, range(1, n + 1)))


# -------------------------------------------------------------------- compiler


def _simplify(clauses: frozenset, lit: int):
    """The clauses after setting lit to true, or None on an empty clause."""
    out = set()
    for c in clauses:
        if lit in c:
            continue
        if -lit in c:
            c = c - {-lit}
            if not c:
                return None
        out.add(c)
    return frozenset(out)


def _components(clauses: frozenset) -> list[frozenset]:
    """The clauses grouped into sets that share no variable."""
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for c in clauses:
        vs = [abs(l) for l in c]
        for v in vs:
            parent.setdefault(v, v)
        for v in vs[1:]:
            a, b = find(vs[0]), find(v)
            if a != b:
                parent[a] = b
    groups: dict[int, set] = {}
    for c in clauses:
        groups.setdefault(find(abs(next(iter(c)))), set()).add(c)
    return [frozenset(g) for g in groups.values()]


class Compiler:
    """Exhaustive DPLL with components and a cache; the trace is a decision-DNNF."""

    def __init__(self, circuit: Circuit | None = None) -> None:
        self.circuit = circuit or Circuit()
        self.cache: dict[frozenset, int] = {}
        self.decisions = 0

    def compile(self, cnf) -> int:
        clauses = frozenset(frozenset(c) for c in cnf)
        if any(any(-l in c for l in c) for c in clauses):
            clauses = frozenset(c for c in clauses if not any(-l in c for l in c))
        return self._compile(clauses)

    def _compile(self, clauses: frozenset) -> int:
        cc = self.circuit
        if not clauses:  # @line L1
            return TRUE
        if clauses in self.cache:  # @line L3
            return self.cache[clauses]
        # Unit propagation: the units become and-children of the result.
        units: list[int] = []
        rest = clauses
        while True:
            unit = next((c for c in rest if len(c) == 1), None)  # @line L4
            if unit is None:
                break
            l = next(iter(unit))
            units.append(l)
            rest = _simplify(rest, l)
            if rest is None:  # @line L2
                self.cache[clauses] = FALSE
                return FALSE
        if units:
            result = cc.conj([cc.lit(l) for l in units] + [self._compile(rest)])  # @line L5
        else:
            parts = _components(rest)
            if len(parts) > 1:  # @line L6
                result = cc.conj(self._compile(p) for p in parts)  # @line L7
            else:  # @line L8
                result = self._decide(rest)
        self.cache[clauses] = result  # @line L11
        return result

    def _decide(self, clauses: frozenset) -> int:
        cc = self.circuit
        freq: dict[int, int] = {}
        for c in clauses:
            for l in c:
                freq[abs(l)] = freq.get(abs(l), 0) + 1
        x = min(freq, key=lambda v: (-freq[v], v))  # @line L9
        self.decisions += 1
        branches = []
        for l in (x, -x):
            sub = _simplify(clauses, l)
            body = FALSE if sub is None else self._compile(sub)
            branches.append(cc.conj([cc.lit(l), body]))
        return cc.disj(branches)  # @line L10


def compile_cnf(cnf) -> tuple[Circuit, int]:
    """Compile a CNF; return the circuit store and the root id."""
    comp = Compiler()
    root = comp.compile(cnf)
    return comp.circuit, root
