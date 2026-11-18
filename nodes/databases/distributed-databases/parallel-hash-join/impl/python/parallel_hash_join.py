# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-hash-join/. The authors are listed in prov/XNDHHS.jsonl.

"""Partitioned parallel hash join on a simulated shared-nothing machine.

The machine has p nodes. Node i holds a part R_i of R and a part S_i of S,
each a dbrel.Relation in bag mode. The join is the natural join on the
common attributes; the tuples are routed by a hash of the key attributes,
which must be common attributes (by default all of them). The simulation
runs in one thread. It counts every tuple that goes from one node to a
different node, and one message for each pair of nodes (i, j) with i != j
that has at least one tuple to send from i to j. All sends happen in one
communication round. Local work is not counted in the network cost.

A NULL in a key attribute never matches, as in SQL. Such a tuple is still
routed, and the probe ignores it.
"""

from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
import zlib

from dbrel import Relation


def stable_hash(key: tuple) -> int:
    """A hash that does not change between runs (Python's str hash does)."""
    return zlib.crc32(repr(key).encode("utf-8"))


@dataclass
class Stats:
    """Network and load figures of one run."""

    tuples_sent: int = 0          # tuples that went to a node other than their home node
    messages: int = 0             # nonempty batches between two different nodes
    rounds: int = 0               # communication rounds
    received: list = field(default_factory=list)   # tuples of R and S that each node holds after the shuffle
    output: list = field(default_factory=list)     # output tuples at each node


def split_round_robin(rel: Relation, p: int) -> list[Relation]:
    """Place the tuples of rel on p nodes in turn, in sorted order (a key-blind placement)."""
    parts: list[Counter] = [Counter() for _ in range(p)]
    for i, t in enumerate(rel.sorted_rows()):
        parts[i % p][t] += 1
    return [Relation(rel.schema, c, rel.mode) for c in parts]


def _key(rel: Relation, key: Sequence[str]) -> list[int]:
    return [rel.index(a) for a in key]


def _send(t: tuple, c: int, i: int, j: int, inbox: list[Counter], stats: Stats, batches: set) -> None:
    """Move c copies of tuple t from node i to node j and count the network cost."""
    inbox[j][t] += c
    if j != i:
        stats.tuples_sent += c
        batches.add((i, j))


def parallel_hash_join(r_parts: Sequence[Relation], s_parts: Sequence[Relation],
                       key: Sequence[str] | None = None,
                       h: Callable[[tuple], int] = stable_hash) -> tuple[Relation, Stats]:
    """Join R and S, given as p parts each, by hash redistribution and local hash joins."""
    p = len(r_parts)
    if p < 1 or len(s_parts) != p:
        raise ValueError("R and S need one part on each of the same p >= 1 nodes")
    r_schema, s_schema = r_parts[0].schema, s_parts[0].schema
    common = [a for a in r_schema if a in s_schema]
    key = tuple(common if key is None else key)
    if not key or any(a not in common for a in key):
        raise ValueError("the routing key must be a nonempty set of common attributes")
    rest = [a for a in s_schema if a not in common]
    stats = Stats(rounds=1)
    batches: set = set()
    r_in: list[Counter] = [Counter() for _ in range(p)]
    s_in: list[Counter] = [Counter() for _ in range(p)]
    rk, sk = _key(r_parts[0], key), _key(s_parts[0], key)
    # Redistribution phase: one round in which every node may send to every node.
    for i in range(p):  # @line L1
        for t, c in r_parts[i].rows.items():  # @line L2
            _send(t, c, i, h(tuple(t[x] for x in rk)) % p, r_in, stats, batches)
        for u, d in s_parts[i].rows.items():  # @line L3
            _send(u, d, i, h(tuple(u[x] for x in sk)) % p, s_in, stats, batches)
    stats.messages = len(batches)
    rc, sc = [r_schema.index(a) for a in common], [s_schema.index(a) for a in common]
    rest_pos = [s_schema.index(a) for a in rest]
    out: Counter = Counter()
    for j in range(p):  # @line L4
        r_local, s_local = r_in[j], s_in[j]  # @line L5
        table: dict = {}
        for t, c in r_local.items():  # @line L6
            k = tuple(t[x] for x in rc)
            if None not in k:
                table.setdefault(k, []).append((t, c))
        made = 0
        for u, d in s_local.items():  # @line L7
            k = tuple(u[x] for x in sc)
            for t, c in table.get(k, ()):
                out[t + tuple(u[x] for x in rest_pos)] += c * d
                made += c * d
        stats.received.append(sum(r_local.values()) + sum(s_local.values()))
        stats.output.append(made)
    return Relation(r_schema + tuple(rest), out, "bag"), stats  # @line L8


def broadcast_join(r_parts: Sequence[Relation], s_parts: Sequence[Relation]) -> tuple[Relation, Stats]:
    """The fragment-and-replicate variant: every node gets all of R and joins it with its own S_i."""
    p = len(r_parts)
    if p < 1 or len(s_parts) != p:
        raise ValueError("R and S need one part on each of the same p >= 1 nodes")
    r_schema, s_schema = r_parts[0].schema, s_parts[0].schema
    common = [a for a in r_schema if a in s_schema]
    rest = [a for a in s_schema if a not in common]
    rc, sc = [r_schema.index(a) for a in common], [s_schema.index(a) for a in common]
    rest_pos = [s_schema.index(a) for a in rest]
    whole: Counter = Counter()
    for part in r_parts:
        whole.update(part.rows)
    stats = Stats(rounds=1)
    for i, part in enumerate(r_parts):
        size = sum(part.rows.values())
        stats.tuples_sent += size * (p - 1)
        if size:
            stats.messages += p - 1
    table: dict = {}
    for t, c in whole.items():
        k = tuple(t[x] for x in rc)
        if None not in k:
            table.setdefault(k, []).append((t, c))
    out: Counter = Counter()
    for j in range(p):
        made = 0
        for u, d in s_parts[j].rows.items():
            for t, c in table.get(tuple(u[x] for x in sc), ()):
                out[t + tuple(u[x] for x in rest_pos)] += c * d
                made += c * d
        stats.received.append(sum(whole.values()) + sum(s_parts[j].rows.values()))
        stats.output.append(made)
    return Relation(r_schema + tuple(rest), out, "bag"), stats
