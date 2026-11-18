# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-granularity-locking/. The authors are listed in prov/ZVVV9H.jsonl.

"""Multiple granularity locking with the modes IS, IX, S, SIX and X.

The items form a tree, here a database with tables and rows. A lock on a node
covers the whole subtree below it. Before a transaction locks a node, it
must hold an intention lock on the parent: IS or stronger for IS and S, and
IX or stronger for IX, SIX and X. It releases locks from the leaves up. With
strict 2PL on top, all locks are released at the end of the transaction.

The lock manager here grants a request when it is compatible with the locks
of the other transactions on the node; otherwise the request waits and is
tried again later. The page lock-table adds a FIFO queue.
"""

IS, IX, S, SIX, X = "IS", "IX", "S", "SIX", "X"
MODES = (IS, IX, S, SIX, X)

_ROWS = {
    IS: {IS: True, IX: True, S: True, SIX: True, X: False},
    IX: {IS: True, IX: True, S: False, SIX: False, X: False},
    S: {IS: True, IX: False, S: True, SIX: False, X: False},
    SIX: {IS: True, IX: False, S: False, SIX: False, X: False},
    X: {IS: False, IX: False, S: False, SIX: False, X: False},
}
COMPAT = _ROWS  # COMPAT[held][requested]

# The supremum: IS < IX, IS < S, IX < SIX, S < SIX, SIX < X.
_UP = {IS: {IS, IX, S, SIX, X}, IX: {IX, SIX, X}, S: {S, SIX, X}, SIX: {SIX, X}, X: {X}}


def sup(a, b):
    if a is None:
        return b
    if b is None:
        return a
    common = _UP[a] & _UP[b]
    return next(m for m in MODES if m in common and _UP[m] >= common)


def at_least(held, needed):
    return held is not None and held in _UP[needed]


# The parent of a node must be held in at least this mode.
PARENT_NEEDS = {IS: IS, S: IS, IX: IX, SIX: IX, X: IX}


class Hierarchy:
    """A tree given by a map from each node to its parent (None for the root)."""

    def __init__(self, parent):
        self.parent = dict(parent)
        self.children = {}
        for v, p in self.parent.items():
            if p is not None:
                self.children.setdefault(p, []).append(v)

    def path(self, v):
        """The nodes from the root down to v."""
        out = []
        while v is not None:
            out.append(v)
            v = self.parent[v]
        return out[::-1]

    def depth(self, v):
        return len(self.path(v)) - 1

    def leaves(self, v):
        kids = self.children.get(v)
        if not kids:
            return [v]
        return [leaf for k in kids for leaf in self.leaves(k)]


class MGLLockManager:
    def __init__(self, tree):
        self.tree = tree
        self.locks = {}  # node -> {txn: mode}
        self.waiting = {}  # txn -> (node, mode) it waits for

    def mode(self, txn, node):
        return self.locks.get(node, {}).get(txn)

    def lock(self, txn, node, mode):
        """Ask for mode on node. Return True if txn holds it now, False if it waits.
        Raise ValueError if txn breaks the parent rule."""
        p = self.tree.parent[node]
        if p is not None and not at_least(self.mode(txn, p), PARENT_NEEDS[mode]):  # @line L1
            raise ValueError("%r needs %s on %r before %s on %r" % (txn, PARENT_NEEDS[mode], p, mode, node))
        old = self.mode(txn, node)
        new = sup(old, mode)  # @line L2
        if new == old:
            return True
        for u, m in self.locks.get(node, {}).items():  # @line L3
            if u != txn and not COMPAT[m][new]:
                self.waiting[txn] = (node, new)  # @line L4
                return False
        self.locks.setdefault(node, {})[txn] = new  # @line L5
        self.waiting.pop(txn, None)
        return True

    def unlock(self, txn, node):
        """Release the lock of txn on node. Raise ValueError if txn still
        holds a lock on a child of node (locks go from the leaves up)."""
        for c in self.tree.children.get(node, ()):
            if self.mode(txn, c) is not None:  # @line L8
                raise ValueError("%r still holds a lock below %r" % (txn, node))
        del self.locks[node][txn]
        if not self.locks[node]:
            del self.locks[node]

    def release_all(self, txn):
        """Drop the wait of txn and release all its locks, deepest first."""
        self.waiting.pop(txn, None)
        mine = [v for v, h in self.locks.items() if txn in h]
        for v in sorted(mine, key=lambda v: (-self.tree.depth(v), repr(v))):  # @line L9
            self.unlock(txn, v)

    def covers(self, txn, leaf, kind):
        """True if the locks of txn on leaf or an ancestor allow kind (r or w) on leaf."""
        for v in self.tree.path(leaf):
            m = self.mode(txn, v)
            if m == X or (kind == "r" and m in (S, SIX)):
                return True
        return False

    def waits_for(self):
        """Edges (T, U): T waits for a mode that the lock of U on the node blocks."""
        edges = set()
        for txn, (node, mode) in self.waiting.items():
            for u, m in self.locks.get(node, {}).items():
                if u != txn and not COMPAT[m][mode]:
                    edges.add((txn, u))
        return edges


def plan(tree, txn, ops):
    """Turn operations into steps of txn: ("lock", node, mode), (kind, txn, leaf)
    for kind r or w, and a final ("c", txn, None). The operations are
    ("read", row), ("write", row), ("scan", table), ("update", table, rows)
    that reads the table and writes the given rows, and ("rewrite", table)
    that writes every row."""
    steps = []

    def path_locks(node, mode):  # @line L6
        intent = IX if mode in (IX, SIX, X) else IS
        for v in tree.path(node)[:-1]:
            steps.append(("lock", v, intent))
        steps.append(("lock", node, mode))  # @line L7

    for op in ops:
        name, node = op[0], op[1]
        if name == "read":
            path_locks(node, S)
            steps.append(("r", txn, node))
        elif name == "write":
            path_locks(node, X)
            steps.append(("w", txn, node))
        elif name == "scan":
            path_locks(node, S)
            steps.extend(("r", txn, leaf) for leaf in tree.leaves(node))
        elif name == "update":
            path_locks(node, SIX)
            steps.extend(("r", txn, leaf) for leaf in tree.leaves(node))
            for row in op[2]:
                steps.append(("lock", row, X))
                steps.append(("w", txn, row))
        elif name == "rewrite":
            path_locks(node, X)
            steps.extend(("w", txn, leaf) for leaf in tree.leaves(node))
        else:
            raise ValueError("unknown operation %r" % (name,))
    steps.append(("c", txn, None))
    return steps


def find_cycle(edges):
    """The nodes of some cycle of the directed graph, or None."""
    succ = {}
    for a, b in sorted(edges, key=repr):
        succ.setdefault(a, []).append(b)
    state = {}
    for start in sorted(succ, key=repr):
        if start in state:
            continue
        path, stack = [start], [iter(succ[start])]
        state[start] = 1
        while stack:
            for w in stack[-1]:
                if state.get(w) == 1:
                    return path[path.index(w):]
                if w not in state:
                    state[w] = 1
                    path.append(w)
                    stack.append(iter(succ.get(w, ())))
                    break
            else:
                state[path.pop()] = 2
                stack.pop()
    return None


def run(tree, plans, arrival, check=None):
    """Run the step lists of plans (txn -> steps) under strict 2PL with
    multiple granularity locks. arrival lists the transaction of each step in
    the order the steps are offered; a waiting transaction keeps its place.
    When every unfinished transaction waits, abort the largest id on a cycle
    of the wait-for graph. check(manager) runs after each step. Return the
    schedule of reads, writes, commits and aborts on the leaves."""
    mgr = MGLLockManager(tree)
    pos = {t: 0 for t in plans}
    out, pending, blocked = [], list(arrival), set()
    while pending:
        k = next((k for k, t in enumerate(pending) if t not in blocked), None)
        if k is None:
            cycle = find_cycle(mgr.waits_for())
            if cycle is None:
                raise RuntimeError("every transaction waits, but there is no cycle")
            victim = max(cycle)
            out.append(("a", victim, None))
            mgr.release_all(victim)
            pending = [t for t in pending if t != victim]
            blocked.clear()
        else:
            t = pending[k]
            step = plans[t][pos[t]]
            if step[0] == "lock":
                if not mgr.lock(t, step[1], step[2]):
                    blocked.add(t)
                    if check:
                        check(mgr)
                    continue
            elif step[0] in "rw":
                if not mgr.covers(t, step[2], step[0]):
                    raise RuntimeError("%r runs %r without a lock" % (t, step))
                out.append(step)
            else:
                out.append(step)
                mgr.release_all(t)
                blocked.clear()
            pos[t] += 1
            pending.pop(k)
        if check:
            check(mgr)
    return tuple(out)
