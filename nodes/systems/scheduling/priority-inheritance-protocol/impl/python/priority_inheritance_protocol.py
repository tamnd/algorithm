# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-inheritance-protocol/. The authors are listed in prov/1XKZ0H.jsonl.

"""Discrete-time simulator of one processor with fixed priorities and locks.

Each job has a base priority (a larger number is more urgent), a release
time and a list of actions: ("run", k) needs k units of processor time,
("lock", s) and ("unlock", s) take no time. Critical sections must be
properly nested. With protocol "pip" a lock holder runs at the largest
current priority of the jobs blocked on its locks (transitively). With
protocol "none" there is no inheritance, which shows plain priority
inversion.

Cost: each scheduling decision takes O(j^2) time for j jobs, and there are
at most (number of actions) decisions without a time step.
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


def simulate(jobs: list[Job], protocol: str = "pip", limit: int | None = None) -> Result:
    """Run the jobs to completion, or until every released unfinished job waits (a deadlock).

    blocking[x] counts the time units in which a job of lower base priority
    ran while x was released and unfinished; blockers[x] names the outermost
    critical sections (job, index) that ran in those units.
    """
    if protocol not in ("none", "pip"):
        raise ValueError(protocol)
    if len({j.priority for j in jobs}) != len(jobs):
        raise ValueError("base priorities must be distinct")
    by = {j.name: j for j in jobs}
    pc = {j.name: 0 for j in jobs}
    left = {j.name: 0 for j in jobs}
    held: dict[str, list[object]] = {j.name: [] for j in jobs}
    cs = {j.name: 0 for j in jobs}
    requested = {j.name: False for j in jobs}
    holder: dict[object, str] = {}
    finish: dict[str, int] = {}
    timeline: list[str | None] = []
    blocking = {j.name: 0 for j in jobs}
    blockers: dict[str, set[tuple[str, int]]] = {j.name: set() for j in jobs}
    if limit is None:
        limit = max([j.release for j in jobs], default=0) + 1
        limit += sum(a for j in jobs for k, a in j.actions if k == "run")

    def head(n: str) -> Action | None:
        return by[n].actions[pc[n]] if pc[n] < len(by[n].actions) else None

    def release_lock(n: str, s: object) -> None:
        assert holder.get(s) == n and held[n] and held[n][-1] == s, "bad nesting"
        held[n].pop()
        del holder[s]

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
        while True:
            blocker: dict[str, str] = {}
            for x in pending:  # @line L3
                h = head(x)
                if requested[x] and h is not None and h[0] == "lock" and h[1] in holder:
                    blocker[x] = holder[h[1]]
            prio = {n: by[n].priority for n in by}  # @line L4
            if protocol == "pip":
                changed = True
                while changed:
                    changed = False
                    for x, b in blocker.items():
                        if prio[x] > prio[b]:
                            prio[b] = prio[x]
                            changed = True
            ready = [n for n in pending if n not in blocker]
            if not ready:  # @line L6
                if pending:  # @line L7
                    return Result(finish, timeline, True, blocking, blockers)
                timeline.append(None)
                t += 1  # @line L8
                break
            j = max(ready, key=lambda n: (prio[n], by[n].priority))  # @line L5
            kind, arg = head(j)
            if kind == "lock":  # @line L9
                if arg not in holder:  # @line L10
                    if not held[j]:
                        cs[j] += 1
                    holder[arg] = j
                    held[j].append(arg)
                    requested[j] = False
                    pc[j] += 1
                else:
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
