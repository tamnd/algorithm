# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/break-even-strategy/. The authors are listed in prov/04HWFP.jsonl.

import random
from fractions import Fraction
from numbers import Rational


class BreakEven:
    """The break-even rule for rent or buy. Call day() once for each new day."""

    def __init__(self, rent: Rational, price: Rational) -> None:
        if rent <= 0 or price <= 0:
            raise ValueError("rent and price must be positive")
        self.rent = rent
        self.price = price
        self.paid = 0  # @line L1
        self.owned = False
        self.cost = 0

    def day(self) -> str:
        """Serve one more day. Return "own", "buy" or "rent"."""
        if self.owned:  # @line L3
            return "own"
        if self.paid + self.rent >= self.price:  # @line L4
            self.owned = True
            self.cost += self.price
            return "buy"
        self.paid += self.rent  # @line L5
        self.cost += self.rent
        return "rent"


def break_even_cost(n: int, rent: Rational, price: Rational) -> Rational:
    """Total cost of the break-even rule on a season of n days."""
    alg = BreakEven(rent, price)
    for _ in range(n):  # @line L2
        alg.day()
    return alg.cost


def buy_day_cost(n: int, j: int | None, rent: Rational = 1, price: Rational = 1) -> Rational:
    """Cost of the rule "rent on days 1 .. j - 1, buy on day j" on n days. j = None never buys."""
    if j is None or n < j:
        return n * rent
    return (j - 1) * rent + price


def opt_cost(n: int, rent: Rational, price: Rational) -> Rational:
    """The offline optimum: rent every day or buy on day 1."""
    return min(n * rent, price) if n > 0 else 0


def worst_ratio(j: int | None, b: int) -> Fraction | None:
    """Exact max over n >= 1 of the ratio of "buy on day j" with rent 1 and price b. None if unbounded."""
    if j is None:
        return None
    # For n >= max(j, b) both costs are constant, so these n are enough.
    return max(Fraction(buy_day_cost(n, j, 1, b), opt_cost(n, 1, b)) for n in range(1, max(j, b) + 1))


def randomized_distribution(b: int) -> list[Fraction]:
    """Probabilities of buying on day 1 .. b in the optimal randomized rule of Karlin et al."""
    q = Fraction(b - 1, b)
    c = 1 / (1 - q**b)
    return [c / b * q ** (b - i) for i in range(1, b + 1)]


def randomized_ratio(b: int) -> Fraction:
    """The strict ratio 1 / (1 - (1 - 1/b)^b) of the randomized rule."""
    return 1 / (1 - Fraction(b - 1, b) ** b)


def randomized_expected_cost(n: int, b: int) -> Fraction:
    """Exact expected cost of the randomized rule on n days, rent 1 and price b."""
    dist = randomized_distribution(b)
    return sum((p * buy_day_cost(n, j, 1, b) for j, p in enumerate(dist, start=1)), Fraction(0))


def sample_buy_day(b: int, rng: random.Random) -> int:
    """Draw a buy day from the randomized rule."""
    u = Fraction(rng.random())
    acc = Fraction(0)
    dist = randomized_distribution(b)
    for j, p in enumerate(dist, start=1):
        acc += p
        if u < acc:
            return j
    return b
