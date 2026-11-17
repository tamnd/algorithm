# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elston-stewart-algorithm/. The authors are listed in prov/7JJWSE.jsonl.

import random
from fractions import Fraction

import pytest

from elston_stewart_algorithm import (
    brute_force_likelihood,
    elston_stewart,
    genotype_posterior,
    one_locus_model,
)


def random_pedigree(rng, n_people):
    """A random loop-free pedigree: each new family joins the old ones at one person."""
    ped = {"F0": (None, None), "M0": (None, None)}
    couples = [("F0", "M0")]
    k = 0
    while len(ped) < n_people:
        if rng.random() < 0.5 or len(ped) == 2:
            f, m = rng.choice(couples)
        else:
            x = rng.choice([p for p in ped if ped[p][0] is not None] or list(ped))
            k += 1
            s = f"S{k}"
            ped[s] = (None, None)
            f, m = (x, s) if rng.random() < 0.5 else (s, x)
            couples.append((f, m))
            if len(ped) >= n_people:
                break
        k += 1
        ped[f"C{k}"] = (f, m)
    # A spouse without children would sit alone; give every couple a child.
    for f, m in couples:
        if not any(v == (f, m) for v in ped.values()):
            k += 1
            ped[f"C{k}"] = (f, m)
    return ped


def random_pen(rng, ped, G, frac=False, missing=0.3):
    pen = {}
    for p in ped:
        if rng.random() < missing:
            continue
        if frac:
            pen[p] = [Fraction(rng.randint(0, 4), 4) for _ in range(G)]
        else:
            pen[p] = [rng.random() for _ in range(G)]
    return pen


def test_mendel_table_rows_sum_to_one():
    genos, prior, trans = one_locus_model([Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)], Fraction(1))
    assert len(genos) == 6
    assert sum(prior) == 1
    for row in trans:
        for cell in row:
            assert sum(cell) == 1
    # Aa x Aa gives AA, Aa, aa in 1:2:1.
    _, _, t2 = one_locus_model([Fraction(1, 2), Fraction(1, 2)], Fraction(1))
    assert t2[1][1] == [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]


def test_no_data_gives_one():
    _, prior, trans = one_locus_model([Fraction(3, 10), Fraction(7, 10)], Fraction(1))
    ped = random_pedigree(random.Random(1), 7)
    assert elston_stewart(ped, prior, trans, {}, Fraction(1)) == 1


def test_recessive_example_of_the_page():
    # Allele 0 is D (frequency 0.9), allele 1 is d (0.1); affected iff dd.
    _, prior, trans = one_locus_model([Fraction(9, 10), Fraction(1, 10)], Fraction(1))
    unaff = [Fraction(1), Fraction(1), Fraction(0)]
    aff = [Fraction(0), Fraction(0), Fraction(1)]
    ped = {"father": (None, None), "mother": (None, None),
           "child1": ("father", "mother"), "child2": ("father", "mother")}
    pen = {"father": unaff, "mother": unaff, "child1": aff, "child2": unaff}
    L = elston_stewart(ped, prior, trans, pen, Fraction(1))
    assert L == Fraction(18, 100) ** 2 * Fraction(3, 16)
    assert L == Fraction(243, 40000)
    post = genotype_posterior(ped, prior, trans, pen, "child2", Fraction(1))
    assert post == [Fraction(1, 3), Fraction(2, 3), Fraction(0)]


def test_nuclear_family_exact_against_brute_force():
    rng = random.Random(7)
    for freqs in ([Fraction(1, 4), Fraction(3, 4)], [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]):
        _, prior, trans = one_locus_model(freqs, Fraction(1))
        G = len(prior)
        ped = {"f": (None, None), "m": (None, None),
               "c1": ("f", "m"), "c2": ("f", "m"), "c3": ("f", "m")}
        for _ in range(3):
            pen = random_pen(rng, ped, G, frac=True, missing=0.2)
            assert elston_stewart(ped, prior, trans, pen, Fraction(1)) == \
                brute_force_likelihood(ped, prior, trans, pen, Fraction(1))


def test_three_generations_against_brute_force():
    # Grandparents, two children who each marry in, and three grandchildren.
    ped = {"GF": (None, None), "GM": (None, None),
           "C1": ("GF", "GM"), "C2": ("GF", "GM"),
           "S1": (None, None), "S2": (None, None),
           "K1": ("C1", "S1"), "K2": ("C1", "S1"), "K3": ("S2", "C2")}
    _, prior, trans = one_locus_model([0.35, 0.65], 1.0)
    rng = random.Random(11)
    for _ in range(2):
        pen = random_pen(rng, ped, 3)
        a = elston_stewart(ped, prior, trans, pen, 1.0)
        b = brute_force_likelihood(ped, prior, trans, pen, 1.0)
        assert abs(a - b) <= 1e-12 * b


def test_half_sibs_and_random_pedigrees():
    # A father with children by two mothers: two families share one person.
    ped = {"f": (None, None), "m1": (None, None), "m2": (None, None),
           "a": ("f", "m1"), "b": ("f", "m1"), "c": ("f", "m2")}
    _, prior, trans = one_locus_model([Fraction(1, 5), Fraction(4, 5)], Fraction(1))
    pen = random_pen(random.Random(3), ped, 3, frac=True, missing=0.0)
    assert elston_stewart(ped, prior, trans, pen, Fraction(1)) == \
        brute_force_likelihood(ped, prior, trans, pen, Fraction(1))
    _, prior, trans = one_locus_model([0.2, 0.5, 0.3], 1.0)
    for seed in range(8):
        rng = random.Random(100 + seed)
        ped = random_pedigree(rng, rng.randint(3, 6))
        pen = random_pen(rng, ped, 6)
        a = elston_stewart(ped, prior, trans, pen, 1.0)
        b = brute_force_likelihood(ped, prior, trans, pen, 1.0)
        assert abs(a - b) <= 1e-12 * max(b, 1e-300)


def test_disconnected_pedigree_is_a_product():
    _, prior, trans = one_locus_model([Fraction(1, 3), Fraction(2, 3)], Fraction(1))
    a = {"f": (None, None), "m": (None, None), "c": ("f", "m")}
    b = {"x": (None, None), "y": (None, None), "z": ("x", "y"), "u": ("x", "y")}
    rng = random.Random(5)
    pa = random_pen(rng, a, 3, frac=True, missing=0.0)
    pb = random_pen(rng, b, 3, frac=True, missing=0.0)
    both = {**a, **b}
    assert elston_stewart(both, prior, trans, {**pa, **pb}, Fraction(1)) == \
        elston_stewart(a, prior, trans, pa, Fraction(1)) * elston_stewart(b, prior, trans, pb, Fraction(1))


def test_loop_is_rejected():
    # First cousins who have a child: an inbreeding loop.
    ped = {"GF": (None, None), "GM": (None, None),
           "A": ("GF", "GM"), "B": ("GF", "GM"),
           "SA": (None, None), "SB": (None, None),
           "X": ("A", "SA"), "Y": ("SB", "B"), "Z": ("X", "Y")}
    _, prior, trans = one_locus_model([0.5, 0.5], 1.0)
    with pytest.raises(ValueError):
        elston_stewart(ped, prior, trans, {}, 1.0)
    with pytest.raises(ValueError):
        elston_stewart({"a": ("b", None), "b": (None, None)}, prior, trans, {}, 1.0)
