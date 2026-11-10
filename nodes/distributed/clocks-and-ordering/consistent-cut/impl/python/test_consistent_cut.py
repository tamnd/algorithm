# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-cut/. The authors are listed in prov/5MWFYB.jsonl.

import random

from consistent_cut import (
    all_cuts,
    consistent_cuts,
    is_consistent,
    is_consistent_frontier,
    is_consistent_vc,
    join,
    meet,
    pairwise_concurrent_frontier,
    random_computation,
    vector_clocks,
)

# The page example: p0 sends m0 to p1, p1 receives it, p1 sends m1 to p2.
EXAMPLE = [
    [("int",), ("send", 0, 1)],
    [("recv", 0, 0), ("send", 1, 2)],
    [("int",), ("recv", 1, 1)],
]


def test_page_example() -> None:
    vc = vector_clocks(EXAMPLE)
    assert vc[1][1] == (2, 2, 0) and vc[2][1] == (2, 2, 2)
    assert is_consistent_vc(vc, (2, 1, 1))
    assert not is_consistent_vc(vc, (1, 1, 1))  # recv of m0 without its send
    assert not is_consistent_vc(vc, (2, 1, 2))  # recv of m1 without its send
    assert len(consistent_cuts(EXAMPLE)) == 11  # of 27 cuts


def test_three_tests_agree_with_definition() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        comp = random_computation(rng.randrange(2, 5), rng.randrange(4, 14), rng)
        vc = vector_clocks(comp)
        for cut in all_cuts(comp):
            want = is_consistent(comp, cut)
            assert is_consistent_vc(vc, cut) == want
            assert is_consistent_frontier(comp, vc, cut) == want
            if pairwise_concurrent_frontier(vc, cut):
                assert want  # sufficient, not necessary


def test_pairwise_concurrency_is_not_necessary() -> None:
    # The cut that holds a send and its receive is consistent, but its frontier
    # events are ordered.
    comp = [[("send", 0, 1)], [("recv", 0, 0)]]
    vc = vector_clocks(comp)
    assert is_consistent(comp, (1, 1))
    assert not pairwise_concurrent_frontier(vc, (1, 1))


def test_consistent_cuts_form_a_lattice() -> None:
    for seed in range(40):
        rng = random.Random(100 + seed)
        comp = random_computation(rng.randrange(2, 5), rng.randrange(4, 12), rng)
        cc = set(consistent_cuts(comp))
        n = len(comp)
        assert tuple([0] * n) in cc and tuple(len(p) for p in comp) in cc
        for a in cc:
            for b in cc:
                assert join(a, b) in cc and meet(a, b) in cc
