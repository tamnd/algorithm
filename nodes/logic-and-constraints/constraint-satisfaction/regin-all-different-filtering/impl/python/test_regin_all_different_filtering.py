# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regin-all-different-filtering/. The authors are listed in prov/A7F2AJ.jsonl.

import itertools
import random

from regin_all_different_filtering import regin_all_different_filtering


def brute_force_gac(domains):
    """Values that occur in some solution, by enumeration of all tuples."""
    keep = [set() for _ in domains]
    found = False
    for t in itertools.product(*domains):
        if len(set(t)) == len(t):
            found = True
            for i, a in enumerate(t):
                keep[i].add(a)
    if not found:
        return None
    return [[a for a in dict.fromkeys(dom) if a in keep[i]] for i, dom in enumerate(domains)]


def pairwise_ac(domains):
    """Arc consistency on the clique of binary not-equal constraints."""
    doms = [list(dict.fromkeys(d)) for d in domains]
    changed = True
    while changed:
        changed = False
        for i in range(len(doms)):
            for j in range(len(doms)):
                if i != j and len(doms[j]) == 1 and doms[j][0] in doms[i]:
                    doms[i].remove(doms[j][0])
                    changed = True
                    if not doms[i]:
                        return None
    return doms


def test_page_example():
    doms = [[1, 2], [1, 2], [1, 2, 3, 4], [2, 3, 4], [3, 5, 6]]
    assert regin_all_different_filtering(doms) == [[1, 2], [1, 2], [3, 4], [3, 4], [5, 6]]
    assert brute_force_gac(doms) == [[1, 2], [1, 2], [3, 4], [3, 4], [5, 6]]
    doms = [[1, 2], [1, 2], [1, 2, 3, 4], [2, 3, 4, 5], [3, 5]]
    assert regin_all_different_filtering(doms) == [[1, 2], [1, 2], [3, 4], [3, 4, 5], [3, 5]]


def test_pairwise_counterexamples():
    # Three variables, two values: pairwise AC removes nothing, GAC fails.
    doms = [[1, 2], [1, 2], [1, 2]]
    assert pairwise_ac(doms) == doms
    assert regin_all_different_filtering(doms) is None
    # GAC removes 1 and 2 from the third variable; pairwise AC does not.
    doms = [[1, 2], [1, 2], [1, 2, 3]]
    assert pairwise_ac(doms) == doms
    assert regin_all_different_filtering(doms) == [[1, 2], [1, 2], [3]]


def test_edges():
    assert regin_all_different_filtering([]) == []
    assert regin_all_different_filtering([[7]]) == [[7]]
    assert regin_all_different_filtering([[]]) is None
    assert regin_all_different_filtering([[1], [1]]) is None
    assert regin_all_different_filtering([[1, 1, 2], [1]]) == [[2], [1]]
    assert regin_all_different_filtering([["a", "b"], ["b"], ["a", "b", "c"]]) == [["a"], ["b"], ["c"]]


def test_against_brute_force():
    rng = random.Random(1994)
    for _ in range(1500):
        n = rng.randint(1, 6)
        k = rng.randint(1, 7)
        doms = [rng.sample(range(k), rng.randint(1, k)) for _ in range(n)]
        assert regin_all_different_filtering(doms) == brute_force_gac(doms)


def test_gac_is_at_least_pairwise_ac():
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(2, 6)
        doms = [rng.sample(range(5), rng.randint(1, 4)) for _ in range(n)]
        g = regin_all_different_filtering(doms)
        p = pairwise_ac(doms)
        if p is None:
            assert g is None
        elif g is not None:
            for gi, pi in zip(g, p):
                assert set(gi) <= set(pi)


def test_permutation_large():
    # A permutation of 300 values: every value stays.
    rng = random.Random(3)
    n = 300
    doms = [rng.sample(range(n), 5) for _ in range(n)]
    for i in range(n):
        doms[i].append(i)
    out = regin_all_different_filtering(doms)
    assert out is not None
    assert all(i in out[i] for i in range(n))
