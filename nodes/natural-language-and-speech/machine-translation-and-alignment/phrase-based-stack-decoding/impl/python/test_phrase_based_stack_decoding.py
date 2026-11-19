# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phrase-based-stack-decoding/. The authors are listed in prov/7R5WTX.jsonl.

import itertools
import math
import random

from phrase_based_stack_decoding import (
    BigramLM,
    Model,
    decode,
    exhaustive,
    future_cost_table,
    score_derivation,
)


def example_model() -> Model:
    table = {
        ("morgen",): [(("tomorrow",), -0.2)],
        ("fliege",): [(("will", "fly"), -0.7), (("fly",), -0.9)],
        ("ich",): [(("I",), -0.1)],
        ("fliege", "ich"): [(("I", "will", "fly"), -1.5)],
    }
    lm = BigramLM(
        {
            ("<s>", "tomorrow"): -1.0,
            ("tomorrow", "I"): -1.2,
            ("I", "will"): -0.6,
            ("will", "fly"): -0.4,
            ("fly", "</s>"): -0.5,
            ("tomorrow", "will"): -2.5,
            ("fly", "I"): -3.0,
            ("I", "</s>"): -1.5,
            ("I", "fly"): -1.0,
            ("tomorrow", "fly"): -3.0,
        },
        floor=-6.0,
    )
    return Model(table, lm, lm_weight=1.0, distortion_weight=0.5)


def test_example() -> None:
    f = "morgen fliege ich".split()
    model = example_model()
    score, words, steps = decode(f, model)
    assert words == ("tomorrow", "I", "will", "fly")
    assert math.isclose(score, -5.4, abs_tol=1e-9)
    assert steps == [(0, 1, ("tomorrow",)), (1, 3, ("I", "will", "fly"))]
    assert math.isclose(exhaustive(f, model)[0], score, abs_tol=1e-9)
    fc = future_cost_table(f, model)
    assert [round(x, 9) for x in fc[0][1:]] == [-1.2, -2.5, -3.8]
    # without the two-word phrase the best derivation reorders
    model.table.pop(("fliege", "ich"))
    score, words, steps = decode(f, model)
    assert words == ("tomorrow", "I", "will", "fly")
    assert steps == [(0, 1, ("tomorrow",)), (2, 3, ("I",)), (1, 2, ("will", "fly"))]
    assert math.isclose(score, -6.2, abs_tol=1e-9)
    # a distortion limit of 1 forbids the jump back from 3 to 1
    model.distortion_limit = 1
    assert decode(f, model)[1] == ("tomorrow", "will", "fly", "I")


def test_narrow_beam_fails() -> None:
    table = {("a",): [(("x",), -0.1), (("y",), -1.0)], ("b",): [(("z",), 0.0)]}
    lm = BigramLM(
        {("<s>", "x"): -1.0, ("<s>", "y"): -1.0, ("x", "z"): -5.0, ("y", "z"): -0.1, ("z", "</s>"): 0.0},
        floor=-20.0,
    )
    model = Model(table, lm, distortion_weight=1.0, distortion_limit=0)
    best = exhaustive(["a", "b"], model)
    assert best[1] == ("y", "z") and math.isclose(best[0], -2.1, abs_tol=1e-9)
    assert math.isclose(decode(["a", "b"], model)[0], -2.1, abs_tol=1e-9)
    narrow = decode(["a", "b"], model, stack_size=1)
    assert narrow[1] == ("x", "z") and math.isclose(narrow[0], -6.1, abs_tol=1e-9)
    tight = decode(["a", "b"], model, threshold=0.5)
    assert tight[1] == ("x", "z")


def random_model(rng: random.Random, m: int) -> tuple[list[str], Model]:
    f = [f"s{k}" for k in range(m)]
    vocab = ["p", "q", "r", "t"]
    table = {}
    for s in range(m):
        for t in range(s + 1, min(m, s + 3) + 1):
            if t - s > 1 and rng.random() < 0.5:
                continue
            opts = []
            for _ in range(rng.randint(1, 2)):
                target = tuple(rng.choice(vocab) for _ in range(rng.randint(1, 2)))
                opts.append((target, -rng.uniform(0.0, 3.0)))
            table[tuple(f[s:t])] = opts
    lp = {}
    for a in ["<s>"] + vocab:
        for b in vocab + ["</s>"]:
            lp[(a, b)] = -rng.uniform(0.1, 4.0)
    model = Model(table, BigramLM(lp), lm_weight=rng.uniform(0.5, 1.5), distortion_weight=rng.uniform(0.0, 1.5), word_penalty=rng.uniform(-0.5, 0.5))
    return f, model


def test_wide_beam_equals_exhaustive() -> None:
    rng = random.Random(2004)
    for _ in range(120):
        m = rng.randint(1, 4)
        f, model = random_model(rng, m)
        model.distortion_limit = rng.choice([None, None, 0, 1, 2])
        exact, _ = exhaustive(f, model)
        score, words, steps = decode(f, model)
        if exact == -math.inf:
            assert score == -math.inf
            continue
        assert math.isclose(score, exact, abs_tol=1e-9)
        assert math.isclose(score_derivation(f, model, steps), score, abs_tol=1e-9)
        no_recomb = decode(f, model, recombine=False)[0]
        assert math.isclose(no_recomb, exact, abs_tol=1e-9)
        for k in (1, 2):
            assert decode(f, model, stack_size=k)[0] <= exact + 1e-9


def test_future_cost_is_best_monotone_segmentation() -> None:
    rng = random.Random(11)
    for _ in range(40):
        m = rng.randint(1, 5)
        f, model = random_model(rng, m)
        fc = future_cost_table(f, model)
        for s in range(m):
            for t in range(s + 1, m + 1):
                best = -math.inf
                for cuts in itertools.product([False, True], repeat=t - s - 1):
                    bounds = [s] + [s + k + 1 for k, c in enumerate(cuts) if c] + [t]
                    total = 0.0
                    for a, b in zip(bounds, bounds[1:]):
                        opts = model.table.get(tuple(f[a:b]), [])
                        if not opts:
                            total = -math.inf
                            break
                        total += max(tm + model.lm_weight * model.lm.estimate(tg) + model.word_penalty * len(tg) for tg, tm in opts)
                    best = max(best, total)
                assert math.isclose(fc[s][t], best, abs_tol=1e-9) or fc[s][t] == best == -math.inf


def test_narrow_beam_failure_is_common() -> None:
    rng = random.Random(5)
    fails = 0
    for _ in range(60):
        f, model = random_model(rng, 4)
        exact = exhaustive(f, model)[0]
        if decode(f, model, stack_size=1)[0] < exact - 1e-9:
            fails += 1
    assert fails > 0
