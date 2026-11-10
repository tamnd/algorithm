# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avr/. The authors are listed in prov/G3Q00A.jsonl.

import heapq
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Job = tuple[Number, Number, Number]  # (release r, work w, deadline d)
Piece = tuple[Number, Number, Number]  # (start, end, speed)


def avr(jobs: list[Job]) -> list[Piece]:
    """Return the AVR speed profile as pieces (a, b, s) with s > 0.

    jobs[j] = (r_j, w_j, d_j) with r_j < d_j and w_j > 0. The speed at
    time t is the sum of w_j / (d_j - r_j) over the jobs with
    r_j <= t < d_j. The pieces are in time order, and the speed is
    constant on each piece.
    """
    events: list[tuple[Number, Number]] = []
    for r, w, d in jobs:  # @line L1
        density = Fraction(w) / (d - r)  # @line L2
        events.append((r, density))
        events.append((d, -density))
    events.sort()  # @line L3
    pieces: list[Piece] = []
    s: Number = 0
    prev: Number | None = None
    for t, delta in events:  # @line L4
        if prev is not None and t > prev and s > 0:  # @line L5
            pieces.append((prev, t, s))
        s += delta  # @line L6
        prev = t
    return pieces  # @line L7


def energy(pieces: list[Piece], alpha: int) -> Number:
    """Return the energy, the integral of s(t) ** alpha, of a speed profile."""
    return sum(s ** alpha * (b - a) for a, b, s in pieces)


def edf_run(jobs: list[Job], pieces: list[Piece]) -> list[Number | None]:
    """Run the jobs by earliest deadline first at the given speeds.

    Return the completion time of each job, or None if a job does not
    finish. Every release time must be the start of a piece or fall in
    a gap, which holds for the AVR pieces.
    """
    n = len(jobs)
    order = sorted(range(n), key=lambda j: (jobs[j][0], j))
    rem = [Fraction(w) for _, w, _ in jobs]
    done: list[Number | None] = [None] * n
    heap: list[tuple[Number, int]] = []
    i = 0
    for a, b, s in pieces:
        while i < n and jobs[order[i]][0] <= a:
            j = order[i]
            heapq.heappush(heap, (jobs[j][2], j))
            i += 1
        t = a
        while heap and t < b:
            _, j = heap[0]
            dt = min(rem[j] / s, b - t)
            rem[j] -= s * dt
            t += dt
            if rem[j] == 0:
                heapq.heappop(heap)
                done[j] = t
    return done
