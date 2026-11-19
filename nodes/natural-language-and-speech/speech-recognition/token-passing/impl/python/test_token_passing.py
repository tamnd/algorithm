# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/token-passing/. The authors are listed in prov/CTEH7D.jsonl.

import itertools
import math
import random

from nlslog import NEG_INF
from token_passing import Network, bigram_network, decode

PHONES = ["p", "q", "r"]
LOG_HALF = math.log(0.5)


def compositions(total: int, parts: int):
    for cuts in itertools.combinations(range(1, total), parts - 1):
        bounds = (0,) + cuts + (total,)
        yield tuple(bounds[i + 1] - bounds[i] for i in range(parts))


def path_score(net, lexicon, emit, arcs, durations, lm_weight, ip):
    phones = [ph for a in arcs for ph in lexicon[net.arcs[a][2]]]
    score, t = 0.0, 0
    for ph, d in zip(phones, durations):
        score += sum(emit[t + i][ph] for i in range(d)) + (d - 1) * LOG_HALF + LOG_HALF
        t += d
    for a in arcs:
        score += lm_weight * net.arcs[a][3] + ip
    return score + lm_weight * net.final[net.arcs[arcs[-1]][1]]


def brute_force(net, lexicon, emit, lm_weight=1.0, ip=0.0):
    """Best score over all arc paths from the start to a final node with at most 5 words."""
    T = len(emit)
    best = NEG_INF
    paths = [[a] for a, arc in enumerate(net.arcs) if arc[0] == net.start]
    while paths:
        longer = []
        for path in paths:
            phones = sum(len(lexicon[net.arcs[a][2]]) for a in path)
            if phones > T:
                continue
            if net.arcs[path[-1]][1] in net.final:
                for d in compositions(T, phones):
                    best = max(best, path_score(net, lexicon, emit, path, d, lm_weight, ip))
            if len(path) < 5:
                longer += [path + [a] for a, arc in enumerate(net.arcs) if arc[0] == net.arcs[path[-1]][1]]
        paths = longer
    return best


def random_lexicon(rng: random.Random):
    return {w: tuple(rng.choice(PHONES) for _ in range(rng.randint(1, 2))) for w in ["A", "B", "C"]}


def random_network(rng: random.Random, lexicon) -> Network:
    net = Network()
    for _ in range(3):
        net.add_node()
    for _ in range(rng.randint(2, 7)):
        net.add_word(rng.randrange(3), rng.randrange(3), rng.choice(sorted(lexicon)), math.log(rng.uniform(0.1, 1.0)))
    for q in rng.sample(range(3), rng.randint(1, 3)):
        net.set_final(q, math.log(rng.uniform(0.1, 1.0)))
    return net


def random_emit(rng: random.Random, T: int):
    return [{ph: -rng.uniform(0.0, 4.0) for ph in PHONES} for _ in range(T)]


def test_random_networks_match_brute_force():
    rng = random.Random(21)
    for _ in range(80):
        lexicon = random_lexicon(rng)
        net = random_network(rng, lexicon)
        T = rng.randint(1, 5)
        emit = random_emit(rng, T)
        kw = {"lm_weight": rng.choice([0.5, 1.0, 2.0]), "ip": rng.choice([-1.0, 0.0, 0.5])}
        words, ends, score = decode(net, lexicon, emit, **kw)
        expected = brute_force(net, lexicon, emit, **kw)
        if expected == NEG_INF:
            assert (words, ends, score) == ([], [], NEG_INF)
            continue
        assert abs(score - expected) < 1e-9
        assert ends[-1] == T - 1
        assert all(a < b for a, b in zip(ends, ends[1:]))


def test_bigram_network():
    rng = random.Random(22)
    for _ in range(30):
        lexicon = random_lexicon(rng)
        vocab = sorted(lexicon)
        lm = {}
        for v in ["<s>"] + vocab:
            probs = [rng.random() + 0.1 for _ in range(len(vocab) + 1)]
            z = sum(probs)
            for w, p in zip(vocab + ["</s>"], probs):
                lm[(v, w)] = math.log(p / z)
        net = bigram_network(vocab, lm)
        assert len(net.arcs) == len(vocab) * (len(vocab) + 1)
        emit = random_emit(rng, 5)
        words, _, score = decode(net, lexicon, emit)
        assert abs(score - brute_force(net, lexicon, emit)) < 1e-9
        # The words returned score the same under the bigram written out by hand.
        prev, lm_part = "<s>", 0.0
        for w in words + ["</s>"]:
            lm_part += lm[(prev, w)]
            prev = w
        n = sum(len(lexicon[w]) for w in words)
        assert n <= 5 and lm_part > NEG_INF


def test_pruning_never_improves():
    rng = random.Random(23)
    for _ in range(40):
        lexicon = random_lexicon(rng)
        net = random_network(rng, lexicon)
        emit = random_emit(rng, 5)
        full = decode(net, lexicon, emit)[2]
        for beam in [0.0, 0.5, 2.0, 1e9]:
            score = decode(net, lexicon, emit, beam=beam)[2]
            assert score <= full + 1e-12
        assert decode(net, lexicon, emit, beam=1e9) == decode(net, lexicon, emit)


def test_narrow_beam_misses_the_best_path():
    lexicon = {"AB": ("a", "b"), "CD": ("c", "d")}
    net = Network()
    s, f = net.add_node(), net.add_node()
    net.add_word(s, f, "AB", 0.0)
    net.add_word(s, f, "CD", 0.0)
    net.set_final(f, 0.0)
    emit = [{"a": -1.0, "b": -9.0, "c": -2.0, "d": -9.0}, {"a": -9.0, "b": -5.0, "c": -9.0, "d": -1.0}]
    assert decode(net, lexicon, emit) == (["CD"], [1], -3.0 + 2 * LOG_HALF)
    assert decode(net, lexicon, emit, beam=0.5) == (["AB"], [1], -6.0 + 2 * LOG_HALF)
    assert decode(net, lexicon, emit, beam=1.0) == (["CD"], [1], -3.0 + 2 * LOG_HALF)


def test_tokens_carry_word_history():
    lexicon = {"one": ("p",), "two": ("q", "r")}
    net = Network()
    a, b, c = net.add_node(), net.add_node(), net.add_node()
    net.add_word(a, b, "one", 0.0)
    net.add_word(b, b, "two", math.log(0.5))
    net.add_word(b, c, "one", 0.0)
    net.set_final(c, 0.0)
    emit = [{x: (0.0 if x == ph else -5.0) for x in "pqr"} for ph in "pqrqrp"]
    words, ends, score = decode(net, lexicon, emit)
    assert words == ["one", "two", "two", "one"] and ends == [0, 2, 4, 5]
    assert abs(score - (2 * math.log(0.5) + 6 * LOG_HALF)) < 1e-12
