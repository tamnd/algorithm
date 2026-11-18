# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byte-level-bpe/. The authors are listed in prov/HZ50C6.jsonl.

import itertools
import random

from byte_level_bpe import (
    BYTE_CHAR,
    decode,
    encode,
    is_char,
    pair_counts,
    pretokenize,
    recover,
    replay,
    show,
    token_ids,
    train,
)

CORPUS = ["日本 日本 日日"]


def random_text(rng, n):
    pool = "ab c\n'!7é日本語😀 x"
    return "".join(rng.choice(pool) for _ in range(n))


def test_byte_map():
    assert len(BYTE_CHAR) == 256 and len(set(BYTE_CHAR.values())) == 256
    assert all(not ch.isspace() and ch.isprintable() for ch in BYTE_CHAR.values())
    assert show(b" world") == "Ġworld"
    assert BYTE_CHAR[ord("A")] == "A"


def test_pretokenizer_examples():
    assert pretokenize("Hello world") == ["Hello", " world"]
    assert pretokenize("I've  got 42 apples!\n") == ["I", "'ve", " ", " got", " 42", " apples", "!", "\n"]
    assert pretokenize("a\n\nb") == ["a", "\n", "\n", "b"]
    assert pretokenize("don't stop") == ["don", "'t", " stop"]
    assert pretokenize(" 日本語x²") == [" 日本語x", "²"]
    assert pretokenize("ab  ") == ["ab", "  "]


def test_pretokens_cover_the_text():
    rng = random.Random(1)
    for _ in range(300):
        t = random_text(rng, rng.randint(0, 20))
        assert "".join(pretokenize(t)) == t


def test_page_example():
    assert len(train(CORPUS, 100)) == 8
    merges = train(CORPUS, 5)
    assert merges == [
        (b"\x97", b"\xa5"),
        (b"\xe6", b"\x97\xa5"),
        (b" ", "日".encode()),
        (b"\x9c", b"\xac"),
        (b"\xe6", b"\x9c\xac"),
    ]
    toks = encode(" 日本語", merges)
    assert toks == [" 日".encode(), "本".encode(), b"\xe8", b"\xaa", b"\x9e"]
    assert token_ids(toks, merges) == [258, 260, 232, 170, 158]
    assert not is_char(b"\x97\xa5")
    seg = {x: [bytes([b]) for b in x.encode()] for x in ["日本", " 日本", " 日日"]}
    p = pair_counts(seg, {"日本": 1, " 日本": 1, " 日日": 1})
    assert p[(b"\x97", b"\xa5")] == 4 and p[(b"\xe6", b"\x97")] == 4 and p[(b"\xa5", b"\xe6")] == 3


def test_round_trip_and_no_unknown():
    rng = random.Random(2)
    corpus = [random_text(rng, 40) for _ in range(5)]
    merges = train(corpus, 30)
    for _ in range(300):
        t = random_text(rng, rng.randint(0, 25))
        toks = encode(t, merges)
        assert decode(toks) == t
        assert all(0 <= i < 256 + len(merges) for i in token_ids(toks, merges))


def test_rank_order_equals_replay():
    rng = random.Random(3)
    for _ in range(20):
        corpus = [random_text(rng, 30) for _ in range(4)]
        merges = train(corpus, 25)
        for _ in range(20):
            t = random_text(rng, rng.randint(0, 20))
            assert encode(t, merges) == replay(t, merges)


def test_rank_order_can_differ_on_a_hand_made_list():
    merges = [(b"x", b"ab"), (b"a", b"b")]
    assert replay("xab", merges) == [b"x", b"ab"]
    assert encode("xab", merges) == [b"xab"]


def test_training_takes_the_most_frequent_pair():
    rng = random.Random(4)
    corpus = [random_text(rng, 30) for _ in range(3)]
    merges = train(corpus, 10)
    for k in range(1, len(merges) + 1):
        seen = merges[: k - 1]
        freq = {}
        for t in corpus:
            for x in pretokenize(t):
                freq[x] = freq.get(x, 0) + 1
        seg = {x: replay(x, seen) for x in freq}
        p = pair_counts(seg, freq)
        assert p[merges[k - 1]] == max(p.values())


def brute_force_recover(data):
    best = (0, set())
    n = len(data)
    for cuts in itertools.product([0, 1], repeat=max(n - 1, 0)):
        chunks, start = [], 0
        for i, c in enumerate(cuts, start=1):
            if c:
                chunks.append(data[start:i])
                start = i
        chunks.append(data[start:])
        if n == 0 or any(len(ch) > 4 for ch in chunks):
            continue
        good = [ch for ch in chunks if is_char(ch)]
        text = "".join(ch.decode("utf-8") for ch in good)
        if len(good) > best[0]:
            best = (len(good), {text})
        elif len(good) == best[0]:
            best[1].add(text)
    return best


def test_recover_against_brute_force():
    rng = random.Random(5)
    pieces = [b"a", b"\xc3\xa9", "日".encode(), "😀".encode(), b"\x97", b"\xa5", b"\xe6", b"\xf0\x9f", b"\xff"]
    for _ in range(300):
        data = b"".join(rng.choice(pieces) for _ in range(rng.randint(1, 5)))[:11]
        count, text = recover(data)
        best_count, texts = brute_force_recover(data)
        assert count == best_count
        assert texts == {text} or (best_count == 0 and text == "")


def test_recover_example():
    data = b"\x97\xa5" + "日".encode()
    assert recover(data) == (1, "日")
    assert decode([b"\x97\xa5", "日".encode()]) == "��日"
    assert recover(b"\xe6\x97\xe6\x97\xa5a\xa5\xc3\xa9") == (3, "日aé")
    assert recover(b"") == (0, "")
