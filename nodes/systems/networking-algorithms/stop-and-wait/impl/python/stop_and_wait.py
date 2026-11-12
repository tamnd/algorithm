# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stop-and-wait/. The authors are listed in prov/R0TNQW.jsonl.

"""Stop-and-wait ARQ over a simulated unreliable channel.

Time is an integer clock. Nothing here opens a socket or sleeps: the two
directions of the link are discrete-event models, and every random choice
comes from a random.Random object that the caller passes in.
"""

import heapq
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, NamedTuple


@dataclass(frozen=True)
class Packet:
    seq: int | None
    data: Any = None


class Channel:
    """One direction of a link.

    A packet sent at time t leaves when the link is free, takes tx_time ticks
    to transmit and delay ticks to propagate. It is lost with probability
    loss, or when drop(i, packet) is true for the i-th packet (from 0) sent on
    this channel. With probability dup a second copy arrives right after the
    first. With jitter > 0 each copy gets an extra delay in 0 .. jitter, so
    the channel can reorder packets; with jitter = 0 it is FIFO.
    """

    def __init__(
        self,
        rng: random.Random | None = None,
        loss: float = 0.0,
        dup: float = 0.0,
        delay: int = 1,
        tx_time: int = 0,
        jitter: int = 0,
        drop: Callable[[int, Packet], bool] | None = None,
        delay_fn: Callable[[int, Packet], int] | None = None,
    ) -> None:
        self.rng = rng if rng is not None else random.Random(0)
        self.loss, self.dup, self.delay = loss, dup, delay
        self.tx_time, self.jitter = tx_time, jitter
        self.drop, self.delay_fn = drop, delay_fn
        self.sent = 0
        self.free_at = 0

    def send(self, now: int, packet: Packet) -> list[int]:
        """Return the arrival times of the copies of packet (empty if lost)."""
        i = self.sent
        self.sent += 1
        depart = max(now, self.free_at)
        self.free_at = depart + self.tx_time
        lost = self.rng.random() < self.loss
        if lost or (self.drop is not None and self.drop(i, packet)):
            return []
        d = self.delay_fn(i, packet) if self.delay_fn is not None else self.delay
        copies = 2 if self.rng.random() < self.dup else 1
        return [
            depart + self.tx_time + d + (self.rng.randint(0, self.jitter) if self.jitter else 0)
            for _ in range(copies)
        ]


class Result(NamedTuple):
    delivered: list[Any]
    transmissions: int
    finish: int


class _Events:
    def __init__(self) -> None:
        self.heap: list[tuple[int, int, str, Any]] = []
        self.n = 0

    def push(self, t: int, kind: str, x: Any) -> None:
        heapq.heappush(self.heap, (t, self.n, kind, x))
        self.n += 1

    def pop(self) -> tuple[int, str, Any]:
        t, _, kind, x = heapq.heappop(self.heap)
        return t, kind, x


def stop_and_wait(
    messages: Sequence[Any],
    data: Channel,
    ack: Channel,
    timeout: int,
    numbered: bool = True,
    max_events: int = 1_000_000,
) -> Result:
    """Send messages one at a time; each one waits for its ACK.

    With numbered=True the packets carry the sequence numbers 0, 1, 2, ...
    (unbounded) and the receiver delivers DATA(s) only when s is the next
    number it expects. With numbered=False there are no sequence numbers,
    which is the broken protocol of the Pitfalls section: a lost ACK makes
    the receiver deliver a duplicate.

    Returns the delivered messages, the number of DATA transmissions and the
    time at which the sender got the last ACK.
    """
    if timeout < 1:
        raise ValueError("the timeout must be at least 1 tick")
    ev = _Events()
    m = len(messages)
    i = 0  # sender: index of the message in flight
    timer = 0  # id of the running timer; a stale timeout has an older id
    transmissions = 0
    r = 0  # receiver: next sequence number it expects  # @line L6
    delivered: list[Any] = []
    finish = 0

    def send_current(now: int) -> None:
        nonlocal timer, transmissions
        pkt = Packet(i if numbered else None, messages[i])
        transmissions += 1
        for t in data.send(now, pkt):  # @line L2
            ev.push(t, "data", pkt)
        timer += 1
        ev.push(now + timeout, "timeout", timer)

    if m:
        send_current(0)
    steps = 0
    while ev.heap:
        steps += 1
        if steps > max_events:
            raise RuntimeError("too many events; is the loss rate 1?")
        now, kind, x = ev.pop()
        if kind == "data":  # @line L7
            if not numbered or x.seq == r:  # @line L8
                delivered.append(x.data)
                r += 1
            for t in ack.send(now, Packet(x.seq)):  # @line L9
                ev.push(t, "ack", x.seq)
        elif i >= m:
            continue  # the sender is done; only the receiver still acts
        elif kind == "ack" and (not numbered or x == i):  # @line L3
            timer += 1  # @line L5
            i += 1  # @line L1
            if i < m:
                send_current(now)
            else:
                finish = now
        elif kind == "timeout" and x == timer:  # @line L4
            send_current(now)
    return Result(delivered, transmissions, finish)


def utilization(frame_bits: int, rate: Fraction | int, rtt: Fraction | int) -> Fraction:
    """Sender utilization (L/R) / (RTT + L/R) of stop-and-wait with no loss."""
    t = Fraction(frame_bits) / Fraction(rate)
    return t / (Fraction(rtt) + t)
