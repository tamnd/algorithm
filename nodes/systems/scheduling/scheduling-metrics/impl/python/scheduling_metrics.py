# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-metrics/. The authors are listed in prov/NMZMS9.jsonl.

"""Per-job and aggregate scheduling metrics of a one-CPU schedule.

A job is (name, arrival, burst) with a single CPU burst. A schedule is a list
of segments (start, end, name). Times are int or Fraction, and every result is
exact. Cost: O(s + n) for s segments and n jobs.
"""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class JobMetrics:
    completion: object
    turnaround: object  # completion - arrival
    waiting: object  # turnaround - burst
    response: object  # first run - arrival
    stretch: Fraction  # turnaround / burst


def per_job(jobs: list, segments: list) -> dict:
    """Return a dict name -> JobMetrics. Raises ValueError on a bad schedule."""
    out = {}
    for name, arrival, burst in jobs:
        mine = [(s, e) for s, e, n in segments if n == name]
        if not mine or sum(e - s for s, e in mine) != burst:
            raise ValueError(f"job {name} does not get its burst")
        first = min(s for s, _ in mine)
        if first < arrival:
            raise ValueError(f"job {name} runs before it arrives")
        c = max(e for _, e in mine)
        t = c - arrival
        out[name] = JobMetrics(c, t, t - burst, first - arrival, Fraction(t) / Fraction(burst))
    return out


def aggregate(jobs: list, segments: list) -> dict:
    """Averages, maxima, throughput and utilization over [first arrival, last completion]."""
    m = per_job(jobs, segments)
    n = len(jobs)
    start = min(a for _, a, _ in jobs)
    end = max(x.completion for x in m.values())
    busy = sum(e - s for s, e, name in segments if name != "*")
    return {
        "avg_turnaround": Fraction(sum(x.turnaround for x in m.values()), n),
        "avg_waiting": Fraction(sum(x.waiting for x in m.values()), n),
        "avg_response": Fraction(sum(x.response for x in m.values()), n),
        "max_stretch": max(x.stretch for x in m.values()),
        "throughput": Fraction(n) / Fraction(end - start),
        "utilization": Fraction(busy) / Fraction(end - start),
    }


def jain_index(xs: list) -> Fraction:
    """Jain's fairness index (sum x)^2 / (n * sum x^2): 1 when all are equal, 1/n at worst."""
    s = sum(Fraction(x) for x in xs)
    q = sum(Fraction(x) ** 2 for x in xs)
    return s * s / (len(xs) * q)


def number_in_system_area(jobs: list, segments: list) -> object:
    """The integral of the number of jobs in the system over time: sum of turnarounds."""
    m = per_job(jobs, segments)
    events = sorted([(a, 1) for _, a, _ in jobs] + [(x.completion, -1) for x in m.values()])
    area, count, last = 0, 0, events[0][0]
    for t, d in events:
        area += count * (t - last)
        count, last = count + d, t
    return area
