# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-backoff/. The authors are listed in prov/SRY509.jsonl.

import random
from itertools import islice

import pytest

from exponential_backoff import JITTERS, backoff_delays, contention, retry


def test_plain_delays_double_then_cap() -> None:
    assert list(islice(backoff_delays(1, 100, "none"), 10)) == [1, 2, 4, 8, 16, 32, 64, 100, 100, 100]
    assert list(islice(backoff_delays(1, 1000, "none", factor=3), 4)) == [1, 3, 9, 27]


@pytest.mark.parametrize("n", [1, 5, 12])
def test_total_wait_is_geometric_sum(n: int) -> None:
    assert sum(islice(backoff_delays(1, 2**20, "none"), n)) == 2**n - 1
    assert sum(islice(backoff_delays(0.25, 2**20, "none"), n)) == 0.25 * (2**n - 1)


def test_jitter_ranges() -> None:
    rng = random.Random(1)
    base, cap = 0.1, 20.0
    for jitter in ("full", "equal"):
        for n, d in enumerate(islice(backoff_delays(base, cap, jitter, rng), 40)):
            v = min(cap, base * 2**n)
            lo = 0 if jitter == "full" else v / 2
            assert lo <= d <= v
    prev = base
    for d in islice(backoff_delays(base, cap, "decorrelated", rng), 200):
        assert base <= d <= min(cap, 3 * prev)
        prev = d


def test_full_jitter_mean_is_half() -> None:
    rng = random.Random(7)
    k, trials = 6, 20000
    mean = sum(list(islice(backoff_delays(1, 1000, "full", rng), k + 1))[k] for _ in range(trials)) / trials
    assert abs(mean - 32) < 1


def test_retry_succeeds_on_fifth_attempt() -> None:
    out = retry(lambda n: n == 4, 1, 100, 10, "none")
    assert out == (True, 5, 15)  # waited 1 + 2 + 4 + 8


def test_retry_gives_up() -> None:
    calls = []
    out = retry(lambda n: calls.append(n) or False, 1, 8, 6, "none")
    assert out == (False, 6, 1 + 2 + 4 + 8 + 8)
    assert calls == [0, 1, 2, 3, 4, 5]


def test_synchronized_clients_without_jitter_never_succeed() -> None:
    res = contention(20, "none", random.Random(0), max_attempts=30)
    assert res.finished == 0 and res.calls == 20 * 30


@pytest.mark.parametrize("jitter", ["full", "equal", "decorrelated"])
def test_jitter_breaks_the_synchrony(jitter: str) -> None:
    for seed in range(20):
        res = contention(20, jitter, random.Random(seed))
        assert res.finished == 20, (jitter, seed)
        assert res.calls < 300


def test_bad_arguments() -> None:
    assert "none" in JITTERS
    with pytest.raises(ValueError):
        next(backoff_delays(1, 10, "half"))
    with pytest.raises(ValueError):
        next(backoff_delays(5, 1, "full"))
