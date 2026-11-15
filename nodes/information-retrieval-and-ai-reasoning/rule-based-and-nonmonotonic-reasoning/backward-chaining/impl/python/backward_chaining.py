# SPDX-License-Identifier: MIT
# Backward chaining for the page https://algorithm.tamnd.com/backward-chaining/. The authors are listed in prov/.
"""Backward chaining over propositional definite rules, with a loop check and memo tables.

A rule is (head, body): head is an atom and body is a tuple of atoms. A fact is
a rule with an empty body. Atoms are any hashable values. The search proves a
goal depth first: to prove an atom, try its rules in the given order and prove
the body atoms from left to right. An atom that is already on the current goal
stack is not tried again (the loop check). Atoms that were proved are stored.
An atom whose failure did not depend on an atom of the stack above it is stored
as failed; other failures are not stored, because the same atom can succeed
later from another stack.

BackwardChainer(rules).prove(goal) returns True exactly when goal is in the
least model. The field calls counts the calls of the inner procedure.
"""

INF = float("inf")


class BackwardChainer:
    def __init__(self, rules):
        self.rules = {}
        for head, body in rules:
            self.rules.setdefault(head, []).append(tuple(body))
        self.proved = set()  # @line L1
        self.failed = set()
        self.depth = {}  # the atoms on the goal stack, with their depths
        self.calls = 0
        self.trace = []

    def prove(self, goal):
        return self._prove(goal)[0]  # @line L2

    def _prove(self, a):
        """Return (ok, low): low is the smallest stack depth of an atom that a loop check met, or INF."""
        self.calls += 1
        if a in self.proved:  # @line L3
            self.trace.append(("memo true", a))
            return True, INF
        if a in self.failed:  # @line L4
            self.trace.append(("memo false", a))
            return False, INF
        if a in self.depth:  # @line L5
            self.trace.append(("loop", a))
            return False, self.depth[a]
        k = len(self.depth)  # @line L6
        self.depth[a] = k
        low = INF
        for body in self.rules.get(a, []):  # @line L7
            ok = True
            for b in body:  # @line L8
                ok, c = self._prove(b)  # @line L9
                low = min(low, c)
                if not ok:  # @line L10
                    break
            if ok:
                del self.depth[a]  # @line L11
                self.proved.add(a)
                self.trace.append(("proved", a))
                return True, INF
        del self.depth[a]  # @line L12
        if low >= k:  # @line L13
            self.failed.add(a)
            self.trace.append(("failed", a))
            return False, INF
        self.trace.append(("failed for now", a))
        return False, low  # @line L14


def backward_chain(rules, goal):
    """True exactly when goal follows from the definite rules."""
    return BackwardChainer(rules).prove(goal)
