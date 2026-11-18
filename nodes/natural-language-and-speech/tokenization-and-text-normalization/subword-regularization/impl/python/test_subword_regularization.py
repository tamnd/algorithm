# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subword-regularization/. The authors are listed in prov/510HA2.jsonl.

import math
import random
from fractions import Fraction

from nlslog import NEG_INF
from subword_regularization import exact_distribution, forward, nbest, sample_lattice, sample_nbest, segmentations

PAGE = {"h": Fraction(1, 10), "u": Fraction(1, 10), "g": Fraction(1, 10), "s": Fraction(15, 100),
        "hu": Fraction(1, 10), "ug": Fraction(15, 100), "hug": Fraction(2, 10), "gs": Fraction(5, 100),
        "ugs": Fraction(5, 100)}
MODEL = {w: math.log(p) for w, p in PAGE.items()}


def frequencies(draw, n):
    counts = {}
    for _ in range(n):
        s = draw()
        counts[s] = counts.get(s, 0) + 1
    return counts


def close(counts, exact, n):
    assert set(counts) <= set(exact)
    for s, q in exact.items():
        sd = math.sqrt(q * (1 - q) / n)
        assert abs(counts.get(s, 0) / n - q) <= 5 * sd + 1e-9


def test_exact_distribution_with_fractions():
    # With a = 1 the law is P(s) / P(x); check it against exact rational arithmetic.
    probs = {}
    for s in segmentations("hugs", MODEL):
        q = Fraction(1)
        for w in s:
            q *= PAGE[w]
        probs[s] = q
    total = sum(probs.values())
    assert total == Fraction(111, 2500)
    d = exact_distribution("hugs", MODEL, 1.0)
    for s, q in probs.items():
        assert abs(d[s] - float(q / total)) < 1e-12
    assert abs(d[("hug", "s")] - 75 / 111) < 1e-12


def test_page_values():
    d = exact_distribution("hugs", MODEL, 0.5)
    assert round(d[("hug", "s")], 4) == 0.3978 and round(d[("h", "u", "g", "s")], 4) == 0.0281
    d = exact_distribution("hugs", MODEL, 2.0)
    assert round(d[("hug", "s")], 4) == 0.9399
    assert {s: round(q, 4) for s, q in exact_distribution("hugs", MODEL, 1.0, 3).items()} == {
        ("hug", "s"): 0.75, ("h", "ugs"): 0.125, ("hu", "gs"): 0.125}


def test_lattice_sampling_matches_the_exact_law():
    rng = random.Random(0)
    n = 3000
    for a in [1.0, 0.5, 0.2]:
        counts = frequencies(lambda: sample_lattice("hugs", MODEL, a, rng), n)
        close(counts, exact_distribution("hugs", MODEL, a), n)


def test_nbest_sampling_matches_the_exact_law():
    rng = random.Random(1)
    n = 3000
    for a, l in [(1.0, 3), (0.5, 5)]:
        counts = frequencies(lambda: sample_nbest("hugs", MODEL, a, l, rng), n)
        close(counts, exact_distribution("hugs", MODEL, a, l), n)


def test_nbest_against_brute_force():
    rng = random.Random(2)
    for _ in range(40):
        pieces = set("ab") | {"".join(rng.choice("ab") for _ in range(rng.randint(2, 3))) for _ in range(4)}
        weights = {w: rng.randint(1, 50) for w in sorted(pieces)}
        z = sum(weights.values())
        model = {w: math.log(c / z) for w, c in weights.items()}
        x = "".join(rng.choice("ab") for _ in range(rng.randint(1, 8)))
        scores = sorted((sum(model[w] for w in s) for s in segmentations(x, model)), reverse=True)
        got = [score for score, _ in nbest(x, model, 4)]
        assert len(got) == min(4, len(scores))
        assert all(abs(g - s) < 1e-9 for g, s in zip(got, scores))


def test_random_models_sample_correctly():
    rng = random.Random(3)
    n = 2000
    for _ in range(3):
        pieces = set("ab") | {"".join(rng.choice("ab") for _ in range(2)) for _ in range(3)}
        weights = {w: rng.randint(1, 9) for w in sorted(pieces)}
        z = sum(weights.values())
        model = {w: math.log(c / z) for w, c in weights.items()}
        x = "".join(rng.choice("ab") for _ in range(5))
        a = rng.choice([0.3, 1.0, 1.5])
        counts = frequencies(lambda: sample_lattice(x, model, a, rng), n)
        close(counts, exact_distribution(x, model, a), n)


def test_log_space_avoids_underflow():
    # "a" * 4000 with p(a) = p(aa) = 1/2: the probability of any segmentation is
    # at most 2^-2000, which underflows to 0.0 as a plain product.
    n = 4000
    model = {"a": math.log(0.5), "aa": math.log(0.5)}
    plain = 1.0
    for _ in range(n // 2):
        plain *= 0.5
    assert plain == 0.0
    alpha = forward("a" * n, model, 1.0)
    assert alpha[n] > NEG_INF
    s = sample_lattice("a" * n, model, 1.0, random.Random(4))
    assert "".join(s) == "a" * n and set(s) <= {"a", "aa"}
