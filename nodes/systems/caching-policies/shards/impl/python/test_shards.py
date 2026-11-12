# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shards/. The authors are listed in prov/8186QR.jsonl.

import random

import pytest

from shards import P, LiveMarks, Shards, item_hash, shards_curve


def exact_distances(trace):
    stack, out = [], []
    for x in trace:
        if x in stack:
            d = stack.index(x)
            del stack[d]
            out.append(d)
        else:
            out.append(None)
        stack.insert(0, x)
    return out


def exact_curve(trace, sizes):
    """The exact LRU curve, with a Fenwick tree over the times of last use."""
    n = len(trace)
    tree = [0] * (n + 1)

    def add(i, v):
        while i <= n:
            tree[i] += v
            i += i & -i

    def prefix(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    last, live, dist = {}, 0, []
    for t, x in enumerate(trace, start=1):
        p = last.get(x)
        if p is not None:
            dist.append(live - prefix(p))
            add(p, -1)
            live -= 1
        add(t, 1)
        live += 1
        last[x] = t
    dist.sort()
    out, j = [], 0
    for c in sizes:
        while j < len(dist) and dist[j] < c:
            j += 1
        out.append(1 - j / n)
    return out


def zipf_trace(seed, n, m, s):
    rng = random.Random(seed)
    weights = [1 / (i + 1) ** s for i in range(m)]
    ids = list(range(m))
    rng.shuffle(ids)  # so that popularity is not tied to the item number
    return [ids[i] for i in rng.choices(range(m), weights, k=n)]


def mae(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def test_live_marks_match_the_lru_stack() -> None:
    rng = random.Random(1)
    marks = LiveMarks()
    trace = [rng.randrange(50) for _ in range(3000)]
    assert [marks.access(x) for x in trace] == exact_distances(trace)
    assert marks.size <= 2 * 50 + 16


def test_rate_one_is_exact() -> None:
    rng = random.Random(2)
    for _ in range(20):
        trace = [rng.randrange(40) for _ in range(rng.randint(1, 500))]
        sizes = list(range(45))
        got = shards_curve(trace, sizes, rate=1.0)
        assert got == pytest.approx(exact_curve(trace, sizes), abs=1e-12)


def test_large_fixed_size_is_exact() -> None:
    rng = random.Random(3)
    trace = [rng.randrange(300) for _ in range(5000)]
    sizes = list(range(0, 320, 5))
    s = Shards(rate=1.0, s_max=300).feed(trace)
    assert s.T == P
    assert s.curve(sizes) == pytest.approx(exact_curve(trace, sizes), abs=1e-12)


def test_sampling_is_by_item() -> None:
    # every request to a sampled item is seen, and no request to another item
    T = round(0.1 * P)
    items = range(10_000)
    chosen = {x for x in items if item_hash(x) < T}
    assert 800 < len(chosen) < 1200
    s = Shards(rate=0.1).feed(list(items) * 2)
    assert set(s.marks.last) == chosen
    assert s.sampled == 2 * len(chosen)


def test_fixed_size_keeps_at_most_s_max_items() -> None:
    trace = zipf_trace(4, 50_000, 20_000, 0.8)
    s = Shards(rate=1.0, s_max=500)
    t_before = s.T
    for x in trace:
        s.access(x)
        assert len(s.marks.last) <= 500
        assert s.T <= t_before
        t_before = s.T
    assert all(item_hash(x) < s.T for x in s.marks.last)


def test_zipf_trace_error_is_small() -> None:
    trace = zipf_trace(5, 100_000, 20_000, 0.9)
    sizes = list(range(0, 20_001, 100))
    exact = exact_curve(trace, sizes)
    salts = range(4)
    plain = [mae(shards_curve(trace, sizes, rate=0.1, salt=s), exact) for s in salts]
    adjusted = [mae(shards_curve(trace, sizes, rate=0.1, salt=s, adjust=True), exact) for s in salts]
    fixed = [mae(shards_curve(trace, sizes, rate=1.0, s_max=4000, salt=s), exact) for s in salts]
    # Measured with these seeds, the mean over the 4 salts is about 0.050 for R = 0.1,
    # 0.008 for R = 0.1 with the adjustment, and 0.016 for s_max = 4000.
    assert sum(adjusted) / 4 < 0.012
    assert max(adjusted) < 0.02
    assert sum(adjusted) < sum(plain)
    assert sum(fixed) / 4 < 0.025


def test_other_salts_give_other_samples() -> None:
    trace = zipf_trace(6, 20_000, 5000, 0.9)
    a = Shards(rate=0.05, salt=1).feed(trace)
    b = Shards(rate=0.05, salt=2).feed(trace)
    assert set(a.marks.last) != set(b.marks.last)


def test_rejects_bad_rate() -> None:
    with pytest.raises(ValueError):
        Shards(rate=0)
