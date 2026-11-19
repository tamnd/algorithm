# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-synchronous-beam-search/. The authors are listed in prov/6JVTAP.jsonl.

"""Time-synchronous Viterbi beam search with a lexical prefix tree and a bigram.

The words are given by a lexicon word -> tuple of phones (one pronunciation per
word). To keep the code short, each phone is one emitting HMM state with a self
loop; a real system has three states per phone and context-dependent models,
and only the tree gets bigger. The phones of all words share one prefix tree,
so words that start alike share their first states.

Scores are log probabilities, higher is better. For a word sequence
w_1 ... w_K and a segmentation in which phone j of the whole sequence occupies
d_j >= 1 frames, the score is

    sum over frames of the emission log score of the phone at that frame
  + sum over phones of ((d_j - 1) * loop + fwd)        (fwd is also the word exit)
  + sum over k of (lm_weight * lm(w_{k-1}, w_k) + ip)  with w_0 = <s>
  + lm_weight * lm(w_K, </s>).

The search finds the best (word sequence, segmentation) pair when nothing is
pruned. A hypothesis is a pair (previous word, tree node): the tree is copied
per previous word, so the bigram score added at the word end is the right one,
and Viterbi recombination of hypotheses with the same key is exact. Word ends
are recombined per word and frame.

Pruning: a beam (drop hypotheses more than beam below the best of the frame)
and a histogram limit (keep at most max_active hypotheses). With pruning the
search can miss the best path.
"""

import heapq
import math
from typing import Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF

BOS = "<s>"
EOS = "</s>"


class PrefixTree:
    """A prefix tree of pronunciations. Node 0 is the root; each other node is one phone."""

    def __init__(self, lexicon: Dict[str, Sequence[str]]) -> None:
        self.phone: List[Optional[str]] = [None]
        self.children: List[List[int]] = [[]]
        self.words: List[List[str]] = [[]]
        for w in sorted(lexicon):
            phones = lexicon[w]
            if not phones:
                raise ValueError("a word needs at least one phone")
            node = 0
            for ph in phones:
                nxt = next((c for c in self.children[node] if self.phone[c] == ph), None)
                if nxt is None:
                    nxt = len(self.phone)
                    self.phone.append(ph)
                    self.children.append([])
                    self.words.append([])
                    self.children[node].append(nxt)
                node = nxt
            self.words[node].append(w)

    def num_nodes(self) -> int:
        return len(self.phone)


def _relax(table: Dict, key, score: float, back: int) -> None:
    old = table.get(key)
    if old is None or score > old[0]:
        table[key] = (score, back)


def _prune(hyps: Dict, beam: float, max_active: Optional[int]) -> Dict:
    if not hyps:
        return hyps
    best = max(s for s, _ in hyps.values())
    kept = {k: v for k, v in hyps.items() if v[0] >= best - beam}
    if max_active is not None and len(kept) > max_active:
        top = heapq.nlargest(max_active, kept.items(), key=lambda kv: (kv[1][0], repr(kv[0])))
        kept = dict(top)
    return kept


def decode(
    lexicon: Dict[str, Sequence[str]],
    lm: Dict[Tuple[str, str], float],
    emit: Sequence[Dict[str, float]],
    lm_weight: float = 1.0,
    ip: float = 0.0,
    loop: float = math.log(0.5),
    fwd: float = math.log(0.5),
    beam: float = math.inf,
    max_active: Optional[int] = None,
):
    """Return (words, ends, score): the best word sequence, the last frame of each word, and its score.

    lm[(v, w)] is the log bigram probability of w after v; missing pairs are
    -inf. emit[t][ph] is the log emission score of phone ph at frame t.
    Return ([], [], -inf) if no hypothesis survives to the end.
    """
    tree = PrefixTree(lexicon)
    T = len(emit)
    if T == 0:
        return [], [], NEG_INF
    records: List[Tuple[str, int, float, int]] = []  # (word, end frame, score, previous record)

    def lm_score(v: str, w: str) -> float:
        return lm.get((v, w), NEG_INF)

    hyps: Dict[Tuple[str, int], Tuple[float, int]] = {}
    for c in tree.children[0]:  # @line L1
        _relax(hyps, (BOS, c), emit[0][tree.phone[c]], -1)
    ends: Dict[str, int] = {}
    for t in range(T):  # @line L2
        hyps = _prune(hyps, beam, max_active)  # @line L3
        ends = {}  # @line L4
        for (v, n), (s, back) in hyps.items():  # @line L5
            for w in tree.words[n]:
                score = s + fwd + lm_weight * lm_score(v, w) + ip
                if score == NEG_INF:
                    continue
                if w not in ends or score > records[ends[w]][2]:
                    records.append((w, t, score, back))
                    ends[w] = len(records) - 1
        if t == T - 1:  # @line L6
            break
        e = emit[t + 1]
        new: Dict[Tuple[str, int], Tuple[float, int]] = {}
        for (v, n), (s, back) in hyps.items():  # @line L7
            _relax(new, (v, n), s + loop + e[tree.phone[n]], back)
            for c in tree.children[n]:
                _relax(new, (v, c), s + fwd + e[tree.phone[c]], back)
        for w, r in ends.items():  # @line L8
            for c in tree.children[0]:
                _relax(new, (w, c), records[r][2] + e[tree.phone[c]], r)
        hyps = new  # @line L9
    best_r, best = -1, NEG_INF
    for w, r in sorted(ends.items()):  # @line L10
        score = records[r][2] + lm_weight * lm_score(w, EOS)
        if score > best:
            best_r, best = r, score
    if best_r < 0:
        return [], [], NEG_INF
    words: List[str] = []
    frames: List[int] = []
    r = best_r
    while r >= 0:
        w, t, _, r = records[r]
        words.append(w)
        frames.append(t)
    return words[::-1], frames[::-1], best


def path_score(
    lexicon: Dict[str, Sequence[str]],
    lm: Dict[Tuple[str, str], float],
    emit: Sequence[Dict[str, float]],
    words: Sequence[str],
    durations: Sequence[int],
    lm_weight: float = 1.0,
    ip: float = 0.0,
    loop: float = math.log(0.5),
    fwd: float = math.log(0.5),
) -> float:
    """Return the score of one word sequence with one duration per phone (the formula above)."""
    phones = [ph for w in words for ph in lexicon[w]]
    if len(phones) != len(durations) or sum(durations) != len(emit) or min(durations, default=1) < 1:
        raise ValueError("durations do not fit")
    score = 0.0
    t = 0
    for ph, d in zip(phones, durations):
        for _ in range(d):
            score += emit[t][ph]
            t += 1
        score += (d - 1) * loop + fwd
    prev = BOS
    for w in list(words) + [EOS]:
        score += lm_weight * lm.get((prev, w), NEG_INF)
        if w != EOS:
            score += ip
        prev = w
    return score
