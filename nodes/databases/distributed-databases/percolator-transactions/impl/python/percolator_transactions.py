# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percolator-transactions/. The authors are listed in prov/FVBYZN.jsonl.
"""A toy model of Percolator transactions (Peng and Dabek, OSDI 2010).

This is not Percolator. There is no Bigtable, no network and no observer
framework. A dict of cells stands for the table, and each method of the
class Table that changes cells is one atomic step, as a Bigtable row
transaction is. A counter stands for the timestamp oracle.

Each cell x has the three columns of the paper:
    data[x]   start_ts  -> value
    lock[x]   start_ts  -> the key of the primary cell
    write[x]  commit_ts -> start_ts (a pointer to the data)

Clients run as Python generators. Each next() does one row transaction or
one call to the oracle, and the scheduler picks the next client with a
seeded random.Random. A client can crash between any two steps. A reader
that finds the lock of a client that seems dead cleans it up through the
primary lock, as in the paper. A reader can also suspect live clients with
some probability, to show that cleanup is safe even when it is wrong.
"""


class Cell:
    def __init__(self):
        self.data = {}
        self.lock = {}
        self.write = {}


class Txn:
    def __init__(self, tid, read_keys, logic):
        """logic(reads) -> {key: value}, the writes, computed from the reads."""
        self.tid = tid
        self.read_keys = list(read_keys)
        self.logic = logic
        self.start = None
        self.commit = None
        self.reads = {}
        self.writes = {}
        self.status = "new"      # new, reading, prewriting, committed, done, aborted
        self.abort_reason = None


class Table:
    def __init__(self, init, rng, suspect=0.0):
        """init: {key: value}, written by a loader transaction with tid 0."""
        self.cells = {k: Cell() for k in init}
        self.rng = rng
        self.suspect = suspect
        self.ts = 0
        self.owner = {}          # start_ts -> Txn
        self.crashed = set()
        self.rolled_forward = 0
        self.rolled_back = 0
        loader = Txn(0, [], None)
        loader.start, loader.commit = self.timestamp(), self.timestamp()
        loader.writes = dict(init)
        loader.status = "done"
        for k, v in init.items():
            self.cells[k].data[loader.start] = v
            self.cells[k].write[loader.commit] = loader.start
        self.loader = loader
        self.rpcs = 0

    def timestamp(self):
        """The timestamp oracle: strictly increasing."""
        self.rpcs = getattr(self, "rpcs", 0) + 1
        self.ts += 1
        return self.ts

    # ------------------------------------------------------------ reads
    def get(self, t, x):
        """One row transaction. Returns (True, value), or (False, None) if the
        reader must wait and try again."""
        self.rpcs += 1
        c = self.cells[x]
        locks = [s for s in c.lock if s <= t.start]
        if locks:                                                       # @line L8
            s = min(locks)
            if self.owner[s].tid in self.crashed or self.rng.random() < self.suspect:
                self.cleanup(x, s)
            return False, None
        latest = max(ct for ct in c.write if ct <= t.start)             # @line L9
        return True, c.data[c.write[latest]]

    def cleanup(self, x, s):
        """Percolator does this with a row transaction on the primary and
        then one on x. The toy does both in one step. That is safe: after
        a roll back the owner can no longer commit, and a roll forward
        writes the same record that the owner would write."""
        self.rpcs += 2
        p = self.cells[x].lock[s]
        pc = self.cells[p]
        done = [ct for ct, st in pc.write.items() if st == s]
        if done:                                                        # @line L12
            self.cells[x].write[done[0]] = s           # roll forward
            del self.cells[x].lock[s]
            self.rolled_forward += 1
        else:
            pc.lock.pop(s, None)                       # roll back, primary first
            pc.data.pop(s, None)
            self.cells[x].lock.pop(s, None)
            self.cells[x].data.pop(s, None)
            self.rolled_back += 1

    # ----------------------------------------------------------- writes
    def prewrite(self, t, x, primary):
        self.rpcs += 1
        c = self.cells[x]
        if any(ct >= t.start for ct in c.write) or c.lock:              # @line L10
            return False
        c.data[t.start] = t.writes[x]                                   # @line L11
        c.lock[t.start] = primary
        return True

    def commit_primary(self, t, p):
        """The commit point."""
        self.rpcs += 1
        c = self.cells[p]
        if t.start not in c.lock:                                       # @line L6
            return False
        c.write[t.commit] = t.start
        del c.lock[t.start]
        return True

    def commit_secondary(self, t, x):
        self.rpcs += 1
        c = self.cells[x]
        c.write[t.commit] = t.start                                     # @line L7
        c.lock.pop(t.start, None)

    def rollback(self, t, keys):
        """The client erases its own locks after an abort, primary first."""
        for x in keys:
            self.rpcs += 1
            self.cells[x].lock.pop(t.start, None)
            self.cells[x].data.pop(t.start, None)

    def is_committed(self, t):
        """A writer is committed if its primary has its write record."""
        if not t.writes:
            return t.status == "done"
        return t.start in self.cells[min(t.writes)].write.values()

    # ----------------------------------------------------------- client
    def steps(self, t):
        t.start = self.timestamp()                                      # @line L1
        self.owner[t.start] = t
        t.status = "reading"
        yield
        for x in t.read_keys:                                           # @line L2
            while True:
                ok, v = self.get(t, x)
                yield
                if ok:
                    t.reads[x] = v
                    break
        t.writes = t.logic(dict(t.reads)) if t.logic else {}
        if not t.writes:
            t.status = "done"
            return
        keys = sorted(t.writes)                                         # @line L3
        primary = keys[0]
        t.status = "prewriting"
        for i, x in enumerate(keys):                                    # @line L4
            if not self.prewrite(t, x, primary):
                self.rollback(t, keys[:i])
                t.status, t.abort_reason = "aborted", "conflict"
                return
            yield
        t.commit = self.timestamp()                                     # @line L5
        yield
        if not self.commit_primary(t, primary):
            self.rollback(t, keys)
            t.status, t.abort_reason = "aborted", "cleaned up"
            return
        t.status = "committed"
        yield
        for x in keys[1:]:
            self.commit_secondary(t, x)
            yield
        t.status = "done"

    def run(self, rng, txns, crash=None, limit=100000):
        """crash: None, (step, tid), or ("commit point", tid) for a crash just
        after the client has committed its primary. Runs until every client
        that did not crash has finished, and returns the number of steps."""
        gens = {t.tid: self.steps(t) for t in txns}
        by_tid = {t.tid: t for t in txns}
        step = 0
        while gens:
            if crash and step == crash[0] and crash[1] in gens:
                del gens[crash[1]]
                self.crashed.add(crash[1])
                if not gens:
                    break
            tid = rng.choice(sorted(gens))
            try:
                next(gens[tid])
                if crash and crash == ("commit point", tid) and by_tid[tid].status == "committed":
                    del gens[tid]
                    self.crashed.add(tid)
            except StopIteration:
                del gens[tid]
            step += 1
            assert step < limit, "no progress"
        return step

    def snapshot(self, rng):
        """A final read-only transaction over every key. It also cleans up
        the locks that crashed clients left behind."""
        t = Txn(-1, sorted(self.cells), None)
        self.run(rng, [t])
        return t.reads
