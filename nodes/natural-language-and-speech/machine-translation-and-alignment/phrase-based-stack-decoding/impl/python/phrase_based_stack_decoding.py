# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phrase-based-stack-decoding/. The authors are listed in prov/7R5WTX.jsonl.

"""Multi-stack beam decoding for a phrase-based translation model (Koehn 2004).

The source f has m words. A span (s, t) is fencepost: it covers f[s + 1 .. t]
(f[s:t] in Python). The model scores a derivation, a sequence of phrase
translations (s_k, t_k, target_k) that covers every source word once, by

    sum_k tm(f[s_k:t_k] -> target_k)
    + lm_weight * log p_lm(<s> e </s>)            (a bigram model, natural log)
    - distortion_weight * sum_k |s_k - t_{k-1}|    (t_0 = 0)
    + word_penalty * |e|

where e is the concatenation of the targets. Stack c holds the hypotheses that
cover c source words. A hypothesis is recombined with another one that has the
same coverage, the same last target word and the same end of its last phrase.
Each stack is pruned to the best `stack_size` hypotheses and to those within
`threshold` of the best, ranked by score plus future cost. With no pruning the
decoder returns a best derivation of the model (see the correctness proof).
"""

import itertools
import math
from dataclasses import dataclass
from typing import Optional

Phrase = tuple[str, ...]
PhraseTable = dict[Phrase, list[tuple[Phrase, float]]]
NEG_INF = float("-inf")


class BigramLM:
    """A bigram language model in natural log. Unseen bigrams get `floor`."""

    def __init__(self, logprobs: dict[tuple[str, str], float], floor: float = -10.0) -> None:
        self.logprobs = dict(logprobs)
        self.floor = floor
        best: dict[str, float] = {}
        for (_, w), lp in self.logprobs.items():
            best[w] = max(best.get(w, floor), lp)
        self._best_first = best

    def logprob(self, prev: str, w: str) -> float:
        return self.logprobs.get((prev, w), self.floor)

    def estimate(self, phrase: Phrase) -> float:
        """LM estimate of a phrase out of context: the first word gets its best
        score over all histories, the others their bigram score inside the phrase."""
        if not phrase:
            return 0.0
        total = self._best_first.get(phrase[0], self.floor)
        for a, b in zip(phrase, phrase[1:]):
            total += self.logprob(a, b)
        return total


@dataclass
class Model:
    table: PhraseTable
    lm: BigramLM
    lm_weight: float = 1.0
    distortion_weight: float = 0.5
    word_penalty: float = 0.0
    max_phrase_len: int = 7
    distortion_limit: Optional[int] = None  # None means unrestricted reordering


@dataclass
class Hyp:
    score: float
    coverage: int  # bit s is set when f[s] (0-based) is covered
    last: str  # last target word, "<s>" at the start
    end: int  # end t of the last source phrase, 0 at the start
    back: Optional["Hyp"]
    step: Optional[tuple[int, int, Phrase]]


def translation_options(f: list[str], model: Model) -> list[tuple[int, int, Phrase, float]]:
    """Every (s, t, target, tm score) whose source phrase f[s:t] is in the table."""
    m = len(f)
    opts = []
    for s in range(m):
        for t in range(s + 1, min(m, s + model.max_phrase_len) + 1):
            for target, tm in model.table.get(tuple(f[s:t]), []):
                opts.append((s, t, target, tm))
    return opts


def future_cost_table(f: list[str], model: Model) -> list[list[float]]:
    """fc[s][t]: the best estimated score of translating f[s:t] alone, in any
    monotone segmentation, without distortion. -inf if no segmentation exists."""
    m = len(f)
    fc = [[NEG_INF] * (m + 1) for _ in range(m + 1)]
    for s, t, target, tm in translation_options(f, model):
        est = tm + model.lm_weight * model.lm.estimate(target) + model.word_penalty * len(target)
        fc[s][t] = max(fc[s][t], est)
    for length in range(2, m + 1):
        for s in range(0, m - length + 1):
            t = s + length
            for k in range(s + 1, t):
                fc[s][t] = max(fc[s][t], fc[s][k] + fc[k][t])
    return fc


def future_cost(coverage: int, m: int, fc: list[list[float]]) -> float:
    """Sum of fc over the maximal runs of uncovered source words."""
    total, s = 0.0, 0
    while s < m:
        if coverage >> s & 1:
            s += 1
            continue
        t = s
        while t < m and not coverage >> t & 1:
            t += 1
        total += fc[s][t]
        s = t
    return total


def _jump_ok(model: Model, s: int, end: int) -> bool:
    return model.distortion_limit is None or abs(s - end) <= model.distortion_limit


def decode(
    f: list[str],
    model: Model,
    stack_size: Optional[int] = None,
    threshold: float = math.inf,
    recombine: bool = True,
) -> tuple[float, Phrase, list[tuple[int, int, Phrase]]]:
    """Return (score, target words, derivation) of the best complete hypothesis
    found; (-inf, (), []) if no hypothesis covers the whole source."""
    m = len(f)
    full = (1 << m) - 1
    opts = translation_options(f, model)
    fc = future_cost_table(f, model)  # @line L1
    stacks: list[dict] = [dict() for _ in range(m + 1)]  # @line L2
    start = Hyp(0.0, 0, "<s>", 0, None, None)
    stacks[0][(0, "<s>", 0)] = start
    for c in range(m):  # @line L3
        hyps = _prune(list(stacks[c].values()), m, fc, stack_size, threshold)  # @line L4
        for h in hyps:  # @line L5
            for s, t, target, tm in opts:  # @line L6
                span_mask = ((1 << (t - s)) - 1) << s
                if h.coverage & span_mask or not _jump_ok(model, s, h.end):  # @line L7
                    continue
                lm = 0.0  # @line L8
                prev = h.last
                for w in target:
                    lm += model.lm.logprob(prev, w)
                    prev = w
                score = (
                    h.score
                    + tm
                    + model.lm_weight * lm
                    - model.distortion_weight * abs(s - h.end)
                    + model.word_penalty * len(target)
                )
                cov = h.coverage | span_mask
                new = Hyp(score, cov, prev, t, h, (s, t, target))
                key = (cov, prev, t) if recombine else (cov, prev, t, id(new))  # @line L9
                stack = stacks[c + t - s]
                old = stack.get(key)
                if old is None or new.score > old.score:  # @line L10
                    stack[key] = new
    best, best_total = None, NEG_INF  # @line L11
    for h in stacks[m].values():
        total = h.score + model.lm_weight * model.lm.logprob(h.last, "</s>")  # @line L12
        if total > best_total:
            best, best_total = h, total
    if best is None:
        return NEG_INF, (), []
    steps = []  # @line L13
    node: Optional[Hyp] = best
    while node is not None and node.step is not None:
        steps.append(node.step)
        node = node.back
    steps.reverse()
    words = tuple(w for _, _, target in steps for w in target)
    assert best.coverage == full
    return best_total, words, steps


def _prune(hyps: list[Hyp], m: int, fc, stack_size: Optional[int], threshold: float) -> list[Hyp]:
    """Histogram and threshold pruning by score plus future cost."""
    ranked = sorted(hyps, key=lambda h: h.score + future_cost(h.coverage, m, fc), reverse=True)
    if not ranked:
        return []
    top = ranked[0].score + future_cost(ranked[0].coverage, m, fc)
    kept = [h for h in ranked if h.score + future_cost(h.coverage, m, fc) >= top - threshold]
    return kept if stack_size is None else kept[:stack_size]


def score_derivation(f: list[str], model: Model, steps: list[tuple[int, int, Phrase]]) -> float:
    """The model score of a complete derivation, computed from scratch."""
    m = len(f)
    covered = [False] * m
    total, end, words = 0.0, 0, []
    for s, t, target in steps:
        if any(covered[s:t]) or not _jump_ok(model, s, end):
            return NEG_INF
        tms = [tm for tgt, tm in model.table.get(tuple(f[s:t]), []) if tgt == target]
        if not tms:
            return NEG_INF
        total += max(tms) - model.distortion_weight * abs(s - end)
        for k in range(s, t):
            covered[k] = True
        end = t
        words.extend(target)
    if not all(covered):
        return NEG_INF
    seq = ["<s>"] + words + ["</s>"]
    lm = sum(model.lm.logprob(a, b) for a, b in zip(seq, seq[1:]))
    return total + model.lm_weight * lm + model.word_penalty * len(words)


def exhaustive(f: list[str], model: Model) -> tuple[float, Phrase]:
    """Best score over every segmentation, every order of the phrases and every
    translation option. Exponential: only for sentences of a few words."""
    m = len(f)
    best, best_words = NEG_INF, ()
    for cuts in itertools.product([False, True], repeat=max(m - 1, 0)):
        bounds = [0] + [k + 1 for k, c in enumerate(cuts) if c] + [m]
        spans = list(zip(bounds, bounds[1:]))
        if any(t - s > model.max_phrase_len for s, t in spans):
            continue
        for order in itertools.permutations(spans):
            choices = [model.table.get(tuple(f[s:t]), []) for s, t in order]
            for pick in itertools.product(*choices):
                steps = [(s, t, tgt) for (s, t), (tgt, _) in zip(order, pick)]
                sc = score_derivation(f, model, steps)
                if sc > best:
                    best = sc
                    best_words = tuple(w for _, _, tgt in steps for w in tgt)
    return best, best_words
