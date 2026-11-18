# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xjoin/. The authors are listed in prov/NRZ4EB.jsonl.

"""XJoin: a pipelined hash join with a memory limit, run as a one-thread simulation.

Both inputs are hashed into P partitions on the join key. Each partition of
each input has a part in memory and a part on disk. Memory holds at most M
tuples in total.

Stage 1 runs on each arrival: insert into the memory part of the own
partition and probe the memory part of the same partition of the other input.
When memory holds more than M tuples, the largest memory part (this choice is
a heuristic of this implementation) moves to disk.

Stage 2 runs when the driver reports that both inputs are blocked: the disk
part of one partition is joined with the memory part of the same partition of
the other input.

Stage 3 runs at the end of the input and joins everything that is left.

Duplicates are avoided with timestamps from one logical clock. Each tuple has
an arrival time ATS and a departure time DTS (when it moved to disk, or
infinity). Each disk part keeps the list of the times at which stage 2 used
it. DONE(a, b) decides from these alone whether a pair was already emitted.

Events are ("R", t), ("S", t) and ("block",). The join is the natural join
on the common attributes, under bag semantics; a NULL key never matches.
"""

import zlib
from collections.abc import Iterable, Sequence

R = "R"
S = "S"
BLOCK = "block"
INF = float("inf")
OTHER = {R: S, S: R}


class Rec:
    """One stored occurrence of a tuple with its timestamps."""

    __slots__ = ("t", "key", "ats", "dts", "side")

    def __init__(self, t: tuple, key: tuple, ats: int, side: str) -> None:
        self.t = t
        self.key = key
        self.ats = ats
        self.dts = INF
        self.side = side


class XJoin:
    def __init__(self, schema_r: Sequence[str], schema_s: Sequence[str],
                 partitions: int = 4, memory: int = 8, avoid_duplicates: bool = True) -> None:
        if partitions < 1 or memory < 1:
            raise ValueError("partitions and memory must be at least 1")
        self.schema = {R: tuple(schema_r), S: tuple(schema_s)}
        self.common = tuple(a for a in self.schema[R] if a in self.schema[S])
        self.key_pos = {x: [self.schema[x].index(a) for a in self.common] for x in (R, S)}
        self.rest_pos = [i for i, a in enumerate(self.schema[S]) if a not in self.common]
        self.P = partitions
        self.M = memory
        self.avoid_duplicates = avoid_duplicates
        self.mem = {x: [[] for _ in range(partitions)] for x in (R, S)}  # @line L1
        self.disk = {x: [[] for _ in range(partitions)] for x in (R, S)}
        self.hist = {x: [[] for _ in range(partitions)] for x in (R, S)}
        self.clock = 0
        self.in_memory = 0
        self.stats = {"stage1": 0, "stage2": 0, "stage3": 0, "disk_writes": 0, "disk_reads": 0}

    # ------------------------------------------------------------ helpers

    def part(self, key: tuple) -> int:
        """A stable hash of the key, independent of Python hash randomization."""
        return zlib.crc32(repr(key).encode()) % self.P

    def _combine(self, a: Rec, b: Rec) -> tuple:
        r, s = (a, b) if a.side == R else (b, a)
        return r.t + tuple(s.t[i] for i in self.rest_pos)

    def done(self, a: Rec, b: Rec, p: int) -> bool:
        """True if the pair (a, b) was emitted before, by stage 1 or stage 2."""
        if not self.avoid_duplicates:
            return False
        if a.ats < b.dts and b.ats < a.dts:  # @line L15
            return True
        for x, y in ((a, b), (b, a)):  # @line L16
            for pt in self.hist[x.side][p]:  # @line L17
                if x.dts < pt and y.ats < pt < y.dts:
                    return True
        return False

    def _flush_largest(self) -> None:
        sizes = [(len(self.mem[x][p]), x == S, p, x) for x in (R, S) for p in range(self.P)]
        size, _, p, x = max(sizes, key=lambda v: (v[0], not v[1], -v[2]))
        self.clock += 1
        for rec in self.mem[x][p]:
            rec.dts = self.clock
        self.disk[x][p].extend(self.mem[x][p])
        self.stats["disk_writes"] += size
        self.in_memory -= size
        self.mem[x][p] = []

    # ------------------------------------------------------------ stages

    def arrive(self, side: str, t: Sequence) -> list[tuple]:
        """Stage 1 for one arriving tuple. Returns the tuples it emits."""
        t = tuple(t)
        self.clock += 1  # @line L3
        key = tuple(t[i] for i in self.key_pos[side])
        if any(v is None for v in key):
            return []
        p = self.part(key)
        rec = Rec(t, key, self.clock, side)  # @line L5
        self.mem[side][p].append(rec)
        self.in_memory += 1
        out = []
        for u in self.mem[OTHER[side]][p]:  # @line L6
            if u.key == key:
                out.append(self._combine(rec, u))
        self.stats["stage1"] += len(out)
        if self.in_memory > self.M:  # @line L7
            self._flush_largest()
        return out

    def blocked(self) -> list[tuple]:
        """Stage 2: both inputs are blocked. Join one disk part with memory."""
        self.clock += 1
        choices = [(len(self.disk[x][p]), x == R, -p, x, p)
                   for x in (R, S) for p in range(self.P) if self.disk[x][p]]
        if not choices:
            return []
        _, _, _, x, p = max(choices)  # @line L9
        pt = self.clock
        y = OTHER[x]
        self.stats["disk_reads"] += len(self.disk[x][p])
        out = []
        for a in self.disk[x][p]:  # @line L10
            for b in self.mem[y][p]:
                if a.key == b.key and not self.done(a, b, p):  # @line L11
                    out.append(self._combine(a, b))
        self.hist[x][p].append(pt)  # @line L12
        self.stats["stage2"] += len(out)
        return out

    def finish(self) -> list[tuple]:
        """Stage 3: the input has ended. Emit every pair that is not yet done."""
        self.clock += 1
        out = []
        for p in range(self.P):  # @line L13
            left = self.mem[R][p] + self.disk[R][p]
            right = self.mem[S][p] + self.disk[S][p]
            self.stats["disk_reads"] += len(self.disk[R][p]) + len(self.disk[S][p])
            for a in left:
                for b in right:
                    if a.key == b.key and not self.done(a, b, p):  # @line L14
                        out.append(self._combine(a, b))
        self.stats["stage3"] += len(out)
        return out


def xjoin(schema_r: Sequence[str], schema_s: Sequence[str], events: Iterable[tuple],
          partitions: int = 4, memory: int = 8, avoid_duplicates: bool = True):
    """Run XJoin over the events. Returns (outputs per event plus a final entry for stage 3, join)."""
    j = XJoin(schema_r, schema_s, partitions, memory, avoid_duplicates)
    steps = []
    for e in events:  # @line L2
        if e[0] == BLOCK:  # @line L8
            steps.append(j.blocked())
        else:  # @line L4
            steps.append(j.arrive(e[0], e[1]))
    steps.append(j.finish())
    return steps, j
