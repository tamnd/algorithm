# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/atomic-snapshot/. The authors are listed in prov/J3M2WS.jsonl.
"""Two simple snapshot objects from single-writer registers, for the explorer.

Process i owns the register ("R", i), which holds (value, seq). An update
writes the new value with the next sequence number, in one write.

- single_collect_scan reads each register once. It is NOT linearizable.
- double_collect_scan collects until two collects in a row are the same.
  It is linearizable and lock-free, but not wait-free.

The wait-free scan of Afek et al. is on the page afek-atomic-snapshot.
"""

from explorer import World


def collect(n):
    out = []
    for j in range(n):
        out.append((yield ("read", ("R", j))))
    return tuple(out)


def single_collect_scan(n):
    a = yield from collect(n)
    return tuple(r[0] for r in a)


def double_collect_scan(n):
    a = yield from collect(n)
    while True:
        b = yield from collect(n)
        if a == b:  # same sequence numbers: nothing changed in between
            return tuple(r[0] for r in b)
        a = b  # the second collect can be the first of the next pair


def program(i, n, ops, scan):
    seq = 0
    for name, v in ops:
        yield ("inv", name, v)
        if name == "update":
            seq += 1
            yield ("write", ("R", i), (v, seq))
            yield ("res", None)
        else:
            view = yield from scan(n)
            yield ("res", view)


def setup_for(programs, scan=double_collect_scan):
    n = len(programs)

    def setup():
        return {("R", j): (0, 0) for j in range(n)}, [program(i, n, ops, scan) for i, ops in enumerate(programs)]

    return setup


class Snapshot:
    """The sequential specification: update(v) by process i sets component i;
    scan returns all components."""

    def __init__(self, n, init=0):
        self.init = tuple([init] * n)

    def apply(self, s, name, arg, pid):
        if name == "update":
            return s[:pid] + (arg,) + s[pid + 1:], None
        if name == "scan":
            return s, s
        raise ValueError(name)


def updater_forever(i):
    seq = 0
    while True:
        seq += 1
        yield ("write", ("R", i), (seq, seq))


def starve_scanner(n, rounds=10_000):
    """Process 0 scans once; process 1 updates for ever. Each time the scanner
    has read R[1], process 1 writes once. So no two collects are the same.
    Returns (scanner done, its reads, writes of process 1)."""

    def setup():
        procs = [program(0, n, [("scan", None)], double_collect_scan)]
        procs += [updater_forever(i) for i in range(1, n)]
        return {("R", j): (0, 0) for j in range(n)}, procs

    w = World(setup)
    for _ in range(rounds):
        if w.done[0]:
            break
        op = w.next[0]
        w.step(0)
        if op == ("read", ("R", 1)):
            w.step(1)
    return w.done[0], w.steps[0], w.steps[1]
