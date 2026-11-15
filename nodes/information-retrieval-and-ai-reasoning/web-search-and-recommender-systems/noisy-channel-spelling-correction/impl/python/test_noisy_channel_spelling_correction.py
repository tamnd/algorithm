# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/noisy-channel-spelling-correction/. The authors are listed in prov/01YMRN.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

import irtoy
from noisy_channel_spelling_correction import BOUNDARY, ErrorModel, candidates, char_counts, correct

TOKENS = [t for d in sorted(irtoy.DOCS) for t in irtoy.tokenize(irtoy.DOCS[d])]
WORDS = Counter(TOKENS)

# The toy confusion tables of the page.
DELS = {("t", "e"): 6, ("t", "i"): 3, ("e", "r"): 2, ("r", "a"): 1}
INS = {("t", "d"): 1, ("s", "s"): 2}
SUBS = {("h", "m"): 1, ("e", "a"): 4, ("a", "e"): 3}
TRANS = {("i", "s"): 2, ("e", "i"): 1}


def toy_model():
    return ErrorModel(DELS, INS, SUBS, TRANS, char_counts(TOKENS))


def forward_channel(vocab, dels, ins, subs, trans, chars, alphabet):
    """Apply every single edit to every word w and record the exact P(x | w)."""

    def ratio(table, key, denom):
        n, d = table.get(key, 0), chars.get(denom, 0)
        return Fraction(n, d) if n and d else Fraction(0)

    chan = {}

    def put(x, w, p):
        if p:
            chan.setdefault(x, {})
            chan[x][w] = chan[x].get(w, Fraction(0)) + p

    for w in vocab:
        s = BOUNDARY + w  # s[j] is the letter before position j of w
        for j in range(len(w)):  # delete w[j]
            put(w[:j] + w[j + 1 :], w, ratio(dels, (s[j], w[j]), s[j] + w[j]))
        for j in range(len(w) + 1):  # insert c after position j - 1
            for c in alphabet:
                put(w[:j] + c + w[j:], w, ratio(ins, (s[j], c), s[j]))
        for j in range(len(w)):  # substitute w[j] by e
            for e in alphabet:
                if e != w[j]:
                    put(w[:j] + e + w[j + 1 :], w, ratio(subs, (w[j], e), w[j]))
        for j in range(len(w) - 1):  # swap w[j] and w[j + 1]
            if w[j] != w[j + 1]:
                put(w[:j] + w[j + 1] + w[j] + w[j + 2 :], w, ratio(trans, (w[j], w[j + 1]), w[j : j + 2]))
    return chan


def brute(x, vocab, chan):
    """Exact argmax of P(w) P(x | w) over every word of the vocabulary; ties to the smaller word."""
    total = sum(vocab.values())
    scores = {w: Fraction(vocab[w], total) * chan.get(x, {}).get(w, Fraction(0)) for w in vocab}
    top = max(scores.values())
    return top, sorted(w for w in vocab if scores[w] == top), scores


def check(x, vocab, model, chan, alphabet):
    got, score = correct(x, vocab, model, alphabet)
    top, winners, scores = brute(x, vocab, chan)
    if top == 0:
        assert got is None and score == 0.0
        return
    assert got in winners
    if len(winners) == 1:
        assert got == winners[0]
    assert math.isclose(score, float(top), rel_tol=1e-12)
    # The backward candidate set equals the forward one.
    back = candidates(x, vocab, model, alphabet)
    fwd = chan.get(x, {})
    assert set(back) == {w for w in fwd if w in vocab}
    for w, p in back.items():
        assert math.isclose(p, float(fwd[w]), rel_tol=1e-12)


def test_examples_of_the_page():
    m = toy_model()
    w, s = correct("sortd", WORDS, m)
    assert w == "sorted" and math.isclose(s, 5 / 79 * 6 / 9, rel_tol=1e-12)
    w, s = correct("tme", WORDS, m)
    assert w == "time" and math.isclose(s, 1 / 79 * 3 / 4, rel_tol=1e-12)
    c = candidates("tme", WORDS, m, sorted({ch for w in WORDS for ch in w}))
    assert math.isclose(c["the"], 1 / 9, rel_tol=1e-12) and math.isclose(c["time"], 3 / 4, rel_tol=1e-12)
    assert correct("sorted", WORDS, m) == ("sorted", None)
    assert correct("qqq", WORDS, m) == (None, 0.0)


def test_toy_model_against_brute_force():
    m = toy_model()
    alphabet = sorted({ch for w in WORDS for ch in w})
    chan = forward_channel(WORDS, DELS, INS, SUBS, TRANS, m.chars, alphabet)
    typed = sorted(x for x in chan if x not in WORDS)
    rng = random.Random(1)
    noise = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6))) for _ in range(300)]
    words = sorted(WORDS)
    for _ in range(300):  # a word with one random edit, most of which the tables give probability 0
        w = rng.choice(words)
        j = rng.randrange(len(w))
        noise.append(w[:j] + rng.choice(alphabet) + w[j + 1 :])
    for x in typed + noise + ["sortd", "tme", "lsit", "postng", "arry", "zzzz"]:
        if x not in WORDS:
            check(x, WORDS, m, chan, alphabet)
    assert len(typed) > 50


@pytest.mark.parametrize("seed", range(6))
def test_random_models_against_brute_force(seed):
    rng = random.Random(seed)
    alphabet = ["a", "b", "c"]
    vocab = Counter()
    while len(vocab) < 12:
        w = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
        vocab[w] = rng.randint(1, 5)
    ctx = alphabet + [BOUNDARY]
    dels = {(p, c): rng.randint(0, 4) for p in ctx for c in alphabet}
    ins = {(p, c): rng.randint(0, 4) for p in ctx for c in alphabet}
    subs = {(c, e): rng.randint(0, 4) for c in alphabet for e in alphabet if c != e}
    trans = {(c, d): rng.randint(0, 4) for c in alphabet for d in alphabet if c != d}
    chars = char_counts([w for w, n in vocab.items() for _ in range(n)])
    m = ErrorModel(dels, ins, subs, trans, chars)
    chan = forward_channel(vocab, dels, ins, subs, trans, chars, alphabet)
    typed = sorted(x for x in chan if x not in vocab)
    for x in typed:
        check(x, vocab, m, chan, alphabet)
