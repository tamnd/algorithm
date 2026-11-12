# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maglev-hashing/. The authors are listed in prov/DA1P19.jsonl.

import random
from collections import Counter

from maglev_hashing import Maglev, changed_fraction, offset_skip, permutations, populate

PRIMES = [7, 13, 101, 251, 1009, 5003]


def reference(perms, m):
    """Pseudocode 1 with stored preference lists."""
    n = len(perms)
    nxt = [0] * n
    entry = [-1] * m
    filled = 0
    while True:
        for i in range(n):
            c = perms[i][nxt[i]]
            while entry[c] >= 0:
                nxt[i] += 1
                c = perms[i][nxt[i]]
            entry[c] = i
            nxt[i] += 1
            filled += 1
            if filled == m:
                return entry


def test_paper_example():
    # Table 1 of the paper: M = 7, (offset, skip) = (3, 4), (0, 2), (3, 1).
    pairs = [(3, 4), (0, 2), (3, 1)]
    assert permutations(pairs, 7) == [
        [3, 0, 4, 1, 5, 2, 6], [0, 2, 4, 6, 1, 3, 5], [3, 4, 5, 6, 0, 1, 2]]
    assert populate(pairs, 7) == [1, 0, 1, 0, 2, 2, 0]  # B2 B1 B2 B1 B3 B3 B1
    # Without B2 the indices 0 and 1 are B1 and B3.
    assert populate([pairs[0], pairs[2]], 7) == [0, 0, 0, 0, 1, 1, 1]


def test_preference_lists_are_permutations_for_prime_m():
    for m in PRIMES:
        for name in ["a", "b", "backend-17"]:
            o, s = offset_skip(name, m)
            assert 0 <= o < m and 1 <= s <= m - 1
            assert sorted(permutations([(o, s)], m)[0]) == list(range(m))


def test_full_table_and_exact_counts():
    rng = random.Random(11)
    for m in PRIMES:
        for n in [1, 2, 3, 5, min(m, 10), min(m, 40)]:
            pairs = [(rng.randrange(m), rng.randrange(1, m)) for _ in range(n)]
            t = populate(pairs, m)
            assert all(0 <= x < n for x in t)
            c = Counter(t)
            q, r = divmod(m, n)
            for i in range(n):
                assert c[i] == (q + 1 if i < r else q)


def test_matches_reference_with_stored_lists():
    rng = random.Random(12)
    for m in [7, 13, 101, 251]:
        for n in [1, 3, 7]:
            pairs = [(rng.randrange(m), rng.randrange(1, m)) for _ in range(n)]
            assert populate(pairs, m) == reference(permutations(pairs, m), m)


def test_lookup_reads_the_table():
    t = Maglev(["b%d" % i for i in range(5)], 101)
    owners = t.owners()
    for k in range(200):
        key = "flow-%d" % k
        assert t.lookup(key) in owners


def test_disruption_on_removal_is_small_but_not_minimal():
    names = ["b%d" % i for i in range(10)]
    m = 5003
    before = Maglev(names, m).owners()
    after = Maglev(names[:3] + names[4:], m).owners()
    f = changed_fraction(before, after)
    own = sum(1 for x in before if x == "b3") / m
    # The slots of b3 must change; a few more change too.
    assert all(a != "b3" for a in after)
    assert f >= own
    assert f - own < 0.03
    # Slots that change but did not belong to b3:
    extra = sum(1 for a, b in zip(before, after) if a != b and a != "b3")
    assert extra > 0


def test_disruption_drops_as_table_grows():
    names = ["b%d" % i for i in range(20)]
    extras = []
    for m in [251, 5003, 65537]:
        before = Maglev(names, m).owners()
        after = Maglev(names[:-1], m).owners()
        extras.append(sum(1 for a, b in zip(before, after) if a != b and a != names[-1]) / m)
    assert extras[0] > extras[2]
