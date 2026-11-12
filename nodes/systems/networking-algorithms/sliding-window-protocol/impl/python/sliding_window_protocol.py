# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-protocol/. The authors are listed in prov/5PJZGD.jsonl.

"""A general sliding window protocol over a simulated unreliable channel.

The sender may have up to ws packets that are not yet acknowledged. The
receiver buffers up to wr packets ahead of the next one it expects. ACKs are
cumulative: ACK(a) says "I expect sequence number a next". The sender keeps
one timer, for its oldest packet, and resends only that packet on a timeout.
Sequence numbers are taken modulo M, or are unbounded when M is None.
Go-Back-N is the case wr = 1, and selective repeat (with individual ACKs) is
on its own page.
"""

import heapq
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, NamedTuple


@dataclass(frozen=True)
class Packet:
    seq: int
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
    ) -> None:
        self.rng = rng if rng is not None else random.Random(0)
        self.loss, self.dup, self.delay = loss, dup, delay
        self.tx_time, self.jitter, self.drop = tx_time, jitter, drop
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
        copies = 2 if self.rng.random() < self.dup else 1
        base = depart + self.tx_time + self.delay
        return [base + (self.rng.randint(0, self.jitter) if self.jitter else 0) for _ in range(copies)]


class Result(NamedTuple):
    delivered: list[Any]
    transmissions: int
    finish: int | None


def sliding_window(
    messages: Sequence[Any],
    data: Channel,
    ack: Channel,
    timeout: int,
    ws: int,
    wr: int,
    modulus: int | None = None,
    check: bool = True,
    max_events: int = 1_000_000,
) -> Result:
    """Run the protocol and return (delivered, transmissions, finish).

    finish is the time of the last ACK, or None if the sender was still not
    done after max_events events (a livelock, which a too small modulus can
    cause).

    With check=True a modulus with ws + wr > modulus is refused, because the
    receiver can then take an old packet for a new one. Tests turn the check
    off to show the failure.
    """
    if ws < 1 or wr < 1 or timeout < 1:
        raise ValueError("ws, wr and the timeout must be at least 1")
    if check and modulus is not None and ws + wr > modulus:
        raise ValueError("a FIFO channel needs ws + wr <= modulus")
    M = modulus
    heap: list[tuple[int, int, str, Any]] = []
    order = 0

    def push(t: int, kind: str, x: Any) -> None:
        nonlocal order
        heapq.heappush(heap, (t, order, kind, x))
        order += 1

    def wire(n: int) -> int:
        return n % M if M is not None else n

    m = len(messages)
    base = nxt = 0  # sender: oldest unacknowledged packet and next new one  # @line L1
    timer = 0  # id of the running timer, or of the last stopped one
    running = False
    transmissions = 0
    r = 0  # receiver: count of delivered messages, the next one it expects
    buf: dict[int, Any] = {}
    delivered: list[Any] = []
    finish = 0

    def transmit(now: int, n: int) -> None:
        nonlocal transmissions
        pkt = Packet(wire(n), messages[n])
        transmissions += 1
        for t in data.send(now, pkt):
            push(t, "data", pkt)

    def start_timer(now: int) -> None:
        nonlocal timer, running
        timer += 1
        running = True
        push(now + timeout, "timeout", timer)

    def fill(now: int) -> None:
        nonlocal nxt
        while nxt < m and nxt < base + ws:  # @line L2
            transmit(now, nxt)  # @line L3
            if not running:
                start_timer(now)
            nxt += 1

    fill(0)
    steps = 0
    while heap:
        steps += 1
        if steps > max_events:
            return Result(delivered, transmissions, None)  # the sender never finished
        now, _, kind, x = heapq.heappop(heap)
        if kind == "data":
            off = (x.seq - r) % M if M is not None else x.seq - r  # @line L10
            if 0 <= off < wr:  # @line L11
                buf.setdefault(r + off, x.data)
                while r in buf:  # @line L12
                    delivered.append(buf.pop(r))
                    r += 1
            for t in ack.send(now, Packet(wire(r))):  # @line L13
                push(t, "ack", wire(r))
        elif base >= m:
            continue
        elif kind == "ack":  # @line L4
            k = (x - base) % M if M is not None else x - base  # @line L5
            if 1 <= k <= nxt - base:  # @line L6
                base += k
                timer += 1
                running = False
                if base < nxt:  # @line L7
                    start_timer(now)
                if base >= m:
                    finish = now
                fill(now)
        elif kind == "timeout" and x == timer and running:  # @line L8
            transmit(now, base)  # @line L9
            start_timer(now)
    return Result(delivered, transmissions, finish)
