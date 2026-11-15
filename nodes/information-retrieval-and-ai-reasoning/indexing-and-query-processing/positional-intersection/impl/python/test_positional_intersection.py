# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-intersection/. The authors are listed in prov/DS6M6D.jsonl.

import random

import irtoy
from positional_intersection import phrase_matches, positional_intersect

Lists = dict[str, list[tuple[int, list[int]]]]


def positional_lists(docs: dict[int, list[str]]) -> Lists:
    index: Lists = {}
    for d in sorted(docs):
        for i, t in enumerate(docs[d]):
            lst = index.setdefault(t, [])
            if not lst or lst[-1][0] != d:
                lst.append((d, []))
            lst[-1][1].append(i)
    return index


def toy() -> tuple[dict[int, list[str]], Lists]:
    docs = {d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()}
    return docs, positional_lists(docs)


def brute_pairs(docs: dict[int, list[str]], s: str, t: str, k: int) -> list[tuple[int, int, int]]:
    out = []
    for d in sorted(docs):
        toks = docs[d]
        for x, a in enumerate(toks):
            if a != s:
                continue
            for y, b in enumerate(toks):
                if b == t and abs(x - y) <= k:
                    out.append((d, x, y))
    return out


def brute_phrase(docs: dict[int, list[str]], phrase: list[str]) -> list[tuple[int, int]]:
    r = len(phrase)
    return [(d, x) for d in sorted(docs) for x in range(len(docs[d]) - r + 1) if docs[d][x:x + r] == phrase]


def check_pair(docs: dict[int, list[str]], ix: Lists, s: str, t: str, k: int) -> None:
    p1, p2 = ix.get(s, []), ix.get(t, [])
    stats: dict[str, int] = {}
    got = positional_intersect(p1, p2, k, stats)
    assert got == brute_pairs(docs, s, t, k)
    if p1 and p2:
        assert stats["doc_steps"] <= len(p1) + len(p2) - 1
    common = {d for d, _ in p1} & {d for d, _ in p2}
    work = sum(len(ps) for d, ps in p1 if d in common) + sum(len(ps) for d, ps in p2 if d in common)
    assert stats["pos_steps"] <= work


def check_phrase(docs: dict[int, list[str]], ix: Lists, phrase: list[str]) -> None:
    lists = [ix.get(t, []) for t in phrase]
    stats: dict[str, int] = {}
    got = phrase_matches(lists, stats)
    assert got == brute_phrase(docs, phrase)
    bound = sum(len(lst) for lst in lists)
    sets = [{d for d, _ in lst} for lst in lists]
    common = set.intersection(*sets)
    for lst in lists:
        bound += sum(len(ps) for d, ps in lst if d in common)
    bound += (len(lists) - 1) * sum(len(ps) for d, ps in lists[0] if d in common)
    assert stats["steps"] <= bound
    if len(phrase) == 2:
        pairs = positional_intersect(lists[0], lists[1], 1)
        assert [(d, x) for d, x, y in pairs if y == x + 1] == got


def test_example() -> None:
    docs, ix = toy()
    assert phrase_matches([ix["posting"], ix["list"]]) == [(3, 8), (4, 1)]
    assert phrase_matches([ix["sorted"], ix["array"]]) == [(1, 7), (2, 8), (8, 1)]
    assert phrase_matches([ix["sorted"], ix["list"]]) == [(4, 5)]
    assert phrase_matches([ix["list"], ix["sorted"]]) == []
    assert phrase_matches([ix["merge"], ix["sort"]]) == [(2, 0)]
    assert phrase_matches([ix["a"], ix["sorted"], ix["list"]]) == [(4, 4)]
    assert positional_intersect(ix["list"], ix["sorted"], 1) == [(4, 6, 5)]
    assert positional_intersect(ix["posting"], ix["list"], 2) == [(3, 8, 9), (4, 1, 2)]
    assert positional_intersect(ix["sorted"], ix["a"], 3) == [(1, 7, 6), (4, 5, 4)]
    stats: dict[str, int] = {}
    got = positional_intersect(ix["list"], ix["a"], 2, stats)
    assert got == [(3, 9, 7), (4, 2, 0), (4, 2, 4), (4, 6, 4)]
    assert stats == {"doc_steps": 3, "pos_steps": 3}


def test_irtoy_all_pairs() -> None:
    docs, ix = toy()
    terms = sorted(ix)
    for s in terms:
        for t in terms:
            check_pair(docs, ix, s, t, 2)
            check_phrase(docs, ix, [s, t])
    rng = random.Random(24)
    for _ in range(300):
        check_phrase(docs, ix, [rng.choice(terms) for _ in range(rng.randint(1, 4))])
    for d in docs:
        toks = docs[d]
        for x in range(len(toks)):
            for r in (1, 2, 3, 4):
                if x + r <= len(toks):
                    check_phrase(docs, ix, toks[x:x + r])


def test_edges() -> None:
    assert positional_intersect([], [(1, [0])], 2) == []
    assert positional_intersect([(1, [0])], [(1, [0])], 0) == [(1, 0, 0)]
    assert positional_intersect([(1, [0, 10])], [(1, [5])], 4) == []
    assert phrase_matches([[]]) == []
    assert phrase_matches([[(2, [0, 3])]]) == [(2, 0), (2, 3)]
    assert phrase_matches([[(1, [0])], []]) == []
    docs = {1: ["a", "a", "a"]}
    ix = positional_lists(docs)
    check_phrase(docs, ix, ["a", "a"])
    check_pair(docs, ix, "a", "a", 1)


def test_random_collections() -> None:
    rng = random.Random(242)
    for _ in range(150):
        vocab = [f"w{i}" for i in range(rng.randint(1, 5))]
        ids = sorted(rng.sample(range(500), rng.randint(0, 25)))
        docs = {d: [rng.choice(vocab) for _ in range(rng.randint(0, 30))] for d in ids}
        ix = positional_lists(docs)
        for _ in range(6):
            s, t = rng.choice(vocab), rng.choice(vocab)
            check_pair(docs, ix, s, t, rng.randint(0, 6))
            check_phrase(docs, ix, [rng.choice(vocab) for _ in range(rng.randint(1, 4))])
