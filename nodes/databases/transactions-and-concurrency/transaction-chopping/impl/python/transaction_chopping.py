# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transaction-chopping/. The authors are listed in prov/G7FCSD.jsonl.
"""Transaction chopping of Shasha, Llirbat, Simon and Valduriez (1995).

A transaction is a list of statements. A statement is ("r", item),
("w", item) or ("rollback",); the last one marks a place where the
program may roll back. A chopping of one transaction is a list of pieces,
and a piece is a half-open interval (start, end) of statement positions.
The pieces are contiguous, in order, and cover every position. A chopping
of the set is one such list per transaction.

finest_chopping(txns)       the finest rollback-safe chopping with no SC-cycle
has_sc_cycle(txns, chop)    the SC-cycle test by connected components
is_rollback_safe(t, pieces) every rollback statement is in the first piece
is_correct(txns, chop)      rollback-safe and no SC-cycle
"""

ROLLBACK = "rollback"


def is_access(op):
    return op[0] in ("r", "w")


def conflict(a, b):
    """Two accesses conflict when they touch the same item and one writes it."""
    return (is_access(a) and is_access(b) and a[1] == b[1]
            and (a[0] == "w" or b[0] == "w"))


class UnionFind:
    """Union by size with path compression."""

    def __init__(self, keys):
        self.parent = {k: k for k in keys}
        self.size = {k: 1 for k in self.parent}

    def find(self, k):
        root = k
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[k] != root:
            self.parent[k], k = root, self.parent[k]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]


def _txn_conflicts(txns):
    """hits[i][p] is the set of j != i with an access in conflict with the
    statement at position p of T_i; adj[j] is the set of k that conflict with T_j."""
    n = len(txns)
    hits = [[set() for _ in t] for t in txns]
    adj = [set() for _ in range(n)]
    for i in range(n):
        for p, a in enumerate(txns[i]):
            for j in range(n):
                if j != i and any(conflict(a, b) for b in txns[j]):
                    hits[i][p].add(j)
                    adj[i].add(j)
    return hits, adj


def _other_components(n, adj, i):
    """Union-find over the transactions other than T_i, joined by conflicts."""
    others = [j for j in range(n) if j != i]
    uf = UnionFind(others)  # @line L2
    for j in others:
        for k in adj[j]:
            if k != i:
                uf.union(j, k)  # @line L3
    return uf


def _intervals(length, reach, first_end):
    """Cut 0..length into the finest intervals such that position p and
    position reach[p] are in one interval, and 0..first_end is in one."""
    pieces, start, cur = [], 0, first_end
    for p in range(length):
        cur = max(cur, reach[p])  # @line L9
        if cur == p:
            pieces.append((start, p + 1))  # @line L10
            start = p + 1
    return pieces


def private_chopping(txns, i, hits=None, adj=None):
    """The finest chopping of T_i when the other transactions are not chopped."""
    if hits is None:
        hits, adj = _txn_conflicts(txns)
    n, t = len(txns), txns[i]
    if not t:
        return []
    comp = _other_components(n, adj, i)
    pos = UnionFind(range(len(t)))  # @line L4
    owner = {}
    for p in range(len(t)):  # @line L5
        for j in hits[i][p]:  # @line L6
            r = comp.find(j)
            if r in owner:
                pos.union(owner[r], p)  # @line L7
            else:
                owner[r] = p
    last = {}
    for p in range(len(t)):
        last[pos.find(p)] = p
    reach = [last[pos.find(p)] for p in range(len(t))]
    rollbacks = [p for p, op in enumerate(t) if op[0] == ROLLBACK]
    first_end = rollbacks[-1] if rollbacks else 0  # @line L8
    return _intervals(len(t), reach, first_end)


def finest_chopping(txns):
    """The union of the private choppings of all transactions."""
    hits, adj = _txn_conflicts(txns)
    chop = []
    for i in range(len(txns)):  # @line L1
        chop.append(private_chopping(txns, i, hits, adj))
    return chop  # @line L11


def valid_chopping(t, pieces):
    """True when pieces are contiguous intervals that cover t in order."""
    pos = 0
    for a, b in pieces:
        if a != pos or b <= a:
            return False
        pos = b
    return pos == len(t)


def is_rollback_safe(t, pieces):
    rollbacks = [p for p, op in enumerate(t) if op[0] == ROLLBACK]
    return not rollbacks or rollbacks[-1] < pieces[0][1]


def has_sc_cycle(txns, chop):
    """An SC-cycle exists if and only if two pieces of one T_i conflict with
    the same connected component of the other transactions."""
    hits, adj = _txn_conflicts(txns)
    n = len(txns)
    for i in range(n):
        comp = _other_components(n, adj, i)
        seen = {}
        for k, (a, b) in enumerate(chop[i]):
            for p in range(a, b):
                for j in hits[i][p]:
                    r = comp.find(j)
                    if seen.setdefault(r, k) != k:
                        return True
    return False


def is_correct(txns, chop):
    """The test of the theorem: rollback-safe and no SC-cycle."""
    return (all(valid_chopping(t, c) for t, c in zip(txns, chop))
            and all(is_rollback_safe(t, c) for t, c in zip(txns, chop) if t)
            and not has_sc_cycle(txns, chop))


def parse_txn(text):
    """Parse "r(a) w(a) rollback r(b)" into a list of statements."""
    out = []
    for tok in text.split():
        if tok == ROLLBACK:
            out.append((ROLLBACK,))
        else:
            kind, item = tok[0], tok[2:-1]
            if kind not in "rw" or tok[1] != "(" or tok[-1] != ")":
                raise ValueError("bad statement %r" % tok)
            out.append((kind, item))
    return out
