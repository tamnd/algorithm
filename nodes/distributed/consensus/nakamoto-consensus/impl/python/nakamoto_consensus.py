# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nakamoto-consensus/. The authors are listed in prov/XQ55B7.jsonl.

"""Nakamoto consensus: the most-work chain rule, its double-spend analysis and selfish mining.

Three parts:

1. A round-based simulator of honest miners. Each miner extends the tip of the
   chain with the most work that it knows, and a block reaches the other miners
   after a delay. It shows forks and the common prefix property.
2. The double-spend probability of the Bitcoin white paper (Section 11): the
   gambler's ruin catch-up probability, the Poisson formula, the exact form
   with the negative binomial, and seeded simulations of the race.
3. The selfish mining strategy of Eyal and Sirer as a Markov chain, simulated.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Optional

# ---------------------------------------------------------------- the protocol


class Block:
    __slots__ = ("bid", "parent", "height", "work", "miner")

    def __init__(self, bid: int, parent: Optional["Block"], work: int, miner: int) -> None:
        self.bid, self.parent, self.miner = bid, parent, miner
        self.height = 0 if parent is None else parent.height + 1
        self.work = work if parent is None else parent.work + work  # total work of the chain


def chain_of(tip: Block) -> list[int]:
    out = []
    b: Optional[Block] = tip
    while b is not None:
        out.append(b.bid)
        b = b.parent
    return out[::-1]


def better(a: Block, b: Block) -> bool:
    """Most-work rule: does tip a carry strictly more total work than tip b?"""
    return a.work > b.work  # @line L4


def simulate(miners: int, p: float, delay: int, rounds: int, seed: int,
             work: int = 1) -> tuple[list[Block], list[Block]]:
    """Honest miners in synchronous rounds. Each finds a block with probability p per round.

    A block found in round r reaches the other miners at round r + delay. Returns the
    final tips of all miners and every block mined.
    """
    rng = random.Random(seed)
    genesis = Block(0, None, 0, -1)
    tips = [genesis] * miners  # @line L1
    inbox: list[list[tuple[int, Block]]] = [[] for _ in range(miners)]
    blocks = [genesis]
    for r in range(rounds):
        for i in range(miners):
            arrived = [b for (t, b) in inbox[i] if t <= r]
            inbox[i] = [(t, b) for (t, b) in inbox[i] if t > r]
            for b in arrived:
                if better(b, tips[i]):
                    tips[i] = b
        for i in range(miners):
            if rng.random() < p:  # @line L2
                b = Block(len(blocks), tips[i], work, i)  # @line L3
                blocks.append(b)
                tips[i] = b
                for j in range(miners):
                    if j != i:
                        inbox[j].append((r + delay, b))
    return tips, blocks


def common_prefix(tips: list[Block], k: int) -> bool:
    """Is every chain, with its last k blocks removed, a prefix of every other chain?"""
    chains = [chain_of(t) for t in tips]
    for a in chains:
        cut = a[: max(1, len(a) - k)]  # @line L5
        for b in chains:
            if b[: len(cut)] != cut:
                return False
    return True


# ------------------------------------------------------ the double-spend race


def catch_up(q: Fraction, z: int) -> Fraction:
    """Probability that an attacker with share q ever catches up from z blocks behind."""
    p = 1 - q
    return Fraction(1) if p <= q else (q / p) ** z


def ruin_finite(q: Fraction, z: int, n: int) -> Fraction:
    """Probability of reaching deficit 0 before deficit n, from deficit z (gambler's ruin)."""
    p = 1 - q
    if p == q:
        return 1 - Fraction(z, n)
    r = q / p
    return (r ** z - r ** n) / (1 - r ** n)


def attacker_success(q: float, z: int) -> float:
    """The white paper formula: attacker progress is Poisson with mean z q / p."""
    p = 1.0 - q
    lam = z * (q / p)
    total, poisson = 1.0, math.exp(-lam)
    for k in range(z + 1):
        if k > 0:
            poisson *= lam / k  # lam^k e^-lam / k!, built step by step to avoid overflow
        total -= poisson * (1 - (q / p) ** (z - k))
    return total


def attacker_success_exact(q: float, z: int) -> float:
    """Same race, with the exact negative binomial count of attacker blocks."""
    p = 1.0 - q
    total = 1.0
    for k in range(z + 1):
        nb = math.comb(k + z - 1, k) * p ** z * q ** k if z > 0 else float(k == 0)
        total -= nb * (1 - (q / p) ** (z - k))
    return total


def min_z(q: float, bound: float = 0.001) -> int:
    z = 0
    while attacker_success(q, z) >= bound:
        z += 1
    return z


def _walk(rng: random.Random, q: float, deficit: int, cap: int) -> bool:
    while 0 < deficit < cap:
        deficit += -1 if rng.random() < q else 1
    return deficit <= 0


def simulate_race(q: float, z: int, trials: int, seed: int, poisson: bool, cap: int = 60) -> float:
    """Seeded estimate of the success probability.

    poisson=True follows the paper's model (attacker progress drawn from a Poisson law);
    poisson=False plays every block: the attacker mines from the time of the payment, the
    merchant waits for z honest blocks, then the race goes on.
    """
    rng = random.Random(seed)
    lam = z * q / (1 - q)
    wins = 0
    for _ in range(trials):
        if poisson:
            k, acc, lim = 0, rng.random(), math.exp(-lam)
            while acc > lim:
                k += 1
                acc *= rng.random()
        else:
            k = h = 0
            while h < z:
                if rng.random() < q:
                    k += 1
                else:
                    h += 1
        wins += _walk(rng, q, z - k, cap)
    return wins / trials


# ----------------------------------------------------------- selfish mining


def selfish_revenue(alpha: float, gamma: float) -> float:
    """Eyal and Sirer: the pool's share of the blocks in the main chain."""
    a, g = alpha, gamma
    num = a * (1 - a) ** 2 * (4 * a + g * (1 - 2 * a)) - a ** 3
    den = 1 - a * (1 + (2 - a) * a)
    return num / den


def simulate_selfish(alpha: float, gamma: float, events: int, seed: int) -> float:
    """Play the selfish mining state machine; return the pool's share of main-chain blocks."""
    rng = random.Random(seed)
    lead, tie = 0, False
    pool = honest = 0
    for _ in range(events):
        mine = rng.random() < alpha
        if tie:  # two branches of length one compete: the pool's and the honest one
            if mine:
                pool += 2
            elif rng.random() < gamma:
                pool += 1
                honest += 1
            else:
                honest += 2
            tie, lead = False, 0
        elif mine:
            lead += 1
        elif lead == 0:
            honest += 1
        elif lead == 1:
            tie, lead = True, 0  # the pool publishes its block
        elif lead == 2:
            pool += 2  # the pool publishes both blocks and wins
            lead = 0
        else:
            pool += 1  # the pool publishes one block; it stays ahead
            lead -= 1
    return pool / (pool + honest)
