# SPDX-License-Identifier: MIT
# Shared helper of the lock-free structure pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A deterministic interleaving explorer for shared memory algorithms.

A process is a Python generator. It yields one tuple for each shared memory
step, and the explorer sends back the result of that step. Each step in
Memory.apply is atomic. Two marker tuples are not steps: ("inv", name, arg)
starts an operation and ("res", value) ends it. The explorer records them as
the history that a linearizability checker reads. An invocation is recorded
just before the first step of its operation, and a response just after the
last step, so the recorded history has the most real-time order that the
run allows.

Steps: ("read", w), ("write", w, v), ("cas", w, old, new) -> bool,
("cmpxchg", w, old, new) -> the old value, ("faa", w, d) -> the old value,
("swap", w, v) -> the old value, ("mark", w) -> the old value of a marked
pointer (ptr, bit) whose bit it sets (fetch-and-or), ("dcas", w1, w2, o1, o2,
n1, n2) -> bool, ("alloc", ((field, value), ...)) -> address, ("free", a),
and ("local",) for a step that touches no shared word (a spin or a delay).

A word is any hashable name: a string for a global variable, or
(address, field) for a field of an allocated block. The allocator can reuse
the address of a freed block (oldest freed first), which is how the ABA
problem appears. A freed block is poisoned: each later access to it is
recorded in Memory.uaf.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any, Callable, Generator, Iterable

NULL = 0
POISON = "POISON"

Proc = Generator[tuple, Any, Any]


class Memory:
    """Shared words, an allocator that can reuse addresses, and a use-after-free log."""

    def __init__(self, reuse: bool = False) -> None:
        self.words: dict[Any, Any] = {}
        self.reuse = reuse
        self.next_addr = 1
        self.free_list: deque[int] = deque()
        self.live: set[int] = set()
        self.layout: dict[int, tuple] = {}
        self.uaf: list[tuple[int, tuple]] = []

    def init(self, word: Any, value: Any) -> None:
        """Set a word before the run starts (not a step)."""
        self.words[word] = value

    def new(self, **fields: Any) -> int:
        """Allocate a block before the run starts (not a step)."""
        return self._alloc(tuple(fields.items()))

    def peek(self, word: Any) -> Any:
        """Read a word without a step. Use it only for data that never changes."""
        return self.words.get(word)

    def key(self) -> tuple:
        return (frozenset(self.words.items()), self.next_addr, tuple(self.free_list))

    def _alloc(self, fields: tuple) -> int:
        if self.reuse and self.free_list:
            addr = self.free_list.popleft()
            for f in self.layout[addr]:
                del self.words[(addr, f)]
        else:
            addr = self.next_addr
            self.next_addr += 1
        self.layout[addr] = tuple(f for f, _ in fields)
        for f, v in fields:
            self.words[(addr, f)] = v
        self.live.add(addr)
        return addr

    def _touch(self, w: Any, pid: int, op: tuple) -> None:
        if isinstance(w, tuple) and w and isinstance(w[0], int) and w[0] in self.layout:
            if w[0] not in self.live:
                self.uaf.append((pid, op))

    def apply(self, op: tuple, pid: int = -1) -> Any:
        """Do one atomic step and return its result."""
        kind = op[0]
        if kind == "local":
            return None
        if kind == "alloc":
            return self._alloc(op[1])
        if kind == "free":
            addr = op[1]
            if addr not in self.live:
                self.uaf.append((pid, op))
                return None
            self.live.discard(addr)
            for f in self.layout[addr]:
                self.words[(addr, f)] = POISON
            self.free_list.append(addr)
            return None
        if kind == "dcas":
            _, w1, w2, o1, o2, n1, n2 = op
            self._touch(w1, pid, op)
            self._touch(w2, pid, op)
            if self.words[w1] == o1 and self.words[w2] == o2:
                self.words[w1], self.words[w2] = n1, n2
                return True
            return False
        w = op[1]
        self._touch(w, pid, op)
        old = self.words[w]
        if kind == "read":
            return old
        if kind == "write":
            self.words[w] = op[2]
            return None
        if kind == "cas":
            if old == op[2]:
                self.words[w] = op[3]
                return True
            return False
        if kind == "cmpxchg":
            if old == op[2]:
                self.words[w] = op[3]
            return old
        if kind == "faa":
            self.words[w] = old + op[2]
            return old
        if kind == "swap":
            self.words[w] = op[2]
            return old
        if kind == "mark":
            self.words[w] = (old[0], True)
            return old
        raise ValueError(f"unknown step {op!r}")


def call(name: str, arg: Any, body: Proc) -> Proc:
    """Wrap one operation with its invocation and response markers."""
    yield ("inv", name, arg)
    result = yield from body
    yield ("res", result)
    return result


def program(obj: Any, ops: Iterable[tuple]) -> Proc:
    """A process that calls the operations (name, arg...) of obj in order."""
    for name, *args in ops:
        yield from call(name, tuple(args), getattr(obj, name)(*args))


class Run:
    """One run in progress: the memory, the processes and the history so far."""

    def __init__(self, setup: Callable[[], tuple[Memory, list[Proc]]]) -> None:
        self.mem, procs = setup()
        self.procs = list(procs)
        n = len(self.procs)
        self.pending: list[tuple | None] = [None] * n
        self.results: list[list[Any]] = [[] for _ in range(n)]
        self.history: list[tuple] = []
        self.trace: list[tuple] = []
        self.op_steps: list[tuple[int, str, int]] = []
        self.deferred: list[tuple | None] = [None] * n
        self.current: list[str | None] = [None] * n
        self.count = [0] * n
        for p in range(n):
            self._advance(p, None)

    def _advance(self, p: int, value: Any) -> None:
        g = self.procs[p]
        try:
            op = g.send(value)
            while op[0] in ("inv", "res"):
                if op[0] == "inv":
                    self.deferred[p] = op
                    self.current[p] = op[1]
                    self.count[p] = 0
                else:
                    self._emit_inv(p)
                    self.history.append((p, "res", op[1]))
                    self.op_steps.append((p, self.current[p] or "", self.count[p]))
                    self.current[p] = None
                op = g.send(None)
            self.pending[p] = op
        except StopIteration:
            self.pending[p] = None

    def _emit_inv(self, p: int) -> None:
        d = self.deferred[p]
        if d is not None:
            self.history.append((p, "inv", d[1], d[2]))
            self.deferred[p] = None

    def enabled(self) -> list[int]:
        return [p for p, op in enumerate(self.pending) if op is not None]

    def step(self, p: int) -> Any:
        op = self.pending[p]
        if op is None:
            raise ValueError(f"process {p} has finished")
        self._emit_inv(p)
        v = self.mem.apply(op, p)
        self.results[p].append(v)
        self.trace.append((p, op, v))
        self.count[p] += 1
        self._advance(p, v)
        return v

    def key(self) -> tuple:
        return (self.mem.key(), tuple(tuple(r) for r in self.results), tuple(self.history))

    def until(self, p: int, pred: Callable[[tuple], bool], limit: int = 1000) -> None:
        """Step p until its next step satisfies pred (that step is not taken)."""
        for _ in range(limit):
            op = self.pending[p]
            if op is None or pred(op):
                return
            self.step(p)
        raise RuntimeError("until: limit reached")

    def finish_op(self, p: int, limit: int = 1000) -> int | None:
        """Run p alone until its current operation responds. Return the steps, or None."""
        before = len(self.op_steps)
        for i in range(1, limit + 1):
            if self.pending[p] is None:
                return None
            self.step(p)
            if len(self.op_steps) > before:
                return i
        return None

    def finish(self, p: int, limit: int = 10000) -> bool:
        """Run p alone until it ends. Return False if it does not end within limit steps."""
        for _ in range(limit):
            if self.pending[p] is None:
                return True
            self.step(p)
        return self.pending[p] is None


def replay(setup: Callable[[], tuple[Memory, list[Proc]]], schedule: Iterable[int]) -> Run:
    run = Run(setup)
    for p in schedule:
        run.step(p)
    return run


class Stats:
    def __init__(self) -> None:
        self.runs = 0
        self.states = 0
        self.failure: tuple[str, list[int]] | None = None


def explore(setup: Callable[[], tuple[Memory, list[Proc]]],
            check: Callable[[Run, bool], str | None],
            max_steps: int = 200, cache: bool = True,
            check_states: Callable[[Run], str | None] | None = None) -> Stats:
    """Visit every interleaving of the processes, depth first.

    check(run, truncated) runs at the end of each run, or when the run has
    max_steps steps (then truncated is True). A state seen before (the same
    memory, the same results for each process and the same history) is not
    explored again. check_states, if given, runs in every new state. Stop at
    the first failure and keep its schedule in stats.failure.
    """
    stats = Stats()
    seen: set = set()
    stack: list[tuple[int, ...]] = [()]
    while stack:
        prefix = stack.pop()
        run = replay(setup, prefix)
        sched = list(prefix)
        while True:
            en = run.enabled()
            if not en or len(sched) >= max_steps:
                stats.runs += 1
                msg = check(run, bool(en))
                if msg:
                    stats.failure = (msg, sched)
                    return stats
                break
            if cache:
                k = run.key()
                if k in seen:
                    break
                seen.add(k)
            stats.states += 1
            if check_states is not None:
                msg = check_states(run)
                if msg:
                    stats.failure = (msg, sched)
                    return stats
            for p in reversed(en[1:]):
                stack.append(tuple(sched) + (p,))
            run.step(en[0])
            sched.append(en[0])
    return stats


def random_run(setup: Callable[[], tuple[Memory, list[Proc]]], seed: int,
               max_steps: int = 2000, crash: dict[int, int] | None = None) -> Run:
    """One run with a seeded random schedule. crash maps a process to the number
    of steps after which it stops forever."""
    rng = random.Random(seed)
    run = Run(setup)
    crash = crash or {}
    for _ in range(max_steps):
        en = [p for p in run.enabled() if p not in crash or len(run.results[p]) < crash[p]]
        if not en:
            break
        run.step(rng.choice(en))
    return run


def round_robin(setup: Callable[[], tuple[Memory, list[Proc]]], max_steps: int = 2000) -> Run:
    run = Run(setup)
    i = 0
    for _ in range(max_steps):
        en = run.enabled()
        if not en:
            break
        p = min((q for q in en if q >= i), default=en[0])
        run.step(p)
        i = p + 1
    return run
