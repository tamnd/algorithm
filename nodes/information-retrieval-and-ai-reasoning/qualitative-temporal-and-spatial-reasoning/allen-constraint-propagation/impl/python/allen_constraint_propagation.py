# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allen-constraint-propagation/. The authors are listed in prov/7P7E2R.jsonl.

"""Allen's incremental constraint propagation for interval networks.

The network keeps a full matrix of labels. A label is a mask over Allen's 13
base relations, in the order of qcn.ALLEN_NAMES. add(i, j, s) intersects the
label of (i, j) with s and propagates the change through the composition table
until no label changes. The labels are then path consistent (algebraically
closed). That is necessary for consistency, and for some subclasses, such as
the ORD-Horn relations, it is also sufficient.
"""

from collections import deque

from qcn import Calculus, allen


class AllenNetwork:
    """An interval network on the nodes 0 .. n-1 that starts with no constraints."""

    def __init__(self, n: int, calc: Calculus | None = None) -> None:
        self.calc = calc if calc is not None else allen()
        self.n = n
        u, e = self.calc.universal, self.calc.identity
        self.r = [[e if i == j else u for j in range(n)] for i in range(n)]
        self.ok = True  # False after a contradiction; the labels are then not meaningful

    def label(self, i: int, j: int) -> int:
        return self.r[i][j]

    def add(self, i: int, j: int, s: int, stats: dict | None = None) -> bool:
        """Add the constraint (i s j), with i != j, and propagate it.

        Return False if the network is now known to be inconsistent. Otherwise
        every label is algebraically closed. Over any sequence of a additions the
        total cost is O(n^3 + a) compositions, because a label can shrink at most
        13 times and each shrink costs O(n) work later.
        """
        if not self.ok:
            return False
        calc, r = self.calc, self.r
        t = r[i][j] & s  # @line L1
        if t == 0:  # @line L2
            self.ok = False
            return False
        if t == r[i][j]:  # @line L3
            return True
        r[i][j], r[j][i] = t, calc.converse(t)  # @line L4
        queue = deque([(i, j)])
        queued = {(min(i, j), max(i, j))}

        def push(a: int, b: int) -> None:
            key = (min(a, b), max(a, b))
            if key not in queued:
                queued.add(key)
                queue.append((a, b))

        while queue:  # @line L5
            p, q = queue.popleft()  # @line L6
            queued.discard((min(p, q), max(p, q)))
            if stats is not None:
                stats["pops"] = stats.get("pops", 0) + 1
            for k in range(self.n):  # @line L7
                if k == p or k == q:
                    continue
                t = r[p][k] & calc.compose(r[p][q], r[q][k])  # @line L8
                if t == 0:  # @line L9
                    self.ok = False
                    return False
                if t != r[p][k]:  # @line L10
                    r[p][k], r[k][p] = t, calc.converse(t)
                    push(p, k)
                t = r[k][q] & calc.compose(r[k][p], r[p][q])  # @line L11
                if t == 0:  # @line L12
                    self.ok = False
                    return False
                if t != r[k][q]:  # @line L13
                    r[k][q], r[q][k] = t, calc.converse(t)
                    push(k, q)
        return True  # @line L14
