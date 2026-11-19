# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/biaffine-dependency-parser/. The authors are listed in prov/XMKHK7.jsonl.

"""The scoring layer, the loss and the decoder of the biaffine parser of Dozat and Manning (2017).

The input is the list r_0, ..., r_n of BiLSTM output vectors (r_0 for the root),
taken as given. Two ReLU layers make a head view and a dependent view of each
word, and a biaffine product scores each arc:

    a_i = relu(W_ah r_i + b_ah)       (head view, k numbers)
    e_i = relu(W_ad r_i + b_ad)       (dependent view, k numbers)
    s(h, d) = a_h^T U e_d + a_h^T u   (U is k x k, u has k numbers)

The labels have their own views a'_i and e'_i (k' numbers) and, for each label l,

    s_l(h, d) = a'_h^T U_l e'_d + w_l^T [e'_d ; a'_h] + c_l.

Training uses, for each word d, the cross-entropy of the softmax of s(., d) over
the heads h != d, and the cross-entropy of the label softmax at the gold head.
Decoding takes the best head of each word; when these heads do not form a tree,
it takes the maximum spanning arborescence by Chu-Liu-Edmonds. Each word then
takes its best label for its head.

The module takes the network outputs as given; it implements one forward pass
of the scoring layer, the loss with its gradients in U and u, and the decoder.
It does not train a network.
"""

import math
from typing import Dict, List, Sequence, Tuple

from nlslog import argmax, log_softmax

Vector = List[float]
Matrix = List[List[float]]


def matvec(W: Matrix, x: Sequence[float]) -> Vector:
    return [math.fsum(w * a for w, a in zip(row, x)) for row in W]


def dot(x: Sequence[float], y: Sequence[float]) -> float:
    return math.fsum(a * b for a, b in zip(x, y))


def relu_layer(W: Matrix, b: Sequence[float], x: Sequence[float]) -> Vector:
    return [max(0.0, v + c) for v, c in zip(matvec(W, x), b)]


def biaffine(a: Sequence[float], U: Matrix, e: Sequence[float], u: Sequence[float]) -> float:
    """a^T U e + a^T u."""
    return dot(a, matvec(U, e)) + dot(a, u)


def arc_scores(A: Sequence[Vector], E: Sequence[Vector], U: Matrix, u: Sequence[float]) -> Matrix:
    """S[h][d] = s(h, d) for h, d in 0..n. Column 0 and the diagonal are not used."""
    m = len(A)
    Ue = [matvec(U, E[d]) for d in range(m)]
    return [[dot(A[h], Ue[d]) + dot(A[h], u) for d in range(m)] for h in range(m)]


def label_scores(Ah: Sequence[Vector], Ed: Sequence[Vector], Us: Sequence[Matrix], ws: Sequence[Vector], cs: Sequence[float], h: int, d: int) -> Vector:
    """[s_l(h, d) for each label l]."""
    cat = list(Ed[d]) + list(Ah[h])
    return [dot(Ah[h], matvec(U, Ed[d])) + dot(w, cat) + c for U, w, c in zip(Us, ws, cs)]


def head_log_probs(S: Matrix, d: int) -> Dict[int, float]:
    """log p(h | d) for each h != d, the softmax of the column S[.][d]."""
    hs = [h for h in range(len(S)) if h != d]
    return dict(zip(hs, log_softmax([S[h][d] for h in hs])))


def head_loss_and_grads(A: Sequence[Vector], E: Sequence[Vector], U: Matrix, u: Sequence[float], gold: Sequence[int]):
    """Sum over d of -log p(gold(d) | d), and its gradients in U and u.

    With q_d(h) = p(h | d) - [h = gold(d)], the gradient of the loss in S[h][d]
    is q_d(h), so d/dU = sum_d sum_h q_d(h) a_h e_d^T and d/du = sum_d sum_h q_d(h) a_h.
    """
    S = arc_scores(A, E, U, u)
    k = len(u)
    gU = [[0.0] * k for _ in range(k)]
    gu = [0.0] * k
    loss = 0.0
    for d in range(1, len(S)):
        lp = head_log_probs(S, d)
        loss -= lp[gold[d]]
        for h, v in lp.items():
            q = math.exp(v) - (1.0 if h == gold[d] else 0.0)
            for i in range(k):
                gu[i] += q * A[h][i]
                for j in range(k):
                    gU[i][j] += q * A[h][i] * E[d][j]
    return loss, gU, gu


def is_tree(heads: Sequence[int]) -> bool:
    n = len(heads) - 1
    for d in range(1, n + 1):
        x, steps = d, 0
        while x != 0:
            x, steps = heads[x], steps + 1
            if x < 0 or steps > n:
                return False
    return True


def _find_cycle(head: Dict[int, int], root: int):
    for start in head:
        seen, x = [], start
        while x != root and x not in seen:
            seen.append(x)
            x = head[x]
        if x != root:
            return seen[seen.index(x):]
    return None


def chu_liu_edmonds(nodes: Sequence[int], root: int, w: Dict[Tuple[int, int], float]) -> Dict[int, int]:
    """A maximum spanning arborescence rooted at root: a map from each other node to its head."""
    best = {}
    for d in nodes:
        if d == root:
            continue
        cands = [(w[h, d], h) for h in nodes if h != d and (h, d) in w]
        best[d] = max(cands)[1]
    cyc = _find_cycle(best, root)
    if cyc is None:
        return best
    cset = set(cyc)
    c = max(nodes) + 1
    cyc_score = math.fsum(w[best[v], v] for v in cyc)
    w2, enter, leave = {}, {}, {}
    for (h, d), s in w.items():
        if h in cset and d not in cset:
            if (c, d) not in w2 or s > w2[c, d]:
                w2[c, d], leave[d] = s, h
        elif h not in cset and d in cset:
            v = s - w[best[d], d] + cyc_score
            if (h, c) not in w2 or v > w2[h, c]:
                w2[h, c], enter[h] = v, d
        elif h not in cset and d not in cset:
            w2[h, d] = s
    sub = chu_liu_edmonds([v for v in nodes if v not in cset] + [c], root, w2)
    out = {}
    for d, h in sub.items():
        if d == c:
            continue
        out[d] = leave[d] if h == c else h
    entry = enter[sub[c]]
    for v in cyc:
        out[v] = best[v]
    out[entry] = sub[c]
    return out


def decode(S: Matrix) -> Tuple[List[int], bool]:
    """Return (heads, used_cle). The best head of each word, repaired by Chu-Liu-Edmonds if needed."""
    m = len(S)
    heads = [-1] + [max((h for h in range(m) if h != d), key=lambda h: S[h][d]) for d in range(1, m)]  # @line L3
    if is_tree(heads):  # @line L4
        return heads, False
    w = {(h, d): S[h][d] for h in range(m) for d in range(1, m) if h != d}
    t = chu_liu_edmonds(list(range(m)), 0, w)  # @line L5
    return [-1] + [t[d] for d in range(1, m)], True


def parse(R: Sequence[Vector], params: dict, labels: Sequence[str]):
    """One forward pass and the decoder. Returns (heads, labels, S, used_cle)."""
    A = [relu_layer(params["W_ah"], params["b_ah"], r) for r in R]  # @line L1
    E = [relu_layer(params["W_ad"], params["b_ad"], r) for r in R]
    S = arc_scores(A, E, params["U"], params["u"])  # @line L2
    heads, used = decode(S)
    Ah = [relu_layer(params["W_lh"], params["b_lh"], r) for r in R]
    Ed = [relu_layer(params["W_ld"], params["b_ld"], r) for r in R]
    out = [None] * len(R)
    for d in range(1, len(R)):
        ls = label_scores(Ah, Ed, params["Us"], params["ws"], params["cs"], heads[d], d)  # @line L6
        out[d] = labels[argmax(ls)]
    return heads, out, S, used  # @line L7
