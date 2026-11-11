# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flat-combining/. The authors are listed in prov/E3Q27Y.jsonl.

"""Flat combining (Hendler, Incze, Shavit and Tzafrir, SPAA 2010).

A sequential object is guarded by one lock. Each thread has a publication
record with a field slot that holds ("req", name, args) while a request is
pending and ("resp", value) once it has been served. The records of the
threads that were active lately form the publication list. A thread writes
its request into its record and puts the record into the list if it is not
in it. Then it loops: if its request has been served, it returns the
response; else, if the lock is free, it takes it and becomes the combiner.
The combiner scans the list, applies every pending request to the
sequential object, writes each response, and releases the lock.

Records are added at the head of the list with a CAS, so a thread can join
without the lock. Every `cleanup_every` combining passes, the combiner
removes records that it has not served for more than `max_age` passes; it
never removes the first record (inserts race with it at the head) or a
record with a pending request. A thread whose record was removed sees that
its flag active is false and adds the record again.

The object is a value in the shared word "data". The combiner reads it once,
applies the requests to a local copy, and writes it back before it releases
the lock; only the lock holder touches it. The object is given as a
sequential specification: seq.init and seq.apply(state, name, args) ->
(new state, result).

Flag that models a bug, for the tests:

- own_first=True: the combiner applies its own operation from its local
  copy, without looking at its record. If another combiner served it after
  it last read its record, its operation takes effect twice.
"""

from __future__ import annotations

from typing import Any, Callable

from explorer import NULL, Memory, Proc

EMPTY = "EMPTY"


class StackSeq:
    """A sequential stack: push returns None, pop returns the top or EMPTY."""

    init: tuple = ()

    def apply(self, s: tuple, name: str, args: tuple) -> tuple[tuple, Any]:
        if name == "push":
            return s + (args[0],), None
        if name == "pop":
            return (s[:-1], s[-1]) if s else (s, EMPTY)
        raise ValueError(name)


class Handle:
    """The view of the object for one thread: handle.push(x) runs op(pid, "push", (x,))."""

    def __init__(self, fc: "FlatCombining", pid: int) -> None:
        self.fc, self.pid = fc, pid

    def __getattr__(self, name: str) -> Callable[..., Proc]:
        return lambda *args: self.fc.op(self.pid, name, args)


class FlatCombining:
    def __init__(self, mem: Memory, nprocs: int, seq: Any = None, cleanup_every: int = 4,
                 max_age: int = 2, own_first: bool = False) -> None:
        self.mem, self.seq = mem, seq or StackSeq()
        self.cleanup_every, self.max_age, self.bug = cleanup_every, max_age, own_first
        mem.init("lock", 0)
        mem.init("count", 0)
        mem.init("head", NULL)
        mem.init("data", self.seq.init)
        self.recs = [mem.new(slot=None, age=0, active=False, next=NULL) for _ in range(nprocs)]

    def handle(self, pid: int) -> Handle:
        return Handle(self, pid)

    def op(self, pid: int, name: str, args: tuple) -> Proc:
        rec = self.recs[pid]
        yield ("write", (rec, "slot"), ("req", name, args))  # @line L1
        while True:
            if not (yield ("read", (rec, "active"))):  # @line L2
                yield ("write", (rec, "active"), True)  # @line L3
                while True:
                    h = yield ("read", "head")  # @line L4
                    yield ("write", (rec, "next"), h)
                    if (yield ("cas", "head", h, rec)):  # @line L5
                        break
            s = yield ("read", (rec, "slot"))  # @line L6
            if s[0] == "resp":  # @line L7
                return s[1]
            if (yield ("read", "lock")) == 0 and (yield ("cas", "lock", 0, 1)):  # @line L8
                yield from self.combine(rec, name, args)  # @line L9
                yield ("write", "lock", 0)  # @line L10

    def combine(self, own: int, name: str, args: tuple) -> Proc:
        c = (yield ("read", "count")) + 1  # @line L11
        yield ("write", "count", c)
        data = yield ("read", "data")  # @line L12
        if self.bug:
            data, v = self.seq.apply(data, name, args)
            yield ("write", (own, "slot"), ("resp", v))
        cleanup = c % self.cleanup_every == 0
        pred, r = NULL, (yield ("read", "head"))  # @line L13
        while r != NULL:  # @line L14
            s = yield ("read", (r, "slot"))  # @line L15
            nxt = yield ("read", (r, "next"))
            if s is not None and s[0] == "req":
                data, v = self.seq.apply(data, s[1], s[2])  # @line L16
                yield ("write", (r, "slot"), ("resp", v))  # @line L17
                yield ("write", (r, "age"), c)
            elif cleanup and pred != NULL and c - (yield ("read", (r, "age"))) > self.max_age:  # @line L18
                yield ("write", (pred, "next"), nxt)  # @line L19
                yield ("write", (r, "active"), False)
                r = nxt
                continue
            pred, r = r, nxt
        yield ("write", "data", data)  # @line L20

    # Not steps: for the tests, read the object when no thread runs.
    def list_records(self) -> list[int]:
        out, r = [], self.mem.peek("head")
        while r != NULL:
            out.append(r)
            r = self.mem.peek((r, "next"))
        return out

    def data(self) -> Any:
        return self.mem.peek("data")
