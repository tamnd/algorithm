# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-partitioning/. The authors are listed in prov/J597QM.jsonl.

import random

from geometric_partitioning import GeometricIndex


def random_postings(rng: random.Random, docs: int, vocab: int) -> list[tuple[str, int, int]]:
    out = []
    for d in range(1, docs + 1):
        for t in rng.sample(range(vocab), rng.randint(0, min(vocab, 6))):
            out.append((f"t{t}", d, rng.randint(1, 3)))
    return out


def direct(postings: list[tuple[str, int, int]]) -> dict[str, list[tuple[int, int]]]:
    m: dict[str, list[tuple[int, int]]] = {}
    for t, d, f in postings:
        m.setdefault(t, []).append((d, f))
    return {t: sorted(p) for t, p in m.items()}


def v(t: int, r: int) -> int:
    """The number of times r divides t, for t >= 1."""
    c = 0
    while t % r == 0:
        t //= r
        c += 1
    return c


def floor_log(m: int, r: int) -> int:
    """floor(log_r m) for m >= 1, in integers."""
    c = 0
    while m >= r:
        m //= r
        c += 1
    return c


def exact_total(m: int, r: int, b: int) -> int:
    """Postings written by m flushes: flush t forms (t mod r^(v_r(t)+1)) b postings."""
    return b * sum(t % r ** (v(t, r) + 1) for t in range(1, m + 1))


def fill(idx: GeometricIndex, count: int) -> None:
    for i in range(count):
        idx.add(("x", i + 1, 1))


def test_radix_three_nine_bufferloads() -> None:
    idx = GeometricIndex(3, 1)
    sizes = []
    for t in range(1, 10):
        before = idx.written
        idx.add(("x", t, 1))
        sizes.append(idx.written - before)
        idx.check_invariant()
    assert sizes == [1, 2, 3, 1, 2, 6, 1, 2, 9]
    assert idx.written == 27
    assert [len(p) for p in idx.parts] == [0, 0, 9]


def test_radix_two_matches_doubling_sizes() -> None:
    idx = GeometricIndex(2, 4)
    fill(idx, 32)
    assert [len(p) for p in idx.parts] == [0, 0, 0, 32]
    assert idx.written == 4 * (1 + 2 + 1 + 4 + 1 + 2 + 1 + 8)


def test_partition_contents() -> None:
    idx = GeometricIndex(3, 2)
    fill(idx, 2 * 14)  # 14 = 112 in base 3
    assert [len(p) for p in idx.parts] == [4, 6, 18]
    idx.check_invariant()


def test_edge_cases() -> None:
    idx = GeometricIndex(2, 1)
    assert idx.postings("a") == [] and idx.all_postings() == []
    idx.add(("a", 3, 1))
    assert idx.parts == [[("a", 3, 1)]] and idx.buffer == []
    for bad in [(1, 1), (2, 0)]:
        try:
            GeometricIndex(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad parameters were accepted")


def test_random_union_and_write_bound() -> None:
    rng = random.Random(20261118)
    for _ in range(150):
        r = rng.randint(2, 5)
        b = rng.randint(1, 6)
        stream = random_postings(rng, rng.randint(0, 40), rng.randint(1, 12))
        idx = GeometricIndex(r, b)
        inserted = []
        for x in stream:
            idx.add(x)
            inserted.append(x)
            idx.check_invariant()
            assert idx.all_postings() == sorted(inserted)
            m = idx.flushes
            bound = (r - 1) * (1 + floor_log(m, r)) if m >= 1 else 0
            assert max(idx.writes.values()) <= bound
            assert idx.written == exact_total(m, r, b)
        want = direct(inserted)
        for t in set(want) | {"absent"}:
            assert idx.postings(t) == want.get(t, [])


def test_bound_is_reached() -> None:
    # With r^K flushes, the first postings are written (r - 1) K + 1 times: r - 1 at
    # each of the levels 1..K and once more when they reach level K + 1.
    for r in (2, 3, 4):
        idx = GeometricIndex(r, 1)
        fill(idx, r ** 3)
        assert max(idx.writes.values()) == (r - 1) * 3 + 1
        assert (r - 1) * 3 + 1 <= (r - 1) * (1 + floor_log(r ** 3, r))
