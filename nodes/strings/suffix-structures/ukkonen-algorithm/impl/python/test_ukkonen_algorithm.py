# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ukkonen-algorithm/. The authors are listed in prov/YN86V8.jsonl.

import random

from ukkonen_algorithm import UkkonenTree


def naive_node_count(s: str) -> int:
    t = list(s) + [None]
    ext: dict[str, set] = {}
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            ext.setdefault(s[i:j], set()).add(t[j])
    return len(s) + 2 + sum(1 for x in ext.values() if len(x) >= 2)


def build(s: str) -> UkkonenTree:
    tr = UkkonenTree(s)
    tr.finish()
    return tr


def test_example() -> None:
    tr = UkkonenTree()
    for c in "abcabx":
        tr.extend(c)
        tr.check_invariant()
    assert tr.contains("cab") and not tr.contains("bb")
    tr.finish()
    tr.check_invariant()
    assert tr.suffix_array() == sorted(range(6), key=lambda i: "abcabx"[i:])
    tr = build("banana")
    tr.check_invariant()
    assert tr.suffix_array() == [5, 3, 1, 0, 4, 2] and tr.node_count() == 11


def test_edges() -> None:
    tr = build("")
    tr.check_invariant()
    assert tr.suffix_array() == [] and tr.node_count() == 2
    for n in (1, 2, 7, 400):
        tr = build("a" * n)
        if n < 50:
            tr.check_invariant()
        assert tr.node_count() == 2 * n + 1
        assert tr.suffix_array() == list(range(n - 1, -1, -1))
    tr = build("ab" * 300)
    assert tr.suffix_array() == sorted(range(600), key=lambda i: ("ab" * 300)[i:])
    tr = build([3, 1, 4, 1, 5, 9, 2, 6])
    tr.check_invariant()
    assert tr.suffix_array() == [1, 3, 6, 0, 2, 4, 7, 5]


def test_online_against_naive() -> None:
    rng = random.Random(1995)
    for trial in range(600):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 22)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 30 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        tr = UkkonenTree()
        for j, c in enumerate(s):
            tr.extend(c)
            if trial % 5 == 0:
                tr.check_invariant()
                pre = s[: j + 1]
                for _ in range(4):
                    p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(1, 4)))
                    assert tr.contains(p) == (p in pre)
        tr.finish()
        tr.check_invariant()
        assert tr.suffix_array() == sorted(range(len(s)), key=lambda i: s[i:])
        assert tr.node_count() == naive_node_count(s)
        for _ in range(6):
            i = rng.randrange(len(s) + 1)
            p = s[i:rng.randint(i, len(s))]
            assert tr.contains(p)
