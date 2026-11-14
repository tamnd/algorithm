# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mustang-state-assignment/. The authors are listed in prov/R8HB82.jsonl.

"""A MUSTANG-style encoder: attraction weights, then a greedy cube embedding.

The machine format is the one of fsmlogic: (ni, no, states, rows) with rows
(inp, ps, ns, out). The weights follow the two ideas of Devadas, Ma, Newton
and Sangiovanni-Vincentelli. The fanout-oriented weight pulls together
present states that go to the same next state or assert the same output;
the fanin-oriented weight pulls together next states reached from the same
present state or under the same input. The exact weight formulas of the
paper are not copied here; these are simplified forms.
"""

from itertools import combinations


def fanout_weights(fsm, k):
    """w(s, t) = k * sum_u a(s, u) a(t, u) + sum_j b(s, j) b(t, j).

    a(s, u) counts the rows from s to u, and b(s, j) counts the rows of s
    that assert output j. A shared next state counts k times because its
    whole code is shared.
    """
    ni, no, states, rows = fsm
    a = {s: {} for s in states}
    b = {s: [0] * no for s in states}
    for inp, ps, ns, out in rows:
        a[ps][ns] = a[ps].get(ns, 0) + 1
        for j, c in enumerate(out):
            if c == "1":
                b[ps][j] += 1
    w = {}
    for s, t in combinations(states, 2):
        x = k * sum(a[s][u] * a[t].get(u, 0) for u in a[s])
        x += sum(b[s][j] * b[t][j] for j in range(no))
        w[(s, t)] = x
    return w


def fanin_weights(fsm, k):
    """w(s, t) = k * sum_p c(p, s) c(p, t) + sum_x d(x, s) d(x, t).

    c(p, s) counts the rows from p to s, and d(x, s) counts the rows with
    input cube x that go to s.
    """
    ni, no, states, rows = fsm
    c = {p: {} for p in states}
    d = {}
    for inp, ps, ns, out in rows:
        c[ps][ns] = c[ps].get(ns, 0) + 1
        d.setdefault(inp, {})
        d[inp][ns] = d[inp].get(ns, 0) + 1
    w = {}
    for s, t in combinations(states, 2):
        x = k * sum(c[p].get(s, 0) * c[p].get(t, 0) for p in states)
        x += sum(dx.get(s, 0) * dx.get(t, 0) for dx in d.values())
        w[(s, t)] = x
    return w


def pair_weight(w, s, t):
    return w.get((s, t), w.get((t, s), 0))


def embedding_cost(w, codes):
    """sum over pairs of w(s, t) times the Hamming distance of their codes."""
    return sum(x * bin(codes[s] ^ codes[t]).count("1") for (s, t), x in w.items())


def greedy_embed(states, w, k):
    """Place the states one by one on the corners of the k-cube.

    The next state to place is the one with the largest total weight to
    the placed states (the largest total weight overall to start). It goes
    to the free corner with the least weighted distance to the placed
    states. Ties go to the earlier state and the smaller code.
    """
    total = {s: sum(pair_weight(w, s, t) for t in states if t != s) for s in states}
    codes = {}  # @line L4
    left = list(states)
    while left:  # @line L5
        if codes:
            s = max(left, key=lambda s: (sum(pair_weight(w, s, t) for t in codes), total[s], -states.index(s)))  # @line L6
        else:
            s = max(left, key=lambda s: (total[s], -states.index(s)))
        used = set(codes.values())
        best = min(  # @line L7
            (c for c in range(1 << k) if c not in used),
            key=lambda c: (sum(pair_weight(w, s, t) * bin(c ^ codes[t]).count("1") for t in codes), c),
        )
        codes[s] = best
        left.remove(s)
    return codes  # @line L8


def mustang_encode(fsm, mode="fanout", k=None):
    """Return (k, codes) for mode "fanout" or "fanin"."""
    ni, no, states, rows = fsm
    if k is None:
        k = max(1, (len(states) - 1).bit_length())  # @line L1
    w = fanout_weights(fsm, k) if mode == "fanout" else fanin_weights(fsm, k)  # @line L2 L3
    return k, greedy_embed(states, w, k)
