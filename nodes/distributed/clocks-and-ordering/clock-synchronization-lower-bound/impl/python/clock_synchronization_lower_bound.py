# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-synchronization-lower-bound/. The authors are listed in prov/1YP4C2.jsonl.

"""Executions, views and shifts for the Lundelius and Lynch bound.

Model. n processes with drift-free hardware clocks H_i(t) = t + c[i]. Each
message from i to j takes delay[i][j] in [d - u, d]. Each process i sends one
message at local time 0 that holds its clock value 0, to every other process.
A deterministic algorithm maps the view of a process (the list of (sender,
value, local receipt time)) to an adjustment adj_i. The adjusted clock is
H_i(t) + adj_i, so its offset from real time is A_i = c[i] + adj_i, and the
skew is max A_i - min A_i.

Shift by x: process i runs x[i] earlier in real time with the same local times,
so c'[i] = c[i] + x[i] and delay'[i][j] = delay[i][j] + x[i] - x[j]. No process
can tell the two executions apart, and A'_i = A_i + x[i].

Code cannot prove a lower bound for every algorithm. It can build the
executions of the proof, check that each process has the same view in all of
them, and check the bound for the algorithms it runs.
"""

from typing import Callable

View = tuple[tuple[int, float, float], ...]
Algorithm = Callable[[int, int, View, float, float], float]  # (i, n, view, d, u) -> adj_i


def views(c: list[float], delay: list[list[float]]) -> list[View]:
    n = len(c)
    out = []
    for j in range(n):
        got = []
        for i in range(n):
            if i != j:
                send_real = 0.0 - c[i]  # local time 0 at process i
                recv_local = send_real + delay[i][j] + c[j]
                got.append((i, 0.0, recv_local))
        out.append(tuple(sorted(got)))
    return out


def run(alg: Algorithm, c: list[float], delay: list[list[float]], d: float, u: float) -> tuple[list[View], list[float]]:
    """Return the views and the offsets A_i of the adjusted clocks."""
    n = len(c)
    for i in range(n):
        for j in range(n):
            if i != j and not (d - u - 1e-12 <= delay[i][j] <= d + 1e-12):
                raise ValueError("delay outside [d - u, d]")
    vs = views(c, delay)
    return vs, [c[i] + alg(i, n, vs[i], d, u) for i in range(n)]


def skew(a: list[float]) -> float:
    return max(a) - min(a)


def shift(c: list[float], delay: list[list[float]], x: list[float]) -> tuple[list[float], list[list[float]]]:
    n = len(c)
    c2 = [c[i] + x[i] for i in range(n)]
    d2 = [[delay[i][j] + x[i] - x[j] if i != j else 0.0 for j in range(n)] for i in range(n)]
    return c2, d2


def averaging(i: int, n: int, view: View, d: float, u: float) -> float:
    """The algorithm of Lundelius and Lynch: estimate each other clock with the
    middle delay d - u/2, and move to the average of the estimates (own clock
    counts with difference 0)."""
    diffs = [value + (d - u / 2) - recv for _, value, recv in view]  # estimates of H_j - H_i
    return sum(diffs) / n


def follow(leader: int, guess_frac: float) -> Algorithm:
    """Each process copies the clock of `leader`, with the delay guessed as
    d - u + guess_frac * u."""

    def alg(i: int, n: int, view: View, d: float, u: float) -> float:
        if i == leader:
            return 0.0
        for j, value, recv in view:
            if j == leader:
                return value + (d - u + guess_frac * u) - recv
        raise AssertionError

    return alg


def weighted(weights: list[float], guess_frac: float) -> Algorithm:
    """A family: adj_i = sum over j of weights[j] * (estimate of H_j - H_i)."""

    def alg(i: int, n: int, view: View, d: float, u: float) -> float:
        est = {i: 0.0}
        for j, value, recv in view:
            est[j] = value + (d - u + guess_frac * u) - recv
        return sum(weights[j] * est[j] for j in range(n))

    return alg


def chain_executions(n: int, d: float, u: float, c0: list[float]) -> list[tuple[list[float], list[list[float]]]]:
    """alpha_0 has delay d - u from p_i to p_j when i < j and d when i > j.
    alpha_k shifts p_0 .. p_(k-1) by u. All of them are admissible."""
    delay0 = [[(d - u if i < j else d) if i != j else 0.0 for j in range(n)] for i in range(n)]
    out = []
    for k in range(n):
        x = [u if i < k else 0.0 for i in range(n)]
        out.append(shift(c0, delay0, x))
    return out
