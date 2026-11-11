# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-word-cas/. The authors are listed in prov/DFK374.jsonl.
"""The multi-word CAS of Harris, Fraser and Pratt (DISC 2002), for the explorer.

Every shared step is one atomic read, CAS or cmpxchg of the explorer. A data
word holds a plain value or a descriptor. Real code tells them apart by two
low bits of the word; here a descriptor is a tuple with a tag:

    ("R", pid, seq, a1, o1, a2, o2, n2)   an RDCSS descriptor
    ("C", pid, seq, entries)               a CASN descriptor

entries is a tuple of (address, old, new), sorted by address. The status of
the CASN descriptor ("C", pid, seq, ...) is the shared word ("status", pid,
seq). A descriptor is never reused, so its identity (pid, seq) is unique, as a
fresh allocation is in the paper. Plain values must not be tuples.

RDCSS(a1, o1, a2, o2, n2) (restricted double-compare single-swap) writes n2
to a2 only if a2 = o2 and a1 = o1, and returns the old value of a2. CASN uses
it with a1 = the status word and o1 = UNDECIDED, so that a descriptor goes
into a data word only while the CASN is still undecided.
"""

from explorer import World

UNDECIDED, SUCCEEDED, FAILED = "undecided", "succeeded", "failed"


def is_rdcss(v):
    return isinstance(v, tuple) and v[0] == "R"


def is_casn(v):
    return isinstance(v, tuple) and v[0] == "C"


def status_of(cd):
    return ("status", cd[1], cd[2])


# ------------------------------------------------------------------- RDCSS


def rdcss_complete(d):
    """Finish the RDCSS d, which is in the word d.a2: look at the control
    word a1, then put n2 or back o2 in place of d."""
    _, _, _, a1, o1, a2, o2, n2 = d
    v = yield ("read", a1)
    if v == o1:
        yield ("cas", a2, d, n2)
    else:
        yield ("cas", a2, d, o2)


def rdcss(d):
    _, _, _, a1, o1, a2, o2, n2 = d
    while True:
        r = yield ("cmpxchg", a2, o2, d)  # put d in a2 if a2 = o2
        if not is_rdcss(r):
            break
        yield from rdcss_complete(r)  # another RDCSS is there: finish it, retry
    if r == o2:
        yield from rdcss_complete(d)
    return r


def rdcss_read(a):
    while True:
        r = yield ("read", a)
        if not is_rdcss(r):
            return r
        yield from rdcss_complete(r)


# -------------------------------------------------------------------- CASN


def casn(cd, ctx):
    """Run the CASN descriptor cd to the end, as its owner or as a helper.

    ctx = [pid, seq] gives fresh identities to the RDCSS descriptors that
    this process makes. Returns True if cd succeeded.
    """
    entries = cd[3]
    st = status_of(cd)
    s = yield ("read", st)
    if s == UNDECIDED:
        # Phase 1: put cd in every word, in address order, while undecided.
        status = SUCCEEDED
        i = 0
        while i < len(entries) and status == SUCCEEDED:
            a, old, _ = entries[i]
            ctx[1] += 1
            d = ("R", ctx[0], ctx[1], st, UNDECIDED, a, old, cd)
            v = yield from rdcss(d)
            if is_casn(v):
                if v != cd:
                    yield from casn(v, ctx)  # another CASN is in the way: help it
                    continue  # and try this word again
            elif v != old:
                status = FAILED
            i += 1
        yield ("cas", st, UNDECIDED, status)  # the decision: one CAS
    # Phase 2: replace cd by the new value (success) or the old one (failure).
    s = yield ("read", st)
    ok = s == SUCCEEDED
    for a, old, new in entries:
        yield ("cas", a, cd, new if ok else old)
    return ok


def casn_read(a, ctx):
    while True:
        r = yield from rdcss_read(a)
        if not is_casn(r):
            return r
        yield from casn(r, ctx)


# --------------------------------------------------------------- programs


def op_casn(pid, seq, entries, ctx, sort=True):
    cd = ("C", pid, seq, tuple(sorted(entries)) if sort else tuple(entries))
    yield ("inv", "casn", tuple(entries))
    ok = yield from casn(cd, ctx)
    yield ("res", ok)
    return ok


def op_read(a, ctx):
    yield ("inv", "read", a)
    v = yield from casn_read(a, ctx)
    yield ("res", v)
    return v


def program(pid, ops, sort=True):
    """ops is a list of ("casn", entries) and ("read", address)."""
    ctx = [pid, 0]
    for k, (name, arg) in enumerate(ops):
        if name == "casn":
            yield from op_casn(pid, k, arg, ctx, sort)
        else:
            yield from op_read(arg, ctx)


def setup_for(programs, init, sort=True):
    """init maps each data address to its first value."""

    def setup():
        mem = dict(init)
        for pid, ops in enumerate(programs):
            for k, (name, _) in enumerate(ops):
                if name == "casn":
                    mem[("status", pid, k)] = UNDECIDED  # a fresh descriptor
        return mem, [program(p, ops, sort) for p, ops in enumerate(programs)]

    return setup


class Words:
    """The sequential specification: some words, a k-word CAS and a read."""

    def __init__(self, init):
        self.addrs = sorted(init)
        self.init = tuple(init[a] for a in self.addrs)

    def apply(self, s, name, arg, pid):
        if name == "read":
            return s, s[self.addrs.index(arg)]
        if name == "casn":
            if all(s[self.addrs.index(a)] == old for a, old, _ in arg):
                s = list(s)
                for a, _, new in arg:
                    s[self.addrs.index(a)] = new
                return tuple(s), True
            return s, False
        raise ValueError(name)


# --------------------------------------------------------- measurements


def solo_cost(k):
    """Steps of one CASN on k words with no other process: (cas, reads)."""
    init = {f"w{i}": 0 for i in range(k)}
    entries = tuple((f"w{i}", 0, 1) for i in range(k))
    w = World(setup_for([[("casn", entries)]], init))
    while not w.done[0]:
        w.step(0)
    cas = sum(1 for _, op, _ in w.trace if op[0] in ("cas", "cmpxchg"))
    reads = sum(1 for _, op, _ in w.trace if op[0] == "read")
    return cas, reads, w.history[-1][2], {a: w.mem.get(a) for a in init}


def counter_loop(pid):
    """Increment the pair (x, y) for ever with 2-word CASN; never returns."""
    ctx = [pid, 0]
    k = 0
    while True:
        x = yield from casn_read("x", ctx)
        y = yield from casn_read("y", ctx)
        cd = ("C", pid, k, (("x", x, x + 1), ("y", y, y + 1)))
        yield ("write", status_of(cd), UNDECIDED)  # a fresh descriptor
        yield from casn(cd, ctx)
        k += 1


def starve_reader(rounds):
    """Process 0 reads x once; process 1 updates x and y for ever.

    The schedule lets process 0 take a step only while x holds a descriptor,
    or while it is not about to read x. Each time, process 0 helps the CASN
    to the end and reads x again, and by then a new descriptor is there.
    Returns (steps of process 0, whether it is done, CASNs of process 1 that
    succeeded).
    """

    def setup():
        return {"x": 0, "y": 0}, [program(0, [("read", "x")]), counter_loop(1)]

    w = World(setup)
    for _ in range(rounds):
        op = w.next[0]
        if op == ("read", "x") and not is_casn(w.mem.get("x")):
            while not is_casn(w.mem.get("x")):
                w.step(1)
        else:
            w.step(0)
        if w.done[0]:
            break
    decided = sum(
        1 for _, op, r in w.trace if op[0] == "cas" and op[1][0] == "status" and op[3] == SUCCEEDED and r
    )
    return w.steps[0], w.done[0], decided
