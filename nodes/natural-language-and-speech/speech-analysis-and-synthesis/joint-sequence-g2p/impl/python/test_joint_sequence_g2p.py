# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-sequence-g2p/. The authors are listed in prov/Z0KB29.jsonl.

import math
import random
from fractions import Fraction
from math import comb

import pytest

from joint_sequence_g2p import (
    EOS,
    decode,
    expected_counts,
    forward,
    inventory,
    joint_log_prob,
    next_history,
    start_history,
    train_em,
    uniform_model,
)
from nlslog import NEG_INF, log_sum


def segmentations(g, phi, lmax, pmax):
    """Every joint segmentation of (g, phi), by plain recursion."""
    if not g:
        return [[]] if not phi else []
    out = []
    for a in range(1, min(lmax, len(g)) + 1):
        for b in range(0, min(pmax, len(phi)) + 1):
            q = (tuple(g[:a]), tuple(phi[:b]))
            for rest in segmentations(g[a:], phi[b:], lmax, pmax):
                out.append([q] + rest)
    return out


def seq_score(model, seq, order):
    h = start_history(order)
    s = 0.0
    for q in list(seq) + [EOS]:
        w = model.get(h, {}).get(q, NEG_INF)
        if w == NEG_INF:
            return NEG_INF
        s += w
        h = next_history(h, q, order)
    return s


def random_model(lexicon, order, lmax, pmax, rng):
    m = uniform_model(lexicon, order, lmax, pmax)
    out = {}
    for h, row in m.items():
        ws = {q: rng.uniform(0.05, 1.0) for q in row}
        s = sum(ws.values())
        out[h] = {q: math.log(w / s) for q, w in ws.items()}
    return out


def random_word(rng, n, alphabet):
    return tuple(rng.choice(alphabet) for _ in range(n))


def test_segmentation_count_one_letter_per_graphone():
    # lmax = 1, pmax = 1: each letter takes 0 or 1 phoneme, so C(n, m) segmentations.
    for n in range(0, 7):
        for m in range(0, n + 2):
            got = len(segmentations("x" * n, "y" * m, 1, 1))
            assert got == (comb(n, m) if m <= n else 0)


def test_six_has_six_segmentations():
    segs = segmentations("six", ("S", "IH", "K", "S"), 1, 2)
    assert len(segs) == 6


@pytest.mark.parametrize("order", [1, 2, 3])
def test_forward_equals_sum_over_segmentations(order):
    rng = random.Random(11 + order)
    for _ in range(6):
        lex = [
            (random_word(rng, rng.randint(1, 4), "ab"), random_word(rng, rng.randint(0, 4), "xy"))
            for _ in range(3)
        ]
        lmax, pmax = rng.randint(1, 2), rng.randint(1, 2)
        lex = [p for p in lex if segmentations(p[0], p[1], lmax, pmax)]
        if not lex:
            continue
        model = random_model(lex, order, lmax, pmax, rng)
        for g, phi in lex:
            brute = log_sum(seq_score(model, s, order) for s in segmentations(g, phi, lmax, pmax))
            assert joint_log_prob(model, g, phi, order, lmax, pmax) == pytest.approx(brute, abs=1e-9)


@pytest.mark.parametrize("order", [1, 2])
def test_expected_counts_equal_brute_force(order):
    rng = random.Random(23 + order)
    for _ in range(5):
        lex = [
            (random_word(rng, rng.randint(1, 4), "ab"), random_word(rng, rng.randint(1, 4), "xy"))
            for _ in range(3)
        ]
        lmax, pmax = 2, 2
        lex = [p for p in lex if segmentations(p[0], p[1], lmax, pmax)]
        model = random_model(lex, order, lmax, pmax, rng)
        brute = {}
        for g, phi in lex:
            segs = segmentations(g, phi, lmax, pmax)
            scores = [seq_score(model, s, order) for s in segs]
            z = log_sum(scores)
            for s, sc in zip(segs, scores):
                post = math.exp(sc - z)
                h = start_history(order)
                for q in s + [EOS]:
                    brute[(h, q)] = brute.get((h, q), 0.0) + post
                    h = next_history(h, q, order)
        counts, _ = expected_counts(model, lex, order, lmax, pmax)
        got = {(h, q): c for h, row in counts.items() for q, c in row.items() if c > 0}
        assert set(got) == set(brute)
        for k in brute:
            assert got[k] == pytest.approx(brute[k], abs=1e-9)


def test_uniform_unigram_exact():
    # Under the uniform unigram model every segmentation of length K has
    # probability V^-(K + 1); check log Z against an exact Fraction sum.
    lex = [("six", ("S", "IH", "K", "S"))]
    model = uniform_model(lex, 1, 1, 2)
    v = len(inventory(lex, 1, 2)) + 1
    exact = sum(Fraction(1, v ** (len(s) + 1)) for s in segmentations(*lex[0], 1, 2))
    got = joint_log_prob(model, *lex[0], 1, 1, 2)
    assert got == pytest.approx(math.log(exact.numerator) - math.log(exact.denominator), abs=1e-12)


@pytest.mark.parametrize("order", [1, 2])
def test_em_likelihood_never_decreases(order):
    rng = random.Random(5 + order)
    lex = [
        (random_word(rng, rng.randint(2, 5), "abc"), random_word(rng, rng.randint(2, 5), "xyz"))
        for _ in range(6)
    ]
    lex = [p for p in lex if segmentations(p[0], p[1], 2, 2)]
    _, lls = train_em(lex, order=order, lmax=2, pmax=2, iterations=8)
    for a, b in zip(lls, lls[1:]):
        assert b >= a - 1e-9


@pytest.mark.parametrize("order", [1, 2])
def test_decode_equals_brute_force(order):
    rng = random.Random(41 + order)
    lex = [
        (random_word(rng, rng.randint(1, 3), "ab"), random_word(rng, rng.randint(1, 3), "xy"))
        for _ in range(4)
    ]
    lmax, pmax = 2, 2
    model = random_model(lex, order, lmax, pmax, rng)
    graphones = sorted({q for row in model.values() for q in row if q != EOS})

    def spell(g):
        if not g:
            return [[]]
        out = []
        for q in graphones:
            a = len(q[0])
            if tuple(g[:a]) == q[0]:
                out += [[q] + rest for rest in spell(g[a:])]
        return out

    for _ in range(6):
        g = random_word(rng, rng.randint(1, 4), "ab")
        cands = [(seq_score(model, s, order), s) for s in spell(g)]
        best = max(c[0] for c in cands)
        phonemes, seq, score = decode(model, g, order, lmax)
        assert score == pytest.approx(best, abs=1e-9)
        assert seq_score(model, seq, order) == pytest.approx(best, abs=1e-9)
        assert "".join("".join(q[0]) for q in seq) == "".join(g)
        assert phonemes == [p for q in seq for p in q[1]]


def test_no_spelling_raises():
    lex = [("ab", ("x",))]
    model = uniform_model(lex, 1, 1, 1)
    with pytest.raises(ValueError):
        decode(model, "c", 1, 1)


def test_long_pair_does_not_underflow():
    # 200 letters, 100 phonemes, one letter per graphone and at most one phoneme.
    # Both graphones have probability 1/100 and EOS has 1/2, so
    # Z = C(200, 100) * 100^-200 / 2, below the smallest positive float.
    n, m = 200, 100
    g, phi = ("a",) * n, ("x",) * m
    model = {(): {(("a",), ()): math.log(0.01), (("a",), ("x",)): math.log(0.01), EOS: math.log(0.5)}}
    want = math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1) + n * math.log(0.01) + math.log(0.5)
    assert want < math.log(5e-324)
    _, z = forward(model, g, phi, 1, 1, 1)
    assert z == pytest.approx(want, rel=1e-12)


def test_em_learns_a_consistent_mapping():
    lex = [
        ("six", ("S", "IH", "K", "S")),
        ("fix", ("F", "IH", "K", "S")),
        ("box", ("B", "AA", "K", "S")),
        ("fox", ("F", "AA", "K", "S")),
        ("sit", ("S", "IH", "T")),
        ("bit", ("B", "IH", "T")),
    ]
    model, lls = train_em(lex, order=1, lmax=1, pmax=2, iterations=30)
    assert decode(model, "sob", 1, 1)[0] == ["S", "AA", "B"]
    assert decode(model, "fit", 1, 1)[0] == ["F", "IH", "T"]
