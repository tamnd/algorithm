# SPDX-License-Identifier: MIT
# Shared helper of the lock-free structure pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A linearizability checker in the style of Wing and Gong, with sequential specifications.

A history is a list of events (pid, "inv", name, arg) and (pid, "res", value),
as the explorer records them. The checker searches for an order of the
operations that respects real time (an operation that responds before
another one is invoked comes first) and that the sequential specification
accepts. An operation with no response (pending) may be put in the order with
any result, or left out. Visited pairs (set of placed operations, spec state)
are cached, as in the algorithm of Lowe.

A specification has a hashable `init` state and a method
`step(state, name, arg)` that returns the list of allowed (new state, result)
pairs. A list with more than one pair is a nondeterministic specification.
"""

from __future__ import annotations

from typing import Any, Callable

EMPTY = "EMPTY"
FULL = "FULL"
ABORT = "ABORT"


class Op:
    __slots__ = ("id", "pid", "name", "arg", "result", "inv", "res")

    def __init__(self, i: int, pid: int, name: str, arg: Any, inv: int) -> None:
        self.id, self.pid, self.name, self.arg, self.inv = i, pid, name, arg, inv
        self.result: Any = None
        self.res: int | None = None

    def __repr__(self) -> str:
        r = "pending" if self.res is None else repr(self.result)
        return f"p{self.pid}:{self.name}{self.arg}->{r}"


def operations(history: list[tuple]) -> list[Op]:
    ops: list[Op] = []
    open_op: dict[int, Op] = {}
    for t, ev in enumerate(history):
        if ev[1] == "inv":
            o = Op(len(ops), ev[0], ev[2], ev[3], t)
            ops.append(o)
            open_op[ev[0]] = o
        else:
            o = open_op.pop(ev[0])
            o.result, o.res = ev[2], t
    return ops


def linearize(history: list[tuple], spec: Any) -> list[Op] | None:
    """Return a legal order of the operations, or None if the history is not linearizable."""
    ops = operations(history)
    complete = [o for o in ops if o.res is not None]
    seen: set = set()
    stack: list[tuple[frozenset, Any, tuple]] = [(frozenset(), spec.init, ())]
    while stack:
        done, state, order = stack.pop()
        rest = [o.res for o in complete if o.id not in done]
        if not rest:
            return [ops[i] for i in order]
        if (done, state) in seen:
            continue
        seen.add((done, state))
        bound = min(rest)
        for o in ops:
            if o.id in done or o.inv > bound:
                continue
            for nxt, r in spec.step(state, o.name, o.arg):
                if o.res is None or r == o.result:
                    stack.append((done | {o.id}, nxt, order + (o.id,)))
    return None


def lin_check(spec: Any) -> Callable[..., str | None]:
    """A check function for explorer.explore: fail when the history is not linearizable."""

    def check(run: Any, truncated: bool = False) -> str | None:
        if linearize(run.history, spec) is None:
            return "not linearizable: " + repr(operations(run.history))
        return None

    return check


class StackSpec:
    init: tuple = ()

    def step(self, s: tuple, name: str, arg: tuple) -> list[tuple[tuple, Any]]:
        if name == "push":
            return [(s + (arg[0],), None)]
        if name == "pop":
            return [(s[:-1], s[-1])] if s else [(s, EMPTY)]
        raise ValueError(name)


class QueueSpec:
    """FIFO queue. With a capacity, enq returns FULL on a full queue. With
    spurious=True, enq may return FULL and deq may return EMPTY at any time,
    with no effect (the try semantics of some bounded queues)."""

    init: tuple = ()

    def __init__(self, capacity: int | None = None, spurious: bool = False) -> None:
        self.capacity, self.spurious = capacity, spurious

    def step(self, s: tuple, name: str, arg: tuple) -> list[tuple[tuple, Any]]:
        out: list[tuple[tuple, Any]] = []
        if name == "enq":
            if self.capacity is not None and len(s) >= self.capacity:
                return [(s, FULL)]
            out.append((s + (arg[0],), True))
            if self.spurious:
                out.append((s, FULL))
            return out
        if name == "deq":
            if not s:
                return [(s, EMPTY)]
            out.append((s[1:], s[0]))
            if self.spurious:
                out.append((s, EMPTY))
            return out
        raise ValueError(name)


class SetSpec:
    init: frozenset = frozenset()

    def step(self, s: frozenset, name: str, arg: tuple) -> list[tuple[frozenset, Any]]:
        k = arg[0]
        if name in ("insert", "add"):
            return [(s, False)] if k in s else [(s | {k}, True)]
        if name in ("delete", "remove"):
            return [(s - {k}, True)] if k in s else [(s, False)]
        if name in ("contains", "find"):
            return [(s, k in s)]
        raise ValueError(name)


class PQSpec:
    """Priority queue of distinct keys: insert returns False for a key already present."""

    init: frozenset = frozenset()

    def step(self, s: frozenset, name: str, arg: tuple) -> list[tuple[frozenset, Any]]:
        if name == "insert":
            k = arg[0]
            return [(s, False)] if k in s else [(s | {k}, True)]
        if name == "delete_min":
            if not s:
                return [(s, EMPTY)]
            m = min(s)
            return [(s - {m}, m)]
        raise ValueError(name)


class WorkStealingDequeSpec:
    """The owner pushes and pops at the bottom (the end of the tuple); thieves
    steal at the top (the start). A steal may return ABORT with no effect."""

    init: tuple = ()

    def __init__(self, abort: bool = True) -> None:
        self.abort = abort

    def step(self, s: tuple, name: str, arg: tuple) -> list[tuple[tuple, Any]]:
        if name == "push":
            return [(s + (arg[0],), None)]
        if name == "pop":
            return [(s[:-1], s[-1])] if s else [(s, EMPTY)]
        if name == "steal":
            out: list[tuple[tuple, Any]] = [(s[1:], s[0])] if s else [(s, EMPTY)]
            if self.abort:
                out.append((s, ABORT))
            return out
        raise ValueError(name)


class CounterSpec:
    """A shared counter: inc returns the old value and adds one."""

    init = 0

    def step(self, s: int, name: str, arg: tuple) -> list[tuple[int, Any]]:
        if name == "inc":
            return [(s + 1, s)]
        raise ValueError(name)
