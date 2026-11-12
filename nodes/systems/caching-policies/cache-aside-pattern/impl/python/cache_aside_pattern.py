# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-aside-pattern/. The authors are listed in prov/XJRN9K.jsonl.

"""The cache-aside pattern, with a deterministic scheduler for its races.

The application talks to two services, a cache and a store. Each operation is
a generator: it yields before each access to a service, and the access runs
when the scheduler resumes it. So one call to next() runs one atomic access,
and a schedule (a list of process numbers) fixes one interleaving. No threads
are used.
"""


class Env:
    """The shared state: a cache (dict) and a store (dict), with access counts."""

    def __init__(self, store=None, cache=None):
        self.store = dict(store or {})
        self.cache = dict(cache or {})
        self.store_reads = 0
        self.store_writes = 0

    def stale_keys(self):
        """Keys whose cached value differs from the store value."""
        return sorted(k for k, v in self.cache.items() if self.store.get(k) != v)


# ---------------------------------------------------------------- the pattern

def read(env, key):
    """Cache-aside read: try the cache; on a miss read the store and fill the cache."""
    yield
    hit = key in env.cache  # @line L1
    if hit:  # @line L2
        return env.cache[key]
    yield
    env.store_reads += 1
    value = env.store.get(key)  # @line L3
    yield
    env.cache[key] = value  # @line L4
    return value  # @line L5


def write(env, key, value):
    """Cache-aside write: update the store, then delete the cache key."""
    yield
    env.store_writes += 1
    env.store[key] = value  # @line L6
    yield
    env.cache.pop(key, None)  # @line L7


# ---------------------------------------------------------------- variants that the page warns against

def write_update_then_set(env, key, value):
    """Update the store, then set the cache to the new value (has a race between writers)."""
    yield
    env.store_writes += 1
    env.store[key] = value
    yield
    env.cache[key] = value


def write_delete_then_update(env, key, value):
    """Delete the cache key first, then update the store (has a race with a reader)."""
    yield
    env.cache.pop(key, None)
    yield
    env.store_writes += 1
    env.store[key] = value


# ---------------------------------------------------------------- the scheduler

def run_alone(gen):
    """Run one operation with no other process. Return its result."""
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


def replay(make, schedule):
    """make() returns (env, [generators]). Run the schedule of process numbers.

    Return (env, results, alive): results[i] is the return value of process i
    if it finished, and alive[i] tells whether it still has steps."""
    env, procs = make()
    for g in procs:
        next(g)  # run to the first yield; no access happens before it
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
    """Every complete interleaving, by depth-first search with replay.

    Yield (schedule, env, results) for each one."""
    stack = [[]]
    while stack:
        prefix = stack.pop()
        env, results, alive = replay(make, prefix)
        live = [i for i, a in enumerate(alive) if a]
        if not live:
            yield prefix, env, results
        for i in reversed(live):
            stack.append(prefix + [i])
