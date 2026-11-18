# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liang-hyphenation/. The authors are listed in prov/6YQPVW.jsonl.

import random

from liang_hyphenation import PatternTrie, hyphen_positions, hyphenate, hyphenation_values, parse_pattern

# The nine patterns of the example in The TeXbook, Appendix H.
TEXBOOK = ["hy3ph", "he2n", "hena4", "hen5at", "1na", "n2at", "1tio", "2io", "o2n"]


def brute_force_values(word, patterns):
    """Try every pattern at every start position of .word. and take the maxima."""
    w = "." + word.lower() + "."
    v = [0] * (len(w) + 1)
    for p in patterns:
        letters, values = parse_pattern(p)
        for i in range(len(w) - len(letters) + 1):
            if w[i : i + len(letters)] == letters:
                for t, d in enumerate(values):
                    v[i + t] = max(v[i + t], d)
    return v[1 : len(word) + 2]


def test_parse_pattern():
    assert parse_pattern("hy3ph") == ("hyph", [0, 0, 3, 0, 0])
    assert parse_pattern("1na") == ("na", [1, 0, 0])
    assert parse_pattern(".ach4") == (".ach", [0, 0, 0, 0, 4])
    assert parse_pattern("hen5at") == ("henat", [0, 0, 0, 5, 0, 0])


def test_texbook_example():
    trie = PatternTrie(TEXBOOK)
    v = hyphenation_values("hyphenation", trie)
    # the values between the letters h y p h e n a t i o n
    assert v[1:11] == [0, 3, 0, 0, 2, 5, 4, 2, 0, 2]
    assert v[0] == 0 and v[11] == 0
    assert hyphen_positions("hyphenation", trie) == [2, 6]
    assert hyphenate("hyphenation", trie) == "hy-phen-ation"
    assert v == brute_force_values("hyphenation", TEXBOOK)


def test_edge_limits_apply_after_the_patterns():
    trie = PatternTrie(TEXBOOK)
    # with lefthyphenmin 3 the odd value 3 after "hy" no longer gives a break
    assert hyphen_positions("hyphenation", trie, left=3) == [6]
    # with righthyphenmin 6 the break before "ation" (5 letters) goes too
    assert hyphen_positions("hyphenation", trie, right=6) == [2]
    # "nation": 1na gives an odd value before the first letter, which is never a break
    assert hyphenation_values("nation", trie)[0] == 1
    assert hyphenation_values("nation", trie) == [1, 2, 1, 2, 0, 2, 0]
    assert hyphen_positions("nation", trie, left=1, right=1) == [2]
    assert hyphenate("nation", trie, left=1, right=1) == "na-tion"
    # plain TeX values: righthyphenmin 3 keeps "tion" (4 letters) after the break
    assert hyphenate("nation", trie) == "na-tion"


def test_exceptions_override_patterns():
    trie = PatternTrie(TEXBOOK)
    exc = {"hyphenation": [2, 6, 8]}
    assert hyphenate("Hyphenation", trie, exceptions=exc) == "Hy-phen-at-ion"


def test_duplicate_letters_keep_the_larger_digit():
    trie = PatternTrie(["a1b", "a3b", "2ab"])
    assert trie.count == 1
    assert hyphenation_values("ab", trie) == [2, 3, 0]


def random_pattern(rng, alphabet):
    k = rng.randint(1, 4)
    letters = [rng.choice(alphabet) for _ in range(k)]
    if rng.random() < 0.2:
        letters[0] = "."
    if rng.random() < 0.2 and k > 1:
        letters[-1] = "."
    out = []
    for t in range(k + 1):
        if rng.random() < 0.4:
            out.append(str(rng.randint(1, 5)))
        if t < k:
            out.append(letters[t])
    return "".join(out)


def test_against_brute_force_on_random_patterns():
    rng = random.Random(2024)
    alphabet = "abc"
    for _ in range(300):
        pats = [random_pattern(rng, alphabet) for _ in range(rng.randint(1, 12))]
        trie = PatternTrie(pats)
        for _ in range(5):
            word = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 9)))
            assert hyphenation_values(word, trie) == brute_force_values(word, pats)


def test_trie_steps_are_at_most_quadratic():
    trie = PatternTrie(["a1a"] + ["a" * k for k in range(1, 12)])
    for k in range(1, 30):
        stats = {}
        hyphenation_values("a" * k, trie, stats)
        n = k + 2
        assert stats["steps"] <= n * (n + 1) // 2
