# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-commit/. The authors are listed in prov/D9GM98.jsonl.

import random

from group_commit import acked_before_durable, simulate


def random_arrivals(rng: random.Random, n: int, gap: int) -> list[int]:
    t, out = 0, []
    for _ in range(n):
        t += rng.randrange(0, 2 * gap + 1)
        out.append(t)
    return out


def test_no_ack_before_durable() -> None:
    rng = random.Random(1)
    for _ in range(300):
        arr = random_arrivals(rng, rng.randrange(1, 60), rng.randrange(0, 12))
        d, k, tau = rng.randrange(1, 15), rng.randrange(1, 6), rng.randrange(0, 20)
        for group in (True, False):
            run = simulate(arr, d, k, tau, group)
            assert not acked_before_durable(run)
            assert all(c.acked >= 0 for c in run.commits)
            # a crash at any time t loses no acknowledged commit
            for t in range(0, max(c.acked for c in run.commits) + 1, 3):
                acked = {c.txn for c in run.commits if 0 <= c.acked <= t}
                durable = {c.txn for c in run.commits if 0 <= c.durable <= t}
                assert acked <= durable
            # one write at a time, and records are written in LSN order
            for (s1, e1, _), (s2, _, _) in zip(run.writes, run.writes[1:]):
                assert e1 <= s2
            assert sorted(run.commits, key=lambda c: c.durable) == sorted(run.commits, key=lambda c: c.lsn)


def test_early_ack_is_caught() -> None:
    run = simulate([0, 1, 2], d=10, early_ack=True)
    assert acked_before_durable(run) == [1, 2, 3]


def test_hand_example() -> None:
    arr = [0, 1, 2, 3, 12]
    g = simulate(arr, d=10)
    assert g.writes == [(0, 10, 1), (10, 20, 3), (20, 30, 1)]
    assert g.latencies() == [10, 19, 18, 17, 18]
    s = simulate(arr, d=10, group=False)
    assert len(s.writes) == 5
    assert s.latencies() == [10, 19, 28, 37, 38]


def test_latency_at_most_two_writes_when_idle_policy() -> None:
    rng = random.Random(2)
    for _ in range(200):
        d = rng.randrange(1, 20)
        arr = random_arrivals(rng, 80, rng.randrange(0, 2 * d))
        run = simulate(arr, d)
        assert max(run.latencies()) <= 2 * d


def test_throughput_under_load() -> None:
    # 1000 commits, one every 2 units; one write takes 10 units.
    arr = list(range(0, 2000, 2))
    g = simulate(arr, d=10)
    s = simulate(arr, d=10, group=False)
    assert len(s.writes) == 1000 and len(g.writes) <= 2000 // 10 + 2
    assert max(g.latencies()) <= 20
    assert max(s.latencies()) > 7000  # the queue grows without bound
    assert sum(n for _, _, n in g.writes) == 1000


def test_batch_size_and_timeout() -> None:
    # k = 3: the writer waits for 3 records or for the timeout.
    run = simulate([0, 1, 30], d=5, k=3, tau=8)
    assert run.writes == [(8, 13, 2), (38, 43, 1)]
    run = simulate([0, 1, 2], d=5, k=3, tau=8)
    assert run.writes == [(2, 7, 3)]
