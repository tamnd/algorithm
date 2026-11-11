# SPDX-License-Identifier: MIT
# Shared helper of the transactional memory pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A deterministic simulator and checkers for word-based software transactional memory.

Memory is a dict of words. A process is a Python generator that yields one
tuple for each shared memory step, and the scheduler sends back the result of
that step. Each step is atomic:

    ("read", a)              -> the value of word a
    ("write", a, v)          -> None
    ("cas", a, old, new)     -> True if a held old (then a := new), else False
    ("faa", a, d)            -> the old value of a (then a := a + d)
    ("ll", a)                -> the value of a, and a link of this process on a
    ("sc", a, v)             -> True if no write hit a since this process's ll(a)
    ("await", a, test, arg)  -> the value of a; the step is enabled only when
                                AWAIT[test](value, arg) holds (a spin loop in one step)
    ("local",)               -> None; a step that touches no shared word

A tuple ("ev", tid, kind, ...) is not a step. It records an event of the
transaction tid in the history: "begin", "read" a v, "write" a v, "tryc"
(the commit has started), "commit" and "abort". A "begin" is recorded just
before the first later step or event of its process, so the history has the
most real-time order that the run allows.

The checkers read a history and look for one serial order of transactions
(brute force with memoization):
    opaque(h, init)              every transaction, aborted ones included,
                                 reads the values of one serial order that
                                 respects real-time order (opacity)
    strictly_serializable(h, init)  the same for the committed transactions only
    serializable(h, init)        committed only, any order
"""

from __future__ import annotations

import random
from typing import Any, Callable, Generator, Iterable

Proc = Generator[tuple, Any, Any]
Setup = Callable[[], tuple["Memory", list[Proc]]]

AWAIT = {
    "even": lambda v, x: v % 2 == 0,
    "eq": lambda v, x: v == x,
    "ne": lambda v, x: v != x,
    "free": lambda v, x: v[1] is None,
}


class Abort(Exception):
    """Raised inside a transaction attempt when the STM decides to abort it."""


class Memory:
    """The shared words. apply() performs one atomic step."""

    def __init__(self, init: dict) -> None:
        self.w = dict(init)
        self.ver: dict = {}
        self.links: dict = {}

    def _set(self, a: Any, v: Any) -> None:
        if a not in self.w:
            raise KeyError(a)
        self.w[a] = v
        self.ver[a] = self.ver.get(a, 0) + 1

    def enabled(self, op: tuple) -> bool:
        return op[0] != "await" or AWAIT[op[2]](self.w[op[1]], op[3])

    def apply(self, op: tuple, p: int) -> Any:
        k = op[0]
        if k in ("read", "await"):
            return self.w[op[1]]
        if k == "write":
            self._set(op[1], op[2])
            return None
        if k == "cas":
            if self.w[op[1]] == op[2]:
                self._set(op[1], op[3])
                return True
            return False
        if k == "faa":
            old = self.w[op[1]]
            self._set(op[1], old + op[2])
            return old
        if k == "ll":
            self.links[(p, op[1])] = self.ver.get(op[1], 0)
            return self.w[op[1]]
        if k == "sc":
            seen = self.links.pop((p, op[1]), None)
            if seen is not None and seen == self.ver.get(op[1], 0):
                self._set(op[1], op[2])
                return True
            return False
        if k == "local":
            return None
        raise ValueError(f"unknown step {op!r}")

    def key(self) -> tuple:
        live = frozenset((pa, c == self.ver.get(pa[1], 0)) for pa, c in self.links.items())
        return (frozenset(self.w.items()), live)


class Run:
    """One run in progress: the memory, the processes and the history so far."""

    def __init__(self, setup: Setup) -> None:
        self.mem, procs = setup()
        self.procs = list(procs)
        n = len(self.procs)
        self.pending: list[tuple | None] = [None] * n
        self.results: list[list[Any]] = [[] for _ in range(n)]
        self.out: list[Any] = [None] * n
        self.history: list[tuple] = []
        self.deferred: list[tuple | None] = [None] * n
        self.trace: list[tuple] = []
        for p in range(n):
            self._advance(p, None)

    def _flush(self, p: int) -> None:
        if self.deferred[p] is not None:
            self.history.append(self.deferred[p])
            self.deferred[p] = None

    def _advance(self, p: int, value: Any) -> None:
        g = self.procs[p]
        try:
            op = g.send(value)
            while op[0] == "ev":
                self._flush(p)
                if op[2] == "begin":
                    self.deferred[p] = op[1:]
                else:
                    self.history.append(op[1:])
                op = g.send(None)
            self.pending[p] = op
        except StopIteration as stop:
            self.pending[p] = None
            self.out[p] = stop.value

    def enabled(self) -> list[int]:
        return [p for p, op in enumerate(self.pending) if op is not None and self.mem.enabled(op)]

    def blocked(self) -> list[int]:
        return [p for p, op in enumerate(self.pending) if op is not None and not self.mem.enabled(op)]

    def step(self, p: int) -> Any:
        op = self.pending[p]
        if op is None or not self.mem.enabled(op):
            raise ValueError(f"process {p} cannot take a step")
        self._flush(p)
        v = self.mem.apply(op, p)
        self.results[p].append(v)
        self.trace.append((p, op, v))
        self._advance(p, v)
        return v

    def key(self) -> tuple:
        return (self.mem.key(), tuple(tuple(r) for r in self.results), tuple(self.history), tuple(self.deferred))

    def finish(self, p: int, limit: int = 10000) -> bool:
        """Run p alone until it ends. Return False if it is blocked or needs more than limit steps."""
        for _ in range(limit):
            if self.pending[p] is None:
                return True
            if not self.mem.enabled(self.pending[p]):
                return False
            self.step(p)
        return self.pending[p] is None

    def steps(self, p: int, k: int) -> None:
        for _ in range(k):
            self.step(p)


class Stats:
    def __init__(self) -> None:
        self.runs = 0
        self.states = 0
        self.failure: tuple[str, list[int]] | None = None


def replay(setup: Setup, schedule: Iterable[int]) -> Run:
    run = Run(setup)
    for p in schedule:
        run.step(p)
    return run


def explore(setup: Setup, check: Callable[[Run, bool], str | None], max_steps: int = 200,
            cache: bool = True) -> Stats:
    """Visit every interleaving depth first, with state caching.

    check(run, truncated) runs at the end of each run (no process can step),
    or when the run reaches max_steps steps (truncated is True). A state seen
    before (the same memory, the same step results of each process and the
    same history) is not explored again. Stop at the first failure.
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
            for p in reversed(en[1:]):
                stack.append(tuple(sched) + (p,))
            run.step(en[0])
            sched.append(en[0])
    return stats


def random_run(setup: Setup, seed: int, max_steps: int = 5000, crash: dict[int, int] | None = None) -> Run:
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


# ---------------------------------------------------------------- transactions


class Tx:
    """One attempt of a transaction. The STM keeps its private state in the attributes."""

    def __init__(self, stm: Any, tid: tuple) -> None:
        self.stm = stm
        self.tid = tid

    def read(self, a: Any) -> Proc:
        v = yield from self.stm.read(self, a)
        yield ("ev", self.tid, "read", a, v)
        return v

    def write(self, a: Any, v: Any) -> Proc:
        yield from self.stm.write(self, a, v)
        yield ("ev", self.tid, "write", a, v)


def atomically(stm: Any, p: int, body: Callable[[Tx], Proc], tries: int | None = None,
               read_only: bool = False) -> Proc:
    """Run body as a transaction of process p. Retry after each abort, at most
    tries attempts. Return the result of body, or None if every attempt aborted.

    An STM has the generators begin(tx), read(tx, a), write(tx, a, v),
    commit(tx) and rollback(tx). read, write and commit raise Abort.
    """
    serial = stm.__dict__.setdefault("_serial", {})
    k = 0
    while tries is None or k < tries:
        tx = Tx(stm, (p, serial.get(p, 0)))
        serial[p] = tx.tid[1] + 1
        tx.read_only = read_only
        k += 1
        yield ("ev", tx.tid, "begin")
        try:
            yield from stm.begin(tx)
            result = yield from body(tx)
            yield ("ev", tx.tid, "tryc")
            yield from stm.commit(tx)
        except Abort:
            yield from stm.rollback(tx)
            yield ("ev", tx.tid, "abort")
            continue
        yield ("ev", tx.tid, "commit")
        return result
    return None


def nothing() -> Proc:
    """An empty generator, for STM operations that take no shared step."""
    return
    yield


# ---------------------------------------------------------------- checkers


def transactions(history: list[tuple]) -> dict:
    """Group the events by transaction: begin and end positions, operations and status."""
    txs: dict = {}
    for i, ev in enumerate(history):
        tid, kind = ev[0], ev[1]
        t = txs.setdefault(tid, {"begin": i, "end": None, "ops": [], "status": "live"})
        if kind in ("read", "write"):
            t["ops"].append((kind, ev[2], ev[3]))
        elif kind == "tryc":
            t["status"] = "pending"
        elif kind in ("commit", "abort"):
            t["status"] = kind
            t["end"] = i
    return txs


def _legal(t: dict, state: dict) -> dict | None:
    """The writes of t if each read of t returns its own last write or the value in state."""
    local: dict = {}
    for kind, a, v in t["ops"]:
        if kind == "write":
            local[a] = v
        elif (local[a] if a in local else state.get(a)) != v:
            return None
    return local


def find_order(history: list[tuple], init: dict, committed_only: bool = False,
               real_time: bool = True) -> list[tuple] | None:
    """Search one legal serial order. Return a list of (tid, committed) or None.

    A live transaction is completed as aborted. A commit-pending transaction
    (tryc with no end) may be completed either way.
    """
    txs = transactions(history)
    ids = [tid for tid, t in txs.items() if not committed_only or t["status"] == "commit"]
    preds = {}
    for T in ids:
        b = txs[T]["begin"]
        preds[T] = frozenset(U for U in ids if real_time and txs[U]["end"] is not None and txs[U]["end"] < b)
    failed: set = set()
    order: list[tuple] = []

    def dfs(placed: frozenset, state: dict) -> bool:
        if len(placed) == len(ids):
            return True
        key = (placed, frozenset(state.items()))
        if key in failed:
            return False
        for T in ids:
            if T in placed or not preds[T] <= placed:
                continue
            t = txs[T]
            local = _legal(t, state)
            if local is None:
                continue
            outs = {"commit": (True,), "pending": (True, False)}.get(t["status"], (False,))
            for c in outs:
                order.append((T, c))
                if dfs(placed | {T}, {**state, **local} if c else state):
                    return True
                order.pop()
        failed.add(key)
        return False

    return list(order) if dfs(frozenset(), dict(init)) else None


def opaque(history: list[tuple], init: dict) -> bool:
    return find_order(history, init) is not None


def strictly_serializable(history: list[tuple], init: dict) -> bool:
    return find_order(history, init, committed_only=True) is not None


def serializable(history: list[tuple], init: dict) -> bool:
    return find_order(history, init, committed_only=True, real_time=False) is not None


def count(history: list[tuple], kind: str) -> int:
    return sum(1 for ev in history if ev[1] == kind)


# ---------------------------------------------------------------- workloads


def bank(m: int, amount: int) -> dict:
    return {f"a{i}": amount for i in range(m)}


def transfer(i: int, j: int, amt: int) -> Callable[[Tx], Proc]:
    def body(tx: Tx) -> Proc:
        x = yield from tx.read(f"a{i}")
        y = yield from tx.read(f"a{j}")
        yield from tx.write(f"a{i}", x - amt)
        yield from tx.write(f"a{j}", y + amt)
    return body


def audit(m: int) -> Callable[[Tx], Proc]:
    def body(tx: Tx) -> Proc:
        s = 0
        for i in range(m):
            s += yield from tx.read(f"a{i}")
        return s
    return body


def read_sums(history: list[tuple], m: int) -> list[int]:
    """The sum that each attempt (committed or not) saw, for attempts that read all m accounts."""
    out = []
    for t in transactions(history).values():
        seen = {a: v for kind, a, v in t["ops"] if kind == "read"}
        if len(seen) == m and not any(kind == "write" for kind, _, _ in t["ops"]):
            out.append(sum(seen.values()))
    return out


INF = 10 ** 9


def sorted_list(keys: Iterable[int], spare: int) -> dict:
    """Words of a sorted linked list: node 0 is the head sentinel, node 1 the tail
    sentinel (key INF), then one node per key, then spare nodes for inserts."""
    keys = sorted(keys)
    w = {("key", 0): -INF, ("key", 1): INF, ("next", 1): None}
    ids = list(range(2, 2 + len(keys)))
    chain = [0] + ids + [1]
    for a, b in zip(chain, chain[1:]):
        w[("next", a)] = b
    for k, node in zip(keys, ids):
        w[("key", node)] = k
    for node in range(2 + len(keys), 2 + len(keys) + spare):
        w[("key", node)] = None
        w[("next", node)] = None
    return w


def list_find(tx: Tx, k: int) -> Proc:
    """Return (pred, cur, key of cur) with key(pred) < k <= key(cur)."""
    pred = 0
    cur = yield from tx.read(("next", 0))
    ck = yield from tx.read(("key", cur))
    while ck < k:
        pred = cur
        cur = yield from tx.read(("next", cur))
        ck = yield from tx.read(("key", cur))
    return pred, cur, ck


def list_insert(k: int, node: int) -> Callable[[Tx], Proc]:
    def body(tx: Tx) -> Proc:
        pred, cur, ck = yield from list_find(tx, k)
        if ck == k:
            return False
        yield from tx.write(("key", node), k)
        yield from tx.write(("next", node), cur)
        yield from tx.write(("next", pred), node)
        return True
    return body


def list_remove(k: int) -> Callable[[Tx], Proc]:
    def body(tx: Tx) -> Proc:
        pred, cur, ck = yield from list_find(tx, k)
        if ck != k:
            return False
        nxt = yield from tx.read(("next", cur))
        yield from tx.write(("next", pred), nxt)
        return True
    return body


def list_contains(k: int) -> Callable[[Tx], Proc]:
    def body(tx: Tx) -> Proc:
        _, _, ck = yield from list_find(tx, k)
        return ck == k
    return body


def list_keys(words: dict) -> list:
    """The keys on the list from the head, in order. Raise if the chain is broken."""
    out, cur, seen = [], words[("next", 0)], set()
    while cur != 1:
        if cur in seen or cur is None:
            raise ValueError("broken list")
        seen.add(cur)
        out.append(words[("key", cur)])
        cur = words[("next", cur)]
    return out
