# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-synchronous-beam-search/. The authors are listed in prov/6JVTAP.jsonl.

import itertools
import math
import random

from nlslog import NEG_INF
from time_synchronous_beam_search import BOS, EOS, PrefixTree, decode, path_score

PHONES = ["p", "q", "r"]


def compositions(total: int, parts: int):
    """Yield every tuple of `parts` positive integers that add up to `total`."""
    for cuts in itertools.combinations(range(1, total), parts - 1):
        bounds = (0,) + cuts + (total,)
        yield tuple(bounds[i + 1] - bounds[i] for i in range(parts))


def brute_force(lexicon, lm, emit, **kw):
    T = len(emit)
    best = NEG_INF
    for k in range(1, min(T, 5) + 1):
        for words in itertools.product(sorted(lexicon), repeat=k):
            n = sum(len(lexicon[w]) for w in words)
            if n > T:
                continue
            for dur in compositions(T, n):
                best = max(best, path_score(lexicon, lm, emit, words, dur, **kw))
    return best


def random_task(rng: random.Random, T: int):
    lexicon = {}
    for w in ["A", "B", "C"]:
        lexicon[w] = tuple(rng.choice(PHONES) for _ in range(rng.randint(1, 2)))
    vocab = sorted(lexicon)
    lm = {}
    for v in [BOS] + vocab:
        probs = [rng.random() + 0.1 for _ in range(len(vocab) + 1)]
        z = sum(probs)
        for w, p in zip(vocab + [EOS], probs):
            lm[(v, w)] = math.log(p / z)
    emit = [{ph: -rng.uniform(0.0, 4.0) for ph in PHONES} for _ in range(T)]
    return lexicon, lm, emit


def test_prefix_tree_shares_prefixes():
    tree = PrefixTree({"cat": ("k", "a", "t"), "cap": ("k", "a", "p"), "a": ("a",), "kay": ("k", "a")})
    assert tree.num_nodes() == 6
    assert len(tree.children[0]) == 2
    assert sorted(w for ws in tree.words for w in ws) == ["a", "cap", "cat", "kay"]


def test_wide_beam_matches_brute_force():
    rng = random.Random(11)
    for _ in range(60):
        T = rng.randint(1, 5)
        lexicon, lm, emit = random_task(rng, T)
        kw = {"lm_weight": rng.choice([0.5, 1.0, 2.0]), "ip": rng.choice([-1.0, 0.0, 0.5])}
        words, ends, score = decode(lexicon, lm, emit, **kw)
        expected = brute_force(lexicon, lm, emit, **kw)
        if expected == NEG_INF:
            assert (words, ends, score) == ([], [], NEG_INF)
            continue
        assert abs(score - expected) < 1e-9
        assert ends[-1] == T - 1
        assert all(a < b for a, b in zip(ends, ends[1:]))
        n = sum(len(lexicon[w]) for w in words)
        rescored = max(path_score(lexicon, lm, emit, words, d, **kw) for d in compositions(T, n))
        assert abs(rescored - score) < 1e-9


def test_large_histogram_limit_changes_nothing():
    rng = random.Random(12)
    for _ in range(30):
        lexicon, lm, emit = random_task(rng, 5)
        assert decode(lexicon, lm, emit) == decode(lexicon, lm, emit, beam=1e9, max_active=10 ** 6)


def test_pruned_score_is_never_better():
    rng = random.Random(13)
    for _ in range(40):
        lexicon, lm, emit = random_task(rng, 5)
        full = decode(lexicon, lm, emit)[2]
        for beam in [0.0, 0.5, 2.0]:
            for max_active in [1, 2, None]:
                words, _, score = decode(lexicon, lm, emit, beam=beam, max_active=max_active)
                assert score <= full + 1e-12
                if words:
                    assert score > NEG_INF


def test_narrow_beam_misses_the_best_path():
    lexicon = {"AB": ("a", "b"), "CD": ("c", "d")}
    lm = {(BOS, "AB"): 0.0, (BOS, "CD"): 0.0, ("AB", EOS): 0.0, ("CD", EOS): 0.0}
    emit = [{"a": -1.0, "b": -9.0, "c": -2.0, "d": -9.0}, {"a": -9.0, "b": -5.0, "c": -9.0, "d": -1.0}]
    fwd = math.log(0.5)
    assert decode(lexicon, lm, emit) == (["CD"], [1], -3.0 + 2 * fwd)
    assert decode(lexicon, lm, emit, beam=0.5) == (["AB"], [1], -6.0 + 2 * fwd)
    assert decode(lexicon, lm, emit, max_active=1) == (["AB"], [1], -6.0 + 2 * fwd)
    assert decode(lexicon, lm, emit, beam=1.0) == (["CD"], [1], -3.0 + 2 * fwd)


def test_bigram_context_is_kept_per_tree_copy():
    # After "x" the word "y" is cheap, after "z" it is expensive. Both "x" and "z" are one frame of
    # the same phone, so only a search that keeps one tree copy per previous word finds x y.
    lexicon = {"x": ("p",), "z": ("p",), "y": ("q",)}
    lm = {(BOS, "x"): math.log(0.4), (BOS, "z"): math.log(0.6), ("x", "y"): 0.0, ("z", "y"): math.log(0.01),
          ("y", EOS): 0.0}
    emit = [{"p": 0.0, "q": -9.0}, {"p": -9.0, "q": 0.0}]
    words, ends, score = decode(lexicon, lm, emit)
    assert words == ["x", "y"] and ends == [0, 1]
    assert abs(score - (math.log(0.4) + 2 * math.log(0.5))) < 1e-12


def test_no_complete_path():
    lexicon = {"AB": ("a", "b")}
    lm = {(BOS, "AB"): 0.0, ("AB", EOS): 0.0}
    emit = [{"a": 0.0, "b": 0.0}]
    assert decode(lexicon, lm, emit) == ([], [], NEG_INF)
