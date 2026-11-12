# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-ceiling-protocol/. The authors are listed in prov/TNQ9RS.jsonl.

"""Discrete-time simulator of one processor with fixed priorities and locks.

Each job has a base priority (a larger number is more urgent), a release
time and a list of actions: ("run", k) needs k units of processor time,
("lock", s) and ("unlock", s) take no time. Critical sections must be
properly nested. The protocol decides when a lock is granted and how
priorities are inherited:

- "none": plain fixed priority, no inheritance;
- "pip": basic priority inheritance;
- "pcp": the priority ceiling protocol of Sha, Rajkumar and Lehoczky;
- "icpp": the immediate ceiling (highest locker) protocol.

Cost: each time unit does O(j^2 + j * s) work per scheduling decision for
j jobs and s locks, and there are at most (number of actions) decisions
without a time step, so the run is polynomial in the input size.
"""

from dataclasses import dataclass, field

Action = tuple[str, object]


@dataclass
class Job:
    name: str
    priority: int
    release: int
    actions: list[Action]


@dataclass
class Result:
    finish: dict[str, int]
    timeline: list[str | None]
    deadlock: bool
    blocking: dict[str, int] = field(default_factory=dict)
    blockers: dict[str, set[tuple[str, int]]] = field(default_factory=dict)


def ceilings(jobs: list[Job]) -> dict[object, int]:
    """The ceiling of a lock is the largest base priority of a job that locks it."""
    c: dict[object, int] = {}
    for j in jobs:
        for kind, arg in j.actions:
            if kind == "lock":
                c[arg] = max(c.get(arg, j.priority), j.priority)
    return c


def simulate(jobs: list[Job], protocol: str = "pcp", limit: int | None = None) -> Result:
    """Run the jobs to completion (or to a deadlock) under the protocol."""
    if protocol not in ("none", "pip", "pcp", "icpp"):
        raise ValueError(protocol)
    if len({j.priority for j in jobs}) != len(jobs):
        raise ValueError("base priorities must be distinct")
    ceil = ceilings(jobs)
    by = {j.name: j for j in jobs}
    pc = {j.name: 0 for j in jobs}
    left = {j.name: 0 for j in jobs}
    held: dict[str, list[object]] = {j.name: [] for j in jobs}
    cs = {j.name: 0 for j in jobs}
    requested = {j.name: False for j in jobs}
    holder: dict[object, str] = {}
    when: dict[object, int] = {}
    stamp = 0
    finish: dict[str, int] = {}
    timeline: list[str | None] = []
    blocking = {j.name: 0 for j in jobs}
    blockers: dict[str, set[tuple[str, int]]] = {j.name: set() for j in jobs}
    if limit is None:
        limit = max([j.release for j in jobs], default=0) + 1
        limit += sum(a for j in jobs for k, a in j.actions if k == "run")

    def head(n: str) -> Action | None:
        return by[n].actions[pc[n]] if pc[n] < len(by[n].actions) else None

    def system_ceiling(n: str) -> tuple[int, str | None]:
        best, who, w = -1, None, -1
        for s, h in holder.items():
            if h != n and (ceil[s], when[s]) > (best, w):
                best, who, w = ceil[s], h, when[s]
        return best, who

    def release_lock(n: str, s: object) -> None:
        assert holder.get(s) == n and held[n] and held[n][-1] == s, "bad nesting"
        held[n].pop()
        del holder[s]
        del when[s]

    def after_run(n: str, t: int) -> None:
        while head(n) is not None and head(n)[0] == "unlock":
            release_lock(n, head(n)[1])
            pc[n] += 1
        if head(n) is None:
            finish[n] = t

    t = 0  # @line L1
    while len(finish) < len(jobs) and t <= limit:  # @line L2
        pending = [n for n in by if by[n].release <= t and n not in finish]
        for n in pending:
            if head(n) is None:
                finish[n] = t
        pending = [n for n in pending if n not in finish]
        steps = 0
        while True:
            steps += 1
            assert steps < 10_000
            prio = {n: by[n].priority for n in by}
            blocker: dict[str, str] = {}
            for _ in range(len(jobs) + 2):  # @line L4
                blocker = {}
                for x in pending:  # @line L3
                    h = head(x)
                    if not requested[x] or h is None or h[0] != "lock":
                        continue
                    s = h[1]
                    if protocol in ("none", "pip"):
                        if s in holder:
                            blocker[x] = holder[s]
                    elif protocol == "pcp":
                        top, who = system_ceiling(x)
                        if s in holder or prio[x] <= top:
                            blocker[x] = who if who is not None else holder[s]
                new = {n: by[n].priority for n in by}
                if protocol == "icpp":
                    for n in by:
                        for s in held[n]:
                            new[n] = max(new[n], ceil[s])
                elif protocol in ("pip", "pcp"):
                    changed = True
                    while changed:
                        changed = False
                        for x, b in blocker.items():
                            if new[x] > new[b]:
                                new[b] = new[x]
                                changed = True
                if new == prio:
                    break
                prio = new
            ready = [n for n in pending if n not in blocker]
            if not ready:  # @line L6
                if pending:  # @line L7
                    return Result(finish, timeline, True, blocking, blockers)
                timeline.append(None)
                t += 1  # @line L8
                break
            # On a tie, a lock holder keeps the processor (it runs at a ceiling).
            j = max(ready, key=lambda n: (prio[n], bool(held[n]), by[n].priority))  # @line L5
            kind, arg = head(j)
            if kind == "lock":  # @line L9
                top, _ = system_ceiling(j)
                ok = arg not in holder
                if protocol == "pcp":
                    ok = ok and prio[j] > top  # @line L10
                if ok:
                    if not held[j]:
                        cs[j] += 1
                    holder[arg] = j
                    stamp += 1
                    when[arg] = stamp
                    held[j].append(arg)
                    requested[j] = False
                    pc[j] += 1
                else:
                    assert protocol != "icpp", "icpp never finds a lock taken"
                    requested[j] = True
                continue
            if kind == "unlock":  # @line L11
                release_lock(j, arg)
                pc[j] += 1
                after_run(j, t)
                if j in finish:
                    pending.remove(j)
                continue
            for x in pending:
                if x != j and by[x].priority > by[j].priority:
                    blocking[x] += 1
                    blockers[x].add((j, cs[j] if held[j] else 0))
            timeline.append(j)  # @line L12
            if left[j] == 0:
                left[j] = int(arg)
            left[j] -= 1
            if left[j] == 0:
                pc[j] += 1
                after_run(j, t + 1)
            t += 1
            break
    return Result(finish, timeline, False, blocking, blockers)
