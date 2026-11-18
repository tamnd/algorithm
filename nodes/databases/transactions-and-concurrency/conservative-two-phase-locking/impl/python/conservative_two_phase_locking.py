# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-two-phase-locking/. The authors are listed in prov/CS6AB2.jsonl.

"""Conservative (static) two-phase locking.

A transaction declares its read set and write set when it begins. The
scheduler grants all its locks at once, or none: X on each item it writes and
S on each item it only reads. A transaction that cannot get all its locks
waits in a FIFO list and holds nothing. A waiting transaction is admitted
when its locks are compatible with the locks held by others and with the
locks wanted by every earlier waiter, so it never passes an earlier waiter
that it conflicts with.

With strict=True every lock is held to the end of the transaction. With
strict=False a lock is released after the last access of the transaction to
the item; the transaction is still two-phase, because it took all its locks
before its first action.

Actions are tuples (kind, txn, item) with kind in "r", "w", "c", "a", as in
the helper dbsched.
"""

S, X = "S", "X"


def conflict(a, b):
    """Two lock modes of different transactions conflict unless both are S."""
    return a == X or b == X


def lock_set(program):
    """The locks a program needs: X on each written item, S on each item it only reads."""
    need = {}
    for kind, _, item in program:
        if kind == "w":
            need[item] = X
        elif kind == "r":
            need.setdefault(item, S)
    return need


class ConservativeScheduler:
    def __init__(self, strict=True):
        self.strict = strict
        self.locks = {}  # item -> {txn: mode}
        self.wait = []  # waiting txns, in order of arrival
        self.need = {}  # txn -> {item: mode}, the declared lock set
        self.left = {}  # txn -> {item: accesses still to come}
        self.held = {}  # txn -> set of items it holds
        self.lock_points = []  # txns in the order of their lock points

    def begin(self, txn, program):
        """Declare the program of txn and ask for all its locks.
        Return True if txn holds them now, False if it waits."""
        self.need[txn] = lock_set(program)  # @line L1
        self.left[txn] = {}
        for kind, _, item in program:
            if kind in "rw":
                self.left[txn][item] = self.left[txn].get(item, 0) + 1
        self.wait.append(txn)  # @line L2
        self._admit()  # @line L3
        return txn not in self.wait

    def _fits(self, txn, wanted):
        for item, mode in self.need[txn].items():
            for u, m in self.locks.get(item, {}).items():
                if u != txn and conflict(m, mode):
                    return False
            if item in wanted and conflict(wanted[item], mode):
                return False
        return True

    def _admit(self):
        """Admit waiting transactions in order of arrival while they fit."""
        admitted = []
        wanted = {}  # item -> strongest mode wanted by an earlier waiter
        for txn in list(self.wait):  # @line L4
            if self._fits(txn, wanted):  # @line L5
                self.wait.remove(txn)  # @line L6
                for item, mode in self.need[txn].items():
                    self.locks.setdefault(item, {})[txn] = mode
                self.held[txn] = set(self.need[txn])
                self.lock_points.append(txn)
                admitted.append(txn)
            else:
                for item, mode in self.need[txn].items():
                    if wanted.get(item) != X:
                        wanted[item] = mode
        return admitted

    def _release(self, txn, item):
        del self.locks[item][txn]
        if not self.locks[item]:
            del self.locks[item]
        self.held[txn].discard(item)

    def access(self, txn, kind, item):
        """Run r or w of txn on item. Return the transactions admitted as a result."""
        mode = self.locks.get(item, {}).get(txn)
        if mode is None or (kind == "w" and mode != X):  # @line L7
            raise ValueError("%r has no %s lock on %r" % (txn, kind, item))
        self.left[txn][item] -= 1
        if not self.strict and self.left[txn][item] == 0:  # @line L8
            self._release(txn, item)
            return self._admit()
        return []

    def end(self, txn):
        """Commit or abort txn: release all its locks. Return the admitted transactions."""
        for item in sorted(self.held.get(txn, ()), key=repr):  # @line L9
            self._release(txn, item)
        self.held.pop(txn, None)
        self.need.pop(txn, None)
        self.left.pop(txn, None)
        return self._admit()

    def waits_for(self):
        """Edges (T, U): T waits and U holds a conflicting lock, or U is an
        earlier waiter that wants a conflicting lock."""
        edges = set()
        for k, txn in enumerate(self.wait):
            for item, mode in self.need[txn].items():
                for u, m in self.locks.get(item, {}).items():
                    if conflict(m, mode):
                        edges.add((txn, u))
                for u in self.wait[:k]:
                    m = self.need[u].get(item)
                    if m is not None and conflict(m, mode):
                        edges.add((txn, u))
        return edges


def run(programs, arrival, strict=True, check=None):
    """Run the programs (sequences of actions, one transaction each) under
    conservative 2PL. arrival lists the transaction of each action in the
    order the actions are offered; a waiting transaction keeps its place and
    the first transaction that does not wait goes next. check(scheduler) is
    called after each step. Return the output schedule and the order of the
    lock points."""
    progs = {p[0][1]: tuple(p) for p in programs}
    sched = ConservativeScheduler(strict)
    pos = {t: 0 for t in progs}
    out, pending = [], list(arrival)
    while pending:
        k = next((k for k, t in enumerate(pending) if t not in sched.wait), None)
        if k is None:
            raise RuntimeError("every transaction waits")
        t = pending[k]
        if pos[t] == 0 and t not in sched.held:
            if not sched.begin(t, progs[t]):
                if check:
                    check(sched)
                continue
        act = progs[t][pos[t]]
        if act[0] in "rw":
            sched.access(t, act[0], act[2])
        else:
            sched.end(t)
        out.append(act)
        pos[t] += 1
        pending.pop(k)
        if check:
            check(sched)
    return tuple(out), tuple(sched.lock_points)
