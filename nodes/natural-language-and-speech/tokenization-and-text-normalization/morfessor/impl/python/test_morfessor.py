# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morfessor/. The authors are listed in prov/TM8W3C.jsonl.

import itertools
import math
import random

from morfessor import K_DEFAULT, Model, cost_of, lexicon_of, morfessor, resplit, segment

PAGE = {"walk": 4, "walked": 3, "walking": 3, "talk": 3, "talked": 2, "talking": 2,
        "jump": 3, "jumped": 2, "jumping": 2}


def splits(w):
    for mask in range(1 << (len(w) - 1)):
        out, last = [], 0
        for i in range(1, len(w)):
            if mask >> (i - 1) & 1:
                out.append(w[last:i])
                last = i
        out.append(w[last:])
        yield out


def brute_force(corpus, k):
    words = sorted(corpus)
    return min(cost_of(corpus, dict(zip(words, combo)), k)
               for combo in itertools.product(*[list(splits(w)) for w in words]))


def random_corpus(rng):
    return {"".join(rng.choice("ab") for _ in range(rng.randint(2, 5))): rng.randint(1, 30)
            for _ in range(rng.randint(2, 4))}


def test_cost_formula():
    # 2 tokens of "ab" and 1 of "c": data cost 3 ln 3 - 2 ln 2, lexicon 3 characters.
    corpus = {"ab": 2, "c": 1}
    want = 3 * math.log(3) - 2 * math.log(2) + 3 * K_DEFAULT
    assert abs(cost_of(corpus, {"ab": ["ab"], "c": ["c"]}) - want) < 1e-12
    assert abs(K_DEFAULT - 5 * math.log(2)) < 1e-15


def test_page_example():
    analysis, trace = morfessor(PAGE, random.Random(0))
    assert {w: "+".join(a) for w, a in analysis.items()} == {
        "walk": "walk", "walked": "walk+ed", "walking": "walk+ing", "talk": "talk", "talked": "talk+ed",
        "talking": "talk+ing", "jump": "jump", "jumped": "jump+ed", "jumping": "jump+ing"}
    assert [round(c, 3) for c in trace] == [228.752, 119.634, 119.634]
    assert lexicon_of(PAGE, analysis) == {"walk": 10, "ed": 7, "ing": 7, "talk": 7, "jump": 7}
    lex = lexicon_of(PAGE, analysis)
    assert segment("talked", lex) == ["talk", "ed"]
    assert segment("walkjump", lex) == ["walk", "jump"]
    assert segment("jumps", lex) == ["jumps"]


def test_first_split_of_walked():
    model = Model()
    for w, f in PAGE.items():
        model.add(w, f)
    model.add("walked", -3)
    whole = model.cost_with(["walked"], 3)
    cuts = {i: model.cost_with(["walked"[:i], "walked"[i:]], 3) for i in range(1, 6)}
    assert round(whole, 3) == 228.752 and round(cuts[4], 3) == 219.527
    assert min(cuts, key=cuts.get) == 4 and all(round(c, 3) == 238.171 for i, c in cuts.items() if i != 4)


def test_analyses_concatenate_and_counts_stay_consistent():
    rng = random.Random(3)
    for _ in range(40):
        corpus = random_corpus(rng)
        analysis, trace = morfessor(corpus, random.Random(rng.randint(0, 99)), k=rng.choice([1.0, K_DEFAULT]))
        assert all("".join(a) == w for w, a in analysis.items())
        assert all(b <= a + 1e-9 for a, b in zip(trace, trace[1:]))


def test_the_cost_never_rises_on_any_reprocessing():
    rng = random.Random(4)
    for _ in range(40):
        corpus = random_corpus(rng)
        start = {w: rng.choice(list(splits(w))) for w in corpus}
        before = cost_of(corpus, start)
        analysis, trace = morfessor(corpus, random.Random(1), start=start)
        assert abs(trace[0] - before) < 1e-9 and trace[-1] <= before + 1e-9


def test_resplit_keeps_the_model_counts_right():
    rng = random.Random(5)
    for _ in range(30):
        corpus = random_corpus(rng)
        model = Model(1.0)
        analysis = {}
        for w, f in corpus.items():
            analysis[w] = resplit(model, w, f)
        assert model.counts == lexicon_of(corpus, analysis)
        assert abs(model.cost() - cost_of(corpus, analysis, 1.0)) < 1e-9


def test_local_optimum_against_brute_force():
    corpus = {"bb": 11, "bbbb": 9}
    analysis, trace = morfessor(corpus, random.Random(0))
    assert analysis == {"bb": ["bb"], "bbbb": ["bb", "bb"]}
    assert abs(trace[-1] - 2 * K_DEFAULT) < 1e-9
    assert abs(brute_force(corpus, K_DEFAULT) - K_DEFAULT) < 1e-9  # every word as single b's
    firsts = set()
    for seed in range(10):
        order = sorted(corpus)
        random.Random(seed).shuffle(order)
        firsts.add(order[0])
        assert morfessor(corpus, random.Random(seed))[0] == analysis
    assert firsts == {"bb", "bbbb"}  # both orders were tried
    rng = random.Random(6)
    for _ in range(25):
        corpus = random_corpus(rng)
        _, trace = morfessor(corpus, random.Random(0), k=1.0)
        assert trace[-1] >= brute_force(corpus, 1.0) - 1e-9


def test_log_space_avoids_underflow():
    # 2000 tokens of a morph of probability 1/2: the product underflows, the cost does not.
    corpus = {"ab": 1000, "cd": 1000}
    product = 1.0
    for _ in range(2000):
        product *= 0.5
    assert product == 0.0
    c = cost_of(corpus, {"ab": ["ab"], "cd": ["cd"]})
    assert abs(c - (2000 * math.log(2) + 4 * K_DEFAULT)) < 1e-9
