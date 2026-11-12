# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-inverse-folding/. The authors are listed in prov/C0K6PX.jsonl.

import itertools
import random

from rna_inverse_folding import (PAIRS, adaptive_walk, cost, exact_designs, fold_count, is_design,
                                 parse_dot_bracket, to_dot_bracket)

M = 3


def subset_structures(n, m=M):
    """All sets of position pairs with the hairpin minimum, no shared base and no crossing,
    by brute force over all subsets of the candidate pairs. Used for n <= 9."""
    cand = [(i, j) for i in range(n) for j in range(i + m + 1, n)]
    out = []
    for r in range(n // 2 + 1):
        for sub in itertools.combinations(cand, r):
            used = [x for p in sub for x in p]
            if len(used) != len(set(used)):
                continue
            if any(i < k < j < l for (i, j) in sub for (k, l) in sub):
                continue
            out.append(tuple(sorted(sub)))
    return out


_CACHE = {}


def position_structures(n, m=M):
    """The same sets, built from shorter lengths: the last base is unpaired, or pairs with k."""
    if n not in _CACHE:
        if n <= m + 1:
            out = [()]
        else:
            out = list(position_structures(n - 1, m))
            for k in range(n - 1 - m):
                for left in position_structures(k, m):
                    for inner in position_structures(n - 2 - k, m):
                        shifted = tuple((i + k + 1, j + k + 1) for i, j in inner)
                        out.append(tuple(sorted(left + shifted + ((k, n - 1),))))
        _CACHE[n] = out
    return _CACHE[n]


def brute_optima(s, structs):
    ok = [p for p in structs if all((s[i], s[j]) in PAIRS for i, j in p)]
    best = max(len(p) for p in ok)
    return best, [p for p in ok if len(p) == best]


def brute_designs(n):
    """For each target, the set of all sequences of length n whose unique optimum it is."""
    structs = position_structures(n)
    out = {p: set() for p in structs}
    for seq in itertools.product("ACGU", repeat=n):
        s = "".join(seq)
        _, opt = brute_optima(s, structs)
        if len(opt) == 1:
            out[opt[0]].add(s)
    return out


def test_structure_lists_agree():
    for n in range(0, 10):
        built = position_structures(n)
        assert len(built) == len(set(built))
        assert set(built) == set(subset_structures(n))


def test_fold_count_matches_enumeration():
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randrange(0, 13)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        best, opt = brute_optima(s, position_structures(n))
        assert fold_count(s) == (best, len(opt))


def test_parse_dot_bracket():
    assert parse_dot_bracket("((...))..") == [(0, 6), (1, 5)]
    assert to_dot_bracket(9, [(0, 6), (1, 5)]) == "((...)).."


def test_exact_solver_equals_brute_force_up_to_7():
    for n in range(0, 8):
        truth = brute_designs(n)
        for target, designs in truth.items():
            assert set(exact_designs(n, list(target))) == designs
            for s in list(designs)[:20]:
                assert cost(s, list(target)) == 0


def test_designability_at_length_8():
    truth = brute_designs(8)
    for target, designs in truth.items():
        assert designs  # every target of length 8 is designable in this model
        found = exact_designs(8, list(target), first_only=True)
        assert found and found[0] in designs


def test_cost_is_zero_exactly_for_designs():
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randrange(4, 11)
        structs = position_structures(n)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        target = list(rng.choice(structs))
        _, opt = brute_optima(s, structs)
        truth = len(opt) == 1 and tuple(sorted(target)) == opt[0]
        assert (cost(s, target) == 0) == truth
        assert cost(s, target) >= 0


def test_adaptive_walk_finds_designs():
    rng = random.Random(2024)
    done = 0
    while done < 15:
        n = rng.randrange(8, 13)
        structs = position_structures(n)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        # Targets that are known to be designable: the unique nonempty optimum of a random sequence.
        _, opt = brute_optima(s, structs)
        if len(opt) != 1 or not opt[0]:
            continue
        target = list(opt[0])
        found = adaptive_walk(n, target, random.Random(done))
        assert found is not None
        _, opt2 = brute_optima(found, structs)
        assert opt2 == [opt[0]]
        assert is_design(found, target)
        done += 1


def test_page_example():
    target = parse_dot_bracket("((....))..")
    assert is_design("GGAAAACCAA", target)
    assert fold_count("GGAAAACCAA") == (2, 1)
    assert fold_count("GGGAAACCAA") == (2, 3) and cost("GGGAAACCAA", target) == 2
    assert fold_count("GGAAAAUCAA") == (2, 3) and cost("GGAAAAUCAA", target) == 2
    assert cost("AAAAAAAAAA", target) == 3
