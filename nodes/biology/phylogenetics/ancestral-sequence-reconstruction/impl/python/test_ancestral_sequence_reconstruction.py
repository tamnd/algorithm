# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-sequence-reconstruction/. The authors are listed in prov/GHTCE8.jsonl.

import itertools
import random
from fractions import Fraction

from ancestral_sequence_reconstruction import (
    joint_reconstruction,
    marginal_posteriors,
    marginal_reconstruction,
    reconstruct_sequences,
)


def jc69_from_x(x):
    same = Fraction(1, 4) + Fraction(3, 4) * x
    diff = Fraction(1, 4) - Fraction(1, 4) * x
    return [[same if i == j else diff for j in range(4)] for i in range(4)]


def random_tree(n, rng):
    nodes = list(range(n))
    children = {}
    nxt = n
    while len(nodes) > 1:
        r = 3 if len(nodes) >= 3 and rng.random() < 0.2 else 2
        picked = rng.sample(nodes, r)
        for v in picked:
            nodes.remove(v)
        children[nxt] = picked
        nodes.append(nxt)
        nxt += 1
    return children, nodes[0]


def joint_probabilities(children, root, P, pi, site):
    """All assignments of the internal nodes with Pr(assignment, leaves)."""
    k = len(pi)
    internal = sorted(children)
    out = []
    for states in itertools.product(range(k), repeat=len(internal)):
        s = dict(site)
        s.update(zip(internal, states))
        prob = pi[s[root]]
        for v, kids in children.items():
            for c in kids:
                prob *= P[c][s[v]][s[c]]
        out.append((dict(zip(internal, states)), prob))
    return out


def random_instance(rng, general):
    k = rng.randint(2, 4) if general else 4
    n = rng.randint(2, 5)
    children, root = random_tree(n, rng)
    if general:
        w = [rng.randint(1, 9) for _ in range(k)]
        pi = [Fraction(x, sum(w)) for x in w]
        P = {}
        for kids in children.values():
            for c in kids:
                rows = []
                for _ in range(k):
                    r = [rng.randint(1, 9) for _ in range(k)]
                    rows.append([Fraction(x, sum(r)) for x in r])
                P[c] = rows
    else:
        pi = [Fraction(1, 4)] * 4
        P = {c: jc69_from_x(Fraction(rng.randint(1, 19), 20)) for kids in children.values() for c in kids}
    site = {v: rng.randrange(k) for v in range(n)}
    return children, root, P, pi, site


def test_joint_against_brute_force():
    rng = random.Random(11)
    for trial in range(150):
        children, root, P, pi, site = random_instance(rng, general=trial % 2 == 1)
        table = joint_probabilities(children, root, P, pi, site)
        best = max(p for _, p in table)
        value, states = joint_reconstruction(children, root, P, pi, site)
        assert value == best
        prob = [p for s, p in table if s == states]
        assert prob == [best]


def test_marginal_against_brute_force():
    rng = random.Random(12)
    for trial in range(150):
        children, root, P, pi, site = random_instance(rng, general=trial % 2 == 1)
        table = joint_probabilities(children, root, P, pi, site)
        total = sum(p for _, p in table)
        post = marginal_posteriors(children, root, P, pi, site)
        k = len(pi)
        for v in children:
            want = [sum(p for s, p in table if s[v] == a) / total for a in range(k)]
            assert post[v] == want
        rec = marginal_reconstruction(children, root, P, pi, site)
        for v in children:
            assert post[v][rec[v]] == max(post[v])


def test_marginal_and_joint_can_differ():
    # Root r has children u and leaf z; u has leaves x and y. Leaf y hangs on a
    # long branch. Sites: x = A, y = C, z = C. All maxima below are strict.
    children = {"r": ["u", "z"], "u": ["x", "y"]}
    short, long_ = jc69_from_x(Fraction(9, 10)), jc69_from_x(Fraction(1, 5))
    P = {"u": short, "z": short, "x": short, "y": long_}
    pi = [Fraction(1, 4)] * 4
    site = {"x": 0, "y": 1, "z": 1}
    value, states = joint_reconstruction(children, "r", P, pi, site)
    assert states == {"r": 1, "u": 1}
    table = joint_probabilities(children, "r", P, pi, site)
    ranked = sorted(p for _, p in table)
    assert value == ranked[-1] > ranked[-2]
    post = marginal_posteriors(children, "r", P, pi, site)
    assert sorted(post["r"])[-1] > sorted(post["r"])[-2]
    assert sorted(post["u"])[-1] > sorted(post["u"])[-2]
    rec = marginal_reconstruction(children, "r", P, pi, site)
    assert rec == {"r": 1, "u": 0}
    total = sum(ranked)
    prob = dict((tuple(sorted(s.items())), p) for s, p in table)
    joint_post = prob[(("r", 1), ("u", 1))] / total
    marg_post = prob[(("r", 1), ("u", 0))] / total
    assert joint_post == 2 * marg_post


def test_sequences_and_edges():
    children = {"r": ["x", "y"]}
    x = Fraction(4, 5)
    P = {"x": jc69_from_x(x), "y": jc69_from_x(x)}
    pi = [Fraction(1, 4)] * 4
    alignment = {"x": [0, 1, 2, 3], "y": [0, 1, 3, 3]}
    rec = reconstruct_sequences(children, "r", P, pi, alignment)
    assert rec["r"][0] == 0 and rec["r"][1] == 1 and rec["r"][3] == 3
    assert rec["r"][2] in (2, 3)
    rec_m = reconstruct_sequences(children, "r", P, pi, alignment, joint=False)
    assert rec_m["r"][0] == 0 and rec_m["r"][3] == 3
