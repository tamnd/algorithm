# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-honest-model/. The authors are listed in prov/ZHSBS2.jsonl.
"""Views and simulators in the semi-honest model, on two small sum protocols.

A semi-honest party runs the protocol as written and then studies its view:
its input, its random choices and every message it received. A protocol is
secure for a coalition I if a simulator, given only the inputs of I and the
outputs of I, can produce views with the same distribution.

Two protocols compute x_1 + ... + x_n mod M:
  * additive_sum: each party splits its input into n additive shares (secure);
  * ring_sum: party 1 sends x_1 to party 2, party 2 sends x_1 + x_2 to party 3,
    and so on (correct, but party 2 sees x_1; no simulator exists).

The functions enumerate all random choices on tiny moduli, so the tests can
compare exact distributions. For study only: not constant time, local parties,
and Python's random module. Use a maintained MPC framework for real data.
"""

import itertools
from collections import Counter
from fractions import Fraction
from typing import Sequence

View = tuple


def additive_sum_view(
    inputs: Sequence[int], coins: Sequence[Sequence[int]], coalition: Sequence[int], m: int
) -> View:
    """The joint view of the coalition in the two-round additive sharing sum.

    coins[i] holds the n-1 random shares of party i; its last share is
    x_i minus their sum. The view is: for each corrupted party, its input,
    its coins and the shares it received; then the n broadcast partial sums.
    """
    n = len(inputs)
    shares = [list(coins[i]) + [(inputs[i] - sum(coins[i])) % m] for i in range(n)]
    partials = tuple(sum(shares[i][j] for i in range(n)) % m for j in range(n))
    view = []
    for j in coalition:
        received = tuple(shares[i][j] for i in range(n))
        view.append((inputs[j], tuple(coins[j]), received))
    return tuple(view) + (partials,)


def additive_sum_simulator(
    coalition_inputs: dict[int, int], y: int, n: int, sim_coins: Sequence[int], m: int
) -> View:
    """Make a view from the coalition's inputs and the output y alone.

    sim_coins supplies the simulator's random values: first the coins of each
    corrupted party, then one share from each honest party to each corrupted
    party, then the partial sums of all honest parties but the last. The last
    honest partial sum is fixed so that the partial sums add up to y.
    Precondition: at least one party is honest.
    """
    coalition = sorted(coalition_inputs)
    honest = [i for i in range(n) if i not in coalition_inputs]
    it = iter(sim_coins)
    own = {j: [next(it) for _ in range(n - 1)] for j in coalition}
    own_shares = {j: own[j] + [(coalition_inputs[j] - sum(own[j])) % m] for j in coalition}
    from_honest = {(i, j): next(it) for i in honest for j in coalition}
    received = {j: tuple(own_shares[i][j] if i in own_shares else from_honest[(i, j)]
                         for i in range(n)) for j in coalition}
    partials = [None] * n
    for j in coalition:
        partials[j] = sum(received[j]) % m
    for i in honest[:-1]:
        partials[i] = next(it)
    partials[honest[-1]] = (y - sum(p for p in partials if p is not None)) % m
    view = [(coalition_inputs[j], tuple(own[j]), received[j]) for j in coalition]
    return tuple(view) + (tuple(partials),)


def simulator_coin_count(n: int, t: int) -> int:
    """Number of random values the simulator uses for a coalition of size t."""
    return t * (n - 1) + (n - t) * t + (n - t - 1)


def distribution(views: list[View]) -> dict[View, Fraction]:
    """Turn a list of equally likely views into a probability table."""
    c = Counter(views)
    total = len(views)
    return {v: Fraction(k, total) for v, k in c.items()}


def real_distribution(inputs: Sequence[int], coalition: Sequence[int], m: int) -> dict[View, Fraction]:
    """Exact distribution of the coalition's view, over all coins of all parties."""
    n = len(inputs)
    views = []
    for flat in itertools.product(range(m), repeat=n * (n - 1)):
        coins = [flat[i * (n - 1):(i + 1) * (n - 1)] for i in range(n)]
        views.append(additive_sum_view(inputs, coins, coalition, m))
    return distribution(views)


def simulated_distribution(
    coalition_inputs: dict[int, int], y: int, n: int, m: int
) -> dict[View, Fraction]:
    """Exact distribution of the simulator's output, over all its coins."""
    k = simulator_coin_count(n, len(coalition_inputs))
    views = [additive_sum_simulator(coalition_inputs, y, n, c, m)
             for c in itertools.product(range(m), repeat=k)]
    return distribution(views)


def leaky_coin_joint(coin: int) -> tuple[int, int]:
    """A randomized functionality: party 1 gets a random bit, party 2 gets nothing.

    The bad protocol: party 1 picks the bit, outputs it and also sends it to
    party 2. Returns (output of party 1, view of party 2) for one coin.
    """
    return (coin, coin)


def ideal_coin_joint(coin: int, sim_coin: int) -> tuple[int, int]:
    """Ideal world plus the best simulator for party 2, which knows nothing
    about party 1's bit and outputs its own random bit."""
    return (coin, sim_coin)


def ring_sum_view_of_party(inputs: Sequence[int], party: int, m: int) -> View:
    """View of one party in the ring protocol: its input, the running sum it
    received (none for party 0), and the final sum. The protocol uses no coins."""
    running = 0
    received = None
    for i, x in enumerate(inputs):
        if i == party:
            received = running if i > 0 else None
        running = (running + x) % m
    return (inputs[party], received, running)
