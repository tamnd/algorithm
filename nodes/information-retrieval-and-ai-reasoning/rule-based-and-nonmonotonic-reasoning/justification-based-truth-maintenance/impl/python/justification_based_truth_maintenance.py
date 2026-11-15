# SPDX-License-Identifier: MIT
# A justification-based truth maintenance system for the page
# https://algorithm.tamnd.com/justification-based-truth-maintenance/. The authors are listed in prov/.
"""A justification-based truth maintenance system (JTMS) with nonmonotonic justifications.

A node is any hashable value. A justification of a node x has an in-list and
an out-list: it is valid when every node of the in-list is IN and every node
of the out-list is OUT, and then x is believed. A justification with both lists
empty is a premise; an assumption is a premise that can be removed again.

Each node has the label IN, OUT or UNDEC. The labels are the well-founded
model of the network read as the normal logic program x <- ins, not outs:
IN is true, OUT is false and UNDEC is undefined. After each change only the
changed node and the nodes that depend on it are labelled again.
"""


IN, OUT, UNDEC = "IN", "OUT", "UNDEC"


class JTMS:
    def __init__(self):
        self.justs = {}  # id -> (node, ins, outs)
        self.of_node = {}  # node -> set of justification ids
        self.users = {}  # node -> set of nodes with a justification that mentions it
        self.label = {}
        self.next_id = 0
        self.relabelled = 0  # the number of nodes that relabel has visited

    def add_node(self, x):
        if x not in self.label:
            self.label[x] = OUT
            self.of_node[x] = set()
            self.users[x] = set()

    def justify(self, x, ins=(), outs=()):
        """Add the justification x <- ins, not outs and return its id."""
        for y in (x, *ins, *outs):
            self.add_node(y)
        jid = self.next_id
        self.next_id += 1
        self.justs[jid] = (x, tuple(ins), tuple(outs))
        self.of_node[x].add(jid)
        for y in (*ins, *outs):
            self.users[y].add(x)
        self.relabel(x)
        return jid

    def assume(self, x):
        return self.justify(x)

    def retract(self, jid):
        """Remove a justification. The users lists may keep x; a larger closed set to relabel is still correct."""
        x, _, _ = self.justs.pop(jid)
        self.of_node[x].discard(jid)
        self.relabel(x)

    def is_in(self, x):
        return self.label.get(x) == IN

    def _valid(self, jid):
        _, ins, outs = self.justs[jid]
        return all(self.label[y] == IN for y in ins) and all(self.label[y] == OUT for y in outs)

    def relabel(self, x):
        affected, stack = {x}, [x]  # @line L1
        while stack:
            y = stack.pop()
            for z in self.users[y]:
                if z not in affected:
                    affected.add(z)
                    stack.append(z)
        self.relabelled += len(affected)
        for y in affected:  # @line L2
            self.label[y] = None
        while True:  # @line L3
            changed = True
            while changed:  # @line L4
                changed = False
                for y in affected:
                    if self.label[y] is None and any(self._valid(j) for j in self.of_node[y]):
                        self.label[y] = IN  # @line L5
                        changed = True
            possible = set()  # @line L6
            grew = True
            while grew:
                grew = False
                for y in affected:
                    if y in possible or self.label[y] == OUT:
                        continue
                    for j in self.of_node[y]:
                        _, ins, outs = self.justs[j]
                        if all(self.label[b] in (IN, UNDEC) or b in possible for b in ins) and all(self.label[c] != IN for c in outs):
                            possible.add(y)
                            grew = True
                            break
            new_out = [y for y in affected if self.label[y] is None and y not in possible]
            for y in new_out:  # @line L7
                self.label[y] = OUT
            if not new_out:  # @line L8
                break
        for y in affected:  # @line L9
            if self.label[y] is None:
                self.label[y] = UNDEC
