# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obstruction-freedom/. The authors are listed in prov/V63Y97.jsonl.
"""The obstruction-free array deque of Herlihy, Luchangco and Moir (2003).

The deque lives in an array A[0..size-1]. Each cell holds a pair
(value, counter). A value is LN (left null), RN (right null) or data. The
array always has the form LN+ data* RN+: at least one LN at the left end
and at least one RN at the right end. The data in between is the deque,
read from left to right.

Every CAS adds 1 to the counter of the cell it writes. An operation first
bumps the counter of the neighbour cell, to stop a concurrent change there,
and then writes its own cell. Two operations at opposite ends of an empty
deque can bump each other's neighbour cell for ever: that is a livelock,
so the deque is obstruction-free but not lock-free.

The oracle finds the edge by a scan of reads. Any oracle is correct, since
the operation checks the two cells again; a bad oracle only costs retries.
"""

from explorer import World, replay, solo

LN, RN = "LN", "RN"


def cell(i):
    return ("A", i)


def oracle_right(size):
    """The index of the leftmost RN, found by a scan from the left."""
    for i in range(1, size):
        c = yield ("read", cell(i))
        if c[0] == RN:
            return i
    return size - 1


def oracle_left(size):
    """The index of the rightmost LN, found by a scan from the right."""
    for i in range(size - 2, -1, -1):
        c = yield ("read", cell(i))
        if c[0] == LN:
            return i
    return 0


def rightpush(v, size):
    yield ("inv", "rightpush", v)
    while True:
        k = yield from oracle_right(size)
        prev = yield ("read", cell(k - 1))
        cur = yield ("read", cell(k))
        if prev[0] != RN and cur[0] == RN:
            if k == size - 1:
                yield ("res", "full")
                return
            if (yield ("cas", cell(k - 1), prev, (prev[0], prev[1] + 1))):
                if (yield ("cas", cell(k), cur, (v, cur[1] + 1))):
                    yield ("res", "ok")
                    return


def rightpop(size):
    yield ("inv", "rightpop", None)
    while True:
        k = yield from oracle_right(size)
        cur = yield ("read", cell(k - 1))
        nxt = yield ("read", cell(k))
        if cur[0] != RN and nxt[0] == RN:
            if cur[0] == LN and (yield ("read", cell(k - 1))) == cur:
                yield ("res", "empty")
                return
            if (yield ("cas", cell(k), nxt, (RN, nxt[1] + 1))):
                if (yield ("cas", cell(k - 1), cur, (RN, cur[1] + 1))):
                    yield ("res", cur[0])
                    return


def leftpush(v, size):
    yield ("inv", "leftpush", v)
    while True:
        k = yield from oracle_left(size)
        prev = yield ("read", cell(k + 1))
        cur = yield ("read", cell(k))
        if prev[0] != LN and cur[0] == LN:
            if k == 0:
                yield ("res", "full")
                return
            if (yield ("cas", cell(k + 1), prev, (prev[0], prev[1] + 1))):
                if (yield ("cas", cell(k), cur, (v, cur[1] + 1))):
                    yield ("res", "ok")
                    return


def leftpop(size):
    yield ("inv", "leftpop", None)
    while True:
        k = yield from oracle_left(size)
        cur = yield ("read", cell(k + 1))
        nxt = yield ("read", cell(k))
        if cur[0] != LN and nxt[0] == LN:
            if cur[0] == RN and (yield ("read", cell(k + 1))) == cur:
                yield ("res", "empty")
                return
            if (yield ("cas", cell(k), nxt, (LN, nxt[1] + 1))):
                if (yield ("cas", cell(k + 1), cur, (LN, cur[1] + 1))):
                    yield ("res", cur[0])
                    return


OPS = {"rightpush": rightpush, "leftpush": leftpush, "rightpop": rightpop, "leftpop": leftpop}


def program(ops, size):
    for name, arg in ops:
        if name.endswith("push"):
            yield from OPS[name](arg, size)
        else:
            yield from OPS[name](size)


def setup_for(programs, items=(), left=2, right=2):
    """An array LN*left, items, RN*right; one program of (name, arg) pairs per process."""
    layout = [LN] * left + list(items) + [RN] * right
    size = len(layout)

    def setup():
        mem = {cell(i): (v, 0) for i, v in enumerate(layout)}
        return mem, [program(p, size) for p in programs]

    return setup


def contents(w):
    """The deque held in the array of w, from left to right."""
    vals = [w.mem.get(cell(i))[0] for i in range(len(w.mem.cells))]
    return tuple(v for v in vals if v not in (LN, RN))


class Deque:
    """The sequential specification. A push answers "ok"; a pop on an empty deque answers "empty"."""

    def __init__(self, init=()):
        self.init = tuple(init)

    def apply(self, s, name, arg, pid):
        if name == "rightpush":
            return s + (arg,), "ok"
        if name == "leftpush":
            return (arg,) + s, "ok"
        if name == "rightpop":
            return (s[:-1], s[-1]) if s else (s, "empty")
        if name == "leftpop":
            return (s[1:], s[0]) if s else (s, "empty")
        raise ValueError(name)


def bounded_states(setup, depth):
    """Every distinct state reachable in at most depth steps, with a schedule to reach it."""
    seen = {}
    stack = [()]
    while stack:
        s = stack.pop()
        w = replay(setup, s)
        k = w.key(history=True)
        if k in seen:
            continue
        seen[k] = s
        if len(s) < depth:
            for p in reversed(w.enabled()):
                stack.append(s + (p,))
    return list(seen.values())


def max_solo_steps(setup, depth, bound=200):
    """Over all states within depth steps, the most steps a process needs to finish alone.

    Returns None if some process does not finish alone (a loop or the bound).
    """
    worst = 0
    for s in bounded_states(setup, depth):
        w = replay(setup, s)
        for p in w.enabled():
            outcome, steps = solo(replay(setup, s), p, bound)
            if outcome != "done":
                return None
            worst = max(worst, steps)
    return worst


def livelock(rounds):
    """rightpush and leftpush on an empty deque that stop each other for ever.

    Each round: p0 runs up to its first CAS, p1 runs up to its first CAS,
    both first CASes succeed, and then both second CASes fail, because each
    process bumped the counter of the cell that the other one wanted to write.
    """
    setup = setup_for([[("rightpush", "a")], [("leftpush", "b")]])
    w = World(setup)
    for _ in range(rounds):
        for p in (0, 1):
            while w.next[p][0] != "cas":
                w.step(p)
        for p in (0, 1, 0, 1):
            w.step(p)
    return w
