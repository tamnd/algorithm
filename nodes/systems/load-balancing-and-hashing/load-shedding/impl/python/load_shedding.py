# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/load-shedding/. The authors are listed in prov/Q0Y7AN.jsonl.

"""Load shedding at one overloaded server.

Model: an integer clock and one server that serves one request at a time.
Every request needs `service` ticks. A request that arrives at time a has the
client deadline a + timeout: a response that completes later is useless, so
it counts as work but not as goodput. Rejecting or dropping a request costs
no server time. In one tick the server first completes the request that ends
then, then takes the arrivals of the tick (admission and eviction), then, if
it is idle, takes requests from the queue: it drops each one whose wait is
above the current queue timeout, and starts the first one that passes.

Policies (combine as needed):
  max_wait       drop at dequeue a request that waited more than this (None = never)
  codel          (m, n): Maurer's controlled delay; the queue timeout is m when
                 the queue has not been empty in the last n ticks, else n
  lifo           serve the newest request first (False = FIFO)
  adaptive_lifo  FIFO while the queue was empty in the last n ticks, LIFO otherwise
  capacity       at most this many requests wait; on overflow drop the lowest
                 priority request (the newest among those) or the arrival itself
  limit          reject at arrival when this many requests are outstanding
                 (waiting plus in service)
  gradient       adapt `limit` with the gradient rule of the Envoy filter
"""

import math
from dataclasses import dataclass, field


@dataclass
class Request:
    rid: int
    arrival: int
    priority: int = 0  # larger means more important


@dataclass
class Result:
    completed: list[tuple[int, int, int]] = field(default_factory=list)  # (rid, arrival, end)
    rejected: list[int] = field(default_factory=list)  # refused at arrival
    dropped: list[int] = field(default_factory=list)  # removed from the queue
    busy_ticks: int = 0
    limits: list[float] = field(default_factory=list)
    evictions: list[tuple[int, int]] = field(default_factory=list)  # (class shed, lowest class kept)

    def goodput(self, timeout: int) -> int:
        return sum(1 for _, a, e in self.completed if e - a <= timeout)

    def late(self, timeout: int) -> int:
        return len(self.completed) - self.goodput(timeout)


@dataclass
class Policy:
    max_wait: int | None = None
    codel: tuple[int, int] | None = None
    lifo: bool = False
    adaptive_lifo: int | None = None
    capacity: int | None = None
    limit: float | None = None
    gradient: tuple[int, float] | None = None  # (window of completions, buffer fraction)
    min_limit: float = 1.0
    max_limit: float = 1000.0


def gradient_update(limit: float, min_rtt: float, sample_rtt: float, buffer: float,
                    lo: float, hi: float) -> float:
    """The gradient controller of the Envoy adaptive concurrency filter:
    gradient = (minRTT + B) / sampleRTT with B = buffer * minRTT, and
    new limit = gradient * limit + sqrt(limit), clamped to [lo, hi]."""
    g = (min_rtt * (1.0 + buffer)) / sample_rtt
    return max(lo, min(hi, g * limit + math.sqrt(limit)))


def simulate(requests: list[Request], service: int, policy: Policy, horizon: int) -> Result:
    """Run the server from time 0 to `horizon` inclusive. `requests` is sorted
    by arrival. Requests still waiting at the end are neither completed nor
    shed."""
    res = Result()
    queue: list[Request] = []  # in arrival order
    current: tuple[Request, int] | None = None  # (request, end time)
    last_empty = 0  # the last tick at which the queue was empty
    limit = policy.limit
    samples: list[int] = []
    min_rtt = math.inf
    i = 0
    for t in range(horizon + 1):
        # 1. completion
        if current is not None and current[1] == t:
            r, end = current
            res.completed.append((r.rid, r.arrival, end))
            current = None
            if policy.gradient is not None:
                rtt = end - r.arrival
                min_rtt = min(min_rtt, rtt)
                samples.append(rtt)
                if len(samples) == policy.gradient[0]:
                    limit = gradient_update(limit, min_rtt, sum(samples) / len(samples),
                                            policy.gradient[1], policy.min_limit, policy.max_limit)
                    samples.clear()
        # 2. arrivals
        while i < len(requests) and requests[i].arrival == t:
            r = requests[i]
            i += 1
            outstanding = len(queue) + (current is not None)
            if limit is not None and outstanding >= math.floor(limit):  # @line L1
                res.rejected.append(r.rid)
                continue
            queue.append(r)  # @line L2
            if policy.capacity is not None and len(queue) > policy.capacity:  # @line L3
                # Evict the lowest priority; among equals, the newest.
                victim = min(range(len(queue)), key=lambda j: (queue[j].priority, -j))  # @line L4
                v = queue.pop(victim)  # @line L5
                (res.rejected if v.rid == r.rid else res.dropped).append(v.rid)
                res.evictions.append((v.priority, min(q.priority for q in queue)))
        res.limits.append(limit if limit is not None else math.inf)
        # 3. start the next request
        if current is None:
            empty_recently = t - last_empty <= (policy.codel[1] if policy.codel else 0)
            while queue:  # @line L6
                newest = policy.lifo or (policy.adaptive_lifo is not None
                                         and t - last_empty > policy.adaptive_lifo)  # @line L7
                r = queue.pop() if newest else queue.pop(0)  # @line L8
                wait = t - r.arrival
                timeout = policy.max_wait
                if policy.codel is not None:
                    m, n = policy.codel
                    timeout = n if empty_recently else m
                if timeout is not None and wait > timeout:  # @line L9
                    res.dropped.append(r.rid)
                    continue
                current = (r, t + service)  # @line L10
                break
        if not queue:
            last_empty = t
        if current is not None:
            res.busy_ticks += 1
    return res


def periodic(period: int, horizon: int, priorities: list[int] | None = None) -> list[Request]:
    """One request every `period` ticks from time 0 up to `horizon`."""
    out = []
    for k, a in enumerate(range(0, horizon + 1, period)):
        p = priorities[k % len(priorities)] if priorities else 0
        out.append(Request(k, a, p))
    return out


def no_shed_useful(service: int, period: int, timeout: int) -> int:
    """Theorem 1: with FIFO, no shedding, one arrival every `period` < `service`
    ticks, the number of responses that ever meet the deadline."""
    if timeout < service:
        return 0
    return (timeout - service) // (service - period) + 1
