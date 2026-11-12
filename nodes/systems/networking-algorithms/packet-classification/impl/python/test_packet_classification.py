# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packet-classification/. The authors are listed in prov/JDP7S8.jsonl.

import random
from functools import lru_cache

from packet_classification import (
    expand_rule,
    linear_classify,
    prefix_range,
    range_to_prefixes,
    ternary_classify,
    to_tcam,
)


def ip(a, b, c, d):
    return (a << 24) | (b << 16) | (c << 8) | d


def pfx(a, b, c, d, l):
    return prefix_range(ip(a, b, c, d) >> (32 - l), l, 32)


ANY32 = (0, (1 << 32) - 1)
ANY16 = (0, 65535)
ANY8 = (0, 255)
WIDTHS = (32, 32, 16, 16, 8)
TCP, UDP = (6, 6), (17, 17)

# The classifier of the page: source, destination, source port, destination port, protocol.
RULES = [
    (pfx(10, 0, 0, 0, 8), pfx(192, 168, 1, 0, 24), ANY16, (80, 80), TCP),
    (ANY32, pfx(192, 168, 1, 0, 24), ANY16, (0, 1023), ANY8),
    (pfx(10, 1, 0, 0, 16), ANY32, (1024, 65535), ANY16, UDP),
    (ANY32, ANY32, ANY16, ANY16, ANY8),
]


def test_page_example():
    packets = [
        ((ip(10, 2, 3, 4), ip(192, 168, 1, 5), 5555, 80, 6), 0),
        ((ip(10, 1, 2, 3), ip(192, 168, 1, 5), 5555, 53, 17), 1),
        ((ip(10, 1, 2, 3), ip(8, 8, 8, 8), 5555, 53, 17), 2),
        ((ip(172, 16, 0, 1), ip(192, 168, 1, 9), 40000, 8080, 6), 3),
    ]
    for packet, want in packets:
        assert linear_classify(RULES, packet) == want
    assert [len(expand_rule(r, WIDTHS)) for r in RULES] == [1, 1, 6, 1]
    assert range_to_prefixes(1024, 65535, 16) == [(1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1)]
    assert len(range_to_prefixes(1, 65534, 16)) == 30
    assert len(range_to_prefixes(0, 1023, 16)) == 1


@lru_cache(maxsize=None)
def min_cover(lo: int, hi: int, w: int) -> int:
    """Fewest disjoint aligned blocks with union [lo, hi], by dynamic programming."""
    if lo > hi:
        return 0
    best = None
    size = 1
    while lo % size == 0 and lo + size - 1 <= hi and size <= (1 << w):
        c = 1 + min_cover(lo + size, hi, w)
        best = c if best is None else min(best, c)
        size <<= 1
    return best


def test_range_expansion_exhaustive():
    for w in range(1, 9):
        worst, worst_ranges = 0, []
        for lo in range(1 << w):
            for hi in range(lo, 1 << w):
                ps = range_to_prefixes(lo, hi, w)
                covered = []
                for p, l in ps:
                    a, b = prefix_range(p, l, w)
                    covered.extend(range(a, b + 1))
                assert covered == list(range(lo, hi + 1))  # disjoint, in order, exact
                assert len(ps) == min_cover(lo, hi, w)  # the greedy is optimal
                if len(ps) > worst:
                    worst, worst_ranges = len(ps), [(lo, hi)]
                elif len(ps) == worst:
                    worst_ranges.append((lo, hi))
        assert worst == max(1, 2 * w - 2)
        if w >= 2:
            assert (1, (1 << w) - 2) in worst_ranges
        if w >= 3:
            assert worst_ranges == [(1, (1 << w) - 2)]


def test_tcam_matches_linear_search():
    rng = random.Random(3)
    widths = (6, 6, 5, 5, 2)
    for _ in range(30):
        rules = []
        for _ in range(rng.randint(1, 12)):
            rule = []
            for f, w in enumerate(widths):
                if f < 2:
                    l = rng.randint(0, w)
                    rule.append(prefix_range(rng.getrandbits(l) if l else 0, l, w))
                else:
                    a, b = sorted((rng.randrange(1 << w), rng.randrange(1 << w)))
                    rule.append((a, b) if rng.random() < 0.7 else (0, (1 << w) - 1))
            rules.append(tuple(rule))
        tcam = to_tcam(rules, widths)
        for _ in range(400):
            packet = tuple(rng.randrange(1 << w) for w in widths)
            want = linear_classify(rules, packet)
            assert ternary_classify(tcam, widths, packet) == want
            if want is not None:
                assert all(not all(lo <= x <= hi for (lo, hi), x in zip(r, packet)) for r in rules[:want])
