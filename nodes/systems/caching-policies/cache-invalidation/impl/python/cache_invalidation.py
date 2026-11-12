# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-invalidation/. The authors are listed in prov/N20ZB0.jsonl.

"""Invalidation with leases, as in memcache at Facebook (Nishtala et al., NSDI 2013).

On a miss the cache gives the client a lease token bound to the key. The client
reads the store and presents the token with its set. A delete of the key voids
the token, so a set that carries a value read before the delete is rejected.
The cache issues at most one token per key per `interval` time units; other
clients that miss in that time get a "wait" reply and retry later. A deleted
value can be kept for `stale_life` time units and returned, marked as stale,
to clients that can use stale data.

The clock is a number passed in by the caller. Tokens come from a counter, so
runs are deterministic. The second part is a small scheduler that runs
operations written as generators in any interleaving, without threads.
"""

from collections import namedtuple

# kind is "hit", "lease" or "wait". value is the cached value on a hit, and
# otherwise a stale value or None. token is set only when kind is "lease".
Reply = namedtuple("Reply", "kind value token")


class LeaseCache:
    def __init__(self, interval=10.0, stale_life=0.0):
        self.interval = interval
        self.stale_life = stale_life
        self.data = {}
        self.lease = {}  # key -> current valid token
        self.issued_at = {}  # key -> time of the last token issued for the key
        self.stale = {}  # key -> (value, time of delete)
        self.counter = 0
        self.rejected_sets = 0

    def _stale_value(self, key, now):
        item = self.stale.get(key)
        if item is not None and now - item[1] < self.stale_life:
            return item[0]
        return None

    def get(self, key, now):
        if key in self.data:
            return Reply("hit", self.data[key], None)
        stale = self._stale_value(key, now)
        last = self.issued_at.get(key)
        if last is not None and now - last < self.interval:
            return Reply("wait", stale, None)
        self.counter += 1
        token = self.counter
        self.lease[key] = token  # a new token replaces (and so voids) any older one
        self.issued_at[key] = now
        return Reply("lease", stale, token)

    def set(self, key, value, token):
        """Store the value only if token is the current lease for the key."""
        if token is None or self.lease.get(key) != token:
            self.rejected_sets += 1
            return False
        del self.lease[key]
        self.data[key] = value
        self.stale.pop(key, None)
        return True

    def delete(self, key, now):
        """Invalidate: remove the value and void any lease token for the key."""
        self.lease.pop(key, None)
        if key in self.data:
            value = self.data.pop(key)
            if self.stale_life > 0:
                self.stale[key] = (value, now)

    def evict(self, key):
        """Drop the value for lack of space. Leases are not affected."""
        self.data.pop(key, None)


class PlainCache:
    """A cache without leases, for comparison: get, set and delete only."""

    def __init__(self):
        self.data = {}

    def get(self, key, now):
        if key in self.data:
            return Reply("hit", self.data[key], None)
        return Reply("lease", None, None)

    def set(self, key, value, token):
        self.data[key] = value
        return True

    def delete(self, key, now):
        self.data.pop(key, None)


class Env:
    def __init__(self, cache, store):
        self.cache = cache
        self.store = dict(store)
        self.store_reads = 0

    def stale_keys(self):
        return sorted(k for k, v in self.cache.data.items() if self.store.get(k) != v)


# ---------------------------------------------------------------- operations as generators

def read(env, key, now=0.0):
    """Cache-aside read with a lease. Return the value, or the Reply if told to wait."""
    yield
    reply = env.cache.get(key, now)
    if reply.kind == "hit":
        return reply.value
    if reply.kind == "wait":
        return reply
    yield
    env.store_reads += 1
    value = env.store.get(key)
    yield
    env.cache.set(key, value, reply.token)
    return value


def write(env, key, value, now=0.0):
    """Update the store, then delete the key in the cache."""
    yield
    env.store[key] = value
    yield
    env.cache.delete(key, now)


def replay(make, schedule):
    env, procs = make()
    for g in procs:
        next(g)
    alive = [True] * len(procs)
    results = [None] * len(procs)
    for i in schedule:
        if not alive[i]:
            raise ValueError("process %d has already finished" % i)
        try:
            next(procs[i])
        except StopIteration as stop:
            alive[i] = False
            results[i] = stop.value
    return env, results, alive


def all_runs(make):
    """Yield (schedule, env, results) for every complete interleaving."""
    stack = [[]]
    while stack:
        prefix = stack.pop()
        env, results, alive = replay(make, prefix)
        live = [i for i, a in enumerate(alive) if a]
        if not live:
            yield prefix, env, results
        for i in reversed(live):
            stack.append(prefix + [i])


# ---------------------------------------------------------------- a herd of readers on a simulated clock

def herd(cache, n_clients, load_time, retry_delay, store_value=1, gap=0.0):
    """n_clients miss on one key, client i at time i * gap. A client that gets a
    lease reads the store for load_time and sets the value; a client told to
    wait retries after retry_delay. Return (store reads, finish times)."""
    events = [(i * gap, i, "get", None) for i in range(n_clients)]
    finish = [None] * n_clients
    reads = 0
    while events:
        events.sort()
        now, i, what, token = events.pop(0)
        if what == "get":
            reply = cache.get("k", now)
            if reply.kind == "hit":
                finish[i] = now
            elif reply.kind == "wait":
                events.append((now + retry_delay, i, "get", None))
            else:
                reads += 1
                events.append((now + load_time, i, "set", reply.token))
        else:
            cache.set("k", store_value, token)
            finish[i] = now
    return reads, finish
