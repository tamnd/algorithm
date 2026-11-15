# SPDX-License-Identifier: MIT
# An assumption-based truth maintenance system for the page
# https://algorithm.tamnd.com/assumption-based-truth-maintenance/. The authors are listed in prov/.
"""An assumption-based truth maintenance system (ATMS), after de Kleer (1986).

Nodes are hashable values. Some nodes are assumptions. A justification is a
Horn clause x <- a_1, ..., a_k over nodes; with k = 0 the node x is a premise.
The node FALSE stands for a contradiction: a justification FALSE <- a_1, ...,
a_k says that the antecedents cannot hold together.

An environment is a frozenset of assumptions. It is inconsistent when FALSE
follows from it, and the minimal inconsistent environments are the nogoods.
The label of a node is the set of environments in which the node holds, kept
sound (each one derives the node), consistent (none contains a nogood),
minimal (none is a superset of another) and complete (every consistent
environment that derives the node contains one of them).

Labels only grow under new justifications, except that a new nogood removes
the environments that contain it. Propagation sends only the new environments
of a node to the justifications that use the node.
"""

from collections import deque
from itertools import product

FALSE = "FALSE"


def minimal(envs):
    """The environments of envs that have no proper subset in envs, without duplicates."""
    envs = sorted(set(envs), key=len)
    out = []
    for e in envs:
        if not any(o <= e for o in out):
            out.append(e)
    return out


class ATMS:
    def __init__(self):
        self.label = {FALSE: []}
        self.assumptions = set()
        self.justs = []  # (consequent, antecedents)
        self.consumers = {FALSE: []}  # node -> indices of the justifications that use it
        self.nogoods = []

    def add_node(self, x):
        if x not in self.label:
            self.label[x] = []
            self.consumers[x] = []

    def add_assumption(self, a):
        self.add_node(a)
        self.assumptions.add(a)
        self._run(deque([(a, [frozenset([a])])]))

    def consistent(self, env):
        return not any(n <= env for n in self.nogoods)

    def holds(self, x, env):
        """True when x holds in the environment env: some label environment is a subset of env."""
        return self.consistent(env) and any(e <= env for e in self.label.get(x, []))

    def justify(self, x, antecedents):
        self.add_node(x)
        for a in antecedents:
            self.add_node(a)
        k = len(self.justs)
        self.justs.append((x, tuple(antecedents)))
        for a in set(antecedents):
            self.consumers[a].append(k)
        self._run(deque([(x, self._combine(k, None, None))]))

    def _combine(self, k, changed, delta):
        """The minimal consistent unions of one environment from the label of each antecedent of justification k.
        When changed is a node, only the products that take an environment of delta for one occurrence of it."""
        _, ants = self.justs[k]
        lists = [self.label[a] for a in ants]
        products = []
        if changed is None:
            products.append(lists)
        else:
            for i, a in enumerate(ants):  # @line L9
                if a == changed:
                    products.append(lists[:i] + [delta] + lists[i + 1 :])
        envs = []
        for ls in products:
            for choice in product(*ls):
                e = frozenset().union(*choice)  # @line L10
                if self.consistent(e):
                    envs.append(e)
        return minimal(envs)  # @line L11

    def _run(self, queue):
        while queue:  # @line L1
            x, envs = queue.popleft()  # @line L2
            envs = [e for e in envs if self.consistent(e)]
            new = minimal(e for e in envs if not any(o <= e for o in self.label[x]))  # @line L3
            if not new:  # @line L4
                continue
            if x == FALSE:  # @line L5
                for e in new:
                    self._nogood(e)
                continue
            self.label[x] = [o for o in self.label[x] if not any(e <= o for e in new)] + new  # @line L6
            for k in self.consumers[x]:  # @line L7
                queue.append((self.justs[k][0], self._combine(k, x, new)))  # @line L8

    def _nogood(self, env):
        if not self.consistent(env):
            return
        self.nogoods = [n for n in self.nogoods if not env <= n] + [env]  # @line L12
        for x in self.label:  # @line L13
            self.label[x] = [e for e in self.label[x] if not env <= e]
