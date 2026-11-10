# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-digest/. The authors are listed in prov/A0RJGY.jsonl.

import bisect
import random

from q_digest import QDigest


def check_all_queries(q: QDigest, data: list[int]) -> None:
    """Check the rank error on every value and the quantile answer on every rank."""
    data = sorted(data)
    n = len(data)
    err = q.levels * (q.n // q.k)
    for x in range(1 << q.levels):
        true = bisect.bisect_right(data, x)
        est = q.rank(x)
        assert 0 <= true - est <= err, (x, true, est, err)
    for r in range(1, n + 1):
        x = q.query(r)
        below = bisect.bisect_left(data, x)  # R(x - 1)
        at_most = bisect.bisect_right(data, x)  # R(x)
        assert at_most >= r
        assert below <= r - 1 + err


def build(stream: list[int], levels: int, k: int) -> QDigest:
    q = QDigest(levels, k)
    for x in stream:
        q.insert(x)
        q.check_invariant()
        assert len(q) <= 4 * k + 1
    return q


def test_worked_example() -> None:
    stream = [1, 6, 3, 3, 0, 7, 3, 5, 3, 2, 6, 4, 3, 1, 7, 3]
    q = QDigest(3, 5)
    for x in stream:
        q.insert(x, auto_compress=False)
    q.compress()
    q.check_invariant(compressed=True)
    assert q.count == {(0, 2): 1, (0, 3): 6, (0, 6): 2, (0, 7): 2, (2, 0): 3, (2, 1): 2}
    assert [q.rank(x) for x in range(8)] == [0, 0, 1, 10, 10, 10, 12, 16]
    assert q.query(8) == 3
    check_all_queries(q, stream)


def test_edge_cases() -> None:
    q = QDigest(0, 1)
    q.insert(0)
    assert q.query(1) == 0
    q = build([5] * 100, 4, 3)
    check_all_queries(q, [5] * 100)
    assert q.query(1) == 5 and q.query(100) == 5


def test_adversarial_streams() -> None:
    levels = 6
    u = 1 << levels
    bitrev = [int(format(i, "06b")[::-1], 2) for i in range(u)]
    streams = [
        list(range(u)) * 5,
        list(range(u - 1, -1, -1)) * 5,
        bitrev * 5,
        [0 if i % 2 else u - 1 for i in range(300)],
        [min(u - 1, i // 7) for i in range(400)],
    ]
    for k in (2, 5, 12, 30):
        for stream in streams:
            q = build(stream, levels, k)
            q.compress()
            q.check_invariant(compressed=True)
            check_all_queries(q, stream)


def test_random_streams() -> None:
    rng = random.Random(2004)
    for trial in range(500):
        levels = rng.randint(1, 6)
        k = rng.randint(1, 12)
        n = rng.randint(1, 120)
        if trial % 2:
            stream = [rng.randrange(1 << levels) for _ in range(n)]
        else:
            stream = [min((1 << levels) - 1, int(rng.expovariate(0.3))) for _ in range(n)]
        q = build(stream, levels, k)
        check_all_queries(q, stream)
        q.compress()
        q.check_invariant(compressed=True)
        check_all_queries(q, stream)


def test_merge() -> None:
    rng = random.Random(11)
    for _ in range(200):
        levels, k = rng.randint(2, 6), rng.randint(1, 10)
        a = [rng.randrange(1 << levels) for _ in range(rng.randint(1, 80))]
        b = [rng.randrange(1 << levels) for _ in range(rng.randint(1, 80))]
        qa, qb = build(a, levels, k), build(b, levels, k)
        qa.merge(qb)
        qa.check_invariant(compressed=True)
        check_all_queries(qa, a + b)
