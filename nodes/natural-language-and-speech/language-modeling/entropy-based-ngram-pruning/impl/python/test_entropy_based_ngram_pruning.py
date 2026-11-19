# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-based-ngram-pruning/. The authors are listed in prov/AG7MBF.jsonl.

import math
import random
from fractions import Fraction

import pytest

from entropy_based_ngram_pruning import BOS, EOS, BackoffLM, log_fraction, prune, pruning_cost

SMALL = [["a", "b"], ["a", "c"], ["b", "c"], ["a", "b"]]


def zipf_corpus(seed, sentences, size, max_len):
    rng = random.Random(seed)
    words = [f"w{i}" for i in range(size)]
    weights = [1 / (i + 1) for i in range(size)]
    return [rng.choices(words, weights, k=rng.randint(1, max_len)) for _ in range(sentences)]


def kl(p, q):
    return sum(float(p[v]) * (log_fraction(p[v]) - log_fraction(q[v])) for v in p if p[v] > 0)


def brute_cost(lm, g):
    """Remove g by hand, renormalize the row of h directly, and take p(h) times the KL of the row."""
    h, w = g[:-1], g[-1]
    keep = lm.explicit[h] - {w}
    old = lm.distribution(h)
    lower = lm.distribution(h[1:])
    left = 1 - sum(lm.pstar(h + (v,)) for v in keep)
    lower_left = sum(lower[v] for v in lm.vocab if v not in keep)
    new = {v: lm.pstar(h + (v,)) if v in keep else left * lower[v] / lower_left for v in lm.vocab}
    assert sum(new.values()) == 1
    return float(lm.history_prob(h)) * kl(old, new)


def full_kl(lm, pruned):
    """The sum over every seen history of length n - 1 of p(h) KL(row of lm, row of pruned)."""
    total = 0.0
    for h in lm.ch:
        if len(h) == lm.n - 1:
            total += float(lm.history_prob(h)) * kl(lm.distribution(h), pruned.distribution(h))
    return total


def explicit_ngrams(lm, order=None):
    return [h + (w,) for h in sorted(lm.explicit) for w in sorted(lm.explicit[h]) if order in (None, len(h) + 1)]


def test_small_model_by_hand():
    lm = BackoffLM(SMALL, 2)
    assert lm.alpha == {(BOS,): Fraction(1, 2), ("a",): Fraction(4, 7), ("b",): Fraction(2, 3), ("c",): Fraction(3, 8)}
    assert lm.distribution((BOS,)) == {EOS: Fraction(1, 6), "a": Fraction(5, 8), "b": Fraction(1, 8), "c": Fraction(1, 12)}
    assert lm.distribution(("c",)) == {EOS: Fraction(3, 4), "a": Fraction(3, 32), "b": Fraction(3, 32), "c": Fraction(1, 16)}
    # removing <s> b changes nothing: alpha'(<s>) p(b) = 1/2 * 1/4 = 1/8 = p*(b | <s>)
    assert pruning_cost(lm, (BOS, "b")) == 0.0
    assert lm.without([(BOS, "b")]).distribution((BOS,)) == lm.distribution((BOS,))
    assert pruning_cost(lm, ("a", "c")) == pytest.approx(brute_cost(lm, ("a", "c")), rel=1e-12)


def test_history_prob_is_the_chain_rule():
    lm = BackoffLM(SMALL, 3)
    assert lm.history_prob((BOS, BOS)) == 1
    assert lm.history_prob((BOS, "a")) == lm.prob("a", (BOS,))
    assert lm.history_prob(("a", "b")) == lm.prob("a", ()) * lm.prob("b", ("a",))


@pytest.mark.parametrize("n,seed", [(2, 1), (3, 2), (4, 3)])
def test_cost_matches_brute_force(n, seed):
    lm = BackoffLM(zipf_corpus(seed, 40, 15, 5), n)
    for g in explicit_ngrams(lm):
        assert pruning_cost(lm, g) == pytest.approx(brute_cost(lm, g), rel=1e-9, abs=1e-15)


@pytest.mark.parametrize("n,seed", [(2, 4), (3, 5)])
def test_top_order_cost_is_the_model_relative_entropy(n, seed):
    lm = BackoffLM(zipf_corpus(seed, 40, 15, 5), n)
    for g in explicit_ngrams(lm, order=n)[::3]:
        assert pruning_cost(lm, g) == pytest.approx(full_kl(lm, lm.without([g])), rel=1e-9, abs=1e-15)


def test_costs_add_only_across_different_histories():
    lm = BackoffLM(zipf_corpus(6, 40, 15, 5), 2)
    by_h = {}
    for g in explicit_ngrams(lm):
        by_h.setdefault(g[:-1], []).append(g)
    hs = [h for h in sorted(by_h) if len(by_h[h]) >= 2]
    g1, g2 = by_h[hs[0]][:2]
    same = full_kl(lm, lm.without([g1, g2]))
    assert abs(same - (pruning_cost(lm, g1) + pruning_cost(lm, g2))) > 1e-6
    g3 = by_h[hs[1]][0]
    apart = full_kl(lm, lm.without([g1, g3]))
    assert apart == pytest.approx(pruning_cost(lm, g1) + pruning_cost(lm, g3), rel=1e-9)


@pytest.mark.parametrize("n,seed", [(2, 7), (3, 8)])
def test_rows_sum_to_one_after_pruning(n, seed):
    lm = BackoffLM(zipf_corpus(seed, 60, 20, 6), n)
    histories = {h for h in lm.ch if len(h) <= n - 1} | {("zz",) * (n - 1)}
    for theta in [0, 1e-4, 1e-3, 1e-2]:
        pruned, _ = prune(lm, theta)
        for h in histories:
            row = pruned.distribution(h[-(n - 1) :] if n > 1 else ())
            assert sum(row.values()) == 1 and all(p > 0 for p in row.values())


def test_threshold_order():
    lm = BackoffLM(zipf_corpus(9, 80, 20, 6), 3)
    assert prune(lm, 0)[1] == []
    sizes, last = [], set()
    for theta in [0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
        pruned, marked = prune(lm, theta)
        assert last <= set(marked)
        last = set(marked)
        sizes.append(pruned.num_explicit())
        assert pruned.num_explicit() + len(marked) == lm.num_explicit()
    assert sizes == sorted(sizes, reverse=True) and sizes[0] > sizes[-1]


def test_huge_threshold_leaves_the_unigram():
    lm = BackoffLM(zipf_corpus(10, 40, 15, 5), 3)
    pruned, marked = prune(lm, 1e9)
    assert len(marked) == lm.num_explicit() and pruned.num_explicit() == 0
    uni = pruned.distribution(())
    assert pruned.distribution(("w0", "w1")) == uni
    assert uni == {w: Fraction(lm.c[(w,)], lm.total) for w in lm.vocab}


def test_pruned_model_is_close_on_training_text():
    corpus = zipf_corpus(11, 80, 20, 6)
    lm = BackoffLM(corpus, 3)
    pruned, marked = prune(lm, 1e-3)
    assert marked
    full = sum(lm.sentence_logprob(s) for s in corpus)
    small = sum(pruned.sentence_logprob(s) for s in corpus)
    assert small < full  # the training text loses probability, but not much
    tokens = sum(len(s) + 1 for s in corpus)
    assert math.exp((full - small) / tokens) < 1.5


def test_log_space_where_the_product_underflows():
    lm = BackoffLM(zipf_corpus(12, 40, 15, 5), 3)
    rng = random.Random(13)
    sent = [rng.choice(lm.vocab[1:]) for _ in range(1500)]
    product = 1.0
    for i, w in enumerate(sent + [EOS]):
        product *= float(lm.prob(w, lm.history(sent[:i])))
    assert product == 0.0
    assert lm.sentence_logprob(sent) < -745


def test_bad_input():
    lm = BackoffLM(SMALL, 2)
    with pytest.raises(ValueError):
        BackoffLM(SMALL, 0)
    with pytest.raises(ValueError):
        BackoffLM(SMALL, 2, d=1)
    with pytest.raises(ValueError):
        prune(lm, -1)
    with pytest.raises(ValueError):
        lm.without([("a",)])
    with pytest.raises(ValueError):
        pruning_cost(lm, ("c", "a"))
    with pytest.raises(ValueError):
        BackoffLM([["a", "a"]], 2)  # a is followed by every word, a and </s>
