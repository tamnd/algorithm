# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-matching-segmentation/. The authors are listed in prov/ZZTPQ8.jsonl.

import math
import random

import pytest

from maximum_matching_segmentation import (
    backward_max_match,
    bidirectional_max_match,
    build_trie,
    forward_max_match,
    longest_match_end,
    unigram_segment,
)
from nlslog import NEG_INF, log_add, log_sum

COUNTS = {
    "the": 30, "table": 3, "down": 4, "there": 5, "theta": 1, "bled": 1,
    "own": 2, "tab": 1, "led": 1, "a": 6, "here": 2,
}
TOTAL = sum(COUNTS.values())
PROB = {w: c / TOTAL for w, c in COUNTS.items()}
TEXT = "thetabledownthere"


def greedy_by_set(s, words):
    """Forward maximum matching with set lookups of every length, longest first."""
    words = set(words)
    m = max((len(w) for w in words), default=0)
    i, out = 0, []
    while i < len(s):
        j = i + 1
        for k in range(min(len(s), i + m), i, -1):
            if s[i:k] in words:
                j = k
                break
        out.append(s[i:j])
        i = j
    return out


def all_segmentations(s, words):
    """Every way to cut s into dictionary words, listed one by one."""
    if not s:
        return [[]]
    out = []
    for j in range(1, len(s) + 1):
        if s[:j] in words:
            out.extend([s[:j]] + rest for rest in all_segmentations(s[j:], words))
    return out


def test_page_example_forward_fails():
    trie = build_trie(COUNTS)
    assert forward_max_match(TEXT, trie) == ["theta", "bled", "own", "there"]
    assert [longest_match_end(TEXT, i, trie) for i in (0, 5, 9, 12)] == [5, 9, 12, 17]


def test_page_example_backward_and_bidirectional():
    assert backward_max_match(TEXT, COUNTS) == ["the", "table", "down", "there"]
    assert bidirectional_max_match(TEXT, COUNTS) == ["the", "table", "down", "there"]


def test_page_example_unigram_dp():
    seg, score = unigram_segment(TEXT, PROB)
    assert seg == ["the", "table", "down", "there"]
    assert score == pytest.approx(math.log(30 * 3 * 4 * 5) - 4 * math.log(56), abs=1e-12)
    assert score == pytest.approx(-8.605865, abs=1e-6)
    greedy = sum(math.log(PROB[w]) for w in ["theta", "bled", "own", "there"])
    assert greedy == pytest.approx(-13.798822, abs=1e-6)
    assert len(all_segmentations(TEXT, COUNTS)) == 3


def test_dead_end_and_fewest_words():
    words = ["ab", "abc", "cd"]
    assert forward_max_match("abcd", build_trie(words)) == ["abc", "d"]
    assert unigram_segment("abcd", {w: 1 / 3 for w in words})[0] == ["ab", "cd"]
    words = ["a", "ab", "bcd", "c", "d"]
    assert forward_max_match("abcd", build_trie(words)) == ["ab", "c", "d"]
    assert min(len(x) for x in all_segmentations("abcd", set(words))) == 2


def test_directions_differ():
    words = ["ab", "a", "bc", "d", "c"]
    assert forward_max_match("abcd", build_trie(words)) == ["ab", "c", "d"]
    assert backward_max_match("abcd", words) == ["a", "bc", "d"]


def test_edge_cases():
    assert forward_max_match("", build_trie(["a"])) == []
    assert forward_max_match("xyz", build_trie([])) == ["x", "y", "z"]
    assert backward_max_match("xyz", []) == ["x", "y", "z"]
    assert unigram_segment("", {"a": 1.0}) == ([], 0.0)
    assert unigram_segment("ab", {"a": 1.0}) is None
    with pytest.raises(ValueError):
        build_trie(["a", ""])


def test_no_underflow_in_log_space():
    s = "a" * 400
    seg, score = unigram_segment(s, {"a": 0.1, "aa": 0.001})
    assert 0.1 ** 400 == 0.0
    assert score == pytest.approx(400 * math.log(0.1), rel=1e-12)
    assert seg == ["a"] * 400


def test_random_against_oracles():
    rng = random.Random(20261118)
    for _ in range(500):
        alphabet = "abc"[: rng.randint(1, 3)]
        size = rng.randint(0, 8)
        words = sorted({"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4))) for _ in range(size)})
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 10)))
        fw = forward_max_match(s, build_trie(words))
        assert "".join(fw) == s
        assert fw == greedy_by_set(s, words)
        bw = backward_max_match(s, words)
        assert "".join(bw) == s
        rev = [w[::-1] for w in words]
        assert bw == [w[::-1] for w in reversed(greedy_by_set(s[::-1], rev))]
        assert bidirectional_max_match(s, words) in (fw, bw)
        if not words:
            continue
        weights = [rng.randint(1, 9) for _ in words]
        prob = {w: c / sum(weights) for w, c in zip(words, weights)}
        cands = all_segmentations(s, set(words))
        res = unigram_segment(s, prob)
        if not cands:
            assert res is None
            continue
        seg, score = res
        assert "".join(seg) == s and all(w in prob for w in seg)
        best = max(sum(math.log(prob[w]) for w in c) for c in cands)
        assert score == pytest.approx(best, abs=1e-9)
        assert sum(math.log(prob[w]) for w in seg) == pytest.approx(best, abs=1e-9)


def test_helper_copy_basics():
    assert log_add(math.log(0.5), math.log(0.25)) == pytest.approx(-0.287682, abs=1e-6)
    assert log_sum([]) == NEG_INF
