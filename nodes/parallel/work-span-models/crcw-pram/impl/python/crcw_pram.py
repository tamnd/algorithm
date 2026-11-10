# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crcw-pram/. The authors are listed in prov/94DN1Q.jsonl.
"""The CRCW PRAM: the four write rules, OR and maximum in O(1) steps, and the
simulation of one priority write step on an EREW PRAM by a bitonic sorting network.

A step maps a processor number to (reads, compute). reads is a tuple of
addresses; compute takes the tuple of values read and returns a list of
(address, value) writes. Reads see the old memory; writes go to a new memory.
A cell that was never written holds 0.
"""

EREW = "EREW"
CREW = "CREW"
COMMON = "common"
ARBITRARY = "arbitrary"
PRIORITY = "priority"
COMBINING = "combining"


class AccessError(Exception):
    pass


def access_sets(step, mem):
    readers, writes = {}, {}
    for pid in sorted(step):
        reads, compute = step[pid]
        for a in reads:
            readers.setdefault(a, set()).add(pid)
        for a, v in compute(tuple(mem.get(a, 0) for a in reads)):
            writes.setdefault(a, []).append((pid, v))
    return readers, writes


def run_step(mem, step, rule, combine=None, choose=None):
    """One synchronous step under the given rule. Return (new memory, readers, writes)."""
    readers, writes = access_sets(step, mem)
    if rule == EREW and any(len(s) > 1 for s in readers.values()):
        raise AccessError("EREW: concurrent read")
    new = dict(mem)
    for a, ws in writes.items():
        if len({pid for pid, _ in ws}) < len(ws):
            raise AccessError(f"a processor wrote cell {a!r} twice")
        if len(ws) == 1:
            new[a] = ws[0][1]
        elif rule in (EREW, CREW):
            raise AccessError(f"{rule}: concurrent write to cell {a!r}")
        elif rule == COMMON:
            if len({v for _, v in ws}) > 1:
                raise AccessError(f"common: different values written to cell {a!r}")
            new[a] = ws[0][1]
        elif rule == ARBITRARY:
            new[a] = (choose or (lambda c: c[-1]))(ws)[1]
        elif rule == PRIORITY:
            new[a] = min(ws)[1]
        elif rule == COMBINING:
            acc = ws[0][1]
            for _, v in ws[1:]:
                acc = combine(acc, v)
            new[a] = acc
        else:
            raise ValueError(f"unknown rule {rule!r}")
    return new, readers, writes


class Machine:
    def __init__(self, mem, rule, **kw):
        self.mem, self.rule, self.kw = dict(mem), rule, kw
        self.time, self.work, self.max_writers, self.max_readers = 0, 0, 0, 0

    def step(self, step):
        self.mem, readers, writes = run_step(self.mem, step, self.rule, **self.kw)
        self.time += 1
        self.work += len(step)
        self.max_readers = max([self.max_readers] + [len(s) for s in readers.values()])
        self.max_writers = max([self.max_writers] + [len(w) for w in writes.values()])


# ------------------------------------------------------------ OR and max


def crcw_or(bits, rule=COMMON):
    """OR of n bits in one step with n processors: each processor that sees a 1 writes 1 to cell r."""
    m = Machine({("A", i): b for i, b in enumerate(bits)}, rule)
    m.step({i: ((("A", i),), lambda v: [("r", 1)] if v[0] else []) for i in range(len(bits))})
    return m.mem.get("r", 0), m


def crcw_max(xs, rule=COMMON, tie_break=True):
    """Maximum of n numbers in three steps with n(n - 1) processors in the middle step.

    Step 1: processor i sets M[i] = 1.
    Step 2: processor (i, j), i != j, reads A[i] and A[j] and sets M[i] = 0 if A[j] beats A[i].
            With tie_break, A[j] beats A[i] if A[j] > A[i], or A[j] == A[i] and j < i.
            Without it, only if A[j] > A[i].
    Step 3: processor i with M[i] == 1 writes A[i] to cell "max" and i to cell "arg".
    Return (max, arg, machine). For n == 0 return (None, None, machine).
    """
    n = len(xs)
    m = Machine({("A", i): x for i, x in enumerate(xs)}, rule)
    if n == 0:
        return None, None, m
    m.step({i: ((), lambda v, i=i: [(("M", i), 1)]) for i in range(n)})

    def beats(i, j):
        return lambda v: [(("M", i), 0)] if v[1] > v[0] or (tie_break and v[1] == v[0] and j < i) else []

    m.step({(i, j): ((("A", i), ("A", j)), beats(i, j)) for i in range(n) for j in range(n) if i != j})
    if tie_break:  # exactly one winner, so the writes are exclusive
        m.step({i: ((("M", i), ("A", i)), lambda v, i=i: [("max", v[1]), ("arg", i)] if v[0] else [])
                for i in range(n)})
        return m.mem["max"], m.mem["arg"], m
    # all winners hold the same value, so the common rule allows their concurrent write
    m.step({i: ((("M", i), ("A", i)), lambda v: [("max", v[1])] if v[0] else []) for i in range(n)})
    return m.mem["max"], None, m


def leftmost_one(bits, rule=PRIORITY):
    """Under priority, each processor with a 1 writes its index to cell "first"; the smallest wins."""
    m = Machine({("A", i): b for i, b in enumerate(bits)}, rule)
    m.step({i: ((("A", i),), lambda v, i=i: [("first", i)] if v[0] else []) for i in range(len(bits))})
    return (m.mem["first"] if any(bits) else None), m


# ------------------------------------- priority writes on an EREW PRAM

INF = float("inf")


def bitonic_stages(q):
    """The comparator stages of Batcher's bitonic sorter on q = 2^k wires.

    Each stage is a list of (low, high) wire pairs, disjoint within the stage;
    the comparator puts the smaller item on the wire low.
    """
    stages = []
    size = 2
    while size <= q:
        stride = size // 2
        while stride >= 1:
            stage = []
            for i in range(q):
                j = i ^ stride
                if j > i:
                    stage.append((i, j) if i & size == 0 else (j, i))
            stages.append(stage)
            stride //= 2
        size *= 2
    return stages


def simulate_priority_write(requests):
    """Run one priority write step on an EREW PRAM.

    requests[i] is None or (address, value): processor i wants to write value to address.
    Return (writes, steps): writes maps each address to the value of the request with the
    smallest processor number, and steps is the list of EREW steps that were run. Every
    step is checked for exclusive reads and writes.

    The method: processor i writes the key (address, i, value) to R[i]; a bitonic sorting
    network sorts R by (address, processor); processor k copies R[k - 1] to L[k]; and
    processor k writes its value to its address if R[k] holds a real request whose address
    differs from that of L[k]. These are the first requests of the groups of equal
    addresses, one writer for each address.
    """
    p = len(requests)
    q = 1
    while q < p:
        q *= 2
    mem = {}
    steps = []

    def run(step):
        nonlocal mem
        mem, readers, writes = run_step(mem, step, EREW)  # raises on any conflict
        steps.append((readers, writes))

    pad = (INF, INF, None)
    run({i: ((), lambda v, i=i: [(("R", i), (requests[i][0], i, requests[i][1]) if i < p and requests[i]
                                   else pad)]) for i in range(q)})
    for stage in bitonic_stages(q):
        run({lo: ((("R", lo), ("R", hi)), lambda v, lo=lo, hi=hi: [(("R", lo), min(v)), (("R", hi), max(v))])
             for lo, hi in stage})
    run({k: (((("R", k - 1),) if k else ()), lambda v, k=k: [(("L", k), v[0] if k else pad)]) for k in range(q)})

    def first(v):
        (addr, _, value), (prev, _, _) = v
        return [(("out", addr), value)] if addr != INF and addr != prev else []

    run({k: ((("R", k), ("L", k)), first) for k in range(q)})
    out = {a[1]: v for a, v in mem.items() if isinstance(a, tuple) and a[0] == "out"}
    return out, steps
