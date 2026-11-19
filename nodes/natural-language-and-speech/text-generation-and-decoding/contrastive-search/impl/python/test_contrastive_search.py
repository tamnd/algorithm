# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrastive-search/. The authors are listed in prov/AYJ2SK.jsonl.

import math
import random

from contrastive_search import contrastive_search, contrastive_step, cosine, top_k_candidates
from nlslog import argmax


def random_model(seed, vocab, dim, scale=1.0):
    """A causal toy model: probs and states are fixed random functions of the prefix."""

    def vec(prefix):
        rng = random.Random(f"{seed}|state|{prefix}")
        return [scale * rng.uniform(-1, 1) for _ in range(dim)]

    def model(prefix):
        rng = random.Random(f"{seed}|probs|{prefix}")
        w = [rng.random() for _ in range(vocab)]
        s = math.fsum(w)
        return [x / s for x in w], [vec(prefix[: j + 1]) for j in range(len(prefix))]

    return model


def greedy(model, prompt, n):
    y = list(prompt)
    for _ in range(n):
        y.append(argmax(model(tuple(y))[0]))
    return y


def looping_model(prefix):
    """Every step gives a 0.5, b 0.3, c 0.15, </s> 0.05; the state of a token is its one-hot vector."""
    probs = [0.05, 0.5, 0.3, 0.15, 0.0]
    states = [[1.0 if d == t else 0.0 for d in range(5)] for t in prefix]
    return probs, states


def test_example_step() -> None:
    probs = [0.5, 0.3, 0.2]
    context = [(1.0, 0.0), (0.6, 0.8)]
    cand_states = [(1.0, 0.1), (0.0, 1.0), (-0.6, 0.8)]
    w, scores = contrastive_step(probs, cand_states, context, [0, 1, 2], 0.6)
    assert w == 2
    for got, want in zip(scores, (0.2 - 0.6 / math.sqrt(1.01), -0.36, -0.088)):
        assert abs(got - want) < 1e-12
    assert contrastive_step(probs, cand_states, context, [0, 1, 2], 0.3)[0] == 2
    assert contrastive_step(probs, cand_states, context, [0, 1, 2], 0.2)[0] == 0
    assert contrastive_step(probs, cand_states, context, [0, 1, 2], 0.0)[0] == 0


def test_alpha_zero_and_k_one_are_greedy() -> None:
    for seed in range(40):
        m = random_model(seed, 6, 4)
        g = greedy(m, [0], 6)
        assert contrastive_search(m, [0], 6, 4, 0.0) == g
        assert contrastive_search(m, [0], 6, 1, 0.7) == g


def test_scale_of_the_states_does_not_matter() -> None:
    for seed in range(40):
        a = contrastive_search(random_model(seed, 6, 4, 1.0), [0], 6, 3, 0.6)
        b = contrastive_search(random_model(seed, 6, 4, 7.5), [0], 6, 3, 0.6)
        assert a == b


def test_matches_a_direct_enumeration() -> None:
    rng = random.Random(1)
    for seed in range(40):
        m = random_model(seed, 7, 3)
        k = rng.randint(1, 7)
        alpha = rng.random()
        y = [0]
        out = contrastive_search(m, y, 5, k, alpha)
        for t in range(1, 6):
            prefix = tuple(out[:t])
            probs, context = m(prefix)
            best_v, best_s = None, None
            # the k most probable tokens, by a second method: a stable sort on -p
            for v in sorted(range(7), key=lambda i: -probs[i])[:k]:
                h = m(prefix + (v,))[1][-1]
                s = (1 - alpha) * probs[v] - alpha * max(cosine(h, c) for c in context)
                if best_s is None or s > best_s:
                    best_v, best_s = v, s
            assert out[t] == best_v


def test_breaks_the_loop_that_greedy_falls_into() -> None:
    prompt = [4]
    g = greedy(looping_model, prompt, 3)
    assert g == [4, 1, 1, 1]
    c = contrastive_search(looping_model, prompt, 3, 3, 0.6)
    assert c == [4, 1, 2, 3]
    # once every candidate has been used, the penalty is 1 for all, and probability decides
    assert contrastive_search(looping_model, prompt, 4, 3, 0.6)[-1] == 1


def test_alpha_one_picks_the_least_similar_candidate() -> None:
    probs = [0.6, 0.3, 0.1]
    context = [(1.0, 0.0)]
    cand_states = [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert contrastive_step(probs, cand_states, context, [0, 1, 2], 1.0)[0] == 2


def test_helpers() -> None:
    assert cosine((0.0, 0.0), (1.0, 2.0)) == 0.0
    assert abs(cosine((1.0, 2.0), (2.0, 4.0)) - 1.0) < 1e-12
    assert top_k_candidates([0.2, 0.4, 0.4], 2) == [1, 2]
    # an empty context gives no penalty: the first step from an empty prompt is greedy
    m = random_model(3, 5, 2)
    assert contrastive_search(m, [], 1, 5, 0.9) == [argmax(m(())[0])]
    for bad in (lambda: top_k_candidates([1.0], 0), lambda: contrastive_step([1.0], [(1.0,)], [], [0], 1.5)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError")


def test_stops_at_the_end_token() -> None:
    def model(prefix):
        probs = [0.9, 0.1] if len(prefix) >= 2 else [0.1, 0.9]
        return probs, [[1.0, float(j)] for j in range(len(prefix))]

    out = contrastive_search(model, [1], 10, 2, 0.0, eos=0)
    assert out == [1, 1, 0]
