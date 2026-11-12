# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connection-draining/. The authors are listed in prov/T00ABF.jsonl.

"""Connection draining at a request-level load balancer, and the HTTP/2
GOAWAY handshake.

Model: an integer clock. Each request has an arrival time and a duration; a
request that starts at time a on a backend ends at a + duration. In one tick
the balancer first finishes the requests that end at that tick, then applies
the drain deadlines, then routes the new arrivals. The balancer picks the
active backend with the fewest requests in flight (lowest index on a tie). It
learns of a drain `lag` ticks after the drain starts, which models the delay
until a deregistration reaches every balancer.
"""

import random
from dataclasses import dataclass, field

ACTIVE, DRAINING, REMOVED = "active", "draining", "removed"


@dataclass
class Backend:
    state: str = ACTIVE
    inflight: dict[int, int] = field(default_factory=dict)  # request id -> end time
    drain_start: int = -1
    deadline: int = -1
    refuse_from: int | None = None  # the backend refuses new requests from this time
    removed_at: int = -1


class Balancer:
    def __init__(self, n: int, lag: int = 0) -> None:
        self.backends = [Backend() for _ in range(n)]
        self.lag = lag
        self.assigned: dict[int, tuple[int, int, int]] = {}  # id -> (backend, start, end)
        self.completed: set[int] = set()
        self.cut: set[int] = set()
        self.errors: list[tuple[int, int]] = []  # (request id, backend) refused at arrival

    def drain(self, b: int, now: int, timeout: int, refuse_after: int | None = None) -> None:
        be = self.backends[b]
        be.state, be.drain_start, be.deadline = DRAINING, now, now + timeout  # @line L1
        if refuse_after is not None:
            be.refuse_from = now + refuse_after

    def _routable(self, b: int, now: int) -> bool:
        be = self.backends[b]
        if be.state == ACTIVE:
            return True
        return be.state == DRAINING and now < be.drain_start + self.lag  # not yet seen

    def tick(self, now: int) -> None:
        for b, be in enumerate(self.backends):
            for rid, end in list(be.inflight.items()):
                if end <= now:  # @line L5
                    del be.inflight[rid]
                    self.completed.add(rid)
            if be.state != DRAINING:
                continue
            if now >= be.deadline:  # @line L6
                for rid in be.inflight:
                    self.cut.add(rid)
                be.inflight.clear()
                be.state, be.removed_at = REMOVED, now  # @line L7
            elif not be.inflight and now >= be.drain_start + self.lag:  # @line L8
                be.state, be.removed_at = REMOVED, now

    def arrive(self, rid: int, now: int, duration: int) -> int | None:
        cands = [b for b in range(len(self.backends)) if self._routable(b, now)]  # @line L2
        if not cands:
            self.errors.append((rid, -1))
            return None
        b = min(cands, key=lambda i: (len(self.backends[i].inflight), i))  # @line L3
        be = self.backends[b]
        if be.refuse_from is not None and now >= be.refuse_from:
            self.errors.append((rid, b))
            return None
        be.inflight[rid] = now + duration  # @line L4
        self.assigned[rid] = (b, now, now + duration)
        return b


def simulate(rng: random.Random, n: int = 4, horizon: int = 200, per_tick: int = 3,
             max_duration: int = 20, drain_at: int = 50, drain_backend: int = 0,
             timeout: int = 15, lag: int = 0, refuse_after: int | None = None) -> Balancer:
    lb = Balancer(n, lag)
    rid = 0
    for t in range(horizon):
        if t == drain_at:
            lb.drain(drain_backend, t, timeout, refuse_after)
        lb.tick(t)
        for _ in range(rng.randint(0, per_tick)):
            lb.arrive(rid, t, rng.randint(1, max_duration))
            rid += 1
    return lb


@dataclass
class GoawayResult:
    last_stream_id: int
    processed: list[int]
    refused: list[int]  # safe to retry on a new connection


def goaway_shutdown(send_times: list[int], delay: int, goaway_at: int, two_step: bool) -> GoawayResult:
    """A client opens stream i (ids 1, 3, 5, ...) at send_times[i], in order.
    Frames take `delay` ticks each way. The server starts a graceful shutdown
    at `goaway_at`. One step: it sends GOAWAY with the largest id it has
    received. Two steps (RFC 9113, Section 6.8): it first sends GOAWAY with
    2^31 - 1, waits one round trip, then sends GOAWAY with the largest id
    received by then. The client opens no stream after it receives the first
    GOAWAY."""
    ids = [2 * i + 1 for i in range(len(send_times))]
    seen_by_client = goaway_at + delay  # the client receives the first GOAWAY
    opened = [(i, t) for i, t in zip(ids, send_times) if t < seen_by_client]
    final_at = goaway_at + 2 * delay if two_step else goaway_at
    received = [i for i, t in opened if t + delay <= final_at]
    last = max(received, default=0)
    processed = [i for i, _ in opened if i <= last]
    refused = [i for i, _ in opened if i > last]
    return GoawayResult(last, processed, refused)
