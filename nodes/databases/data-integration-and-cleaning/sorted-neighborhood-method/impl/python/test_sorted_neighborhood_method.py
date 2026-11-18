# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sorted-neighborhood-method/. The authors are listed in prov/7P2CSB.jsonl.

import random

from sorted_neighborhood_method import (
    all_pairs,
    clusters_from_pairs,
    expected_calls,
    precision_recall,
    snm_pass,
    sorted_neighborhood,
)

FIRST = ["anna", "boris", "carla", "david", "elena", "frank", "greta", "hugo", "irene", "jonas",
         "karin", "lukas", "maria", "nils", "olga", "paul", "rosa", "simon", "tina", "viktor"]
LAST = ["adler", "becker", "fischer", "graf", "hahn", "keller", "lang", "meyer", "neumann", "otto",
        "peters", "richter", "schulz", "vogel", "wagner", "weber", "wolf", "ziegler", "brandt", "kraus"]
CITY = ["bonn", "essen", "kiel", "mainz", "trier", "ulm", "jena", "hof"]


def typo(rng, s):
    """One random edit: substitute, delete, insert or swap two neighbours."""
    i = rng.randrange(len(s))
    kind = rng.randrange(4)
    letter = rng.choice("abcdefghijklmnopqrstuvwxyz")
    if kind == 0:
        return s[:i] + letter + s[i + 1:]
    if kind == 1 and len(s) > 2:
        return s[:i] + s[i + 1:]
    if kind == 2:
        return s[:i] + letter + s[i:]
    if i + 1 < len(s):
        return s[:i] + s[i + 1] + s[i] + s[i + 2:]
    return s + letter


def synthetic(seed, entities=60):
    """Records (first, last, city, year) and the true clusters of record numbers."""
    rng = random.Random(seed)
    records, truth = [], []
    for _ in range(entities):
        base = (rng.choice(FIRST), rng.choice(LAST), rng.choice(CITY), rng.randint(1950, 1999))
        ids = []
        for copy in range(1 + rng.randint(0, 3)):
            first, last, city, year = base
            if copy > 0:
                for _ in range(rng.randint(0, 2)):
                    if rng.random() < 0.5:
                        first = typo(rng, first)
                    else:
                        last = typo(rng, last)
                if rng.random() < 0.15:
                    last = rng.choice("bcdfgklmprstw") + last[1:]
                if rng.random() < 0.1:
                    city = rng.choice(CITY)
            ids.append(len(records))
            records.append((first, last, city, year))
        truth.append(ids)
    return records, truth


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def match(r, s):
    """The pairwise rule: same year and at most 2 edits over the two names."""
    return r[3] == s[3] and edit_distance(r[0], s[0]) + edit_distance(r[1], s[1]) <= 2


KEYS = [
    lambda r: (r[1][:3], r[0][:1], r[3]),
    lambda r: (r[0][:3], r[1][:1], r[3]),
    lambda r: (r[3], r[2], r[1][:1]),
]


def test_call_count_formula():
    for n in range(0, 30):
        for w in range(1, 12):
            records = list(range(n))
            _, calls = snm_pass(records, lambda r: r, lambda r, s: False, w)
            assert calls == expected_calls(n, w)
            if n >= w:
                assert calls == (w - 1) * n - w * (w - 1) // 2


def test_page_example():
    records = [("smith", 1970), ("smyth", 1970), ("jones", 1962), ("smith", 1985), ("jonas", 1962), ("brown", 1970)]

    def m(r, s):
        return r[1] == s[1] and edit_distance(r[0], s[0]) <= 1

    by_name = lambda r: r[0]
    by_year = lambda r: (r[1], r[0])
    assert snm_pass(records, by_name, m, 2) == ({(2, 4)}, 5)
    assert snm_pass(records, by_name, m, 3) == ({(0, 1), (2, 4)}, 9)
    assert snm_pass(records, by_year, m, 2) == ({(0, 1), (2, 4)}, 5)
    clusters, pairs, calls = sorted_neighborhood(records, [by_name, by_year], m, 2)
    assert clusters == [[0, 1], [2, 4], [3], [5]] and calls == 10


def test_full_window_equals_all_pairs():
    records, _ = synthetic(1, entities=25)
    n = len(records)
    for key in KEYS:
        pairs, calls = snm_pass(records, key, match, n)
        assert pairs == all_pairs(records, match)
        assert calls == n * (n - 1) // 2


def test_pass_finds_subset_of_all_pairs():
    records, _ = synthetic(2)
    full = all_pairs(records, match)
    for key in KEYS:
        for w in (2, 4, 8):
            pairs, _ = snm_pass(records, key, match, w)
            assert pairs <= full


def test_precision_and_recall_seed_42():
    records, truth = synthetic(42)
    n = len(records)
    full_clusters = clusters_from_pairs(n, all_pairs(records, match))
    p_full, r_full = precision_recall(full_clusters, truth)
    single = []
    for key in KEYS:
        clusters, _, calls = sorted_neighborhood(records, [key], match, 4)
        assert calls == expected_calls(n, 4)
        single.append(precision_recall(clusters, truth))
    multi, _, calls = sorted_neighborhood(records, KEYS, match, 4)
    p_multi, r_multi = precision_recall(multi, truth)
    assert calls == 3 * expected_calls(n, 4) < n * (n - 1) // 2
    assert all(r_multi >= r for _, r in single)
    assert r_multi <= r_full + 1e-12
    assert r_multi > max(r for _, r in single)
    assert p_multi >= 0.9 and r_multi >= 0.8
