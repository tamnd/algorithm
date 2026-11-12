# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nagle-algorithm/. The authors are listed in prov/0F8CT9.jsonl.

"""Nagle's algorithm (RFC 896) on a simulated TCP connection.

The application writes bytes at given times. With Nagle's rule, the sender
holds a segment that is smaller than the MSS while any sent data is not yet
acknowledged. With nagle=False (the effect of TCP_NODELAY), the sender sends
whatever it has at once. The receiver ACKs every segment, or it uses delayed
ACKs: ACK every second segment, or when a timer of ack_delay expires.
Times are integers (for example milliseconds). The receive window is large,
so flow control never limits the sender here.
"""

import heapq
from typing import NamedTuple


class Result(NamedTuple):
    segments: list[tuple[int, int]]  # (send time, payload bytes)
    finish: int  # time at which the receiver has every byte

    def wire_bytes(self, header: int = 40) -> int:
        return sum(n + header for _, n in self.segments)


def simulate(
    writes: list[tuple[int, int]],
    mss: int,
    delay: int,
    nagle: bool = True,
    ack_delay: int | None = None,
) -> Result:
    """Run the connection. writes holds (time, nbytes) pairs."""
    events: list[tuple[int, int, str, int]] = []
    order = 0

    def push(t: int, kind: str, value: int) -> None:
        nonlocal order
        heapq.heappush(events, (t, order, kind, value))
        order += 1

    for t, n in writes:
        if n <= 0:
            raise ValueError("a write has at least one byte")
        push(t, "write", n)

    buf = 0  # written by the application, not yet sent
    sent = 0  # bytes sent (the next sequence number)
    acked = 0  # bytes acknowledged
    segments: list[tuple[int, int]] = []
    received, pending, timer_on, gen, finish = 0, 0, False, 0, 0
    total = sum(n for _, n in writes)

    def try_send(now: int) -> None:
        nonlocal buf, sent
        while buf > 0:  # @line L3
            if buf >= mss:  # @line L4
                n = mss
            elif not nagle or sent == acked:  # @line L5
                n = buf
            else:
                return  # @line L6
            buf -= n
            sent += n
            segments.append((now, n))
            push(now + delay, "data", n)

    while events:
        now, _, kind, value = heapq.heappop(events)
        if kind == "write":
            buf += value  # @line L1
            try_send(now)
        elif kind == "ack":
            acked = max(acked, value)  # @line L2
            try_send(now)
        elif kind == "data":
            received += value
            if received == total:
                finish = now
            pending += 1
            if ack_delay is None or pending >= 2:
                pending, timer_on = 0, False
                push(now + delay, "ack", received)
            elif not timer_on:
                timer_on = True
                gen += 1
                push(now + ack_delay, "timer", gen)
        elif kind == "timer" and timer_on and value == gen:
            pending, timer_on = 0, False
            push(now + delay, "ack", received)
    return Result(segments, finish)
