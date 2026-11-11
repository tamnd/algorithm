# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutex/. The authors are listed in prov/CKW457.jsonl.
import pytest

from explorer import Explorer
from mutex import (MutexSpec, broken_lock, check, mutex3_lock, mutex3_trylock, mutex3_unlock, solo_calls,
                   take1_lock, take1_unlock)


def test_spec_laws():
    m = MutexSpec()
    assert m.lock(0)
    assert not m.trylock(1) and not m.lock(1)
    with pytest.raises(RuntimeError):
        m.unlock(1)
    with pytest.raises(RuntimeError):
        m.lock(0)
    m.unlock(0)
    assert m.trylock(1)
    m.unlock(1)
    assert m.owner is None


def test_mutex3_exhaustive():
    for n, rounds in ((2, -1), (3, 1)):
        res = check(mutex3_lock, mutex3_unlock, n, rounds)
        assert res["mutual_exclusion"]
        assert res["lost_wakeups"] == 0
    # A thread that returns from futex_wait can lose the race to a newcomer again and again.
    assert not check(mutex3_lock, mutex3_unlock, 2, -1)["starvation_free"]


def test_take1_is_safe():
    res = check(take1_lock, take1_unlock, 2, 1)
    assert res["mutual_exclusion"] and res["lost_wakeups"] == 0


def test_broken_variant_loses_a_wakeup():
    res = check(broken_lock, mutex3_unlock, 2, -1)
    assert res["mutual_exclusion"]
    assert res["lost_wakeups"] > 0
    assert not res["starvation_free"]


def test_lost_wakeup_schedule():
    from explorer import procs
    ex = Explorer(procs(broken_lock, mutex3_unlock, 2, 1), {"val": 0})
    # p0 takes the lock, p1 fails its cas and sleeps on value 1, p0 unlocks.
    s = ex.run([0, 0, 1, 1, 1, 0, 0])
    assert s[1][1][6] == "val" and s[1][0][2] == "F" and ex.value(s, "val") == 0


def test_uncontended_cost():
    # mutex3: one cas to lock, one atomic decrement to unlock, and no system call.
    assert solo_calls(mutex3_lock, mutex3_unlock) == {"atomic": 2, "plain": 0, "futex": 0}
    # Take 1 calls futex_wake on every unlock, even with no waiter.
    assert solo_calls(take1_lock, take1_unlock) == {"atomic": 1, "plain": 1, "futex": 1}


def test_trylock():
    g = mutex3_trylock(0)
    assert next(g) == ("cas", "val", 0, 1)
    with pytest.raises(StopIteration) as stop:
        g.send(1)
    assert stop.value.value is False
