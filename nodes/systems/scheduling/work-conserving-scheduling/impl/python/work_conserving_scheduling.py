# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-conserving-scheduling/. The authors are listed in prov/VBE4E8.jsonl.

"""Work conservation on one CPU: busy periods and unfinished work do not depend
on the order of service, as long as the CPU never idles while work is waiting.

Jobs have arrival times and bursts (int or Fraction). Every scheduler returns a
list of slices (job, start, end). Switches cost nothing, and a preempted job
resumes where it stopped.
"""

from collections import deque


def nonpreemptive(arrival: list, burst: list, key, delay=0) -> list:
    """Run, at each free moment, the waiting job of least key to completion.

    key(i) gives the rank of job i: FCFS, LCFS, SJF and nonpreemptive priority
    are all of this form. With delay > 0, a job may start only `delay` units
    after its arrival, which makes the scheduler not work-conserving.
    """
    n = len(arrival)
    done, out, t = set(), [], 0
    while len(done) < n:
        ready = [j for j in range(n) if j not in done and arrival[j] + delay <= t]
        if not ready:
            t = min(arrival[j] + delay for j in range(n) if j not in done)
            continue
        j = min(ready, key=key)
        out.append((j, t, t + burst[j]))
        t += burst[j]
        done.add(j)
    return out


def preemptive_priority(arrival: list, burst: list, prio: list) -> list:
    """Preemptive priority (smaller is higher): run the best job until the next arrival."""
    n = len(arrival)
    left, out, t = list(burst), [], 0
    while any(left):
        ready = [j for j in range(n) if arrival[j] <= t and left[j] > 0]
        later = [arrival[j] for j in range(n) if arrival[j] > t]
        if not ready:
            t = min(later)
            continue
        j = min(ready, key=lambda j: (prio[j], arrival[j], j))
        end = min([t + left[j]] + later)
        out.append((j, t, end))
        left[j] -= end - t
        t = end
    return out


def round_robin(arrival: list, burst: list, q) -> list:
    """Round robin with quantum q; arrivals join the queue before a preempted job."""
    n = len(arrival)
    order = sorted(range(n), key=lambda i: (arrival[i], i))
    left, out, ready, k, t = list(burst), [], deque(), 0, 0
    while k < n or ready:
        if not ready and t < arrival[order[k]]:
            t = arrival[order[k]]
        while k < n and arrival[order[k]] <= t:
            ready.append(order[k])
            k += 1
        j = ready.popleft()
        d = min(q, left[j])
        out.append((j, t, t + d))
        t += d
        left[j] -= d
        while k < n and arrival[order[k]] <= t:
            ready.append(order[k])
            k += 1
        if left[j] > 0:
            ready.append(j)
    return out


def busy_periods(slices: list) -> list:
    """The maximal intervals in which the CPU is busy."""
    out = []
    for _, s, e in sorted(slices, key=lambda x: x[1]):
        if out and out[-1][1] == s:
            out[-1] = (out[-1][0], e)
        elif e > s:
            out.append((s, e))
    return out


def busy_periods_from_trace(arrival: list, burst: list) -> list:
    """The busy periods of every work-conserving scheduler, from the input alone.

    A busy period starts at an arrival when the CPU is idle, and it ends when
    the work that arrived since its start has been done.
    """
    out = []
    for a, b in sorted(zip(arrival, burst)):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], out[-1][1] + b)
        else:
            out.append((a, a + b))
    return out


def unfinished_work(arrival: list, burst: list, slices: list, t) -> object:
    """Work that has arrived by time t and has not been done by t."""
    arrived = sum(b for a, b in zip(arrival, burst) if a <= t)
    served = sum(max(0, min(e, t) - s) for _, s, e in slices)
    return arrived - served


def work_area(slices: list, arrival: list, burst: list) -> object:
    """The integral of the unfinished work over time, exactly.

    The unfinished work is piecewise linear, with breakpoints at arrivals and
    slice ends, so the trapezoid rule on these points is exact.
    """
    points = sorted({0, *arrival, *(s for _, s, _ in slices), *(e for _, _, e in slices)})
    total = 0
    for x, y in zip(points, points[1:]):
        # just after x and just before y; the jumps at arrivals happen at x
        vx = unfinished_work(arrival, burst, slices, x)
        vy = vx - sum(max(0, min(e, y) - max(s, x)) for _, s, e in slices)
        total += (vx + vy) * (y - x) / 2
    return total


def waiting_times(arrival: list, burst: list, slices: list) -> list:
    """C_j - a_j - b_j for each job."""
    end = {}
    for j, _, e in slices:
        end[j] = max(end.get(j, e), e)
    return [end[j] - arrival[j] - burst[j] for j in range(len(arrival))]
