# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byte-pair-encoding/. The authors are listed in prov/8H71X7.jsonl.

import random

from byte_pair_encoding import (
    END,
    compress,
    compress_block,
    decompress,
    expand_block,
    learn_merges,
    segment,
)


def test_worked_example_compressor() -> None:
    table, packed = compress_block(b"aaabdaaabac", threshold=2)
    a, b = ord("a"), ord("b")
    assert table == [(0, a, a), (1, 0, a), (2, 1, b)]
    assert bytes(packed) == b"\x02d\x02ac"
    assert expand_block(table, packed) == b"aaabdaaabac"
    table, packed = compress_block(b"ABABCABCD", threshold=2)
    assert table == [(0, ord("A"), ord("B")), (1, 0, ord("C"))]
    assert bytes(packed) == b"\x00\x01\x01D"
    table, packed = compress_block(b"abcabcabcabc", threshold=2)
    assert table == [(0, a, b), (1, 0, ord("c")), (2, 1, 1)]
    assert bytes(packed) == b"\x02\x02"


def test_edges_compressor() -> None:
    for data in (b"", b"x", b"xx", b"xxx", b"xxxx", b"\x00" * 1000, bytes(range(256)), bytes(range(256)) * 3):
        assert decompress(compress(data)) == data
    # no unused byte value: nothing can be replaced
    table, packed = compress_block(bytes(range(256)) * 2, threshold=2)
    assert table == [] and bytes(packed) == bytes(range(256)) * 2
    # a run counts only non-overlapping pairs
    assert compress_block(b"zzz", threshold=2) == ([], list(b"zzz"))
    table, packed = compress_block(b"zzzz", threshold=2)
    assert table == [(0, 122, 122)] and packed == [0, 0]


def test_codes_are_unused_and_counts_reach_threshold() -> None:
    rng = random.Random(12)
    for _ in range(200):
        block = bytes(rng.choice(b"abcde") for _ in range(rng.randrange(0, 300)))
        table, packed = compress_block(block, threshold=3)
        assert all(code not in block for code, _, _ in table)
        assert len({code for code, _, _ in table}) == len(table)
        assert expand_block(table, packed) == block


def test_random_round_trip() -> None:
    rng = random.Random(8810)
    for _ in range(600):
        n = rng.randrange(0, 400)
        kind = rng.randrange(3)
        if kind == 0:
            data = bytes(rng.randrange(256) for _ in range(n))
        elif kind == 1:
            data = bytes(rng.choice(b"ab") for _ in range(n))
        else:
            unit = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 9)))
            data = (unit * (n // len(unit) + 1))[:n]
        size = rng.choice([1, 7, 64, 4096])
        assert decompress(compress(data, size, rng.choice([2, 3, 4]))) == data


def test_fibonacci_word() -> None:
    a, b = b"a", b"ab"
    while len(b) < 3000:
        a, b = b, b + a
    blob = compress(b)
    assert decompress(blob) == b
    assert len(blob) < len(b)


TOY = {"low": 5, "lower": 2, "newest": 6, "widest": 3}


def test_worked_example_tokenizer() -> None:
    merges = learn_merges(TOY, 10)
    assert merges == [
        ("e", "s"), ("es", "t"), ("est", END), ("l", "o"), ("lo", "w"),
        ("e", "w"), ("ew", "est" + END), ("n", "ewest" + END), ("low", END), ("d", "est" + END),
    ]
    assert segment("low", merges) == ["low" + END]
    assert segment("lower", merges) == ["low", "e", "r", END]
    assert segment("widest", merges) == ["w", "i", "dest" + END]
    assert segment("lowest", merges) == ["low", "est" + END]
    assert segment("newer", merges) == ["n", "ew", "e", "r", END]


def test_tokenizer_edges() -> None:
    assert learn_merges({}, 5) == []
    assert learn_merges({"a": 3}, 5) == [("a", END)]
    assert segment("", []) == [END]
    assert segment("abc", []) == ["a", "b", "c", END]


def test_segment_reproduces_training() -> None:
    rng = random.Random(3)
    for _ in range(500):
        counts = {}
        for _ in range(rng.randrange(1, 6)):
            word = "".join(rng.choice("abc") for _ in range(rng.randrange(1, 8)))
            counts[word] = counts.get(word, 0) + rng.randrange(1, 5)
        k = rng.randrange(0, 12)
        merges = learn_merges(counts, k)
        for w in counts:
            syms = list(w) + [END]
            for pair in merges:
                syms = segment_step(syms, pair)
            assert segment(w, merges) == syms
            assert "".join(syms) == w + END
        # the learned merges are the ones a full recount picks at each step
        for t, pair in enumerate(merges):
            stats = {}
            for w in counts:
                syms = list(w) + [END]
                for p in merges[:t]:
                    syms = segment_step(syms, p)
                for x, y in zip(syms, syms[1:]):
                    stats[(x, y)] = stats.get((x, y), 0) + counts[w]
            top = max(stats.values())
            assert pair == min(p for p in stats if stats[p] == top)


def segment_step(syms, pair):
    out, i = [], 0
    while i < len(syms):
        if i + 1 < len(syms) and (syms[i], syms[i + 1]) == pair:
            out.append(syms[i] + syms[i + 1])
            i += 2
        else:
            out.append(syms[i])
            i += 1
    return out
