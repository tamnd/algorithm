# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-table/. The authors are listed in prov/J4XAN4.jsonl.

"""A lock table: a hash table from items to a granted group and a FIFO wait queue.

Each entry holds the granted group (a dict from transaction to its mode), the
group mode (the supremum of the granted modes) and a queue of waiting
requests. A request is granted at once only if it is compatible with the group
mode and nobody waits; otherwise it waits. A conversion (an upgrade of a lock
that the transaction already holds) goes ahead of all new requests in the
queue, behind earlier conversions. A release grants waiting requests from the
head of the queue for as long as they are compatible.

The modes, the compatibility matrix and the supremum are parameters, so the
same table serves S and X locks and the five modes of multiple granularity
locking. A transaction has at most one waiting request at a time.
"""

from collections import namedtuple

S, X = "S", "X"

# compatible[held][requested]
COMPAT_SX = {S: {S: True, X: False}, X: {S: False, X: False}}
SUP_SX = {(S, S): S, (S, X): X, (X, S): X, (X, X): X}

Request = namedtuple("Request", "txn mode conversion")


class Entry:
    """The lock entry of one item."""

    __slots__ = ("granted", "group", "queue")

    def __init__(self):
        self.granted = {}  # txn -> mode, in grant order
        self.group = None  # supremum of the granted modes, None if no holder
        self.queue = []  # waiting Requests, conversions first


class LockTable:
    def __init__(self, compat=COMPAT_SX, sup=SUP_SX):
        self.compat = compat
        self.sup = sup
        self.table = {}  # item -> Entry; a Python dict is a hash table
        self.waiting = {}  # txn -> item it waits on
        self.held = {}  # txn -> set of items it holds locks on

    # ----- helpers -----

    def _group_of(self, entry, without=None):
        g = None
        for t, m in entry.granted.items():
            if t != without:
                g = m if g is None else self.sup[(g, m)]
        return g

    def _ok(self, group, mode):
        return group is None or self.compat[group][mode]

    def _grant(self, entry, txn, item, mode):
        entry.granted[txn] = mode
        entry.group = self._group_of(entry)
        self.held.setdefault(txn, set()).add(item)

    # ----- operations -----

    def request(self, txn, item, mode):
        """Ask for a lock. Return True if it is granted now, False if txn waits."""
        if txn in self.waiting:
            raise ValueError("transaction %r already waits" % (txn,))
        entry = self.table.get(item)  # @line L1
        if entry is None:
            entry = self.table[item] = Entry()
        old = entry.granted.get(txn)
        if old is not None:  # @line L2
            new = self.sup[(old, mode)]
            if new == old:
                return True  # @line L3
            if self._ok(self._group_of(entry, without=txn), new):  # @line L4
                self._grant(entry, txn, item, new)
                return True
            k = 0  # @line L5
            while k < len(entry.queue) and entry.queue[k].conversion:
                k += 1
            entry.queue.insert(k, Request(txn, new, True))
            self.waiting[txn] = item
            return False
        if not entry.queue and self._ok(entry.group, mode):  # @line L6
            self._grant(entry, txn, item, mode)
            return True
        entry.queue.append(Request(txn, mode, False))  # @line L7
        self.waiting[txn] = item
        return False

    def _wake(self, item):
        """Grant requests from the head of the queue while they fit."""
        entry = self.table[item]
        grants = []
        while entry.queue:  # @line L10
            req = entry.queue[0]
            others = self._group_of(entry, without=req.txn) if req.conversion else entry.group
            if not self._ok(others, req.mode):  # @line L11
                break
            entry.queue.pop(0)  # @line L12
            self._grant(entry, req.txn, item, req.mode)
            del self.waiting[req.txn]
            grants.append((req.txn, item, req.mode))
        if not entry.granted and not entry.queue:  # @line L13
            del self.table[item]
        return grants

    def release(self, txn, item):
        """Release the lock of txn on item. Return the requests granted as a result."""
        entry = self.table.get(item)
        if entry is None or txn not in entry.granted:
            raise ValueError("%r holds no lock on %r" % (txn, item))
        del entry.granted[txn]  # @line L8
        entry.group = self._group_of(entry)  # @line L9
        self.held[txn].discard(item)
        return self._wake(item)

    def cancel(self, txn):
        """Remove the waiting request of txn, if any (used when txn aborts)."""
        item = self.waiting.pop(txn, None)
        if item is None:
            return []
        entry = self.table[item]
        entry.queue = [r for r in entry.queue if r.txn != txn]
        return self._wake(item)

    def release_all(self, txn):
        """Cancel the wait of txn and release all its locks, in sorted item order."""
        grants = self.cancel(txn)
        for item in sorted(self.held.get(txn, ()), key=repr):
            grants += self.release(txn, item)
        self.held.pop(txn, None)
        return grants

    # ----- inspection -----

    def mode(self, txn, item):
        entry = self.table.get(item)
        return None if entry is None else entry.granted.get(txn)

    def holders(self, item):
        entry = self.table.get(item)
        return {} if entry is None else dict(entry.granted)

    def queue(self, item):
        entry = self.table.get(item)
        return [] if entry is None else [(r.txn, r.mode) for r in entry.queue]

    def waits_for(self):
        """Edges (T, U): T waits for U because U holds an incompatible lock on
        the item, or U has a request ahead of T in the queue (FIFO)."""
        edges = set()
        for txn, item in sorted(self.waiting.items(), key=repr):
            entry = self.table[item]
            pos = next(k for k, r in enumerate(entry.queue) if r.txn == txn)
            mode = entry.queue[pos].mode
            for u, m in entry.granted.items():
                if u != txn and not self.compat[m][mode]:
                    edges.add((txn, u))
            for r in entry.queue[:pos]:
                if r.txn != txn:
                    edges.add((txn, r.txn))
        return edges


def find_cycle(edges):
    """Return the nodes of some cycle of the directed graph, or None."""
    succ = {}
    for a, b in sorted(edges, key=repr):
        succ.setdefault(a, []).append(b)
    color = {}
    for start in sorted(succ, key=repr):
        if start in color:
            continue
        stack = [(start, iter(succ.get(start, ())))]
        path = [start]
        color[start] = 1
        while stack:
            v, it = stack[-1]
            for w in it:
                if color.get(w) == 1:
                    return path[path.index(w):]
                if w not in color:
                    color[w] = 1
                    stack.append((w, iter(succ.get(w, ()))))
                    path.append(w)
                    break
            else:
                color[v] = 2
                stack.pop()
                path.pop()
    return None
