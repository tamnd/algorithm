# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forced-alignment/. The authors are listed in prov/4HHCES.jsonl.

"""Forced alignment: Viterbi through the left-to-right HMM of a known transcript.

The transcript w_1 ... w_U is expanded with a pronunciation lexicon into phones,
and each phone into its emitting HMM states (3 by default, no skips). The result
is one chain of S states, numbered 0..S-1 in the code. A path must start in
state 0 at frame 0, end in state S-1 at frame T-1, and at each frame either stay
in its state (self loop) or move to the next state.

The acoustic model is outside this file: the caller gives log_emit[t][j], the
log emission score log b_j(o_t) of chain state j at frame t (a Gaussian mixture
log density, or a scaled network output). The code works in log space, so a
long utterance does not underflow. Non-emitting entry and exit states (the HTK
convention) are left out: the exit transition of the last state is the same
for every path and does not change the best path.

Tie rule: when staying and moving give the same score, the path stays (line L5).
"""

from typing import Dict, List, Sequence, Tuple

from nlslog import NEG_INF, safe_log


def expand_transcript(words: Sequence[str], lexicon: Dict[str, Sequence[Sequence[str]]], states_per_phone: int = 3):
    """Return one label per chain state: (word index, word, phone index, phone, state index).

    The first pronunciation of each word in the lexicon is used. Raise KeyError
    for a word that is not in the lexicon.
    """
    labels = []
    for u, w in enumerate(words):
        phones = lexicon[w][0]
        for p, ph in enumerate(phones):
            for s in range(states_per_phone):
                labels.append((u, w, p, ph, s))
    return labels


def forced_align(log_emit: Sequence[Sequence[float]], log_self: Sequence[float], log_next: Sequence[float]):
    """Return (path, score): the best state path of the chain and its log score.

    log_emit is T x S. log_self[j] is the log self-loop probability of state j,
    log_next[j] the log probability of the move j -> j + 1 (log_next[S-1] is
    not used). Raise ValueError if T < S (no path) or every path scores -inf.
    Cost: O(T S) time and O(T S) memory for the back pointers.
    """
    T = len(log_emit)
    S = len(log_self)
    if S == 0 or T < S:
        raise ValueError("need at least one frame per state")
    delta = [NEG_INF] * S
    delta[0] = log_emit[0][0]  # @line L1
    back: List[List[int]] = [[0] * S]
    for t in range(1, T):  # @line L2
        new = [NEG_INF] * S
        ptr = [0] * S
        lo = max(0, S - (T - t))  # states that can still reach S-1 by the end
        hi = min(S - 1, t)  # states that can be reached by frame t
        for j in range(lo, hi + 1):  # @line L3
            stay = delta[j] + log_self[j]  # @line L4
            move = delta[j - 1] + log_next[j - 1] if j > 0 else NEG_INF
            if move > stay:  # @line L5: a tie keeps the self loop
                new[j], ptr[j] = move + log_emit[t][j], j - 1  # @line L6
            else:
                new[j], ptr[j] = stay + log_emit[t][j], j
        delta = new
        back.append(ptr)
    score = delta[S - 1]  # @line L7
    if score == NEG_INF:
        raise ValueError("every path has probability 0")
    path = [S - 1]
    for t in range(T - 1, 0, -1):  # @line L8
        path.append(back[t][path[-1]])
    path.reverse()
    return path, score  # @line L9


def segments(path: Sequence[int], labels: Sequence[Tuple], level: str = "phone"):
    """Turn a state path into spans (label, start, end) with frames start <= t < end.

    level is "state", "phone" or "word". A phone span is keyed by (word index,
    phone index), so two equal phones in a row stay two spans.
    """
    if level == "state":
        key = lambda j: (j,)
        name = lambda j: labels[j]
    elif level == "phone":
        key = lambda j: labels[j][:3]
        name = lambda j: labels[j][3]
    elif level == "word":
        key = lambda j: labels[j][:1]
        name = lambda j: labels[j][1]
    else:
        raise ValueError("level must be state, phone or word")
    out = []
    start = 0
    for t in range(1, len(path) + 1):
        if t == len(path) or key(path[t]) != key(path[start]):
            out.append((name(path[start]), start, t))
            start = t
    return out


def align_transcript(words, lexicon, log_b, T, self_loop=0.5, states_per_phone=3, level="phone"):
    """Align a transcript to T frames.

    log_b(t, phone, state) is the log emission score of the given phone state at
    frame t. Every state has the same self-loop probability. Return (spans, score).
    """
    labels = expand_transcript(words, lexicon, states_per_phone)
    S = len(labels)
    log_emit = [[log_b(t, labels[j][3], labels[j][4]) for j in range(S)] for t in range(T)]
    ls = [safe_log(self_loop)] * S
    ln = [safe_log(1 - self_loop)] * S
    path, score = forced_align(log_emit, ls, ln)
    return segments(path, labels, level), score
