# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-knowledge-proof/. The authors are listed in prov/EZD2B7.jsonl.
"""Two classic zero-knowledge proofs, each with a simulator.

1. Graph isomorphism (Goldreich, Micali and Wigderson 1991). The prover knows
   a permutation pi with G1 = pi(G0). Each round: send H = sigma(G1) for a
   random sigma, receive a bit b, answer with a permutation tau with
   tau(G_b) = H. Soundness error 1/2 per round. Perfect zero knowledge.

2. Graph 3-coloring (the same paper). The prover knows a proper 3-coloring.
   Each round: permute the three colors at random, commit to the color of each
   vertex with a hash commitment, receive an edge, open its two ends.
   Soundness error at most 1 - 1/|E| per round. Computational zero knowledge,
   because the unopened commitments are only computationally hiding.

Graphs are frozensets of edges (u, v) with u < v on vertices 0..n-1, and a
permutation is a tuple perm with perm[v] the new name of v.

For study only. The code is not constant time and the parties are local
simulated objects. Use a reviewed proof system library for real proofs.
"""

import hashlib


# ---------------------------------------------------------------- graphs
def edge(u, v):
    return (u, v) if u < v else (v, u)


def apply_perm(perm, graph):
    return frozenset(edge(perm[u], perm[v]) for u, v in graph)


def compose(p, q):
    """(p o q)[v] = p[q[v]]: first q, then p."""
    return tuple(p[q[v]] for v in range(len(q)))


def random_perm(n, rng):
    perm = list(range(n))
    rng.shuffle(perm)
    return tuple(perm)


# --------------------------------------------------- graph isomorphism proof
class GIProver:
    def __init__(self, g0, g1, pi, n):
        assert apply_perm(pi, g0) == g1
        self.g0, self.g1, self.pi, self.n = g0, g1, pi, n

    def first(self, rng, sigma=None):
        self.sigma = random_perm(self.n, rng) if sigma is None else sigma
        return apply_perm(self.sigma, self.g1)          # H = sigma(G1)

    def answer(self, b):
        if b == 1:
            return self.sigma                            # sigma(G1) = H
        return compose(self.sigma, self.pi)              # sigma(pi(G0)) = H


def gi_verify(g0, g1, h, b, tau):
    return apply_perm(tau, g1 if b else g0) == h


def gi_run(prover, g0, g1, rounds, rng):
    for _ in range(rounds):
        h = prover.first(rng)
        b = rng.getrandbits(1)
        if not gi_verify(g0, g1, h, b, prover.answer(b)):
            return False
    return True


def gi_simulate(g0, g1, n, rng, b=None, tau=None):
    """An honest-verifier transcript (H, b, tau) made without pi."""
    b = rng.getrandbits(1) if b is None else b
    tau = random_perm(n, rng) if tau is None else tau
    return apply_perm(tau, g1 if b else g0), b, tau


def gi_simulate_against(verifier_bit, g0, g1, n, rng, max_tries=200):
    """Simulator for any verifier, given as a function H -> b. Rewinds.

    Guess b', make H = tau(G_b'), ask the verifier; keep the transcript if
    the verifier's bit equals the guess, else rewind. Expected 2 tries.
    """
    for tries in range(1, max_tries + 1):
        guess = rng.getrandbits(1)
        tau = random_perm(n, rng)
        h = apply_perm(tau, g1 if guess else g0)
        if verifier_bit(h) == guess:
            return (h, guess, tau), tries
    return None, max_tries


class GICheater:
    """A prover with no isomorphism: prepares H for a guessed bit."""

    def __init__(self, g0, g1, n):
        self.g0, self.g1, self.n = g0, g1, n

    def first(self, rng):
        self.guess = rng.getrandbits(1)
        self.tau = random_perm(self.n, rng)
        return apply_perm(self.tau, self.g1 if self.guess else self.g0)

    def answer(self, b):
        return self.tau            # right only when b equals the guess


# --------------------------------------------------- 3-coloring proof
def commit(value: int, r: bytes):
    return hashlib.sha256(r + bytes([value])).digest()


class ColoringProver:
    def __init__(self, graph, coloring):
        for u, v in graph:
            assert coloring[u] != coloring[v]
        self.graph, self.coloring = graph, coloring

    def first(self, rng, perm=None):
        if perm is None:
            perm = [0, 1, 2]
            rng.shuffle(perm)
        self.colors = [perm[c] for c in self.coloring]
        self.rs = [rng.getrandbits(256).to_bytes(32, "big") for _ in self.colors]
        return [commit(c, r) for c, r in zip(self.colors, self.rs)]

    def answer(self, e):
        u, v = e
        return (self.colors[u], self.rs[u]), (self.colors[v], self.rs[v])


def coloring_verify(graph, commitments, e, opening):
    if e not in graph:
        return False
    (cu, ru), (cv, rv) = opening
    u, v = e
    return (
        commit(cu, ru) == commitments[u]
        and commit(cv, rv) == commitments[v]
        and cu in (0, 1, 2)
        and cv in (0, 1, 2)
        and cu != cv
    )


def coloring_run(prover, graph, rounds, rng):
    edges = sorted(graph)
    for _ in range(rounds):
        coms = prover.first(rng)
        e = rng.choice(edges)
        if not coloring_verify(graph, coms, e, prover.answer(e)):
            return False
    return True


def coloring_simulate(graph, n, rng, e=None, pair=None):
    """Honest-verifier transcript without a coloring.

    Pick the edge first, give its ends two random distinct colors, commit to
    color 0 for every other vertex.
    """
    e = rng.choice(sorted(graph)) if e is None else e
    cu, cv = rng.sample([0, 1, 2], 2) if pair is None else pair
    colors = [0] * n
    colors[e[0]], colors[e[1]] = cu, cv
    rs = [rng.getrandbits(256).to_bytes(32, "big") for _ in range(n)]
    coms = [commit(c, r) for c, r in zip(colors, rs)]
    return coms, e, ((cu, rs[e[0]]), (cv, rs[e[1]]))


def best_cheating_acceptance(graph, n):
    """Max over all color assignments of the fraction of edges with distinct colors.

    A prover bound by its commitments passes a round exactly when the
    verifier picks such an edge. Exhaustive over 3^n assignments.
    """
    best = 0
    for code in range(3 ** n):
        colors = [(code // 3 ** i) % 3 for i in range(n)]
        good = sum(colors[u] != colors[v] for u, v in graph)
        best = max(best, good)
    return best, len(graph)
