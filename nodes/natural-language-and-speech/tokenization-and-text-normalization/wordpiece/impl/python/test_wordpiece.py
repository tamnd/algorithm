# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wordpiece/. The authors are listed in prov/N8960R.jsonl.

import math
import random

import pytest

from wordpiece import (
    UNK,
    count_pair,
    encode,
    encode_word,
    initial_units,
    join_units,
    log_likelihood,
    merge_gain,
    merge_units,
    pair_counts,
    segment_with_merges,
    train_wordpiece,
    unit_counts,
)

FREQ = {"hug": 2, "pug": 2, "pun": 2, "bun": 10, "hugs": 10}


def recount_gain(seg, freq, a, b):
    """The gain by brute force: apply the merge and recount everything."""
    before = log_likelihood(unit_counts(seg, freq))
    after_seg = {w: merge_units(u, a, b) for w, u in seg.items()}
    return log_likelihood(unit_counts(after_seg, freq)) - before


def greedy_by_brute_force(word, vocab):
    """Greedy longest match first, written as a search over all piece lengths."""
    out, i = [], 0
    while i < len(word):
        cands = [j for j in range(i + 1, len(word) + 1) if (word[i:j] if i == 0 else "##" + word[i:j]) in vocab]
        if not cands:
            return [UNK]
        j = max(cands)
        out.append(word[i:j] if i == 0 else "##" + word[i:j])
        i = j
    return out


def test_initial_units_and_join():
    assert initial_units("hugs") == ["h", "##u", "##g", "##s"]
    assert join_units("h", "##u") == "hu"
    assert join_units("##u", "##g") == "##ug"
    with pytest.raises(ValueError):
        join_units("h", "u")
    with pytest.raises(ValueError):
        initial_units("")


def test_pair_count_does_not_overlap():
    units = ["a"] + ["##a"] * 5
    assert count_pair(units, "##a", "##a") == 2
    assert merge_units(units, "##a", "##a") == ["a", "##aa", "##aa", "##a"]
    assert count_pair(units, "a", "##a") == 1


def test_first_step_gains_of_the_page():
    seg = {w: initial_units(w) for w in FREQ}
    c, p = unit_counts(seg, FREQ), pair_counts(seg, FREQ)
    assert sum(c.values()) == 88
    assert p[("##u", "##g")] == 14 and p[("##g", "##s")] == 10
    assert log_likelihood(c) == pytest.approx(-161.1137, abs=1e-4)
    assert merge_gain(c, "##g", "##s", 10) == pytest.approx(22.7807, abs=1e-4)
    assert merge_gain(c, "##u", "##g", 14) == pytest.approx(20.6132, abs=1e-4)


def test_closed_form_gain_equals_recount():
    rng = random.Random(7)
    for _ in range(60):
        words = {"".join(rng.choice("aab") for _ in range(rng.randint(1, 6))) for _ in range(5)}
        freq = {w: rng.randint(1, 9) for w in words}
        seg = {w: initial_units(w) for w in freq}
        for _ in range(3):
            c, p = unit_counts(seg, freq), pair_counts(seg, freq)
            for (a, b), k in p.items():
                assert merge_gain(c, a, b, k) == pytest.approx(recount_gain(seg, freq, a, b), abs=1e-9)
            if not p:
                break
            a, b = min(p)
            seg = {w: merge_units(u, a, b) for w, u in seg.items()}


def test_training_picks_the_best_gain_each_step():
    vocab, merges = train_wordpiece(FREQ, 5)
    assert merges == [("##g", "##s"), ("##u", "##n"), ("h", "##u"), ("b", "##un"), ("hu", "##gs")]
    seg = {w: initial_units(w) for w in FREQ}
    for a, b in merges:
        p = pair_counts(seg, FREQ)
        gains = {pair: recount_gain(seg, FREQ, *pair) for pair in p}
        assert gains[(a, b)] == pytest.approx(max(gains.values()), abs=1e-9)
        seg = {w: merge_units(u, a, b) for w, u in seg.items()}
    assert {"hugs", "bun", "hu", "##un", "##gs"} <= vocab


def test_the_gain_differs_from_the_pair_count():
    seg = {w: initial_units(w) for w in FREQ}
    p = pair_counts(seg, FREQ)
    assert max(p, key=p.get) == ("##u", "##g")
    assert train_wordpiece(FREQ, 1)[1] == [("##g", "##s")]


def test_training_stops_when_no_pair_is_left():
    vocab, merges = train_wordpiece({"ab": 3}, 10)
    assert merges == [("a", "##b")]
    assert vocab == {"a", "##b", "ab"}


def test_encoder_examples():
    vocab, merges = train_wordpiece(FREQ, 5)
    assert encode_word("hugs", vocab) == ["hugs"]
    assert encode_word("hug", vocab) == ["hu", "##g"]
    assert encode_word("bugs", vocab) == ["b", "##u", "##gs"]
    assert encode_word("gun", vocab) == [UNK]
    assert encode_word("unaffable", {"un", "##aff", "##able", "##a"}) == ["un", "##aff", "##able"]
    assert encode(["hugs", "gun", "bun"], vocab) == ["hugs", UNK, "bun"]


def test_long_word_is_unknown():
    vocab = {"a", "##a"}
    assert encode_word("a" * 200, vocab) == ["a"] + ["##a"] * 199
    assert encode_word("a" * 201, vocab) == [UNK]
    assert encode_word("aaa", vocab, max_chars=2) == [UNK]


def test_encoder_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        vocab = {"".join(rng.choice("abc") for _ in range(rng.randint(1, 3))) for _ in range(5)}
        vocab |= {"##" + "".join(rng.choice("abc") for _ in range(rng.randint(1, 3))) for _ in range(6)}
        word = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        assert encode_word(word, vocab) == greedy_by_brute_force(word, vocab)


def test_greedy_is_not_the_merge_order():
    # The encoder and the merge replay can differ: greedy longest match is a different rule.
    vocab, merges = train_wordpiece(FREQ, 5)
    differ = 0
    rng = random.Random(3)
    for _ in range(200):
        w = "".join(rng.choice("hugsbpn") for _ in range(rng.randint(1, 6)))
        if UNK not in encode_word(w, vocab) and encode_word(w, vocab) != segment_with_merges(w, merges):
            differ += 1
    assert differ > 0


def test_pieces_concatenate_to_the_word():
    vocab, _ = train_wordpiece(FREQ, 5)
    rng = random.Random(5)
    for _ in range(200):
        w = "".join(rng.choice("hugsbpn") for _ in range(rng.randint(1, 7)))
        pieces = encode_word(w, vocab)
        if pieces != [UNK]:
            assert "".join(x[2:] if i else x for i, x in enumerate(pieces)) == w
            assert all(x in vocab for x in pieces)
