# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brill-tagger/. The authors are listed in prov/W3YAEV.jsonl.

import random
from itertools import product

import pytest

from brill_tagger import (LEFT, RIGHT, TEMPLATES, Lexicon, apply_rule, best_rule, errors, instances,
                          holds, rule_key, tag, train)

ONE_ARG = ["PREV1", "NEXT1", "PREV2", "NEXT2", "PREV1OR2", "NEXT1OR2", "PREV1OR2OR3", "NEXT1OR2OR3"]
TWO_ARG = ["SURROUND", "PREVBIGRAM", "NEXTBIGRAM"]

EXAMPLE = [
    ("we want to race".split(), ["PRP", "VBP", "TO", "VB"]),
    ("the race ended".split(), ["DT", "NN", "VBD"]),
    ("the race".split(), ["DT", "NN"]),
    ("a race is fun".split(), ["DT", "NN", "VBZ", "JJ"]),
    ("they like to race".split(), ["PRP", "VBP", "TO", "VB"]),
    ("we went to the race".split(), ["PRP", "VBD", "TO", "DT", "NN"]),
]


def all_rules(tags, vocab):
    vals = list(tags) + [LEFT, RIGHT]
    envs = [(t, (z,)) for t in ONE_ARG for z in vals]
    envs += [(t, (z, w)) for t in TWO_ARG for z in vals for w in vals]
    envs += [("CURWD", (w,)) for w in vocab]
    return [(t, args, a, b) for t, args in envs for a in tags for b in tags if a != b]


def brute_best(words_list, cur, gold, lex, rules):
    base = errors(cur, gold)
    best, best_score = None, None
    for r in sorted(rules, key=rule_key):
        new = [apply_rule(r, w, ts, lex) for w, ts in zip(words_list, cur)]
        s = base - errors(new, gold)
        if best is None or s > best_score:
            best, best_score = r, s
    return best, best_score


def random_corpus(rng, tags, vocab, sentences):
    corpus = []
    for _ in range(sentences):
        n = rng.randint(1, 6)
        ws = [rng.choice(vocab) for _ in range(n)]
        gs = [rng.choice(tags) for _ in range(n)]
        corpus.append((ws, gs))
    return corpus


def test_delayed_and_immediate_effect():
    """Brill (1995), Section 2: A A A A A A and the rule A -> B if the previous tag is A."""
    words = ["x"] * 6
    rule = ("PREV1", ("A",), "A", "B")
    assert apply_rule(rule, words, ["A"] * 6) == ["A", "B", "B", "B", "B", "B"]
    assert apply_rule(rule, words, ["A"] * 6, delayed=False) == ["A", "B", "A", "B", "A", "B"]


def test_instances_agree_with_holds():
    rng = random.Random(4)
    tags = ["A", "B", "C"]
    vals = tags + [LEFT, RIGHT]
    for _ in range(50):
        n = rng.randint(1, 6)
        words = [rng.choice("pqr") for _ in range(n)]
        ts = [rng.choice(tags) for _ in range(n)]
        for p in range(n):
            inst = instances(words, ts, p)
            for t in ONE_ARG:
                for z in vals:
                    assert holds(t, (z,), words, ts, p) == ((t, (z,)) in inst)
            for t in TWO_ARG:
                for z, w in product(vals, vals):
                    assert holds(t, (z, w), words, ts, p) == ((t, (z, w)) in inst)
            assert ("CURWD", (words[p],)) in inst


def test_best_rule_matches_brute_force():
    rng = random.Random(1995)
    tags = ["A", "B", "C"]
    vocab = ["p", "q", "r", "s"]
    rules = all_rules(tags, vocab)
    checked = 0
    for _ in range(12):
        corpus = random_corpus(rng, tags, vocab, rng.randint(2, 5))
        lex = Lexicon(corpus)
        words_list = [w for w, _ in corpus]
        gold = [g for _, g in corpus]
        cur = [lex.initial(w) for w in words_list]
        for _ in range(3):
            r, s = best_rule(words_list, cur, gold, lex)
            rb, sb = brute_best(words_list, cur, gold, lex, rules)
            if sb < 1:
                assert r is None or s == sb or s <= 0
                break
            assert (r, s) == (rb, sb)
            checked += 1
            cur = [apply_rule(r, w, ts, lex) for w, ts in zip(words_list, cur)]
    assert checked >= 10


def test_training_scores_are_error_reductions():
    rng = random.Random(7)
    tags = ["A", "B", "C"]
    vocab = ["p", "q", "r", "s", "t"]
    corpus = random_corpus(rng, tags, vocab, 8)
    lex, rules, scores = train(corpus)
    cur = [lex.initial(w) for w, _ in corpus]
    gold = [g for _, g in corpus]
    e = errors(cur, gold)
    for r, s in zip(rules, scores):
        cur = [apply_rule(r, w, ts, lex) for (w, _), ts in zip(corpus, cur)]
        e2 = errors(cur, gold)
        assert e - e2 == s >= 1
        e = e2
    assert rules
    assert [tag(w, lex, rules) for w, _ in corpus] == cur


def test_lexicon_rule_blocks_unseen_tags():
    corpus = [(["the", "dog"], ["D", "N"])]
    lex = Lexicon(corpus)
    rule = ("PREV1", ("D",), "N", "V")
    assert apply_rule(rule, ["the", "dog"], ["D", "N"], lex) == ["D", "N"]
    assert apply_rule(rule, ["the", "cat"], ["D", "N"], lex) == ["D", "V"]
    assert apply_rule(rule, ["the", "dog"], ["D", "N"]) == ["D", "V"]


def test_example_learns_nn_to_vb_after_to():
    lex, rules, scores = train(EXAMPLE)
    assert lex.initial(["race"]) == ["NN"]
    assert rules[0] == ("PREV1", ("TO",), "NN", "VB") and scores[0] == 2
    assert tag("they want to race".split(), lex, rules) == ["PRP", "VBP", "TO", "VB"]
    assert tag("the race".split(), lex, rules) == ["DT", "NN"]


def test_initial_annotator_and_errors():
    lex = Lexicon([(["a", "a", "b"], ["X", "Y", "Y"]), (["a"], ["Y"])], default="Z")
    assert lex.initial(["a", "b", "c"]) == ["Y", "Y", "Z"]
    with pytest.raises(ValueError):
        train(EXAMPLE, threshold=0)
    assert len(TEMPLATES) == 12
