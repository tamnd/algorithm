# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-prediction/. The authors are listed in prov/DHVXMW.jsonl.

import itertools
import math
import random

import pytest

from structured_prediction import (
    START,
    brute_force_decode,
    hamming,
    phi,
    score,
    ssvm_subgradient,
    structured_hinge,
    structured_perceptron,
    viterbi,
)

L = ["D", "N", "V"]
DATA = [(s.split(), t.split()) for s, t in [
    ("the dog runs", "D N V"), ("a cat sees the dog", "D N V D N"),
    ("the cat runs", "D N V"), ("a dog sees a cat", "D N V D N")]]


def random_weights(rng, labels, vocab, integer):
    w = {}
    for a in labels:
        for tok in vocab:
            w[("E", a, tok)] = rng.randint(-3, 3) if integer else rng.gauss(0, 1)
        for b in [START] + list(labels):
            w[("T", b, a)] = rng.randint(-3, 3) if integer else rng.gauss(0, 1)
    return w


def test_viterbi_matches_brute_force() -> None:
    rng = random.Random(1)
    vocab = list("abcd")
    for _ in range(300):
        labels = list(range(rng.randint(1, 4)))
        w = random_weights(rng, labels, vocab, integer=rng.random() < 0.5)
        x = [rng.choice(vocab) for _ in range(rng.randint(0, 6))]
        z = viterbi(w, x, labels)
        best, _ = brute_force_decode(w, x, labels)
        if x:
            assert score(w, x, z) == pytest.approx(best)
        else:
            assert z == []


def test_loss_augmented_viterbi_matches_brute_force() -> None:
    rng = random.Random(2)
    vocab = list("abc")
    for _ in range(300):
        labels = list(range(rng.randint(1, 4)))
        w = random_weights(rng, labels, vocab, integer=rng.random() < 0.5)
        x = [rng.choice(vocab) for _ in range(rng.randint(1, 6))]
        gold = [rng.choice(labels) for _ in x]
        z = viterbi(w, x, labels, gold=gold)
        best, _ = brute_force_decode(w, x, labels, gold=gold)
        assert score(w, x, z) + hamming(gold, z) == pytest.approx(best)
        hinge = structured_hinge(w, x, gold, labels)
        assert hinge >= -1e-9
        assert hinge >= hamming(gold, viterbi(w, x, labels)) - 1e-9


def test_hand_example() -> None:
    assert viterbi({}, "the dog runs".split(), L) == ["D", "D", "D"]
    w, mistakes = structured_perceptron(DATA[:1], L, 1, average=False)
    assert mistakes == [1]
    assert {k: v for k, v in w.items() if v} == {
        ("E", "N", "dog"): 1, ("E", "D", "dog"): -1, ("E", "V", "runs"): 1, ("E", "D", "runs"): -1,
        ("T", "D", "N"): 1, ("T", "N", "V"): 1, ("T", "D", "D"): -2,
    }
    assert viterbi(w, "a cat sees the dog".split(), L) == ["D", "N", "V", "D", "N"]
    assert score(w, "a cat sees the dog".split(), "D N V D N".split()) == 4
    assert viterbi(w, "the cat sees".split(), L) == ["D", "N", "V"]
    assert score(w, "the cat sees".split(), ["D", "N", "V"]) == 2


def test_perceptron_mistake_bound() -> None:
    # Data labeled by a random w*: separable with margin delta > 0, so Collins'
    # Theorem 1 bounds the total number of mistakes by R^2 / delta^2.
    rng = random.Random(3)
    labels, vocab = [0, 1, 2], list("abcde")
    for _ in range(5):
        w_star = random_weights(rng, labels, vocab, integer=False)
        norm = math.sqrt(sum(v * v for v in w_star.values()))
        data = []
        for _ in range(12):
            x = [rng.choice(vocab) for _ in range(rng.randint(1, 4))]
            data.append((x, viterbi(w_star, x, labels)))
        delta, r2 = math.inf, 0.0
        for x, y in data:
            for z in itertools.product(labels, repeat=len(x)):
                if list(z) == list(y):
                    continue
                d = phi(x, y)
                d.subtract(phi(x, z))
                delta = min(delta, sum(w_star.get(k, 0) * v for k, v in d.items()) / norm)
                r2 = max(r2, sum(v * v for v in d.values()))
        assert delta > 0
        _, mistakes = structured_perceptron(data, labels, 10000, average=False)
        assert mistakes[-1] == 0
        assert sum(mistakes) <= r2 / delta ** 2


def test_averaged_weights_are_the_mean_of_the_iterates() -> None:
    rng = random.Random(4)
    labels, vocab = [0, 1], list("ab")
    data = [([rng.choice(vocab) for _ in range(3)], [rng.choice(labels) for _ in range(3)]) for _ in range(5)]
    avg, mistakes = structured_perceptron(data, labels, 3)
    w, total, steps = {}, {}, 0
    for _ in range(len(mistakes)):
        for x, y in data:
            z = viterbi(w, x, labels)
            if z != y:
                d = phi(x, y)
                d.subtract(phi(x, z))
                for k, v in d.items():
                    w[k] = w.get(k, 0) + v
            for k, v in w.items():
                total[k] = total.get(k, 0) + v
            steps += 1
    for k in set(avg) | set(total):
        assert avg.get(k, 0) == pytest.approx(total.get(k, 0) / steps)


def test_toy_tagger_learns() -> None:
    w, mistakes = structured_perceptron(DATA, L, 20)
    assert mistakes[-1] == 0
    assert viterbi(w, "a cat runs".split(), L) == ["D", "N", "V"]
    assert viterbi(w, "the dog sees a dog".split(), L) == ["D", "N", "V", "D", "N"]


def test_structured_svm_subgradient() -> None:
    w, hist = ssvm_subgradient(DATA, L, 50)
    assert hist[0] == pytest.approx(4.0)  # w = 0: loss-augmented decoding gets every tag wrong
    assert hist[-1] < 0.1 * hist[0]
    for x, y in DATA:
        assert viterbi(w, x, L) == y
