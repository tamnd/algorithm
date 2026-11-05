# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aho-corasick/. The authors are listed in prov/P3M1B3.jsonl.

import random

from aho_corasick import NIL, ROOT, Automaton, aho_corasick


def oracle(t: str, pats: list[str]) -> list[tuple[int, int]]:
    return sorted(
        (s, j) for j, p in enumerate(pats) for s in range(len(t) - len(p) + 1) if t[s : s + len(p)] == p
    )


def node_strings(a: Automaton) -> list[str]:
    s = [""] * len(a.goto)
    stack = [ROOT]
    while stack:
        v = stack.pop()
        for c, u in a.goto[v].items():
            s[u] = s[v] + c
            stack.append(u)
    return s


def test_example() -> None:
    pats = ["he", "she", "his", "hers"]
    assert aho_corasick("ushers", pats) == [(1, 1), (2, 0), (2, 3)]
    a = Automaton(pats)
    s = node_strings(a)
    fail = {s[v]: s[a.fail[v]] for v in range(1, len(s))}
    assert fail == {"h": "", "s": "", "he": "", "hi": "", "sh": "h", "she": "he", "his": "s", "her": "", "hers": "s"}
    dict_link = {s[v]: (s[a.dict_link[v]] if a.dict_link[v] != NIL else None) for v in range(1, len(s))}
    assert dict_link["she"] == "he"
    assert all(dict_link[x] is None for x in dict_link if x != "she")


def test_edges() -> None:
    assert aho_corasick("", []) == []
    assert aho_corasick("abc", []) == []
    assert aho_corasick("", [""]) == [(0, 0)]
    assert aho_corasick("ab", [""]) == [(0, 0), (1, 0), (2, 0)]
    assert aho_corasick("ab", ["abc"]) == []
    assert aho_corasick("aaaa", ["aa", "a"]) == [(0, 1), (0, 0), (1, 1), (1, 0), (2, 1), (2, 0), (3, 1)]
    assert sorted(aho_corasick("abab", ["ab", "ab"])) == [(0, 0), (0, 1), (2, 0), (2, 1)]


def test_dictionary_links_needed() -> None:
    # "b" is a suffix of "abc"'s prefix "ab" but str(v) = "ab" itself is not a pattern
    assert sorted(aho_corasick("abd", ["abc", "b"])) == [(1, 1)]
    # a pattern hidden two failure links deep
    assert sorted(aho_corasick("xabcd", ["abcd", "bcd", "cd", "d", "bc"])) == oracle("xabcd", ["abcd", "bcd", "cd", "d", "bc"])


def test_fail_links_against_definition() -> None:
    rng = random.Random(5)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(200):
            pats = ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7))) for _ in range(rng.randint(1, 5))]
            a = Automaton(pats)
            s = node_strings(a)
            nodes = {x: v for v, x in enumerate(s)}
            ends = {p for p in pats}
            for v in range(1, len(s)):
                x = s[v]
                want = max((x[k:] for k in range(1, len(x) + 1) if x[k:] in nodes), key=len)
                assert s[a.fail[v]] == want
                dl = [x[k:] for k in range(1, len(x) + 1) if x[k:] in ends]
                got = a.dict_link[v]
                assert (s[got] if got != NIL else None) == (max(dl, key=len) if dl else None)


def random_patterns(rng: random.Random, alphabet: str, text: str) -> list[str]:
    pats = []
    for _ in range(rng.randint(0, 6)):
        r = rng.random()
        if r < 0.1:
            pats.append("")
        elif r < 0.4 and text:
            i = rng.randrange(len(text))
            pats.append(text[i : i + rng.randint(1, 6)])
        elif r < 0.55 and pats:
            p = rng.choice(pats)
            pats.append(p[: rng.randint(0, len(p))] if rng.random() < 0.5 else p[rng.randint(0, len(p)) :])
        elif r < 0.7:
            unit = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3)))
            pats.append((unit * 5)[: rng.randint(1, 8)])
        else:
            pats.append("".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6))))
    return pats


def test_random_against_oracle() -> None:
    rng = random.Random(2024)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            if rng.random() < 0.3:
                unit = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3)))
                t = (unit * 20)[: rng.randint(0, 30)]
            else:
                t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
            pats = random_patterns(rng, alphabet, t)
            got = aho_corasick(t, pats)
            assert sorted(got) == oracle(t, pats)
            ends = [s + len(pats[j]) for s, j in got]
            assert ends == sorted(ends)


def test_sequences_of_integers() -> None:
    assert sorted(aho_corasick([1, 2, 1, 2, 1], [[1, 2, 1], [2]])) == [(0, 0), (1, 1), (2, 0), (3, 1)]
