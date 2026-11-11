# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crdt-convergence-theorem/. The authors are listed in prov/TXVMWX.jsonl.

"""A seeded replication simulator for the two convergence theorems of CRDTs.

State-based part (Theorem 1 of Shapiro et al. 2011). Replicas apply updates
locally and send copies of their whole state. The network may lose, duplicate
and reorder copies. The simulator tracks the causal history of every replica
(the set of update ids it has seen) and checks strong convergence: two
replicas with the same history have equivalent states. It also checks the
invariant of the proof: the state of a replica is the join of the states
right after each update in its history.

Op-based part (Theorem 2). Replicas broadcast operations. A causal broadcast
layer with vector clocks buffers an operation until all operations that
happened before it have been delivered; it delivers each operation exactly
once. With it, op-based objects whose concurrent operations commute
converge.
"""

import random
from dataclasses import dataclass, field
from typing import Callable, Generic, Hashable, TypeVar

S = TypeVar("S")


# State-based objects --------------------------------------------------------

@dataclass(frozen=True)
class StateCRDT(Generic[S]):
    """(bottom, update, merge, query). update(state, replica, arg) returns the new state."""

    name: str
    bottom: Callable[[int], S]
    update: Callable[[S, int, object], S]
    merge: Callable[[S, S], S]
    query: Callable[[S], object]
    gen_arg: Callable[[random.Random], object]


G_COUNTER: StateCRDT = StateCRDT(
    "g-counter",
    lambda n: tuple([0] * n),
    lambda s, i, _: tuple(v + 1 if j == i else v for j, v in enumerate(s)),
    lambda a, b: tuple(max(x, y) for x, y in zip(a, b)),
    lambda s: sum(s),
    lambda rng: None,
)

G_SET: StateCRDT = StateCRDT(
    "g-set",
    lambda n: frozenset(),
    lambda s, i, x: s | {x},
    lambda a, b: a | b,
    lambda s: s,
    lambda rng: rng.randrange(6),
)

# Not a CRDT: a register that keeps the last state it received. Its merge is
# not commutative, so replicas can end in different states.
LAST_ARRIVAL: StateCRDT = StateCRDT(
    "last-arrival register",
    lambda n: 0,
    lambda s, i, x: x,
    lambda a, b: b,
    lambda s: s,
    lambda rng: rng.randrange(1, 100),
)

# Not a CRDT: a vector counter merged by pointwise addition. The merge is
# commutative and associative but not idempotent, so a duplicate counts twice.
SUM_MERGE: StateCRDT = StateCRDT(
    "sum-merge counter",
    lambda n: tuple([0] * n),
    lambda s, i, _: tuple(v + 1 if j == i else v for j, v in enumerate(s)),
    lambda a, b: tuple(x + y for x, y in zip(a, b)),
    lambda s: sum(s),
    lambda rng: None,
)

# Not a CRDT: a set merged by union whose remove deletes the element. The
# states form a semilattice, but remove is not inflationary.
REMOVE_SET: StateCRDT = StateCRDT(
    "union set with a deleting remove",
    lambda n: frozenset(),
    lambda s, i, x: s | {x[1]} if x[0] == "add" else s - {x[1]},
    lambda a, b: a | b,
    lambda s: s,
    lambda rng: (rng.choice(["add", "rm"]), rng.randrange(3)),
)


@dataclass
class StateRun:
    states: list
    histories: list[frozenset]
    converged_pairs_ok: bool
    invariant_ok: bool


def run_state_based(obj: StateCRDT, rng: random.Random, n: int, steps: int,
                    p_loss: float = 0.2, p_dup: float = 0.3) -> StateRun:
    states = [obj.bottom(n) for _ in range(n)]
    hist: list[frozenset] = [frozenset() for _ in range(n)]
    after: dict[int, object] = {}  # update id -> source state right after it
    net: list[tuple[int, object, frozenset]] = []
    uid = 0
    pairs_ok = True
    inv_ok = True

    def check() -> None:
        nonlocal pairs_ok, inv_ok
        for i in range(n):
            for j in range(i + 1, n):
                if hist[i] == hist[j] and states[i] != states[j]:
                    pairs_ok = False
            acc = obj.bottom(n)
            for e in sorted(hist[i]):
                acc = obj.merge(acc, after[e])
            if acc != states[i]:
                inv_ok = False

    for _ in range(steps):
        a = rng.random()
        i = rng.randrange(n)
        if a < 0.3:
            uid += 1
            states[i] = obj.update(states[i], i, obj.gen_arg(rng))
            hist[i] = hist[i] | {uid}
            after[uid] = states[i]
        elif a < 0.65:
            net.append((rng.randrange(n), states[i], hist[i]))
        elif net:
            k = rng.randrange(len(net))  # any message: reordering
            dst, st, h = net[k]
            if rng.random() >= p_dup:
                net.pop(k)  # otherwise it stays and may be delivered again
            if rng.random() >= p_loss:
                states[dst] = obj.merge(states[dst], st)
                hist[dst] = hist[dst] | h
        check()
    # Eventual delivery: each replica sends its state to each other one, in
    # a random order, until all histories are equal.
    while len(set(hist)) > 1:
        i, j = rng.randrange(n), rng.randrange(n)
        states[j] = obj.merge(states[j], states[i])
        hist[j] = hist[j] | hist[i]
        check()
    return StateRun(states, hist, pairs_ok, inv_ok)


# Causal broadcast and op-based objects ---------------------------------------

@dataclass(frozen=True)
class OpMsg:
    sender: int
    vc: tuple[int, ...]
    op: tuple


class CausalReplica:
    """Delivers a message from j with vector clock V when V[j] = D[j] + 1 and
    V[k] <= D[k] for k != j, where D counts the delivered messages per sender."""

    def __init__(self, n: int, i: int, apply: Callable[[tuple], None]) -> None:
        self.n, self.i = n, i
        self.delivered = [0] * n
        self.buffer: list[OpMsg] = []
        self.seen: set[tuple[int, int]] = set()
        self.apply = apply
        self.log: list[tuple[int, int]] = []  # delivered (sender, seq) in order

    def broadcast(self, op: tuple) -> OpMsg:
        self.delivered[self.i] += 1
        vc = tuple(self.delivered)
        self.apply(op)
        self.log.append((self.i, vc[self.i]))
        self.seen.add((self.i, vc[self.i]))
        return OpMsg(self.i, vc, op)

    def receive(self, m: OpMsg) -> None:
        key = (m.sender, m.vc[m.sender])
        if key in self.seen:
            return  # a duplicate
        self.seen.add(key)
        self.buffer.append(m)
        progress = True
        while progress:
            progress = False
            for b in list(self.buffer):
                j = b.sender
                if b.vc[j] == self.delivered[j] + 1 and all(b.vc[k] <= self.delivered[k] for k in range(self.n) if k != j):
                    self.buffer.remove(b)
                    self.delivered[j] += 1
                    self.apply(b.op)
                    self.log.append((j, b.vc[j]))
                    progress = True


class OpCounter:
    """inc and dec commute with each other, so any delivery order works."""

    def __init__(self) -> None:
        self.v = 0

    def prepare(self, rng: random.Random) -> tuple:
        return ("add", rng.choice([1, -1]))

    def effect(self, op: tuple) -> None:
        self.v += op[1]

    def value(self) -> int:
        return self.v


class OpORSet:
    """Observed-remove set. add(e) creates a unique tag; remove(e) sends the tags
    of e that the source has observed. Concurrent add and remove commute; a remove
    applied before the add it observed does not."""

    def __init__(self, i: int) -> None:
        self.i = i
        self.tags: set[tuple[Hashable, tuple[int, int]]] = set()
        self.counter = 0

    def prepare(self, rng: random.Random) -> tuple:
        e = rng.randrange(3)
        present = [t for t in self.tags if t[0] == e]
        if present and rng.random() < 0.5:
            return ("rm", e, frozenset(t[1] for t in present))
        self.counter += 1
        return ("add", e, (self.i, self.counter))

    def effect(self, op: tuple) -> None:
        if op[0] == "add":
            self.tags.add((op[1], op[2]))
        else:
            self.tags -= {(op[1], t) for t in op[2]}

    def value(self) -> frozenset:
        return frozenset(e for e, _ in self.tags)


class OpRegister:
    """A plain register: set(v) overwrites. Two concurrent sets do not commute."""

    def __init__(self) -> None:
        self.v: object = None

    def effect(self, op: tuple) -> None:
        self.v = op[1]

    def value(self) -> object:
        return self.v


def or_set_without_causal_delivery() -> tuple[frozenset, frozenset]:
    """A constructed run. Replica 0 adds x; replica 1 receives the add and then
    removes x. Replica 2 receives the remove first and the add second, which a
    network without causal order allows. Replicas 0 and 2 apply the same two
    operations, and end with different values."""
    r = [OpORSet(i) for i in range(3)]
    add = ("add", "x", (0, 1))
    r[0].effect(add)
    r[1].effect(add)
    rm = ("rm", "x", frozenset({(0, 1)}))
    r[1].effect(rm)
    r[0].effect(rm)
    r[2].effect(rm)  # the remove arrives before the add it observed
    r[2].effect(add)
    return r[0].value(), r[2].value()


def run_op_based(make: Callable[[int], object], rng: random.Random, n: int, steps: int,
                 p_dup: float = 0.3) -> list:
    """Op-based run over causal broadcast on a duplicating, reordering network.
    Every message is delivered in the end (reliable broadcast)."""
    objs = [make(i) for i in range(n)]
    reps = [CausalReplica(n, i, objs[i].effect) for i in range(n)]
    net: list[tuple[int, OpMsg]] = []
    for _ in range(steps):
        i = rng.randrange(n)
        if rng.random() < 0.4:
            m = reps[i].broadcast(objs[i].prepare(rng))
            net.extend((j, m) for j in range(n) if j != i)
        elif net:
            k = rng.randrange(len(net))
            dst, m = net[k]
            if rng.random() >= p_dup:
                net.pop(k)
            reps[dst].receive(m)
        _check_equal_logs_equal_states(reps, objs)
    while net:
        dst, m = net.pop(rng.randrange(len(net)))
        reps[dst].receive(m)
        _check_equal_logs_equal_states(reps, objs)
    return objs


def _check_equal_logs_equal_states(reps: list[CausalReplica], objs: list) -> None:
    for a in range(len(reps)):
        for b in range(a + 1, len(reps)):
            if set(reps[a].log) == set(reps[b].log):
                assert objs[a].value() == objs[b].value()
