# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chen-manning-parser/. The authors are listed in prov/ZT8KWQ.jsonl.

"""The neural transition-based dependency parser of Chen and Manning (2014).

The parser is greedy arc-standard parsing. At each configuration it reads 48
features, embeds them, and a feedforward network with the cube activation
gives one score per transition:

    x = [e(w_1); ...; e(w_18); e(t_1); ...; e(t_18); e(l_1); ...; e(l_12)]   (48 d numbers)
    h = (W1 x + b1) ** 3                                                    (H numbers, cube per entry)
    z = W2 h                                                                (one logit per transition)

The parser takes the legal transition with the largest logit. Training uses the
cross-entropy of the softmax of z over the legal transitions; the gold
transitions come from the "shortest stack" oracle, which prefers LEFT-ARC.

The words are 1..n and 0 is the root. The stack starts as [0]; s0 is its top,
s1 and s2 are under it; b0, b1, b2 are the first three buffer words. (Chen and
Manning number them from 1: their s1 is s0 here.) lc1(w) and lc2(w) are the
leftmost and second leftmost dependents of w, rc1(w) and rc2(w) the rightmost
and second rightmost.

This module takes the weights as given (from a seeded generator in the tests).
It implements the features, one forward pass, the pre-computation trick, the
greedy parser, the oracle and the loss with its gradient in W2; it does not
train the network.
"""

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF, log_softmax

NULL, ROOT, UNK = "<NULL>", "<ROOT>", "<UNK>"


class Vocab:
    """Strings to ids; ids 0, 1 and 2 are NULL, ROOT and UNK."""

    def __init__(self, items: Sequence[str]):
        self.items: List[str] = [NULL, ROOT, UNK]
        self.ids: Dict[str, int] = {s: i for i, s in enumerate(self.items)}
        for s in items:
            if s not in self.ids:
                self.ids[s] = len(self.items)
                self.items.append(s)

    def __len__(self) -> int:
        return len(self.items)

    def id(self, s: str) -> int:
        return self.ids.get(s, self.ids[UNK])


class Config:
    def __init__(self, n: int):
        self.n = n
        self.stack: List[int] = [0]
        self.next = 1
        self.heads = [-1] * (n + 1)
        self.labels: List[Optional[str]] = [None] * (n + 1)

    def is_terminal(self) -> bool:
        return self.next > self.n and len(self.stack) == 1

    def copy(self) -> "Config":
        c = Config(self.n)
        c.stack = list(self.stack)
        c.next = self.next
        c.heads = list(self.heads)
        c.labels = list(self.labels)
        return c


def transitions(labels: Sequence[str]) -> List[Tuple[str, Optional[str]]]:
    """Index 0 is SHIFT, then LEFT-ARC with each label, then RIGHT-ARC with each label."""
    return [("SH", None)] + [("LA", l) for l in labels] + [("RA", l) for l in labels]


def is_legal(c: Config, t, single_root: bool = False) -> bool:
    kind = t[0]
    if kind == "SH":
        return c.next <= c.n
    if len(c.stack) < 2:
        return False
    if kind == "LA":
        return c.stack[-2] != 0
    if single_root and c.stack[-2] == 0:
        return c.next > c.n
    return True


def apply(c: Config, t) -> None:
    kind, label = t
    if kind == "SH":
        c.stack.append(c.next)
        c.next += 1
    elif kind == "LA":
        s0 = c.stack.pop()
        s1 = c.stack.pop()
        c.heads[s1], c.labels[s1] = s0, label
        c.stack.append(s0)
    else:
        s0 = c.stack.pop()
        c.heads[s0], c.labels[s0] = c.stack[-1], label


def _left_kids(c: Config, w: int) -> List[int]:
    return [d for d in range(1, w) if c.heads[d] == w]


def _right_kids(c: Config, w: int) -> List[int]:
    return [d for d in range(c.n, w, -1) if c.heads[d] == w]


def _kid(kids: List[int], i: int) -> Optional[int]:
    return kids[i - 1] if len(kids) >= i else None


def lc(c: Config, w: Optional[int], i: int) -> Optional[int]:
    return None if w is None else _kid(_left_kids(c, w), i)


def rc(c: Config, w: Optional[int], i: int) -> Optional[int]:
    return None if w is None else _kid(_right_kids(c, w), i)


def feature_positions(c: Config) -> Tuple[List[Optional[int]], List[Optional[int]]]:
    """Return the 18 word positions (also used for the tags) and the 12 label positions.

    None is a missing element. The 18 are s0, s1, s2, b0, b1, b2, then for
    s in (s0, s1): lc1(s), rc1(s), lc2(s), rc2(s), lc1(lc1(s)), rc1(rc1(s)).
    The 12 label positions are the last 12 of these.
    """
    st = [c.stack[-k] if len(c.stack) >= k else None for k in (1, 2, 3)]
    bu = [c.next + k if c.next + k <= c.n else None for k in (0, 1, 2)]
    kids: List[Optional[int]] = []
    for s in st[:2]:
        kids += [lc(c, s, 1), rc(c, s, 1), lc(c, s, 2), rc(c, s, 2), lc(c, lc(c, s, 1), 1), rc(c, rc(c, s, 1), 1)]
    return st + bu + kids, kids


def features(c: Config, words: Sequence[str], tags: Sequence[str], wv: Vocab, tv: Vocab, lv: Vocab) -> List[int]:
    """Return the 48 feature ids: 18 words, 18 tags, 12 labels. words[0] and tags[0] are unused."""
    pos, kids = feature_positions(c)

    def tok(p, seq, v):
        if p is None:
            return v.id(NULL)
        if p == 0:
            return v.id(ROOT)
        return v.id(seq[p])

    fw = [tok(p, words, wv) for p in pos]
    ft = [tok(p, tags, tv) for p in pos]
    fl = [lv.id(NULL) if p is None else lv.id(c.labels[p]) for p in kids]
    return fw + ft + fl


class Model:
    """Embeddings E_w, E_t, E_l (d numbers each), W1 (H x 48d), b1 (H), W2 (T x H)."""

    def __init__(self, n_words: int, n_tags: int, n_labels: int, d: int, hidden: int, n_trans: int, rng: random.Random, scale: float = 0.5):
        def mat(r, k):
            return [[rng.uniform(-scale, scale) for _ in range(k)] for _ in range(r)]

        self.d, self.hidden = d, hidden
        self.Ew, self.Et, self.El = mat(n_words, d), mat(n_tags, d), mat(n_labels, d)
        self.W1 = mat(hidden, 48 * d)
        self.b1 = [rng.uniform(-scale, scale) for _ in range(hidden)]
        self.W2 = mat(n_trans, hidden)

    def table(self, k: int):
        """The embedding table of feature number k (0..47)."""
        return self.Ew if k < 18 else self.Et if k < 36 else self.El

    def embed(self, f: Sequence[int]) -> List[float]:
        x: List[float] = []
        for k, v in enumerate(f):
            x += self.table(k)[v]
        return x

    def hidden_layer(self, x: Sequence[float]) -> List[float]:
        return [(math.fsum(w * a for w, a in zip(row, x)) + b) ** 3 for row, b in zip(self.W1, self.b1)]

    def logits(self, h: Sequence[float]) -> List[float]:
        return [math.fsum(w * a for w, a in zip(row, h)) for row in self.W2]

    def forward(self, f: Sequence[int]) -> Tuple[List[float], List[float]]:
        h = self.hidden_layer(self.embed(f))
        return h, self.logits(h)


def precompute(model: Model, ids_per_feature: Sequence[Sequence[int]]):
    """The pre-computation trick: store W1[:, block k] E[v] for feature k and id v.

    Chen and Manning store these products for the most frequent words; then the
    first layer is H * 48 additions per configuration instead of H * 48 d
    multiplications.
    """
    d = model.d
    pre = []
    for k, ids in enumerate(ids_per_feature):
        tab = model.table(k)
        cols = range(k * d, (k + 1) * d)
        pre.append({v: [math.fsum(row[j] * tab[v][j - k * d] for j in cols) for row in model.W1] for v in ids})
    return pre


def hidden_from_precomputed(model: Model, pre, f: Sequence[int]) -> List[float]:
    z = list(model.b1)
    for k, v in enumerate(f):
        z = [a + b for a, b in zip(z, pre[k][v])]
    return [a ** 3 for a in z]


def legal_log_probs(z: Sequence[float], legal: Sequence[bool]) -> List[float]:
    """Log softmax of the logits over the legal transitions; NEG_INF for the others."""
    idx = [i for i, ok in enumerate(legal) if ok]
    lp = log_softmax([z[i] for i in idx])
    out = [NEG_INF] * len(z)
    for i, v in zip(idx, lp):
        out[i] = v
    return out


def parse(model: Model, words, tags, wv: Vocab, tv: Vocab, lv: Vocab, labels: Sequence[str], single_root: bool = False):
    """Greedy parsing. Returns (heads, labels, transitions, total log probability)."""
    trans = transitions(labels)
    n = len(words) - 1
    c = Config(n)  # @line L1
    seq, total = [], 0.0
    while not c.is_terminal():  # @line L2
        f = features(c, words, tags, wv, tv, lv)  # @line L3
        _, z = model.forward(f)  # @line L4
        legal = [is_legal(c, t, single_root) for t in trans]
        lp = legal_log_probs(z, legal)  # @line L5
        best = max((i for i in range(len(trans)) if legal[i]), key=lambda i: z[i])  # @line L6
        total += lp[best]
        apply(c, trans[best])  # @line L7
        seq.append(trans[best])
    return c.heads, c.labels, seq, total  # @line L8


def exhaustive_best(model: Model, words, tags, wv: Vocab, tv: Vocab, lv: Vocab, labels: Sequence[str], single_root: bool = False):
    """The complete sequence with the largest total log probability, by search over all sequences."""
    trans = transitions(labels)
    n = len(words) - 1
    best = [NEG_INF, None]

    def go(c, total, seq):
        if c.is_terminal():
            if total > best[0]:
                best[0], best[1] = total, (list(c.heads), list(seq))
            return
        _, z = model.forward(features(c, words, tags, wv, tv, lv))
        legal = [is_legal(c, t, single_root) for t in trans]
        lp = legal_log_probs(z, legal)
        for i, t in enumerate(trans):
            if legal[i]:
                c2 = c.copy()
                apply(c2, t)
                seq.append(t)
                go(c2, total + lp[i], seq)
                seq.pop()

    go(Config(n), 0.0, [])
    return best[0], best[1][0], best[1][1]


def shortest_stack_oracle(c: Config, gold_heads: Sequence[int], gold_labels: Sequence[Optional[str]]):
    """LEFT-ARC if the gold head of s1 is s0; RIGHT-ARC if the gold head of s0 is s1 and s0 has
    all its dependents; else SHIFT. Return None when no move is right (a non-projective tree)."""
    if len(c.stack) >= 2:
        s1, s0 = c.stack[-2], c.stack[-1]
        if s1 != 0 and gold_heads[s1] == s0:
            return ("LA", gold_labels[s1])
        if gold_heads[s0] == s1 and all(c.heads[d] == s0 for d in range(1, c.n + 1) if gold_heads[d] == s0):
            return ("RA", gold_labels[s0])
    return ("SH", None) if c.next <= c.n else None


def training_examples(words, tags, gold_heads, gold_labels, wv: Vocab, tv: Vocab, lv: Vocab):
    """The (features, gold transition) pairs along the oracle sequence of a projective tree."""
    n = len(words) - 1
    c = Config(n)
    out = []
    while not c.is_terminal():
        t = shortest_stack_oracle(c, gold_heads, gold_labels)
        if t is None:
            raise ValueError("the gold tree is not projective")
        out.append((features(c, words, tags, wv, tv, lv), t, c.copy()))
        apply(c, t)
    if c.heads != list(gold_heads):
        raise ValueError("the gold tree is not projective")
    return out


def loss_and_grad_W2(model: Model, f: Sequence[int], legal: Sequence[bool], gold: int):
    """Cross-entropy -log p(gold) over the legal transitions, and its gradient in W2.

    d loss / d W2[t][j] = (p_t - [t = gold]) h_j for legal t, and 0 for the others.
    """
    h, z = model.forward(f)
    lp = legal_log_probs(z, legal)
    loss = -lp[gold]
    grad = []
    for t in range(len(z)):
        g = (math.exp(lp[t]) if legal[t] else 0.0) - (1.0 if t == gold else 0.0)
        grad.append([g * a for a in h])
    return loss, grad
