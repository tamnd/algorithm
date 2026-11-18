# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/similarity-flooding/. The authors are listed in prov/BY6RCV.jsonl.

import itertools
import random

from similarity_flooding import (
    FORMULAS,
    flood,
    pairwise_connectivity_graph,
    similarity_flooding,
    stable_filter,
)

A = [("Emp", "col", "Name"), ("Emp", "col", "Dept"), ("Name", "type", "string"), ("Dept", "type", "int")]
B = [("Staff", "col", "Unit"), ("Staff", "col", "FullName"), ("FullName", "type", "varchar"), ("Unit", "type", "integer")]
S0 = {("string", "varchar"): 1.0, ("int", "integer"): 1.0}


def dense_flood(ga, gb, sigma0, formula, iters):
    """The oracle: the matrix of the definition, built from the two graphs directly, and the same iteration."""
    na = sorted({x for a, _, a2 in ga for x in (a, a2)})
    nb = sorted({x for b, _, b2 in gb for x in (b, b2)})
    pairs = sorted(set(itertools.product(na, nb)) | set(sigma0))
    idx = {p: i for i, p in enumerate(pairs)}
    n = len(pairs)
    m = [[0.0] * n for _ in range(n)]  # m[y][x]: weight of x -> y
    sa, sb = sorted(set(ga)), sorted(set(gb))
    for x in pairs:
        for label in sorted({e[1] for e in sa}):
            outs = [(a2, b2) for (a, l1, a2) in sa for (b, l2, b2) in sb
                    if l1 == label and l2 == label and (a, b) == x]
            ins = [(a, b) for (a, l1, a2) in sa for (b, l2, b2) in sb
                   if l1 == label and l2 == label and (a2, b2) == x]
            for y in outs:
                m[idx[y]][idx[x]] += 1.0 / len(outs)
            for y in ins:
                m[idx[y]][idx[x]] += 1.0 / len(ins)
    s0 = [float(sigma0.get(p, 0.0)) for p in pairs]
    s = list(s0)
    for _ in range(iters):
        if formula == "basic":
            base, arg = s, s
        elif formula == "A":
            base, arg = s0, s
        elif formula == "B":
            base, arg = [0.0] * n, [u + v for u, v in zip(s0, s)]
        else:
            arg = [u + v for u, v in zip(s0, s)]
            base = arg
        new = [base[i] + sum(m[i][j] * arg[j] for j in range(n)) for i in range(n)]
        top = max(new, default=0.0)
        if top > 0:
            new = [v / top for v in new]
        s = new
    return {p: s[idx[p]] for p in pairs}


def random_graph(rng, prefix, n_nodes, n_edges, labels):
    nodes = [prefix + str(i) for i in range(n_nodes)]
    return [(rng.choice(nodes), rng.choice(labels), rng.choice(nodes)) for _ in range(n_edges)]


def test_example_pcg():
    pcg = pairwise_connectivity_graph(A, B)
    assert len(pcg) == 8
    assert (("Emp", "Staff"), "col", ("Name", "FullName")) in pcg


def test_example_values():
    sig, it = flood(A, B, S0, "C")
    assert abs(sig[("Emp", "Staff")] - 1.0) < 1e-12
    assert round(sig[("Name", "FullName")], 4) == 0.9653
    assert round(sig[("Dept", "FullName")], 4) == 0.1418
    pairs, _ = similarity_flooding(A, B, S0, "C", threshold=0.5)
    assert pairs == [("Dept", "Unit"), ("Emp", "Staff"), ("Name", "FullName"), ("int", "integer"), ("string", "varchar")]
    # The basic formula forgets the initial similarities: the two column pairs tie.
    sig_b, _ = flood(A, B, S0, "basic")
    assert abs(sig_b[("Name", "FullName")] - sig_b[("Name", "Unit")]) < 1e-6


def test_first_steps_by_hand():
    sig, _ = flood(A, B, S0, "basic", eps=0, max_iter=3)
    assert abs(sig[("Dept", "FullName")] - 1 / 12) < 1e-12
    assert abs(sig[("Name", "FullName")] - 0.75) < 1e-12
    assert abs(sig[("int", "integer")] - 2 / 3) < 1e-12


def test_against_dense_oracle():
    rng = random.Random(7)
    for _ in range(40):
        ga = random_graph(rng, "a", rng.randint(1, 4), rng.randint(0, 6), ["l", "m"])
        gb = random_graph(rng, "b", rng.randint(1, 4), rng.randint(0, 6), ["l", "m"])
        na = sorted({x for a, _, a2 in ga for x in (a, a2)}) or ["a0"]
        nb = sorted({x for b, _, b2 in gb for x in (b, b2)}) or ["b0"]
        s0 = {(x, y): rng.choice([0.0, 0.5, 1.0]) for x in na for y in nb}
        for formula in FORMULAS:
            k = rng.randint(1, 6)
            got, it = flood(ga, gb, s0, formula, eps=0, max_iter=k)
            assert it == k
            want = dense_flood(ga, gb, s0, formula, k)
            for p in set(got) | set(want):
                assert abs(got.get(p, 0.0) - want.get(p, 0.0)) < 1e-9


def test_range_and_symmetry():
    rng = random.Random(11)
    for _ in range(30):
        ga = random_graph(rng, "a", 3, rng.randint(1, 6), ["l", "m"])
        gb = random_graph(rng, "b", 3, rng.randint(1, 6), ["l", "m"])
        s0 = {("a%d" % i, "b%d" % j): rng.random() for i in range(3) for j in range(3)}
        for formula in FORMULAS:
            sig, _ = flood(ga, gb, s0, formula, max_iter=50)
            vals = list(sig.values())
            assert all(-1e-12 <= v <= 1 + 1e-12 for v in vals)
            # Formula B drops sigma0 when no edge propagates, so the vector can be zero.
            assert abs(max(vals) - 1.0) < 1e-12 or max(vals) == 0.0
            rev, _ = flood(gb, ga, {(y, x): v for (x, y), v in s0.items()}, formula, max_iter=50)
            for (x, y), v in sig.items():
                assert abs(rev[(y, x)] - v) < 1e-9


def test_stable_filter_is_stable():
    rng = random.Random(3)
    for _ in range(200):
        na, nb = rng.randint(0, 4), rng.randint(0, 4)
        sig = {("a%d" % i, "b%d" % j): rng.choice([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
               for i in range(na) for j in range(nb)}
        th = rng.choice([0.0, 0.3, 0.7])
        pairs = stable_filter(sig, th)
        left = [a for a, _ in pairs]
        right = [b for _, b in pairs]
        assert len(set(left)) == len(left) and len(set(right)) == len(right)
        assert all(sig[p] >= th and sig[p] > 0 for p in pairs)
        mate_a = dict(pairs)
        mate_b = {b: a for a, b in pairs}

        def pref_a(a, b):  # smaller is better
            return (-sig[(a, b)], b)

        def pref_b(b, a):
            return (-sig[(a, b)], a)

        for (a, b), v in sig.items():
            if v < th or v <= 0 or mate_a.get(a) == b:
                continue
            a_wants = a not in mate_a or pref_a(a, b) < pref_a(a, mate_a[a])
            b_wants = b not in mate_b or pref_b(b, a) < pref_b(b, mate_b[b])
            assert not (a_wants and b_wants)


def test_edges():
    sig, it = flood([], [], {}, "C")
    assert sig == {} and it == 1
    # No common label: nothing propagates, and the basic formula keeps sigma0 scaled.
    sig, _ = flood([("x", "l", "y")], [("u", "m", "v")], {("x", "u"): 0.5, ("y", "v"): 0.25}, "basic")
    assert sig == {("x", "u"): 1.0, ("y", "v"): 0.5}
    assert stable_filter({}, 0.0) == []
    try:
        flood(A, B, S0, "D")
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown formula must fail")
