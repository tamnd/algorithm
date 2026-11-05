# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/commentz-walter/. The authors are listed in prov/1K05ZQ.jsonl.

import random

from commentz_walter import ReversedTrie, commentz_walter


def naive(t, pats) -> list[tuple[int, int]]:
    out = []
    for j, q in enumerate(pats):
        for s in range(len(t) - len(q) + 1):
            if t[s : s + len(q)] == q:
                out.append((s, j))
    return sorted(out)


def node_strings(tr: ReversedTrie) -> list[str]:
    """The forward string (a suffix of a pattern) of every node."""
    names = [""] * len(tr.children)
    for v, kids in enumerate(tr.children):
        for ch, u in kids.items():
            names[u] = ch + names[v]
    return names


def test_example() -> None:
    pats = ["caacb", "cbaa", "accb"]
    tr = ReversedTrie(pats)
    names = node_strings(tr)
    table = {names[v]: (tr.shift1[v], tr.shift2[v]) for v in range(len(names))}
    assert table == {
        "": (1, 4), "b": (2, 4), "cb": (2, 2), "acb": (4, 2), "aacb": (4, 2), "caacb": (4, 2),
        "a": (1, 3), "aa": (2, 3), "baa": (4, 3), "cbaa": (4, 3), "ccb": (4, 2), "accb": (4, 2),
    }
    assert tr.char == {"a": 1, "b": 1, "c": 2} and tr.wmin == 4
    stats: dict[str, int] = {}
    assert commentz_walter("ccdaaacaacbaaddbcd", pats, stats) == [(6, 0), (9, 1)]
    assert stats == {"windows": 7, "reads": 21}


def test_small_cases() -> None:
    assert commentz_walter("", []) == []
    assert commentz_walter("", [""]) == [(0, 0)]
    assert commentz_walter("ab", ["", "x", "abc"]) == [(0, 0), (1, 0), (2, 0)]
    assert commentz_walter("ushers", ["he", "she", "his", "hers"]) == [(1, 1), (2, 0), (2, 3)]
    assert commentz_walter("aaaa", ["aa", "a", "aa"]) == naive("aaaa", ["aa", "a", "aa"])
    assert commentz_walter([1, 2, 1, 2], [[2, 1], [1, 2, 1]]) == [(0, 1), (1, 0)]


def definitions(pats: list[str], tr: ReversedTrie):
    """shift1, shift2 and char computed directly from their definitions on strings."""
    nonempty = [p for p in pats if p]
    w = min(len(p) for p in nonempty)
    suffixes = {p[len(p) - i :] for p in nonempty for i in range(len(p) + 1)}
    names = node_strings(tr)
    s1, s2 = [], []
    for y in names:
        # set1: node strings z y' with y as a proper prefix (y occurs |z'| before a pattern end).
        d1 = [len(x) - len(y) for x in suffixes if len(x) > len(y) and x.startswith(y)]
        s1.append(min([w] + d1))
        # shift2: a pattern P whose prefix of length i, 1 <= i < |P|, is a suffix of y; shift |P| - i.
        d2 = [len(p) - i for p in nonempty for i in range(1, min(len(y), len(p) - 1) + 1) if p[:i] == y[len(y) - i :]]
        s2.append(min([w] + d2))
    char = {}
    for p in nonempty:
        for e in range(len(p)):
            c = p[len(p) - 1 - e]
            char[c] = min(char.get(c, w + 1), e + 1)
    return s1, s2, char


def test_tables_match_definitions() -> None:
    rng = random.Random(17)
    for _ in range(400):
        sigma = rng.choice([1, 2, 3])
        pats = ["".join(rng.choice("abc"[:sigma]) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(1, 4))]
        if not any(pats):
            continue
        tr = ReversedTrie(pats)
        s1, s2, char = definitions(pats, tr)
        assert tr.shift1 == s1
        assert tr.shift2 == s2
        w = tr.wmin
        assert {c: v for c, v in tr.char.items() if v <= w} == {c: v for c, v in char.items() if v <= w}


def largest_safe_shift(pats: list[str], y: str, c: str | None) -> int:
    """The smallest delta >= 1 at which some pattern can end, given that the text read backward
    from the window end is y preceded by c (c is None at the start of the text)."""
    nonempty = [p for p in pats if p]
    known = {-len(y) + 1 + i: ch for i, ch in enumerate(y)}  # window end at position 0
    if c is not None:
        known[-len(y)] = c
    delta = 1
    while True:
        for p in nonempty:
            start = delta - len(p) + 1
            if c is None and start < -len(y) + 1:
                continue
            if all(known.get(start + i, p[i]) == p[i] for i in range(len(p))):
                return delta
        delta += 1


def test_shift_is_safe() -> None:
    rng = random.Random(23)
    for _ in range(300):
        sigma = rng.choice([1, 2, 3])
        alpha = "abc"[:sigma]
        pats = ["".join(rng.choice(alpha) for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 4))]
        tr = ReversedTrie(pats)
        names = node_strings(tr)
        for v, y in enumerate(names):
            for c in list(alpha) + ["d", None]:
                if c is not None and c in tr.children[v]:
                    continue  # the reading would not stop here
                assert 1 <= tr.shift(v, c) <= largest_safe_shift(pats, y, c)


def random_text(rng: random.Random, sigma: int, n: int) -> str:
    kind = rng.randrange(3)
    if kind == 0:
        return "".join(rng.choice("abcd"[:sigma]) for _ in range(n))
    period = "".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randint(1, 4)))
    s = (period * (n // len(period) + 1))[:n]
    if kind == 2 and n > 0:
        i = rng.randrange(n)
        s = s[:i] + rng.choice("abcd"[:sigma]) + s[i + 1 :]
    return s


def random_patterns(rng: random.Random, t: str, sigma: int) -> list[str]:
    pats: list[str] = []
    for _ in range(rng.randint(1, 6)):
        kind = rng.randrange(5)
        if kind == 0 and t:
            i = rng.randrange(len(t))
            pats.append(t[i : i + rng.randint(1, 7)])
        elif kind == 1 and pats:
            q = rng.choice(pats)
            pats.append(q[: rng.randint(0, len(q))])  # a prefix of another pattern
        elif kind == 2 and pats:
            q = rng.choice(pats)
            pats.append(q[rng.randint(0, len(q)) :])  # a suffix of another pattern
        elif kind == 3 and pats:
            pats.append(rng.choice(pats))  # a pattern listed twice
        else:
            pats.append(random_text(rng, sigma, rng.randint(0, 7)))
    return pats


def test_random_against_naive() -> None:
    rng = random.Random(20261106)
    cases = 0
    for sigma in (1, 2, 4):
        for _ in range(500):
            t = random_text(rng, sigma, rng.randint(0, 40))
            pats = random_patterns(rng, t, sigma)
            assert commentz_walter(t, pats) == naive(t, pats)
            cases += 1
    assert cases >= 500


def test_worst_case_reads() -> None:
    # Text a^n with the patterns a^(L-1) b and b a^(L-1): no occurrence, every window reads
    # L characters and shifts by 1.
    for L in (4, 8, 16):
        stats: dict[str, int] = {}
        assert commentz_walter("a" * 100, ["a" * (L - 1) + "b", "b" + "a" * (L - 1)], stats) == []
        assert stats == {"windows": 100 - L + 1, "reads": (100 - L + 1) * L}
