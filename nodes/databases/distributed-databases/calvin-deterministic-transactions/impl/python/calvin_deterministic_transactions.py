# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calvin-deterministic-transactions/. The authors are listed in prov/AX20CH.jsonl.
"""A toy model of Calvin (Thomson et al., SIGMOD 2012) in one thread.

This is not a database. It keeps only the parts of Calvin that make the
protocol correct: sequencers that cut the input into epochs, a global order
of the batches, a scheduler per partition that requests all locks of each
transaction in that order and grants them in request order, and the five
phases of execution, in which partitions send their local reads to the
active participants and every active participant runs the same logic.

Each replica holds every partition. The input log is the same for all
replicas; in Calvin, Paxos agrees on each batch, and here the batch is given
to everyone. Messages between nodes are delivered in an order chosen by a
seeded random.Random. A whole replica can crash and later rebuild its state
by replaying the input log.

A transaction declares its read set and write set, and its logic is a
function of the values it reads. The logic returns a dict of writes, None
for a deterministic abort, or RESTART when an OLLP prediction of the read
and write sets was wrong.
"""

RESTART = "restart"


class Txn:
    def __init__(self, tid, reads, writes, logic):
        self.tid = tid
        self.reads = frozenset(reads)
        self.writes = frozenset(writes)
        self.logic = logic


def run_logic(t, vals):
    out = t.logic(dict(vals))
    if isinstance(out, dict):
        assert set(out) <= t.writes, (t.tid, out)
        return "commit", out
    return ("abort" if out is None else RESTART), {}


class Scheduler:
    """The scheduler, lock manager and workers of one partition of one replica."""

    def __init__(self, db, replica, part, store):
        self.db, self.r, self.q = db, replica, part
        self.store = dict(store)
        self.batches = {}            # (epoch, sequencer) -> transactions that touch this partition
        self.next_epoch = 0
        self.locks = {}              # key -> [(tid, mode)] in request order
        self.txn = {}                # tid -> (txn, local keys)
        self.order = []              # tids in global order
        self.started = set()
        self.reads = {}              # tid -> ({key: value}, set of partitions that sent)
        self.finished = set()
        self.results = {}            # tid -> (outcome, values read), at active participants
        self.down = False

    # ------------------------------------------------------- lock thread
    def on_batch(self, e, p, txns):
        self.batches[(e, p)] = txns
        n = self.db.nparts
        while all((self.next_epoch, s) in self.batches for s in range(n)):     # @line L3
            for s in range(n):
                for t in self.batches.pop((self.next_epoch, s)):
                    self.lock_all(t)
            self.next_epoch += 1
        self.work()

    def lock_all(self, t):
        keys = sorted(k for k in t.reads | t.writes if self.db.place[k] == self.q)
        self.txn[t.tid] = (t, keys)
        self.order.append(t.tid)
        for k in keys:                                                        # @line L4
            self.locks.setdefault(k, []).append((t.tid, "X" if k in t.writes else "S"))

    def granted(self, tid, k):
        queue = self.locks[k]
        mine = next(m for o, m in queue if o == tid)
        for other, mode in queue:                                             # @line L5
            if other == tid:
                return True
            if mode == "X" or mine == "X":
                return False

    def release(self, tid):
        _, keys = self.txn[tid]
        for k in keys:
            self.locks[k] = [e for e in self.locks[k] if e[0] != tid]
        self.finished.add(tid)

    # ----------------------------------------------------------- workers
    def work(self):
        changed = True
        while changed:
            changed = False
            for tid in self.order:
                if tid in self.finished:
                    continue
                t, keys = self.txn[tid]
                if tid not in self.started and all(self.granted(tid, k) for k in keys):
                    self.start(t, keys)
                    changed = True
                elif tid in self.started and self.q in self.db.active(t):
                    vals, senders = self.reads.get(tid, ({}, set()))
                    if senders >= self.db.read_parts(t):                      # @line L9
                        self.finish(t, vals)
                        changed = True

    def start(self, t, keys):
        self.started.add(t.tid)
        if self.q in self.db.read_parts(t):
            vals = {k: self.store[k] for k in keys if k in t.reads}           # @line L6
            for a in sorted(self.db.active(t)):                               # @line L7
                if a == self.q:
                    self.on_reads(t.tid, self.q, vals)
                else:
                    self.db.send((self.r, a), ("reads", t.tid, self.q, vals), True)
        if self.q not in self.db.active(t):                                   # @line L8
            self.release(t.tid)

    def on_reads(self, tid, sender, vals):
        got, senders = self.reads.setdefault(tid, ({}, set()))
        got.update(vals)
        senders.add(sender)

    def finish(self, t, vals):
        outcome, writes = run_logic(t, vals)                                  # @line L10
        for k, v in writes.items():                                           # @line L11
            if self.db.place[k] == self.q:
                self.store[k] = v
        self.results[t.tid] = (outcome, dict(vals))
        self.release(t.tid)
        if outcome == RESTART and self.r == 0 and self.q == min(self.db.active(t)):
            self.db.restart(t.tid)


class Calvin:
    def __init__(self, place, replicas=2, init=None):
        """place: {key: partition number}. init: {key: value}, default 0."""
        self.place = dict(place)
        self.nparts = max(place.values()) + 1
        self.replicas = replicas
        self.init = {k: 0 for k in place}
        self.init.update(init or {})
        self.sched = {(r, q): self.new_scheduler(r, q) for r in range(replicas) for q in range(self.nparts)}
        self.net = []
        self.read_messages = 0       # messages of phase 3, between partitions
        self.batch_messages = 0      # messages from sequencers to schedulers
        self.log = {}                # (epoch, sequencer) -> the agreed batch
        self.pending = {}            # sequencer -> requests of the open epoch
        self.epoch = 0
        self.recon = {}              # tid -> function(read) -> new Txn, for OLLP
        self.next_tid = 1000

    def new_scheduler(self, r, q):
        return Scheduler(self, r, q, {k: v for k, v in self.init.items() if self.place[k] == q})

    def parts(self, t):
        return {self.place[k] for k in t.reads | t.writes}

    def read_parts(self, t):
        return {self.place[k] for k in t.reads}

    def active(self, t):
        return {self.place[k] for k in (t.writes or t.reads)}

    def send(self, dst, payload, read=False):
        if read:
            self.read_messages += 1
        else:
            self.batch_messages += 1
        self.net.append((dst, payload))

    # --------------------------------------------------------- sequencers
    def submit(self, p, t):
        self.pending.setdefault(p, []).append(t)                              # @line L1

    def end_epoch(self):
        e = self.epoch
        for p in range(self.nparts):
            batch = self.pending.pop(p, [])
            self.log[(e, p)] = batch                                          # @line L2
            for (r, q) in sorted(self.sched):
                self.send((r, q), ("batch", e, p, [t for t in batch if q in self.parts(t)]))
        self.epoch += 1

    def global_order(self):
        return [t for key in sorted(self.log) for t in self.log[key]]

    # --------------------------------------------------------------- OLLP
    def read_no_lock(self, k):
        """A reconnaissance read: no locks, from replica 0."""
        return self.sched[(0, self.place[k])].store[k]

    def restart(self, tid):
        make = self.recon[tid]
        self.next_tid += 1
        t = make(self.next_tid, self.read_no_lock)
        self.recon[t.tid] = make
        self.submit(0, t)

    # ------------------------------------------------------------ network
    def deliver(self, k):
        dst, payload = self.net.pop(k)
        s = self.sched[dst]
        if s.down:
            return
        if payload[0] == "batch":
            s.on_batch(*payload[1:])
        else:
            _, tid, sender, vals = payload
            s.on_reads(tid, sender, vals)
            s.work()

    def crash(self, r):
        for q in range(self.nparts):
            self.sched[(r, q)].down = True

    def recover(self, r):
        """Rebuild replica r from the initial state by replaying the input log."""
        self.net = [m for m in self.net if m[0][0] != r]
        for q in range(self.nparts):
            self.sched[(r, q)] = self.new_scheduler(r, q)
        for (e, p) in sorted(self.log):
            for q in range(self.nparts):
                self.send((r, q), ("batch", e, p, [t for t in self.log[(e, p)] if q in self.parts(t)]))

    def drain(self, rng):
        while self.net:
            self.deliver(rng.randrange(len(self.net)))

    def run(self, rng, requests, per_epoch=8, crash=None):
        """requests: [(epoch, sequencer, txn)]. crash: (epoch, replica) or None.
        Each epoch delivers up to per_epoch messages, then closes."""
        by_epoch = {}
        for e, p, t in requests:
            by_epoch.setdefault(e, []).append((p, t))
        last = max(by_epoch, default=0)
        while True:
            if self.epoch <= last or any(self.pending.values()):
                if crash and crash[0] == self.epoch:
                    self.crash(crash[1])
                for p, t in by_epoch.get(self.epoch, []):
                    self.submit(p, t)
                for _ in range(per_epoch):
                    if self.net:
                        self.deliver(rng.randrange(len(self.net)))
                self.end_epoch()
            elif self.net:
                self.deliver(rng.randrange(len(self.net)))
            else:
                return

    def state(self, r):
        out = {}
        for q in range(self.nparts):
            out.update(self.sched[(r, q)].store)
        return out

    def results(self, r):
        out = {}
        for q in range(self.nparts):
            out.update(self.sched[(r, q)].results)
        return out


def serial(init, order):
    """The brute force oracle: run the transactions one at a time in order."""
    db = dict(init)
    results = {}
    for t in order:
        vals = {k: db[k] for k in t.reads}
        outcome, writes = run_logic(t, vals)
        db.update(writes)
        results[t.tid] = (outcome, vals)
    return db, results
