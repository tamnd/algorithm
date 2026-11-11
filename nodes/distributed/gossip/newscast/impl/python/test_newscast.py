# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newscast/. The authors are listed in prov/BZKMAQ.jsonl.

from newscast import Newscast, stats


def check_invariants(s: Newscast) -> None:
    for p in s.alive:
        cache = s.cache[p]
        assert len(cache) <= s.c
        assert p not in cache
        assert all(ts <= s.time for ts in cache.values())


def test_invariants_and_full_caches():
    s = Newscast(300, 15, 1)
    for _ in range(20):
        s.cycle()
        check_invariants(s)
    assert all(len(s.cache[p]) == 15 for p in s.alive)


def test_in_degree_is_uneven():
    # the mean in-degree is c, but the spread is far wider than in a random
    # graph with out-degree c, where the variance is about c (1 - c/n)
    for seed in range(3):
        s = Newscast(500, 20, seed)
        for _ in range(25):
            s.cycle()
        m, v = stats(s.in_degrees().values())
        assert abs(m - 20) < 1e-9
        assert v > 2.5 * 20 * (1 - 20 / 500)


def test_dead_links_are_removed_after_a_large_crash():
    for seed in range(3):
        s = Newscast(500, 20, seed)
        for _ in range(15):
            s.cycle()
        crash_time = s.time
        s.crash(0.5)
        before = s.dead_links()
        assert before > 0.4 * 250 * 20
        for _ in range(12):
            s.cycle()
        assert s.dead_links() < 0.01 * before
        assert s.largest_component() == len(s.alive)
        # an item about a crashed node is never refreshed
        for p in s.alive:
            for q, ts in s.cache[p].items():
                if q not in s.alive:
                    assert ts <= crash_time


def test_churn_keeps_overlay_connected():
    for seed in range(2):
        s = Newscast(400, 20, seed)
        for _ in range(10):
            s.cycle()
        for _ in range(30):
            s.churn_cycle(0.02)
        check_invariants(s)
        assert s.largest_component() == len(s.alive)
        links = sum(len(s.cache[p]) for p in s.alive)
        assert s.dead_links() < 0.05 * links


def test_from_a_ring_start():
    s = Newscast(400, 10, 4, init="ring")
    for _ in range(30):
        s.cycle()
    # after mixing, most cache entries are far from the ring neighbours
    # (a uniform view would have 95 percent of them far; Newscast keeps
    # some locality, as the clustering found by Jelasity et al. shows)
    far = sum(1 for p in s.alive for q in s.cache[p] if min((q - p) % 400, (p - q) % 400) > 10)
    assert far > 0.7 * 400 * 10
