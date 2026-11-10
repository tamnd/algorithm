# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-inapproximability/. The authors are listed in prov/KWSQM6.jsonl.

"""The FGLSS graph of a nonadaptive verifier, and a brute-force check of it.

A verifier is a list of tests, one for each random string. A test is a pair
(positions, accepted): positions is a tuple of distinct proof positions in
increasing order, and accepted is a set of tuples of bits, one bit for each
position, on which the verifier accepts. A proof is a tuple of bits.
The brute-force helpers are exponential and are for small instances only.
"""

from itertools import product

Test = tuple[tuple[int, ...], frozenset[tuple[int, ...]]]


def acceptance_count(tests: list[Test], proof: tuple[int, ...]) -> int:
    """The number of random strings on which the verifier accepts the proof."""
    return sum(1 for pos, acc in tests if tuple(proof[i] for i in pos) in acc)


def max_acceptance(tests: list[Test], proof_length: int) -> int:
    """max over all proofs of acceptance_count, by trying all 2^proof_length proofs."""
    return max(acceptance_count(tests, p) for p in product((0, 1), repeat=proof_length))


def fglss_graph(tests: list[Test]) -> tuple[list[tuple[int, tuple[int, ...]]], list[int]]:
    """Vertices are the accepting views (r, a). Two views are joined when r differ and they agree.

    Returns the list of vertices and the adjacency of each vertex as a bit mask.
    """
    verts = [(r, a) for r, (pos, acc) in enumerate(tests) for a in sorted(acc)]
    views = [dict(zip(tests[r][0], a)) for r, a in verts]
    adj = [0] * len(verts)
    for u in range(len(verts)):
        for v in range(u + 1, len(verts)):
            if verts[u][0] == verts[v][0]:
                continue
            du, dv = views[u], views[v]
            if all(dv[i] == b for i, b in du.items() if i in dv):
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    return verts, adj


def max_clique(adj: list[int]) -> list[int]:
    """A maximum clique, by branch and bound on bit masks with an explicit stack."""
    best: list[int] = []
    stack = [([], (1 << len(adj)) - 1)]
    while stack:
        clique, cand = stack.pop()
        if not cand:
            if len(clique) > len(best):
                best = clique
            continue
        if len(clique) + bin(cand).count("1") <= len(best):
            continue
        v = cand.bit_length() - 1
        rest = cand & ~(1 << v)
        stack.append((clique, rest))  # cliques without v
        stack.append((clique + [v], rest & adj[v]))  # cliques with v
    return best


def clique_to_proof(tests: list[Test], verts: list[tuple[int, tuple[int, ...]]], clique: list[int], proof_length: int) -> tuple[int, ...]:
    """The map from a clique to a proof: copy the bits of the views; other bits are 0."""
    proof = [0] * proof_length
    for v in clique:
        r, a = verts[v]
        for i, b in zip(tests[r][0], a):
            proof[i] = b
    return tuple(proof)


def clause_verifier(clauses: list[tuple[int, ...]]) -> list[Test]:
    """The verifier that reads an assignment, picks a random clause and checks it.

    The proof position i holds the value of variable i + 1.
    """
    tests = []
    for c in clauses:
        pos = tuple(sorted({abs(l) - 1 for l in c}))
        acc = set()
        for bits in product((0, 1), repeat=len(pos)):
            val = dict(zip(pos, bits))
            if any(val[abs(l) - 1] == (1 if l > 0 else 0) for l in c):
                acc.add(bits)
        tests.append((pos, frozenset(acc)))
    return tests


def repeat_verifier(tests: list[Test], k: int) -> list[Test]:
    """Sequential repetition: k independent random strings; accept when all k tests accept."""
    out = list(tests)
    for _ in range(k - 1):
        new = []
        for pos1, acc1 in out:
            for pos2, acc2 in tests:
                pos = tuple(sorted(set(pos1) | set(pos2)))
                acc = set()
                for bits in product((0, 1), repeat=len(pos)):
                    val = dict(zip(pos, bits))
                    if tuple(val[i] for i in pos1) in acc1 and tuple(val[i] for i in pos2) in acc2:
                        acc.add(bits)
                new.append((pos, frozenset(acc)))
        out = new
    return out
