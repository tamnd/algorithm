# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linearization-point/. The authors are listed in prov/X31NPD.jsonl.
"""The linearization point method, on the Treiber stack.

The stack is one shared word "top". A node is an immutable tuple
(uid, value, next), and a uid is never used twice, so a node is never
reused (as with a garbage collector, so there is no ABA problem).

Each operation yields ("lp",) right after the step that the proof names as
its linearization point. lp_order() then sorts the operations by these
points and checks that the sequence is a legal run of a sequential stack,
with the same results. A wrong choice of points fails this check even
though the stack is linearizable.
"""

from lincheck import Stack


def push(v, uid, lp_at="cas"):
    """Treiber push. lp_at="read" puts the point at the first read, which is wrong."""
    yield ("inv", "push", v)
    first = True
    while True:
        t = yield ("read", "top")                 # L1
        if lp_at == "read" and first:
            yield ("lp",)
            first = False
        ok = yield ("cas", "top", t, (uid, v, t))  # L2
        if ok:
            if lp_at == "cas":
                yield ("lp",)                       # the successful CAS
            yield ("res", None)
            return None


def pop():
    """Treiber pop."""
    yield ("inv", "pop", None)
    while True:
        t = yield ("read", "top")                 # L3
        if t is None:
            yield ("lp",)                           # the read that saw an empty stack
            yield ("res", None)
            return None
        ok = yield ("cas", "top", t, t[2])        # L4
        if ok:
            yield ("lp",)                           # the successful CAS
            yield ("res", t[1])
            return t[1]


def pop_no_cas():
    """A broken pop: it reads top and then writes top.next with a plain write."""
    yield ("inv", "pop", None)
    t = yield ("read", "top")
    if t is None:
        yield ("lp",)
        yield ("res", None)
        return None
    yield ("write", "top", t[2])
    yield ("lp",)
    yield ("res", t[1])
    return t[1]


def program(pid, ops, lp_at="cas", bad_pop=False):
    """Run a list of operations: ("push", v) or ("pop",)."""
    for k, op in enumerate(ops):
        if op[0] == "push":
            yield from push(op[1], (pid, k), lp_at)
        else:
            yield from (pop_no_cas() if bad_pop else pop())


def setup_for(programs, initial=(), lp_at="cas", bad_pop=False):
    """A setup function for the explorer. initial lists values bottom first."""

    def setup():
        top = None
        for i, v in enumerate(initial):
            top = (("init", i), v, top)
        procs = [program(p, ops, lp_at, bad_pop) for p, ops in enumerate(programs)]
        return {"top": top}, procs

    return setup


def lp_order(history, init=()):
    """Check the order given by the linearization points.

    Returns (True, sequence) when the operations, taken in the order of
    their points, form a legal stack history with the recorded results, and
    each point lies in its interval. Returns (False, reason) otherwise.
    """
    spec = Stack()
    state = tuple(init)
    current, seq, results = {}, [], {}
    for t, e in enumerate(history):
        if e[0] == "inv":
            current[e[1]] = (e[2], e[3], t)
        elif e[0] == "lp":
            name, arg, t0 = current[e[1]]
            state, r = spec.apply(state, name, arg, e[1])
            seq.append((e[1], name, arg, r, t0))
        elif e[0] == "res":
            results.setdefault(e[1], []).append(e[2])
    expected = {}
    for pid, name, arg, r, _ in seq:
        expected.setdefault(pid, []).append(r)
    for pid, rs in results.items():
        if expected.get(pid, [])[: len(rs)] != rs:
            return False, f"process {pid} returned {rs}, the point order gives {expected.get(pid)}"
    return True, seq
