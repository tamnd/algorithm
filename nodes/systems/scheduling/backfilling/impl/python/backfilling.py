# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backfilling/. The authors are listed in prov/ARFFDA.jsonl.

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Job:
    """A rigid parallel job. It needs `size` processors at once. The user
    gives `estimate`; the job really runs min(runtime, estimate), because the
    system kills a job that reaches its estimate."""

    name: str
    arrival: int
    size: int
    estimate: int
    runtime: int


@dataclass
class Trace:
    start: dict = field(default_factory=dict)
    end: dict = field(default_factory=dict)
    # EASY: the shadow time computed when the job was first a blocked head.
    # Conservative: the reservation given at arrival.
    reservation: dict = field(default_factory=dict)


def earliest_fit(now: int, size: int, dur: int, busy: list, procs: int) -> int:
    """Earliest time s >= now such that `size` processors are free during
    [s, s + dur), given busy intervals (start, end, size)."""
    cands = sorted({now} | {e for _, e, _ in busy if e > now})
    for s in cands:
        points = [s] + [b for b, _, _ in busy if s < b < s + dur]
        if all(sum(k for b, e, k in busy if b <= p < e) + size <= procs for p in points):
            return s
    raise AssertionError("unreachable: the last end time always fits")


def _easy_pass(t, queue, running, procs, tr):
    free = procs - sum(r[2] for r in running.values())
    while queue and queue[0].size <= free:  # @line L1
        j = queue.pop(0)
        running[j.name] = (t, t + j.estimate, j.size, t + min(j.runtime, j.estimate))
        tr.start[j.name] = t
        free -= j.size
    if not queue:  # @line L2
        return
    h = queue[0]  # @line L3
    ends = sorted((r[1], r[2]) for r in running.values())  # @line L4
    avail, shadow = free, None
    for e, k in ends:  # @line L5
        avail += k
        if avail >= h.size:
            shadow = e
            break
    extra = sum(k for e, k in ends if e <= shadow) + free - h.size  # @line L6
    tr.reservation.setdefault(h.name, shadow)
    for j in list(queue[1:]):  # @line L7
        if j.size <= free and (t + j.estimate <= shadow or j.size <= extra):  # @line L8
            queue.remove(j)
            running[j.name] = (t, t + j.estimate, j.size, t + min(j.runtime, j.estimate))
            tr.start[j.name] = t
            free -= j.size  # @line L9
            if t + j.estimate > shadow:
                extra -= j.size


def _conservative_reserve(t, j, reserved, running, procs, by_name):
    busy = [(r[0], r[1], r[2]) for r in running.values()]
    busy += [(s, s + by_name[n].estimate, by_name[n].size) for n, s in reserved.items() if n != j.name]
    return earliest_fit(t, j.size, j.estimate, busy, procs)


def backfill(procs: int, jobs: list[Job], policy: str = "easy") -> Trace:
    """Simulate a space-shared machine of `procs` processors with a FCFS
    queue and the given policy: "fcfs" (no backfilling), "easy" (Lifka 1995)
    or "conservative" (Mu'alem and Feitelson 2001)."""
    if policy not in ("fcfs", "easy", "conservative"):
        raise ValueError(policy)
    for j in jobs:
        if not (1 <= j.size <= procs and j.estimate >= 1 and j.runtime >= 1):
            raise ValueError(f"bad job {j.name}")
    by_name = {j.name: j for j in jobs}
    pending = sorted(jobs, key=lambda j: (j.arrival, j.name))
    queue: list[Job] = []
    running: dict[str, tuple] = {}  # name -> (start, estimated end, size, real end)
    reserved: dict[str, int] = {}  # conservative: current reservation of each queued job
    tr = Trace()
    nxt = 0
    while nxt < len(pending) or queue or running:
        cands = [r[3] for r in running.values()]
        if nxt < len(pending):
            cands.append(pending[nxt].arrival)
        if not cands:
            raise AssertionError("a queued job with no event to start it")
        t = min(cands)
        ended = [n for n, r in running.items() if r[3] == t]
        for n in ended:
            tr.end[n] = t
            del running[n]
        if policy == "conservative" and ended:
            # compress: in order of reservation, move each job to its earliest fit
            for n in sorted(reserved, key=lambda n: (reserved[n], by_name[n].arrival, n)):
                new = _conservative_reserve(t, by_name[n], reserved, running, procs, by_name)
                assert new <= reserved[n]
                reserved[n] = new
        while nxt < len(pending) and pending[nxt].arrival == t:
            j = pending[nxt]
            nxt += 1
            queue.append(j)
            if policy == "conservative":
                reserved[j.name] = _conservative_reserve(t, j, reserved, running, procs, by_name)
                tr.reservation[j.name] = reserved[j.name]
        if policy == "easy":
            _easy_pass(t, queue, running, procs, tr)
        elif policy == "fcfs":
            free = procs - sum(r[2] for r in running.values())
            while queue and queue[0].size <= free:
                j = queue.pop(0)
                running[j.name] = (t, t + j.estimate, j.size, t + min(j.runtime, j.estimate))
                tr.start[j.name] = t
                free -= j.size
        else:
            for j in [j for j in queue if reserved[j.name] == t]:
                queue.remove(j)
                del reserved[j.name]
                running[j.name] = (t, t + j.estimate, j.size, t + min(j.runtime, j.estimate))
                tr.start[j.name] = t
    return tr
