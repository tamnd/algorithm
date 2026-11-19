# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repetition-penalty/. The authors are listed in prov/9K28B7.jsonl.

"""Three forms of the repetition penalty on next-token logits.

Tokens are integers 0 ... |V| - 1, the logits are a list of |V| floats, and
the history is the list of tokens so far (the prompt and the output, or
only the output; the caller chooses). Each function returns a new list of
logits and does not change its input. The code takes the logits of the
model as given; it does not run or train a network.
"""

from collections import Counter
from typing import List, Sequence


def ctrl_penalty(logits: Sequence[float], history: Sequence[int], theta: float) -> List[float]:
    """Divide the logit of every token in the history by theta, as written in CTRL.

    With theta > 1 this lowers a positive logit but raises a negative one,
    so on its own it can make a repeated token more likely.
    """
    seen = set(history)
    return [x / theta if j in seen else x for j, x in enumerate(logits)]


def scaled_penalty(logits: Sequence[float], history: Sequence[int], theta: float) -> List[float]:
    """The sign-aware scaling of common libraries: divide positive logits, multiply negative ones.

    With theta >= 1 the logit of a token in the history never goes up.
    """
    if not theta > 0:
        raise ValueError("theta must be positive")
    seen = set(history)  # @line L1
    out = list(logits)
    for j in seen:  # @line L2
        out[j] = out[j] / theta if out[j] > 0 else out[j] * theta  # @line L3
    return out  # @line L5


def additive_penalty(
    logits: Sequence[float], history: Sequence[int], frequency: float, presence: float
) -> List[float]:
    """Subtract count * frequency + presence from the logit of every token in the history.

    This is the form z_j - c_j * alpha_frequency - [c_j > 0] * alpha_presence.
    """
    counts = Counter(history)  # @line L1
    out = list(logits)
    for j, c in counts.items():  # @line L2
        out[j] = out[j] - c * frequency - presence  # @line L4
    return out  # @line L5
