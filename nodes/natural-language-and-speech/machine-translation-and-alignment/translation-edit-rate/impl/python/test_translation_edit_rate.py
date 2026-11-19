# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/translation-edit-rate/. The authors are listed in prov/EWE8J4.jsonl.

import random
from collections import deque
from functools import lru_cache

from translation_edit_rate import (
    corpus_ter,
    edit_distance_errors,
    sentence_ter,
    shift,
    ter_edits,
)


def levenshtein(a, b):
    """Word edit distance by plain recursion with a cache."""
    a, b = tuple(a), tuple(b)

    @lru_cache(maxsize=None)
    def go(i, j):
        if i == 0 or j == 0:
            return i + j
        return min(go(i - 1, j - 1) + (a[i - 1] != b[j - 1]), go(i - 1, j) + 1, go(i, j - 1) + 1)

    return go(len(a), len(b))


def exact_with_shifts(h, r):
    """The fewest edits: any number of shifts of any block, then the edit distance."""
    start = tuple(h)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        x = queue.popleft()
        for i in range(len(x)):
            for k in range(1, len(x) - i + 1):
                for p in range(len(x) - k + 1):
                    if p != i:
                        y = tuple(shift(x, i, k, p))
                        if y not in dist:
                            dist[y] = dist[x] + 1
                            queue.append(y)
    return min(s + levenshtein(y, r) for y, s in dist.items())


def test_paper_example():
    ref = "saudi arabia denied this week information published in the american new york times".split()
    hyp = "this week the saudis denied information published in the new york times".split()
    edits, shifts, final = ter_edits(hyp, ref)
    assert (edits, shifts) == (4, 1)
    assert final[:5] == ["the", "saudis", "denied", "this", "week"]
    assert sentence_ter(hyp, [ref]) == 4 / 13
    assert levenshtein(hyp, ref) == 6


def test_shift_example():
    edits, shifts, final = ter_edits("a d e b c f".split(), "a b c d e f c".split())
    assert final == "a b c d e f".split()
    assert (edits, shifts) == (2, 1)


def test_greedy_is_not_optimal():
    h, r = "a a b b".split(), "b c c a".split()
    edits, shifts, _ = ter_edits(h, r)
    assert (edits, shifts) == (4, 2)
    assert exact_with_shifts(h, r) == 3


def test_edit_distance_and_flags():
    rng = random.Random(99)
    for _ in range(300):
        h = [rng.choice("abcd") for _ in range(rng.randint(0, 7))]
        r = [rng.choice("abcd") for _ in range(rng.randint(0, 7))]
        d, herr, rerr = edit_distance_errors(h, r)
        assert d == levenshtein(h, r)
        # the matched words, in order, are equal on both sides
        hm = [w for w, e in zip(h, herr) if not e]
        rm = [w for w, e in zip(r, rerr) if not e]
        assert hm == rm
        # an optimal alignment with c matches costs max(n, m) - c at least
        assert d >= max(len(h), len(r)) - len(hm)


def test_bounds_against_brute_force():
    rng = random.Random(2006)
    for _ in range(120):
        h = [rng.choice("abc") for _ in range(rng.randint(1, 4))]
        r = [rng.choice("abc") for _ in range(rng.randint(1, 5))]
        edits, shifts, final = ter_edits(h, r)
        assert exact_with_shifts(h, r) <= edits <= levenshtein(h, r)
        assert sorted(final) == sorted(h)
        assert edits == shifts + levenshtein(final, r)


def test_no_shift_cases():
    assert ter_edits("a b c".split(), "a b c".split())[:2] == (0, 0)
    assert ter_edits("x y".split(), "a b c".split())[:2] == (3, 0)
    assert sentence_ter([], [[]]) == 0.0
    assert sentence_ter(["a"], [[]]) == 1.0
    assert sentence_ter([], [["a", "b"]]) == 1.0
    assert sentence_ter("a b c d".split(), [["a"]]) == 3.0


def test_several_references_and_corpus():
    h = "the cat sat".split()
    refs = ["a cat sat down".split(), "the cat sat".split()]
    # the edits are the fewest over the references, the length is the mean length
    assert sentence_ter(h, refs) == 0 / 3.5
    refs2 = ["a cat sat down".split(), "the dog sat".split()]
    assert sentence_ter(h, refs2) == 1 / 3.5
    hyps = ["a b".split(), "c d e f".split()]
    rs = [["a c".split()], ["c d e f".split()]]
    assert corpus_ter(hyps, rs) == 1 / 6
