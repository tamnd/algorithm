# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrastive-search/. The authors are listed in prov/AYJ2SK.jsonl.

"""Contrastive search (Su et al. 2022) over a given model.

Tokens are integers 0 ... |V| - 1. A model is a function that takes a
sequence of tokens (a tuple of ints) and returns a pair (probs, states):
probs is the next-token distribution, a list of |V| probabilities, and
states is a list with one hidden-state vector (a sequence of floats) per
position of the input. The state of position j may depend only on the
tokens up to j. The code takes these values as given; it does not run or
train a network.
"""

import math
from typing import Callable, List, Optional, Sequence, Tuple

Vector = Sequence[float]
Model = Callable[[Tuple[int, ...]], Tuple[Sequence[float], Sequence[Vector]]]


def cosine(a: Vector, b: Vector) -> float:
    """Return the cosine similarity of a and b, and 0 if either has length 0."""
    na = math.sqrt(math.fsum(x * x for x in a))
    nb = math.sqrt(math.fsum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return math.fsum(x * y for x, y in zip(a, b)) / (na * nb)


def top_k_candidates(probs: Sequence[float], k: int) -> List[int]:
    """Return the min(k, |V|) most probable tokens, from high to low, smaller index first on ties."""
    if k < 1:
        raise ValueError("k must be at least 1")
    return sorted(range(len(probs)), key=lambda i: (-probs[i], i))[: min(k, len(probs))]


def degeneration_penalty(state: Vector, context: Sequence[Vector]) -> float:
    """Return the largest cosine similarity of state to a context state, 0 for no context."""
    return max((cosine(state, h) for h in context), default=0.0)


def contrastive_step(
    probs: Sequence[float],
    cand_states: Sequence[Vector],
    context: Sequence[Vector],
    candidates: Sequence[int],
    alpha: float,
) -> Tuple[int, List[float]]:
    """Choose one token among the candidates by the contrastive score.

    cand_states[j] is the hidden state of candidates[j] when it is appended
    to the prefix. The score is (1 - alpha) p(v) - alpha * max cosine to the
    context states. The first candidate (the more probable one) wins ties.
    Return the chosen token and the list of scores.
    """
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be in [0, 1]")
    scores = []
    for v, h in zip(candidates, cand_states):  # @line L5
        scores.append((1 - alpha) * probs[v] - alpha * degeneration_penalty(h, context))  # @line L7
    best = 0
    for j in range(1, len(scores)):  # @line L8
        if scores[j] > scores[best]:
            best = j
    return candidates[best], scores


def contrastive_search(
    model: Model,
    prompt: Sequence[int],
    max_len: int,
    k: int,
    alpha: float,
    eos: Optional[int] = None,
) -> List[int]:
    """Return the prompt followed by up to max_len tokens chosen by contrastive search.

    Each step calls the model once on the prefix and once on each of the k
    candidate extensions, k + 1 calls in all. The search stops after the
    token eos, if eos is given. With alpha = 0 or k = 1 it is greedy decoding.
    """
    y = list(prompt)  # @line L1
    for _ in range(max_len):  # @line L2
        probs, context = model(tuple(y))  # @line L3
        cands = top_k_candidates(probs, k)  # @line L4
        cand_states = [model(tuple(y) + (v,))[1][-1] for v in cands]  # @line L6
        w, _ = contrastive_step(probs, cand_states, context, cands, alpha)  # @line L8
        y.append(w)  # @line L9
        if w == eos:  # @line L10
            return y
    return y  # @line L11
