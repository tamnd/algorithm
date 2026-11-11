# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/op-based-crdt/. The authors are listed in prov/G9QCWP.jsonl.

"""Operation-based CRDTs over three delivery layers, in a seeded simulator.

An operation runs in two phases. prepare runs at the source only, reads the
local state and returns an effect; effect runs at every replica, the source
first. Effects travel over a network that may duplicate and reorder messages,
and the delivery layer decides what reaches the object:

- "causal": reliable causal broadcast with vector clocks. Each effect is
  applied exactly once, and never before an effect that happened before it.
- "exactly-once": duplicates are dropped, but effects are applied in arrival
  order, which may break causality.
- "raw": every arriving message is applied, duplicates included.
"""

import random
from dataclasses import dataclass
from typing import Callable, Hashable, Protocol


class OpObject(Protocol):
    def prepare(self, rng: random.Random) -> tuple: ...
    def effect(self, op: tuple) -> None: ...
    def value(self) -> object: ...


class OpCounter:
    """add(k) has the effect v += k. All effects commute."""

    def __init__(self, i: int) -> None:
        self.v = 0

    def prepare(self, rng: random.Random) -> tuple:
        return ("add", rng.choice([1, 1, -1, 2]))

    def effect(self, op: tuple) -> None:
        self.v += op[1]

    def value(self) -> int:
        return self.v


class OpORSet:
    """Observed-remove (add-wins) set. add(e) makes a fresh tag (replica, seq).
    remove(e) sends the tags of e that the source has observed. Concurrent
    effects commute; a remove that arrives before an add it observed does not
    commute with it."""

    def __init__(self, i: int) -> None:
        self.i = i
        self.seq = 0
        self.tags: set[tuple[Hashable, tuple[int, int]]] = set()

    def prepare(self, rng: random.Random) -> tuple:
        e = rng.randrange(3)
        seen = frozenset(t for x, t in self.tags if x == e)
        if seen and rng.random() < 0.5:
            return ("rm", e, seen)
        self.seq += 1
        return ("add", e, (self.i, self.seq))

    def effect(self, op: tuple) -> None:
        if op[0] == "add":
            self.tags.add((op[1], op[2]))
        else:
            self.tags -= {(op[1], t) for t in op[2]}

    def value(self) -> frozenset:
        return frozenset(x for x, _ in self.tags)


@dataclass(frozen=True)
class Msg:
    sender: int
    vc: tuple[int, ...]  # vector clock of the effect: its causal past
    op: tuple


class Endpoint:
    """The delivery layer of one replica."""

    def __init__(self, n: int, i: int, obj: OpObject, mode: str) -> None:
        self.n, self.i, self.obj, self.mode = n, i, obj, mode
        self.clock = [0] * n  # effects applied, per sender
        self.seen: set[tuple[int, int]] = set()
        self.buffer: list[Msg] = []
        self.applied = 0

    def local(self, rng: random.Random) -> Msg:
        op = self.obj.prepare(rng)
        self.clock[self.i] += 1
        m = Msg(self.i, tuple(self.clock), op)
        self.seen.add((self.i, m.vc[self.i]))
        self._apply(m)
        return m

    def receive(self, m: Msg) -> None:
        key = (m.sender, m.vc[m.sender])
        if self.mode == "raw":
            self._apply(m)
            return
        if key in self.seen:
            return
        self.seen.add(key)
        if self.mode == "exactly-once":
            self._apply(m)
            return
        self.buffer.append(m)
        ready = True
        while ready:
            ready = False
            for b in list(self.buffer):
                j = b.sender
                if b.vc[j] == self.clock[j] + 1 and all(b.vc[k] <= self.clock[k] for k in range(self.n) if k != j):
                    self.buffer.remove(b)
                    self.clock[j] += 1
                    self._apply(b)
                    ready = True

    def _apply(self, m: Msg) -> None:
        if self.mode != "causal" and m.sender != self.i:
            # Outside causal mode the clock only records what has arrived.
            self.clock[m.sender] = max(self.clock[m.sender], m.vc[m.sender])
        self.obj.effect(m.op)
        self.applied += 1


@dataclass
class Run:
    objects: list
    ops: list[tuple]  # every prepared effect, in the order of preparation


def run(make: Callable[[int], OpObject], mode: str, rng: random.Random, n: int, steps: int,
        p_dup: float = 0.3) -> Run:
    """A random run. The network may duplicate and reorder; every message is
    delivered in the end, so the broadcast is reliable."""
    eps = [Endpoint(n, i, make(i), mode) for i in range(n)]
    net: list[tuple[int, Msg]] = []
    ops: list[tuple] = []
    for _ in range(steps):
        i = rng.randrange(n)
        if rng.random() < 0.4:
            m = eps[i].local(rng)
            ops.append(m.op)
            net.extend((j, m) for j in range(n) if j != i)
        elif net:
            k = rng.randrange(len(net))
            dst, m = net[k]
            if rng.random() >= p_dup:
                net.pop(k)
            eps[dst].receive(m)
    while net:
        dst, m = net.pop(rng.randrange(len(net)))
        eps[dst].receive(m)
    return Run([e.obj for e in eps], ops)


def or_set_model(ops: list[tuple]) -> frozenset:
    """The specification of the observed-remove set: e is in the set if some
    add of e has a tag that no remove has observed."""
    removed = {(op[1], t) for op in ops if op[0] == "rm" for t in op[2]}
    return frozenset(op[1] for op in ops if op[0] == "add" and (op[1], op[2]) not in removed)


def or_set_remove_before_add() -> tuple[frozenset, frozenset, frozenset]:
    """A constructed run over exactly-once delivery without causal order.
    Replica 0 adds x. Replica 1 receives the add and removes x. Replica 2
    receives the remove first. Returns the values at replicas 0, 1 and 2 after
    every replica has applied both effects."""
    eps = [Endpoint(3, i, OpORSet(i), "exactly-once") for i in range(3)]
    add = Msg(0, (1, 0, 0), ("add", "x", (0, 1)))
    eps[0].obj.effect(add.op)
    eps[0].seen.add((0, 1))
    eps[1].receive(add)
    rm = Msg(1, (1, 1, 0), ("rm", "x", frozenset({(0, 1)})))
    eps[1].obj.effect(rm.op)
    eps[1].seen.add((1, 1))
    eps[0].receive(rm)
    eps[2].receive(rm)  # the remove overtakes the add
    eps[2].receive(add)
    return eps[0].obj.value(), eps[1].obj.value(), eps[2].obj.value()


def same_run_with_causal_delivery() -> tuple[frozenset, frozenset, frozenset]:
    """The same messages in the same arrival order, over causal broadcast:
    replica 2 buffers the remove until the add has been applied."""
    eps = [Endpoint(3, i, OpORSet(i), "causal") for i in range(3)]
    add = Msg(0, (1, 0, 0), ("add", "x", (0, 1)))
    eps[0].clock[0] = 1
    eps[0].seen.add((0, 1))
    eps[0].obj.effect(add.op)
    eps[1].receive(add)
    rm = Msg(1, (1, 1, 0), ("rm", "x", frozenset({(0, 1)})))
    eps[1].clock[1] = 1
    eps[1].seen.add((1, 1))
    eps[1].obj.effect(rm.op)
    eps[0].receive(rm)
    eps[2].receive(rm)
    eps[2].receive(add)
    return eps[0].obj.value(), eps[1].obj.value(), eps[2].obj.value()
