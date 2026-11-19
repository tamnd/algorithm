# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stack-decoding/. The authors are listed in prov/A0NEW4.jsonl.

import itertools
import math
import random

from nlslog import NEG_INF
from stack_decoding import BOS, EOS, decode, default_heuristic, word_scores

PHONES = ["p", "q", "r"]
LOG_HALF = math.log(0.5)


def brute_force(lexicon, lm, emit, lm_weight=1.0, ip=0.0, max_words=5):
    """Best score over all word sequences of at most max_words words and all segmentations."""
    T = len(emit)
    best = NEG_INF
    for k in range(1, max_words + 1):
        for words in itertools.product(sorted(lexicon), repeat=k):
            phones = [ph for w in words for ph in lexicon[w]]
            if len(phones) > T:
                continue
            lm_part, prev = 0.0, BOS
            for w in list(words) + [EOS]:
                lm_part += lm_weight * lm.get((prev, w), NEG_INF)
                prev = w
            if lm_part == NEG_INF:
                continue
            for cuts in itertools.combinations(range(1, T), len(phones) - 1):
                bounds = (0,) + cuts + (T,)
                s = lm_part + k * ip
                for j, ph in enumerate(phones):
                    d = bounds[j + 1] - bounds[j]
                    s += sum(emit[u][ph] for u in range(bounds[j], bounds[j + 1])) + (d - 1) * LOG_HALF + LOG_HALF
                best = max(best, s)
    return best


def random_task(rng: random.Random, T: int):
    lexicon = {w: tuple(rng.choice(PHONES) for _ in range(rng.randint(1, 2))) for w in ["A", "B", "C"]}
    vocab = sorted(lexicon)
    lm = {}
    for v in [BOS] + vocab:
        probs = [rng.random() + 0.1 for _ in range(len(vocab) + 1)]
        z = sum(probs)
        for w, p in zip(vocab + [EOS], probs):
            lm[(v, w)] = math.log(p / z)
    emit = [{ph: -rng.uniform(0.0, 4.0) for ph in PHONES} for _ in range(T)]
    return lexicon, lm, emit


def test_word_scores():
    emit = [{"a": -1.0, "b": -2.0}, {"a": -3.0, "b": -0.5}, {"a": -1.0, "b": -1.0}]
    out = word_scores(("a", "b"), emit, 0, LOG_HALF, LOG_HALF)
    assert set(out) == {2, 3}
    assert abs(out[2] - (-1.0 - 0.5 + 2 * LOG_HALF)) < 1e-12
    assert abs(out[3] - (-1.0 - 0.5 - 1.0 + 3 * LOG_HALF)) < 1e-12


def test_heuristic_is_an_upper_bound():
    rng = random.Random(30)
    for _ in range(30):
        lexicon, lm, emit = random_task(rng, 4)
        h = default_heuristic(emit, 0.0)
        for t in range(5):
            rest = emit[t:]
            if rest:
                # The best score of any single word that covers the rest is at most h[t].
                for w in lexicon:
                    s = word_scores(lexicon[w], emit, t, LOG_HALF, LOG_HALF).get(4, NEG_INF)
                    assert s <= h[t] + 1e-12


def test_matches_brute_force():
    rng = random.Random(31)
    for _ in range(60):
        T = rng.randint(1, 5)
        lexicon, lm, emit = random_task(rng, T)
        kw = {"lm_weight": rng.choice([0.5, 1.0, 2.0]), "ip": rng.choice([-1.0, 0.0, 0.5])}
        words, ends, score, _ = decode(lexicon, lm, emit, **kw)
        expected = brute_force(lexicon, lm, emit, **kw)
        if expected == NEG_INF:
            assert (words, ends, score) == ([], [], NEG_INF)
            continue
        assert abs(score - expected) < 1e-9
        assert ends[-1] == T - 1
        assert all(a < b for a, b in zip(ends, ends[1:]))


def test_wide_stack_changes_nothing():
    rng = random.Random(32)
    for _ in range(30):
        lexicon, lm, emit = random_task(rng, 5)
        a = decode(lexicon, lm, emit)
        b = decode(lexicon, lm, emit, max_stack=10 ** 6)
        assert a[:3] == b[:3]


def narrow_task():
    lexicon = {"x": ("a",), "y": ("b",), "z": ("c", "d")}
    lm = {(v, w): 0.0 for v in [BOS, "x", "y", "z"] for w in ["x", "y", "z", EOS]}
    emit = [{"a": 0.0, "b": -9.0, "c": -1.0, "d": -9.0}, {"a": -9.0, "b": -9.0, "c": -9.0, "d": -1.0}]
    return lexicon, lm, emit


def test_narrow_stack_misses_the_best_path():
    lexicon, lm, emit = narrow_task()
    words, ends, score, _ = decode(lexicon, lm, emit)
    assert (words, ends) == (["z"], [1]) and abs(score - (-2.0 + 2 * LOG_HALF)) < 1e-12
    words, ends, score, _ = decode(lexicon, lm, emit, max_stack=1)
    assert words[0] == "x"
    assert abs(score - (-9.0 + 2 * LOG_HALF)) < 1e-12


def test_inadmissible_heuristic_can_fail():
    lexicon = {"x": ("a",), "y": ("b",)}
    lm = {(BOS, "x"): LOG_HALF, (BOS, "y"): LOG_HALF}
    for v in ["x", "y"]:
        for w in ["x", "y", EOS]:
            lm[(v, w)] = math.log(1 / 3)
    emit = [{"a": 0.0, "b": -5.0}, {"a": -5.0, "b": 0.0}]
    best = decode(lexicon, lm, emit)
    assert best[0] == ["x", "y"]
    assert abs(best[2] - (2 * LOG_HALF + LOG_HALF + 2 * math.log(1 / 3))) < 1e-12
    # A heuristic far below the true rest makes any complete hypothesis look better than a partial one.
    worse = decode(lexicon, lm, emit, heuristic=lambda t: -100.0 * (2 - t))
    assert len(worse[0]) == 1
    assert worse[2] < best[2] - 3.0


def test_closed_set_limits_pops():
    rng = random.Random(33)
    lexicon, lm, emit = random_task(rng, 5)
    _, _, _, pops = decode(lexicon, lm, emit)
    # At most one expansion per (last word, start frame), plus duplicate and complete pops.
    pushes_bound = 1 + (len(lexicon) + 1) * 6 * len(lexicon) * 6
    assert pops <= pushes_bound
