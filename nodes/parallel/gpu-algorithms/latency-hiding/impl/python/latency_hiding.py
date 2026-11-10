# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latency-hiding/.
"""Latency hiding on one warp scheduler, and Little's law.

The scheduler issues at most one warp instruction per cycle, from any warp that is ready. Each
warp runs `ilp` independent dependency chains, interleaved: its instruction k depends on its
instruction k - ilp, and a dependent instruction can issue `latency` cycles after the one it
depends on. Little's law says that the scheduler is busy every cycle only when about
latency x (issue rate) instructions are in flight.
"""

from fractions import Fraction


def needed_parallelism(latency, throughput):
    """Little's law: the work in flight that keeps a pipe of this latency at this throughput."""
    return Fraction(latency) * Fraction(throughput)


def predicted_rate(warps, ilp, latency):
    """Instructions per cycle in steady state: min(1, warps * ilp / latency)."""
    return min(Fraction(1), Fraction(warps * ilp, latency))


def simulate(warps, ilp, latency, per_warp):
    """Cycles to issue per_warp instructions from each warp. Greedy, round robin among ready warps."""
    issued = [0] * warps
    times = [[] for _ in range(warps)]  # issue cycle of each instruction of each warp
    cycle, start, done = 0, 0, 0
    total = warps * per_warp
    while done < total:
        for j in range(warps):  # round robin from `start`
            w = (start + j) % warps
            k = issued[w]
            if k == per_warp:
                continue
            if k >= ilp and times[w][k - ilp] + latency > cycle:
                continue  # waits for the instruction it depends on
            times[w].append(cycle)
            issued[w] += 1
            done += 1
            start = (w + 1) % warps
            break
        cycle += 1
    return cycle


def bytes_in_flight(bandwidth_bytes_per_s, latency_s):
    return Fraction(bandwidth_bytes_per_s) * Fraction(latency_s)
