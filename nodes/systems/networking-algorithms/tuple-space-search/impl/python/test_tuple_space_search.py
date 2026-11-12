# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tuple-space-search/. The authors are listed in prov/DFBVFN.jsonl.

import itertools
import random

from tuple_space_search import (
    FIVE_TUPLE,
    TupleSpace,
    linear_classify,
    random_prefix_classifier,
)


def bits(s: str):
    """'10*' -> (2, 2): a prefix from its bit string."""
    s = s.rstrip("*")
    return (int(s, 2) if s else 0), len(s)


# The example of the page: two 4-bit fields, priority = rule number.
PAGE = [
    (1, (bits("10*"), bits("0*")), 1),
    (2, (bits("1*"), bits("01*")), 2),
    (3, (bits("101*"), bits("*")), 3),
    (4, (bits("11*"), bits("1*")), 4),
    (5, (bits("*"), bits("0110")), 5),
    (6, (bits("*"), bits("*")), 6),
]


def build(rules, widths):
    ts = TupleSpace(widths)
    for rid, prefixes, prio in rules:
        ts.insert(rid, prefixes, prio)
    return ts


def test_page_example():
    ts = build(PAGE, (4, 4))
    assert sorted(ts.tuples()) == [(0, 0), (0, 4), (1, 2), (2, 1), (3, 0)]
    assert ts.lookup((0b1011, 0b0110)) == (1, 5)
    assert ts.lookup((0b1100, 0b1001)) == (4, 5)
    assert ts.lookup_sorted((0b1011, 0b0110)) == (1, 1)
    assert ts.lookup_sorted((0b1100, 0b1001)) == (4, 3)
    assert ts.candidate_tuples((0b1100, 0b1001)) == {(0, 0), (2, 1)}
    assert ts.lookup_pruned((0b1100, 0b1001)) == (4, 2)
    for x in itertools.product(range(16), repeat=2):
        want = linear_classify(PAGE, x, (4, 4))
        assert ts.lookup(x)[0] == ts.lookup_sorted(x)[0] == ts.lookup_pruned(x)[0] == want


def random_rule(rng, widths):
    out = []
    for w in widths:
        l = rng.randint(0, w)
        out.append((rng.getrandbits(l) if l else 0, l))
    return tuple(out)


def test_exhaustive_with_updates():
    rng = random.Random(21)
    widths = (5, 4, 3)
    packets = list(itertools.product(*(range(1 << w) for w in widths)))
    for _ in range(6):
        ts = TupleSpace(widths)
        live = {}
        next_id = 0
        for step in range(120):
            if live and rng.random() < 0.35:
                rid = rng.choice(list(live))
                assert ts.delete(rid)
                del live[rid]
                assert not ts.delete(rid)
            else:
                prefixes, prio = random_rule(rng, widths), rng.randrange(40)
                ts.insert(next_id, prefixes, prio)
                live[next_id] = (prefixes, prio)
                next_id += 1
            if step % 20 == 19:
                rules = [(rid, p, pr) for rid, (p, pr) in live.items()]
                n_tuples = len({tuple(l for _, l in p) for _, p, _ in rules})
                assert len(ts.tuples()) == n_tuples  # empty tuples are dropped
                for x in packets:
                    want = linear_classify(rules, x, widths)
                    got, probes = ts.lookup(x)
                    assert got == want and probes == n_tuples
                    got_s, probes_s = ts.lookup_sorted(x)
                    got_p, probes_p = ts.lookup_pruned(x)
                    assert got_s == want and probes_s <= n_tuples
                    assert got_p == want and probes_p <= n_tuples


def test_synthetic_five_tuple():
    rng = random.Random(7)
    rules = random_prefix_classifier(rng, 400)
    ts = build(rules, FIVE_TUPLE)
    assert len(ts) == 400
    rng = random.Random(8)
    for _ in range(1500):
        _, prefixes, _ = rules[rng.randrange(len(rules))]
        x = tuple((p << (w - l)) | rng.getrandbits(w - l) if l < w else p for (p, l), w in zip(prefixes, FIVE_TUPLE))
        want = linear_classify(rules, x, FIVE_TUPLE)
        assert ts.lookup(x)[0] == want
        assert ts.lookup_sorted(x)[0] == want
        assert ts.lookup_pruned(x)[0] == want
