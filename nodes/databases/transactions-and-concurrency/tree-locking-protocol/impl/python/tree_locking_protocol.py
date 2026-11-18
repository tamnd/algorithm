# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-locking-protocol/. The authors are listed in prov/AV253P.jsonl.

"""The tree locking protocol of Silberschatz and Kedem, with exclusive locks.

The items are the nodes of a rooted tree. A transaction may lock any node
first. After that, it may lock a node only while it holds the parent of the
node. It may unlock a node at any time, but it may not lock a node again
after it unlocked it. It reads or writes a node only while it holds the lock
on the node. These rules make every schedule conflict serializable and free
of deadlocks, although the locking is not two-phase.
"""


class TreeLockManager:
    def __init__(self, parent):
        self.parent = dict(parent)  # node -> parent, None for the root
        self.holder = {}  # node -> txn that holds the lock
        self.locked = {}  # txn -> the nodes it has locked so far
        self.waiting = {}  # txn -> the node it waits for

    def lock(self, txn, node):
        """Ask for the lock on node. Return True if txn holds it now and
        False if it waits. Raise ValueError if the request breaks a rule."""
        done = self.locked.get(txn, set())
        if node in done:  # @line L1
            raise ValueError("%r may not lock %r again" % (txn, node))
        p = self.parent[node]
        if done and (p is None or self.holder.get(p) != txn):  # @line L2
            raise ValueError("%r must hold the parent of %r" % (txn, node))
        if node in self.holder:  # @line L3
            self.waiting[txn] = node
            return False
        self.holder[node] = txn  # @line L4
        self.locked.setdefault(txn, set()).add(node)
        self.waiting.pop(txn, None)
        return True

    def unlock(self, txn, node):
        if self.holder.get(node) != txn:  # @line L5
            raise ValueError("%r does not hold %r" % (txn, node))
        del self.holder[node]

    def held(self, txn):
        return {v for v, t in self.holder.items() if t == txn}

    def waits_for(self):
        """Edges (T, U): T waits for a node that U holds."""
        return {(t, self.holder[x]) for t, x in self.waiting.items() if x in self.holder}


def path(parent, v):
    """The nodes from the root down to v."""
    out = []
    while v is not None:
        out.append(v)
        v = parent[v]
    return out[::-1]


def lowest_common_ancestor(parent, nodes):
    paths = [path(parent, v) for v in nodes]
    k = 0
    while all(len(p) > k for p in paths) and len({p[k] for p in paths}) == 1:
        k += 1
    return paths[0][k - 1]


def plan(parent, txn, accesses):
    """Turn the accesses [(kind, node), ...] of txn, kind r or w, into steps
    ("lock", node), ("unlock", node), (kind, txn, node) and a final
    ("c", txn, None) that follow the protocol. The first lock is on the
    lowest common ancestor of the accessed nodes. Paths are locked top down
    just before they are needed, and a node is unlocked as soon as it has no
    later access and no child that is still to be locked."""
    top = lowest_common_ancestor(parent, [v for _, v in accesses])  # @line L6
    need = set()
    for _, v in accesses:
        p = path(parent, v)
        need.update(p[p.index(top):])
    children = {v: [c for c in need if parent[c] == v] for v in need}
    steps, held, locked = [], set(), set()

    def release_free(k):  # the accesses from index k on are still to come
        future = {v for _, v in accesses[k:]}
        for v in sorted(held, key=repr):
            if v not in future and all(c in locked for c in children[v]):  # @line L8
                steps.append(("unlock", v))
                held.discard(v)

    for k, (kind, v) in enumerate(accesses):
        p = path(parent, v)
        for u in p[p.index(top):]:
            if u not in locked:
                steps.append(("lock", u))  # @line L7
                locked.add(u)
                held.add(u)
                release_free(k)
        steps.append((kind, txn, v))
        release_free(k + 1)
    assert not held
    steps.append(("c", txn, None))
    return steps


def run(parent, plans, arrival, check=None):
    """Run the step lists of plans (txn -> steps). arrival lists the
    transaction of each step in the order the steps are offered; a waiting
    transaction keeps its place. check(manager) runs after each step. Return
    the schedule of reads, writes and commits, and the log of lock and unlock
    events. Raise RuntimeError if every transaction waits."""
    mgr = TreeLockManager(parent)
    pos = {t: 0 for t in plans}
    out, log, pending, blocked = [], [], list(arrival), set()
    while pending:
        k = next((k for k, t in enumerate(pending) if t not in blocked), None)
        if k is None:
            raise RuntimeError("deadlock: %r" % sorted(mgr.waits_for()))
        t = pending[k]
        step = plans[t][pos[t]]
        if step[0] == "lock":
            if not mgr.lock(t, step[1]):
                blocked.add(t)
                continue
            log.append(("lock", t, step[1]))
        elif step[0] == "unlock":
            mgr.unlock(t, step[1])
            log.append(("unlock", t, step[1]))
            blocked.clear()
        elif step[0] in "rw":
            if mgr.holder.get(step[2]) != t:
                raise RuntimeError("%r runs %r without the lock" % (t, step))
            out.append(step)
        else:
            out.append(step)
        pos[t] += 1
        pending.pop(k)
        if check:
            check(mgr)
    return tuple(out), log
