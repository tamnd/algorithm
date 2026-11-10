# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-available/. The authors are listed in prov/4DSS0A.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Job = tuple[Number, Number, Number]  # (release r, work w, deadline d)
Piece = tuple[Number, Number, Number]  # (start, end, speed)


def optimal_available(jobs: list[Job]) -> tuple[list[Piece], list[Number]]:
    """Run Optimal Available on one processor.

    jobs[j] = (r_j, w_j, d_j) with r_j < d_j and w_j > 0. Return the speed
    profile as pieces (a, b, s) and the completion time of each job. At
    each release, the speed is the optimal speed for the remaining work,
    and the jobs run in deadline order. Ties in the deadline go to the
    smaller index.
    """
    n = len(jobs)
    releases = sorted({r for r, _, _ in jobs})
    rem: dict[int, Fraction] = {}
    done: list[Number] = [0] * n
    pieces: list[Piece] = []
    for idx, t in enumerate(releases):  # @line L1
        for j in range(n):  # @line L2
            if jobs[j][0] == t:
                rem[j] = Fraction(jobs[j][1])
        nxt = releases[idx + 1] if idx + 1 < len(releases) else None  # @line L3
        while rem and (nxt is None or t < nxt):  # @line L4
            order = sorted(rem, key=lambda j: (jobs[j][2], j))  # @line L5
            prefix = Fraction(0)
            speed, end = Fraction(0), t
            for j in order:
                prefix += rem[j]
                g = prefix / (jobs[j][2] - t)
                if g >= speed:
                    speed, end = g, jobs[j][2]
            if nxt is not None and nxt < end:  # @line L6
                end = nxt
            pieces.append((t, end, speed))  # @line L7
            for j in order:
                if t >= end:
                    break
                dt = min(rem[j] / speed, end - t)
                rem[j] -= speed * dt
                t += dt
                if rem[j] == 0:
                    del rem[j]
                    done[j] = t
            t = end
    return pieces, done  # @line L8


def energy(pieces: list[Piece], alpha: int) -> Number:
    """Return the energy, the integral of s(t) ** alpha, of a speed profile."""
    return sum(s ** alpha * (b - a) for a, b, s in pieces)
