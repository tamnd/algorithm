# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-perceptron/. The authors are listed in prov/KYD1XY.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from structured_perceptron import BOS, EOS, brute_force, phi, score, train, train_naive_average, viterbi

TAGS = ["A", "B", "C"]
VOCAB = ["p", "q", "r", "s"]

CORPUS = [
    ("the dog runs".split(), ["D", "N", "V"]),
    ("the old dog runs".split(), ["D", "J", "N", "V"]),
    ("dogs run".split(), ["N", "V"]),
    ("the runs".split(), ["D", "N"]),
    ("old dogs walk".split(), ["J", "N", "V"]),
]


def all_features(tags, vocab):
    feats = [("T", a, b) for a in [BOS] + tags for b in tags + [EOS]]
    return feats + [("E", t, x) for t in tags for x in vocab]


def random_weights(rng, tags, vocab, lo=-5, hi=5):
    return {f: rng.randint(lo, hi) for f in all_features(tags, vocab)}


def sq_norm(d):
    return sum(v * v for v in d.values())


def diff(a, b):
    d = dict(a)
    for k, v in b.items():
        d[k] = d.get(k, 0) - v
    return {k: v for k, v in d.items() if v}


def test_phi_counts():
    f = phi(["p", "q", "p"], ["A", "A", "B"])
    assert f == {("T", BOS, "A"): 1, ("E", "A", "p"): 1, ("T", "A", "A"): 1, ("E", "A", "q"): 1,
                 ("T", "A", "B"): 1, ("E", "B", "p"): 1, ("T", "B", EOS): 1}
    assert sum(f.values()) == 2 * 3 + 1


def test_viterbi_matches_brute_force():
    rng = random.Random(2002)
    for _ in range(300):
        k = rng.randint(1, 3)
        tags = TAGS[:k]
        n = rng.randint(1, 6)
        words = [rng.choice(VOCAB) for _ in range(n)]
        w = random_weights(rng, tags, VOCAB, -3, 3)
        ys, s = viterbi(words, tags, w)
        assert len(ys) == n
        assert s == score(w, words, ys) == brute_force(words, tags, w)


def test_viterbi_ties_and_errors():
    assert viterbi(["p", "q"], TAGS, {}) == (["A", "A"], 0)
    with pytest.raises(ValueError):
        viterbi([], TAGS, {})


def test_lazy_average_equals_naive_average():
    rng = random.Random(5)
    for _ in range(10):
        data = []
        for _ in range(rng.randint(1, 6)):
            n = rng.randint(1, 5)
            data.append(([rng.choice(VOCAB) for _ in range(n)], [rng.choice(TAGS) for _ in range(n)]))
        epochs = rng.randint(1, 4)
        _, avg, _ = train(data, TAGS, epochs)
        naive = train_naive_average(data, TAGS, epochs)
        keys = set(avg) | set(naive)
        assert all(avg.get(k, Fraction(0)) == naive.get(k, Fraction(0)) for k in keys)


def separable_data(rng, tags, count):
    """Label random sentences with a fixed weight vector, keeping only those with a unique best tagging."""
    u = random_weights(rng, tags, VOCAB)
    data, margin, r2 = [], None, 0
    while len(data) < count:
        n = rng.randint(1, 5)
        words = [rng.choice(VOCAB) for _ in range(n)]
        scored = sorted(((score(u, words, ys), ys) for ys in product(tags, repeat=n)), reverse=True)
        if len(scored) > 1 and scored[0][0] == scored[1][0]:
            continue
        gold = list(scored[0][1])
        data.append((words, gold))
        if len(scored) > 1:
            m = scored[0][0] - scored[1][0]
            margin = m if margin is None else min(margin, m)
        fg = phi(words, gold)
        for _, ys in scored[1:]:
            r2 = max(r2, sq_norm(diff(fg, phi(words, ys))))
    return u, data, margin, r2


def test_mistake_bound_on_separable_data():
    """Collins (2002), Theorem 1: mistakes <= R^2 / delta^2 with delta = margin / ||u||."""
    rng = random.Random(17)
    for _ in range(6):
        u, data, margin, r2 = separable_data(rng, TAGS, 12)
        w, _, mistakes = train(data, TAGS, 60)
        total = sum(mistakes)
        assert total * margin * margin <= r2 * sq_norm(u)
        assert mistakes[-1] == 0
        assert all(viterbi(x, TAGS, w)[0] == y for x, y in data)


def test_mistakes_stop_once_an_epoch_is_clean():
    rng = random.Random(3)
    _, data, _, _ = separable_data(rng, TAGS[:2], 10)
    _, _, mistakes = train(data, TAGS[:2], 40)
    first_clean = mistakes.index(0)
    assert all(m == 0 for m in mistakes[first_clean:])


def test_averaged_tagger_on_small_corpus():
    tags = ["D", "J", "N", "V"]
    w, avg, mistakes = train(CORPUS, tags, 10)
    assert mistakes[-1] == 0
    for x, y in CORPUS:
        assert viterbi(x, tags, avg)[0] == y
    assert viterbi("the old dogs walk".split(), tags, avg)[0] == ["D", "J", "N", "V"]
