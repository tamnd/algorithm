# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-state-crdt/. The authors are listed in prov/QRFZEK.jsonl.

"""Delta-state CRDTs and the causal anti-entropy algorithm of Almeida, Shoker
and Baquero (Algorithm 2 of the arXiv version), in a seeded simulator.

A delta-mutator returns a small element of the state lattice; the replica
joins it into its state and keeps it in a buffer D under a sequence number.
Each replica sends to a neighbour the join of the deltas that the neighbour
has not acknowledged (a delta-interval), or its whole state when the deltas
it needs are gone. The network may lose, duplicate and reorder messages, and
replicas may crash and lose their buffers.

The simulator tracks, for analysis only, the set of updates that each state
reflects, and checks the claim of Proposition 2: every state is the join of
the states that a standard full-state CRDT reaches right after each of those
updates. It also counts the bytes that are sent and the bytes that full-state
messages would cost.
"""

import random
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Lattice:
    name: str
    bottom: Callable[[], object]
    join: Callable[[object, object], object]
    leq: Callable[[object, object], bool]
    delta_mutator: Callable[[object, int, random.Random], object]  # m^delta(X)
    decompose: Callable[[object], list]  # join-irreducible parts
    encode: Callable[[object], bytes]


def _cjoin(a: dict, b: dict) -> dict:
    return {k: max(a.get(k, 0), b.get(k, 0)) for k in a.keys() | b.keys()}


def _cleq(a: dict, b: dict) -> bool:
    return all(v <= b.get(k, 0) for k, v in a.items())


# A grow-only counter: a map from replica id to count, joined by pointwise
# max. inc^delta_i(m) = {i: m(i) + 1}, one entry instead of the whole map.
G_COUNTER = Lattice(
    "g-counter",
    dict,
    _cjoin,
    _cleq,
    lambda m, i, rng: {i: m.get(i, 0) + 1},
    lambda m: [{k: v} for k, v in m.items() if v > 0],
    lambda m: ",".join(f"{k}:{m[k]}" for k in sorted(m)).encode(),
)

# A grow-only set: add^delta(s, e) = {e}.
G_SET = Lattice(
    "g-set",
    frozenset,
    lambda a, b: a | b,
    lambda a, b: a <= b,
    lambda s, i, rng: frozenset({(i, rng.randrange(10**6))}),
    lambda s: [frozenset({x}) for x in s],
    lambda s: ",".join(f"{x[0]}.{x[1]}" for x in sorted(s)).encode(),
)


def join_all(lat: Lattice, xs: list) -> object:
    acc = lat.bottom()
    for x in xs:
        acc = lat.join(acc, x)
    return acc


def optimal_delta(lat: Lattice, a: object, b: object) -> object:
    """The smallest delta that brings b up to a join b: the join of the
    join-irreducible parts of a that are not below b."""
    return join_all(lat, [p for p in lat.decompose(a) if not lat.leq(p, b)])


@dataclass
class Node:
    x: object  # durable state X_i
    c: int = 0  # durable sequence number c_i
    deltas: dict[int, object] = field(default_factory=dict)  # volatile D_i
    origin: dict[int, int] = field(default_factory=dict)  # sender of each delta (-1: local)
    acks: dict[int, int] = field(default_factory=dict)  # volatile A_i
    hist: frozenset = frozenset()  # analysis only: updates reflected in x
    hist_at: dict[int, frozenset] = field(default_factory=dict)  # analysis: hist after k joins
    x_at: dict[int, object] = field(default_factory=dict)  # analysis: X_i^k


@dataclass
class Stats:
    states: list
    model: object  # the state of a standard CRDT that has seen every update
    invariant_ok: bool  # every state = join of post-update full states
    merging_ok: bool  # the causal delta-merging condition always held
    bytes_sent: int  # delta and ack messages, as encoded
    full_state_bytes: int  # what the same sends cost with full states
    delta_messages: int
    full_messages: int


def run(lat: Lattice, rng: random.Random, n: int, steps: int, p_loss: float = 0.2,
        p_dup: float = 0.2, p_crash: float = 0.01, p_op: float = 0.3,
        latest_only: bool = False, avoid_back_propagation: bool = False,
        remove_redundant: bool = False) -> Stats:
    """Algorithm 2. avoid_back_propagation and remove_redundant are the two
    optimizations of Enes et al. (2019): do not send a delta back to the
    replica it came from, and keep only the new part of a received delta.
    With latest_only=True the sender ignores acks and ships only its newest
    delta: a broken variant that violates the causal delta-merging condition."""
    nodes = [Node(lat.bottom()) for _ in range(n)]
    for nd in nodes:
        nd.x_at[0], nd.hist_at[0] = nd.x, nd.hist
    post: dict[int, object] = {}  # update id -> full state of its source after it
    net: list[tuple] = []
    uid = 0
    inv_ok = merge_ok = True
    sent = full = dmsg = fmsg = 0

    def joined(nd: Node, d: object, h: frozenset, origin: int) -> None:
        if remove_redundant and origin >= 0:
            d = optimal_delta(lat, d, nd.x)  # keep only what is new here
        nd.x = lat.join(nd.x, d)
        nd.deltas[nd.c] = d
        nd.origin[nd.c] = origin
        nd.c += 1
        nd.hist = nd.hist | h
        nd.x_at[nd.c], nd.hist_at[nd.c] = nd.x, nd.hist

    def check(nd: Node) -> None:
        nonlocal inv_ok
        if join_all(lat, [post[e] for e in nd.hist]) != nd.x:
            inv_ok = False

    def ship(i: int, j: int, final: bool = False) -> None:
        nonlocal sent, full, dmsg, fmsg
        src = nodes[i]
        a = src.acks.get(j, 0)
        if latest_only:
            if src.c == 0:
                return
            a, d = src.c - 1, src.deltas.get(src.c - 1, src.x)
            dmsg += 1
        elif a >= src.c:
            return  # j has acked everything: send nothing
        elif not src.deltas or min(src.deltas) > a:
            a, d = 0, src.x  # the full state is the interval from 0
            fmsg += 1
        else:
            # With avoid_back_propagation, skip the deltas that came from j:
            # j already holds them.
            d = join_all(lat, [src.deltas[k] for k in range(a, src.c)
                               if not (avoid_back_propagation and src.origin[k] == j)])
            dmsg += 1
        msg = ("delta", i, j, d, a, src.c, src.hist_at[src.c])
        sent += len(lat.encode(d)) + 8
        full += len(lat.encode(src.x)) + 8
        if final:
            deliver(msg)
        else:
            net.append(msg)

    def deliver(msg: tuple) -> None:
        nonlocal merge_ok, sent
        if msg[0] == "ack":
            _, j, i, b = msg
            nodes[i].acks[j] = max(nodes[i].acks.get(j, 0), b)
            return
        _, j, i, d, a, b, h = msg
        nd = nodes[i]
        if not lat.leq(d, nd.x):
            if not lat.leq(nodes[j].x_at[a], nd.x):
                merge_ok = False
            joined(nd, d, h, j)
        else:
            nd.hist = nd.hist | h
            nd.hist_at[nd.c] = nd.hist
        check(nd)
        sent += 8
        net.append(("ack", i, j, b))

    # Each step: maybe one update, one periodic send, up to two deliveries,
    # and maybe a garbage collection or a crash at a random node.
    for _ in range(steps):
        if rng.random() < p_op:
            i = rng.randrange(n)
            nd = nodes[i]
            uid += 1
            d = lat.delta_mutator(nd.x, i, rng)
            joined(nd, d, frozenset({uid}), -1)
            post[uid] = nd.x
        i = rng.randrange(n)
        if n > 1:
            ship(i, rng.choice([k for k in range(n) if k != i]))
        for _ in range(2):
            if net:
                k = rng.randrange(len(net))
                msg = net[k] if rng.random() < p_dup else net.pop(k)
                if rng.random() >= p_loss:
                    deliver(msg)
        nd = nodes[rng.randrange(n)]
        if nd.acks and len(nd.acks) == n - 1 and rng.random() < 0.2:
            low = min(nd.acks.values())  # garbage collect deltas acked by all
            nd.deltas = {k: v for k, v in nd.deltas.items() if k >= low}
        if rng.random() < p_crash:
            nd.deltas, nd.acks = {}, {}  # crash and recover: volatile state lost
    # A quiet period with no loss: rounds of shipping until all states agree.
    net.clear()
    for _ in range(4 * n + 4):
        for i in range(n):
            for j in range(n):
                if i != j:
                    ship(i, j, final=True)
        while net:
            deliver(net.pop(0))
        if len({lat.encode(nd.x) for nd in nodes}) == 1 and not latest_only:
            break
    model = join_all(lat, list(post.values()))
    return Stats([nd.x for nd in nodes], model, inv_ok, merge_ok, sent, full, dmsg, fmsg)


def full_mutator(lat: Lattice, x: object, i: int, rng: random.Random) -> object:
    """The mutator of the standard state-based CRDT, written directly: the
    whole new state. Used to check m(X) = X join m^delta(X)."""
    if lat is G_COUNTER:
        y = dict(x)
        y[i] = y.get(i, 0) + 1
        return y
    return x | frozenset({(i, rng.randrange(10**6))})
