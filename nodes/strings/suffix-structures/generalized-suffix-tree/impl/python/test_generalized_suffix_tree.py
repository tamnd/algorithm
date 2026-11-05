# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-suffix-tree/. The authors are listed in prov/4HGXBV.jsonl.

import random

from generalized_suffix_tree import GeneralizedSuffixTree


def one_string(rng: random.Random) -> str:
    kind = rng.randrange(6)
    n = rng.randrange(9)
    if kind == 0:
        return "a" * n
    if kind == 1:
        return "ab" * (n // 2)
    sigma = rng.choice([1, 2, 4])
    return "".join(rng.choice("abcd"[:sigma]) for _ in range(n))


def collections(seed: int, count: int = 600) -> list[list[str]]:
    rng = random.Random(seed)
    out = [[], [""], ["a"], ["", ""], ["xabxa", "babxba"], ["banana", "cabana"], ["aaaa", "aa"], ["abab", "baba"]]
    for _ in range(count):
        out.append([one_string(rng) for _ in range(rng.randint(1, 4))])
    return out


def naive_find(strings: list[str], p: str) -> list[tuple[int, int]]:
    return sorted((k, j) for k, s in enumerate(strings) for j in range(len(s) - len(p) + 1) if s[j : j + len(p)] == p)


def naive_internal_labels(strings: list[str]) -> list[str]:
    """Right-branching substrings: the path labels of the internal nodes, root included."""
    follow: dict[str, set] = {}
    for k, s in enumerate(strings):
        for i in range(len(s)):
            for j in range(i, len(s) + 1):
                nxt = s[j] if j < len(s) else ("$", k)
                follow.setdefault(s[i:j], set()).add(nxt)
    labels = {u for u, f in follow.items() if len(f) >= 2}
    labels.add("")
    return sorted(labels)


def naive_lcs_length(strings: list[str], k: int) -> int:
    best = 0
    subs = [{s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)} for s in strings]
    for u in set().union(*subs) if subs else set():
        if len(u) > best and sum(u in t for t in subs) >= k:
            best = len(u)
    return best


def label(t: GeneralizedSuffixTree, v: int) -> str:
    return "".join(t.symbol[c] for c in t.z[t.pos[v] : t.pos[v] + t.depth[v]])


def test_example() -> None:
    t = GeneralizedSuffixTree(["xabxa", "babxba"])
    t.check_invariant()
    assert t.node_count() == (8, 11)
    assert t.find("bx") == [(0, 2), (1, 2)]
    assert t.find("xa") == [(0, 0), (0, 3)]
    assert t.strings_containing("ba") == [1]
    assert "".join(t.longest_common_substring(2)) == "abx"
    assert "".join(t.longest_common_substring(1)) == "babxba"


def test_structure_against_brute_force() -> None:
    for strings in collections(1):
        t = GeneralizedSuffixTree(strings)
        t.check_invariant()
        internal = sorted(label(t, v) for v in range(len(t.depth)) if t.leaf[v] is None)
        assert internal == naive_internal_labels(strings), strings


def test_find_against_brute_force() -> None:
    rng = random.Random(2)
    for strings in collections(3):
        t = GeneralizedSuffixTree(strings)
        pats = {s[i:j] for s in strings for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
        pats = sorted(pats)[:12] + ["".join(rng.choice("abcde") for _ in range(rng.randint(1, 4))) for _ in range(4)]
        for p in pats:
            assert t.find(p) == naive_find(strings, p), (strings, p)
            assert t.strings_containing(p) == sorted({k for k, _ in naive_find(strings, p)})


def test_longest_common_substring_against_brute_force() -> None:
    for strings in collections(4):
        t = GeneralizedSuffixTree(strings)
        for k in range(1, len(strings) + 1):
            u = "".join(t.longest_common_substring(k))
            assert len(u) == naive_lcs_length(strings, k), (strings, k)
            assert sum(u in s for s in strings) >= k or u == ""
