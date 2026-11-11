# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclon/. The authors are listed in prov/NQF31F.jsonl.

from cyclon import Cyclon, stats


def check_invariants(s: Cyclon) -> None:
    for p in s.alive:
        assert len(s.cache[p]) <= s.c
        assert p not in s.cache[p]


def test_in_degree_is_balanced():
    # a random graph with out-degree c has in-degree variance c (1 - c/n);
    # Cyclon's swaps keep the in-degree much closer to c
    for seed in range(2):
        s = Cyclon(500, 20, 8, seed)
        for _ in range(30):
            s.cycle()
            check_invariants(s)
        m, v = stats(s.in_degrees().values())
        assert abs(m - 20) < 0.05
        assert v < 0.6 * 20 * (1 - 20 / 500)


def test_low_clustering_from_a_ring_start():
    s = Cyclon(500, 20, 8, 3, init="ring")
    before = s.clustering()
    for _ in range(30):
        s.cycle()
    assert before > 0.4
    assert s.clustering() < 0.12          # about 0.076 for a random graph of this density


def test_dead_links_are_removed():
    for seed in range(2):
        s = Cyclon(500, 20, 8, seed)
        for _ in range(15):
            s.cycle()
        s.crash(0.5)
        start = s.dead_links()
        history = [start]
        for _ in range(40):
            s.cycle()
            history.append(s.dead_links())
        assert history[10] < history[0]
        assert history[-1] < 0.05 * start
        assert s.largest_component() == len(s.alive)


def test_join_gives_in_degree_without_changing_other_out_degrees():
    s = Cyclon(300, 15, 6, 4)
    for _ in range(10):
        s.cycle()
    sizes = {p: len(s.cache[p]) for p in s.alive}
    p = s.join()
    assert all(len(s.cache[q]) == sizes[q] for q in sizes)
    assert s.in_degrees()[p] == len(s.cache[p]) > 0.5 * 15


def test_churn_keeps_overlay_connected():
    s = Cyclon(400, 20, 8, 5)
    for _ in range(10):
        s.cycle()
    for _ in range(25):
        s.churn_cycle(0.01)
    check_invariants(s)
    assert s.largest_component() == len(s.alive)
    links = sum(len(s.cache[p]) for p in s.alive)
    assert s.dead_links() < 0.15 * links
