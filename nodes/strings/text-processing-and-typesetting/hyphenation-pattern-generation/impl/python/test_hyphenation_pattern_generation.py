# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyphenation-pattern-generation/. The authors are listed in prov/980NJ6.jsonl.

import random

from hyphenation_pattern_generation import (
    Level,
    counted_gaps,
    gap_values,
    generate,
    hyphens,
    parse_hyphenated,
    pattern_strings,
)

# A word list made up for this test. The hyphens were marked by hand in the
# American style; they are not copied from any dictionary.
WORDS = """hy-phen-ation com-put-er al-go-rithm pat-tern pat-terns let-ter let-ters mat-ter
but-ter bet-ter lad-der num-ber num-bers ta-ble ca-ble sta-tion na-tion ac-tion mo-tion
frac-tion dic-tion-ary pro-gram pro-cess in-ter-est in-ter-val win-ter sis-ter mon-ster
con-stant con-cept be-gin be-come""".split()

# (good_wt, bad_wt, thresh, shortest, longest): hyphenate, inhibit, then safe hyphenating patterns
LEVELS = [Level(1, 1, 2, 2, 3), Level(1, 2, 1, 2, 4), Level(1, 100, 1, 2, 8)]


def brute_force_values(word, patterns):
    w = "." + word + "."
    v = [0] * (len(w) + 1)
    for letters, vals in patterns.items():
        for i in range(len(w) - len(letters) + 1):
            if w[i : i + len(letters)] == letters:
                for t, d in enumerate(vals):
                    v[i + t] = max(v[i + t], d)
    return v[1 : len(word) + 2]


def test_parse_hyphenated():
    assert parse_hyphenated("hy-phen-ation") == ("hyphenation", frozenset({2, 6}))
    assert parse_hyphenated("ta-ble") == ("table", frozenset({2}))


def test_levels_counts():
    pats, rep = generate(WORDS, LEVELS)
    assert len(WORDS) == 32
    got = [(r.level, r.patterns, r.passes, r.found, r.errors, r.missed) for r in rep]
    assert got == [
        (1, 7, 7, 27, 3, 11),
        (2, 3, 12, 27, 0, 11),
        (3, 11, 42, 38, 0, 0),
    ]
    # a pattern of length k takes k + 1 passes: lengths 2..3 give 3 + 4 = 7 passes
    assert [r.passes for r in rep] == [sum(k + 1 for k in range(L.min_len, L.max_len + 1)) for L in LEVELS]


def test_patterns_of_each_level():
    p1, _ = generate(WORDS, LEVELS[:1])
    assert pattern_strings(p1) == ["1be", "1bl", "1ce", "n1a", "n1s", "1te", "1ti"]
    p2, _ = generate(WORDS, LEVELS[:2])
    assert pattern_strings(p2) == ["1be", "1bl", "1ce", "ena2", "n1a", "n1s2", "1te", "1ti", "u2t"]


def test_final_patterns_find_every_hyphen_and_no_bad_hyphen():
    pats, _ = generate(WORDS, LEVELS)
    for e in WORDS:
        w, true = parse_hyphenated(e)
        assert hyphens(w, pats, 2, 2) == {g for g in true if g in counted_gaps(len(w), 2, 2)}
        assert gap_values(w, pats) == brute_force_values(w, pats)


def test_first_pass_follows_the_selection_rule():
    # length 2, dot 0, level 1, no earlier patterns: count by brute force
    words = [parse_hyphenated(e) for e in WORDS]
    good, bad = {}, {}
    for w, true in words:
        s = "." + w + "."
        for g in counted_gaps(len(w), 2, 2):
            letters = s[g + 1 : g + 3]
            d = good if g in true else bad
            d[letters] = d.get(letters, 0) + 1
    want = sorted(x for x in set(good) | set(bad) if good.get(x, 0) - bad.get(x, 0) >= 2)
    pats, _ = generate(WORDS, [Level(1, 1, 2, 2, 2)])
    first_pass = sorted(x for x, v in pats.items() if v[0] == 1)
    assert first_pass == want
    assert want == ["be", "bl", "ce", "te", "ti"]
    assert (good["te"], bad["te"]) == (11, 2) and (good["ti"], bad["ti"]) == (6, 1)
    assert (good.get("er", 0), bad["er"]) == (1, 15)


def test_random_lists_with_enough_levels_are_learned_exactly():
    rng = random.Random(31)
    for _ in range(10):
        entries = set()
        while len(entries) < 12:
            k = rng.randint(4, 8)
            w = "".join(rng.choice("abcde") for _ in range(k))
            pos = sorted(rng.sample(range(2, k - 1), rng.randint(0, min(2, k - 3)))) if k > 4 else []
            e = "".join(("-" if i in pos else "") + c for i, c in enumerate(w))
            if w not in {parse_hyphenated(x)[0] for x in entries}:
                entries.add(e)
        entries = sorted(entries)
        levels = [Level(1, 1, 2, 2, 3), Level(1, 1, 1, 2, 4), Level(1, 100, 1, 2, 10), Level(1, 100, 1, 2, 10)]
        pats, rep = generate(entries, levels)
        assert rep[-1].errors == 0 and rep[-1].missed == 0
        for e in entries:
            w, true = parse_hyphenated(e)
            assert hyphens(w, pats, 2, 2) == set(true)
