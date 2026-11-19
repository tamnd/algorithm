# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lesk-algorithm/. The authors are listed in prov/JX07Y6.jsonl.

import itertools
import random

from lesk_algorithm import (
    STOP_WORDS,
    Sense,
    all_pairs_lesk,
    gloss_pair_lesk,
    overlap_scores,
    signature,
    simplified_lesk,
)


def sense(name: str, gloss: str, examples: str = "") -> Sense:
    return Sense(name, tuple(gloss.split()), tuple(examples.split()))


BANK = [
    sense("bank.1", "a financial institution that accepts deposits and lends money", "she opened an account at the bank"),
    sense("bank.2", "sloping land beside a body of water", "they sat on the bank of the river and watched the boats"),
    sense("bank.3", "a row of similar objects", "a bank of switches"),
]
PINE = [
    sense("pine.1", "an evergreen tree with needle shaped leaves"),
    sense("pine.2", "to waste away from sorrow or longing"),
]
CONE = [
    sense("cone.1", "a solid body that narrows to a point from a round base"),
    sense("cone.2", "the woody fruit of an evergreen tree"),
    sense("cone.3", "a crisp wafer shaped to hold ice cream"),
]


def test_worked_example() -> None:
    c1 = "the fishermen pulled their boats onto the bank when the river rose".split()
    assert overlap_scores("bank", c1, BANK) == [0, 2, 0]
    assert simplified_lesk("bank", c1, BANK).name == "bank.2"
    c2 = "I went to the bank to deposit my money".split()
    assert overlap_scores("bank", c2, BANK) == [1, 0, 0]
    assert simplified_lesk("bank", c2, BANK).name == "bank.1"
    c3 = "the bank was closed".split()
    assert overlap_scores("bank", c3, BANK) == [0, 0, 0]
    assert simplified_lesk("bank", c3, BANK).name == "bank.1"
    c4 = "a body of water and a bank of switches".split()
    assert overlap_scores("bank", c4, BANK) == [0, 2, 1]
    assert simplified_lesk("bank", c4, BANK).name == "bank.2"


def test_pine_cone() -> None:
    a, b, k = gloss_pair_lesk(PINE, CONE)
    assert (a.name, b.name, k) == ("pine.1", "cone.2", 2)
    assert signature(a) & signature(b) == {"evergreen", "tree"}
    chosen, score = all_pairs_lesk({"pine": PINE, "cone": CONE}, ["pine", "cone"])
    assert chosen["pine"].name == "pine.1" and chosen["cone"].name == "cone.2" and score == 2


def test_edges() -> None:
    assert simplified_lesk("bank", [], BANK).name == "bank.1"
    assert simplified_lesk("bank", ["bank", "bank"], BANK).name == "bank.1"
    assert simplified_lesk("Bank", "RIVER Boats".split(), BANK).name == "bank.2"
    assert simplified_lesk("x", ["y"], [BANK[2]]).name == "bank.3"
    assert "the" not in signature(BANK[0]) and "money" in signature(BANK[0])
    assert signature(BANK[0], frozenset()) >= {"the", "a", "money"}
    for bad in ([],):
        try:
            simplified_lesk("x", ["y"], bad)
        except ValueError:
            pass
        else:
            raise AssertionError("no senses must fail")


def random_sense(rng: random.Random, name: str, vocab: list[str]) -> Sense:
    return Sense(name, tuple(rng.choice(vocab) for _ in range(rng.randrange(0, 6))),
                 tuple(rng.choice(vocab) for _ in range(rng.randrange(0, 3))))


def test_against_brute_force() -> None:
    rng = random.Random(11)
    vocab = ["w%d" % i for i in range(12)] + ["the", "of", "a"]
    for trial in range(600):
        senses = [random_sense(rng, "s%d" % i, vocab) for i in range(rng.randrange(1, 6))]
        context = [rng.choice(vocab) for _ in range(rng.randrange(0, 8))]
        target = rng.choice(vocab)
        ctx = set(context) - STOP_WORDS - {target}
        scores = [len((set(s.gloss) | set(s.examples)) - STOP_WORDS & ctx) for s in senses]
        top = max(scores)
        want = 0 if top == 0 else scores.index(top)
        assert simplified_lesk(target, context, senses) is senses[want]
        others = [random_sense(rng, "t%d" % i, vocab) for i in range(rng.randrange(1, 5))]
        best = max(
            itertools.product(range(len(senses)), range(len(others))),
            key=lambda ij: (len(signature(senses[ij[0]]) & signature(others[ij[1]])), -ij[0], -ij[1]),
        )
        a, b, k = gloss_pair_lesk(senses, others)
        assert (a, b) == (senses[best[0]], others[best[1]])
        assert k == len(signature(a) & signature(b))
        if trial % 3 == 0:
            chosen, score = all_pairs_lesk({"x": senses, "y": others}, ["x", "y"])
            assert score == k and (chosen["x"], chosen["y"]) == (a, b)
