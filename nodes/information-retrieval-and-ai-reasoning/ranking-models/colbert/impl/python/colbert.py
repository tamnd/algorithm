# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/colbert/. The authors are listed in prov/26Y1DV.jsonl.

"""ColBERT late interaction on given token embeddings.

The encoders are outside this file. A query is a list of token vectors
q_1..q_n and a document is a list of token vectors d_1..d_m, all scaled to
unit length. The score is the sum of MaxSim:

    S(q, d) = sum over i of max over j of q_i . d_j.

End-to-end retrieval has two stages. Stage 1 runs, for each query vector,
an exact top-k' search over all document token vectors and keeps the
documents that own a hit. Stage 2 scores these candidates exactly and
returns the top k, with ties broken by the smaller document id. The real
system uses an approximate index in stage 1; this file uses an exact one.
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def normalize(v):
    n = math.sqrt(dot(v, v))
    return [x / n for x in v] if n > 0 else list(v)


def maxsim_score(q, d):
    return sum(max(dot(qi, dj) for dj in d) for qi in q)


def by_score(scored):
    return [doc for _, doc in sorted(scored, key=lambda t: (-t[0], t[1]))]


def exhaustive_top_k(q, docs, k):
    return by_score([(maxsim_score(q, d), i) for i, d in enumerate(docs)])[:k]


def token_index(docs):
    """(document id, token position, vector) for every token of every document."""
    return [(i, j, v) for i, d in enumerate(docs) for j, v in enumerate(d)]   # @line L1


def candidates(q, docs, k_prime):
    """The ids of the documents that own one of the top-k' tokens of some q_i."""
    index = token_index(docs)
    found = set()                                                            # @line L2
    for qi in q:                                                             # @line L3
        hits = sorted(index, key=lambda t: (-dot(qi, t[2]), t[0], t[1]))[:k_prime]
        found.update(doc for doc, _, _ in hits)                              # @line L4
    return sorted(found)


def missed_bound(q, docs, k_prime):
    """sum over i of the k'-th largest q_i . e over all document tokens.

    A document that stage 1 does not find scores at most this value.
    """
    total = 0.0
    for qi in q:
        vals = sorted((dot(qi, v) for _, _, v in token_index(docs)), reverse=True)
        total += vals[min(k_prime, len(vals)) - 1]
    return total


def end_to_end(q, docs, k_prime, k):
    cand = candidates(q, docs, k_prime)
    scored = [(maxsim_score(q, docs[i]), i) for i in cand]                   # @line L5
    return by_score(scored)[:k]                                              # @line L6


def pairwise_loss(q, pos, neg):
    """-log softmax over the two scores S(q, d+) and S(q, d-), for d+."""
    a, b = maxsim_score(q, pos), maxsim_score(q, neg)
    m = max(a, b)
    return -(a - m) + math.log(math.exp(a - m) + math.exp(b - m))


def argmax_token(qi, d):
    best = 0
    for j in range(1, len(d)):
        if dot(qi, d[j]) > dot(qi, d[best]):
            best = j
    return best


def pairwise_loss_gradient(q, pos, neg):
    """dL/dq_i, valid where each max has a unique argmax.

    The gradient is taken in the given vectors, not through normalize().
    """
    a, b = maxsim_score(q, pos), maxsim_score(q, neg)
    m = max(a, b)
    p_pos = math.exp(a - m) / (math.exp(a - m) + math.exp(b - m))
    out = []
    for qi in q:
        dp = pos[argmax_token(qi, pos)]
        dn = neg[argmax_token(qi, neg)]
        out.append([(p_pos - 1.0) * x + (1.0 - p_pos) * y for x, y in zip(dp, dn)])
    return out
