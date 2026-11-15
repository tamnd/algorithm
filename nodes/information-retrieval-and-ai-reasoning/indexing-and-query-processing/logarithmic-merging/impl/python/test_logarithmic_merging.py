# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logarithmic-merging/. The authors are listed in prov/GRDTV2.jsonl.

import random

from logarithmic_merging import LogarithmicIndex, merge


def random_postings(rng: random.Random, docs: int, vocab: int) -> list[tuple[str, int, int]]:
    """Postings of a random collection, document by document, as a stream to index."""
    out = []
    for d in range(1, docs + 1):
        terms = rng.sample(range(vocab), rng.randint(0, min(vocab, 6)))
        for t in terms:
            out.append((f"t{t}", d, rng.randint(1, 3)))
    return out


def direct(postings: list[tuple[str, int, int]]) -> dict[str, list[tuple[int, int]]]:
    m: dict[str, list[tuple[int, int]]] = {}
    for t, d, f in postings:
        m.setdefault(t, []).append((d, f))
    return {t: sorted(p) for t, p in m.items()}


def floor_log2(x: int) -> int:
    return x.bit_length() - 1


def trailing_zeros(x: int) -> int:
    return (x & -x).bit_length() - 1


def test_merge() -> None:
    assert merge([], []) == []
    assert merge([("a", 1, 1), ("b", 2, 1)], [("a", 3, 1)]) == [("a", 1, 1), ("a", 3, 1), ("b", 2, 1)]


def test_sizes_follow_binary_counter() -> None:
    idx = LogarithmicIndex(4)
    for t in range(1, 33):
        for j in range(4):
            idx.add(("x", 4 * (t - 1) + j + 1, 1))
        present = [i for i, lv in enumerate(idx.levels) if lv is not None]
        assert present == [i for i in range(t.bit_length()) if t >> i & 1]
        idx.check_invariant()
    # 32 flushes of 4 postings: k log2 k flushes of work, each worth n postings.
    assert idx.merged == 4 * 32 * 5


def test_example_eight_flushes() -> None:
    idx = LogarithmicIndex(4)
    per_flush = []
    for t in range(1, 9):
        before = idx.merged
        for j in range(4):
            idx.add(("x", 4 * (t - 1) + j + 1, 1))
        per_flush.append(idx.merged - before)
    assert per_flush == [0, 8, 0, 24, 0, 8, 0, 56]
    assert idx.merged == 96
    assert max(idx.merge_count.values()) == 3
    naive = sum(4 * t for t in range(2, 9))
    assert naive == 140


def test_edge_cases() -> None:
    idx = LogarithmicIndex(1)
    assert idx.postings("a") == [] and idx.all_postings() == []
    idx.add(("a", 1, 2))
    assert idx.levels[0] == [("a", 1, 2)] and idx.z0 == []
    assert idx.postings("a") == [(1, 2)]
    try:
        LogarithmicIndex(0)
    except ValueError:
        pass
    else:
        raise AssertionError("n = 0 was accepted")


def test_random_union_and_merge_bound() -> None:
    rng = random.Random(20261117)
    for _ in range(150):
        n = rng.randint(1, 9)
        stream = random_postings(rng, rng.randint(0, 40), rng.randint(1, 12))
        idx = LogarithmicIndex(n)
        inserted = []
        for x in stream:
            idx.add(x)
            inserted.append(x)
            idx.check_invariant()
            assert idx.all_postings() == sorted(inserted)
            T = len(inserted)
            bound = floor_log2(T // n) if T >= n else 0
            assert max(idx.merge_count.values()) <= bound
        want = direct(inserted)
        for t in set(want) | {"absent"}:
            assert idx.postings(t) == want.get(t, [])
        k = len(inserted) // n
        assert idx.merged == n * sum(2 ** (trailing_zeros(t) + 1) - 2 for t in range(1, k + 1))
