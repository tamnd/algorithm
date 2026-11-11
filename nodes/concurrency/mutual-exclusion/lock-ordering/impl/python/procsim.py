# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-ordering/. The authors are listed in prov/QFVDF2.jsonl.

"""A deterministic simulator of concurrent processes, for small models.

Each process is a Python generator. It yields one operation (a tuple) at
each step that touches shared state or a synchronization object, and the
simulator performs that operation as one atomic step. Code between two
yields touches only local variables. A process whose pending operation
cannot run now (P on a zero semaphore, lock on a held mutex, a wait that
nobody signalled) is blocked. A state in which no process can step, but
the goal is not met, is a deadlock.

Operations:
  ("tick",)                      a step with no effect (a scheduling point)
  ("atomic", f)                  run f(sim) as one step; the result is f's value
  ("await", pred)                block until pred(sim) is true
  ("when", pred, f)              block until pred(sim), then run f(sim), in one step
  ("lock", m), ("unlock", m), ("trylock", m), ("lock_all", [m, ...])
  ("P", s), ("V", s)             semaphores, weak or FIFO (strong)
  ("wait", c), ("signal", c), ("broadcast", c)
                                 condition variables, Mesa or Hoare semantics
  ("sleep",), ("wakeup", name)   sleep and wakeup; a wakeup of a process that
                                 is not asleep is lost
  ("send", ch, x), ("recv", ch)  unbounded FIFO channels

explore() visits every reachable state once (depth first, with a cache of
states), and run() follows one schedule chosen by a function, for example
a seeded random choice. No module level state is mutable.
"""

import random
from typing import Any, Callable, Iterator, Optional

Op = tuple
Gen = Iterator[Op]


class Mutex:
    def __init__(self) -> None:
        self.owner: Optional[str] = None
        self.urgent: list[str] = []  # Hoare monitors: signallers that wait

    def key(self) -> tuple:
        return (self.owner, tuple(self.urgent))


class Semaphore:
    def __init__(self, value: int, fifo: bool) -> None:
        self.count = value
        self.fifo = fifo
        self.queue: list[str] = []
        self.granted: set[str] = set()

    def key(self) -> tuple:
        return (self.count, tuple(self.queue), tuple(sorted(self.granted)))


class Cond:
    def __init__(self, mutex: str, mode: str) -> None:
        assert mode in ("mesa", "hoare")
        self.mutex = mutex
        self.mode = mode
        self.queue: list[str] = []

    def key(self) -> tuple:
        return tuple(self.queue)


class Proc:
    def __init__(self, name: str, gen: Gen, daemon: bool) -> None:
        self.name = name
        self.gen = gen
        self.daemon = daemon
        self.op: Optional[Op] = None
        self.done = False


def _freeze(x: Any) -> Any:
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    if isinstance(x, (list, tuple)):
        return tuple(_freeze(i) for i in x)
    if isinstance(x, dict):
        return tuple(sorted((repr(k), _freeze(v)) for k, v in x.items()))
    if isinstance(x, (set, frozenset)):
        return tuple(sorted(repr(_freeze(i)) for i in x))
    if isinstance(x, Sim):
        return "sim"
    code = getattr(x, "__code__", None)
    if code is not None:
        cells = tuple(_freeze(c.cell_contents) for c in (x.__closure__ or ()))
        return ("fn", code.co_firstlineno, cells)
    return ("obj", type(x).__name__)


class Sim:
    """Shared state, synchronization objects and processes."""

    def __init__(self) -> None:
        self.v: dict[str, Any] = {}
        self.mutexes: dict[str, Mutex] = {}
        self.sems: dict[str, Semaphore] = {}
        self.conds: dict[str, Cond] = {}
        self.chans: dict[str, list] = {}
        self.procs: dict[str, Proc] = {}
        self.wakeups: set[str] = set()
        self.log: list[tuple] = []  # events for the tests; not part of the state
        self.current: Optional[str] = None
        self.steps = 0

    # set up
    def mutex(self, name: str) -> None:
        self.mutexes[name] = Mutex()

    def semaphore(self, name: str, value: int, fifo: bool = False) -> None:
        self.sems[name] = Semaphore(value, fifo)

    def cond(self, name: str, mutex: str, mode: str = "mesa") -> None:
        self.conds[name] = Cond(mutex, mode)

    def channel(self, name: str) -> None:
        self.chans[name] = []

    def spawn(self, name: str, fn: Callable[..., Gen], *args: Any, daemon: bool = False) -> None:
        p = Proc(name, fn(self, name, *args), daemon)
        self.procs[name] = p
        self._advance(p, None)

    def emit(self, *event: Any) -> None:
        """Record an event in the log (the log is not part of the state)."""
        self.log.append(event)

    # the semantics
    def _advance(self, p: Proc, result: Any) -> None:
        try:
            p.op = p.gen.send(result) if p.op is not None else next(p.gen)
        except StopIteration:
            p.op, p.done = None, True

    def _release(self, m: str) -> None:
        mx = self.mutexes[m]
        mx.owner = mx.urgent.pop() if mx.urgent else None

    def can_step(self, name: str) -> bool:
        p = self.procs[name]
        if p.done or p.op is None:
            return False
        op, k = p.op, p.op[0]
        if k == "lock" or k == "_reacquire":
            return self.mutexes[op[1]].owner is None
        if k == "lock_all":
            return all(self.mutexes[m].owner is None for m in op[1])
        if k == "P":
            s = self.sems[op[1]]
            return True if s.fifo else s.count > 0
        if k == "_granted":
            return name in self.sems[op[1]].granted
        if k == "_waiting":
            return False
        if k in ("_hoare_resume", "_urgent"):
            return self.mutexes[op[1]].owner == name
        if k in ("await", "when"):
            return bool(op[1](self))
        if k == "_asleep":
            return name in self.wakeups
        if k == "recv":
            return len(self.chans[op[1]]) > 0
        return True

    def enabled(self) -> list[str]:
        return [n for n in self.procs if self.can_step(n)]

    def step(self, name: str) -> None:
        p = self.procs[name]
        assert self.can_step(name), (name, p.op)
        self.current = name
        self.steps += 1
        op, k = p.op, p.op[0]
        result: Any = None
        if k in ("tick", "await", "_hoare_resume", "_urgent"):
            pass
        elif k == "atomic":
            result = op[1](self)
        elif k == "when":
            result = op[2](self)
        elif k == "lock" or k == "_reacquire":
            self.mutexes[op[1]].owner = name
        elif k == "lock_all":
            for m in op[1]:
                self.mutexes[m].owner = name
        elif k == "trylock":
            mx = self.mutexes[op[1]]
            result = mx.owner is None
            if result:
                mx.owner = name
        elif k == "unlock":
            assert self.mutexes[op[1]].owner == name, (name, op)
            self._release(op[1])
        elif k == "P":
            s = self.sems[op[1]]
            if s.count > 0 and not s.queue:
                s.count -= 1
            else:
                s.queue.append(name)
                p.op = ("_granted", op[1])
                return
        elif k == "_granted":
            self.sems[op[1]].granted.discard(name)
        elif k == "V":
            s = self.sems[op[1]]
            if s.fifo and s.queue:
                s.granted.add(s.queue.pop(0))
            else:
                s.count += 1
        elif k == "wait":
            c = self.conds[op[1]]
            assert self.mutexes[c.mutex].owner == name, (name, op)
            c.queue.append(name)
            self._release(c.mutex)
            p.op = ("_waiting", op[1])
            return
        elif k in ("signal", "broadcast"):
            c = self.conds[op[1]]
            assert self.mutexes[c.mutex].owner == name, (name, op)
            if c.mode == "hoare":
                assert k == "signal", "Hoare monitors have no broadcast"
                if c.queue:
                    w = c.queue.pop(0)
                    mx = self.mutexes[c.mutex]
                    mx.owner = w
                    mx.urgent.append(name)
                    self.procs[w].op = ("_hoare_resume", c.mutex)
                    p.op = ("_urgent", c.mutex)
                    return
            else:
                woken = c.queue[:1] if k == "signal" else c.queue[:]
                del c.queue[: len(woken)]
                for w in woken:
                    self.procs[w].op = ("_reacquire", c.mutex)
        elif k == "sleep":
            p.op = ("_asleep",)
            return
        elif k == "_asleep":
            self.wakeups.discard(name)
        elif k == "wakeup":
            if self.procs[op[1]].op == ("_asleep",):
                self.wakeups.add(op[1])
        elif k == "send":
            self.chans[op[1]].append(op[2])
        elif k == "recv":
            result = self.chans[op[1]].pop(0)
        else:
            raise ValueError(f"unknown operation {op!r}")
        self._advance(p, result)

    # inspection
    def key(self) -> tuple:
        procs = []
        for n in sorted(self.procs):
            p = self.procs[n]
            frames = []
            g: Any = p.gen
            while g is not None and getattr(g, "gi_frame", None) is not None:
                f = g.gi_frame
                frames.append((f.f_lasti, _freeze(dict(f.f_locals))))
                g = g.gi_yieldfrom
            procs.append((n, p.done, _freeze(p.op), tuple(frames)))
        return (
            _freeze(self.v),
            tuple((n, m.key()) for n, m in sorted(self.mutexes.items())),
            tuple((n, s.key()) for n, s in sorted(self.sems.items())),
            tuple((n, c.key()) for n, c in sorted(self.conds.items())),
            _freeze(self.chans),
            tuple(sorted(self.wakeups)),
            tuple(procs),
        )

    def all_done(self) -> bool:
        return all(p.done for p in self.procs.values() if not p.daemon)

    def blocked(self) -> list[str]:
        return [n for n, p in self.procs.items() if not p.done and not self.can_step(n)]

    def waits_for(self) -> dict[str, set[str]]:
        """Wait-for edges from blocked processes to the owners of the mutexes they need."""
        g: dict[str, set[str]] = {}
        for n in self.blocked():
            op = self.procs[n].op
            if op[0] in ("lock", "_reacquire"):
                ms = [op[1]]
            elif op[0] == "lock_all":
                ms = list(op[1])
            else:
                ms = []
            for m in ms:
                o = self.mutexes[m].owner
                if o is not None and o != n:
                    g.setdefault(n, set()).add(o)
        return g


Build = Callable[[], Sim]
Goal = Callable[[Sim], bool]
Check = Callable[[Sim], Optional[str]]


class Explored:
    def __init__(self) -> None:
        self.states = 0
        self.deadlocks: list[tuple] = []  # schedules that end in a deadlock
        self.violations: list[tuple] = []  # (schedule, message)
        self.finals = 0  # states where no process can step and the goal holds
        self.truncated = False


def explore(build: Build, goal: Optional[Goal] = None, invariant: Optional[Check] = None,
            max_states: int = 200_000, max_depth: int = 10_000, stop_at_first: bool = False) -> Explored:
    """Visit every reachable state of build() once, depth first.

    Precondition: build() returns a fresh Sim each time, and the processes
    are deterministic given the results of their operations.
    A state with no enabled process is final if goal(sim) holds (by default:
    every non-daemon process has finished) and a deadlock otherwise. The
    invariant is checked in every state; it returns an error text or None.
    A state is rebuilt by replaying its schedule from build().
    Cost: O(S * d) steps for S reachable states and schedules of length d.
    """
    goal = goal or Sim.all_done
    res = Explored()
    seen: set = set()
    stack: list[tuple] = [()]
    sim, cur = build(), ()
    while stack:
        sched = stack.pop()
        if len(sched) == len(cur) + 1 and sched[:-1] == cur:
            sim.step(sched[-1])
        elif sched != cur:
            sim = build()
            for n in sched:
                sim.step(n)
        cur = sched
        k = sim.key()
        if k in seen:
            continue
        seen.add(k)
        res.states += 1
        if invariant is not None:
            msg = invariant(sim)
            if msg:
                res.violations.append((sched, msg))
                if stop_at_first:
                    break
                continue
        en = sim.enabled()
        if not en:
            if goal(sim):
                res.finals += 1
            else:
                res.deadlocks.append(sched)
                if stop_at_first:
                    break
            continue
        if res.states >= max_states or len(sched) >= max_depth:
            res.truncated = True
            continue
        for n in reversed(en):
            stack.append(sched + (n,))
    return res


class Run:
    def __init__(self, outcome: str, schedule: list[str], sim: Sim, message: str = "") -> None:
        self.outcome = outcome  # "done", "deadlock", "violation" or "limit"
        self.schedule = schedule
        self.sim = sim
        self.message = message


def run(build: Build, choose: Callable[[Sim, list[str]], str], max_steps: int = 10_000,
        goal: Optional[Goal] = None, invariant: Optional[Check] = None) -> Run:
    """Follow one schedule: at each step choose(sim, enabled) picks the process."""
    goal = goal or Sim.all_done
    sim = build()
    sched: list[str] = []
    while True:
        if invariant is not None:
            msg = invariant(sim)
            if msg:
                return Run("violation", sched, sim, msg)
        en = sim.enabled()
        if not en:
            return Run("done" if goal(sim) else "deadlock", sched, sim)
        if len(sched) >= max_steps:
            return Run("limit", sched, sim)
        n = choose(sim, en)
        sim.step(n)
        sched.append(n)


def random_run(build: Build, seed: int, max_steps: int = 10_000, goal: Optional[Goal] = None,
               invariant: Optional[Check] = None) -> Run:
    """One run in which a random.Random(seed) picks each step."""
    rng = random.Random(seed)
    return run(build, lambda sim, en: rng.choice(en), max_steps, goal, invariant)


def replay(build: Build, schedule: list[str]) -> Sim:
    """The state after the given schedule."""
    sim = build()
    for n in schedule:
        sim.step(n)
    return sim
