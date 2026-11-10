# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-contraction/. The authors are listed in prov/QF7GHN.jsonl.

import math
import random

from list_contraction import Stats, choose, suffix_sums


def random_lists(n: int, k: int, rng: random.Random) -> list[int | None]:
    order = list(range(n))
    rng.shuffle(order)
    cuts = set(rng.sample(range(1, n), min(k - 1, n - 1))) if n > 1 else set()
    nxt: list[int | None] = [None] * n
    for t in range(n - 1):
        if t + 1 not in cuts:
            nxt[order[t]] = order[t + 1]
    return nxt


def walk_suffix(nxt: list[int | None], x: list[str]) -> list[str]:
    """Sequential reference with an explicit walk from each head."""
    n = len(nxt)
    has_pred = [False] * n
    for j in nxt:
        if j is not None:
            has_pred[j] = True
    y = [""] * n
    for h in range(n):
        if not has_pred[h]:
            path = []
            v: int | None = h
            while v is not None:
                path.append(v)
                v = nxt[v]
            acc = ""
            for v in reversed(path):
                acc = x[v] + acc
                y[v] = acc
    return y


def concat(a: str, b: str) -> str:
    return a + b


def test_example() -> None:
    nxt = [6, 7, 5, 0, None, 1, 2, 4]
    x = ["a", "b", "c", "d", "e", "f", "g", "h"]
    y = suffix_sums(nxt, x, concat, random.Random(1))
    assert y[3] == "dagcfbhe"
    assert y == walk_suffix(nxt, x)


def test_edges() -> None:
    rng = random.Random(0)
    assert suffix_sums([], [], concat, rng) == []
    assert suffix_sums([None], ["z"], concat, rng) == ["z"]
    assert suffix_sums([None, None], ["p", "q"], concat, rng) == ["p", "q"]


def test_random_against_walk() -> None:
    rng = random.Random(1985)
    for _ in range(600):
        n = rng.choice([0, 1, 2, 3, 4, 7, 8, 9, 16, 31, 32, 50])
        nxt = random_lists(n, rng.randint(1, 4), rng)
        x = [chr(97 + rng.randrange(26)) for _ in range(n)]
        assert suffix_sums(nxt, x, concat, rng) == walk_suffix(nxt, x)


def test_independent_set() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 40)
        nxt = random_lists(n, rng.randint(1, 3), rng)
        r = set(choose(list(range(n)), nxt, rng))
        assert all(nxt[i] is None or nxt[i] not in r for i in r)


def test_fraction_removed() -> None:
    # one list of m nodes: the expected number removed in a round is (m + 1) / 4
    rng = random.Random(11)
    m, trials, total = 1000, 60, 0
    for _ in range(trials):
        nxt = random_lists(m, 1, rng)
        total += len(choose(list(range(m)), nxt, rng))
    mean = total / trials
    assert abs(mean - (m + 1) / 4) < 0.02 * m


def test_round_count() -> None:
    rng = random.Random(4)
    for n in [2, 8, 64, 100, 512, 1000]:
        rounds = []
        for _ in range(30):
            st = Stats()
            nxt = random_lists(n, 1, rng)
            suffix_sums(nxt, [1] * n, lambda a, b: a + b, rng, st)
            rounds.append(len(st.live))
            # no round may remove more than half of the nodes plus the tail
            assert all(r <= (lv + 1) // 2 for lv, r in zip(st.live, st.removed))
        assert sum(rounds) / len(rounds) <= math.log(n, 4 / 3) + 5
