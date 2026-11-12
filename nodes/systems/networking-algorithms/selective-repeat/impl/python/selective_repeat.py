# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-repeat/. The authors are listed in prov/NTM3PJ.jsonl.

"""Selective repeat ARQ over a simulated unreliable channel.

Both ends have a window of w sequence numbers. The sender keeps one timer for
each unacknowledged packet and resends only the packet whose timer expires.
The receiver buffers packets inside its window, acknowledges each packet
individually with ACK(seq), and delivers the buffered packets in order.
Sequence numbers have k bits (modulo 2^k), or are unbounded when k is None.
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


def selective_repeat(
    messages: Sequence[Any],
    data: Channel,
    ack: Channel,
    timeout: int,
    w: int,
    k: int | None = None,
    check: bool = True,
    max_events: int = 1_000_000,
) -> Result:
    """Run selective repeat with window w and k-bit sequence numbers.

    Returns the delivered messages, the number of DATA transmissions and the
    time of the last ACK (None if the sender was not done after max_events
    events). With check=True a window w > 2^(k-1) is refused.
    """
    if w < 1 or timeout < 1:
        raise ValueError("the window and the timeout must be at least 1")
    M = None if k is None else 2**k
    if check and M is not None and 2 * w > M:
        raise ValueError("selective repeat needs a window w <= 2^(k-1)")
    heap: list[tuple[int, int, str, Any]] = []
    order = 0

    def push(t: int, kind: str, x: Any) -> None:
        nonlocal order
        heapq.heappush(heap, (t, order, kind, x))
        order += 1

    def wire(j: int) -> int:
        return j % M if M is not None else j

    def offset(s: int, origin: int) -> int:
        return (s - origin) % M if M is not None else s - origin

    m = len(messages)
    base = nxt = 0
    acked: set[int] = set()
    timer_id: dict[int, int] = {}
    ids = 0
    transmissions = 0
    r = 0  # receiver: next packet to deliver, the base of its window
    buf: dict[int, Any] = {}
    delivered: list[Any] = []
    finish = 0

    def transmit(now: int, j: int) -> None:
        nonlocal transmissions, ids
        pkt = Packet(wire(j), messages[j])
        transmissions += 1
        for t in data.send(now, pkt):
            push(t, "data", pkt)
        ids += 1
        timer_id[j] = ids
        push(now + timeout, "timeout", (j, ids))

    def fill(now: int) -> None:
        nonlocal nxt
        while nxt < m and nxt < base + w:  # @line L1
            transmit(now, nxt)  # @line L2
            nxt += 1

    fill(0)
    steps = 0
    while heap:
        steps += 1
        if steps > max_events:
            return Result(delivered, transmissions, None)
        now, _, kind, x = heapq.heappop(heap)
        if kind == "data":
            off = offset(x.seq, r)  # @line L9
            if 0 <= off < w:  # @line L10
                buf.setdefault(r + off, x.data)  # @line L11
                send_ack = True
                while r in buf:  # @line L12
                    delivered.append(buf.pop(r))
                    r += 1
            else:
                old = off >= M - w if M is not None else -w <= off < 0  # @line L13
                send_ack = old  # @line L14
            if send_ack:
                for t in ack.send(now, Packet(x.seq)):  # @line L11
                    push(t, "ack", x.seq)
        elif base >= m:
            continue
        elif kind == "ack":  # @line L3
            off = offset(x, base)  # @line L4
            if 0 <= off < nxt - base:  # @line L5
                acked.add(base + off)
                timer_id.pop(base + off, None)
                while base in acked:  # @line L6
                    acked.discard(base)
                    base += 1
                if base >= m:
                    finish = now
                fill(now)
        elif kind == "timeout":
            j, tid = x
            if timer_id.get(j) == tid:  # @line L7
                transmit(now, j)  # @line L8
    return Result(delivered, transmissions, finish)
