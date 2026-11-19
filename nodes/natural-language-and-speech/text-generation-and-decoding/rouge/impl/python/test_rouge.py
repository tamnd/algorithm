# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rouge/. The authors are listed in prov/MTNGKQ.jsonl.

import random
from fractions import Fraction as Fr
from itertools import combinations

from rouge import (
    jackknife,
    lcs_length,
    lcs_positions,
    ngrams,
    rouge_l,
    rouge_l_summary,
    rouge_multi,
    rouge_n,
    rouge_n_pooled,
    rouge_s,
    skip_bigrams,
    union_lcs,
)

REF = "the cat sat on the mat".split()
CAND = "the cat on the mat".split()


def test_check_values():
    assert rouge_n(CAND, REF, 1)[:2] == (Fr(5, 6), Fr(1))
    assert rouge_n(CAND, REF, 2)[:2] == (Fr(3, 5), Fr(3, 4))
    assert lcs_length(CAND, REF) == 5
    assert rouge_l(CAND, REF) == (Fr(5, 6), Fr(1), Fr(10, 11))
    assert rouge_n(CAND, REF, 1)[2] == Fr(10, 11)


def test_clipping():
    # "the the the" against a reference with two "the": two matches, not three.
    assert rouge_n("the the the".split(), "the cat the".split(), 1)[:2] == (Fr(2, 3), Fr(2, 3))


def test_lin_lcs_examples():
    s1 = "police killed the gunman".split()
    s2 = "police kill the gunman".split()
    s3 = "the gunman kill police".split()
    s4 = "the gunman police killed".split()
    assert rouge_l(s2, s1)[2] == Fr(3, 4)
    assert rouge_l(s3, s1)[2] == Fr(1, 2)
    assert rouge_l(s4, s1)[2] == Fr(1, 2)
    # Bigrams cannot tell S2 from S3 here, and skip-bigrams prefer S4 to S3.
    assert rouge_n(s2, s1, 2)[2] == Fr(1, 3)
    assert rouge_n(s3, s1, 2)[2] == Fr(1, 3)
    assert rouge_s(s2, s1)[2] == Fr(1, 2)
    assert rouge_s(s3, s1)[2] == Fr(1, 6)
    assert rouge_s(s4, s1)[2] == Fr(1, 3)


def test_union_lcs_example():
    r = ["w1", "w2", "w3", "w4", "w5"]
    c1 = ["w1", "w2", "w6", "w7", "w8"]
    c2 = ["w1", "w3", "w8", "w9", "w5"]
    assert lcs_positions(r, c1) == {0, 1}
    assert lcs_positions(r, c2) == {0, 2, 4}
    assert union_lcs(r, [c1, c2]) == 4
    rec, prec, _ = rouge_l_summary([c1, c2], [r])
    assert rec == Fr(4, 5) and prec == Fr(4, 10)


def brute_lcs(a, b):
    for k in range(min(len(a), len(b)), -1, -1):
        subs = {tuple(a[i] for i in idx) for idx in combinations(range(len(a)), k)}
        for idx in combinations(range(len(b)), k):
            if tuple(b[i] for i in idx) in subs:
                return k
    return 0


def brute_ngram_match(cand, ref, n):
    """Count matches by pairing equal n-gram occurrences one to one."""
    cg = [tuple(cand[i:i + n]) for i in range(len(cand) - n + 1)]
    rg = [tuple(ref[i:i + n]) for i in range(len(ref) - n + 1)]
    used, match = [False] * len(cg), 0
    for g in rg:
        for k, h in enumerate(cg):
            if not used[k] and h == g:
                used[k] = True
                match += 1
                break
    return match, len(rg), len(cg)


def test_random_against_brute_force():
    rng = random.Random(2004)
    vocab = list("abcd")
    for _ in range(400):
        a = [rng.choice(vocab) for _ in range(rng.randint(0, 7))]
        b = [rng.choice(vocab) for _ in range(rng.randint(0, 7))]
        k = lcs_length(a, b)
        assert k == brute_lcs(a, b)
        pos = lcs_positions(a, b)
        assert len(pos) == k
        sub = [a[i] for i in sorted(pos)]
        assert brute_lcs(sub, b) == k
        for n in (1, 2, 3):
            m, nr, nc = brute_ngram_match(b, a, n)
            rec, prec, _ = rouge_n(b, a, n)
            assert rec == (Fr(m, nr) if nr else 0)
            assert prec == (Fr(m, nc) if nc else 0)
        sb = skip_bigrams(a)
        assert sum(sb.values()) == len(a) * (len(a) - 1) // 2
        assert sum(skip_bigrams(a, 0).values()) == max(0, len(a) - 1)
        assert skip_bigrams(a, 0) == ngrams(a, 2)


def test_multiple_references():
    refs = [REF, "a cat sat on a mat".split(), "the dog sat".split()]
    one = lambda c, r: rouge_n(c, r, 1)[0]
    assert rouge_multi(CAND, refs, one) == Fr(5, 6)
    # Equation 1 pools the counts: (5 + 3 + 1) matches of (6 + 6 + 3) reference unigrams.
    assert rouge_n_pooled(CAND, refs, 1) == Fr(9, 15)
    # Jackknife: the best of each pair of references, averaged.
    want = (max(Fr(3, 6), Fr(1, 3)) + max(Fr(5, 6), Fr(1, 3)) + max(Fr(5, 6), Fr(3, 6))) / 3
    assert jackknife(CAND, refs, one) == want == Fr(13, 18)


def test_edge_cases():
    assert rouge_n([], REF, 1) == (0, 0, 0)
    assert rouge_n(["a"], ["a"], 2) == (0, 0, 0)
    assert rouge_l([], []) == (0, 0, 0)
    assert rouge_l(REF, REF) == (1, 1, 1)
    # A large beta weights recall: F tends to R.
    r, p, f = rouge_l(CAND, REF, beta=Fr(1000))
    assert abs(f - r) < Fr(1, 10 ** 5)
