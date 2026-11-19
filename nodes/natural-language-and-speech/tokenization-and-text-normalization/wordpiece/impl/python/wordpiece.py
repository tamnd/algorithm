# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wordpiece/. The authors are listed in prov/N8960R.jsonl.

"""WordPiece: vocabulary learning by likelihood gain, and greedy longest-match encoding.

train_wordpiece learns merges. Each word starts as its characters, and every
character after the first carries the prefix "##". At each step the merge of
the adjacent pair (a, b) that raises the log likelihood of the corpus most is
applied, where the likelihood is that of a unigram model over the current
units with maximum likelihood probabilities c(x) / N. Logs are natural logs,
so the likelihood is in nats.

encode_word is the encoder of BERT: from left to right, take the longest
vocabulary piece that starts at the current position (with "##" after the
first piece), and give [UNK] for the whole word when no piece fits.
"""

import math
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

PREFIX = "##"
UNK = "[UNK]"

Pair = Tuple[str, str]


def initial_units(word: str) -> List[str]:
    """Return the first segmentation of a nonempty word: w1, ##w2, ..., ##wn."""
    if not word:
        raise ValueError("a word must not be empty")
    return [word[0]] + [PREFIX + ch for ch in word[1:]]


def join_units(a: str, b: str) -> str:
    """Return the unit made from a followed by b. b is never word-initial."""
    if not b.startswith(PREFIX):
        raise ValueError("the right unit of a pair must start with ##")
    return a + b[len(PREFIX):]


def count_pair(units: Sequence[str], a: str, b: str) -> int:
    """Return the number of non-overlapping occurrences of (a, b), taken from the left."""
    k, i = 0, 0
    while i + 1 < len(units):
        if units[i] == a and units[i + 1] == b:
            k, i = k + 1, i + 2
        else:
            i += 1
    return k


def merge_units(units: Sequence[str], a: str, b: str) -> List[str]:
    """Replace each non-overlapping occurrence of (a, b), taken from the left, by one unit."""
    out, i, ab = [], 0, join_units(a, b)
    while i < len(units):
        if i + 1 < len(units) and units[i] == a and units[i + 1] == b:
            out.append(ab)
            i += 2
        else:
            out.append(units[i])
            i += 1
    return out


def unit_counts(seg: Mapping[str, Sequence[str]], freq: Mapping[str, int]) -> Dict[str, int]:
    """Return c(x): the number of times unit x occurs in the corpus."""
    c: Dict[str, int] = {}
    for w, units in seg.items():
        for x in units:
            c[x] = c.get(x, 0) + freq[w]
    return c


def pair_counts(seg: Mapping[str, Sequence[str]], freq: Mapping[str, int]) -> Dict[Pair, int]:
    """Return k(a, b): the number of merges that (a, b) would make in the corpus."""
    p: Dict[Pair, int] = {}
    for w, units in seg.items():
        for pair in set(zip(units, units[1:])):
            k = count_pair(units, pair[0], pair[1])
            p[pair] = p.get(pair, 0) + k * freq[w]
    return p


def xlogx(x: int) -> float:
    """Return x ln x, with 0 ln 0 = 0."""
    return 0.0 if x == 0 else x * math.log(x)


def log_likelihood(c: Mapping[str, int]) -> float:
    """Return the unigram log likelihood sum_x c(x) ln(c(x) / N) in nats."""
    n = sum(c.values())
    return math.fsum(xlogx(v) for v in c.values()) - xlogx(n)


def merge_gain(c: Mapping[str, int], a: str, b: str, k: int) -> float:
    """Return the change in log likelihood when k occurrences of (a, b) become ab.

    Only c(a), c(b), c(ab) and N change, so the gain is a sum of six or eight
    terms of the form x ln x. When a = b, c(a) drops by 2k.
    """
    ab = join_units(a, b)
    n = sum(c.values())
    ca, cab = c.get(a, 0), c.get(ab, 0)
    g = xlogx(cab + k) - xlogx(cab) - (xlogx(n - k) - xlogx(n))
    if a == b:
        return g + xlogx(ca - 2 * k) - xlogx(ca)
    cb = c.get(b, 0)
    return g + xlogx(ca - k) - xlogx(ca) + xlogx(cb - k) - xlogx(cb)


def train_wordpiece(freq: Mapping[str, int], merges: int) -> Tuple[Set[str], List[Pair]]:
    """Learn at most `merges` merges from a map of word counts.

    Return the vocabulary (all initial units and all merged units) and the
    list of merges in the order they were made. Ties in the gain go to the
    smallest pair in string order, so the result is deterministic. Gains are
    compared to 9 decimals, so that rounding in the logarithms cannot break
    an exact tie.
    Cost per merge: O(L) for the counts, where L is the total word length.
    """
    seg = {w: initial_units(w) for w in freq}  # @line L1
    vocab = {x for units in seg.values() for x in units}  # @line L2
    done: List[Pair] = []
    for _ in range(merges):  # @line L3
        c, p = unit_counts(seg, freq), pair_counts(seg, freq)  # @line L4
        if not p:  # @line L5
            break
        gain = {pair: merge_gain(c, pair[0], pair[1], k) for pair, k in p.items()}  # @line L6
        a, b = min(gain, key=lambda pair: (-round(gain[pair], 9), pair))  # @line L7
        seg = {w: merge_units(units, a, b) for w, units in seg.items()}  # @line L8
        vocab.add(join_units(a, b))  # @line L9
        done.append((a, b))
    return vocab, done  # @line L10


def segment_with_merges(word: str, merges: Iterable[Pair]) -> List[str]:
    """Apply the learned merges to one word in training order."""
    units = initial_units(word)
    for a, b in merges:
        units = merge_units(units, a, b)
    return units


def encode_word(word: str, vocab: Set[str], max_chars: int = 200) -> List[str]:
    """Encode one word by greedy longest match first, as BERT does.

    Return [UNK] when the word is longer than max_chars or when some position
    has no matching piece. Cost: at most n(n + 1) / 2 set lookups for a word
    of n characters.
    """
    if len(word) > max_chars:  # @line E1
        return [UNK]
    out, start = [], 0  # @line E2
    while start < len(word):  # @line E3
        end, piece = len(word), None  # @line E4
        while start < end:  # @line E5
            sub = word[start:end] if start == 0 else PREFIX + word[start:end]  # @line E6
            if sub in vocab:  # @line E7
                piece = sub
                break
            end -= 1  # @line E8
        if piece is None:  # @line E9
            return [UNK]
        out.append(piece)  # @line E10
        start = end
    return out  # @line E11


def encode(words: Iterable[str], vocab: Set[str], max_chars: int = 200) -> List[str]:
    """Encode a list of pre-tokenized words and join the pieces."""
    out: List[str] = []
    for w in words:
        out.extend(encode_word(w, vocab, max_chars))
    return out
