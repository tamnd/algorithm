# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-beam-search/. The authors are listed in prov/ZN2NZT.jsonl.

"""Grid beam search: beam search with phrases that the output must hold (Hokamp and Liu 2017).

A model is a function that takes the prefix y_1 ... y_t (a tuple of strings)
and returns a dict from each token to log p(w | prefix), in natural log. The
end token is the string "</s>". The code takes these log probabilities as
given; it does not run or train a network.

A constraint is a phrase: a non-empty list of tokens that must appear, as a
contiguous block, in the output. The phrases must take disjoint positions.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF

EOS = "</s>"

Model = Callable[[Tuple[str, ...]], Dict[str, float]]


@dataclass(frozen=True)
class Hyp:
    """A partial output. phrase is the index of the open constraint, or -1."""

    tokens: Tuple[str, ...]
    score: float
    covered: Tuple[bool, ...]
    phrase: int = -1
    pos: int = 0


def grid_beam_search(
    model: Model,
    phrases: Sequence[Sequence[str]],
    max_len: int,
    width: int,
    stats: Optional[Dict[str, int]] = None,
) -> Optional[Tuple[List[str], float]]:
    """Return (tokens, log p) of the best finished output that holds every phrase.

    Grid[t][c] holds at most width hypotheses with t tokens, c of which are
    constraint tokens. The output has at most max_len tokens, "</s>"
    included. Return None if no output that holds every phrase is found.
    If stats is a dict, stats["calls"] counts the model calls.
    """
    if width < 1 or max_len < 1:
        raise ValueError("width and max_len must be at least 1")
    phrases = [list(p) for p in phrases]
    if any(len(p) == 0 for p in phrases):
        raise ValueError("a constraint must not be empty")
    if any(EOS in p for p in phrases):
        raise ValueError("a constraint must not contain the end token")
    total = sum(len(p) for p in phrases)
    m = len(phrases)
    grid: List[List[Hyp]] = [[] for _ in range(total + 1)]
    grid[0] = [Hyp((), 0.0, (False,) * m)]  # @line L1
    best: Optional[Tuple[List[str], float]] = None
    calls = 0
    for t in range(1, max_len + 1):  # @line L2
        nxt: List[List[Hyp]] = [[] for _ in range(total + 1)]
        for c in range(total + 1):  # @line L3
            for h in grid[c]:
                logp = model(h.tokens)  # @line L4
                calls += 1
                if h.phrase < 0 and c == total and logp.get(EOS, NEG_INF) > NEG_INF:  # @line L5
                    s = h.score + logp[EOS]
                    if best is None or s > best[1]:
                        best = (list(h.tokens) + [EOS], s)
                if t == max_len:
                    continue
                if h.phrase < 0:
                    for w, lp in logp.items():  # @line L6
                        if w != EOS and lp > NEG_INF:
                            nxt[c].append(Hyp(h.tokens + (w,), h.score + lp, h.covered))
                    for i, p in enumerate(phrases):  # @line L7
                        if not h.covered[i] and logp.get(p[0], NEG_INF) > NEG_INF:
                            nxt[c + 1].append(_advance(h, i, 0, p, logp[p[0]]))
                else:
                    p = phrases[h.phrase]  # @line L8
                    w = p[h.pos]
                    if logp.get(w, NEG_INF) > NEG_INF:
                        nxt[c + 1].append(_advance(h, h.phrase, h.pos, p, logp[w]))
        low = total - (max_len - 1 - t)
        for c in range(total + 1):  # @line L9
            if c < low:
                nxt[c] = []
            else:
                order = sorted(range(len(nxt[c])), key=lambda j: (-nxt[c][j].score, j))
                nxt[c] = [nxt[c][j] for j in order[:width]]
        grid = nxt
    if stats is not None:
        stats["calls"] = calls
    return best  # @line L10


def _advance(h: Hyp, i: int, pos: int, phrase: List[str], lp: float) -> Hyp:
    """Append token pos of phrase i to h, and close the phrase if it is complete."""
    tokens = h.tokens + (phrase[pos],)
    if pos + 1 == len(phrase):
        covered = h.covered[:i] + (True,) + h.covered[i + 1 :]
        return Hyp(tokens, h.score + lp, covered)
    return Hyp(tokens, h.score + lp, h.covered, i, pos + 1)
