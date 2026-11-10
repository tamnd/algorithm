# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fault-tolerance-by-recomputation/. The authors are listed in prov/M9PXF3.jsonl.

import random
from collections import Counter

from fault_tolerance_by_recomputation import run_job

WORDS = "a b c d e f g h".split()


def make_splits(rng, M):
    return [" ".join(rng.choice(WORDS) for _ in range(rng.randint(0, 8))) for _ in range(M)]


def test_no_failures():
    rng = random.Random(0)
    splits = make_splits(rng, 6)
    out, st = run_job(splits, 3, 4, {}, rng)
    assert out == dict(Counter(" ".join(splits).split()))
    assert st["map_runs"] == 6 and st["reduce_runs"] == 3
    assert st["lost_map_outputs"] == st["killed_running"] == 0


def test_seeded_failures_give_the_same_output():
    lost_any = killed_any = 0
    for seed in range(200):
        rng = random.Random(seed)
        M, R, W = rng.randint(1, 10), rng.randint(1, 5), rng.randint(2, 6)
        splits = make_splits(rng, M)
        fail_at = {}
        for w in rng.sample(range(W), rng.randint(0, W - 1)):  # at least one worker survives
            fail_at.setdefault(rng.randint(1, 12), []).append(w)
        out, st = run_job(splits, R, W, fail_at, rng)
        assert out == dict(Counter(" ".join(splits).split()))
        # A lost map output costs one more map run. Completed reduce tasks never run again.
        assert st["map_runs"] == M + st["lost_map_outputs"] - st["maps_not_done_at_end"]
        assert st["reduce_runs"] == R
        lost_any += st["lost_map_outputs"] > 0
        killed_any += st["killed_running"] > 0
    assert lost_any > 0 and killed_any > 0
