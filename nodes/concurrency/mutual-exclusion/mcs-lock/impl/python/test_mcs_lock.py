# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcs-lock/. The authors are listed in prov/YFEJH1.jsonl.

from interleave import explore, max_passage_rmr, no_progress, run, starvation
from mcs_lock import client, home, init


def test_two_processes_two_rounds() -> None:
    g = explore([client(2)] * 2, init(2), home=home(2), cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(2)] == [8, 8]
    # process 0 holds the tail word, so its fetch-and-store and compare-and-swap are local
    assert [max_passage_rmr(g, p, "dsm") for p in range(2)] == [2, 4]


def test_three_processes() -> None:
    g = explore([client(1)] * 3, init(3), home=home(3), cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(3)] == [8, 8, 8]
    assert [max_passage_rmr(g, p, "dsm") for p in range(3)] == [2, 4, 4]


def test_starvation_free_forever() -> None:
    g = explore([client(None)] * 2, init(2))
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def test_random_runs_constant_cost() -> None:
    for seed in range(50):
        n = 2 + seed % 7
        m = run([client(3)] * n, init(n), home=home(n), seed=seed)
        assert m.violations == [] and len(m.entries) == 3 * n
        assert all(cc <= 8 and dsm <= 4 for p in range(n) for cc, dsm in m.passages[p])
