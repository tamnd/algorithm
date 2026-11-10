# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marking-algorithm/. The authors are listed in prov/5WP5GD.jsonl.

import random
from collections.abc import Hashable, Sequence

from marking_algorithm import MarkingCache, marking, oldest


def opt_faults(sigma: Sequence[Hashable], k: int) -> int:
    """Optimal faults by search over all caches (small inputs only)."""
    states = {frozenset()}
    best = {frozenset(): 0}
    for p in sigma:
        new: dict[frozenset, int] = {}
        for c in states:
            f = best[c]
            if p in c:
                outs = [(c, f)]
            elif len(c) < k:
                outs = [(c | {p}, f + 1)]
            else:
                outs = [((c - {q}) | {p}, f + 1) for q in c]
            for c2, f2 in outs:
                if f2 < new.get(c2, f2 + 1):
                    new[c2] = f2
        states, best = set(new), new
    return min(best.values())


def lfd_faults(sigma: Sequence[Hashable], k: int) -> int:
    """Optimal faults by furthest in the future, O(n^2) time."""
    cache: set[Hashable] = set()
    faults = 0
    n = len(sigma)
    for t, p in enumerate(sigma):
        if p in cache:
            continue
        faults += 1
        if len(cache) == k:
            def nxt(q: Hashable) -> int:
                for s in range(t + 1, n):
                    if sigma[s] == q:
                        return s
                return n
            cache.remove(max(cache, key=nxt))
        cache.add(p)
    return faults


def phase_count(sigma: Sequence[Hashable], k: int) -> int:
    count, seen = 0, set()
    for p in sigma:
        if not seen or (p not in seen and len(seen) == k):
            count += 1
            seen = set()
        seen.add(p)
    return count


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


def fifo_victims(sigma: Sequence[Hashable], k: int) -> list[Hashable | None]:
    queue: list[Hashable] = []
    out: list[Hashable | None] = []
    for p in sigma:
        v = None
        if p not in queue:
            if len(queue) == k:
                v = queue.pop(0)
            queue.append(p)
        out.append(v)
    return out


def newest(unmarked: list[Hashable]) -> Hashable:
    return unmarked[-1]


def test_example() -> None:
    sigma = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    assert marking(sigma, 3) == (10, 4)
    assert marking(sigma, 3, newest) == (8, 4)
    assert opt_faults(sigma, 3) == 7
    m = MarkingCache(3)
    victims = [m.request(p) for p in sigma]
    assert victims == [None, None, None, 1, 2, 3, 4, None, None, 5, 1, 2]


def test_edges() -> None:
    assert marking([], 2) == (0, 0)
    assert marking([5], 1) == (1, 1)
    assert marking([1, 1, 2, 2, 1], 1) == (3, 3)
    assert marking([1, 2, 1, 2], 2) == (2, 1)


def test_bound_with_many_rules() -> None:
    rng = random.Random(1)
    rules = [oldest, newest, lambda u: u[len(u) // 2], lambda u: rng.choice(u), lambda u: min(u)]
    for _ in range(600):
        k = rng.randint(1, 4)
        pages = rng.randint(1, k + 3)
        sigma = [rng.randrange(pages) for _ in range(rng.randint(0, 11))]
        opt = opt_faults(sigma, k)
        n_ph = phase_count(sigma, k)
        assert n_ph <= opt
        for rule in rules:
            f, ph = marking(sigma, k, rule)
            assert ph == n_ph
            assert f <= k * ph <= k * opt


def test_never_evicts_a_marked_page() -> None:
    rng = random.Random(2)
    for _ in range(500):
        k = rng.randint(1, 5)
        sigma = [rng.randrange(k + 3) for _ in range(rng.randint(0, 40))]
        m = MarkingCache(k, lambda u: rng.choice(u))
        seen: set[Hashable] = set()
        for p in sigma:
            if p not in seen and len(seen) == k:
                seen = set()
            v = m.request(p)
            assert v is None or v not in seen
            seen.add(p)
            assert m.cache() >= seen and len(m.cache()) <= k


def test_oldest_rule_is_lru() -> None:
    rng = random.Random(3)
    for _ in range(500):
        k = rng.randint(1, 6)
        sigma = [rng.randrange(2 * k + 2) for _ in range(rng.randint(0, 80))]
        assert marking(sigma, k)[0] == lru_faults(sigma, k)


def test_adversary_forces_ratio_k() -> None:
    for k in range(1, 7):
        for rule in (oldest, newest):
            m = MarkingCache(k, rule)
            sigma = []
            for _ in range(60 * k):
                missing = next(p for p in range(k + 1) if p not in m.cache())
                sigma.append(missing)
                m.request(missing)
            opt = lfd_faults(sigma, k)
            assert m.faults == len(sigma)
            # k cold faults, then LFD faults at most once in each k requests.
            assert opt <= k + (len(sigma) - k - 1) // k + 1
            assert m.faults >= k * (opt - k - 1)


def test_fifo_is_not_marking_but_within_k() -> None:
    sigma = [1, 2, 3, 4, 2, 1]
    assert fifo_victims(sigma, 3)[-1] == 2
    rng = random.Random(4)
    for _ in range(500):
        k = rng.randint(1, 5)
        sigma = [rng.randrange(k + 4) for _ in range(rng.randint(0, 50))]
        # FIFO never shrinks its cache, so its faults are its evictions plus its first min(k, d) loads.
        fifo = sum(v is not None for v in fifo_victims(sigma, k)) + min(k, len(set(sigma)))
        assert fifo <= k * lfd_faults(sigma, k)
