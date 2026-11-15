# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/possible-models-approach/. The authors are listed in prov/J9PKJ2.jsonl.

"""Winslett's possible models approach (PMA) to belief update.

A world over n atoms is an integer w with 0 <= w < 2**n: bit i of w is 1 when
atom i is true. A belief base is given by its set of models. The set of atoms
on which two worlds w and v differ is the integer w ^ v.

The update K <> p is the union, over the models w of K, of the models v of p
whose change set w ^ v is minimal under set inclusion among the change sets
from w to the models of p (Winslett 1988, Section 3).

For one model w, the method marks in an array C of 2**n bits every change set
x that leads from w into p, and then closes C upwards, one atom at a time, so
that C[x] says "some model of p differs from w only on atoms inside x". This
is the zeta transform over subsets. A model v of p is kept when no proper
subset of x = w ^ v is marked, and it is enough to test the n sets that miss
one atom of x.
"""


def _check_worlds(worlds, n, name):
    out = frozenset(worlds)
    limit = 1 << n
    for w in out:
        if not isinstance(w, int) or isinstance(w, bool) or w < 0 or w >= limit:
            raise ValueError(f"{name} holds {w!r}, which is not a world over {n} atoms")
    return out


def closest_models(w, p, n):
    """The models v of p for which w ^ v is minimal under set inclusion."""
    if w in p:
        return frozenset([w])  # the empty change set is below every other one
    size = 1 << n
    c = [False] * size
    for v in p:
        c[w ^ v] = True
    for i in range(n):
        bit = 1 << i
        for x in range(size):
            if x & bit and not c[x]:
                c[x] = c[x ^ bit]
    keep = []
    for v in p:
        x = w ^ v
        if not any(x >> i & 1 and c[x ^ (1 << i)] for i in range(n)):
            keep.append(v)
    return frozenset(keep)


def pma_update(k_models, p_models, n):
    """Mod(K <> p) under the possible models approach, as a frozenset."""
    if n < 0:
        raise ValueError("n must be at least 0")
    k = _check_worlds(k_models, n, "k_models")
    p = _check_worlds(p_models, n, "p_models")
    result = set()  # @line L1
    size = 1 << n
    for w in sorted(k):  # @line L2
        if w in p:  # @line L3
            result.add(w)  # @line L4
            continue
        c = [False] * size
        for v in p:
            c[w ^ v] = True  # @line L5
        for i in range(n):  # @line L6
            bit = 1 << i
            for x in range(size):
                if x & bit and not c[x]:
                    c[x] = c[x ^ bit]  # @line L7
        for v in p:  # @line L8
            x = w ^ v
            if not any(x >> i & 1 and c[x ^ (1 << i)] for i in range(n)):  # @line L9
                result.add(v)  # @line L10
    return frozenset(result)  # @line L11


def pma_update_per_model(k_models, p_models, n):
    """The same update, returned as a dict from each model of K to its set of closest models of p."""
    k = _check_worlds(k_models, n, "k_models")
    p = _check_worlds(p_models, n, "p_models")
    return {w: closest_models(w, p, n) for w in sorted(k)}
