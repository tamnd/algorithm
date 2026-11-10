# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrier-synchronization/. The authors are listed in prov/1ACZ46.jsonl.

import random

from barrier_synchronization import (barrier_property_holds, ceil_log, ceil_log2, dissemination,
                                     dissemination_exit_times, naive_barrier, run_interleaved,
                                     sense_barrier, tree_barrier)


def test_dissemination_rounds_and_knowledge():
    for p in range(1, 70):
        rounds, know, messages = dissemination(p)
        assert rounds == ceil_log2(p)
        assert all(k == set(range(p)) for k in know)
        assert messages == p * ceil_log2(p)


def test_dissemination_knowledge_doubles():
    # After rounds 0..r processor i knows exactly i, i-1, ..., i-(2^(r+1)-1) (mod p).
    p = 13
    for r_end in range(ceil_log2(p)):
        know = [{i} for i in range(p)]
        for r in range(r_end + 1):
            old = [set(k) for k in know]
            for i in range(p):
                know[(i + (1 << r)) % p] |= old[i]
        for i in range(p):
            assert know[i] == {(i - j) % p for j in range(min(p, 1 << (r_end + 1)))}


def test_dissemination_exit_times():
    rng = random.Random(7)
    for p in [1, 2, 3, 5, 8, 13, 32]:
        for _ in range(30):
            arrive = [rng.randint(0, 20) for _ in range(p)]
            out = dissemination_exit_times(arrive)
            k = ceil_log2(p)
            # No processor leaves before the last arrival, and all leave by k units after it.
            assert all(max(arrive) <= t <= max(arrive) + k for t in out)
            if p > 1:
                assert min(out) >= max(arrive) + 1


def test_tree_barrier():
    for p in range(1, 60):
        for k in (2, 3, 4, 8):
            up, down, fan, root = tree_barrier(p, k)
            assert up == down == ceil_log(p, k)
            assert root == set(range(p))
            assert fan <= k - 1


def test_sense_reversing_barrier_is_safe_and_live():
    for seed in range(150):
        rng = random.Random(seed)
        p = rng.randint(2, 5)
        status, log = run_interleaved(sense_barrier, p, 4, rng)
        assert status == "ok"
        assert barrier_property_holds(log, p)


def test_naive_barrier_works_once_but_can_deadlock_on_reuse():
    for seed in range(100):
        rng = random.Random(seed)
        status, log = run_interleaved(naive_barrier, 3, 1, rng)
        assert status == "ok" and barrier_property_holds(log, 3)
    stuck = 0
    for seed in range(100):
        status, _ = run_interleaved(naive_barrier, 3, 3, random.Random(seed))
        stuck += status == "deadlock"
    assert stuck > 0
