# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-recoding/. The authors are listed in prov/K1G2D0.jsonl.

# Oracles: the worked examples of the page, a plain move-to-front list (an
# independent way to get the recency rank), the definitions of the interval
# and the rank by a scan of the history, the inequality rank + 1 <= interval,
# and round trips.

import random

from locality_recoding import (
    interval_decode,
    interval_encode,
    inversion_frequencies,
    inversion_frequencies_decode,
    recency_rank_decode,
    recency_rank_encode,
)


def mtf(x, alphabet):
    table, out = list(alphabet), []
    for s in x:
        r = table.index(s)
        out.append(r)
        table.insert(0, table.pop(r))
    return out


def by_definition(x, alphabet):
    history = list(reversed(alphabet))
    sigma = len(alphabet)
    intervals, ranks = [], []
    for t, s in enumerate(x):
        j = max(i for i, h in enumerate(history) if h == s)
        intervals.append(t + sigma - j)
        ranks.append(len(set(history[j + 1 :])))
        history.append(s)
    return intervals, ranks


def random_cases():
    rng = random.Random(1987)
    out = [("", "ab"), ("a", "a"), ("aaaa", "ab"), ("abracadabra", "abcdr")]
    for _ in range(300):
        alphabet = "abcdefgh"[: rng.randrange(1, 9)]
        n = rng.randrange(0, 40)
        out.append(("".join(rng.choice(alphabet) for _ in range(n)), alphabet))
    return out


def test_worked_example() -> None:
    x, a = "abracadabra", "abcdr"
    assert interval_encode(x, a) == [1, 3, 7, 3, 7, 2, 10, 2, 7, 7, 3]
    assert recency_rank_encode(x, a) == [0, 1, 4, 2, 3, 1, 4, 1, 4, 4, 2]
    assert inversion_frequencies(x, a) == [[0, 2, 1, 1, 2], [0, 3], [1], [1], [0, 0]]


def test_against_definitions() -> None:
    for x, a in random_cases():
        intervals, ranks = by_definition(x, a)
        assert interval_encode(x, a) == intervals
        assert recency_rank_encode(x, a) == ranks == mtf(x, a)


def test_rank_below_interval() -> None:
    for x, a in random_cases():
        for r, d in zip(recency_rank_encode(x, a), interval_encode(x, a)):
            assert r + 1 <= d


def test_round_trips() -> None:
    for x, a in random_cases():
        assert "".join(interval_decode(interval_encode(x, a), a)) == x
        assert "".join(recency_rank_decode(recency_rank_encode(x, a), a)) == x
        assert "".join(inversion_frequencies_decode(inversion_frequencies(x, a), a)) == x


def test_runs_give_ones_and_zeros() -> None:
    x = "a" * 50 + "b" * 50
    assert interval_encode(x, "ab")[51:] == [1] * 49
    assert recency_rank_encode(x, "ab")[51:] == [0] * 49


def test_large_input_is_fast() -> None:
    rng = random.Random(2)
    alphabet = list(range(1000))
    x = [rng.choice(alphabet[:50]) if rng.random() < 0.9 else rng.choice(alphabet) for _ in range(20000)]
    assert interval_decode(interval_encode(x, alphabet), alphabet) == x
    assert recency_rank_encode(x, alphabet) == mtf(x, alphabet)
