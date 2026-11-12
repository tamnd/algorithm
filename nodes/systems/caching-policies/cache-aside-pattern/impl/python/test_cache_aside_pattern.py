# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-aside-pattern/. The authors are listed in prov/XJRN9K.jsonl.

from math import factorial

from cache_aside_pattern import (Env, all_runs, read, replay, run_alone, write,
                                 write_delete_then_update, write_update_then_set)


def maker(ops, store=None, cache=None):
    """ops: list of (operation, args). Return a make() function for the scheduler."""
    def make():
        env = Env(store or {"x": 0}, cache)
        return env, [op(env, *args) for op, args in ops]
    return make


def stale_runs(make):
    runs = list(all_runs(make))
    return len(runs), [s for s, env, _ in runs if env.stale_keys()]


def test_sequential_behavior():
    env = Env({"x": 5})
    assert run_alone(read(env, "x")) == 5 and env.store_reads == 1
    assert run_alone(read(env, "x")) == 5 and env.store_reads == 1  # hit
    run_alone(write(env, "x", 6))
    assert "x" not in env.cache and env.store["x"] == 6
    assert run_alone(read(env, "x")) == 6 and env.store_reads == 2


def test_number_of_interleavings():
    # a reader that misses has 3 steps and a writer 2: 5! / (3! 2!) = 10 interleavings
    n, _ = stale_runs(maker([(read, ("x",)), (write, ("x", 1))]))
    assert n == factorial(5) // (factorial(3) * factorial(2)) == 10


def test_two_writers_update_then_set_race():
    make = maker([(write_update_then_set, ("x", 1)), (write_update_then_set, ("x", 2))])
    n, bad = stale_runs(make)
    assert (n, sorted(bad)) == (6, [[0, 1, 1, 0], [1, 0, 0, 1]])
    env, _, _ = replay(make, [0, 1, 1, 0])  # W1 store, W2 store, W2 set, W1 set
    assert env.store["x"] == 2 and env.cache["x"] == 1


def test_two_writers_with_delete_never_stale():
    n, bad = stale_runs(maker([(write, ("x", 1)), (write, ("x", 2))]))
    assert (n, bad) == (6, [])


def test_reader_writer_race_with_delete():
    make = maker([(read, ("x",)), (write, ("x", 1))])
    n, bad = stale_runs(make)
    assert (n, bad) == (10, [[0, 0, 1, 1, 0]])
    env, results, _ = replay(make, [0, 0, 1, 1, 0])  # R get, R store read, W store, W delete, R set
    assert results[0] == 0 and env.store["x"] == 1 and env.cache["x"] == 0
    # the stale entry stays until the next write or eviction
    run_alone(write(env, "x", 2))
    assert env.stale_keys() == []


def test_stale_iff_read_window_covers_write_window():
    make = maker([(read, ("x",)), (write, ("x", 1))])
    for schedule, env, _ in all_runs(make):
        pos_r = [i for i, p in enumerate(schedule) if p == 0]  # get, store read, set
        pos_w = [i for i, p in enumerate(schedule) if p == 1]  # store write, delete
        predicted = pos_r[1] < pos_w[0] and pos_r[2] > pos_w[1]
        assert bool(env.stale_keys()) == predicted


def test_delete_first_is_worse():
    n, bad = stale_runs(maker([(read, ("x",)), (write_delete_then_update, ("x", 1))]))
    assert (n, len(bad)) == (10, 6)


def test_many_readers_one_writer_final_state():
    # two readers and one writer: stale only if some reader's read window covers the write
    make = maker([(read, ("x",)), (read, ("x",)), (write, ("x", 1))])
    runs = list(all_runs(make))
    assert all(set(env.cache.values()) <= {0, 1} for _, env, _ in runs)
    stale = [s for s, env, _ in runs if env.stale_keys()]
    for s in stale:
        w = [i for i, p in enumerate(s) if p == 2]
        assert any(
            len(r) == 3 and r[1] < w[0] and r[2] > w[1]
            for r in ([i for i, p in enumerate(s) if p == q] for q in (0, 1)))
