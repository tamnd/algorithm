# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-bit-protocol/. The authors are listed in prov/FAZPQ4.jsonl.

"""The alternating bit protocol over a simulated unreliable channel.

Time is an integer clock, the two directions of the link are discrete-event
models, and every random choice comes from a random.Random object that the
caller passes in.
"""

import heapq
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, NamedTuple


@dataclass(frozen=True)
class Packet:
    bit: int
    data: Any = None


class Channel:
    """One direction of a link.

    A packet sent at time t takes delay ticks to arrive (or delay_fn(i, p)
    ticks for the i-th packet p sent on this channel, counted from 0). It is
    lost with probability loss, or when drop(i, p) is true. With probability
    dup a second copy arrives right after the first. With jitter > 0 each copy
    gets an extra delay in 0 .. jitter, so packets can be reordered. With
    jitter = 0 and no delay_fn the channel is FIFO.
    """

    def __init__(
        self,
        rng: random.Random | None = None,
        loss: float = 0.0,
        dup: float = 0.0,
        delay: int = 1,
        jitter: int = 0,
        drop: Callable[[int, Packet], bool] | None = None,
        delay_fn: Callable[[int, Packet], int] | None = None,
    ) -> None:
        self.rng = rng if rng is not None else random.Random(0)
        self.loss, self.dup, self.delay, self.jitter = loss, dup, delay, jitter
        self.drop, self.delay_fn = drop, delay_fn
        self.sent = 0

    def send(self, now: int, packet: Packet) -> list[int]:
        """Return the arrival times of the copies of packet (empty if lost)."""
        i = self.sent
        self.sent += 1
        lost = self.rng.random() < self.loss
        if lost or (self.drop is not None and self.drop(i, packet)):
            return []
        d = self.delay_fn(i, packet) if self.delay_fn is not None else self.delay
        copies = 2 if self.rng.random() < self.dup else 1
        return [now + d + (self.rng.randint(0, self.jitter) if self.jitter else 0) for _ in range(copies)]


class Result(NamedTuple):
    delivered: list[Any]
    transmissions: int
    finish: int


def alternating_bit(
    messages: Sequence[Any],
    data: Channel,
    ack: Channel,
    timeout: int,
    log: list[tuple[int, str]] | None = None,
    max_events: int = 1_000_000,
) -> Result:
    """Send messages with the alternating bit protocol.

    Message i travels as DATA(i mod 2, message). The receiver delivers a DATA
    packet only if its bit is the bit it expects, and it acknowledges every
    DATA packet with ACK(bit). The sender moves on only on ACK(its bit), and
    it resends on each timeout. If log is a list, one line per event is
    appended to it.

    Returns the delivered messages, the number of DATA transmissions and the
    time of the last ACK that the sender accepted.
    """
    if timeout < 1:
        raise ValueError("the timeout must be at least 1 tick")
    heap: list[tuple[int, int, str, Any]] = []
    order = 0

    def push(t: int, kind: str, x: Any) -> None:
        nonlocal order
        heapq.heappush(heap, (t, order, kind, x))
        order += 1

    def note(t: int, text: str) -> None:
        if log is not None:
            log.append((t, text))

    m = len(messages)
    i = 0  # sender: index of the message in flight  # @line L1
    b = 0  # sender: its bit, i mod 2
    timer = 0
    transmissions = 0
    e = 0  # receiver: the bit it expects  # @line L8
    delivered: list[Any] = []
    finish = 0

    def send_current(now: int) -> None:
        nonlocal timer, transmissions
        pkt = Packet(b, messages[i])
        transmissions += 1
        arrivals = data.send(now, pkt)  # @line L3
        note(now, f"send DATA({b}, {messages[i]!r})" + ("" if arrivals else ", lost"))
        for t in arrivals:
            push(t, "data", pkt)
        timer += 1
        push(now + timeout, "timeout", timer)

    if m:  # @line L2
        send_current(0)
    steps = 0
    while heap:
        steps += 1
        if steps > max_events:
            raise RuntimeError("too many events; is the loss rate 1?")
        now, _, kind, x = heapq.heappop(heap)
        if kind == "data":
            if x.bit == e:  # @line L9
                delivered.append(x.data)  # @line L10
                e ^= 1
                note(now, f"receive DATA({x.bit}, {x.data!r}), deliver")
            else:
                note(now, f"receive DATA({x.bit}, {x.data!r}), duplicate")
            arrivals = ack.send(now, Packet(x.bit))  # @line L11
            note(now, f"send ACK({x.bit})" + ("" if arrivals else ", lost"))
            for t in arrivals:
                push(t, "ack", x.bit)
        elif i >= m:
            continue
        elif kind == "ack":
            if x == b:  # @line L4
                note(now, f"receive ACK({x}), next message")
                timer += 1
                i += 1  # @line L6
                b ^= 1  # @line L7
                if i < m:
                    send_current(now)
                else:
                    finish = now
            else:
                note(now, f"receive ACK({x}), ignore")  # @line L5
        elif kind == "timeout" and x == timer:
            note(now, "timeout")
            send_current(now)  # @line L5
    return Result(delivered, transmissions, finish)
