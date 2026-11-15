# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cori-resource-selection/. The authors are listed in prov/47WHK1.jsonl.

import math
import random

import pytest

import irtoy
from cori_resource_selection import Description, cori_scores, cori_select

# The split of the page: three collections of the irtoy documents.
GROUPS = [[1, 2, 8], [3, 4, 5], [6, 7]]


def toy() -> list[Description]:
    return [Description([irtoy.tokenize(irtoy.DOCS[d]) for d in g]) for g in GROUPS]


def direct(query: list[str], groups: list[list[list[str]]]) -> list[float]:
    """CORI written out term by term from the raw documents, with the formula of Callan (2000)."""
    k = len(groups)
    cw = [sum(len(doc) for doc in g) for g in groups]
    avg = sum(cw) / k
    out = []
    for i, g in enumerate(groups):
        total = 0.0
        for t in query:
            df = sum(1 for doc in g if t in doc)
            c = sum(1 for h in groups if any(t in doc for doc in h))
            if c == 0:
                total += 0.4
                continue
            big_t = df / (df + 50 + 150 * cw[i] / avg)
            big_i = math.log10((k + 0.5) / c) / math.log10(k + 1.0)
            total += 0.4 + 0.6 * big_t * big_i
        out.append(total / len(query))
    return out


def test_toy_example() -> None:
    d = toy()
    assert [x.cw for x in d] == [29, 30, 20]
    q1 = irtoy.tokenize(irtoy.QUERIES["q1"])
    s = cori_scores(q1, d)
    assert [round(x, 6) for x in s] == [0.403969, 0.400364, 0.40049]
    assert cori_select(q1, d, 3) == [0, 2, 1]
    assert round(cori_scores(["array"], d)[0], 6) == 0.407455
    q2 = irtoy.tokenize(irtoy.QUERIES["q2"])
    assert cori_select(q2, d, 1) == [1]
    q3 = irtoy.tokenize(irtoy.QUERIES["q3"])
    assert cori_select(q3, d, 1) == [2]


def test_term_in_no_collection_gives_default_belief_and_ties() -> None:
    d = toy()
    q4 = irtoy.tokenize(irtoy.QUERIES["q4"])
    assert cori_scores(q4, d) == [0.4, 0.4, 0.4]
    assert cori_select(q4, d, 2) == [0, 1]


def test_matches_direct_formula() -> None:
    rng = random.Random(8)
    words = ["w%d" % j for j in range(12)]
    for _ in range(200):
        k = rng.randrange(1, 6)
        groups = [[[rng.choice(words) for _ in range(rng.randrange(1, 9))] for _ in range(rng.randrange(1, 7))] for _ in range(k)]
        query = [rng.choice(words + ["zz"]) for _ in range(rng.randrange(1, 5))]
        got = cori_scores(query, [Description(g) for g in groups])
        want = direct(query, groups)
        assert all(abs(x - y) < 1e-12 for x, y in zip(got, want))


def test_bounds_and_monotonicity() -> None:
    rng = random.Random(10)
    for _ in range(200):
        k = rng.randrange(1, 6)
        groups = [[["a"] * rng.randrange(0, 3) + ["b"] * rng.randrange(1, 4) for _ in range(rng.randrange(1, 6))] for _ in range(k)]
        d = [Description(g) for g in groups]
        for x in cori_scores(["a", "b"], d):
            assert 0.4 <= x < 1.0
    # More documents with the term, same size: higher belief.
    small = Description([["a", "x"], ["x", "x"]])
    more = Description([["a", "x"], ["a", "x"]])
    other = Description([["y", "y"], ["y", "y"]])
    s = cori_scores(["a"], [small, more, other])
    assert s[1] > s[0] > s[2] == 0.4
    # Same df, larger collection: lower belief.
    short = Description([["a"], ["z"]])
    long = Description([["a", "z", "z", "z"], ["z", "z", "z", "z"]])
    s = cori_scores(["a"], [short, long])
    assert s[0] > s[1]


def test_repeated_query_terms_count() -> None:
    d = toy()
    s1 = cori_scores(["array"], d)
    s2 = cori_scores(["array", "array", "rank"], d)
    s3 = cori_scores(["rank"], d)
    assert all(abs(x - (2 * a + c) / 3) < 1e-15 for x, a, c in zip(s2, s1, s3))


def test_errors() -> None:
    with pytest.raises(ValueError):
        cori_scores([], toy())
    with pytest.raises(ValueError):
        cori_scores(["a"], [Description([]), Description([[]])])
    assert cori_scores(["a"], []) == []
