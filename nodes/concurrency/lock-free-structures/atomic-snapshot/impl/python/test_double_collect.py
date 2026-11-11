# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/atomic-snapshot/. The authors are listed in prov/J3M2WS.jsonl.

import pytest

from double_collect import Snapshot, double_collect_scan, setup_for, single_collect_scan, starve_scanner
from explorer import explore, final_histories
from lincheck import is_linearizable

WORKLOADS = {
    "update and scan": [[("update", 1)], [("scan", None)]],
    "two updates and scan": [[("update", 1), ("update", 2)], [("scan", None)]],
    "update then scan, twice": [[("update", 1), ("scan", None)], [("update", 2), ("scan", None)]],
    "two updaters and scan": [[("update", 1)], [("update", 1)], [("scan", None)]],
}


def histories(progs, scan):
    return final_histories(setup_for(progs, scan), max_depth=200)


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_double_collect_is_linearizable(name) -> None:
    progs = WORKLOADS[name]
    hs = histories(progs, double_collect_scan)
    assert hs
    for h in hs:
        assert is_linearizable(list(h), Snapshot(len(progs))), h


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_double_collect_every_run_of_a_finite_workload_ends(name) -> None:
    explore(setup_for(WORKLOADS[name], double_collect_scan), max_depth=200)


def test_single_collect_is_not_linearizable() -> None:
    # The scanner reads R[0] = 0; then process 0 writes 1 and returns; then
    # process 1 writes 1; the scanner reads R[1] = 1 and returns (0, 1, 0).
    # In every order that respects real time, R[0] = 1 before R[1] = 1.
    progs = WORKLOADS["two updaters and scan"]
    bad = [h for h in histories(progs, single_collect_scan) if not is_linearizable(list(h), Snapshot(3))]
    assert bad
    assert any(e[0] == "res" and e[2] == (0, 1, 0) for e in bad[0])


@pytest.mark.parametrize("n", [2, 3, 4])
def test_double_collect_can_run_for_ever(n) -> None:
    done, reads, writes = starve_scanner(n, rounds=10_000)
    assert not done
    assert reads == 10_000
    assert writes == 10_000 // n
