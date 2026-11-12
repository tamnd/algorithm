# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-fair-queueing/. The authors are listed in prov/XAQ195.jsonl.

"""Weighted fair queueing, or packet-by-packet GPS (Parekh and Gallager 1993).

The scheduler tracks the virtual time V(t) of the fluid GPS model, which
grows at rate r / (sum of phi over the flows that are backlogged in GPS). A
flow is backlogged in GPS while the finish tag of its last packet is above
V. A packet of L bits of flow i that arrives at time a gets

    S = max(F_prev, V(a)),   F = S + L / phi_i,

and the link sends the queued packet with the least F, without preemption.
All values are Fractions, so ties and bounds are exact.
"""

import heapq
from fractions import Fraction


class WFQ:
    def __init__(self, rate, phi: dict) -> None:
        self.rate = Fraction(rate)
        self.phi = {f: Fraction(w) for f, w in phi.items()}
        self.v = Fraction(0)  # virtual time
        self.clock = Fraction(0)  # time at which v was last brought up to date
        self.last_f: dict = {}  # flow -> F of its last packet
        self.active_heap: list = []  # (F_last, flow); stale entries are skipped
        self.phi_active = Fraction(0)  # sum of phi over the GPS-backlogged flows
        self.packets: list = []  # (F, seq, flow, size, pid)
        self.seq = 0

    def _least_active(self):
        while self.active_heap:
            f, flow = self.active_heap[0]
            if self.last_f[flow] == f:
                return f
            heapq.heappop(self.active_heap)
        return None

    def advance(self, t) -> None:
        """Bring V up to time t, with the GPS departures in between."""
        t = Fraction(t)
        while self.phi_active > 0:  # @line L5
            m = self._least_active()
            dt = (m - self.v) * self.phi_active / self.rate
            if self.clock + dt > t:
                break
            self.clock += dt
            self.v = m
            while self._least_active() == m:  # these flows empty in GPS
                _, flow = heapq.heappop(self.active_heap)
                self.phi_active -= self.phi[flow]
        if self.phi_active > 0:  # @line L6
            self.v += (t - self.clock) * self.rate / self.phi_active
        self.clock = t  # @line L7

    def arrive(self, t, flow, size, pid):
        self.advance(t)  # @line L1
        prev = self.last_f.get(flow, Fraction(0))
        start = max(prev, self.v)  # @line L2
        finish = start + Fraction(size) / self.phi[flow]  # @line L3
        if prev <= self.v:
            self.phi_active += self.phi[flow]  # the flow becomes backlogged in GPS
        self.last_f[flow] = finish
        heapq.heappush(self.active_heap, (finish, flow))
        heapq.heappush(self.packets, (finish, self.seq, flow, size, pid))  # @line L4
        self.seq += 1
        return start, finish

    def next_packet(self):
        if not self.packets:  # @line L8
            return None
        f, _, flow, size, pid = heapq.heappop(self.packets)
        return f, flow, size, pid


def simulate(wfq: WFQ, arrivals):
    """arrivals: list of (time, flow, size) sorted by time. Return a dict
    pid -> (start, finish, F) for the non-preemptive link."""
    out = {}
    i, n = 0, len(arrivals)
    t = Fraction(0)
    while i < n or wfq.packets:
        if not wfq.packets and arrivals[i][0] > t:
            t = Fraction(arrivals[i][0])
        while i < n and arrivals[i][0] <= t:
            a, flow, size = arrivals[i]
            wfq.arrive(a, flow, size, i)
            i += 1
        f, flow, size, pid = wfq.next_packet()
        finish = t + Fraction(size) / wfq.rate
        out[pid] = (t, finish, f)
        t = finish
    return out
