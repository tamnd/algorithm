# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/go-back-n/. The authors are listed in prov/AT48F9.jsonl.

"""Go-Back-N ARQ over a simulated unreliable channel.

The sender keeps up to N unacknowledged packets and one timer, for the oldest
of them. On a timeout it resends every unacknowledged packet. The receiver
keeps no buffer: it delivers a packet only if it carries the next expected
sequence number, and it answers every packet with the cumulative ACK(r),
"I expect r next". Sequence numbers have k bits (modulo 2^k), or are
unbounded when k is None.
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
    first. The channel is FIFO.
    """

    def __init__(
        self,
        rng: random.Random | None = None,
        loss: float = 0.0,
        dup: float = 0.0,
        delay: int = 1,
        tx_time: int = 0,
        drop: Callable[[int, Packet], bool] | None = None,
    ) -> None:
        self.rng = rng if rng is not None else random.Random(0)
        self.loss, self.dup, self.delay, self.tx_time, self.drop = loss, dup, delay, tx_time, drop
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
        return [depart + self.tx_time + self.delay] * copies


class Result(NamedTuple):
    delivered: list[Any]
    transmissions: int
    finish: int | None


def go_back_n(
    messages: Sequence[Any],
    data: Channel,
    ack: Channel,
    timeout: int,
    n: int,
    k: int | None = None,
    check: bool = True,
    max_events: int = 1_000_000,
) -> Result:
    """Run Go-Back-N with window n and k-bit sequence numbers.

    Returns the delivered messages, the number of DATA transmissions and the
    time of the last ACK (None if the sender was not done after max_events
    events). With check=True a window n > 2^k - 1 is refused.
    """
    if n < 1 or timeout < 1:
        raise ValueError("the window and the timeout must be at least 1")
    M = None if k is None else 2**k
    if check and M is not None and n > M - 1:
        raise ValueError("Go-Back-N needs a window n <= 2^k - 1")
    heap: list[tuple[int, int, str, Any]] = []
    order = 0

    def push(t: int, kind: str, x: Any) -> None:
        nonlocal order
        heapq.heappush(heap, (t, order, kind, x))
        order += 1

    def wire(j: int) -> int:
        return j % M if M is not None else j

    m = len(messages)
    base = nxt = 0  # @line L1
    timer = 0
    running = False
    transmissions = 0
    r = 0  # receiver: next expected packet; it sends r mod 2^k
    delivered: list[Any] = []
    finish = 0

    def transmit(now: int, j: int) -> None:
        nonlocal transmissions
        pkt = Packet(wire(j), messages[j])
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
        while nxt < m and nxt < base + n:  # @line L2
            transmit(now, nxt)  # @line L3
            if not running:  # @line L4
                start_timer(now)
            nxt += 1  # @line L5

    fill(0)
    steps = 0
    while heap:
        steps += 1
        if steps > max_events:
            return Result(delivered, transmissions, None)
        now, _, kind, x = heapq.heappop(heap)
        if kind == "data":
            if x.seq == wire(r):  # @line L14
                delivered.append(x.data)  # @line L15
                r += 1
            for t in ack.send(now, Packet(wire(r))):  # @line L16
                push(t, "ack", wire(r))
        elif base >= m:
            continue
        elif kind == "ack":  # @line L6
            c = (x - base) % M if M is not None else x - base  # @line L7
            if 1 <= c <= nxt - base:  # @line L8
                base += c
                timer += 1
                running = False
                if base < nxt:  # @line L9
                    start_timer(now)
                if base >= m:
                    finish = now
                fill(now)
        elif kind == "timeout" and x == timer and running:  # @line L10
            start_timer(now)  # @line L11
            for j in range(base, nxt):  # @line L12
                transmit(now, j)  # @line L13
    return Result(delivered, transmissions, finish)
