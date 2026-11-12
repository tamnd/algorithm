# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latent-dirichlet-allocation/. The authors are listed in prov/JHNS1Q.jsonl.

"""Latent Dirichlet allocation: the generative process and collapsed Gibbs sampling
(Griffiths and Steyvers 2004), with symmetric priors alpha on topic proportions and beta on topics.

A corpus is a list of documents; a document is a list of word ids in 0 .. V-1.
"""

import random
from fractions import Fraction


def dirichlet(rng: random.Random, a, size):
    g = [rng.gammavariate(a, 1.0) for _ in range(size)]
    s = sum(g)
    return [v / s for v in g]


def categorical(rng: random.Random, p):
    u = rng.random() * sum(p)
    acc = 0.0
    for i, v in enumerate(p):
        acc += v
        if u < acc:
            return i
    return len(p) - 1


def generate(rng: random.Random, topics, alpha, num_docs, doc_len):
    """Draw a corpus from the LDA generative process with the given topic-word distributions.
    Return the documents and the true topic of each token."""
    k = len(topics)
    docs, zs = [], []
    for _ in range(num_docs):
        theta = dirichlet(rng, alpha, k)
        z = [categorical(rng, theta) for _ in range(doc_len)]
        docs.append([categorical(rng, topics[t]) for t in z])
        zs.append(z)
    return docs, zs


class Counts:
    """The count tables n_dk, n_kw and n_k of a topic assignment z."""

    def __init__(self, docs, z, k, v):
        self.ndk = [[0] * k for _ in docs]
        self.nkw = [[0] * v for _ in range(k)]
        self.nk = [0] * k
        for d, doc in enumerate(docs):
            for w, t in zip(doc, z[d]):
                self.add(d, w, t, 1)

    def add(self, d, w, t, c):
        self.ndk[d][t] += c
        self.nkw[t][w] += c
        self.nk[t] += c


def conditional(cnt, d, w, alpha, beta, v):
    """Unnormalized P(z_i = t | z_-i, w) for all t; token i must already be removed from cnt."""
    return [(cnt.ndk[d][t] + alpha) * (cnt.nkw[t][w] + beta) / (cnt.nk[t] + v * beta)
            for t in range(len(cnt.nk))]


def gibbs_sweep(docs, z, cnt, alpha, beta, v, rng: random.Random):
    for d, doc in enumerate(docs):  # @line L3
        for i, w in enumerate(doc):
            cnt.add(d, w, z[d][i], -1)  # @line L4
            p = conditional(cnt, d, w, alpha, beta, v)  # @line L5
            z[d][i] = categorical(rng, p)  # @line L6
            cnt.add(d, w, z[d][i], 1)  # @line L7


def collapsed_gibbs(docs, k, v, alpha, beta, sweeps, rng: random.Random):
    """Run collapsed Gibbs sampling; return the final assignment and its count tables."""
    z = [[rng.randrange(k) for _ in doc] for doc in docs]  # @line L1
    cnt = Counts(docs, z, k, v)  # @line L1
    for _ in range(sweeps):  # @line L2
        gibbs_sweep(docs, z, cnt, alpha, beta, v, rng)
    return z, cnt  # @line L8


def estimates(cnt, alpha, beta):
    """Posterior mean estimates of phi (topics) and theta (proportions) given one sample."""
    k, v = len(cnt.nk), len(cnt.nkw[0])
    phi = [[(cnt.nkw[t][w] + beta) / (cnt.nk[t] + v * beta) for w in range(v)] for t in range(k)]  # @line L9
    theta = [[(row[t] + alpha) / (sum(row) + k * alpha) for t in range(k)] for row in cnt.ndk]  # @line L9
    return phi, theta


def rising(a, n):
    """The rising factorial a (a + 1) ... (a + n - 1) = Gamma(a + n) / Gamma(a)."""
    r = Fraction(1) if isinstance(a, Fraction) else 1.0
    for i in range(n):
        r *= a + i
    return r


def collapsed_joint(docs, z, k, v, alpha, beta):
    """P(w, z | alpha, beta) with theta and phi integrated out (a product of Dirichlet-multinomials).
    Exact when alpha and beta are Fractions."""
    cnt = Counts(docs, z, k, v)
    p = Fraction(1) if isinstance(alpha, Fraction) else 1.0
    for d, doc in enumerate(docs):
        for t in range(k):
            p *= rising(alpha, cnt.ndk[d][t])
        p /= rising(k * alpha, len(doc))
    for t in range(k):
        for w in range(v):
            p *= rising(beta, cnt.nkw[t][w])
        p /= rising(v * beta, cnt.nk[t])
    return p
