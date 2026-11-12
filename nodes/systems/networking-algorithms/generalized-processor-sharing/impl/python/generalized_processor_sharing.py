# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-processor-sharing/. The authors are listed in prov/REWV62.jsonl.

"""An exact event-driven simulation of generalized processor sharing (GPS).

A link of rate r serves N flows. Flow i has weight phi[i]. At each instant,
every backlogged flow i is served at rate phi[i] * r / (sum of phi over the
backlogged flows), and the bits of one flow are served in FIFO order. A
packet arrives all at once. All values are Fractions, so the finish times
are exact.

The simulation also tracks the virtual time V(t) of Parekh and Gallager,
which grows at rate r / (sum of phi over the backlogged flows) and stays
constant while the system is empty.
"""

from collections import deque
from fractions import Fraction


def gps(arrivals, phi, rate):
    """arrivals: list of (time, flow, size) sorted by time; phi: dict flow ->
    weight; rate: the link rate.

    Return a dict pid -> (finish time, V at arrival, V at finish), where pid
    is the index of the packet in arrivals.
    """
    rate = Fraction(rate)
    queues = {f: deque() for f in phi}  # flow -> deque of [bits left, pid]
    t = Fraction(0)
    v = Fraction(0)
    v_arrival = {}
    out = {}
    i, n = 0, len(arrivals)
    while True:
        while i < n and arrivals[i][0] <= t:  # take in the arrivals up to t
            _, flow, size = arrivals[i]
            queues[flow].append([Fraction(size), i])
            v_arrival[i] = v
            i += 1
        backlogged = [f for f in phi if queues[f]]
        if not backlogged:
            if i == n:
                return out
            t = Fraction(arrivals[i][0])  # idle: V stays constant
            continue
        total = sum(Fraction(phi[f]) for f in backlogged)
        share = {f: Fraction(phi[f]) * rate / total for f in backlogged}
        dt = min(queues[f][0][0] / share[f] for f in backlogged)
        if i < n and t + dt > arrivals[i][0]:
            dt = Fraction(arrivals[i][0]) - t  # stop at the next arrival
        t += dt
        v += dt * rate / total
        for f in backlogged:
            head = queues[f][0]
            head[0] -= share[f] * dt
            if head[0] == 0:
                queues[f].popleft()
                out[head[1]] = (t, v_arrival[head[1]], v)


def virtual_finish_tags(arrivals, phi, v_arrival):
    """The tags of Parekh and Gallager: S = max(F_prev, V(a)), F = S + L / phi."""
    last = {}
    tags = {}
    for pid, (_, flow, size) in enumerate(arrivals):
        s = max(last.get(flow, Fraction(0)), v_arrival[pid])
        f = s + Fraction(size) / Fraction(phi[flow])
        last[flow] = f
        tags[pid] = f
    return tags
