# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-index/. The authors are listed in prov/D8XXKM.jsonl.

import random

from r_index import RIndex


def occurrences(s: str, p: str) -> list[int]:
    return [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]


def bwt_runs(s: str) -> int:
    t = s + "\0"
    sa = sorted(range(len(t)), key=lambda i: t[i:])
    b = [t[i - 1] for i in sa]
    return sum(1 for i in range(len(b)) if i == 0 or b[i] != b[i - 1])


def test_example() -> None:
    idx = RIndex("banana")
    idx.check_invariant()
    assert idx.r == 5 and idx.heads == [1, 3, 2, 0, 1] and idx.starts == [0, 1, 3, 4, 5]
    assert idx.locate("ana") == [1, 3] and idx.count("an") == 2 and idx.count("a") == 3
    assert idx.locate("nab") == [] and not idx.contains("x")
    assert idx.phi_keys == [0, 3, 4, 5] and idx.phi_vals == [1, 5, 0, 6]


def test_edges() -> None:
    idx = RIndex("")
    idx.check_invariant()
    assert idx.r == 1 and idx.count("a") == 0 and idx.locate("") == [0]
    for n in (1, 2, 9, 300):
        s = "a" * n
        idx = RIndex(s)
        idx.check_invariant()
        assert idx.r == 2
        assert sorted(idx.locate("aa")) == occurrences(s, "aa")
        assert idx.count("a" * n) == 1 and idx.count("a" * (n + 1)) == 0
    s = "ab" * 200
    idx = RIndex(s)
    idx.check_invariant()
    assert idx.r == bwt_runs(s) and idx.r <= 4
    assert sorted(idx.locate("bab")) == occurrences(s, "bab")
    assert sorted(RIndex("abcab").locate("")) == list(range(6))
    idx = RIndex([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    assert idx.locate([5]) and sorted(idx.locate([5])) == [4, 8, 10]


def test_against_naive() -> None:
    rng = random.Random(2018)
    for trial in range(1500):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 18)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 25 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        idx = RIndex(s)
        idx.check_invariant()
        assert idx.r == bwt_runs(s)
        for _ in range(8):
            if s and rng.random() < 0.6:
                i = rng.randrange(len(s))
                p = s[i:i + rng.randint(1, 5)]
            else:
                p = "".join(rng.choice(sigma + "e") for _ in range(rng.randint(1, 4)))
            occ = occurrences(s, p)
            assert sorted(idx.locate(p)) == occ
            assert idx.count(p) == len(occ) and idx.contains(p) == bool(occ)


def test_repetitive_text_is_small() -> None:
    """On a highly repetitive text the index keeps far fewer values than n."""
    rng = random.Random(3)
    base = "".join(rng.choice("acgt") for _ in range(50))
    copies = []
    for _ in range(40):
        c = list(base)
        c[rng.randrange(50)] = rng.choice("acgt")
        copies.append("".join(c))
    s = "".join(copies)
    idx = RIndex(s)
    idx.check_invariant()
    assert idx.r < len(s) // 4
    assert idx.stored_values() < 8 * idx.r + 10
    p = base[10:30]
    assert sorted(idx.locate(p)) == occurrences(s, p)
