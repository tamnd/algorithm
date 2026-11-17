# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lander-green-algorithm/. The authors are listed in prov/13J1K1.jsonl.

import itertools
import math
import random

import pytest

from lander_green_algorithm import (
    emission,
    gene_flow,
    haldane_theta,
    ibd_distribution,
    lander_green,
    nonfounders,
    topological,
    transition,
)

NUCLEAR = {"F": (None, None), "M": (None, None), "A": ("F", "M"), "B": ("F", "M")}
THREE_GEN = {"GF": (None, None), "GM": (None, None), "C": ("GF", "GM"),
             "S": (None, None), "K1": ("C", "S"), "K2": ("S", "C")}


def founders(ped):
    return [p for p in ped if ped[p][0] is None]


def brute_emission(ped, v, typed, freqs):
    """Sum over all allele labels of all founder genes."""
    genes = gene_flow(ped, v)
    fg = [(p, s) for p in founders(ped) for s in (0, 1)]
    total = 0.0
    for labels in itertools.product(range(len(freqs)), repeat=len(fg)):
        lab = dict(zip(fg, labels))
        ok = all(sorted((lab[genes[p][0]], lab[genes[p][1]])) == sorted(g) for p, g in typed.items())
        if ok:
            term = 1.0
            for x in labels:
                term *= freqs[x]
            total += term
    return total


def brute_likelihood(ped, markers, freqs, thetas):
    """Sum over all paths of inheritance vectors, with brute-force emissions."""
    bits = 2 * len(nonfounders(ped))
    size = 1 << bits
    e = [[brute_emission(ped, v, markers[j], freqs[j]) for v in range(size)] for j in range(len(markers))]
    total = 0.0
    for path in itertools.product(range(size), repeat=len(markers)):
        p = e[0][path[0]] / size
        for j in range(1, len(markers)):
            flips = bin(path[j] ^ path[j - 1]).count("1")
            p *= thetas[j - 1] ** flips * (1 - thetas[j - 1]) ** (bits - flips) * e[j][path[j]]
        total += p
    return total


def genotype_brute_single_marker(ped, typed, freqs):
    """One marker: sum over unordered genotypes with Hardy-Weinberg founders and Mendel."""
    k = len(freqs)
    genos = [(a, b) for a in range(k) for b in range(a, k)]
    order = topological(ped)
    total = 0.0
    for assign in itertools.product(range(len(genos)), repeat=len(order)):
        g = {p: genos[assign[t]] for t, p in enumerate(order)}
        if any(tuple(sorted(typed[p])) != g[p] for p in typed):
            continue
        term = 1.0
        for p in order:
            f, m = ped[p]
            a, b = g[p]
            if f is None:
                term *= freqs[a] * freqs[b] * (1 if a == b else 2)
            else:
                cnt = 0
                for x in g[f]:
                    for y in g[m]:
                        if tuple(sorted((x, y))) == (a, b):
                            cnt += 1
                term *= cnt / 4
        total += term
    return total


def simulate(rng, ped, n_markers, n_alleles, thetas, untyped=()):
    """Marker data from the model: random founder alleles and a Markov path of vectors."""
    bits = 2 * len(nonfounders(ped))
    freqs = []
    for _ in range(n_markers):
        w = [rng.random() + 0.2 for _ in range(n_alleles)]
        s = sum(w)
        freqs.append([x / s for x in w])
    v = rng.randrange(1 << bits)
    markers = []
    for j in range(n_markers):
        if j > 0:
            for b in range(bits):
                if rng.random() < thetas[j - 1]:
                    v ^= 1 << b
        genes = gene_flow(ped, v)
        lab = {}
        for p in founders(ped):
            for s in (0, 1):
                lab[(p, s)] = rng.choices(range(n_alleles), weights=freqs[j])[0]
        markers.append({p: (lab[genes[p][0]], lab[genes[p][1]]) for p in ped if p not in untyped})
    return markers, freqs


def test_haldane_and_transition():
    assert haldane_theta(0.0) == 0.0
    assert abs(haldane_theta(0.1) - 0.0906346) < 1e-7
    # The bitwise update equals the full matrix product.
    rng = random.Random(2)
    bits, theta = 3, 0.13
    x = [rng.random() for _ in range(8)]
    full = []
    for u in range(8):
        s = 0.0
        for v in range(8):
            fl = bin(u ^ v).count("1")
            s += theta ** fl * (1 - theta) ** (bits - fl) * x[v]
        full.append(s)
    fast = transition(x, bits, theta)
    assert max(abs(a - b) for a, b in zip(full, fast)) < 1e-14


def test_emission_against_founder_allele_sum():
    rng = random.Random(4)
    for ped in (NUCLEAR, THREE_GEN):
        bits = 2 * len(nonfounders(ped))
        markers, freqs = simulate(rng, ped, 3, 3, [0.2, 0.2], untyped=("GF",))
        for j in range(3):
            for v in range(1 << bits):
                a = emission(gene_flow(ped, v), markers[j], freqs[j])
                b = brute_emission(ped, v, markers[j], freqs[j])
                assert abs(a - b) <= 1e-12


def test_single_marker_against_genotype_sum():
    rng = random.Random(9)
    for ped, untyped in ((NUCLEAR, ()), (THREE_GEN, ("C",))):
        markers, freqs = simulate(rng, ped, 1, 3, [], untyped=untyped)
        ll, _ = lander_green(ped, markers, freqs, [])
        ref = genotype_brute_single_marker(ped, markers[0], freqs[0])
        assert abs(math.exp(ll) - ref) <= 1e-12 * ref


def test_multipoint_against_brute_force_paths():
    rng = random.Random(21)
    cases = ((NUCLEAR, 3, [0.1, 0.3], ()), (THREE_GEN, 2, [0.05], ("GF", "GM")))
    for ped, M, thetas, untyped in cases:
        markers, freqs = simulate(rng, ped, M, 2, thetas, untyped=untyped)
        ll, post = lander_green(ped, markers, freqs, thetas)
        ref = brute_likelihood(ped, markers, freqs, thetas)
        assert abs(ll - math.log(ref)) < 1e-10
        for pj in post:
            assert abs(sum(pj) - 1.0) < 1e-12


def test_unlinked_markers_factor():
    rng = random.Random(33)
    markers, freqs = simulate(rng, THREE_GEN, 3, 3, [0.5, 0.5])
    ll, _ = lander_green(THREE_GEN, markers, freqs, [0.5, 0.5])
    single = sum(lander_green(THREE_GEN, [markers[j]], [freqs[j]], [])[0] for j in range(3))
    assert abs(ll - single) < 1e-10


def test_ibd_of_relatives_without_data():
    ped = {"F": (None, None), "M": (None, None), "M2": (None, None),
           "A": ("F", "M"), "B": ("F", "M"), "H": ("F", "M2")}
    _, post = lander_green(ped, [{}], [[1.0]], [])
    sib = ibd_distribution(ped, post[0], "A", "B")
    half = ibd_distribution(ped, post[0], "A", "H")
    par = ibd_distribution(ped, post[0], "F", "A")
    assert [round(x, 12) for x in sib] == [0.25, 0.5, 0.25]
    assert [round(x, 12) for x in half] == [0.5, 0.5, 0.0]
    assert [round(x, 12) for x in par] == [0.0, 1.0, 0.0]


def test_sib_pair_example_of_the_page():
    # Parents 1/2 and 3/4, both children 1/3: the sibs share both genes for sure.
    markers = [{"F": (0, 1), "M": (2, 3), "A": (0, 2), "B": (0, 2)},
               {}]
    freqs = [[0.25] * 4, [1.0]]
    ll, post = lander_green(NUCLEAR, markers, freqs, [0.1])
    # Four of the 16 vectors fit (the phase of each parent is free), each with
    # founder allele probability (1/4)^4.
    assert abs(math.exp(ll) - 4 * 0.25 ** 4 / 16) < 1e-15
    assert [round(x, 12) for x in ibd_distribution(NUCLEAR, post[0], "A", "B")] == [0.0, 0.0, 1.0]
    p2 = ibd_distribution(NUCLEAR, post[1], "A", "B")
    # Each sib keeps the same gene from a parent when both or neither recombine.
    same = 0.9 ** 2 + 0.1 ** 2
    assert abs(p2[2] - same ** 2) < 1e-12
    assert abs(p2[1] - 2 * same * (1 - same)) < 1e-12


def test_mendel_error_raises():
    markers = [{"F": (0, 0), "M": (0, 0), "A": (1, 1)}]
    with pytest.raises(ValueError):
        lander_green(NUCLEAR, markers, [[0.5, 0.5]], [])
