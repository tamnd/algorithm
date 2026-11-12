# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/on-the-fly-garbage-collection/. The authors are listed in prov/R73E8Z.jsonl.

import random

import pytest

from on_the_fly_garbage_collection import ASYNC, SYNC1, SYNC2, System, all_runs, random_run

DLG = (SYNC1, SYNC2, ASYNC)


def two_threads(handshakes=DLG, barrier=True, long=False) -> System:
    """G is shared (register 0 of both threads), G.f0 = B and B.f0 = Z.
    Thread 0 reads Z through B; thread 1 cuts B.f0."""
    s = System(4, threads=2, registers=3, handshakes=handshakes, barrier=barrier)
    g, b, z = s.allocate(0), s.allocate(0), s.allocate(0)
    s.fields[g][0], s.fields[b][0] = b, z
    for t in s.threads:
        t.regs[0] = g
    p0 = [("load", 1, 0, 0), ("load", 2, 1, 0)]
    if long:  # then put Z into G and drop the registers
        p0 += [("store", 0, 1, 2), ("clear", 2), ("clear", 1)]
    s.threads[0].program = p0
    s.threads[1].program = [("load", 1, 0, 0), ("store", 1, 0, None), ("clear", 1)]
    return s


@pytest.mark.parametrize("handshakes,runs,lost", [
    (DLG, 8881776, 0),
    ((SYNC1, ASYNC), 2208774, 0),
    ((ASYNC,), 474461, 50),
])
def test_every_schedule_of_the_short_program(handshakes, runs, lost) -> None:
    assert all_runs(two_threads(handshakes)) == (runs, lost)


def test_every_schedule_without_the_barrier() -> None:
    assert all_runs(two_threads(barrier=False)) == (8431446, 112656)


def test_every_schedule_of_the_long_program() -> None:
    assert all_runs(two_threads(long=True)) == (7901664022, 0)
    assert all_runs(two_threads((ASYNC,), long=True)) == (211684994, 28308)


def run_schedule(s: System, schedule: list[tuple[str, int]]) -> None:
    for ch in schedule:
        assert ch in s.choices(), ch
        s.do(ch)


def test_one_handshake_loses_z() -> None:
    s = two_threads((ASYNC,))
    run_schedule(s, [("m", 1), ("m", 1),  # thread 1 holds B and reads the flag: off
                     ("c", 0),  # the collector posts async
                     ("a", 0),  # thread 0 shades its roots: G
                     ("m", 0), ("m", 0),  # thread 0 loads B, then Z
                     ("m", 1),  # thread 1 stores nil into B.f0 with no shade
                     ("a", 1)])  # thread 1 shades G and B
    while s.phase != "idle":
        s.do(("c", 0))
    z = 2
    assert s.threads[0].regs[2] == z and s.is_free[z]


def test_the_sync_handshake_saves_z() -> None:
    s = two_threads(DLG)
    run_schedule(s, [("m", 1), ("m", 1), ("c", 0),  # the collector posts sync1
                     ("m", 1),  # the store ends: the flag it read was off
                     ("a", 0), ("a", 1), ("c", 0),  # sync2
                     ("a", 0), ("a", 1), ("c", 0),  # async
                     ("a", 0)])
    assert s.threads[1].regs[1] == 1 and s.fields[1][0] is None
    # Thread 0 can no longer reach Z: B.f0 was cut before it answered async.
    run_schedule(s, [("m", 0), ("m", 0)])
    assert s.threads[0].regs[2] is None


@pytest.mark.parametrize("seed", range(6))
def test_random_threads_never_lose_a_cell(seed: int) -> None:
    s = System(36, threads=3, registers=3, trigger=12)
    g = s.allocate(0)
    for t in s.threads:
        t.regs[0] = g
    assert random_run(s, 12, 4000, random.Random(seed)) == -1
    assert s.cycles >= 8
