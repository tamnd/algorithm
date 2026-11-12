# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lottery-scheduling/. The authors are listed in prov/Z4WQ0E.jsonl.

import random
from fractions import Fraction
from math import lcm
from typing import Optional


class Lottery:
    """Lottery scheduling of Waldspurger and Weihl (OSDI 1994).

    Each client holds an integer number of base tickets. A draw picks a
    uniform ticket number among all effective tickets and walks the client
    list to find its holder. A client that used only a fraction f < 1 of its
    last quantum holds a compensation ticket, so that its effective tickets
    are base / f until it wins again. Exact: effective tickets are Fractions,
    and the draw scales them to integers by their common denominator.
    """

    def __init__(self, seed: int = 0, rng: Optional[random.Random] = None) -> None:
        self.rng = rng if rng is not None else random.Random(seed)
        self.order: list[str] = []  # the list that the draw walks
        self.base: dict[str, int] = {}
        self.eff: dict[str, Fraction] = {}

    def add(self, name: str, tickets: int) -> None:
        if name in self.base or tickets < 0:
            raise ValueError("new client with a non-negative ticket count")
        self.order.append(name)
        self.base[name] = tickets
        self.eff[name] = Fraction(tickets)  # @line L1

    def remove(self, name: str) -> None:
        self.order.remove(name)
        del self.base[name], self.eff[name]

    def set_tickets(self, name: str, tickets: int) -> None:
        """Ticket inflation (more tickets) or deflation (fewer tickets)."""
        if tickets < 0:
            raise ValueError("negative tickets")
        self.base[name] = tickets
        self.eff[name] = Fraction(tickets)

    def transfer(self, src: str, dst: str, amount: int) -> None:
        """Move base tickets, for example from a client blocked on a server
        to the server. Any compensation of the two clients ends."""
        if not 0 <= amount <= self.base[src]:
            raise ValueError("cannot transfer more tickets than src holds")
        self.base[src] -= amount
        self.base[dst] += amount
        self.eff[src] = Fraction(self.base[src])
        self.eff[dst] = Fraction(self.base[dst])

    def draw(self) -> str:
        den = lcm(*(e.denominator for e in self.eff.values()))
        scaled = [self.eff[c].numerator * (den // self.eff[c].denominator) for c in self.order]
        total = sum(scaled)  # @line L3
        if total == 0:
            raise ValueError("no tickets")
        w = self.rng.randrange(total)  # @line L4
        s = 0
        for c, x in zip(self.order, scaled):  # @line L5
            s += x
            if w < s:
                return c
        raise AssertionError("unreachable")

    def charge(self, name: str, used: Fraction, compensate: bool = True) -> None:
        """Record that the winner used the fraction `used` of its quantum."""
        if not 0 < used <= 1:
            raise ValueError("used must be in (0, 1]")
        if compensate and used < 1:  # @line L7
            self.eff[name] = Fraction(self.base[name]) / used
        else:  # @line L8
            self.eff[name] = Fraction(self.base[name])


def lottery_schedule(
    tickets: dict[str, int],
    n: int,
    seed: int = 0,
    use: Optional[dict[str, Fraction]] = None,
    compensate: bool = True,
) -> tuple[list[str], dict[str, Fraction]]:
    """Hold n lotteries. use[c] is the fraction of a quantum that client c
    uses each time it runs (default 1). Return the winners in order and the
    CPU time (in quanta) that each client received."""
    lot = Lottery(seed)
    for c, t in tickets.items():
        lot.add(c, t)
    use = use or {}
    winners: list[str] = []
    cpu = {c: Fraction(0) for c in tickets}
    for _ in range(n):  # @line L2
        c = lot.draw()
        f = Fraction(use.get(c, 1))
        winners.append(c)
        cpu[c] += f  # @line L6
        lot.charge(c, f, compensate)
    return winners, cpu
