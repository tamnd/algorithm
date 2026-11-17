# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variant-normalization/. The authors are listed in prov/YT7FC7.jsonl.

import os
import random

import pytest

from variant_normalization import all_representations, apply, normalize

REF = "GTCACACAGT"


def lcp(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k


def closed_form(ref, hap):
    """The normalized (pos, REF, ALT) from the proof: it depends only on ref and hap."""
    s = lcp(ref[::-1], hap[::-1])
    assert s < min(len(ref), len(hap))
    a = min(lcp(ref, hap), min(len(ref), len(hap)) - s - 1)
    return a + 1, ref[a:len(ref) - s], hap[a:len(hap) - s]


def test_page_example():
    hap = "GTCACAGT"
    reps = all_representations(REF, hap)
    assert (2, "TCA", "T") in reps and (3, "CAC", "C") in reps and (6, "ACA", "A") in reps
    for pos, r, a in reps:
        assert normalize(REF, pos, (r, a)) == (2, ("TCA", "T"))
    assert normalize(REF, 3, ("CACA", "CA", "CACACA")) == (2, ("TCA", "T", "TCACA"))


def test_snv_and_mnv_are_trimmed():
    assert normalize(REF, 3, ("CAC", "CGC")) == (4, ("A", "G"))
    assert normalize(REF, 1, ("GTCA", "GACA")) == (2, ("T", "A"))
    assert normalize(REF, 3, ("CACA", "TACG")) == (3, ("CACA", "TACG"))


def test_all_equivalent_placements_give_one_form():
    rng = random.Random(11)
    for _ in range(300):
        body = "".join(rng.choice("AC") for _ in range(rng.randint(3, 12)))
        ref = "G" + body
        i = rng.randint(1, len(ref) - 1)
        if rng.random() < 0.5:
            j = rng.randint(i + 1, min(len(ref), i + 3))
            hap = ref[:i] + ref[j:]
        else:
            ins = "".join(rng.choice("AC") for _ in range(rng.randint(1, 3)))
            hap = ref[:i] + ins + ref[i:]
        if hap == ref:
            continue
        reps = all_representations(ref, hap)
        expect = closed_form(ref, hap)
        assert expect in reps
        best = min(reps, key=lambda t: (len(t[1]), t[0]))
        assert best == expect
        for pos, r, a in reps:
            got = normalize(ref, pos, (r, a))
            assert got == (expect[0], (expect[1], expect[2]))
            assert apply(ref, got[0], got[1][0], got[1][1]) == hap


def test_errors():
    with pytest.raises(ValueError):
        normalize(REF, 3, ("CA", "CA"))
    with pytest.raises(ValueError):
        normalize(REF, 3, ("GG", "G"))
    with pytest.raises(ValueError):
        normalize("AAAC", 2, ("AA", "A"))


if __name__ == "__main__":
    raise SystemExit(pytest.main([os.path.abspath(__file__), "-q"]))
