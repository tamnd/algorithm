# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/noisy-channel-spelling-correction/. The authors are listed in prov/01YMRN.jsonl.
"""Noisy channel spelling correction in the style of Kernighan, Church and Gale.

A typed string x that is not a word of the vocabulary is corrected to the
word w that maximizes P(w) P(x | w). The candidates are the words that
give x by one edit: a deletion, an insertion, a substitution, or a swap of
two adjacent letters. The channel P(x | w) of one edit is a confusion count
divided by the count of the intended letters in a corpus, as in the
four confusion matrices of the method. When several edits turn w into x,
their probabilities are added.

The keys of the confusion tables are always (intended, typed context):
  dels[(p, c)]  number of times "pc" was typed as "p"
  ins[(p, c)]   number of times "p" was typed as "pc"
  subs[(c, e)]  number of times the letter c was typed as e
  trans[(c, d)] number of times "cd" was typed as "dc"
The letter p before an edit at the start of a word is "#".
Ties between candidates go to the smaller word in string order.
"""

from collections import Counter

BOUNDARY = "#"


def char_counts(tokens):
    """Counts of single letters and adjacent pairs, with "#" before each token."""
    counts = Counter()
    for t in tokens:
        s = BOUNDARY + t
        for i, ch in enumerate(s):
            counts[ch] += 1
            if i + 1 < len(s):
                counts[s[i : i + 2]] += 1
    return counts


class ErrorModel:
    """The channel P(x | w) for one edit, from four confusion tables."""

    def __init__(self, dels, ins, subs, trans, chars):
        self.dels = dict(dels)
        self.ins = dict(ins)
        self.subs = dict(subs)
        self.trans = dict(trans)
        self.chars = dict(chars)

    def _ratio(self, table, key, denom):
        n = table.get(key, 0)
        d = self.chars.get(denom, 0)
        return n / d if n and d else 0.0

    def p_deletion(self, p, c):
        return self._ratio(self.dels, (p, c), p + c)

    def p_insertion(self, p, c):
        return self._ratio(self.ins, (p, c), p)

    def p_substitution(self, c, e):
        return self._ratio(self.subs, (c, e), c)

    def p_transposition(self, c, d):
        return self._ratio(self.trans, (c, d), c + d)


def candidates(x, vocab, model, alphabet):
    """Map each vocabulary word w one edit from x to P(x | w), by undoing each edit of x."""
    out = {}  # @line L2

    def add(w, p):
        if p > 0.0 and w in vocab:  # @line L10
            out[w] = out.get(w, 0.0) + p

    for i in range(len(x) + 1):  # @line L3
        prev = x[i - 1] if i > 0 else BOUNDARY
        for c in alphabet:  # x lost the letter c after prev: w = x[:i] + c + x[i:]
            add(x[:i] + c + x[i:], model.p_deletion(prev, c))  # @line L4
    for i in range(len(x)):  # @line L5
        prev = x[i - 1] if i > 0 else BOUNDARY
        add(x[:i] + x[i + 1 :], model.p_insertion(prev, x[i]))  # x has an extra x[i]  # @line L6
        for c in alphabet:  # x has x[i] where w has c
            if c != x[i]:
                add(x[:i] + c + x[i + 1 :], model.p_substitution(c, x[i]))  # @line L7
    for i in range(len(x) - 1):  # @line L8
        a, b = x[i], x[i + 1]
        if a != b:  # x has "ab" where w has "ba"
            add(x[:i] + b + a + x[i + 2 :], model.p_transposition(b, a))  # @line L9
    return out


def correct(x, word_counts, model, alphabet=None):
    """Return (best word, its score P(w) P(x | w)), or (x, None) for a known word, or (None, 0.0)."""
    if x in word_counts:  # @line L1
        return x, None
    if alphabet is None:
        alphabet = sorted({ch for w in word_counts for ch in w})
    total = sum(word_counts.values())
    best, best_score = None, 0.0
    for w, channel in sorted(candidates(x, word_counts, model, alphabet).items()):
        score = word_counts[w] / total * channel  # @line L11
        if score > best_score:  # ties keep the smaller word, seen first
            best, best_score = w, score
    return best, best_score  # @line L12
