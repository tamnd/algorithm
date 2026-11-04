# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muthukrishnan-document-listing/. The authors are listed in prov/QK2HK3.jsonl.

import random

import pytest

from muthukrishnan_document_listing import DocumentListing


def test_example() -> None:
    x = DocumentListing(["banana", "ananas", "cabana"])
    assert x.sa_range("an") == (6, 11)
    assert x.d[6:11] == [2, 0, 0, 1, 1]
    assert x.c[6:11] == [5, 4, 7, 2, 9]
    x.rmq_calls = 0
    assert x.list_documents("an") == [1, 0, 2]
    assert x.rmq_calls == 5
    assert sorted(x.list_documents("ban")) == [0, 2]
    assert x.list_documents("s") == [1]
    assert x.list_documents("xyz") == []


def test_edges() -> None:
    x = DocumentListing(["", "a", "aaaa"])
    assert sorted(x.list_documents("a")) == [1, 2]
    assert x.list_documents("aa") == [2]
    assert DocumentListing([]).list_documents("a") == []
    with pytest.raises(ValueError):
        x.list_documents("")
    with pytest.raises(ValueError):
        DocumentListing(["a\x01b"])


def test_random_against_scan() -> None:
    rng = random.Random(2002)
    for _ in range(600):
        docs = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 8))) for _ in range(rng.randint(0, 6))]
        x = DocumentListing(docs)
        for _ in range(3):
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
            x.rmq_calls = 0
            got = x.list_documents(p)
            want = [k for k, d in enumerate(docs) if p in d]
            assert sorted(got) == want and len(got) == len(set(got))
            assert x.rmq_calls <= 2 * len(got) + 1
