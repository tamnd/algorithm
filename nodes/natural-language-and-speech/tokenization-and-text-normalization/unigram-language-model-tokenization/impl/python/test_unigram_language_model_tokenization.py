# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unigram-language-model-tokenization/. The authors are listed in prov/9PE3NB.jsonl.

import math
import random
from fractions import Fraction

from nlslog import NEG_INF
from unigram_language_model_tokenization import (
    backward,
    corpus_log_likelihood,
    em_step,
    expected_counts,
    forward,
    log_prob,
    piece_loss,
    remove_piece,
    seed_vocabulary,
    segmentations,
    train,
    viterbi,
)

PAGE = {"h": Fraction(1, 10), "u": Fraction(1, 10), "g": Fraction(1, 10), "s": Fraction(15, 100),
        "hu": Fraction(1, 10), "ug": Fraction(15, 100), "hug": Fraction(2, 10), "gs": Fraction(5, 100),
        "ugs": Fraction(5, 100)}
CORPUS = {"hug": 10, "pug": 5, "pun": 12, "bun": 4, "hugs": 5}


def as_model(probs):
    return {w: math.log(p) for w, p in probs.items()}


def exact(x, probs):
    """Brute force with Fractions: {segmentation: probability}."""
    out = {}
    for s in segmentations(x, probs):
        q = Fraction(1)
        for w in s:
            q *= probs[w]
        out[tuple(s)] = q
    return out


def random_probs(rng, alphabet, k):
    pieces = set(alphabet)
    while len(pieces) < len(alphabet) + k:
        pieces.add("".join(rng.choice(alphabet) for _ in range(rng.randint(2, 4))))
    weights = {w: Fraction(rng.randint(1, 20)) for w in sorted(pieces)}
    z = sum(weights.values())
    return {w: q / z for w, q in weights.items()}


def test_page_example():
    probs = exact("hugs", PAGE)
    assert len(probs) == 7
    assert sum(probs.values()) == Fraction(111, 2500)
    m = as_model(PAGE)
    assert abs(log_prob("hugs", m) - math.log(Fraction(111, 2500))) < 1e-12
    score, pieces = viterbi("hugs", m)
    assert pieces == ["hug", "s"] and abs(score - math.log(Fraction(3, 100))) < 1e-12
    alpha = [math.exp(a) for a in forward("hugs", m)]
    beta = [math.exp(b) for b in backward("hugs", m)]
    for got, want in zip(alpha, [1, 0.1, 0.11, 0.226, 0.0444]):
        assert abs(got - want) < 1e-12
    for got, want in zip(beta, [0.0444, 0.079, 0.065, 0.15, 1]):
        assert abs(got - want) < 1e-12
    assert abs(expected_counts("hugs", m)["hug"] - 75 / 111) < 1e-12


def test_viterbi_forward_and_counts_match_brute_force():
    rng = random.Random(1)
    for _ in range(60):
        probs = random_probs(rng, "abc", rng.randint(1, 8))
        m = as_model(probs)
        x = "".join(rng.choice("abc") for _ in range(rng.randint(1, 9)))
        table = exact(x, probs)
        total = sum(table.values())
        assert abs(log_prob(x, m) - math.log(total)) < 1e-9
        best = max(table.values())
        score, pieces = viterbi(x, m)
        assert abs(score - math.log(best)) < 1e-9 and table[tuple(pieces)] == best
        counts = expected_counts(x, m)
        for w in probs:
            want = sum(q * s.count(w) for s, q in table.items()) / total
            assert abs(counts.get(w, 0.0) - float(want)) < 1e-9


def test_no_segmentation():
    m = as_model({"a": Fraction(1, 2), "bc": Fraction(1, 2)})
    assert viterbi("ab", m) == (NEG_INF, None)
    assert log_prob("ab", m) == NEG_INF
    assert viterbi("", m) == (0.0, [])


def test_em_never_lowers_the_likelihood():
    rng = random.Random(2)
    for _ in range(5):
        corpus = {"".join(rng.choice("ab") for _ in range(rng.randint(1, 6))): rng.randint(1, 5) for _ in range(6)}
        m = as_model(random_probs(rng, "ab", 6))
        last = corpus_log_likelihood(corpus, m)
        for _ in range(8):
            m = em_step(corpus, m)
            now = corpus_log_likelihood(corpus, m)
            assert now >= last - 1e-9
            last = now
        assert abs(math.fsum(math.exp(lp) for lp in m.values()) - 1) < 1e-9


def test_page_em_trace():
    seed = seed_vocabulary(CORPUS, 100, 8)
    assert len(seed) == 19 and sum(len(w) == 1 for w in seed) == 7
    z = sum(seed.values())
    m = {w: math.log(f / z) for w, f in seed.items()}
    trace = [corpus_log_likelihood(CORPUS, m)]
    for _ in range(3):
        m = em_step(CORPUS, m)
        trace.append(corpus_log_likelihood(CORPUS, m))
    assert [round(v, 2) for v in trace] == [-110.31, -68.21, -55.62, -54.54]


def test_loss_is_the_drop_in_likelihood():
    m = as_model(PAGE)
    corpus = {"hugs": 1}
    rest = remove_piece(m, "hug")
    assert abs(math.fsum(math.exp(lp) for lp in rest.values()) - 1) < 1e-12
    q = Fraction(1) / (1 - PAGE["hug"])
    without = sum(exact("hugs", {w: p * q for w, p in PAGE.items() if w != "hug"}).values())
    want = math.log(Fraction(111, 2500)) - math.log(without)
    assert abs(piece_loss(corpus, m, "hug") - want) < 1e-12


def test_training_keeps_characters_and_reaches_the_target():
    m = train(CORPUS, 10)
    assert len(m) <= 10
    assert set("hugpnbs") <= set(m)
    assert abs(math.fsum(math.exp(lp) for lp in m.values()) - 1) < 1e-9
    assert viterbi("pugs", m)[1] == ["pug", "s"]
    assert viterbi("bugs", m)[1] == ["b", "u", "g", "s"]
    assert all(lp > NEG_INF for lp in m.values())
    assert set(m) == set("hugpnbs") | {"hug", "pun", "pug"}
    assert abs(expected_counts("hugs", as_model(PAGE))["s"] - 0.0339 / 0.0444) < 1e-12
    assert set(train(CORPUS, 12)) == set("hugpnbs") | set(CORPUS)


def test_log_space_avoids_underflow():
    # "a" * 3000 with p(a) = p(aa) = 1/2. P(x) satisfies Z(n) = (Z(n-1) + Z(n-2)) / 2.
    n = 3000
    probs = {"a": Fraction(1, 2), "aa": Fraction(1, 2)}
    z_prev, z = Fraction(1), Fraction(1, 2)
    for _ in range(n - 1):
        z_prev, z = z, (z + z_prev) / 2
    want = math.log(z.numerator) - math.log(z.denominator)
    plain = 1.0
    for _ in range(n):
        plain *= 0.5
    assert plain == 0.0  # the product of one segmentation underflows
    got = log_prob("a" * n, as_model(probs))
    assert got > NEG_INF and abs(got - want) < 1e-9 * abs(want)
    score, pieces = viterbi("a" * n, as_model(probs))
    assert pieces == ["aa"] * (n // 2) and abs(score - (n // 2) * math.log(0.5)) < 1e-9
