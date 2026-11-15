# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/focused-crawling/. The authors are listed in prov/CT80NW.jsonl.

import math
import random
from collections import deque

import pytest

from focused_crawling import NaiveBayes, focused_crawl, harvest_rate

TOPIC = ["t%d" % i for i in range(20)]
OTHER = ["g%d" % i for i in range(60)]


def text(rng: random.Random, on: bool, length: int = 30) -> list[str]:
    share = 0.3 if on else 0.03
    return [rng.choice(TOPIC) if rng.random() < share else rng.choice(OTHER) for _ in range(length)]


def planted(rng: random.Random, n: int, share: float, out: int, stay: float):
    """A web graph in which on-topic pages cluster: a link stays inside the class of its page with probability `stay`."""
    label = [rng.random() < share for _ in range(n)]
    group = {True: [u for u in range(n) if label[u]], False: [u for u in range(n) if not label[u]]}
    graph = {}
    for u in range(n):
        graph[u] = [rng.choice(group[label[u]]) if rng.random() < stay else rng.randrange(n) for _ in range(out)]
    words = [text(rng, label[u]) for u in range(n)]
    return graph, label, words


def classifier(rng: random.Random) -> NaiveBayes:
    labels = [i % 2 for i in range(200)]
    return NaiveBayes([text(rng, y == 1) for y in labels], labels)


def bfs_crawl(graph, seeds, budget):
    seen, queue, order = set(seeds), deque(seeds), []
    while queue and len(order) < budget:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return order


def reference(graph, seeds, rel, budget, hard):
    """Pick the next page by brute force: the unfetched page with the largest priority, ties to the smaller id."""
    order: list = []
    while len(order) < budget:
        prio = {s: 1.0 for s in seeds}
        for u in order:
            if hard is None or rel(u) >= hard:
                for v in graph[u]:
                    prio[v] = max(prio.get(v, -1.0), rel(u))
        cand = [(-p, v) for v, p in prio.items() if v not in order]
        if not cand:
            break
        order.append(min(cand)[1])
    return order


def reachable(graph, seeds):
    seen, stack = set(seeds), list(seeds)
    while stack:
        for v in graph[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def setup(seed: int, n: int = 1000):
    rng = random.Random(seed)
    graph, label, words = planted(rng, n, share=0.2, out=6, stay=0.6)
    nb = classifier(rng)
    score = [nb.prob(w) for w in words]
    seeds = rng.sample([u for u in range(n) if label[u]], 3)
    return graph, label, score, seeds


def test_order_matches_brute_force() -> None:
    for seed in range(30):
        rng = random.Random(seed)
        n = rng.randrange(1, 40)
        graph = {u: [rng.randrange(n) for _ in range(rng.randrange(0, 4))] for u in range(n)}
        # Few distinct scores, so ties occur and the tie rule is tested.
        score = [rng.choice([0.0, 0.25, 0.5, 0.75, 1.0]) for _ in range(n)]
        seeds = rng.sample(range(n), rng.randrange(1, min(n, 3) + 1))
        budget = rng.randrange(1, n + 2)
        for hard in (None, 0.5):
            got = focused_crawl(graph.__getitem__, seeds, score.__getitem__, budget, hard)
            assert got == reference(graph, seeds, score.__getitem__, budget, hard)


def test_each_page_once_and_reachable() -> None:
    graph, label, score, seeds = setup(7)
    order = focused_crawl(graph.__getitem__, seeds, score.__getitem__, 10**9)
    assert len(order) == len(set(order))
    # Soft focus follows every link, so with no budget it fetches all reachable pages.
    assert set(order) == reachable(graph, seeds)
    hard = focused_crawl(graph.__getitem__, seeds, score.__getitem__, 10**9, hard=0.5)
    assert len(hard) == len(set(hard)) and set(hard) <= reachable(graph, seeds)


def test_hard_focus_follows_only_relevant_pages() -> None:
    graph, label, score, seeds = setup(8)
    order = focused_crawl(graph.__getitem__, seeds, score.__getitem__, 300, hard=0.5)
    # Every fetched page that is not a seed is linked from a fetched page with score at least 0.5.
    fetched = set(order)
    for v in order:
        if v not in seeds:
            assert any(v in graph[u] and score[u] >= 0.5 for u in fetched)


def test_budget_and_empty() -> None:
    graph = {0: [1, 2], 1: [], 2: []}
    assert focused_crawl(graph.__getitem__, [0], lambda u: 0.5, 2) == [0, 1]
    assert focused_crawl(graph.__getitem__, [], lambda u: 0.5, 5) == []
    assert focused_crawl(graph.__getitem__, [0], lambda u: 0.5, 0) == []


def test_small_example() -> None:
    # The example of the page: soft focus goes into the on-topic branch first.
    graph = {"a": ["b", "c"], "b": ["d", "e"], "c": ["f", "g"], "d": [], "e": [], "f": ["h"], "g": [], "h": []}
    score = {"a": 0.9, "b": 0.1, "c": 0.8, "d": 0.2, "e": 0.1, "f": 0.9, "g": 0.3, "h": 0.7}
    assert focused_crawl(graph.__getitem__, ["a"], score.__getitem__, 8) == ["a", "b", "c", "f", "h", "g", "d", "e"]
    assert focused_crawl(graph.__getitem__, ["a"], score.__getitem__, 8, hard=0.5) == ["a", "b", "c", "f", "h", "g"]
    assert bfs_crawl(graph, ["a"], 8) == ["a", "b", "c", "d", "e", "f", "g", "h"]


def test_harvest_rate_is_higher_than_bfs_on_planted_graphs() -> None:
    # A measured effect on these fixed seeds, not a theorem.
    focus, base = [], []
    for seed in range(10):
        graph, label, score, seeds = setup(100 + seed)
        on = label.__getitem__
        focus.append(harvest_rate(focused_crawl(graph.__getitem__, seeds, score.__getitem__, 200), on))
        base.append(harvest_rate(bfs_crawl(graph, seeds, 200), on))
    assert all(f > b for f, b in zip(focus, base))
    assert sum(focus) / 10 > sum(base) / 10 + 0.15


def test_naive_bayes_matches_direct_formula() -> None:
    nb = NaiveBayes([["a", "a", "b"], ["b", "c"]], [1, 0])
    # P(1) ∝ 1/2 · (2 + 1)/(3 + 3) and P(0) ∝ 1/2 · (0 + 1)/(2 + 3), so P(1 | "a") = 5/7.
    assert math.isclose(nb.prob(["a"]), 5 / 7)
    assert math.isclose(nb.prob(["zzz"]), 1 / 2)
    for d in (["a"] * 2000, ["c"] * 2000):
        assert 0.0 <= nb.prob(d) <= 1.0
    with pytest.raises(ValueError):
        NaiveBayes([["a"]], [1])
