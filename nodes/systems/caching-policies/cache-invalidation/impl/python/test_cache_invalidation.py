# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-invalidation/. The authors are listed in prov/N20ZB0.jsonl.

from cache_invalidation import (Env, LeaseCache, PlainCache, all_runs, herd,
                                read, replay, write)


def maker(cache_cls, ops):
    def make():
        env = Env(cache_cls(), {"x": 0})
        return env, [op(env, *args) for op, args in ops]
    return make


def stale_count(make):
    runs = list(all_runs(make))
    return len(runs), [s for s, env, _ in runs if env.stale_keys()]


def test_lease_life_cycle():
    c = LeaseCache(interval=10)
    r = c.get("x", 0)
    assert r.kind == "lease" and r.token is not None
    assert c.get("x", 1).kind == "wait"  # one token per key per interval
    assert c.set("x", 7, r.token)
    assert c.get("x", 2) == ("hit", 7, None)
    assert not c.set("x", 8, r.token)  # a token is used once


def test_delete_voids_the_token():
    c = LeaseCache()
    r = c.get("x", 0)
    c.delete("x", 0)
    assert not c.set("x", 0, r.token) and "x" not in c.data


def test_plain_cache_aside_race_and_lease_fix():
    ops = [(read, ("x",)), (write, ("x", 1))]
    n, bad = stale_count(maker(PlainCache, ops))
    assert (n, bad) == (10, [[0, 0, 1, 1, 0]])
    n, bad = stale_count(maker(LeaseCache, ops))
    assert (n, bad) == (10, [])
    env, results, _ = replay(maker(LeaseCache, ops), [0, 0, 1, 1, 0])
    assert results[0] == 0 and "x" not in env.cache.data and env.cache.rejected_sets == 1


def test_two_readers_one_writer_never_stale_with_leases():
    ops = [(read, ("x",)), (read, ("x",)), (write, ("x", 1))]
    n, bad = stale_count(maker(LeaseCache, ops))
    assert n > 0 and bad == []
    n_plain, bad_plain = stale_count(maker(PlainCache, ops))
    assert n_plain > n and bad_plain  # without leases some runs are stale


def test_lost_lease_holder_is_replaced_after_interval():
    c = LeaseCache(interval=10)
    a = c.get("x", 0)  # client A gets a token and then stalls
    assert c.get("x", 5).kind == "wait"
    b = c.get("x", 10)
    assert b.kind == "lease" and b.token != a.token
    assert not c.set("x", "old", a.token)  # A's late set is rejected
    assert c.set("x", "new", b.token)


def test_stale_values_after_delete():
    c = LeaseCache(interval=10, stale_life=2)
    r = c.get("x", 0)
    c.set("x", "v1", r.token)
    c.delete("x", 20)
    r = c.get("x", 21)
    assert r.kind == "lease" and r.value == "v1"  # stale value with a token
    assert c.get("x", 21.5) == ("wait", "v1", None)
    assert c.get("x", 22.5).value is None  # the stale copy is gone after 2 units


def test_herd_one_store_read_with_leases():
    reads, finish = herd(LeaseCache(interval=10), 50, load_time=0.1, retry_delay=0.01, gap=0.001)
    assert reads == 1 and all(t is not None and t < 0.12 for t in finish)
    reads, finish = herd(PlainCache(), 50, load_time=0.1, retry_delay=0.01, gap=0.001)
    assert reads == 50
