# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dalal-revision/. The authors are listed in prov/WXMFTE.jsonl.

"""Dalal's revision operator on finite propositional belief bases.

A world (an interpretation) over n atoms is an integer w with 0 <= w < 2**n:
bit i of w is 1 when atom i is true. A belief base is given by its set of
models, a set of worlds. The revision K o p keeps the models of p that are at
minimum Hamming distance from some model of K (Dalal 1988).

The method grows the set of worlds around the models of K one Hamming layer at
a time, which is Dalal's generalization operator G applied again and again:
layer 0 is Mod(K), and layer d + 1 holds the worlds that differ in one atom
from a world of layer d and are in no earlier layer. The first layer that
meets Mod(p) is at the minimum distance, and its common part with Mod(p) is
the result.
"""


def hamming(u, v):
    """The number of atoms on which the worlds u and v differ."""
    return bin(u ^ v).count("1")


def _check_worlds(worlds, n, name):
    out = frozenset(worlds)
    limit = 1 << n
    for w in out:
        if not isinstance(w, int) or w < 0 or w >= limit:
            raise ValueError(f"{name} holds {w!r}, which is not a world over {n} atoms")
    return out


def dalal_revision_with_stats(k_models, p_models, n):
    """Return (result, d, visited, flips).

    result is Mod(K o p) as a frozenset. d is the minimum Hamming distance
    between a model of K and a model of p, or None when K or p has no model.
    visited is the number of worlds put in some layer, and flips is the number
    of one-atom changes that the layer loop tried.
    """
    if n < 0:
        raise ValueError("n must be at least 0")
    k = _check_worlds(k_models, n, "k_models")
    p = _check_worlds(p_models, n, "p_models")
    if not p:
        return frozenset(), None, 0, 0  # @line L1
    if not k:
        # Mod(K) is empty: every model of p is kept (Eiter and Gottlob 1992).
        return p, None, 0, 0  # @line L2
    layer, seen, d = k, set(k), 0  # @line L3
    flips = 0
    while not (layer & p):  # @line L4
        nxt = set()  # @line L5
        for w in layer:  # @line L6
            for i in range(n):  # @line L7
                flips += 1
                v = w ^ (1 << i)  # @line L8
                if v not in seen:  # @line L9
                    seen.add(v)
                    nxt.add(v)
        # nxt is not empty here: p has a model outside seen, and the cube is connected.
        layer, d = frozenset(nxt), d + 1  # @line L10
    return frozenset(layer & p), d, len(seen), flips  # @line L11


def dalal_revision(k_models, p_models, n):
    """Mod(K o p): the models of p at minimum Hamming distance from Mod(K)."""
    return dalal_revision_with_stats(k_models, p_models, n)[0]


def dalal_distance(k_models, p_models, n):
    """The minimum Hamming distance between Mod(K) and Mod(p), or None."""
    return dalal_revision_with_stats(k_models, p_models, n)[1]
