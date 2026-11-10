# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erew-pram/. The authors are listed in prov/Z1W3PV.jsonl.
"""The EREW PRAM: a step simulator with the exclusive-read exclusive-write check,
broadcast by doubling, and the tree sum.

A step maps a processor number to (reads, compute). reads is a tuple of
addresses; compute takes the tuple of values read and returns a list of
(address, value) writes. Reads see the old memory; writes go to a new one.
A cell that was never written holds 0.
"""


class AccessError(Exception):
    pass


def access_sets(step, mem):
    """Return (readers, writers, writes) for one step, before any rule is applied."""
    readers, writers, writes = {}, {}, {}
    for pid in sorted(step):
        reads, compute = step[pid]
        for a in reads:
            readers.setdefault(a, set()).add(pid)
        for a, v in compute(tuple(mem.get(a, 0) for a in reads)):
            writers.setdefault(a, set()).add(pid)
            writes.setdefault(a, []).append((pid, v))
    return readers, writers, writes


def is_exclusive(readers, writers):
    return all(len(s) == 1 for s in readers.values()) and all(len(s) == 1 for s in writers.values())


def run_step(mem, step, concurrent_read=False):
    """One step of an EREW PRAM (or of a CREW PRAM if concurrent_read is True)."""
    readers, writers, writes = access_sets(step, mem)
    if not concurrent_read:
        for a, s in readers.items():
            if len(s) > 1:
                raise AccessError(f"concurrent read of cell {a!r} by {sorted(s)}")
    for a, s in writers.items():
        if len(s) > 1:
            raise AccessError(f"concurrent write of cell {a!r} by {sorted(s)}")
    new = dict(mem)
    for a, ws in writes.items():
        if len(ws) > 1:
            raise AccessError(f"processor {ws[0][0]} wrote cell {a!r} twice")
        new[a] = ws[0][1]
    return new


def run(mem, steps, concurrent_read=False):
    """Run a list of steps. Return (memory, trace), where trace[k] = (readers, writers) of step k."""
    trace = []
    for step in steps:
        readers, writers, _ = access_sets(step, mem)
        trace.append((readers, writers))
        mem = run_step(mem, step, concurrent_read)
    return mem, trace


def broadcast_steps(p):
    """Copy the value in cell "x" to cells ("B", 0..p-1) in 1 + ceil(lg p) EREW steps.

    Step 0: processor 0 copies x into B[0].
    Step with d = 1, 2, 4, ...: processor i, for d <= i < min(2d, p), copies B[i - d] into B[i].
    """
    if p == 0:
        return []
    steps = [{0: (("x",), lambda v: [(("B", 0), v[0])])}]
    d = 1
    while d < p:
        steps.append({i: ((("B", i - d),), lambda v, i=i: [(("B", i), v[0])]) for i in range(d, min(2 * d, p))})
        d *= 2
    return steps


def naive_broadcast_steps(p):
    """Every processor reads x in the same step: legal on a CREW PRAM, illegal on an EREW PRAM."""
    return [{i: (("x",), lambda v, i=i: [(("B", i), v[0])]) for i in range(p)}]


def tree_sum_steps(n):
    """Add cells ("A", 0..n-1) into ("A", 0) by a balanced tree in ceil(lg n) EREW steps."""
    steps, d = [], 1
    while d < n:
        steps.append({i: ((("A", i), ("A", i + d)), lambda v, i=i: [(("A", i), v[0] + v[1])])
                      for i in range(0, n - d, 2 * d)})
        d *= 2
    return steps


def affected_counts(mem0, mem1, steps):
    """Run the same steps on two memories and count the cells whose contents differ.

    Return the list c[0], c[1], ...: c[t] is the number of differing cells after t steps.
    It also returns k[t], the number of processors in step t whose read values differ.
    """
    cells = [sum(1 for a in set(mem0) | set(mem1) if mem0.get(a, 0) != mem1.get(a, 0))]
    procs = [0]
    for step in steps:
        k = 0
        for pid, (reads, _) in step.items():
            if any(mem0.get(a, 0) != mem1.get(a, 0) for a in reads):
                k += 1
        procs.append(k)
        mem0, mem1 = run_step(mem0, step), run_step(mem1, step)
        cells.append(sum(1 for a in set(mem0) | set(mem1) if mem0.get(a, 0) != mem1.get(a, 0)))
    return cells, procs
