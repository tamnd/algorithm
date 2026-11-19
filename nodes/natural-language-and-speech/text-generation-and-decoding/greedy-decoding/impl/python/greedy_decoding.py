# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-decoding/. The authors are listed in prov/61Q9XF.jsonl.

"""Greedy decoding of an autoregressive model.

A model is a function that takes the prefix y_1 ... y_t (a tuple of strings)
and returns a dict from each token of the vocabulary to log p(w | prefix),
in natural log. The end token is the string "</s>". The input x of a
conditional model is fixed inside the function. The code takes these log
probabilities as given; it does not run or train a network.
"""

from typing import Callable, Dict, List, Tuple

from nlslog import argmax

EOS = "</s>"

Model = Callable[[Tuple[str, ...]], Dict[str, float]]


def greedy_decode(model: Model, max_len: int) -> Tuple[List[str], float]:
    """Return (tokens, log probability) of the greedy output.

    At each step the decoder appends the most probable next token (the first
    one in the order of the dict, on ties) and stops after "</s>". If no
    "</s>" comes within max_len tokens, the unfinished prefix of max_len
    tokens is returned with its log probability.
    """
    if max_len < 1:
        raise ValueError("max_len must be at least 1")
    y: List[str] = []
    score = 0.0  # @line L1
    for _ in range(max_len):  # @line L2
        logp = model(tuple(y))  # @line L3
        tokens = list(logp)
        w = tokens[argmax([logp[t] for t in tokens])]  # @line L4
        y.append(w)
        score += logp[w]  # @line L5
        if w == EOS:  # @line L6
            return y, score
    return y, score  # @line L7
