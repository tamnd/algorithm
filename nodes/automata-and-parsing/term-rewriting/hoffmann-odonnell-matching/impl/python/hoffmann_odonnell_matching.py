# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoffmann-odonnell-matching/. The authors are listed in prov/R5TC80.jsonl.

"""Hoffmann-O'Donnell bottom-up tree pattern matching.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). Positions are tuples of 1-based argument indexes.

Preprocessing builds the pattern forest PF: every subterm of every pattern,
with all variables identified with one wildcard v (id 0). A match set is the
set of members of PF that match one subject node. The preprocessing computes
every reachable match set and, for each symbol f of arity k, the table
T[f/k][(M1, ..., Mk)] of the match set of f(t1, ..., tk) when ti has the match
set Mi. This is a deterministic bottom-up tree automaton. Matching is then one
table lookup for each node of the subject.

The wildcard forgets which variables are equal, so the automaton decides
matching for linear patterns. A non-linear pattern is reported only after an
equality check of the subterms that its repeated variables take. Variables of
the subject are treated as constants. All functions use explicit stacks.
"""

from itertools import product
from typing import Optional, Union

Term = Union[str, tuple]
State = int


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def term_eq(s: Term, t: Term) -> bool:
    """Syntactic equality, without recursion."""
    stack = [(s, t)]
    while stack:
        u, v = stack.pop()
        if u is v:
            continue
        if is_var(u) or is_var(v):
            if u != v:
                return False
            continue
        if len(u) != len(v) or u[0] != v[0]:
            return False
        stack.extend(zip(u[1:], v[1:]))
    return True


def match(pattern: Term, t: Term) -> Optional[dict[str, Term]]:
    """The matcher sigma with pattern sigma = t, or None."""
    sigma: dict[str, Term] = {}
    stack = [(pattern, t)]
    while stack:
        p, u = stack.pop()
        if is_var(p):
            if p in sigma:
                if not term_eq(sigma[p], u):
                    return None
            else:
                sigma[p] = u
        elif is_var(u) or len(p) != len(u) or p[0] != u[0]:
            return None
        else:
            stack.extend(zip(p[1:], u[1:]))
    return sigma


def is_linear(t: Term) -> bool:
    seen: set[str] = set()
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            if u in seen:
                return False
            seen.add(u)
        else:
            stack.extend(u[1:])
    return True


class Matcher:
    """The bottom-up matching automaton of a list of patterns."""

    def __init__(self, patterns: list[Term], max_states: int = 100000) -> None:
        self.patterns = list(patterns)
        # PF by hash-consing: id 0 is the wildcard, other ids are (f, k, child ids)
        self.node_id: dict[tuple, int] = {}
        self.by_symbol: dict[tuple, list[tuple[int, tuple[int, ...]]]] = {}
        self.root_id: list[int] = []
        for p in self.patterns:  # @line L1
            self.root_id.append(self._intern(p))
        self.linear = [is_linear(p) for p in self.patterns]
        self.states: list[frozenset[int]] = []  # @line L2
        self.state_of: dict[frozenset[int], State] = {}
        self.table: dict[tuple, dict[tuple[State, ...], State]] = {sym: {} for sym in self.by_symbol}
        self.wild = self._add(frozenset([0]))  # the match set of a node whose symbol is in no pattern
        changed = True
        while changed:  # @line L3
            changed = False
            for sym, members in self.by_symbol.items():  # @line L4
                k = sym[1]
                tab = self.table[sym]
                for tup in product(range(len(self.states)), repeat=k):
                    if tup in tab:
                        continue
                    m = {0}  # @line L5
                    for pid, kids in members:
                        if all(kids[i] in self.states[tup[i]] for i in range(k)):
                            m.add(pid)
                    s = self._add(frozenset(m))  # @line L6
                    if s == len(self.states) - 1 and len(self.states) > max_states:
                        raise RuntimeError("too many match sets")
                    tab[tup] = s
                    changed = True
        # for each state, the patterns it reports
        self.reports: list[list[int]] = [
            [j for j, rid in enumerate(self.root_id) if rid in m] for m in self.states
        ]  # @line L7

    def _add(self, m: frozenset[int]) -> State:
        s = self.state_of.get(m)
        if s is None:
            s = len(self.states)
            self.states.append(m)
            self.state_of[m] = s
        return s

    def _intern(self, p: Term) -> int:
        ids: list[int] = []
        stack: list[tuple[bool, Term]] = [(False, p)]
        while stack:
            done, u = stack.pop()
            if is_var(u):
                ids.append(0)
            elif done or len(u) == 1:
                k = len(u) - 1
                kids = tuple(ids[len(ids) - k:]) if k else ()
                del ids[len(ids) - k:]
                key = (u[0], k) + kids
                pid = self.node_id.get(key)
                if pid is None:
                    pid = len(self.node_id) + 1
                    self.node_id[key] = pid
                    self.by_symbol.setdefault((u[0], k), []).append((pid, kids))
                ids.append(pid)
            else:
                stack.append((True, u))
                for a in reversed(u[1:]):
                    stack.append((False, a))
        return ids[0]

    def num_states(self) -> int:
        return len(self.states)

    def match_sets(self, t: Term) -> tuple[list[Term], list[int], list[int], list[State]]:
        """Number the nodes of t and compute their states bottom-up.

        Returns the subterms, the parent and argument index of each node (for
        positions), and the state of each node.
        """
        nodes: list[Term] = [t]
        parent: list[int] = [-1]
        argi: list[int] = [0]
        kids: list[list[int]] = [[]]
        state: list[State] = [self.wild]
        stack: list[tuple[bool, int]] = [(False, 0)]
        while stack:  # @line L8
            done, i = stack.pop()
            u = nodes[i]
            if is_var(u):
                state[i] = self.wild  # @line L9
            elif done or len(u) == 1:
                tab = self.table.get((u[0], len(u) - 1))
                key = tuple(state[c] for c in kids[i])
                state[i] = self.wild if tab is None else tab[key]  # @line L10
            else:
                stack.append((True, i))
                for a in range(1, len(u)):
                    nodes.append(u[a])
                    parent.append(i)
                    argi.append(a)
                    kids.append([])
                    state.append(self.wild)
                    kids[i].append(len(nodes) - 1)
                for c in reversed(kids[i]):
                    stack.append((False, c))
        return nodes, parent, argi, state

    def find_all(self, t: Term) -> list[tuple[tuple[int, ...], int]]:
        """All (position, pattern index) with the pattern matching t at the position.

        The list is sorted by position, then by pattern index.
        """
        nodes, parent, argi, state = self.match_sets(t)
        out: list[tuple[tuple[int, ...], int]] = []
        for i, u in enumerate(nodes):
            for j in self.reports[state[i]]:  # @line L11
                if self.linear[j] or match(self.patterns[j], u) is not None:  # @line L12
                    pos: list[int] = []
                    k = i
                    while parent[k] >= 0:
                        pos.append(argi[k])
                        k = parent[k]
                    out.append((tuple(reversed(pos)), j))
        out.sort()
        return out  # @line L13
