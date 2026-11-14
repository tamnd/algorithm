# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/and-or-graph-of-assembly-plans/. The authors are listed in prov/XTSFWX.jsonl.
"""The AND/OR graph of all monotone two-handed assembly plans.

A node is a connected subassembly (a bit mask of parts). A hyperarc joins a
node S to the two nodes S1 and S2 of a feasible split of S. A plan is a
solution tree: the root, and for each node of the tree with two or more
parts, one of its hyperarcs.

The default model: parts are axis-aligned boxes, a subassembly counts only
if its parts are connected in the liaison graph, and a split is feasible if
one side can leave the other by one translation to infinity along one of
the six axis directions.
"""

from assembly_boxes import AXES6, blocks, face_contact


def low_bit(mask):
    return mask & -mask


class AndOrGraph:
    def __init__(self, n, adj, feasible):
        """n parts, adj[i] the bit mask of the liaison neighbours of i, and
        feasible(s1, s2) the test of a split into two connected sets."""
        self.n = n
        self.adj = adj
        self.feasible = feasible
        self.root = (1 << n) - 1
        self.arcs = {}              # node -> list of (s1, s2), lowest part in s1
        self._plans = {}
        if n > 0:
            self._decompose(self.root)  # @line L1

    # ---- liaison graph queries ----

    def neighbourhood(self, mask):
        out = 0
        m = mask
        while m:
            b = low_bit(m)
            out |= self.adj[b.bit_length() - 1]
            m ^= b
        return out & ~mask

    def connected(self, mask):
        if mask == 0:
            return False
        reach = low_bit(mask)
        while True:
            grow = (reach | self.neighbourhood(reach)) & mask
            if grow == reach:
                return reach == mask
            reach = grow

    def _connected_containing(self, v, within):
        """Each connected set S1 with v in S1 inside within, once."""
        out = []

        def grow(s, banned):
            out.append(s)
            cand = self.neighbourhood(s) & within & ~banned
            while cand:
                w = low_bit(cand)
                grow(s | w, banned)
                banned |= w
                cand ^= w

        grow(v, ~within)
        return out

    # ---- construction ----

    def _decompose(self, root):
        stack = [root]
        while stack:
            s = stack.pop()
            if s in self.arcs:  # @line L2
                continue
            self.arcs[s] = []  # @line L3
            if s & (s - 1) == 0:  # @line L4
                continue
            v = low_bit(s)  # @line L5
            for s1 in self._connected_containing(v, s):  # @line L6
                if s1 == s:
                    continue
                s2 = s & ~s1  # @line L7
                if self.connected(s2) and self.feasible(s1, s2):  # @line L8
                    self.arcs[s].append((s1, s2))  # @line L9
                    stack.append(s1)
                    stack.append(s2)

    # ---- queries ----

    def nodes(self):
        return sorted(self.arcs)

    def hyperarc_count(self):
        return sum(len(a) for a in self.arcs.values())

    def count_plans(self, s=None):
        """The number of solution trees below s, by memoized recursion."""
        if s is None:
            s = self.root
        if s in self._plans:
            return self._plans[s]
        if s & (s - 1) == 0:  # @line L12
            return 1
        total = 0
        for s1, s2 in self.arcs[s]:  # @line L13
            total += self.count_plans(s1) * self.count_plans(s2)
        self._plans[s] = total
        return total

    def count_linear_plans(self, s=None, memo=None):
        """Solution trees in which every split takes off one single part."""
        if s is None:
            s = self.root
        if memo is None:
            memo = {}
        if s & (s - 1) == 0:
            return 1
        if s in memo:
            return memo[s]
        total = 0
        for s1, s2 in self.arcs[s]:
            if s1 & (s1 - 1) == 0 or s2 & (s2 - 1) == 0:
                total += (self.count_linear_plans(s1, memo)
                          * self.count_linear_plans(s2, memo))
        memo[s] = total
        return total

    def plans(self, s=None):
        """Yield each plan as a nested pair of frozensets of parts."""
        if s is None:
            s = self.root
        if s & (s - 1) == 0:
            yield s.bit_length() - 1
            return
        for s1, s2 in self.arcs[s]:
            for t1 in self.plans(s1):
                for t2 in self.plans(s2):
                    yield frozenset((t1, t2))

    def solvable_nodes(self):
        """The nodes with at least one plan below them."""
        return [s for s in self.nodes() if self.count_plans(s) > 0]


def from_boxes(boxes, motions=AXES6):
    """The AND/OR graph of a product of boxes under one-step translations."""
    n = len(boxes)
    adj = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if face_contact(boxes[i], boxes[j]) is not None:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    # stop[d][i]: the parts that block part i when it moves along d
    stop = {d: [sum(1 << j for j in range(n) if j != i and blocks(boxes[i], boxes[j], d))
                for i in range(n)] for d in motions}

    def free(s1, s2, d):
        m = s1
        while m:
            b = low_bit(m)
            if stop[d][b.bit_length() - 1] & s2:
                return False
            m ^= b
        return True

    def feasible(s1, s2):
        for d in motions:
            if free(s1, s2, d) or free(s2, s1, d):  # @line L10
                return True
        return False  # @line L11

    return AndOrGraph(n, adj, feasible)
