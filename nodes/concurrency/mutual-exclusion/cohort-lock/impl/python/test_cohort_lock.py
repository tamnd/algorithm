# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cohort-lock/. The authors are listed in prov/KR24FX.jsonl.

from cohort_lock import client, init
from interleave import explore, no_progress, run, starvation


def test_mutual_exclusion_two_in_one_cluster_two_rounds() -> None:
    cl = [0, 0]
    g = explore([client(cl, 1, rounds=2)] * 2, init(cl))
    assert g.violation is None and not g.stuck


def test_mutual_exclusion_three_processes_two_clusters() -> None:
    for bound in (0, 1):
        cl = [0, 0, 1]
        g = explore([client(cl, bound, rounds=1)] * 3, init(cl))
        assert g.violation is None and not g.stuck


def test_deadlock_free_but_not_starvation_free() -> None:
    # with one process in each cluster all handovers go through the global lock
    cl = [0, 1]
    g = explore([client(cl, 2, rounds=None)] * 2, init(cl))
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) != []


def test_cohort_is_starvation_free_inside_a_cluster() -> None:
    cl = [0, 0]
    g = explore([client(cl, 1, rounds=None)] * 2, init(cl))
    assert g.violation is None and no_progress(g) == []
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def batches(m):
    """The numbers of critical sections between two takes of the global lock."""
    out = []
    for entry in m.log:
        if entry[1] == "global":
            out.append(0)
        elif entry[1] == "cs":
            out[-1] += 1
    return out


def test_may_pass_local_bound() -> None:
    cl = [0, 0, 0, 1, 1, 1]
    for bound in range(0, 5):
        seen_full = False
        for seed in range(30):
            m = run([client(cl, bound, rounds=4, max_delay=3)] * 6, init(cl), seed=seed)
            assert m.violations == [] and len(m.entries) == 24
            b = batches(m)
            assert sum(b) == 24 and max(b) <= bound + 1
            seen_full |= max(b) == bound + 1
        assert seen_full
