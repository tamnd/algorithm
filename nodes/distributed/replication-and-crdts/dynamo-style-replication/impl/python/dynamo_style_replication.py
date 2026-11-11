# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamo-style-replication/. The authors are listed in prov/4YS13H.jsonl.

"""A small model of Dynamo's replication (DeCandia et al., SOSP 2007).

- A consistent hashing ring with virtual nodes. The preference list of a key is
  the first N distinct physical nodes met clockwise from the key's hash.
- Each stored value carries a vector clock. A node keeps every version that no
  other version it holds descends from (siblings).
- put(key, value, context): the coordinator merges the clocks in the context,
  adds one to its own entry and sends the version to the N targets; the put
  succeeds when W of them store it.
- get(key): ask the targets, use R replies, return all versions not dominated
  by another; read repair sends the merged result to the stale repliers.
- Strict quorum: the targets are the N home nodes that are reachable.
  Sloppy quorum: the targets are the first N reachable nodes on the ring walk;
  a stand-in for an unreachable home keeps a hint and hands the data back
  when the home is reachable again (hinted handoff).

Operations here are atomic steps; a "side" is the set of nodes the coordinator
can reach, which models crashes and partitions.
"""

import hashlib
import random
from bisect import bisect_right

Clock = dict[str, int]
Version = tuple[tuple[tuple[str, int], ...], object]  # (sorted clock items, value)


def h32(s: str) -> int:
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:4], "big")


def clock_of(v: Version) -> Clock:
    return dict(v[0])


def make_version(clock: Clock, value: object) -> Version:
    return (tuple(sorted(clock.items())), value)


def descends(a: Clock, b: Clock) -> bool:
    """a has seen everything b has seen."""
    return all(a.get(k, 0) >= c for k, c in b.items())


def reconcile(versions: list[Version]) -> list[Version]:
    """Drop every version that another version strictly descends from; drop duplicates."""
    out: list[Version] = []
    for v in versions:
        cv = clock_of(v)
        if any(descends(clock_of(o), cv) and (o[0] != v[0]) for o in versions):
            continue
        if v not in out:
            out.append(v)
    return sorted(out, key=lambda v: (v[0], repr(v[1])))


class Ring:
    def __init__(self, nodes: list[str], vnodes: int) -> None:
        self.points = sorted((h32(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))
        self.tokens = [p[0] for p in self.points]

    def walk(self, key: str) -> list[str]:
        """Distinct physical nodes clockwise from the key's position."""
        i = bisect_right(self.tokens, h32(key))
        seen: list[str] = []
        for j in range(len(self.points)):
            n = self.points[(i + j) % len(self.points)][1]
            if n not in seen:
                seen.append(n)
        return seen

    def preference_list(self, key: str, n: int) -> list[str]:
        return self.walk(key)[:n]


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.store: dict[str, list[Version]] = {}
        self.hints: list[tuple[str, str]] = []  # (home node, key)

    def put_local(self, key: str, versions: list[Version]) -> None:
        self.store[key] = reconcile(self.store.get(key, []) + versions)

    def get_local(self, key: str) -> list[Version]:
        return list(self.store.get(key, []))


class Cluster:
    def __init__(self, names: list[str], n: int, r: int, w: int, vnodes: int = 8,
                 sloppy: bool = False, seed: int = 0) -> None:
        self.ring = Ring(names, vnodes)
        self.nodes = {x: Node(x) for x in names}
        self.n, self.r, self.w = n, r, w
        self.sloppy = sloppy
        self.rng = random.Random(seed)
        self.up: set[str] = set(names)

    def homes(self, key: str) -> list[str]:
        return self.ring.preference_list(key, self.n)

    def targets(self, key: str, side: set[str] | None) -> list[tuple[str, str | None]]:
        """(node, hint) pairs. hint is the home node a stand-in replaces."""
        reach = (self.up if side is None else side & self.up)
        homes = self.homes(key)  # @line L1
        if not self.sloppy:
            return [(x, None) for x in homes if x in reach]
        chosen = [x for x in self.ring.walk(key) if x in reach][: self.n]  # @line L2
        missing = [x for x in homes if x not in chosen]
        out = []
        for x in chosen:
            out.append((x, None) if x in homes else (x, missing.pop(0)))
        return out

    def put(self, key: str, value: object, context: list[Version],
            side: set[str] | None = None) -> bool:
        tg = self.targets(key, side)
        if not tg:
            return False
        coord = tg[0][0]
        clock: Clock = {}
        for v in context:
            for k, c in clock_of(v).items():
                clock[k] = max(clock.get(k, 0), c)
        clock[coord] = clock.get(coord, 0) + 1  # @line L3
        ver = make_version(clock, value)
        for x, hint in tg:
            self.nodes[x].put_local(key, [ver])  # @line L4
            if hint is not None:
                self.nodes[x].hints.append((hint, key))
        return len(tg) >= self.w  # @line L5

    def get(self, key: str, side: set[str] | None = None,
            repair: bool = True) -> tuple[bool, list[Version]]:
        tg = [x for x, _ in self.targets(key, side)]
        if len(tg) < self.r:
            return False, []
        # the first R replies come from R targets in a seeded random order
        ask = self.rng.sample(tg, self.r)  # @line L6
        replies = {x: self.nodes[x].get_local(key) for x in ask}
        result = reconcile([v for vs in replies.values() for v in vs])  # @line L7
        if repair:
            for x, vs in replies.items():
                if vs != result:
                    self.nodes[x].put_local(key, result)  # @line L8
        return True, result  # @line L9

    def handoff(self) -> int:
        """Every reachable stand-in sends hinted data to its home. Returns the count."""
        moved = 0
        for node in self.nodes.values():
            if node.name not in self.up:
                continue
            keep = []
            for home, key in node.hints:
                if home in self.up:
                    self.nodes[home].put_local(key, node.get_local(key))  # @line L10
                    if node.name not in self.homes(key):
                        node.store.pop(key, None)
                    moved += 1
                else:
                    keep.append((home, key))
            node.hints = keep
        return moved


def values(vs: list[Version]) -> list[object]:
    return sorted(v[1] for v in vs)


def sloppy_partition_run(sloppy: bool) -> dict:
    """Five nodes, N = 3, R = W = 2. A partition puts the first home and two
    other nodes on side 1 and the other two homes on side 2. A client on side 1
    writes; then a client on side 2 reads."""
    names = ["A", "B", "C", "D", "E"]
    c = Cluster(names, 3, 2, 2, sloppy=sloppy, seed=1)
    key = "cart:42"
    assert c.put(key, "old", [])
    _, ctx = c.get(key)  # the client reads before the partition
    homes = c.homes(key)
    others = [x for x in names if x not in homes]
    side1 = {homes[0]} | set(others)
    side2 = set(homes[1:])
    ok_w = c.put(key, "new", ctx, side1)
    ok_r, got = c.get(key, side2)
    return {"cluster": c, "key": key, "homes": homes, "write_ok": ok_w,
            "read_ok": ok_r, "read": values(got), "side1": side1, "side2": side2}
