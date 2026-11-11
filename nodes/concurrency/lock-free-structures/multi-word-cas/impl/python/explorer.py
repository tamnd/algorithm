# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-word-cas/. The authors are listed in prov/DFK374.jsonl.
"""A deterministic interleaving explorer for shared memory algorithms.

A process is a Python generator. It yields one tuple at each shared memory
step, and gets the result of the step back from the yield. Each step is
atomic. The steps are:

    ("read", a)                    -> value
    ("write", a, v)                -> None
    ("cas", a, expected, new)      -> True or False
    ("cmpxchg", a, expected, new)  -> the old value
    ("faa", a, d)                  -> the old value
    ("tas", a)                     -> the old value (0 or 1); sets a to 1
    ("swap", a, v)                 -> the old value
    ("ll", a), ("sc", a, v), ("vl", a)  load-linked, store-conditional, validate
    ("decide", a, v)               -> a one-shot consensus object: the first v wins
    ("deq", a), ("pop", a)         -> an atomic queue or stack held in a tuple

Two more tuples are not steps. They record the history for a checker:

    ("inv", name, arg)   the process invokes an operation
    ("res", value)       the operation responds
    ("lp",)              the step just taken is the linearization point

They are not scheduling points. An invocation is recorded just before the
first step of its operation, and a response just after the last step, so
each recorded interval is inside the real one, and a check of the recorded
history is never weaker than a check of the real one. A schedule is a
sequence of process ids.

A state is the memory, the program point and local variables of each
generator (read from its frame), and the return values. The exhaustive
search replays each schedule from the start, because a generator cannot be
copied, and skips a state that it has seen before.
"""

import random
import types


def freeze(x):
    """A hashable copy of x."""
    if isinstance(x, (list, tuple)):
        return tuple(freeze(i) for i in x)
    if isinstance(x, dict):
        return tuple(sorted(((freeze(k), freeze(v)) for k, v in x.items()), key=repr))
    if isinstance(x, (set, frozenset)):
        return frozenset(freeze(i) for i in x)
    if isinstance(x, types.GeneratorType):
        return "<gen>"
    if callable(x):
        return getattr(x, "__qualname__", repr(x))
    try:
        hash(x)
        return x
    except TypeError:
        return repr(x)


def proc_key(g):
    """The program point and the locals of a generator and of the ones it delegates to."""
    out = []
    while isinstance(g, types.GeneratorType):
        f = g.gi_frame
        if f is None:
            out.append(None)
            break
        out.append((g.gi_code.co_qualname, f.f_lasti, freeze(dict(f.f_locals))))
        g = g.gi_yieldfrom
    return tuple(out)


class Memory:
    """Shared memory: a map from addresses to hashable values."""

    def __init__(self, cells=None):
        self.cells = dict(cells or {})
        self.links = {}

    def get(self, a):
        return self.cells.get(a)

    def put(self, a, v):
        self.cells[a] = v
        self.links.pop(a, None)

    def apply(self, pid, op):
        k, a = op[0], op[1]
        old = self.get(a)
        if k == "read":
            return old
        if k == "write":
            self.put(a, op[2])
            return None
        if k == "cas":
            if old == op[2]:
                self.put(a, op[3])
                return True
            return False
        if k == "cmpxchg":
            if old == op[2]:
                self.put(a, op[3])
            return old
        if k == "faa":
            self.put(a, (old or 0) + op[2])
            return old or 0
        if k == "tas":
            self.put(a, 1)
            return old or 0
        if k == "swap":
            self.put(a, op[2])
            return old
        if k == "ll":
            self.links.setdefault(a, set()).add(pid)
            return old
        if k == "sc":
            if pid in self.links.get(a, ()):
                self.put(a, op[2])
                return True
            return False
        if k == "vl":
            return pid in self.links.get(a, ())
        if k == "decide":
            if old is None:
                self.put(a, op[2])
            return self.get(a)
        if k in ("deq", "pop"):
            if not old:
                return None
            if k == "deq":
                self.put(a, old[1:])
                return old[0]
            self.put(a, old[:-1])
            return old[-1]
        raise ValueError(f"unknown step {op!r}")

    def key(self):
        cells = tuple(sorted(self.cells.items(), key=repr))
        links = tuple(sorted(((a, frozenset(s)) for a, s in self.links.items() if s), key=repr))
        return cells, links


class World:
    """The memory and the processes of one run."""

    def __init__(self, setup):
        mem, procs = setup()
        self.mem = mem if isinstance(mem, Memory) else Memory(mem)
        self.gens = list(procs)
        n = len(self.gens)
        self.next = [None] * n
        self.done = [False] * n
        self.ret = [None] * n
        self.steps = [0] * n
        self.history = []
        self.trace = []
        self.waiting = [None] * n
        for p in range(n):
            self._advance(p, None)

    def _advance(self, p, value):
        g = self.gens[p]
        try:
            op = g.send(value)
            while op[0] in ("inv", "res", "lp"):
                if op[0] == "inv":
                    self.waiting[p] = ("inv", p, op[1], op[2] if len(op) > 2 else None)
                elif op[0] == "res":
                    self._flush(p)
                    self.history.append(("res", p, op[1]))
                else:
                    self.history.append(("lp", p))
                op = g.send(None)
        except StopIteration as stop:
            self.done[p], self.ret[p], self.next[p] = True, stop.value, None
            return
        self.next[p] = op

    def enabled(self):
        return [p for p in range(len(self.gens)) if not self.done[p]]

    def _flush(self, p):
        if self.waiting[p]:
            self.history.append(self.waiting[p])
            self.waiting[p] = None

    def step(self, p):
        op = self.next[p]
        self._flush(p)
        r = self.mem.apply(p, op)
        self.steps[p] += 1
        self.trace.append((p, op, r))
        self._advance(p, r)
        return r

    def key(self, history=False):
        k = (self.mem.key(), tuple(proc_key(g) for g in self.gens), freeze(self.ret))
        return k + (tuple(self.history),) if history else k


def replay(setup, schedule):
    w = World(setup)
    for p in schedule:
        w.step(p)
    return w


class Found(Exception):
    """A state that breaks the property. It holds the message and the schedule."""

    def __init__(self, msg, schedule):
        super().__init__(f"{msg} after schedule {list(schedule)}")
        self.msg, self.schedule = msg, tuple(schedule)


def explore(setup, check=None, final=None, history=False, max_depth=400, max_states=200_000):
    """Visit every reachable state once, by depth first search.

    check(world) runs at each state and final(world) at each state where all
    processes are done. Each returns None or a message; a message raises
    Found. A step back to a state on the current path (a cycle) raises
    Found, and so does a schedule longer than max_depth. So on a finite
    workload this search shows that every run ends.
    Returns the number of states and of final states.
    """
    seen = set()
    on_path = set()
    stack = [("enter", (), None)]
    states = finals = 0
    while stack:
        kind, s, k = stack.pop()
        if kind == "exit":
            on_path.discard(k)
            continue
        w = replay(setup, s)
        k = w.key(history)
        if k in on_path:
            raise Found("a cycle of states: a run can go on for ever", s)
        if k in seen:
            continue
        seen.add(k)
        states += 1
        if states > max_states:
            raise RuntimeError("too many states")
        if check and (msg := check(w)):
            raise Found(msg, s)
        en = w.enabled()
        if not en:
            finals += 1
            if final and (msg := final(w)):
                raise Found(msg, s)
            continue
        if len(s) >= max_depth:
            raise Found("a run is longer than the depth bound", s)
        on_path.add(k)
        stack.append(("exit", s, k))
        for p in reversed(en):
            stack.append(("enter", s + (p,), None))
    return states, finals


def final_histories(setup, max_depth=400, max_states=200_000):
    """The set of distinct complete histories of all runs."""
    out = set()

    def keep(w):
        out.add(tuple(w.history))

    explore(setup, final=keep, history=True, max_depth=max_depth, max_states=max_states)
    return out


def solo(w, p, bound):
    """Run p alone from the state of w. Returns (outcome, steps).

    The outcome is "done", "loop" (a state came back, so p runs forever
    alone), or "bound" (p is not done after bound steps).
    """
    seen = {w.key()}
    for i in range(1, bound + 1):
        w.step(p)
        if w.done[p]:
            return "done", i
        k = w.key()
        if k in seen:
            return "loop", i
        seen.add(k)
    return "bound", bound


def random_run(setup, seed, max_steps=10_000, crash=None):
    """Run with a seeded random scheduler. crash maps a pid to the step count
    after which it stops for ever."""
    rng = random.Random(seed)
    w = World(setup)
    crash = crash or {}
    for _ in range(max_steps):
        en = [p for p in w.enabled() if w.steps[p] < crash.get(p, float("inf"))]
        if not en:
            break
        w.step(rng.choice(en))
    return w


def run_schedule(setup, schedule_fn, max_steps=100_000):
    """Run with a scheduler function f(world) -> pid, or None to stop."""
    w = World(setup)
    for _ in range(max_steps):
        p = schedule_fn(w)
        if p is None:
            break
        w.step(p)
    return w
