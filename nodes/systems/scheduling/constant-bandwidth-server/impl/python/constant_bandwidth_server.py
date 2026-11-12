# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-bandwidth-server/. The authors are listed in prov/P5NM45.jsonl.

"""Constant bandwidth servers under EDF on one processor, in discrete time.

Hard tasks are (C, T) with deadline equal to the period and release at 0.
Each server is (Q, T) with bandwidth U = Q / T and serves its own list of
soft jobs (arrival, demand) first come, first served. Rules of Abeni and
Buttazzo (1998): the budget c and the server deadline d start at 0; when a
job arrives at r and the server is idle, if c >= (d - r) U then d = r + T and
c = Q, else d and c are kept; each unit of service takes one unit of c; when
c reaches 0, c = Q and d = d + T. EDF runs the ready entity with the
earliest deadline. All tests use integers, so c >= (d - r) U is checked as
c T >= (d - r) Q.

With cbs=False each soft job instead runs as a plain EDF job with the fixed
deadline arrival + T and no budget, to show what the server prevents.
Cost: O(n + s) work per time unit for n hard tasks and s servers.
"""

from dataclasses import dataclass, field


@dataclass
class Server:
    q: int
    t: int
    c: int = 0
    d: int = 0
    queue: list[list[int]] = field(default_factory=list)
    log: list[tuple[int, str, int]] = field(default_factory=list)


@dataclass
class Result:
    timeline: list[object]
    hard_misses: list[tuple[int, int]]
    soft_finish: list[list[int | None]]
    servers: list[Server]
    invariant_ok: bool


def cbs_schedule(hard: list[tuple[int, int]], servers: list[tuple[int, int]],
                 requests: list[list[tuple[int, int]]], horizon: int, cbs: bool = True) -> Result:
    """Simulate time units 0 .. horizon - 1 and report hard deadline misses (task, release)."""
    srv = [Server(q, t) for q, t in servers]
    jobs: list[list[int]] = []  # [deadline, remaining, task, release]
    misses: list[tuple[int, int]] = []
    finish: list[list[int | None]] = [[None] * len(r) for r in requests]
    work = [0] * len(srv)
    started = [False] * len(srv)
    ok = True
    timeline: list[object] = []
    for now in range(horizon):  # @line L1
        for j in [j for j in jobs if j[0] <= now]:
            misses.append((j[2], j[3]))
            jobs.remove(j)
        for i, (c, p) in enumerate(hard):  # @line L2
            if now % p == 0:
                jobs.append([now + p, c, i, now])
        for s, (sv, reqs) in enumerate(zip(srv, requests)):
            for k, (a, demand) in enumerate(reqs):
                if a != now:
                    continue
                if not cbs:
                    sv.queue.append([k, demand, a + sv.t])
                    continue
                if not sv.queue:  # @line L3
                    if sv.c * sv.t >= (sv.d - now) * sv.q:  # @line L4
                        sv.d, sv.c = now + sv.t, sv.q  # @line L5
                        sv.log.append((now, "new", sv.d))
                    else:
                        sv.log.append((now, "keep", sv.d))
                started[s] = True
                sv.queue.append([k, demand, sv.d])
        best = None
        for j in jobs:
            key = (j[0], 0, j[2])
            if best is None or key < best[0]:
                best = (key, "hard", j)
        for s, sv in enumerate(srv):
            if sv.queue:
                key = (sv.d if cbs else sv.queue[0][2], 1, s)
                if best is None or key < best[0]:  # @line L6
                    best = (key, "server", s)
        if best is None:
            timeline.append(None)
        elif best[1] == "hard":
            j = best[2]
            timeline.append(("H", j[2]))
            j[1] -= 1
            if j[1] == 0:
                jobs.remove(j)
        else:
            s = best[2]
            sv = srv[s]
            timeline.append(("S", s))
            head = sv.queue[0]
            head[1] -= 1  # @line L7
            work[s] += 1
            if head[1] == 0:
                finish[s][head[0]] = now + 1
                sv.queue.pop(0)
            if cbs:
                sv.c -= 1
                if sv.c == 0:  # @line L8
                    sv.c, sv.d = sv.q, sv.d + sv.t
                    sv.log.append((now + 1, "recharge", sv.d))
        for s, sv in enumerate(srv):
            if cbs and started[s] and (work[s] + sv.c) * sv.t > sv.d * sv.q:
                ok = False
    for j in jobs:
        if j[0] <= horizon:
            misses.append((j[2], j[3]))
    return Result(timeline, misses, finish, srv, ok)
