# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fair-queueing/. The authors are listed in prov/YH4B2M.jsonl.

"""Fair queueing of Demers, Keshav and Shenker (SIGCOMM 1989).

The scheduler simulates bit-by-bit round robin with a round number R(t),
which grows at rate r / N_active, where N_active is the number of flows that
still have bits in the bit-by-bit model. A packet of P bytes of flow i that
arrives at time t gets the finish number F = max(F_last[i], R(t)) + P. The
link sends the queued packet with the least F, and never preempts.

Times, rates and sizes may be ints or Fractions; with Fractions all values
are exact.
"""

import heapq
from fractions import Fraction


class FairQueueing:
    def __init__(self, rate) -> None:
        self.rate = Fraction(rate)  # bytes per unit of time
        self.R = Fraction(0)  # the round number
        self.clock = Fraction(0)  # the time at which R was last brought up to date
        self.last_f: dict = {}  # flow -> finish number of its last packet
        self.active_heap: list = []  # (F_last, flow), with stale entries
        self.n_active = 0
        self.packets: list = []  # (F, seq, flow, size, pid)
        self.seq = 0

    def _least_active(self):
        """The least F_last of an active flow. The valid heap entries are
        exactly the active flows; an entry is stale when its flow got a
        newer packet."""
        while self.active_heap:
            f, flow = self.active_heap[0]
            if self.last_f[flow] == f:
                return f
            heapq.heappop(self.active_heap)
        return None

    def advance(self, t) -> None:
        """Bring the round number up to time t."""
        t = Fraction(t)
        while self.n_active > 0:  # @line L5
            fmin = self._least_active()
            dt = (fmin - self.R) * self.n_active / self.rate
            if self.clock + dt > t:
                break
            self.clock += dt
            self.R = fmin
            while self._least_active() == fmin:  # these flows become inactive
                heapq.heappop(self.active_heap)
                self.n_active -= 1
        if self.n_active > 0:  # @line L6
            self.R += (t - self.clock) * self.rate / self.n_active
        self.clock = t  # @line L7

    def arrive(self, t, flow, size, pid):
        """A packet of size bytes of the given flow arrives at time t."""
        self.advance(t)  # @line L1
        prev = self.last_f.get(flow, Fraction(0))
        if prev <= self.R:
            self.n_active += 1  # the flow becomes active
        f = max(prev, self.R) + size  # @line L2
        self.last_f[flow] = f  # @line L3
        heapq.heappush(self.active_heap, (f, flow))
        heapq.heappush(self.packets, (f, self.seq, flow, size, pid))  # @line L4
        self.seq += 1
        return f

    def next_packet(self):
        """Return (F, flow, size, pid) of the packet to send, or None."""
        if not self.packets:  # @line L8
            return None
        f, _, flow, size, pid = heapq.heappop(self.packets)
        return f, flow, size, pid


def simulate(fq: FairQueueing, arrivals):
    """arrivals: list of (time, flow, size), sorted by time.

    Return a dict pid -> (start, finish, F), where pid is the index in the
    list. The link is non-preemptive and work conserving.
    """
    out = {}
    i = 0
    n = len(arrivals)
    t = Fraction(0)
    while i < n or fq.packets:
        if not fq.packets and arrivals[i][0] > t:
            t = Fraction(arrivals[i][0])
        while i < n and arrivals[i][0] <= t:
            a, flow, size = arrivals[i]
            fq.arrive(a, flow, size, i)
            i += 1
        f, flow, size, pid = fq.next_packet()
        finish = t + size / fq.rate
        out[pid] = (t, finish, f)
        t = finish
    return out
