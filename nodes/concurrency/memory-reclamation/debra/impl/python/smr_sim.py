# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/debra/. The authors are listed in prov/K7CR9Y.jsonl.
"""A small simulator for safe memory reclamation schemes.

A process is a generator. It yields one shared step at a time as a tuple,
and the scheduler sends back the result of the step. The memory is a set of
blocks. An int block is a node from the allocator; a str block is a static
global that is never freed. The allocator poisons freed blocks: a read or
write of a freed block raises UseAfterFree, and a second free raises
DoubleFree. Freed addresses are reused in LIFO order, which is what makes
the ABA problem show.

Steps:
  ("read", a, f)                      -> value
  ("read2", a, f, g)                  -> (a.f, a.g), one double-width load
  ("write", a, f, v)                  -> None
  ("cas", a, f, old, new)             -> bool
  ("dcas", a, f, g, o1, o2, n1, n2)   -> bool, double-width CAS on a.f, a.g
  ("dcas2", a, f, b, g, o1, o2, n1, n2) -> bool, CAS on two arbitrary words
  ("faa", a, f, d)                    -> old value
  ("swap", a, f, v)                   -> old value
  ("wait", a, f, ok)                  -> value; enabled only if a.f is in ok
  ("alloc", fields)                   -> new address
  ("free", a)                         -> None
  ("signal", q)                       -> None, sets the pending signal of q

The explorer runs every interleaving of a small run (with a cache of seen
states); run_random runs seeded random schedules; run_stall stops one
process for good and measures how much garbage the others leave.
Cost: the explorer is exponential in the number of steps; use it only for
two or three processes with one or two operations each.
"""

from __future__ import annotations

import random
from typing import Any, Callable, Iterator, Optional

Gen = Iterator[Any]


class SimError(Exception):
    """A memory safety violation found by the simulator."""


class UseAfterFree(SimError):
    pass


class DoubleFree(SimError):
    pass


class Corrupt(SimError):
    """The final state is wrong: a value is lost or returned twice."""


class Restart(Exception):
    """A scheme asks the client to restart the current attempt."""


class Neutralized(Restart):
    """Thrown into a process when it handles a signal in a restartable phase."""


class Memory:
    """Blocks with a poisoning, address-reusing allocator.

    With type_stable=True a freed block stays a node: reads of it are
    allowed (and counted in stale_reads), and so are writes of the fields
    in stable. This models a type-stable pool.
    """

    def __init__(self, reuse: bool = True, type_stable: bool = False, stable: tuple = ()) -> None:
        self.cells: dict = {}
        self.freed: set = set()
        self.pool: list = []
        self.top = 0
        self.reuse = reuse
        self.type_stable = type_stable
        self.stable = set(stable)
        self.retired: set = set()
        self.nretired = 0
        self.nfreed = 0
        self.peak = 0
        self.stale_reads = 0

    def static(self, name: str, **fields: Any) -> None:
        self.cells[name] = dict(fields)

    def new(self, **fields: Any) -> int:
        """Allocate outside of any process, for the initial state."""
        return self.step(("alloc", fields))

    def note_retire(self, a: int) -> None:
        if a in self.retired or a in self.freed:
            raise DoubleFree(f"node {a} retired twice")
        self.retired.add(a)
        self.nretired += 1
        self.peak = max(self.peak, len(self.retired))

    def unreclaimed(self) -> int:
        return len(self.retired)

    def _cell(self, a: Any, f: Any, write: bool) -> dict:
        if a in self.freed:
            if self.type_stable and (not write or f in self.stable):
                self.stale_reads += 0 if write else 1
                return self.cells[a]
            raise UseAfterFree(f"{'write' if write else 'read'} of {a}.{f} after free")
        if a not in self.cells:
            raise UseAfterFree(f"access to {a}.{f}, which is not a block")
        return self.cells[a]

    def step(self, op: tuple) -> Any:
        k = op[0]
        if k == "read" or k == "wait":
            return self._cell(op[1], op[2], False).get(op[2])
        if k == "read2":
            c = self._cell(op[1], op[2], False)
            return (c.get(op[2]), c.get(op[3]))
        if k == "write":
            self._cell(op[1], op[2], True)[op[2]] = op[3]
            return None
        if k == "cas":
            c = self._cell(op[1], op[2], True)
            if c.get(op[2]) == op[3]:
                c[op[2]] = op[4]
                return True
            return False
        if k == "dcas":
            _, a, f, g, o1, o2, n1, n2 = op
            c = self._cell(a, f, True)
            if (c.get(f), c.get(g)) == (o1, o2):
                c[f], c[g] = n1, n2
                return True
            return False
        if k == "dcas2":
            _, a, f, b, g, o1, o2, n1, n2 = op
            c, d = self._cell(a, f, True), self._cell(b, g, True)
            if c.get(f) == o1 and d.get(g) == o2:
                c[f], d[g] = n1, n2
                return True
            return False
        if k == "faa" or k == "swap":
            c = self._cell(op[1], op[2], True)
            old = c.get(op[2])
            c[op[2]] = old + op[3] if k == "faa" else op[3]
            return old
        if k == "alloc":
            if self.reuse and self.pool:
                a = self.pool.pop()
                self.freed.discard(a)
                kept = {f: v for f, v in self.cells[a].items() if f in self.stable}
                self.cells[a] = dict(op[1])
                if self.type_stable:
                    self.cells[a].update(kept)
            else:
                self.top += 1
                a = self.top
                self.cells[a] = dict(op[1])
            return a
        if k == "free":
            a = op[1]
            if a in self.freed:
                raise DoubleFree(f"node {a} freed twice")
            if a not in self.cells or isinstance(a, str):
                raise UseAfterFree(f"free of {a}, which is not a node")
            self.freed.add(a)
            self.retired.discard(a)
            self.nfreed += 1
            self.pool.append(a)
            if not self.type_stable:
                self.cells[a] = {f: "poison" for f in self.cells[a]}
            return None
        if k == "signal":
            self.cells["sig"][op[1]] = True
            return None
        raise ValueError(f"unknown step {op!r}")

    def enabled(self, op: Optional[tuple]) -> bool:
        if op is None:
            return False
        if op[0] == "wait":
            c = self.cells.get(op[1])
            return c is not None and op[1] not in self.freed and c.get(op[2]) in op[3]
        return True

    def key(self) -> tuple:
        def items(d: dict) -> tuple:
            return tuple(sorted(d.items(), key=lambda kv: repr(kv[0])))

        return (
            tuple((repr(a), items(c)) for a, c in sorted(self.cells.items(), key=lambda kv: repr(kv[0]))),
            tuple(sorted(self.freed)),
            tuple(self.pool),
            tuple(sorted(self.retired)),
        )


class World:
    """One run. make() returns (memory, list of generators, scheme, check)."""

    def __init__(self, make: Callable[[], tuple]) -> None:
        self.mem, gens, self.scheme, self.check = make()
        self.gens = list(gens)
        self.n = len(self.gens)
        self.hist: list = [[] for _ in range(self.n)]
        self.rets: list = [None] * self.n
        self.ops: list = [None] * self.n
        self.steps = 0
        for i, g in enumerate(self.gens):
            self._resume(i, None, first=True)

    def _resume(self, i: int, res: Any, first: bool = False, throw: bool = False) -> None:
        g = self.gens[i]
        try:
            if throw:
                self.ops[i] = g.throw(Neutralized())
            else:
                self.ops[i] = next(g) if first else g.send(res)
        except StopIteration as e:
            self.ops[i] = None
            self.rets[i] = e.value

    def signalled(self, i: int) -> bool:
        s = self.mem.cells.get("sig")
        return s is not None and bool(s.get(i))

    def enabled(self) -> list:
        return [i for i in range(self.n) if self.ops[i] is not None and (self.signalled(i) or self.mem.enabled(self.ops[i]))]

    def done(self) -> bool:
        return all(op is None for op in self.ops)

    def step(self, i: int) -> None:
        """One step of process i. A pending signal is handled first, as its own step."""
        self.steps += 1
        if self.signalled(i):
            self.mem.cells["sig"][i] = False
            self.hist[i].append("SIG")
            if self.scheme is not None and self.scheme.on_signal(i):
                self._resume(i, None, throw=True)
            return
        res = self.mem.step(self.ops[i])
        self.hist[i].append(res)
        self._resume(i, res)

    def key(self) -> tuple:
        return (self.mem.key(), tuple(tuple(h) for h in self.hist))

    def finish(self) -> None:
        if self.check is not None:
            self.check(self.mem, self.rets)


class Result:
    def __init__(self) -> None:
        self.violation: Optional[str] = None
        self.kind: Optional[str] = None
        self.schedule: tuple = ()
        self.states = 0
        self.finals = 0
        self.cut = 0


def _kind(e: Exception) -> str:
    return {UseAfterFree: "use-after-free", DoubleFree: "double-free", Corrupt: "corrupt"}.get(type(e), "error")


def explore(make: Callable[[], tuple], max_steps: int = 200, max_states: int = 400000) -> Result:
    """Run every interleaving of make(), depth first, with a cache of seen states.

    Stops at the first violation. A schedule longer than max_steps is cut.
    """
    r = Result()
    seen: set = set()
    stack: list = [()]
    while stack:
        sched = stack.pop()
        try:
            w = World(make)
            for i in sched:
                w.step(i)
            while True:  # go down the first child in place; replay only for the others
                if w.done():
                    w.finish()
                    r.finals += 1
                    break
                en = w.enabled()
                if not en:
                    r.violation, r.kind, r.schedule = "deadlock: no process can move", "deadlock", sched
                    return r
                if len(sched) >= max_steps:
                    r.cut += 1
                    break
                k = w.key()
                if k in seen:
                    break
                seen.add(k)
                r.states += 1
                if r.states > max_states:
                    raise RuntimeError("state space too large")
                for i in reversed(en[1:]):
                    stack.append(sched + (i,))
                sched = sched + (en[0],)
                w.step(en[0])
        except SimError as e:
            r.violation, r.kind, r.schedule = str(e), _kind(e), sched
            return r
    return r


def run_schedule(make: Callable[[], tuple], rng: random.Random, max_steps: int = 100000,
                 stall: Optional[int] = None, stall_after: int = 0) -> World:
    """One run with a random schedule. Process `stall` stops for good after stall_after steps."""
    w = World(make)
    own = 0
    while not w.done() and w.steps < max_steps:
        en = w.enabled()
        if stall is not None:
            if own >= stall_after:
                en = [i for i in en if i != stall]
            if not en and w.ops[stall] is not None and own >= stall_after:
                break
        if not en:
            raise SimError("deadlock: no process can move")
        if stall is not None and stall in en and own < stall_after:
            i = stall
        else:
            i = rng.choice(en)
        if i == stall:
            own += 1
        w.step(i)
    if w.done():
        w.finish()
    return w


def run_random(make: Callable[[], tuple], seeds: range, max_steps: int = 100000) -> Result:
    """Many seeded random schedules. Stops at the first violation."""
    r = Result()
    for s in seeds:
        try:
            run_schedule(make, random.Random(s), max_steps)
            r.finals += 1
        except SimError as e:
            r.violation, r.kind, r.schedule = str(e), _kind(e), (s,)
            return r
    return r


def run_stall(make: Callable[[], tuple], seed: int, stall_after: int) -> World:
    """Process 0 runs stall_after steps and then never again. Returns the world."""
    return run_schedule(make, random.Random(seed), stall=0, stall_after=stall_after)


# ---------------------------------------------------------------- clients


class NoReclaim:
    """The base scheme: plain reads, and retire never frees. Schemes override parts."""

    name = "none"

    def __init__(self, mem: Memory, n: int) -> None:
        self.mem, self.n = mem, n

    def restartable(self, t: int) -> bool:
        return False

    def on_signal(self, t: int) -> bool:
        """Called when t handles a signal. True means: throw Neutralized into t."""
        return self.restartable(t)

    def alloc(self, t: int, fields: dict) -> Gen:
        return (yield ("alloc", dict(fields)))

    def begin(self, t: int) -> Gen:
        return
        yield

    def attempt(self, t: int) -> Gen:
        return
        yield

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        return (yield ("read", a, f))

    def read(self, t: int, a: Any, f: str) -> Gen:
        return (yield ("read", a, f))

    def before_write(self, t: int, ptrs: list) -> Gen:
        return
        yield

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        return
        yield

    def end(self, t: int) -> Gen:
        return
        yield


class ImmediateFree(NoReclaim):
    """The naive scheme: free a node as soon as it is unlinked. Unsafe."""

    name = "immediate"

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        yield ("free", a)


def push(S: NoReclaim, t: int, v: Any) -> Gen:
    """Treiber push."""
    yield from S.begin(t)
    node = yield from S.alloc(t, {"val": v, "next": None})
    while True:
        try:
            yield from S.attempt(t)
            top = yield from S.read(t, "root", "top")
            yield ("write", node, "next", top)
            yield from S.before_write(t, [top])
            if (yield ("cas", "root", "top", top, node)):
                break
        except Restart:
            continue
    yield from S.end(t)


def pop(S: NoReclaim, t: int) -> Gen:
    """Treiber pop. Returns the value, or None on an empty stack."""
    yield from S.begin(t)
    while True:
        try:
            yield from S.attempt(t)
            top = yield from S.protect(t, 0, "root", "top")
            if top is None:
                v = None
                break
            nxt = yield from S.read(t, top, "next")
            v = yield from S.read(t, top, "val")
            yield from S.before_write(t, [top, nxt])
            if (yield ("cas", "root", "top", top, nxt)):
                yield from S.retire(t, top)
                break
        except Restart:
            continue
    yield from S.end(t)
    return v


def enq(S: NoReclaim, t: int, v: Any) -> Gen:
    """Michael and Scott enqueue."""
    yield from S.begin(t)
    node = yield from S.alloc(t, {"val": v, "next": None})
    while True:
        try:
            yield from S.attempt(t)
            tl = yield from S.protect(t, 0, "q", "tail")
            nx = yield from S.read(t, tl, "next")
            if (yield from S.read(t, "q", "tail")) != tl:
                continue
            if nx is None:
                yield from S.before_write(t, [tl, node])
                if (yield ("cas", tl, "next", None, node)):
                    yield ("cas", "q", "tail", tl, node)
                    break
            else:
                yield from S.before_write(t, [tl, nx])
                yield ("cas", "q", "tail", tl, nx)
        except Restart:
            continue
    yield from S.end(t)


def deq(S: NoReclaim, t: int) -> Gen:
    """Michael and Scott dequeue with the head re-check after the protection of next."""
    yield from S.begin(t)
    while True:
        try:
            yield from S.attempt(t)
            hd = yield from S.protect(t, 0, "q", "head")
            tl = yield from S.read(t, "q", "tail")
            nx = yield from S.protect(t, 1, hd, "next")
            if (yield from S.read(t, "q", "head")) != hd:
                continue
            if nx is None:
                v = None
                break
            if hd == tl:
                yield from S.before_write(t, [tl, nx])
                yield ("cas", "q", "tail", tl, nx)
                continue
            v = yield from S.read(t, nx, "val")
            yield from S.before_write(t, [hd, nx])
            if (yield ("cas", "q", "head", hd, nx)):
                yield from S.retire(t, hd)
                break
        except Restart:
            continue
    yield from S.end(t)
    return v


def program(S: NoReclaim, t: int, ops: list) -> Gen:
    """Run a list of operations: ("push", v), ("pop",), ("enq", v), ("deq",), ("q",) for a quiescent state."""
    out = []
    for op in ops:
        if op[0] == "push":
            yield from push(S, t, op[1])
        elif op[0] == "pop":
            out.append((yield from pop(S, t)))
        elif op[0] == "enq":
            yield from enq(S, t, op[1])
        elif op[0] == "deq":
            out.append((yield from deq(S, t)))
        elif op[0] == "q":
            yield from S.quiescent(t)  # type: ignore[attr-defined]
    return out


def stack_values(mem: Memory) -> list:
    out, a, seen = [], mem.cells["root"]["top"], set()
    while a is not None:
        if a in mem.freed or a not in mem.cells or a in seen:
            raise Corrupt(f"the stack holds the freed or bad node {a}")
        seen.add(a)
        out.append(mem.cells[a]["val"])
        a = mem.cells[a]["next"]
    return out


def queue_values(mem: Memory) -> list:
    out, a = [], mem.cells["q"]["head"]
    if a in mem.freed:
        raise Corrupt(f"the queue head {a} is freed")
    a = mem.cells[a]["next"]
    while a is not None:
        if a in mem.freed or a not in mem.cells:
            raise Corrupt(f"the queue holds the freed node {a}")
        out.append(mem.cells[a]["val"])
        a = mem.cells[a]["next"]
    return out


def conserve(pushed: list, popped: list, left: list) -> None:
    got = [v for v in popped if v is not None]
    if sorted(got + left, key=repr) != sorted(pushed, key=repr):
        raise Corrupt(f"values lost or duplicated: pushed {pushed}, popped {got}, left {left}")


def setup(scheme: Callable[[Memory, int], NoReclaim], programs: list, kind: str = "stack",
          initial: int = 2, mem: Optional[Callable[[], Memory]] = None) -> Callable[[], tuple]:
    """Build a make() for the explorer: a stack or queue with `initial` values and one program per process."""

    def make() -> tuple:
        m = mem() if mem is not None else Memory()
        n = len(programs)
        S = scheme(m, n)
        if kind == "stack":
            m.static("root", top=None)
            for j in range(initial):
                m.cells["root"]["top"] = m.new(val=("init", j), next=m.cells["root"]["top"])
        else:
            d = m.new(val=None, next=None)
            m.static("q", head=d, tail=d)
            for j in range(initial):
                a = m.new(val=("init", j), next=None)
                m.cells[m.cells["q"]["tail"]]["next"] = a
                m.cells["q"]["tail"] = a
        if hasattr(S, "setup"):
            S.setup()
        pushed = [("init", j) for j in range(initial)]
        pushed += [op[1] for p in programs for op in p if op[0] in ("push", "enq")]
        gens = [program(S, t, programs[t]) for t in range(n)]

        def check(mm: Memory, rets: list) -> None:
            left = stack_values(mm) if kind == "stack" else queue_values(mm)
            conserve(pushed, [v for r in rets for v in r], left)

        return m, gens, S, check

    return make


def workload(n: int, m: int, kind: str = "stack") -> list:
    """n programs of m operations each: process t alternates insert and remove."""
    ins, rem = ("push", "pop") if kind == "stack" else ("enq", "deq")
    return [[(ins, (t, j)) if j % 2 == 0 else (rem,) for j in range(m)] for t in range(n)]


def stall_peak(scheme: Callable[[Memory, int], NoReclaim], n: int, m: int, kind: str = "stack",
               seed: int = 1, stall_after: int = 6) -> int:
    """Process 0 stalls inside its first operation; n - 1 others run m operations each. Returns the peak garbage."""
    progs = workload(n, m, kind)
    progs[0] = [("pop",) if kind == "stack" else ("deq",)]
    w = run_stall(setup(scheme, progs, kind, initial=4), seed, stall_after)
    return w.mem.peak
