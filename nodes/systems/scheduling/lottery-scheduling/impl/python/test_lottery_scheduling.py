# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lottery-scheduling/. The authors are listed in prov/Z4WQ0E.jsonl.

import bisect
from fractions import Fraction

import pytest

from lottery_scheduling import Lottery, lottery_schedule


class FixedDraw:
    """A stand-in generator whose randrange returns a chosen value."""

    def __init__(self) -> None:
        self.value = 0
        self.last_bound = 0

    def randrange(self, bound: int) -> int:
        self.last_bound = bound
        return self.value


def test_each_ticket_number_maps_to_its_holder() -> None:
    # Oracle: binary search over the prefix sums of the scaled tickets.
    fake = FixedDraw()
    lot = Lottery(rng=fake)
    for c, t in [("A", 3), ("B", 0), ("C", 5), ("D", 2)]:
        lot.add(c, t)
    lot.charge("D", Fraction(2, 3))  # D now holds 2 / (2/3) = 3 effective tickets
    lot.draw()
    total = fake.last_bound
    assert total == 3 + 5 + 3  # common denominator 1
    prefix = [3, 3, 8, 11]
    names = ["A", "B", "C", "D"]
    counts = {c: 0 for c in names}
    for w in range(total):
        fake.value = w
        got = lot.draw()
        assert got == names[bisect.bisect_right(prefix, w)]
        counts[got] += 1
    assert counts == {"A": 3, "B": 0, "C": 5, "D": 3}


def test_fractional_compensation_is_exact() -> None:
    fake = FixedDraw()
    lot = Lottery(rng=fake)
    lot.add("A", 1)
    lot.add("B", 1)
    lot.charge("B", Fraction(2, 3))  # B holds 3/2
    lot.draw()
    assert fake.last_bound == 5  # 2 * (1 + 3/2)
    fake.value = 1
    assert lot.draw() == "A"  # scaled tickets: A holds 0 and 1
    fake.value = 2
    assert lot.draw() == "B"  # B holds 2, 3 and 4
    lot.charge("B", Fraction(1))  # a full quantum ends the compensation
    fake.value = 0
    lot.draw()
    assert fake.last_bound == 2


def test_wins_are_binomial() -> None:
    # p = 3/4. Over m runs of n lotteries, the number of wins of A has mean
    # n p = 375 and variance n p (1 - p) = 93.75.
    n, m = 500, 160
    xs = []
    for seed in range(m):
        winners, _ = lottery_schedule({"A": 3, "B": 1}, n, seed=seed)
        xs.append(winners.count("A"))
    mean = sum(xs) / m
    var = sum((x - mean) ** 2 for x in xs) / (m - 1)
    assert abs(mean - 375) < 4 * (93.75 / m) ** 0.5
    assert 0.65 * 93.75 < var < 1.35 * 93.75


def test_response_time_is_geometric() -> None:
    # p = 1/4: the number of lotteries up to and including the next win of C
    # has mean 1/p = 4 and variance (1 - p) / p^2 = 12.
    winners, _ = lottery_schedule({"A": 2, "B": 1, "C": 1}, 40000, seed=7)
    gaps, last = [], -1
    for i, w in enumerate(winners):
        if w == "C":
            gaps.append(i - last)
            last = i
    mean = sum(gaps) / len(gaps)
    var = sum((g - mean) ** 2 for g in gaps) / (len(gaps) - 1)
    assert abs(mean - 4) < 0.15
    assert abs(var - 12) < 1.5
    assert abs(sum(1 for g in gaps if g == 1) / len(gaps) - 0.25) < 0.02


def test_relative_error_falls_with_n() -> None:
    # The error of the share is about sqrt(n p (1 - p)), so the relative
    # error falls like 1 / sqrt(n).
    def mean_abs_err(n: int) -> float:
        errs = []
        for seed in range(40):
            w, _ = lottery_schedule({"A": 1, "B": 1}, n, seed=1000 + seed)
            errs.append(abs(w.count("A") - n / 2))
        return sum(errs) / len(errs)

    small, big = mean_abs_err(100), mean_abs_err(1600)
    assert big > small  # the absolute error grows
    assert big / 1600 < small / 100 / 2  # the relative error falls


def test_compensation_tickets_restore_the_share() -> None:
    # A and B hold 400 tickets each. B uses 1/5 of each quantum.
    use = {"B": Fraction(1, 5)}
    _, cpu = lottery_schedule({"A": 400, "B": 400}, 6000, seed=3, use=use)
    assert 0.9 < cpu["B"] / cpu["A"] < 1.1
    _, cpu = lottery_schedule({"A": 400, "B": 400}, 6000, seed=3, use=use, compensate=False)
    assert 0.17 < cpu["B"] / cpu["A"] < 0.23


def test_transfer_and_inflation() -> None:
    lot = Lottery(seed=11)
    lot.add("client", 100)
    lot.add("server", 0)
    lot.add("other", 100)
    with pytest.raises(ValueError):
        lot.transfer("client", "server", 101)
    lot.transfer("client", "server", 100)  # the client blocks on the server
    assert lot.base == {"client": 0, "server": 100, "other": 100}
    wins = [lot.draw() for _ in range(2000)]
    assert "client" not in wins
    assert 0.45 < wins.count("server") / 2000 < 0.55
    lot.transfer("server", "client", 100)  # the reply returns the tickets
    lot.set_tickets("other", 300)  # inflation
    wins = [lot.draw() for _ in range(4000)]
    assert "server" not in wins
    assert 0.7 < wins.count("other") / 4000 < 0.8


def test_edges() -> None:
    lot = Lottery()
    with pytest.raises(ValueError):
        lot.add("A", -1)
    lot.add("A", 0)
    with pytest.raises(ValueError):
        lot.draw()
    with pytest.raises(ValueError):
        lot.charge("A", Fraction(0))
    assert lottery_schedule({"A": 5}, 3) == (["A"] * 3, {"A": 3})
    assert lottery_schedule({"A": 1, "B": 2}, 50, seed=4) == lottery_schedule({"A": 1, "B": 2}, 50, seed=4)
