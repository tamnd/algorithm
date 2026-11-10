# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-clocks/. The authors are listed in prov/R8TGNF.jsonl.

"""Lamport logical clocks (Lamport 1978, rules IR1 and IR2).

The model is the asynchronous message-passing model with n processes
0 .. n - 1 and reliable channels that need not be FIFO. An execution is a
list of steps in the order they occur:

    (p, "local", None)      process p does a local event
    (p, "send", (q, mid))   process p sends message mid to process q
    (p, "recv", mid)        process p receives message mid

Each step is one event. A receive step names a message that was sent
earlier and not yet received. Cost: O(1) time and one integer of space per
event, per process and per message.
"""

import random


class LamportClock:
    """The clock C_i of one process."""

    def __init__(self, pid: int) -> None:
        self.pid = pid
        self.c = 0  # @line L1

    def local_event(self) -> int:
        """IR1: tick before the event. Return the timestamp of the event."""
        self.c += 1  # @line L2
        return self.c  # @line L3

    def send(self) -> int:
        """IR1 then IR2(a): tick, and return the timestamp T_m for the message."""
        self.c += 1  # @line L4
        return self.c  # @line L6

    def receive(self, t_m: int) -> int:
        """IR2(b) and IR1: jump past T_m and past the present value."""
        self.c = max(self.c, t_m) + 1  # @line L7
        return self.c  # @line L8


def timestamp_execution(n: int, execution: list[tuple]) -> list[int]:
    """Run one Lamport clock per process over the execution.

    Precondition: each receive names a message sent earlier in the list.
    Return C(e) for each event e, in execution order. Time O(len(execution)).
    """
    clocks = [LamportClock(p) for p in range(n)]
    stamp_of_msg: dict[int, int] = {}
    out: list[int] = []
    for p, kind, x in execution:
        if kind == "local":
            out.append(clocks[p].local_event())
        elif kind == "send":
            t = clocks[p].send()
            stamp_of_msg[x[1]] = t  # @line L5
            out.append(t)
        elif kind == "recv":
            out.append(clocks[p].receive(stamp_of_msg[x]))
        else:
            raise ValueError(f"unknown step kind {kind!r}")
    return out


def total_order_key(c: int, pid: int) -> tuple[int, int]:
    """The key of Lamport's total order: compare C first, then the process id."""
    return (c, pid)


def random_execution(n: int, steps: int, rng: random.Random, p_send: float = 0.4, p_recv: float = 0.4) -> list[tuple]:
    """A seeded random execution. In-transit messages are received in a random order."""
    in_transit: list[tuple[int, int]] = []
    out: list[tuple] = []
    mid = 0
    for _ in range(steps):
        r = rng.random()
        if r < p_recv and in_transit:
            m, q = in_transit.pop(rng.randrange(len(in_transit)))
            out.append((q, "recv", m))
        elif r < p_recv + p_send and n > 1:
            p = rng.randrange(n)
            q = rng.randrange(n - 1)
            q += q >= p
            out.append((p, "send", (q, mid)))
            in_transit.append((mid, q))
            mid += 1
        else:
            out.append((rng.randrange(n), "local", None))
    return out
