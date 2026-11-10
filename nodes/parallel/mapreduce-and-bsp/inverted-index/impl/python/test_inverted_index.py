# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverted-index/. The authors are listed in prov/GZMPCF.jsonl.

import random

from inverted_index import (build_index_baseline, build_index_one_machine, build_index_vtk, decode_postings,
                            encode_postings, gamma_bits, gaps, vbyte, vbyte_decode)

DOCS = [(0, "the cat sat"), (1, "the dog"), (2, "the cat and the dog")]


def zipf_docs(rng, n_docs, max_len, vocab):
    names = [f"t{i}" for i in range(1, vocab + 1)]
    weights = [1 / i for i in range(1, vocab + 1)]
    return [(d, " ".join(rng.choices(names, weights=weights, k=rng.randrange(max_len + 1))))
            for d in range(n_docs)]


def test_page_example():
    want = {"the": [(0, [0]), (1, [0]), (2, [0, 3])], "cat": [(0, [1]), (2, [1])], "sat": [(0, [2])],
            "dog": [(1, [1]), (2, [4])], "and": [(2, [2])]}
    assert build_index_one_machine(DOCS) == want
    base, sent_b, _ = build_index_baseline(DOCS, 2, 2)
    vtk, enc, sent_v, _ = build_index_vtk(DOCS, 2, 2)
    assert base == vtk == want
    assert sent_b == 10 and sent_v == 9
    # doc gap, term frequency, position gaps: (1, 1, 1), (1, 1, 1), (1, 2, 1, 3)
    assert list(enc["the"]) == [0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0x82, 0x81, 0x83]


def test_matches_one_machine_on_seeded_inputs():
    rng = random.Random(8)
    for _ in range(150):
        docs = zipf_docs(rng, rng.randrange(0, 15), 12, rng.choice([1, 4, 40]))
        m, r = rng.randrange(1, 5), rng.randrange(1, 5)
        want = build_index_one_machine(docs)
        base, sent_b, _ = build_index_baseline(docs, m, r, rng=rng)
        vtk, enc, sent_v, _ = build_index_vtk(docs, m, r, rng=rng)
        assert base == vtk == want
        assert sent_b == sum(len(t.split()) for _, t in docs)
        assert sent_v == sum(len(ps) for ps in want.values())
        assert all(decode_postings(enc[t]) == want[t] for t in want)


def test_empty_and_one_term():
    assert build_index_vtk([], 2, 3)[0] == {}
    docs = [(d, "x x") for d in range(30)]
    vtk, enc, sent, largest = build_index_vtk(docs, 3, 4)
    assert vtk == {"x": [(d, [0, 1]) for d in range(30)]}
    assert sent == largest == 30
    assert len(enc["x"]) == 30 * 4


def test_codes():
    assert vbyte(1) == b"\x81" and vbyte(127) == b"\xff" and vbyte(128) == b"\x01\x80"
    assert vbyte(824) == bytes([0x06, 0xB8])
    nums = [1, 5, 127, 128, 16383, 16384, 10**6]
    assert vbyte_decode(b"".join(vbyte(n) for n in nums)) == nums
    assert [gamma_bits(n) for n in (1, 2, 3, 4, 13)] == [1, 3, 3, 5, 7]
    assert gaps([0, 3, 4, 10]) == [1, 3, 1, 6]
    p = [(5, [1, 9]), (130, [0])]
    assert decode_postings(encode_postings(p)) == p
