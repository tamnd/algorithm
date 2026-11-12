# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hicuts/. The authors are listed in prov/RAB6MQ.jsonl.

import random

from hicuts import FIVE_TUPLE, HiCuts, linear_classify, random_classifier

# Table 1 of Gupta and McKeown (1999): two 8-bit fields X and Y.
PAPER = [
    ((0, 31), (0, 255)),
    ((0, 255), (128, 131)),
    ((64, 71), (128, 255)),
    ((67, 67), (0, 127)),
    ((64, 71), (0, 15)),
    ((128, 191), (4, 131)),
    ((192, 192), (0, 255)),
]


def leaves(tree):
    out, seen, stack = [], set(), [tree.root]
    while stack:
        v = stack.pop()
        if id(v) in seen:
            continue
        seen.add(id(v))
        if v.is_leaf():
            out.append(v)
        else:
            stack.extend(v.children)
    return out


def random_rule(rng, widths):
    rule = []
    for w in widths:
        if rng.random() < 0.3:
            rule.append((0, (1 << w) - 1))
        else:
            a, b = sorted((rng.randrange(1 << w), rng.randrange(1 << w)))
            rule.append((a, b))
    return tuple(rule)


def test_paper_example():
    h = HiCuts(PAPER, (8, 8), binth=2, spfac=4)
    h.check()
    assert h.root.dim == 0  # the root cuts X, as in the paper
    for x in range(256):
        for y in range(256):
            assert h.classify((x, y))[0] == linear_classify(PAPER, (x, y))
    # In X 0..31, R1 covers the whole box, so R2 is hidden there.
    assert h.classify((5, 130)) == (0, 2)


def test_random_2d_exhaustive():
    rng = random.Random(11)
    widths = (6, 6)
    for binth, spfac in [(1, 2), (2, 4), (4, 1), (4, 8)]:
        for _ in range(8):
            rules = [random_rule(rng, widths) for _ in range(rng.randint(1, 25))]
            h = HiCuts(rules, widths, binth=binth, spfac=spfac)
            h.check()
            for x in range(64):
                for y in range(64):
                    assert h.classify((x, y))[0] == linear_classify(rules, (x, y))


def test_random_five_fields():
    rng = random.Random(12)
    widths = (6, 6, 4, 4, 2)
    for _ in range(15):
        rules = [random_rule(rng, widths) for _ in range(rng.randint(5, 60))]
        h = HiCuts(rules, widths, binth=4, spfac=4)
        h.check()
        assert h.stats()["max_depth"] <= sum(widths)
        for _ in range(1500):
            packet = tuple(rng.randrange(1 << w) for w in widths)
            assert h.classify(packet)[0] == linear_classify(rules, packet)


def test_redundant_rules_are_dropped():
    rules = [((0, 127), (0, 255)), ((10, 20), (30, 40)), ((128, 255), (0, 9)), ((200, 210), (5, 6))]
    h = HiCuts(rules, (8, 8), binth=1, spfac=4)
    h.check()
    stored = {i for leaf in leaves(h) for i in leaf.rules}
    assert stored == {0, 2}  # rules 1 and 3 lie inside earlier rules


def test_synthetic_five_tuple():
    rng = random.Random(7)
    rules = random_classifier(rng, 300)
    h = HiCuts(rules, FIVE_TUPLE, binth=8, spfac=4)
    h.check()
    for leaf in leaves(h):
        assert len(leaf.rules) <= 8
    rng = random.Random(8)
    for _ in range(2000):
        rule = rules[rng.randrange(len(rules))]
        packet = tuple(rng.randint(lo, hi) for lo, hi in rule)
        assert h.classify(packet)[0] == linear_classify(rules, packet)
