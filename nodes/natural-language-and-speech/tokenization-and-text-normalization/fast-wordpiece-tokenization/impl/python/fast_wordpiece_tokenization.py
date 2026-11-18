# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-wordpiece-tokenization/. The authors are listed in prov/PZXMS8.jsonl.

"""Fast WordPiece tokenization: LinMaxMatch of Song et al. (2021).

The vocabulary is put in a trie. Each node v gets a failure link f(v) and a
list of failure pops F(v): the tokens that greedy longest match first emits
when the match cannot go on from v. With these, one left-to-right pass over a
word gives the same tokens as the greedy encoder of BERT, in time linear in
the length of the word.

Nodes are integers. Node 0 is the root r, and SUFFIX_ROOT is the node of the
suffix indicator "##". A missing link is None.
"""

from collections import deque
from typing import Dict, List, Optional, Sequence, Set, Tuple

PREFIX = "##"
UNK = "[UNK]"
END = " "  # the end mark appended to a word; no token may contain it


class Trie:
    """The trie of a vocabulary, with failure links and failure pops."""

    def __init__(self, vocab: Set[str]):
        for tok in vocab:
            if not tok or tok == PREFIX or END in tok:
                raise ValueError("a token must be nonempty, not the bare prefix, and free of the end mark")
        self.vocab = set(vocab)
        self.children: List[Dict[str, int]] = [{}]
        self.string: List[str] = [""]
        for tok in sorted(self.vocab | {PREFIX}):
            self._insert(tok)
        self.root = 0
        self.suffix_root = self.node_of(PREFIX)
        n = len(self.children)
        self.fail: List[Optional[int]] = [None] * n
        self.pops: List[List[str]] = [[] for _ in range(n)]

    def _insert(self, tok: str) -> None:
        u = 0
        for ch in tok:
            nxt = self.children[u].get(ch)
            if nxt is None:
                nxt = len(self.children)
                self.children[u][ch] = nxt
                self.children.append({})
                self.string.append(self.string[u] + ch)
            u = nxt

    def node_of(self, s: str) -> Optional[int]:
        """Return the node whose string is s, or None."""
        u: Optional[int] = 0
        for ch in s:
            u = self.children[u].get(ch)
            if u is None:
                return None
        return u

    def delta(self, u: int, ch: str) -> Optional[int]:
        return self.children[u].get(ch)


def precompute(vocab: Set[str]) -> Trie:
    """Algorithm 2 of Song et al.: fill f and F by a breadth-first search."""
    t = Trie(vocab)  # @line P1
    assert all(f is None for f in t.fail) and not any(t.pops)  # @line P2
    r, rs = t.root, t.suffix_root
    queue = deque([r, rs])  # @line P3
    while queue:  # @line P4
        u = queue.popleft()  # @line P5
        for c, v in t.children[u].items():  # @line P6
            if v == rs:  # @line P7
                continue
            if t.string[v] in t.vocab:  # @line P8
                t.fail[v], t.pops[v] = rs, [t.string[v]]
            else:  # @line P9
                z, zpops = t.fail[u], []  # @line P10
                while z is not None and t.delta(z, c) is None:  # @line P11
                    zpops, z = zpops + t.pops[z], t.fail[z]  # @line P12
                if z is not None:  # @line P13
                    t.fail[v], t.pops[v] = t.delta(z, c), t.pops[u] + zpops
            queue.append(v)  # @line P14
    return t  # @line P15


def max_match(word: str, vocab: Set[str]) -> List[str]:
    """The original greedy longest-match-first encoder, with no length limit."""
    out, start = [], 0
    while start < len(word):
        end, piece = len(word), None
        while start < end:
            sub = word[start:end] if start == 0 else PREFIX + word[start:end]
            if sub in vocab:
                piece = sub
                break
            end -= 1
        if piece is None:
            return [UNK]
        out.append(piece)
        start = end
    return out


def lin_max_match(word: str, t: Trie, stats: Optional[Dict[str, int]] = None) -> List[str]:
    """Algorithm 1 of Song et al.: the tokens of one word in one pass.

    If stats is a dict, it gets the number of goto steps ("goto") and of
    failure steps ("fail") of the pass.
    """
    if END in word:
        raise ValueError("the word must not contain the end mark")
    s = word + END  # @line L1
    u, tokens, i = t.root, [], 0  # @line L2
    goto = fail = 0
    stuck = False
    while i < len(s) and not stuck:  # @line L3
        while t.delta(u, s[i]) is None:  # @line L4
            if t.fail[u] is None:  # @line L5
                stuck = True
                break
            tokens.extend(t.pops[u])  # @line L6
            u = t.fail[u]  # @line L7
            fail += 1
        if not stuck:
            u, i = t.delta(u, s[i]), i + 1  # @line L8
            goto += 1
    if stats is not None:
        stats["goto"], stats["fail"] = goto, fail
    if i < len(word) or u not in (t.root, t.suffix_root):  # @line L9
        return [UNK]
    if u == t.suffix_root and not tokens:  # @line L10
        return max_match(PREFIX, t.vocab)
    return tokens  # @line L11


def tokenize(words: Sequence[str], vocab: Set[str]) -> List[str]:
    """Build the trie once and encode a list of words."""
    t = precompute(vocab)
    out: List[str] = []
    for w in words:
        out.extend(lin_max_match(w, t))
    return out


def failure_table(t: Trie) -> Dict[str, Tuple[List[str], Optional[str]]]:
    """Map each node string to (F(v), string of f(v)), for checks and display."""
    return {
        t.string[v]: (list(t.pops[v]), None if t.fail[v] is None else t.string[t.fail[v]])
        for v in range(len(t.children))
    }
