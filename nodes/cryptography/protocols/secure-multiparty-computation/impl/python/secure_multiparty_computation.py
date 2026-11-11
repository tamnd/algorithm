# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-multiparty-computation/. The authors are listed in prov/RFTBQB.jsonl.
"""A small harness for the ideal/real paradigm of secure multiparty computation.

The ideal world: each party hands its input to a trusted party, the ideal
functionality, which computes f(x_1, ..., x_n) and hands each party its output.
The real world: the parties run a protocol and exchange messages. Here the
protocol computes a weighted sum modulo M with additive secret sharing:

  round 1: party i splits x_i into n random shares that add up to x_i mod M,
           and sends share j to party j;
  round 2: party j adds the shares it received, and broadcasts that partial sum;
  output : each party adds the n partial sums.

The harness runs both worlds on the same inputs and checks that the outputs
agree. It also records the view of each party (its input, its randomness and
the messages it received), which the semi-honest model uses for simulation.

For study only. The code is not constant time, it uses Python's random module,
and the parties are local objects, not separate machines with private channels.
Use a reviewed MPC framework (for example MP-SPDZ or the libraries listed by
the MPC community) for real data.
"""

import random
from dataclasses import dataclass, field
from typing import Callable, Sequence

Inputs = Sequence[int]


def ideal_world(f: Callable[[Inputs], list[int]], inputs: Inputs) -> list[int]:
    """The trusted party: receive every input, return f's output vector.

    f returns one output per party. Cost: one call to f.
    """
    out = f(list(inputs))
    if len(out) != len(inputs):
        raise ValueError("f must give one output to each party")
    return out


def share_additive(x: int, n: int, modulus: int, rng: random.Random) -> list[int]:
    """Split x into n shares, uniform subject to sum = x mod modulus."""
    shares = [rng.randrange(modulus) for _ in range(n - 1)]
    shares.append((x - sum(shares)) % modulus)
    return shares


@dataclass
class Transcript:
    """What the real run produced: outputs, views, and message counts."""

    outputs: list[int]
    views: list[dict] = field(default_factory=list)
    messages: int = 0
    rounds: int = 0
    field_elements_sent: int = 0


def real_weighted_sum(
    inputs: Inputs, weights: Sequence[int], modulus: int, rng: random.Random
) -> Transcript:
    """Run the two-round additive sharing protocol for sum_i w_i x_i mod modulus.

    Every party learns the result. Cost: n(n-1) point-to-point messages in
    round 1, n(n-1) in round 2 (a broadcast sent as n-1 messages), so
    2n(n-1) messages of one field element each, in 2 rounds.
    """
    n = len(inputs)
    if n < 2 or len(weights) != n:
        raise ValueError("need at least two parties and one weight per party")
    views = [{"input": inputs[i], "sent_shares": None, "received_shares": [None] * n,
              "partials": [None] * n} for i in range(n)]
    messages = 0
    # Round 1: each party shares w_i x_i (the weight is public).
    for i in range(n):
        sh = share_additive(weights[i] * inputs[i] % modulus, n, modulus, rng)
        views[i]["sent_shares"] = sh
        for j in range(n):
            views[j]["received_shares"][i] = sh[j]
            if j != i:
                messages += 1
    # Round 2: each party broadcasts the sum of the shares it holds.
    for j in range(n):
        partial = sum(views[j]["received_shares"]) % modulus
        for k in range(n):
            views[k]["partials"][j] = partial
            if k != j:
                messages += 1
    outputs = [sum(v["partials"]) % modulus for v in views]
    return Transcript(outputs, views, messages, 2, messages)


def weighted_sum_functionality(weights: Sequence[int], modulus: int) -> Callable[[Inputs], list[int]]:
    """The ideal functionality: every party gets sum_i w_i x_i mod modulus."""

    def f(xs: Inputs) -> list[int]:
        y = sum(w * x for w, x in zip(weights, xs)) % modulus
        return [y] * len(xs)

    return f


def harness(inputs: Inputs, weights: Sequence[int], modulus: int, rng: random.Random) -> bool:
    """Run the ideal world and the real protocol on the same inputs.

    Returns True when every party gets the same output in both worlds.
    """
    ideal = ideal_world(weighted_sum_functionality(weights, modulus), inputs)
    real = real_weighted_sum(inputs, weights, modulus, rng)
    return ideal == real.outputs
