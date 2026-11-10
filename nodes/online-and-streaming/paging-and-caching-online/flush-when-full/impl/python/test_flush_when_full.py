# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flush-when-full/. The authors are listed in prov/9TFRYX.jsonl.

import random
from collections.abc import Hashable, Sequence

from flush_when_full import FlushWhenFull, flush_when_full


def opt_faults(sigma: Sequence[Hashable], k: int) -> int:
    """Optimal faults by search over all caches (small inputs only)."""
    best: dict[frozenset, int] = {frozenset(): 0}
    for p in sigma:
        new: dict[frozenset, int] = {}
        for c, f in best.items():
            if p in c:
                outs = [(c, f)]
            elif len(c) < k:
                outs = [(c | {p}, f + 1)]
            else:
                outs = [((c - {q}) | {p}, f + 1) for q in c]
            for c2, f2 in outs:
                if f2 < new.get(c2, f2 + 1):
                    new[c2] = f2
        best = new
    return min(best.values())


def lfd_faults(sigma: Sequence[Hashable], k: int) -> int:
    cache: set[Hashable] = set()
    faults, n = 0, len(sigma)
    for t, p in enumerate(sigma):
        if p in cache:
            continue
        faults += 1
        if len(cache) == k:
            def nxt(q: Hashable) -> int:
                return next((s for s in range(t + 1, n) if sigma[s] == q), n)
            cache.remove(max(cache, key=nxt))
        cache.add(p)
    return faults


def phases(sigma: Sequence[Hashable], k: int) -> list[set[Hashable]]:
    out: list[set[Hashable]] = []
    for p in sigma:
        if not out or (p not in out[-1] and len(out[-1]) == k):
            out.append(set())
        out[-1].add(p)
    return out


def random_marking_faults(sigma: Sequence[Hashable], k: int, rng: random.Random) -> int:
    cache: set[Hashable] = set()
    marked: set[Hashable] = set()
    faults = 0
    for p in sigma:
        if p not in cache:
            faults += 1
            if len(cache) == k:
                if marked == cache:
                    marked = set()
                cache.remove(rng.choice(sorted(cache - marked)))
            cache.add(p)
        marked.add(p)
    return faults


def lru_faults(sigma: Sequence[Hashable], k: int) -> int:
    order: list[Hashable] = []
    faults = 0
    for p in sigma:
        if p in order:
            order.remove(p)
        else:
            faults += 1
            if len(order) == k:
                order.pop(0)
        order.append(p)
    return faults


def test_example() -> None:
    sigma = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3]
    assert flush_when_full(sigma, 3) == 10
    assert lru_faults(sigma, 3) == 8
    assert opt_faults(sigma, 3) == 6
    c = FlushWhenFull(3)
    assert [sorted(c.request(p)) for p in sigma][3] == [1, 2, 3]
    assert c.flushes == 3 and c.cache == {3}


def test_edges() -> None:
    assert flush_when_full([], 3) == 0
    assert flush_when_full([4, 4, 4], 1) == 1
    assert flush_when_full([1, 2, 1, 2], 1) == 4
    assert flush_when_full([1, 2, 1, 2], 2) == 2


def test_faults_are_distinct_pages_per_phase() -> None:
    rng = random.Random(1)
    for _ in range(500):
        k = rng.randint(1, 5)
        sigma = [rng.randrange(k + 4) for _ in range(rng.randint(0, 60))]
        c = FlushWhenFull(k)
        for p in sigma:
            c.request(p)
            assert len(c.cache) <= k
        ph = phases(sigma, k)
        assert c.faults == sum(len(s) for s in ph)
        assert c.flushes == max(0, len(ph) - 1)


def test_within_k_times_opt() -> None:
    rng = random.Random(2)
    for _ in range(600):
        k = rng.randint(1, 4)
        sigma = [rng.randrange(rng.randint(1, k + 3)) for _ in range(rng.randint(0, 11))]
        opt = opt_faults(sigma, k)
        assert len(phases(sigma, k)) <= opt
        assert flush_when_full(sigma, k) <= k * opt


def test_worst_marking_algorithm() -> None:
    rng = random.Random(3)
    for _ in range(500):
        k = rng.randint(1, 5)
        sigma = [rng.randrange(k + 3) for _ in range(rng.randint(0, 50))]
        f = flush_when_full(sigma, k)
        assert f >= lru_faults(sigma, k)
        assert f >= random_marking_faults(sigma, k, rng)


def test_adversary_forces_ratio_k() -> None:
    for k in range(1, 7):
        c = FlushWhenFull(k)
        sigma = []
        for _ in range(60 * k):
            p = next(q for q in range(k + 1) if q not in c.cache)
            sigma.append(p)
            c.request(p)
        assert c.faults == len(sigma)
        opt = lfd_faults(sigma, k)
        assert opt <= k + (len(sigma) - k - 1) // k + 1
        assert c.faults >= k * (opt - k - 1)


def test_not_conservative_and_not_demand() -> None:
    sigma = [1, 2, 3, 2]
    c = FlushWhenFull(2)
    evicted = [c.request(p) for p in sigma]
    assert evicted[2] == {1, 2}
    assert c.faults == 4
    # The block 2 3 2 has 2 distinct pages and 3 faults.
    assert lru_faults(sigma, 2) == 3
