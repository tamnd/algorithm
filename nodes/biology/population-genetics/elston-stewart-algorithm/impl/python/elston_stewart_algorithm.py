# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elston-stewart-algorithm/. The authors are listed in prov/7JJWSE.jsonl.
"""The Elston-Stewart algorithm (peeling) for the likelihood of a pedigree.

A pedigree maps each individual to a pair (father, mother). A founder has
(None, None); a non-founder has both parents in the pedigree. Individuals
with the same two parents form one nuclear family.

The genotype space is general: genotypes are the indices 0 .. G-1, prior[g]
is the probability of genotype g in a founder, trans[gf][gm][gc] is the
probability that parents with genotypes gf and gm have a child with genotype
gc, and pen[i][g] is the probability of the phenotype of individual i given
genotype g (the penetrance). An individual that is not a key of pen has no
data, which is the same as a penetrance of 1 for every genotype.

For one autosomal locus, one_locus_model() builds the unordered genotypes,
the Hardy-Weinberg prior and Mendel's transmission table.

The code uses only +, * and comparisons on the numbers, so it works with
float and with fractions.Fraction alike.
"""

from __future__ import annotations

from typing import Dict, Hashable, List, Mapping, Optional, Sequence, Tuple

Person = Hashable
Pedigree = Mapping[Person, Tuple[Optional[Person], Optional[Person]]]


def one_locus_model(freqs: Sequence, one=1):
    """Genotypes, founder prior and Mendelian transmission for one locus.

    freqs are the allele frequencies. The genotypes are the unordered pairs
    (a, b) with a <= b, in lexicographic order. The prior is Hardy-Weinberg:
    p_a^2 for (a, a) and 2 p_a p_b for (a, b). Each parent passes each of its
    two alleles with probability 1/2, independently of the other parent.
    """
    k = len(freqs)
    genos = [(a, b) for a in range(k) for b in range(a, k)]
    index = {g: i for i, g in enumerate(genos)}
    prior = [freqs[a] * freqs[b] * (1 if a == b else 2) for a, b in genos]
    half = one / 2
    quarter = half * half
    G = len(genos)
    zero = one - one
    trans = [[[zero] * G for _ in range(G)] for _ in range(G)]
    for i, gf in enumerate(genos):
        for j, gm in enumerate(genos):
            row = trans[i][j]
            for x in gf:
                for y in gm:
                    c = index[(min(x, y), max(x, y))]
                    row[c] += quarter
    return genos, prior, trans


def _families(ped: Pedigree):
    """The nuclear families as a dict (father, mother) -> list of children."""
    fams: Dict[Tuple[Person, Person], List[Person]] = {}
    for i, (f, m) in ped.items():
        if (f is None) != (m is None):
            raise ValueError(f"{i!r} has only one parent")
        if f is None:
            continue
        if f not in ped or m not in ped:
            raise ValueError(f"a parent of {i!r} is not in the pedigree")
        fams.setdefault((f, m), []).append(i)
    return fams


def _tree(ped: Pedigree, fams):
    """The bipartite graph of individuals and families, as a forest.

    Returns (roots, order, parent): order lists every node so that each node
    comes after its parent in the forest (a preorder), parent maps a node to
    its parent node (None for a root). A node is ('i', person) or
    ('f', (father, mother)). Raises ValueError if the graph has a cycle,
    which is a marriage or inbreeding loop of the pedigree.
    """
    adj: Dict[tuple, List[tuple]] = {("i", p): [] for p in ped}
    n_edges = 0
    for key, kids in fams.items():
        fnode = ("f", key)
        adj[fnode] = []
        for member in (key[0], key[1], *kids):
            adj[fnode].append(("i", member))
            adj[("i", member)].append(fnode)
            n_edges += 1
    parent: Dict[tuple, Optional[tuple]] = {}
    order: List[tuple] = []
    roots: List[tuple] = []
    for p in ped:
        start = ("i", p)
        if start in parent:
            continue
        roots.append(start)
        parent[start] = None
        stack = [start]
        while stack:
            v = stack.pop()
            order.append(v)  # @line L2
            for w in adj[v]:
                if w not in parent:
                    parent[w] = v
                    stack.append(w)
    if n_edges != len(adj) - len(roots):
        raise ValueError("the pedigree has a loop; peeling needs a loop-free pedigree")
    return roots, order, parent


def elston_stewart(ped: Pedigree, prior: Sequence, trans, pen: Mapping[Person, Sequence],
                   one=1):
    """The likelihood of the phenotypes of a loop-free pedigree, by peeling."""
    G = len(prior)
    zero = one - one
    ones = [one] * G
    fams = _families(ped)
    roots, order, parent = _tree(ped, fams)  # @line L1
    child_fams: Dict[Person, List[tuple]] = {}
    for node in order:
        par = parent[node]
        if node[0] == "f":
            child_fams.setdefault(par[1], []).append(node)
    w: Dict[Person, List] = {}  # the message from an individual to its parent family
    msg: Dict[tuple, List] = {}  # the message from a family to its parent individual
    total = one
    for v in reversed(order):  # @line L3
        if v[0] == "i":  # @line L4
            i = v[1]
            vec = list(pen.get(i, ones))
            if ped[i][0] is None:
                vec = [vec[g] * prior[g] for g in range(G)]
            for fnode in child_fams.get(i, ()):
                m = msg[fnode]
                vec = [vec[g] * m[g] for g in range(G)]
            w[i] = vec  # @line L5
            if parent[v] is None:
                s = zero
                for g in range(G):
                    s += vec[g]
                total = total * s  # @line L10
            continue
        f, m = v[1]  # @line L6
        kids = fams[(f, m)]
        p = parent[v][1]
        S = {}
        for c in kids:  # @line L7
            if c == p:
                continue
            wc = w[c]
            table = [[zero] * G for _ in range(G)]
            for gf in range(G):
                for gm in range(G):
                    row = trans[gf][gm]
                    s = zero
                    for gc in range(G):
                        s += row[gc] * wc[gc]
                    table[gf][gm] = s
            S[c] = table

        def kids_product(gf, gm):
            prod = one
            for table in S.values():
                prod = prod * table[gf][gm]
            return prod

        out = [zero] * G
        if p == f or p == m:  # @line L8
            other = w[m] if p == f else w[f]
            for gp in range(G):
                s = zero
                for go in range(G):
                    if other[go] == zero:
                        continue
                    gf, gm = (gp, go) if p == f else (go, gp)
                    s += other[go] * kids_product(gf, gm)
                out[gp] = s
        else:  # @line L9
            wf, wm = w[f], w[m]
            for gf in range(G):
                if wf[gf] == zero:
                    continue
                for gm in range(G):
                    if wm[gm] == zero:
                        continue
                    base = wf[gf] * wm[gm] * kids_product(gf, gm)
                    row = trans[gf][gm]
                    for gp in range(G):
                        out[gp] += base * row[gp]
        msg[v] = out
    return total


def brute_force_likelihood(ped: Pedigree, prior: Sequence, trans, pen, one=1):
    """The same likelihood as a sum over all G^n joint genotype assignments."""
    people = list(ped)
    G = len(prior)
    pos = {p: k for k, p in enumerate(people)}
    total = one - one
    assign = [0] * len(people)
    n = len(people)
    while True:
        term = one
        for k, p in enumerate(people):
            g = assign[k]
            f, m = ped[p]
            if f is None:
                term = term * prior[g]
            else:
                term = term * trans[assign[pos[f]]][assign[pos[m]]][g]
            if p in pen:
                term = term * pen[p][g]
        total += term
        k = 0
        while k < n and assign[k] == G - 1:
            assign[k] = 0
            k += 1
        if k == n:
            return total
        assign[k] += 1


def genotype_posterior(ped: Pedigree, prior: Sequence, trans, pen, person, one=1):
    """P(genotype of person = g | all phenotypes), for each g, by G + 1 peelings."""
    L = elston_stewart(ped, prior, trans, pen, one)
    base = pen.get(person, [one] * len(prior))
    zero = one - one
    post = []
    for g in range(len(prior)):
        pen_g = dict(pen)
        pen_g[person] = [base[h] if h == g else zero for h in range(len(prior))]
        post.append(elston_stewart(ped, prior, trans, pen_g, one) / L)
    return post
