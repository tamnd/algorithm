# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clh-lock/. The authors are listed in prov/RHBQNE.jsonl.

from clh_lock import client, home, init
from interleave import explore, max_passage_rmr, no_progress, run, starvation


def test_two_processes_two_rounds() -> None:
    g = explore([client(2)] * 2, init(2), home=home(2), cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(2)] == [5, 5]
    # each process spins on the node of its predecessor, which lives elsewhere
    assert [max_passage_rmr(g, p, "dsm") for p in range(2)] == [float("inf")] * 2


def test_three_processes() -> None:
    g = explore([client(1)] * 3, init(3), home=home(3), cache=True)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(3)] == [5, 5, 5]


def test_starvation_free_forever() -> None:
    g = explore([client(None)] * 2, init(2))
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def test_nodes_move_between_processes() -> None:
    # after a passage each process owns the node of its predecessor
    m = run([client(1)] * 3, init(3), policy=lambda t, e, r: e[0])
    assert m.entries == [0, 1, 2] and m.violations == []
    assert m.mem["tail"] == 2


def test_random_runs_constant_cost() -> None:
    for seed in range(50):
        n = 2 + seed % 7
        m = run([client(3)] * n, init(n), seed=seed)
        assert m.violations == [] and len(m.entries) == 3 * n
        assert all(cc <= 5 for p in range(n) for cc, _ in m.passages[p])
