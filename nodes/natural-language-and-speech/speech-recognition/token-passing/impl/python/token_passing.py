# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/token-passing/. The authors are listed in prov/CTEH7D.jsonl.

"""Token passing (Young, Russell and Thornton 1989) over a word network.

The network has grammar nodes, which do not emit, and word arcs between them.
A word arc (src, dst, word, g) is one copy of the HMM of the word, entered from
src with the log grammar score g and left into dst. A node can be final with a
log score. A bigram is the network with one node per previous word.

To keep the code short, each phone is one emitting HMM state with a self loop
(log probability loop) and a forward move (log probability fwd); the exit from
the last phone of a word is a forward move too. Scores are log probabilities,
higher is better. The score of a path is

    sum of the emission scores e_t(phone at frame t)
  + sum over phones of ((d - 1) * loop + fwd)          (d frames in the phone)
  + sum over the word arcs taken of (lm_weight * g + ip)
  + lm_weight * final(last node).

A token is (score, link). The link points to a word-link record (word, end
frame, score, previous link), so a token carries its word history. Each frame
every state keeps the best token that reaches it: this is the Viterbi max.
Each grammar node keeps the best token that leaves a word into it. With no
pruning the result is the best path; a beam can lose it.
"""

import math
from typing import Dict, List, Sequence, Tuple

from nlslog import NEG_INF

Token = Tuple[float, int]


class Network:
    """A word network: grammar nodes 0..n-1, a start node, final nodes and word arcs."""

    def __init__(self) -> None:
        self.num_nodes = 0
        self.start = 0
        self.final: Dict[int, float] = {}
        self.arcs: List[Tuple[int, int, str, float]] = []

    def add_node(self) -> int:
        self.num_nodes += 1
        return self.num_nodes - 1

    def add_word(self, src: int, dst: int, word: str, g: float = 0.0) -> None:
        self.arcs.append((src, dst, word, g))

    def set_final(self, q: int, score: float = 0.0) -> None:
        self.final[q] = score


def _better(a: Token, b: Token) -> bool:
    return a[0] > b[0]


def decode(
    net: Network,
    lexicon: Dict[str, Sequence[str]],
    emit: Sequence[Dict[str, float]],
    lm_weight: float = 1.0,
    ip: float = 0.0,
    loop: float = math.log(0.5),
    fwd: float = math.log(0.5),
    beam: float = math.inf,
):
    """Return (words, ends, score) for the best path through the network, or ([], [], -inf)."""
    n = len(emit)
    links: List[Tuple[str, int, float, int]] = []  # (word, end frame, score, previous link)
    node: Dict[int, Token] = {net.start: (0.0, -1)}  # @line L1
    toks: Dict[Tuple[int, int], Token] = {}
    for t in range(n):  # @line L2
        e = emit[t]
        new: Dict[Tuple[int, int], Token] = {}

        def offer(key: Tuple[int, int], tok: Token) -> None:
            if tok[0] > NEG_INF and (key not in new or _better(tok, new[key])):
                new[key] = tok

        for (a, j), (s, link) in toks.items():  # @line L3
            offer((a, j), (s + loop, link))
            if j + 1 < len(lexicon[net.arcs[a][2]]):
                offer((a, j + 1), (s + fwd, link))
        for a, (src, _, _, g) in enumerate(net.arcs):
            if src in node:
                s, link = node[src]
                offer((a, 0), (s + lm_weight * g + ip, link))
        toks = {}
        for (a, j), (s, link) in new.items():
            toks[(a, j)] = (s + e[lexicon[net.arcs[a][2]][j]], link)
        if toks:  # @line L4
            best = max(s for s, _ in toks.values())
            toks = {k: v for k, v in toks.items() if v[0] >= best - beam and v[0] > NEG_INF}
        node = {}  # @line L5
        for (a, j), (s, link) in sorted(toks.items()):  # @line L6
            src, dst, word, _ = net.arcs[a]
            if j == len(lexicon[word]) - 1:
                out = s + fwd
                if dst not in node or out > node[dst][0]:
                    links.append((word, t, out, link))
                    node[dst] = (out, len(links) - 1)
    best_link, best = -1, NEG_INF
    for q in sorted(node):  # @line L7
        if q in net.final:
            s = node[q][0] + lm_weight * net.final[q]
            if s > best:
                best_link, best = node[q][1], s
    if best_link < 0:
        return [], [], NEG_INF
    words: List[str] = []
    ends: List[int] = []
    r = best_link
    while r >= 0:
        w, t, _, r = links[r]
        words.append(w)
        ends.append(t)
    return words[::-1], ends[::-1], best


def bigram_network(vocab: Sequence[str], lm: Dict[Tuple[str, str], float]) -> Network:
    """Build the network of a bigram: node 0 is <s>, node i + 1 is vocab[i]; missing pairs get no arc."""
    net = Network()
    net.add_node()
    for _ in vocab:
        net.add_node()
    index = {"<s>": 0}
    index.update({w: i + 1 for i, w in enumerate(vocab)})
    for v in ["<s>"] + list(vocab):
        for w in vocab:
            if (v, w) in lm:
                net.add_word(index[v], index[w], w, lm[(v, w)])
    for w in vocab:
        if (w, "</s>") in lm:
            net.set_final(index[w], lm[(w, "</s>")])
    return net
