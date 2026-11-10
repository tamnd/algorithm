# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-virtual-time/. The authors are listed in prov/9E7NPE.jsonl.

from global_virtual_time import INF, System


def test_estimate_never_exceeds_true_gvt() -> None:
    # run() asserts after every event that no unprocessed or in-transit
    # timestamp is below the best estimate so far.
    rounds_done = 0
    for seed in range(40):
        sysm = System(n=2 + seed % 5, seed=seed, end=150)
        est = sysm.run(rounds=12)
        rounds_done += len(est)
        finite = [e for _, e in est if e != INF]
        assert finite and max(finite) > 0  # the estimate moves forward
    assert rounds_done > 300


def test_estimate_is_at_least_gvt_at_round_start() -> None:
    for seed in range(40):
        sysm = System(n=2 + seed % 5, seed=seed, end=150)
        est = sysm.run(rounds=12)
        for (_, e), g0 in zip(est, sysm.start_gvt):
            assert g0 <= e
