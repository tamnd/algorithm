# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-retransmit-fast-recovery/. The authors are listed in prov/RVRJVD.jsonl.

"""Fast retransmit and fast recovery (RFC 5681, Section 3.2), with the
NewReno change for partial ACKs (RFC 6582), in a small discrete-event model.

Units: one segment is one SMSS, so cwnd and ssthresh count segments. The
model has a fixed round-trip time, no rate limit and no queue. The caller
chooses which transmissions are lost. The receiver sends one cumulative ACK
for each segment that it gets (no delayed ACKs).
"""

import heapq
import itertools
from dataclasses import dataclass, field
from typing import Callable, Optional

DropRule = Callable[[int, int, int], bool]


class FastRecoverySender:
    """A TCP sender with slow start, congestion avoidance, fast retransmit
    and fast recovery. With newreno=True, a partial ACK keeps the sender in
    fast recovery and resends the next hole (RFC 6582).

    Each event handler returns the list of segment numbers to transmit now.
    """

    def __init__(self, total: int, iw: int = 1, ssthresh: int = 10**9, newreno: bool = False) -> None:
        self.total = total
        self.cwnd = iw
        self.ssthresh = ssthresh
        self.newreno = newreno
        self.snd_una = 0
        self.snd_nxt = 0
        self.dupacks = 0
        self.in_recovery = False
        self.recover = -1
        self.ca_count = 0
        self.timed_out = -1
        self.log: list[tuple[str, int, int]] = []

    def _fill(self) -> list[int]:
        out = []
        while self.snd_nxt < self.total and self.snd_nxt - self.snd_una < self.cwnd:  # @line L18
            out.append(self.snd_nxt)
            self.snd_nxt += 1
        return out

    def _grow(self) -> None:
        if self.cwnd < self.ssthresh:
            self.cwnd += 1  # slow start: one segment per ACK
        else:
            self.ca_count += 1  # congestion avoidance: one segment per window of ACKs
            if self.ca_count >= self.cwnd:
                self.cwnd += 1
                self.ca_count = 0

    def start(self) -> list[int]:
        return self._fill()

    def on_ack(self, a: int) -> list[int]:
        """Handle a cumulative ACK that names the next expected segment a."""
        out: list[int] = []
        if a == self.snd_una and self.snd_nxt > self.snd_una:  # @line L1
            if self.in_recovery:  # @line L2
                self.cwnd += 1
            else:  # @line L3
                self.dupacks += 1  # @line L4
                if self.dupacks == 3 and (not self.newreno or a > self.recover):  # @line L5
                    self.ssthresh = max((self.snd_nxt - self.snd_una) // 2, 2)  # @line L6
                    self.recover = self.snd_nxt - 1  # @line L7
                    out.append(self.snd_una)  # @line L8
                    self.cwnd = self.ssthresh + 3  # @line L9
                    self.in_recovery = True
                    self.log.append(("fast retransmit", self.snd_una, self.cwnd))
        elif a > self.snd_una:  # @line L10
            acked = a - self.snd_una  # @line L11
            self.snd_una = a
            self.dupacks = 0
            if self.snd_nxt < self.snd_una:
                self.snd_nxt = self.snd_una
            if self.in_recovery and self.newreno and a <= self.recover:  # @line L12
                out.append(self.snd_una)  # @line L13
                self.cwnd = max(self.cwnd - acked + 1, 1)  # @line L14
                self.log.append(("partial ack", self.snd_una, self.cwnd))
            elif self.in_recovery:  # @line L15
                self.cwnd = self.ssthresh  # @line L16
                self.in_recovery = False
                self.ca_count = 0
                self.log.append(("exit recovery", self.snd_una, self.cwnd))
            else:
                self._grow()  # @line L17
        return out + self._fill()

    def on_timeout(self) -> list[int]:
        """Retransmission timeout: RFC 5681 loss window, go back to snd_una.
        A repeated timeout of the same segment keeps ssthresh."""
        if self.snd_una != self.timed_out:
            self.ssthresh = max((self.snd_nxt - self.snd_una) // 2, 2)
        self.timed_out = self.snd_una
        self.recover = self.snd_nxt - 1
        self.cwnd = 1
        self.snd_nxt = self.snd_una
        self.dupacks = 0
        self.in_recovery = False
        self.ca_count = 0
        self.log.append(("timeout", self.snd_una, self.cwnd))
        return self._fill()


@dataclass
class Run:
    delivered: list[int] = field(default_factory=list)
    trace: list[tuple[int, int, int, int]] = field(default_factory=list)
    transmissions: int = 0
    timeouts: int = 0
    finish: Optional[int] = None


def lose_first(seqs: set[int]) -> DropRule:
    """Drop the first transmission of each segment in seqs."""
    return lambda seq, k, n: k == 1 and seq in seqs


def simulate(sender, drop: DropRule, rtt: int = 2, rto: int = 8, max_time: int = 10**6) -> Run:
    """Run the sender until all its segments are acknowledged or max_time.

    A segment sent at time t reaches the receiver at t + rtt/2 unless drop
    says it is lost; its ACK reaches the sender at t + rtt. The timer runs
    for the oldest unacknowledged segment, restarts on each ACK of new data
    and doubles on each timeout. trace holds (time, ack, cwnd, ssthresh)
    after each ACK. Cost: O(T log T) for T transmissions.
    """
    half = rtt // 2
    run = Run()
    events: list[tuple[int, int, str, int]] = []
    order = itertools.count()
    tx: dict[int, int] = {}
    rcv_nxt = 0
    buffered: set[int] = set()
    timer: Optional[int] = None
    backoff = 1

    def transmit(segs: list[int], now: int) -> None:
        nonlocal timer
        for s in segs:
            tx[s] = tx.get(s, 0) + 1
            run.transmissions += 1
            if not drop(s, tx[s], run.transmissions):
                heapq.heappush(events, (now + half, next(order), "data", s))
        if timer is None and sender.snd_nxt > sender.snd_una:
            timer = now + rto * backoff

    transmit(sender.start(), 0)
    while sender.snd_una < sender.total:
        if timer is not None and (not events or timer < events[0][0]):
            now = timer
            if now > max_time:
                break
            run.timeouts += 1
            backoff *= 2
            timer = None
            transmit(sender.on_timeout(), now)
            continue
        if not events:
            break
        now, _, kind, value = heapq.heappop(events)
        if now > max_time:
            break
        if kind == "data":
            if value >= rcv_nxt:
                buffered.add(value)
            while rcv_nxt in buffered:
                buffered.remove(rcv_nxt)
                run.delivered.append(rcv_nxt)
                rcv_nxt += 1
            heapq.heappush(events, (now + half, next(order), "ack", rcv_nxt))
        else:
            before = sender.snd_una
            segs = sender.on_ack(value)
            if sender.snd_una > before:
                backoff = 1
                timer = now + rto if sender.snd_nxt > sender.snd_una else None
            run.trace.append((now, value, sender.cwnd, sender.ssthresh))
            transmit(segs, now)
    if sender.snd_una >= sender.total:
        run.finish = run.trace[-1][0] if run.trace else 0
    return run
