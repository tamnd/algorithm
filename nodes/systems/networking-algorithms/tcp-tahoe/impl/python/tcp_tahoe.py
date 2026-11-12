# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-tahoe/. The authors are listed in prov/TX7EHD.jsonl.

"""The TCP Tahoe sender (slow start, congestion avoidance, fast retransmit,
and a return to slow start on every loss) in a small discrete-event model.

Units: one segment is one SMSS, so cwnd and ssthresh count segments. The
model has a fixed round-trip time, no rate limit and no queue; the caller
chooses which transmissions are lost. The receiver sends one cumulative ACK
per segment (no delayed ACKs). On a loss the sender goes back to the first
unacknowledged segment, as in the simulations of Fall and Floyd (1996).
"""

import heapq
import itertools
from dataclasses import dataclass, field
from typing import Callable, Optional

DropRule = Callable[[int, int, int], bool]


class TahoeSender:
    """TCP Tahoe. Each handler returns the list of segments to send now."""

    def __init__(self, total: int, iw: int = 1, ssthresh: int = 10**9) -> None:
        self.total = total
        self.cwnd = iw
        self.ssthresh = ssthresh
        self.snd_una = 0
        self.snd_nxt = 0
        self.dupacks = 0
        self.ca_count = 0
        self.timed_out = -1
        self.log: list[tuple[str, int, int]] = []

    def _fill(self) -> list[int]:
        out = []
        while self.snd_nxt < self.total and self.snd_nxt - self.snd_una < self.cwnd:  # @line L8
            out.append(self.snd_nxt)
            self.snd_nxt += 1
        return out

    def _loss(self, why: str, keep_ssthresh: bool = False) -> list[int]:
        if not keep_ssthresh:
            self.ssthresh = max((self.snd_nxt - self.snd_una) // 2, 2)  # @line L9
        self.cwnd = 1  # @line L10
        self.snd_nxt = self.snd_una  # @line L11
        self.ca_count = 0
        self.log.append((why, self.snd_una, self.ssthresh))
        return self._fill()

    def start(self) -> list[int]:
        return self._fill()

    def on_ack(self, a: int) -> list[int]:
        """Handle a cumulative ACK that names the next expected segment a."""
        if a == self.snd_una and self.snd_nxt > self.snd_una:  # @line L1
            self.dupacks += 1  # @line L2
            if self.dupacks == 3:  # @line L3
                return self._loss("fast retransmit")
            return []
        if a > self.snd_una:  # @line L4
            self.snd_una = a  # @line L5
            self.dupacks = 0
            if self.snd_nxt < self.snd_una:
                self.snd_nxt = self.snd_una
            if self.cwnd < self.ssthresh:  # @line L6
                self.cwnd += 1
            else:  # @line L7
                self.ca_count += 1
                if self.ca_count >= self.cwnd:
                    self.cwnd += 1
                    self.ca_count = 0
        return self._fill()

    def on_timeout(self) -> list[int]:
        """Retransmission timeout: the same reaction as three duplicate ACKs.
        A repeated timeout of the same segment keeps ssthresh (RFC 5681)."""
        self.dupacks = 0
        repeated = self.snd_una == self.timed_out
        self.timed_out = self.snd_una
        return self._loss("timeout", keep_ssthresh=repeated)


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


def simulate(sender: TahoeSender, drop: DropRule, rtt: int = 2, rto: int = 8, max_time: int = 10**6) -> Run:
    """Run the sender until all its segments are acknowledged or max_time.

    A segment sent at time t reaches the receiver at t + rtt/2 unless drop
    says it is lost; its ACK reaches the sender at t + rtt. The timer runs
    for the oldest unacknowledged segment, restarts on each ACK of new data
    and doubles on each timeout. Cost: O(T log T) for T transmissions.
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
