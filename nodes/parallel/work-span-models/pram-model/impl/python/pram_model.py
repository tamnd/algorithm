# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pram-model/. The authors are listed in prov/43RZPV.jsonl.
"""A simulator for one synchronous step of a PRAM, with the access rules of its variants.

A step is a dict that maps a processor number to a pair (reads, compute):

    reads    a tuple of memory addresses that the processor reads
    compute  a function of the tuple of values read; it returns a list
             of (address, value) pairs that the processor writes

All reads see the memory as it was before the step. All writes go to a
new memory. A cell that was never written holds 0.

The rules:

    EREW            no cell is read by two processors, and no cell is written by two
    CREW            any number of readers; no cell is written by two processors
    CRCW common     concurrent writers of a cell must all write the same value
    CRCW arbitrary  one of the concurrent writers succeeds; the choice is not known
    CRCW priority   the writer with the smallest processor number succeeds
    CRCW combining  the cell gets the values combined by a given operator
"""

EREW = "EREW"
CREW = "CREW"
COMMON = "CRCW common"
ARBITRARY = "CRCW arbitrary"
PRIORITY = "CRCW priority"
COMBINING = "CRCW combining"
RULES = (EREW, CREW, COMMON, ARBITRARY, PRIORITY, COMBINING)


class AccessError(Exception):
    """A step broke the access rule of the model."""


def access_sets(step, mem):
    """Return (readers, writers, writes): readers[a] and writers[a] are sets of processors.

    writes[a] is the list of (processor, value) pairs for address a, in processor order.
    """
    readers, writers, writes = {}, {}, {}
    for pid in sorted(step):
        reads, compute = step[pid]
        for a in reads:
            readers.setdefault(a, set()).add(pid)
        values = tuple(mem.get(a, 0) for a in reads)
        for a, v in compute(values):
            writers.setdefault(a, set()).add(pid)
            writes.setdefault(a, []).append((pid, v))
    return readers, writers, writes


def resolve(rule, writes, combine=None, choose=None):
    """Apply the write rule and return the value written to each address."""
    out = {}
    for a, ws in writes.items():
        pids = {pid for pid, _ in ws}
        if len(pids) < len(ws):
            raise AccessError(f"a processor wrote cell {a!r} twice in one step")
        if len(ws) == 1:
            out[a] = ws[0][1]
        elif rule in (EREW, CREW):
            raise AccessError(f"{rule}: concurrent write to cell {a!r} by {sorted(pids)}")
        elif rule == COMMON:
            values = {v for _, v in ws}
            if len(values) > 1:
                raise AccessError(f"{rule}: different values written to cell {a!r}")
            out[a] = ws[0][1]
        elif rule == ARBITRARY:
            out[a] = (choose or (lambda c: c[-1]))(ws)[1]
        elif rule == PRIORITY:
            out[a] = min(ws)[1]
        elif rule == COMBINING:
            if combine is None:
                raise AccessError("the combining rule needs an operator")
            acc = ws[0][1]
            for _, v in ws[1:]:
                acc = combine(acc, v)
            out[a] = acc
        else:
            raise ValueError(f"unknown rule {rule!r}")
    return out


def run_step(mem, step, rule, combine=None, choose=None):
    """Run one synchronous step and return the new memory. mem is not changed."""
    readers, _, writes = access_sets(step, mem)
    if rule == EREW:
        for a, r in readers.items():
            if len(r) > 1:
                raise AccessError(f"EREW: concurrent read of cell {a!r} by {sorted(r)}")
    new = dict(mem)
    new.update(resolve(rule, writes, combine, choose))
    return new


class Pram:
    """A PRAM that counts time (steps) and work (processor steps)."""

    def __init__(self, rule, mem=None, combine=None, choose=None):
        if rule not in RULES:
            raise ValueError(f"unknown rule {rule!r}")
        self.rule = rule
        self.mem = dict(mem or {})
        self.combine = combine
        self.choose = choose
        self.step_work = []

    def step(self, step):
        self.mem = run_step(self.mem, step, self.rule, self.combine, self.choose)
        self.step_work.append(len(step))

    @property
    def time(self):
        return len(self.step_work)

    @property
    def work(self):
        return sum(self.step_work)


def brent_time(step_work, p):
    """Steps on p processors when step k of the work-time algorithm has step_work[k] operations."""
    return sum(-(-w // p) for w in step_work)


def run_step_on_p(mem, step, rule, p, combine=None, choose=None):
    """Run one step of many virtual processors on p real ones, in rounds of p.

    Every round reads the old memory, and the writes of all rounds are kept
    until the end, so the result is the same as one step of the full machine.
    Return (new memory, number of rounds).
    """
    pids = sorted(step)
    rounds = [pids[i:i + p] for i in range(0, len(pids), p)]
    readers, writes = {}, {}
    for chunk in rounds:
        part = {pid: step[pid] for pid in chunk}
        r, _, w = access_sets(part, mem)
        for a, s in r.items():
            readers.setdefault(a, set()).update(s)
        for a, ws in w.items():
            writes.setdefault(a, []).extend(ws)
    if rule == EREW:
        for a, r in readers.items():
            if len(r) > 1:
                raise AccessError(f"EREW: concurrent read of cell {a!r}")
    for a in writes:
        writes[a].sort()
    new = dict(mem)
    new.update(resolve(rule, writes, combine, choose))
    return new, len(rounds)


# ----------------------------------------------------------- examples


def tree_sum(values, rule=EREW):
    """Sum n values on an EREW PRAM by a balanced tree in ceil(lg n) steps and n - 1 operations.

    Cell ("A", i) holds the input. In the step with stride d, processor i
    (for i a multiple of 2d with i + d < n) adds A[i + d] into A[i].
    Return (sum, machine).
    """
    n = len(values)
    m = Pram(rule, {("A", i): v for i, v in enumerate(values)})
    d = 1
    while d < n:
        step = {}
        for i in range(0, n - d, 2 * d):
            step[i] = ((("A", i), ("A", i + d)), lambda x, i=i: [(("A", i), x[0] + x[1])])
        m.step(step)
        d *= 2
    return (m.mem.get(("A", 0), 0) if n else 0), m


def write_conflict_step(values):
    """Processor i writes values[i] to cell "x": the step that tells the write rules apart."""
    return {i: ((), lambda _, v=v: [("x", v)]) for i, v in enumerate(values)}
