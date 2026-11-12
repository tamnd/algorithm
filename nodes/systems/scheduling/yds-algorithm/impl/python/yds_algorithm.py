# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yds-algorithm/. The authors are listed in prov/ZZVKP5.jsonl.

"""The offline speed scaling algorithm of Yao, Demers and Shenker (FOCS 1995).

Each job j has a release time, a deadline and an amount of work. The
processor may run at any speed s >= 0, with power s**alpha. YDS repeatedly
finds an interval of maximum intensity (work of the jobs inside it divided
by its length), runs those jobs at that speed by EDF, removes the interval
and compresses time. It gives the schedule of minimum energy. Each round
costs O(n^2), so the whole run costs O(n^3). All arithmetic is exact.
"""

from fractions import Fraction
from typing import NamedTuple, Sequence

INF = float("inf")


class Job(NamedTuple):
    release: Fraction
    deadline: Fraction
    work: Fraction


class Round(NamedTuple):
    speed: Fraction
    pieces: list  # real time intervals (a, b) of this round
    jobs: list  # indices of the jobs that run in this round


class Schedule(NamedTuple):
    rounds: list  # Round, in the order YDS finds them
    segments: list  # (start, end, job), in time order
    speed: dict  # job -> its speed

    def energy(self, alpha) -> Fraction:
        return sum((r.speed**alpha * sum(b - a for a, b in r.pieces) for r in self.rounds), Fraction(0))


def _squeeze(t, z, z2):
    """Compressed time after the interval [z, z2] is removed."""
    if t <= z:
        return t
    return z if t <= z2 else t - (z2 - z)


def _real_pieces(used, z, z2):
    """The real times that are not used and whose compressed time is in [z, z2]."""
    pieces, off, start = [], Fraction(0), -INF
    for a, b in used + [(INF, INF)]:
        lo, hi = max(start - off, z), min(a - off, z2)
        if lo < hi:
            pieces.append((lo + off, hi + off))
        if a == INF:
            break
        off += b - a
        start = b
    return pieces


def _merge(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and out[-1][1] >= a:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _edf(pieces, members, jobs, g):
    """Run the members by earliest deadline first at speed g during the pieces."""
    left = {j: jobs[j].work for j in members}
    segs = []
    for a, b in pieces:
        t = a
        while t < b:
            waiting = [j for j in members if left[j] > 0]
            ready = [j for j in waiting if jobs[j].release <= t]
            later = [jobs[j].release for j in waiting if jobs[j].release > t]
            nxt = min(later + [b])
            if not ready:
                t = nxt
                continue
            j = min(ready, key=lambda k: (jobs[k].deadline, k))
            end = min(nxt, t + left[j] / g)
            if end > jobs[j].deadline:
                raise AssertionError("EDF missed a deadline")
            segs.append((t, end, j))
            left[j] -= (end - t) * g
            t = end
    if any(left.values()):
        raise AssertionError("EDF left work")
    return segs


def yds(jobs: Sequence[Sequence]) -> Schedule:
    """Minimum energy schedule for jobs given as (release, deadline, work)."""
    jobs = [Job(Fraction(r), Fraction(d), Fraction(w)) for r, d, w in jobs]
    for j in jobs:
        if not (j.release < j.deadline and j.work > 0):
            raise ValueError("each job needs release < deadline and work > 0")
    window = {k: (j.release, j.deadline) for k, j in enumerate(jobs)}  # compressed
    used, rounds, segments, speed = [], [], [], {}  # @line L1
    while window:  # @line L2
        by_deadline = sorted(window, key=lambda k: window[k][1])
        best = None
        for z in sorted({r for r, _ in window.values()}):  # @line L3
            acc = Fraction(0)
            for k in by_deadline:
                r, d = window[k]
                if r >= z:
                    acc += jobs[k].work
                    g = acc / (d - z)
                    if best is None or g > best[0]:
                        best = (g, z, d)
        g, z, z2 = best
        members = sorted(k for k, (r, d) in window.items() if z <= r and d <= z2)  # @line L4
        pieces = _real_pieces(used, z, z2)  # @line L5
        segments += _edf(pieces, members, jobs, g)  # @line L6
        rounds.append(Round(g, pieces, members))
        for k in members:
            speed[k] = g
            del window[k]
        for k, (r, d) in window.items():  # @line L7
            window[k] = (_squeeze(r, z, z2), _squeeze(d, z, z2))
        used = _merge(used + pieces)
    segments.sort()
    return Schedule(rounds, segments, speed)  # @line L8


def avr_energy(jobs, alpha) -> Fraction:
    """Energy of AVR: at time t, run at the sum of w/(d - r) over the active jobs."""
    jobs = [Job(Fraction(r), Fraction(d), Fraction(w)) for r, d, w in jobs]
    points = sorted({j.release for j in jobs} | {j.deadline for j in jobs})
    total = Fraction(0)
    for a, b in zip(points, points[1:]):
        s = sum((j.work / (j.deadline - j.release) for j in jobs if j.release <= a and b <= j.deadline), Fraction(0))
        total += (b - a) * s**alpha
    return total
