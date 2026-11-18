# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-range-locking/. The authors are listed in prov/VVNHG6.jsonl.

"""Next-key locking on an ordered index, with S and X locks held to the end.

A lock on a key that is in the index covers the key and the gap below it,
down to the previous key. EOF is a key above all others that covers the last
gap. A scan locks every key that it returns and the next key after the
range; a lookup that finds nothing locks the next key; an insert tests the
next key with an instant X lock; a delete keeps an X lock on the next key.
So a phantom cannot appear in a range or in a gap that a transaction read.
"""

import bisect
import math

S, X = "S", "X"
EOF = math.inf


class LockManager:
    def __init__(self):
        self.locks = {}  # key -> {txn: mode}
        self.waiting = {}  # txn -> (key, mode)

    def mode(self, txn, key):
        return self.locks.get(key, {}).get(txn)

    def try_lock(self, txn, key, mode, instant=False):
        """Grant mode on key to txn, or record a wait and return False. An
        instant lock is only tested; nothing is kept unless txn held it."""
        old = self.mode(txn, key)
        new = X if X in (old, mode) else S
        if old == new:
            return True
        for u, m in self.locks.get(key, {}).items():
            if u != txn and not (m == S and new == S):
                self.waiting[txn] = (key, new)
                return False
        if not instant:
            self.locks.setdefault(key, {})[txn] = new
        self.waiting.pop(txn, None)
        return True

    def release_all(self, txn):
        self.waiting.pop(txn, None)
        for key in [k for k, h in self.locks.items() if txn in h]:
            del self.locks[key][txn]
            if not self.locks[key]:
                del self.locks[key]

    def waits_for(self):
        edges = set()
        for txn, (key, mode) in self.waiting.items():
            for u, m in self.locks.get(key, {}).items():
                if u != txn and not (m == S and mode == S):
                    edges.add((txn, u))
        return edges


class KeyRangeIndex:
    """An ordered set of keys with next-key locking. With naive=True, it
    locks only the keys that exist and that the operation touches, which
    lets phantoms through."""

    def __init__(self, keys, naive=False):
        self.keys = sorted(keys)
        self.naive = naive
        self.lm = LockManager()
        self.undo = {}  # txn -> list of (op, key) to undo on abort

    def present(self, k):
        i = bisect.bisect_left(self.keys, k)
        return i < len(self.keys) and self.keys[i] == k

    def next_key(self, k):
        i = bisect.bisect_right(self.keys, k)  # @line L1
        return self.keys[i] if i < len(self.keys) else EOF

    def needs(self, op):
        """The locks (key, mode, instant) that op needs now."""
        name, k = op[0], op[1]
        if name == "scan":
            lo, hi = k, op[2]
            out = [(v, S, False) for v in self.keys if lo <= v <= hi]
            if not self.naive:
                out.append((self.next_key(hi), S, False))  # @line L2
            return out
        if name == "fetch":
            if self.present(k):
                return [(k, S, False)]
            return [] if self.naive else [(self.next_key(k), S, False)]  # @line L4
        if name == "insert":
            if self.present(k):
                return [(k, S, False)]  # @line L5
            nxt = [] if self.naive else [(self.next_key(k), X, True)]  # @line L6
            return nxt + [(k, X, False)]  # @line L7
        if name == "delete":
            if not self.present(k):
                return [] if self.naive else [(self.next_key(k), S, False)]  # @line L8
            return [(k, X, False)] + ([] if self.naive else [(self.next_key(k), X, False)])  # @line L9
        raise ValueError("unknown operation %r" % (name,))

    def execute(self, txn, op):
        """Run op, whose locks are held. Return (result, slot accesses)."""
        name, k = op[0], op[1]
        if name == "scan":
            lo, hi = k, op[2]
            found = tuple(v for v in self.keys if lo <= v <= hi)  # @line L3
            return found, [("r", v) for v in range(lo, hi + 1)]
        if name == "fetch":
            return self.present(k), [("r", k)]
        if name == "insert":
            if self.present(k):
                return False, [("r", k)]
            bisect.insort(self.keys, k)
            self.undo.setdefault(txn, []).append(("insert", k))
            return True, [("w", k)]
        if not self.present(k):
            return False, [("r", k)]
        self.keys.remove(k)
        self.undo.setdefault(txn, []).append(("delete", k))
        return True, [("w", k)]

    def attempt(self, txn, op):
        """Ask for the locks that op needs now, in order. If one must wait,
        return None; the caller tries again later, and the locks are then
        computed again. Otherwise run op."""
        for key, mode, instant in self.needs(op):
            if not self.lm.try_lock(txn, key, mode, instant):
                return None
        return self.execute(txn, op)

    def end(self, txn, commit):
        """Commit, or abort and undo the changes of txn, then release its locks."""
        for name, k in reversed(self.undo.pop(txn, [])):
            if not commit:  # @line L10
                if name == "insert":
                    self.keys.remove(k)
                else:
                    bisect.insort(self.keys, k)
        self.lm.release_all(txn)


def find_cycle(edges):
    """The nodes of some cycle of the directed graph, or None."""
    succ = {}
    for a, b in sorted(edges):
        succ.setdefault(a, []).append(b)
    state = {}
    for start in sorted(succ):
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


def slot(k):
    return "EOF" if k == EOF else "k%d" % k


def run(keys, programs, arrival, naive=False, check=None):
    """Run programs (txn -> list of operations) on an index with the given
    keys. arrival lists the transaction of each step (each operation, and
    the commit at the end) in the order the steps are offered; a waiting
    transaction keeps its place. When every unfinished transaction waits,
    abort the largest id on a cycle of the wait-for graph. check(index,
    touched) runs after each step. Return the results of each committed
    transaction, the schedule on the key slots, and the final keys."""
    idx = KeyRangeIndex(keys, naive)
    pos = {t: 0 for t in programs}
    results = {t: [] for t in programs}
    touched = {t: {} for t in programs}  # txn -> {key: "r" or "w"}
    out, pending, blocked = [], list(arrival), set()
    while pending:
        k = next((k for k, t in enumerate(pending) if t not in blocked), None)
        if k is None:
            cycle = find_cycle(idx.lm.waits_for())
            if cycle is None:
                raise RuntimeError("every transaction waits, but there is no cycle")
            victim = max(cycle)
            idx.end(victim, commit=False)
            out.append(("a", victim, None))
            results.pop(victim)
            touched[victim] = {}
            pending = [t for t in pending if t != victim]
            blocked.clear()
        else:
            t = pending[k]
            if pos[t] == len(programs[t]):
                idx.end(t, commit=True)
                out.append(("c", t, None))
                touched[t] = {}
            else:
                got = idx.attempt(t, programs[t][pos[t]])
                if got is None:
                    blocked.add(t)
                    continue
                result, acts = got
                results[t].append(result)
                for kind, v in acts:
                    out.append((kind, t, slot(v)))
                    if touched[t].get(v) != "w":
                        touched[t][v] = kind
            blocked.clear()
            pos[t] += 1
            pending.pop(k)
        if check:
            check(idx, touched)
    return results, tuple(out), tuple(idx.keys)


def serial_results(keys, programs, order):
    """Run the programs one after the other on a plain sorted list."""
    cur = sorted(keys)
    results = {}
    for t in order:
        res = []
        for op in programs[t]:
            name, k = op[0], op[1]
            if name == "scan":
                res.append(tuple(v for v in cur if k <= v <= op[2]))
            elif name == "fetch":
                res.append(k in cur)
            elif name == "insert":
                res.append(k not in cur)
                if k not in cur:
                    bisect.insort(cur, k)
            else:
                res.append(k in cur)
                if k in cur:
                    cur.remove(k)
        results[t] = res
    return results, tuple(cur)
