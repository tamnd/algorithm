# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-mixing/. The authors are listed in prov/S2R9ZZ.jsonl.

import math
import random

from context_mixing import LagModel, Mixer, mixed_length, segmented_source, single_length, squash, stretch

CONTEXTS = [(), (1,), (1, 2, 3), (8,), tuple(range(1, 9))]


def test_stretch_and_squash() -> None:
    for p in (0.001, 0.1, 0.5, 0.77, 0.999):
        assert abs(squash(stretch(p)) - p) < 1e-12
    assert squash(0) == 0.5
    assert squash(-800) == 0.0 and squash(800) == 1.0


def test_one_model_with_fixed_weight_is_that_model() -> None:
    rng = random.Random(4)
    bits = [int(rng.random() < 0.2) for _ in range(2000)]
    model, mixer = LagModel((1, 2)), Mixer(1, lr=0.0, w0=1.0)
    total = 0.0
    for y in bits:
        p = mixer.mix([model.predict()])
        total -= math.log2(p if y else 1 - p)
        mixer.update(y)
        model.update(y)
    assert abs(total - single_length(bits, (1, 2))) < 1e-6


def test_mixture_beats_every_single_model_on_segmented_data() -> None:
    for seed in (1, 2, 3):
        bits = segmented_source(seed)
        singles = [single_length(bits, c) for c in CONTEXTS]
        mixed = mixed_length(bits, CONTEXTS)
        assert mixed < 0.9 * min(singles)
        # Without the order-8 model, no single model is good everywhere, but the mixture is.
        assert mixed_length(bits, CONTEXTS[:4]) < 0.75 * min(singles[:4])


def test_mixture_is_never_much_worse_than_the_best_model() -> None:
    rng = random.Random(2005)
    n = 12000
    sources = {
        "iid": [int(rng.random() < 0.1) for _ in range(n)],
        "random": [rng.randint(0, 1) for _ in range(n)],
    }
    chain = [0]
    for _ in range(n - 1):
        chain.append(int(rng.random() < (0.2 if chain[-1] else 0.85)))
    sources["order1"] = chain
    for name, bits in sources.items():
        best = min(single_length(bits, c) for c in CONTEXTS)
        assert mixed_length(bits, CONTEXTS) <= best + 0.02 * n, name
