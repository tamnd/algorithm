# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/afek-atomic-snapshot/. The authors are listed in prov/KGSNTB.jsonl.
"""The wait-free single-writer atomic snapshot of Afek, Attiya, Dolev, Gafni,
Merritt and Shavit (JACM 1993), unbounded version, for the explorer.

Process i owns the register ("R", i). It holds (val, seq, view): the value of
component i, the number of updates of i so far, and the result of the scan
that i made inside its last update. Every shared step is one atomic read or
write of one register.

For comparison, double_collect_scan is the simple lock-free scan: collect
until two collects in a row are the same. It is not wait-free.
"""

from explorer import World


def collect(n):
    """Read R[0], ..., R[n-1], one at a time."""
    out = []
    for j in range(n):
        out.append((yield ("read", ("R", j))))
    return tuple(out)


def afek_scan(n):
    """Returns (view, number of reads)."""
    moved = [False] * n  # @line L3
    reads = 0
    while True:  # @line L4
        a = yield from collect(n)  # @line L5
        b = yield from collect(n)  # @line L6
        reads += 2 * n
        if all(a[j][1] == b[j][1] for j in range(n)):  # @line L7
            return tuple(r[0] for r in b), reads  # @line L8
        for j in range(n):  # @line L9
            if a[j][1] != b[j][1]:
                if moved[j]:  # @line L10
                    return b[j][2], reads  # @line L11
                moved[j] = True  # @line L12


def double_collect_scan(n):
    """Returns (view, number of reads). It may loop for ever."""
    reads = 0
    while True:
        a = yield from collect(n)
        b = yield from collect(n)
        reads += 2 * n
        if all(a[j][1] == b[j][1] for j in range(n)):
            return tuple(r[0] for r in b), reads


def update(i, n, v, seq, afek=True):
    """The seq-th update of process i. Returns the number of reads and writes."""
    if afek:
        view, reads = yield from afek_scan(n)  # @line L1
    else:
        view, reads = None, 0  # the simple object needs no view
    yield ("write", ("R", i), (v, seq, view))  # @line L2
    return reads + 1


def program(i, n, ops, afek=True):
    """ops is a list of ("update", v) and ("scan", None).
    Returns the number of shared steps of each operation."""
    seq = 0  # process i is the only writer of R[i], so it keeps its seq locally
    cost = []
    for name, v in ops:
        yield ("inv", name, v)
        if name == "update":
            seq += 1
            c = yield from update(i, n, v, seq, afek)
            yield ("res", None)
        else:
            view, c = yield from (afek_scan(n) if afek else double_collect_scan(n))
            yield ("res", view)
        cost.append(c)
    return cost


def initial_memory(n, init=0):
    return {("R", j): (init, 0, tuple([init] * n)) for j in range(n)}


def setup_for(programs, afek=True):
    n = len(programs)

    def setup():
        return initial_memory(n), [program(i, n, ops, afek) for i, ops in enumerate(programs)]

    return setup


class Snapshot:
    """The sequential specification: n components, update(v) by process i
    sets component i, scan returns all components."""

    def __init__(self, n, init=0):
        self.init = tuple([init] * n)

    def apply(self, s, name, arg, pid):
        if name == "update":
            return s[:pid] + (arg,) + s[pid + 1:], None
        if name == "scan":
            return s, s
        raise ValueError(name)


def updater_forever(i, n, afek):
    seq = 0
    while True:
        seq += 1
        yield from update(i, n, seq, seq, afek)


def adversary(n, afek, rounds=5000):
    """Process 0 scans once; processes 1 .. n-1 update for ever.

    The schedule: whenever the scanner has just finished its first collect,
    process 1 completes one update before the scanner reads again. So the
    two collects of the scanner always differ in R[1].
    Returns (scanner done, its reads, updates done by the others).
    """

    def setup():
        procs = [program(0, n, [("scan", None)], afek)]
        procs += [updater_forever(i, n, afek) for i in range(1, n)]
        return initial_memory(n), procs

    w = World(setup)
    reads_in_collect = 0
    for _ in range(rounds):
        if w.done[0]:
            break
        w.step(0)
        reads_in_collect += 1
        if reads_in_collect == n:  # the first collect of a pair is complete
            while True:  # process 1 runs to the end of its next write
                op = w.next[1]
                w.step(1)
                if op[0] == "write":
                    break
        if reads_in_collect == 2 * n:
            reads_in_collect = 0
    updates = sum(1 for _, op, _ in w.trace if op[0] == "write")
    return w.done[0], w.steps[0], updates
