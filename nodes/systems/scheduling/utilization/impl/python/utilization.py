# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utilization/. The authors are listed in prov/KNYA42.jsonl.

"""Exact utilization measures on one processor.

Schedules are lists of slices (job, start, end). Times are int or Fraction, and
every result is exact.
"""

from fractions import Fraction
from math import lcm


def busy_time(slices: list, t0, t1) -> object:
    """Time in [t0, t1) during which the processor runs some job."""
    return sum(max(0, min(e, t1) - max(s, t0)) for _, s, e in slices)


def measured_utilization(slices: list, t0, t1) -> Fraction:
    """U = busy time / length of the interval."""
    return Fraction(busy_time(slices, t0, t1)) / (t1 - t0)


def utilization_law(slices: list, completions: list, t0, t1) -> tuple:
    """Return (U, X, S): utilization, throughput X = C / T and mean service
    S = B / C per completion, over [t0, t1). The law says U = X * S."""
    length = t1 - t0
    done = sum(1 for c in completions if t0 < c <= t1)
    b = busy_time(slices, t0, t1)
    return Fraction(b) / length, Fraction(done) / length, Fraction(b) / done


def task_set_utilization(tasks: list) -> Fraction:
    """U = sum of C_i / T_i for periodic tasks given as (C_i, T_i)."""
    return sum((Fraction(c, t) for c, t in tasks), Fraction(0))


def hyperperiod_demand(tasks: list) -> tuple:
    """Return (H, D): the hyperperiod H = lcm of the periods, and the work D
    that all jobs released in [0, H) need. D = U * H."""
    h = lcm(*(t for _, t in tasks))
    return h, sum((h // t) * c for c, t in tasks)


def number_in_system_area(arrival: list, completion: list) -> object:
    """The integral of N(t), the number of jobs present, over all time.

    N is a step function, so the integral is a finite sum over its steps.
    """
    events = sorted([(a, 1) for a in arrival] + [(c, -1) for c in completion])
    area, n, last = 0, 0, None
    for t, d in events:
        if last is not None:
            area += n * (t - last)
        n += d
        last = t
    return area


def littles_law(arrival: list, completion: list, t0, t1) -> tuple:
    """Return (L, lam, W) over [t0, t1), for a trace in which every job arrives
    and completes inside the interval: L is the time average of N(t), lam the
    arrival rate and W the mean time in system. Then L = lam * W exactly."""
    assert all(t0 <= a and c <= t1 for a, c in zip(arrival, completion))
    length = t1 - t0
    n = len(arrival)
    big_l = Fraction(number_in_system_area(arrival, completion)) / length
    lam = Fraction(n) / length
    w = Fraction(sum(c - a for a, c in zip(arrival, completion))) / n
    return big_l, lam, w


def fcfs(arrival: list, burst: list) -> list:
    """Slices of first-come, first-served on one processor."""
    t, out = 0, []
    for j in sorted(range(len(arrival)), key=lambda j: (arrival[j], j)):
        t = max(t, arrival[j])
        out.append((j, t, t + burst[j]))
        t += burst[j]
    return out


def preemptive_priority(arrival: list, burst: list, prio: list) -> list:
    """Slices of preemptive priority scheduling (smaller is higher)."""
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


def completions(slices: list, n: int) -> list:
    out = [None] * n
    for j, _, e in slices:
        out[j] = e if out[j] is None else max(out[j], e)
    return out
