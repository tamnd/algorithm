# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chen-manning-parser/. The authors are listed in prov/ZT8KWQ.jsonl.

import itertools
import math
import random

import pytest

from chen_manning_parser import (
    NULL,
    ROOT,
    Config,
    Model,
    Vocab,
    apply,
    exhaustive_best,
    feature_positions,
    features,
    hidden_from_precomputed,
    is_legal,
    legal_log_probs,
    loss_and_grad_W2,
    parse,
    precompute,
    shortest_stack_oracle,
    training_examples,
    transitions,
)
from nlslog import NEG_INF

WORDS = [None, "the", "cat", "sat", "on", "the", "mat"]
TAGS = [None, "DET", "NOUN", "VERB", "ADP", "DET", "NOUN"]
GOLD_HEADS = [-1, 2, 3, 0, 6, 6, 3]
GOLD_LABELS = [None, "det", "nsubj", "root", "case", "det", "obl"]
LABELS = ["det", "nsubj", "root", "case", "obl"]
WV, TV, LV = Vocab(WORDS[1:]), Vocab(TAGS[1:]), Vocab(LABELS)


def is_tree(heads):
    n = len(heads) - 1
    for d in range(1, n + 1):
        x, steps = d, 0
        while x != 0:
            x, steps = heads[x], steps + 1
            if x == -1 or steps > n:
                return False
    return True


def is_projective(heads):
    n = len(heads) - 1
    for d in range(1, n + 1):
        h = heads[d]
        for k in range(min(h, d) + 1, max(h, d)):
            x = k
            while x != h and x != 0:
                x = heads[x]
            if x != h:
                return False
    return True


def run(seq_names, n=6):
    c = Config(n)
    for name in seq_names:
        kind, _, lab = name.partition("-")
        apply(c, (kind, lab or None))
    return c


def test_vocab_specials():
    assert [WV.id(NULL), WV.id(ROOT), WV.id("zebra")] == [0, 1, 2]
    assert WV.id("the") == 3 and len(WV) == 3 + 5


def test_feature_positions_on_the_example():
    c = run(["SH", "SH", "LA-det", "SH"])
    words_pos, label_pos = feature_positions(c)
    assert words_pos[:6] == [3, 2, 0, 4, 5, 6]
    assert words_pos[6:12] == [None] * 6  # "sat" has no dependent yet
    assert words_pos[12:] == [1, None, None, None, None, None]  # lc1(cat) = the
    assert label_pos == words_pos[6:]
    f = features(c, WORDS, TAGS, WV, TV, LV)
    assert len(f) == 48
    assert f[:6] == [WV.id("sat"), WV.id("cat"), WV.id(ROOT), WV.id("on"), WV.id("the"), WV.id("mat")]
    assert f[18:21] == [TV.id("VERB"), TV.id("NOUN"), TV.id(ROOT)]
    assert f[36:] == [LV.id(NULL)] * 6 + [LV.id("det")] + [LV.id(NULL)] * 5


def test_second_children_and_grandchildren():
    c = Config(6)
    c.stack, c.next = [0, 3], 7
    c.heads = [-1, 2, 3, -1, 3, 6, 3]  # 3 has left 2 (with 1 under it), right 4 and 6 (with 5 under it)
    words_pos, _ = feature_positions(c)
    assert words_pos[6:12] == [2, 6, None, 4, 1, None]
    c.heads[1] = 3
    words_pos, _ = feature_positions(c)
    assert words_pos[6:12] == [1, 6, 2, 4, None, None]


def test_oracle_sequence_and_projectivity():
    ex = training_examples(WORDS, TAGS, GOLD_HEADS, GOLD_LABELS, WV, TV, LV)
    names = [t[0] if t[1] is None else f"{t[0]}-{t[1]}" for _, t, _ in ex]
    assert names == ["SH", "SH", "LA-det", "SH", "LA-nsubj", "SH", "SH", "SH", "LA-det", "LA-case", "RA-obl", "RA-root"]
    for n in range(1, 6):
        words, tags = [None] + ["w"] * n, [None] + ["t"] * n
        for hs in itertools.product(range(n + 1), repeat=n):
            heads = [-1] + list(hs)
            if not is_tree(heads):
                continue
            labels = [None] + ["dep"] * n
            if is_projective(heads):
                assert len(training_examples(words, tags, heads, labels, Vocab(["w"]), Vocab(["t"]), Vocab(["dep"]))) == 2 * n
            else:
                with pytest.raises(ValueError):
                    training_examples(words, tags, heads, labels, Vocab(["w"]), Vocab(["t"]), Vocab(["dep"]))


def test_cube_activation_and_precomputation():
    rng = random.Random(1)
    trans = transitions(LABELS)
    m = Model(len(WV), len(TV), len(LV), 4, 6, len(trans), rng)
    ex = training_examples(WORDS, TAGS, GOLD_HEADS, GOLD_LABELS, WV, TV, LV)
    pre = precompute(m, [range(len(WV))] * 18 + [range(len(TV))] * 18 + [range(len(LV))] * 12)
    for f, _, _ in ex:
        h, _ = m.forward(f)
        h2 = hidden_from_precomputed(m, pre, f)
        assert all(abs(a - b) <= 1e-9 * max(1.0, abs(a)) for a, b in zip(h, h2))
    m.W1 = [[0.0] * (48 * 4) for _ in range(6)]
    m.b1 = [1.0, -2.0, 0.5, 0.0, 3.0, -1.0]
    h, _ = m.forward(ex[0][0])
    assert h == [1.0, -8.0, 0.125, 0.0, 27.0, -1.0]


def test_softmax_over_legal_transitions():
    z = [2.0, 1.0, -1.0, 0.5]
    lp = legal_log_probs(z, [True, False, True, True])
    assert lp[1] == NEG_INF
    assert abs(math.fsum(math.exp(v) for v in lp) - 1.0) <= 1e-12
    assert abs(lp[0] - lp[3] - 1.5) <= 1e-12


def test_greedy_parser_gives_projective_trees():
    rng = random.Random(2)
    for trial in range(30):
        n = rng.randint(1, 7)
        words = [None] + [rng.choice(WORDS[1:]) for _ in range(n)]
        tags = [None] + [rng.choice(TAGS[1:]) for _ in range(n)]
        m = Model(len(WV), len(TV), len(LV), 3, 5, len(transitions(LABELS)), random.Random(trial))
        single = trial % 2 == 1
        heads, labels, seq, total = parse(m, words, tags, WV, TV, LV, LABELS, single_root=single)
        assert len(seq) == 2 * n and is_tree(heads) and is_projective(heads)
        assert all(labels[d] in LABELS for d in range(1, n + 1))
        if single:
            assert sum(1 for d in range(1, n + 1) if heads[d] == 0) == 1
        assert total <= 0.0


def test_greedy_is_not_exact():
    words, tags = [None, "the", "cat", "sat", "down"], [None, "DT", "NN", "VBD", "RP"]
    wv, tv, lv = Vocab(words[1:]), Vocab(tags[1:]), Vocab(["dep"])
    worse = 0
    for seed in range(12):
        m = Model(len(wv), len(tv), len(lv), 3, 5, 3, random.Random(seed))
        _, _, _, greedy = parse(m, words, tags, wv, tv, lv, ["dep"])
        best, heads, seq = exhaustive_best(m, words, tags, wv, tv, lv, ["dep"])
        assert best >= greedy - 1e-12 and len(seq) == 8 and is_projective(heads)
        worse += best > greedy + 1e-9
    m = Model(len(wv), len(tv), len(lv), 3, 5, 3, random.Random(10))
    _, _, _, greedy = parse(m, words, tags, wv, tv, lv, ["dep"])
    best, _, _ = exhaustive_best(m, words, tags, wv, tv, lv, ["dep"])
    assert best > greedy + 0.1
    assert worse >= 1


def test_gradient_in_W2_by_finite_differences():
    rng = random.Random(5)
    trans = transitions(LABELS)
    m = Model(len(WV), len(TV), len(LV), 3, 4, len(trans), rng)
    ex = training_examples(WORDS, TAGS, GOLD_HEADS, GOLD_LABELS, WV, TV, LV)
    f, t, c = ex[4]
    legal = [is_legal(c, u) for u in trans]
    gold = trans.index(t)
    loss, grad = loss_and_grad_W2(m, f, legal, gold)
    eps = 1e-6
    for i in range(len(trans)):
        for j in range(4):
            old = m.W2[i][j]
            m.W2[i][j] = old + eps
            up, _ = loss_and_grad_W2(m, f, legal, gold)
            m.W2[i][j] = old - eps
            down, _ = loss_and_grad_W2(m, f, legal, gold)
            m.W2[i][j] = old
            assert abs((up - down) / (2 * eps) - grad[i][j]) <= 1e-6 * max(1.0, abs(grad[i][j]))
    assert loss > 0


def test_oracle_prefers_left_arc():
    c = run(["SH", "SH"])
    assert shortest_stack_oracle(c, GOLD_HEADS, GOLD_LABELS) == ("LA", "det")
