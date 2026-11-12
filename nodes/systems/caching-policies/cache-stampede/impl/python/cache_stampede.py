# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-stampede/. The authors are listed in prov/WMTKQ5.jsonl.

"""Cache stampede on one hot key, and two fixes: single flight and XFetch.

The key holds a value that takes delta time units to recompute. A recompute
that starts at time s writes the new value at s + delta with expiry
s + delta + ttl. Requests come at given times on a simulated clock.

Policies:
  "plain"          a request that finds the key expired starts a recompute.
  "single_flight"  as plain, but only if no recompute is already running;
                   other requests wait for it.
  "xfetch"         probabilistic early expiration (Vattani, Chierichetti and
                   Lowenstein, PVLDB 8(8), 2015): a request at time t also
                   recomputes when t - delta * beta * ln(u) >= expiry, with u
                   uniform on (0, 1].

The stampede size is the number of recomputes that start before the first one
finishes, since every one of them hits the store with the same work.
"""

import math


def xfetch_should_recompute(now, delta, beta, expiry, rng):
    """The XFetch test. u = 1 - rng.random() lies in (0, 1], so ln(u) <= 0."""
    u = 1.0 - rng.random()
    return now - delta * beta * math.log(u) >= expiry


class Clock:
    """A simulated clock. A recompute function advances it by its own cost."""

    def __init__(self, now=0.0):
        self.now = now


class TTLStore:
    """A cache of key -> (value, delta, expiry); an expired item reads as missing."""

    def __init__(self, clock):
        self.clock = clock
        self.items = {}

    def read(self, key):
        item = self.items.get(key)
        if item is None or self.clock.now >= item[2]:
            return None, None, None
        return item

    def write(self, key, value, delta, ttl):
        self.items[key] = (value, delta, self.clock.now + ttl)


def xfetch(cache, key, ttl, recompute, rng, beta=1.0):
    """XFetch: read the key, and recompute it early with a probability that
    grows as the expiry comes near. Figure 3 of Vattani et al."""
    clock = cache.clock
    value, delta, expiry = cache.read(key)  # @line L1
    if value is None or xfetch_should_recompute(clock.now, delta, beta, expiry, rng):  # @line L2
        start = clock.now  # @line L3
        value = recompute(key)  # @line L4
        delta = clock.now - start  # @line L5
        cache.write(key, value, delta, ttl)  # @line L6
    return value  # @line L7


def simulate(times, policy, expiry, delta, ttl, beta=1.0, rng=None):
    """Run the requests at the sorted `times`. The cache starts with a value
    that expires at `expiry` and was computed in `delta` time units.

    Return (starts, first_done): the start times of all recomputes, and the
    time when the first recompute finishes (None if no recompute started)."""
    entry_expiry, entry_delta = expiry, delta
    running = []  # finish times of recomputes in progress
    starts = []
    first_done = None
    for t in times:
        running.sort()
        while running and running[0] <= t:
            done = running.pop(0)
            entry_expiry, entry_delta = done + ttl, delta
        live = t < entry_expiry
        if policy == "plain":
            go = not live
        elif policy == "single_flight":
            go = not live and not running
        elif policy == "xfetch":
            go = not live or xfetch_should_recompute(t, entry_delta, beta, entry_expiry, rng)
        else:
            raise ValueError(policy)
        if go:
            starts.append(t)
            running.append(t + delta)
            if first_done is None:
                first_done = t + delta
    return starts, first_done


def stampede_size(starts, first_done):
    """Recomputes that start before the first one finishes."""
    if first_done is None:
        return 0
    return sum(1 for s in starts if s < first_done)


def trigger_probability(t, expiry, delta, beta):
    """P(a request at time t triggers XFetch) for an entry with this expiry."""
    if t >= expiry:
        return 1.0
    if beta == 0:
        return 0.0
    return math.exp(-(expiry - t) / (delta * beta))


def expected_stampede(times, expiry, delta, beta):
    """Exact expected stampede size of XFetch for the sorted request `times`.

    Request i starts the first recompute with probability
    p_i * prod_{j < i} (1 - p_j). Then every request j > i with
    t_j < t_i + delta decides on its own with probability p_j, because the
    cache still holds the old entry. So
    E[S] = sum_i p_i prod_{j<i} (1 - p_j) (1 + sum_{j>i, t_j < t_i + delta} p_j)."""
    p = [trigger_probability(t, expiry, delta, beta) for t in times]
    total, none_yet = 0.0, 1.0
    for i, ti in enumerate(times):
        first = none_yet * p[i]
        extra = sum(p[j] for j in range(i + 1, len(times)) if times[j] < ti + delta)
        total += first * (1.0 + extra)
        none_yet *= 1.0 - p[i]
    return total


def early_probability(times, expiry, delta, beta):
    """P(XFetch starts a recompute before the expiry time)."""
    q = 1.0
    for t in times:
        if t < expiry:
            q *= 1.0 - trigger_probability(t, expiry, delta, beta)
    return 1.0 - q
