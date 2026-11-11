# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/livelock/. The authors are listed in prov/92X6MQ.jsonl.

from interleave import explore, lockstep, no_progress, run
from livelock import INIT, client, collisions_before_first_entry


def test_polite_protocol_is_safe_but_can_livelock() -> None:
    g = explore([client(False)] * 2, INIT)
    assert g.violation is None and not g.stuck
    # a fair cycle with both processes moving and nobody entering
    cycles = no_progress(g)
    assert cycles
    assert any({e[0] for _, e in inner} == {0, 1} for _, inner in cycles)


def test_lock_step_run_never_enters() -> None:
    m = run([client(False)] * 2, INIT, policy=lockstep(2), max_steps=3000)
    assert m.entries == []
    # one attempt is four steps (raise, look, lower, retreat), so each process retreats about 3000 / 8 times
    assert sum(1 for e in m.log if e[1] == "retreat") == 748


def test_randomized_fix_enters_and_stays_safe() -> None:
    g = explore([client(True)] * 2, INIT)
    assert g.violation is None and not g.stuck
    for seed in range(200):
        m = run([client(True)] * 2, INIT, policy=lockstep(2), seed=seed)
        assert sorted(m.entries) == [0, 1] and m.violations == []


def test_expected_collisions_is_two() -> None:
    # the number of collisions is geometric with success probability 1/2
    counts = []
    for seed in range(4000):
        m = run([client(True)] * 2, INIT, policy=lockstep(2), seed=seed)
        counts.append(collisions_before_first_entry(m.log))
    assert min(counts) == 1
    mean = sum(counts) / len(counts)
    assert 1.9 < mean < 2.1
    for k in (1, 2, 3, 4):
        tail = sum(c > k for c in counts) / len(counts)
        assert abs(tail - 2.0 ** -k) < 0.03
