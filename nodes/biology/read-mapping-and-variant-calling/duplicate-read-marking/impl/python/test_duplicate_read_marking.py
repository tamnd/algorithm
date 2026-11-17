# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/duplicate-read-marking/. The authors are listed in prov/398WVT.jsonl.

import os
import random

import pytest

from duplicate_read_marking import Read, mark_duplicates, read_score, unclipped_five_prime


def rd(pos, cigar, reverse, quals, chrom="chr1", library="L1"):
    return Read(library, chrom, pos, cigar, reverse, tuple(quals))


def brute_force(templates):
    """Compare every template with every other one, straight from the definition."""
    def ends(t):
        return sorted((r.library, r.chrom, unclipped_five_prime(r), r.reverse) for r in t)

    def rank(i):
        return (sum(read_score(r) for r in templates[i]), -i)

    dups = set()
    for i, t in enumerate(templates):
        for j, u in enumerate(templates):
            if i == j:
                continue
            if len(t) == 2 and len(u) == 2 and ends(t) == ends(u) and rank(j) > rank(i):
                dups.add(i)
            if len(t) == 1 and len(u) == 2 and ends(t)[0] in ends(u):
                dups.add(i)
            if len(t) == 1 and len(u) == 1 and ends(t) == ends(u) and rank(j) > rank(i):
                dups.add(i)
    return dups


def test_unclipped_five_prime():
    # Forward read: the 5' end is the leftmost base, moved left by the leading clip.
    assert unclipped_five_prime(rd(100, "10M", False, [30] * 10)) == 100
    assert unclipped_five_prime(rd(100, "3S7M", False, [30] * 10)) == 97
    assert unclipped_five_prime(rd(100, "2H3S7M", False, [30] * 10)) == 95
    # Reverse read: the 5' end is the rightmost base, moved right by the trailing clip.
    assert unclipped_five_prime(rd(100, "10M", True, [30] * 10)) == 109
    assert unclipped_five_prime(rd(100, "4M2D4M2S", True, [30] * 10)) == 111
    assert unclipped_five_prime(rd(100, "4M2I4M", True, [30] * 10)) == 107
    assert unclipped_five_prime(rd(16, "6M14N5M", True, [30] * 11)) == 40


def test_page_example():
    q = [30] * 10
    a = (rd(100, "10M", False, q), rd(290, "10M", True, q))
    b = (rd(102, "2S8M", False, [30] * 9 + [10]), rd(290, "10M", True, q))  # same ends, lower score
    c = (rd(100, "10M", False, q), rd(291, "10M", True, q))  # mate end differs: not a duplicate
    d = (rd(100, "10M", False, q),)  # fragment on a pair end
    e = (rd(500, "10M", False, [20] * 10),)
    f = (rd(500, "10M", False, [40] * 10),)
    g = (rd(500, "10M", True, [40] * 10),)  # other strand
    h = (rd(100, "10M", False, q, library="L2"),)  # other library
    ts = [a, b, c, d, e, f, g, h]
    assert mark_duplicates(ts) == {1, 3, 4}


def test_scores_follow_picard():
    assert read_score(rd(1, "4M", False, [40, 14, 15, 2])) == 55
    assert read_score(rd(1, "500M", False, [40] * 500)) == 16383
    # Equal scores: the first template in the input is kept.
    t = (rd(7, "5M", False, [30] * 5),)
    assert mark_duplicates([t, t, t]) == {1, 2}


def test_mate_order_does_not_matter():
    q = [30] * 10
    x = (rd(100, "10M", False, q), rd(290, "10M", True, q))
    y = (rd(290, "10M", True, [20] * 10), rd(100, "10M", False, q))
    assert mark_duplicates([x, y]) == {1}


def test_against_brute_force():
    rng = random.Random(5)
    cigars = ["10M", "2S8M", "8M2S", "1S8M1S", "4M1D6M", "4M1I5M", "3H10M"]
    for _ in range(300):
        ts = []
        for _ in range(rng.randint(0, 14)):
            def one():
                return rd(rng.randint(100, 104), rng.choice(cigars), rng.random() < 0.5,
                          [rng.choice((2, 10, 14, 15, 30, 40)) for _ in range(10)],
                          chrom=rng.choice(("chr1", "chr1", "chr2")), library=rng.choice(("L1", "L1", "L2")))
            ts.append((one(), one()) if rng.random() < 0.6 else (one(),))
        assert mark_duplicates(ts) == brute_force(ts)


def test_errors():
    with pytest.raises(ValueError):
        mark_duplicates([()])
    with pytest.raises(ValueError):
        unclipped_five_prime(rd(1, "10Q", False, [30]))


if __name__ == "__main__":
    raise SystemExit(pytest.main([os.path.abspath(__file__), "-q"]))
