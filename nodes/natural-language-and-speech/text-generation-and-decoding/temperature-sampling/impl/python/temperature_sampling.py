# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temperature-sampling/. The authors are listed in prov/C3YE2Y.jsonl.

"""Temperature sampling of the next token.

The input is a list of logits z, one per token of the vocabulary, in the
order of the vocabulary. A logit of float("-inf") means a token that is
not allowed. The random source is any object with a random() method that
returns u in [0, 1), such as random.Random(seed). The code takes the logits
of the model as given; it does not run or train a network.
"""

import math
from typing import List, Sequence

from nlslog import NEG_INF, softmax


def temperature_distribution(logits: Sequence[float], temperature: float) -> List[float]:
    """Return softmax(z / T), computed after subtracting the largest logit."""
    return softmax(logits, temperature)


def temperature_sample(logits: Sequence[float], temperature: float, rng) -> int:
    """Draw one token index from softmax(z / T) without forming the normalized list.

    The weights exp((z_i - m) / T) are at most 1, so nothing overflows, and
    r = u Z replaces the division by Z.
    """
    if not temperature > 0:
        raise ValueError("the temperature must be positive")
    m = max(logits)  # @line L1
    if m == NEG_INF:
        raise ValueError("every logit is -inf")
    w = [math.exp((x - m) / temperature) for x in logits]  # @line L2
    z = math.fsum(w)  # @line L3
    r = rng.random() * z  # @line L4
    c = 0.0
    for i, x in enumerate(w):  # @line L5
        c += x
        if r < c:
            return i
    return max(i for i, x in enumerate(w) if x > 0)


def limit_distribution(logits: Sequence[float], which: str) -> List[float]:
    """Return the limit of softmax(z / T) as T goes to 0 ("zero") or to infinity ("inf").

    As T goes to 0, the mass goes uniformly to the tokens of largest logit.
    As T grows, it goes uniformly to the tokens of finite logit.
    """
    m = max(logits)
    if which == "zero":
        keep = [x == m for x in logits]
    elif which == "inf":
        keep = [x != NEG_INF for x in logits]
    else:
        raise ValueError("which must be 'zero' or 'inf'")
    n = sum(keep)
    return [1.0 / n if k else 0.0 for k in keep]
