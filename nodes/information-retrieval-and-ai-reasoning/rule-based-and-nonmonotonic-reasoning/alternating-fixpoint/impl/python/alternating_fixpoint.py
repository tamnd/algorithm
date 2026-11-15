# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-fixpoint/. The authors are listed in prov/8YTFM5.jsonl.
"""The alternating fixpoint of Van Gelder (1993) for ground normal programs.

A program is a list of rules (head, pos, neg), as in lp.py. S(J) is the least
model of the Gelfond-Lifschitz reduct of the program by J. It is computed in
time linear in the size of the program by counting, for each rule, the
positive body atoms that are not yet derived.

well_founded(program) returns (true, false), two disjoint frozensets of atoms.
The atoms of the program in neither set are undefined. alternating_trace
returns the pairs (K_i, U_i) of the iteration.
"""

from collections import deque


def _atoms(program):
    out = set()
    for h, pos, neg in program:
        out.add(h)
        out.update(pos)
        out.update(neg)
    return out


class _Index:
    """The rules, with the list of the rules in which each atom occurs positively."""

    def __init__(self, program):
        self.rules = [(h, tuple(set(pos)), tuple(set(neg))) for h, pos, neg in program]
        self.occurs = {}
        for i, (_, pos, _) in enumerate(self.rules):
            for b in pos:
                self.occurs.setdefault(b, []).append(i)

    def s(self, j):
        """The least model of the reduct by j, by forward chaining with counters."""
        model, queue = set(), deque()  # @line L8
        count = []
        for h, pos, neg in self.rules:  # @line L9
            if any(c in j for c in neg):  # @line L10
                count.append(-1)
                continue
            count.append(len(pos))  # @line L11
            if not pos and h not in model:
                model.add(h)
                queue.append(h)
        while queue:  # @line L12
            b = queue.popleft()  # @line L13
            for i in self.occurs.get(b, ()):  # @line L14
                if count[i] > 0:
                    count[i] -= 1  # @line L15
                    h = self.rules[i][0]
                    if count[i] == 0 and h not in model:  # @line L16
                        model.add(h)
                        queue.append(h)
        return frozenset(model)  # @line L17


def least_model_of_reduct(program, j):
    """S(j): the least model of the reduct of the program by the set j."""
    return _Index(program).s(j)


def alternating_trace(program):
    """The list of pairs (K_i, U_i) with K_0 = {}, U_i = S(K_i) and K_{i+1} = S(U_i), up to the fixpoint."""
    index = _Index(program)
    k = frozenset()  # @line L1
    u = index.s(k)  # @line L2
    trace = [(k, u)]
    while True:  # @line L3
        k_next = index.s(u)  # @line L4
        if k_next == k:  # @line L5
            return trace
        k = k_next  # @line L6
        u = index.s(k)  # @line L7
        trace.append((k, u))


def well_founded(program):
    """The well-founded model as (true, false): true = K, false = the atoms not in U = S(K)."""
    k, u = alternating_trace(program)[-1]
    return k, frozenset(_atoms(program) - u)
