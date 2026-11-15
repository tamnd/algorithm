# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/url-frontier/. The authors are listed in prov/91KJAA.jsonl.

import heapq
import random

import pytest

from url_frontier import URLFrontier, host_of


def web(rng: random.Random, hosts: int, pages: int, links: int) -> dict[str, list[str]]:
    """A random web graph: each page links to `links` random pages, half of them on its own host."""
    urls = ["http://h%d.example/p%d" % (h, p) for h in range(hosts) for p in range(pages)]
    graph = {}
    for u in urls:
        own = [v for v in urls if host_of(v) == host_of(u)]
        graph[u] = [rng.choice(own) if rng.random() < 0.5 else rng.choice(urls) for _ in range(links)]
    return graph


def reachable(graph: dict[str, list[str]], seeds: list[str]) -> set[str]:
    seen, stack = set(seeds), list(seeds)
    while stack:
        for v in graph[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def crawl(graph, seeds, frontier, fetchers, rng, prio):
    """Simulate `fetchers` crawler threads. Return the list of (start, url) in the order of hand-out."""
    for s in seeds:
        frontier.add(s, prio[s])
    now, idle, inflight, log = 0.0, fetchers, [], []
    while True:
        while idle:
            r = frontier.next_url(now)
            if r is None:
                break
            url, start = r
            assert start >= now
            idle -= 1
            heapq.heappush(inflight, (start + rng.uniform(0.1, 2.0), url))
            log.append((start, url))
        if not inflight:
            return log
        finish, url = heapq.heappop(inflight)
        now, idle = max(now, finish), idle + 1
        for v in graph[url]:
            frontier.add(v, prio[v])


def run(seed: int, front: int, back: int, fetchers: int, biased: bool):
    rng = random.Random(seed)
    graph = web(rng, hosts=rng.randrange(1, 9), pages=rng.randrange(1, 12), links=rng.randrange(1, 5))
    prio = {u: rng.randrange(front) for u in graph}
    gaps = {host_of(u): rng.uniform(0.5, 5.0) for u in graph}
    seeds = rng.sample(sorted(graph), rng.randrange(1, 4))
    f = URLFrontier(front, back, gaps.__getitem__, random.Random(seed + 1) if biased else None)
    pulls: list[tuple[str, int]] = []

    def on_pull(url: str, i: int) -> None:
        # The strict selector takes the highest priority queue that is not empty.
        if not biased:
            assert all(not f.front[k] for k in range(i))
        pulls.append((url, i))

    f.on_pull = on_pull
    added: list[tuple[str, int]] = []
    real_add = f.add

    def add(url: str, priority: int) -> bool:
        ok = real_add(url, priority)
        if ok:
            added.append((url, priority))
        return ok

    f.add = add  # type: ignore[method-assign]
    log = crawl(graph, seeds, f, fetchers, rng, prio)
    return graph, seeds, gaps, log, added, pulls, f


@pytest.mark.parametrize("biased", [False, True])
def test_simulated_crawl(biased: bool) -> None:
    for seed in range(60):
        rng = random.Random(1000 + seed)
        front, back, fetchers = rng.randrange(1, 5), rng.randrange(1, 7), rng.randrange(1, 4)
        graph, seeds, gaps, log, added, pulls, f = run(seed, front, back, fetchers, biased)
        urls = [u for _, u in log]
        # Every reachable URL is fetched, and each exactly once.
        assert len(urls) == len(set(urls))
        assert set(urls) == reachable(graph, seeds)
        assert len(f) == 0
        # No host is contacted twice within its politeness gap.
        last: dict[str, float] = {}
        for start, u in sorted(log):
            h = host_of(u)
            if h in last:
                assert start - last[h] >= gaps[h] - 1e-9
            last[h] = start
        # Inside each front queue, URLs leave in the order they came in.
        for i in range(front):
            assert [u for u, p in pulls if p == i] == [u for u, p in added if p == i]
        # A host has at most one back queue at any time, and every queue holds one host.
        assert not f.queue_of and all(o is None for o in f.owner)


def test_back_queue_holds_one_host_during_crawl() -> None:
    f = URLFrontier(2, 2, lambda h: 1.0)
    for u, p in [("http://a/1", 0), ("http://a/2", 0), ("http://b/1", 1), ("http://c/1", 0), ("http://a/3", 1)]:
        f.add(u, p)
    got = []
    now = 0.0
    while True:
        r = f.next_url(now)
        if r is None:
            break
        for j, q in enumerate(f.back):
            assert len({host_of(u) for u in q}) <= 1
            if q:
                assert f.queue_of[f.owner[j]] == j
        got.append(r)
        now = r[1]
    # b/1 has a lower priority than a/2 but goes first, because host a must wait for its gap.
    assert got == [("http://a/1", 0.0), ("http://c/1", 0.0), ("http://b/1", 0.0), ("http://a/2", 1.0), ("http://a/3", 2.0)]


def test_host_that_returns_keeps_its_gap() -> None:
    # Host a leaves its back queue after one URL and comes back later through the front queues.
    f = URLFrontier(1, 1, lambda h: 10.0)
    f.add("http://a/1", 0)
    assert f.next_url(0.0) == ("http://a/1", 0.0)
    assert f.next_url(1.0) is None
    f.add("http://a/2", 0)
    assert f.next_url(2.0) == ("http://a/2", 10.0)


def test_duplicates_and_errors() -> None:
    f = URLFrontier(1, 1, lambda h: 1.0)
    assert f.add("http://a/1", 0)
    assert not f.add("http://a/1", 0)
    assert len(f) == 1
    assert host_of("https://x.org/a/b") == "x.org"
    with pytest.raises(ValueError):
        URLFrontier(0, 1, lambda h: 1.0)
