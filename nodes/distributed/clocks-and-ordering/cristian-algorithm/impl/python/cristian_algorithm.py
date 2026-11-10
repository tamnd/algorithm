# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cristian-algorithm/. The authors are listed in prov/F0PB77.jsonl.

"""Cristian's probabilistic clock reading, run in a small deterministic simulator.

Model. The time server S has a correct clock: its reading is real time t. The
client clock is C(t) = c0 + integral of its rate, and the rate stays in
[1 - rho, 1 + rho]; here the rate is a constant chosen by the caller. Each
one-way delay is at least dmin. The server may hold the request for a while
before it reads its clock, and again before it replies; both waits are inside
the round trip, so the bound still holds.

One attempt (lines L1 to L6 of the page):
  T0 <- client clock, send a request
  the server reads T = its clock at some instant, and replies with T
  T1 <- client clock when the reply arrives, RTT <- T1 - T0
  estimate <- T + RTT / (2 (1 - rho))     (T + RTT / 2 when rho = 0)
  the error bound is RTT / (2 (1 - rho)) - dmin

The client retries until RTT <= 2 U, so that the bound is at most about U - dmin.
"""

import random
from dataclasses import dataclass
from typing import Callable, Optional

DelayFn = Callable[[random.Random], float]


@dataclass
class Reading:
    t0: float  # client clock at the send
    t1: float  # client clock at the receipt
    server_time: float  # the value T in the reply
    true_time: float  # real time at the receipt (the simulator knows it)
    d1: float  # request delay
    d2: float  # reply delay

    @property
    def rtt(self) -> float:
        return self.t1 - self.t0


class Client:
    """A client clock with a constant rate and an offset from real time."""

    def __init__(self, offset: float, rate: float = 1.0) -> None:
        self.offset = offset
        self.rate = rate

    def read(self, t: float) -> float:
        return self.offset + self.rate * t


def one_reading(client: Client, start: float, d1: float, d2: float, hold: float, read_frac: float) -> Reading:
    """Simulate one request sent at real time `start`."""
    t0 = client.read(start)  # @line L1
    arrive = start + d1
    t_read = arrive + read_frac * hold  # the server reads its clock here
    t_back = arrive + hold + d2
    t1 = client.read(t_back)  # @line L2
    return Reading(t0=t0, t1=t1, server_time=t_read, true_time=t_back, d1=d1, d2=d2)


def estimate(r: Reading, rho: float = 0.0) -> tuple[float, float]:
    """Return (the new clock value, the error bound) for a reading."""
    half = r.rtt / (2.0 * (1.0 - rho))  # @line L3
    return r.server_time + half, half  # @line L4


def cristian(
    client: Client,
    dmin: float,
    delay: DelayFn,
    target: float,
    rng: random.Random,
    rho: float = 0.0,
    hold: float = 0.0,
    max_tries: int = 1000,
    start: float = 0.0,
) -> tuple[Optional[Reading], int, float]:
    """Retry until the round trip is at most 2 * target.

    Returns (the accepted reading or None, the number of attempts, the real
    time at the end). `delay(rng)` returns a one-way delay of at least dmin.
    """
    t = start
    for attempt in range(1, max_tries + 1):  # @line L5
        d1, d2 = delay(rng), delay(rng)
        assert d1 >= dmin and d2 >= dmin
        r = one_reading(client, t, d1, d2, hold, rng.random())
        t = r.true_time
        if r.rtt <= 2.0 * target:  # @line L6
            return r, attempt, t
    return None, max_tries, t


def error_of(r: Reading, rho: float = 0.0) -> float:
    """The real error of the estimate: estimate minus real time at the receipt."""
    value, _ = estimate(r, rho)
    return value - r.true_time
