# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/silo-concurrency-control/. The authors are listed in prov/023YX3.jsonl.
"""A toy model of the Silo commit protocol (Tu, Zheng, Kohler, Liskov and
Madden, SOSP 2013).

This is not Silo. It runs in one thread, and a seeded scheduler interleaves
the steps of several simulated workers and of the thread that advances the
global epoch. Each step is atomic, so there are no memory fences, no
cache lines and no spinning. There are no inserts, deletes, range scans,
node sets, snapshot transactions, garbage collection or logging. What it
keeps is the order of the commit protocol: lock the write set in a global
order, read the epoch (the serialization point), validate the read set,
choose the TID, install and unlock.

A TID is a pair (epoch, sequence), compared as a tuple; the real system
packs the epoch into the high bits of a 64-bit word.
"""


class Record:
    __slots__ = ("value", "tid", "owner")

    def __init__(self, value):
        self.value = value
        self.tid = (0, 0)
        self.owner = None  # the transaction that holds the lock bit


class Txn:
    def __init__(self, tid_name, worker, program, program_id=None):
        self.name = tid_name      # an int, unique for each attempt
        self.worker = worker
        self.program = list(program)
        self.program_id = program_id
        self.pc = 0
        self.reads = {}           # item -> TID seen at the first read
        self.seen = []            # the values returned by reads, in order
        self.writes = {}          # item -> new value
        self.phase = "exec"
        self.locked = []
        self.to_lock = []
        self.to_check = []
        self.to_install = []
        self.epoch = None
        self.tid = None


class Silo:
    def __init__(self, items, initial=0, validate=True):
        self.db = {x: Record(initial) for x in items}
        self.E = 1
        self.last = {}            # worker -> its most recent TID
        self.log = []             # actions for dbsched, in the order they happen
        self.sp = []              # names of transactions, in the order of their serialization points
        self.committed = {}       # name -> Txn
        self.check = validate     # False gives the broken variant without Phase 2

    # ------------------------------------------------------------ execution

    def read(self, t, x):
        if x in t.writes:
            return t.writes[x]  # @line L1
        rec = self.db[x]
        t.reads.setdefault(x, rec.tid)  # @line L2
        self.log.append(("r", t.name, x))
        return rec.value

    def write(self, t, x, v):
        t.writes[x] = v  # @line L3

    def exec_step(self, t):
        """Run the next statement of the program. A write stores a value that
        depends on every value the transaction has read so far."""
        kind, x = t.program[t.pc]
        if kind == "r":
            t.seen.append(self.read(t, x))
        else:
            self.write(t, x, (t.program_id, x, tuple(t.seen)))
        t.pc += 1
        if t.pc == len(t.program):
            t.phase = "lock"
            t.to_lock = sorted(t.writes)

    # --------------------------------------------------------------- commit

    def lock_step(self, t):
        """Phase 1: lock the next record of the write set in sorted order.
        Return False if another transaction holds it (the worker waits)."""
        if t.to_lock:
            x = t.to_lock[0]
            rec = self.db[x]
            if rec.owner is not None:
                return False
            rec.owner = t.name  # @line L4
            t.locked.append(x)
            t.to_lock.pop(0)
        if not t.to_lock:
            t.phase = "epoch"
        return True

    def epoch_step(self, t):
        t.epoch = self.E  # @line L5
        self.sp.append(t.name)
        t.phase = "validate"
        t.to_check = sorted(t.reads) if self.check else []

    def validate_step(self, t):
        """Phase 2: check one record of the read set. Return False on abort."""
        if t.to_check:
            x = t.to_check.pop(0)  # @line L6
            rec = self.db[x]
            if rec.tid != t.reads[x] or (rec.owner is not None and rec.owner != t.name):
                self.abort(t)  # @line L7
                return False
        if not t.to_check:
            t.phase = "tid"
        return True

    def tid_step(self, t):
        bound = max([t.reads[x] for x in t.reads]
                    + [self.db[x].tid for x in t.writes]
                    + [self.last.get(t.worker, (0, 0))])
        assert bound[0] <= t.epoch
        t.tid = (t.epoch, bound[1] + 1) if bound[0] == t.epoch else (t.epoch, 0)  # @line L8
        self.last[t.worker] = t.tid  # @line L9
        t.phase = "install"
        t.to_install = sorted(t.writes)

    def install_step(self, t):
        """Phase 3: write one record with the new TID and release its lock."""
        if t.to_install:
            x = t.to_install.pop(0)
            rec = self.db[x]
            rec.value, rec.tid, rec.owner = t.writes[x], t.tid, None  # @line L10
            self.log.append(("w", t.name, x))
        if not t.to_install:
            self.log.append(("c", t.name, None))
            self.committed[t.name] = t
            t.phase = "done"

    def abort(self, t):
        for x in t.locked:
            self.db[x].owner = None
        self.sp.remove(t.name)
        self.log.append(("a", t.name, None))
        t.phase = "aborted"

    def advance_epoch(self):
        self.E += 1  # @line L11

    def step(self, t):
        """One atomic step of t. Return False if t had to wait."""
        if t.phase == "exec":
            self.exec_step(t)
        elif t.phase == "lock":
            return self.lock_step(t)
        elif t.phase == "epoch":
            self.epoch_step(t)
        elif t.phase == "validate":
            self.validate_step(t)
        elif t.phase == "tid":
            self.tid_step(t)
        elif t.phase == "install":
            self.install_step(t)
        return True


def simulate(rng, workers, items, epoch_rate=0.05, retries=2, validate=True):
    """Run the programs of each worker one after the other. workers is a list
    of lists of programs; a program is a list of ("r", x) and ("w", x). An
    aborted attempt restarts with a new name, at most retries times. Return
    the Silo object, with its log and its committed transactions."""
    silo = Silo(items, validate=validate)
    queues = [[(pid, p) for pid, p in progs] for progs in workers]
    current = [None] * len(workers)
    tries = [0] * len(workers)
    names = iter(range(1, 10 ** 9))
    while True:
        live = [w for w in range(len(workers)) if current[w] or queues[w]]
        if not live:
            return silo
        if rng.random() < epoch_rate:
            silo.advance_epoch()
            continue
        w = rng.choice(live)
        if current[w] is None:
            pid, prog = queues[w][0]
            current[w] = Txn(next(names), w, prog, pid)
        t = current[w]
        silo.step(t)
        if t.phase == "done":
            queues[w].pop(0)
            current[w], tries[w] = None, 0
        elif t.phase == "aborted":
            current[w] = None
            tries[w] += 1
            if tries[w] > retries:
                queues[w].pop(0)
                tries[w] = 0
