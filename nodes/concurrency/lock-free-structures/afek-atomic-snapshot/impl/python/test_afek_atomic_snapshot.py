# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/afek-atomic-snapshot/. The authors are listed in prov/KGSNTB.jsonl.

import pytest

from afek_atomic_snapshot import Snapshot, adversary, setup_for
from explorer import World, explore, final_histories
from lincheck import is_linearizable

WORKLOADS = {
    "update and scan": [[("update", 1)], [("scan", None)]],
    "two updates and scan": [[("update", 1), ("update", 2)], [("scan", None)]],
    "update then scan, twice": [[("update", 1), ("scan", None)], [("update", 2), ("scan", None)]],
    "two updaters and scan": [[("update", 1)], [("update", 2)], [("scan", None)]],
}


@pytest.mark.parametrize("afek", [True, False], ids=["afek", "double-collect"])
@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_every_history_is_linearizable(name, afek) -> None:
    progs = WORKLOADS[name]
    hs = final_histories(setup_for(progs, afek), max_depth=500)
    assert hs
    for h in hs:
        assert is_linearizable(list(h), Snapshot(len(progs))), h


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_step_bound_in_every_run(name) -> None:
    # A scan reads at most 2 n^2 registers; an update adds one write.
    progs = WORKLOADS[name]
    n = len(progs)
    worst = {"update": 0, "scan": 0}

    def final(w):
        for i, ops in enumerate(progs):
            for (op, _), cost in zip(ops, w.ret[i]):
                worst[op] = max(worst[op], cost)

    explore(setup_for(progs, True), final=final, max_depth=500)
    assert worst["scan"] <= 2 * n * n
    assert worst["update"] <= 2 * n * n + 1
    if name in ("two updaters and scan", "update then scan, twice"):
        assert worst["scan"] == 2 * n * n  # the bound is reached


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_adversary_double_collect_never_ends_afek_does(n) -> None:
    done, reads, updates = adversary(n, afek=False, rounds=5000)
    assert not done and reads == 5000 and updates == 5000 // (2 * n)
    done, reads, updates = adversary(n, afek=True, rounds=5000)
    assert done and reads == 4 * n  # two double collects, then it borrows a view


def test_scan_alone_takes_one_double_collect() -> None:
    w = World(setup_for([[("scan", None)], [], []], True))
    while not w.done[0]:
        w.step(0)
    assert w.ret[0] == [6]
    assert w.history[-1] == ("res", 0, (0, 0, 0))
