# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-implementation/. The authors are listed in prov/2V6QRX.jsonl.

import itertools
import random
from collections import Counter

from threshold_implementation import component_inputs, masked_and, sharings, ti_and, two_share_and

BITS = list(itertools.product((0, 1), repeat=2))
RANDS = list(itertools.product((0, 1), repeat=2))


def xor(s):
    return sum(s) % 2


def test_sharings() -> None:
    for v in (0, 1):
        s = sharings(v, 3)
        assert len(s) == 4 and all(xor(t) == v for t in s)


def test_correct_for_all_sharings() -> None:
    for x, y in BITS:
        for xs in sharings(x, 3):
            for ys in sharings(y, 3):
                assert xor(ti_and(xs, ys)) == x & y
                for r in RANDS:
                    assert xor(ti_and(xs, ys, r)) == x & y


def test_non_completeness() -> None:
    # Output share i does not change when share i of both inputs changes.
    for xs in itertools.product((0, 1), repeat=3):
        for ys in itertools.product((0, 1), repeat=3):
            z = ti_and(xs, ys)
            for i in range(3):
                for fx, fy in BITS:
                    xs2 = tuple(v ^ (fx if j == i else 0) for j, v in enumerate(xs))
                    ys2 = tuple(v ^ (fy if j == i else 0) for j, v in enumerate(ys))
                    assert ti_and(xs2, ys2)[i] == z[i]


def glitch_views(component, rands):
    """For each secret pair, the distribution of what one extended probe sees."""
    return {
        (x, y): Counter(
            component_inputs(xs, ys, r)[component]
            for xs in sharings(x, 3)
            for ys in sharings(y, 3)
            for r in rands
        )
        for x, y in BITS
    }


def test_glitch_extended_probe_is_secure() -> None:
    for rands in ([None], RANDS):
        for i in range(3):
            views = glitch_views(i, rands)
            first = views[(0, 0)]
            assert all(v == first for v in views.values())


def test_two_share_and_leaks_with_glitches() -> None:
    views = {}
    for a, b in BITS:
        outs = Counter()
        seen = Counter()
        for a_s in sharings(a, 2):
            for b_s in sharings(b, 2):
                for r in (0, 1):
                    c, comps = two_share_and(a_s, b_s, r)
                    assert xor(c) == a & b
                    outs[c[0]] += 1
                    seen[comps[0]] += 1
        assert outs == Counter({0: 4, 1: 4})  # each output share alone is uniform
        views[(a, b)] = seen
    # The inputs of one component give b = b1 xor b2.
    assert views[(0, 0)] != views[(0, 1)]


def output_counts(x, y, rands):
    return Counter(
        ti_and(xs, ys, r) for xs in sharings(x, 3) for ys in sharings(y, 3) for r in rands
    )


def test_output_is_not_uniform_without_fresh_bits() -> None:
    for x, y in BITS[:3]:
        assert output_counts(x, y, [None]) == Counter(
            {(0, 0, 0): 7, (0, 1, 1): 3, (1, 0, 1): 3, (1, 1, 0): 3}
        )
    assert output_counts(1, 1, [None]) == Counter(
        {(0, 0, 1): 5, (0, 1, 0): 5, (1, 0, 0): 5, (1, 1, 1): 1}
    )


def test_non_uniform_output_leaks_in_the_next_stage() -> None:
    # A next component that reads output shares 1 and 2 sees different laws for x AND y = 0 and 1.
    def pair_law(x, y, rands):
        return Counter(z[:2] for z, n in output_counts(x, y, rands).items() for _ in range(n))

    assert pair_law(0, 0, [None]) != pair_law(1, 1, [None])
    assert pair_law(0, 0, RANDS) == pair_law(1, 1, RANDS) == Counter(
        {(0, 0): 16, (0, 1): 16, (1, 0): 16, (1, 1): 16}
    )


def test_fresh_bits_make_the_output_uniform() -> None:
    for x, y in BITS:
        counts = output_counts(x, y, RANDS)
        assert counts == Counter({s: 16 for s in sharings(x & y, 3)})


def test_random_oracle() -> None:
    rng = random.Random(20240509)
    for _ in range(1000):
        x, y = rng.randrange(2), rng.randrange(2)
        assert xor(masked_and(rng, x, y)) == x & y
