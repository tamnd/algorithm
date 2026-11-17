# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variation-graph/. The authors are listed in prov/XJVQNQ.jsonl.

import itertools
import random

from variation_graph import build, find, haplotype_path, spell, walks

EXAMPLE_REF = "CTAGGATCCAGT"
EXAMPLE_VARIANTS = [(2, "A", "G"), (5, "AT", ""), (9, "", "TT")]


def apply(ref, variants, chosen):
    """ref with the chosen variants (indices into the sorted list) applied, built directly."""
    out, t = [], 0
    for v, (pos, a, b) in enumerate(sorted(variants)):
        out.append(ref[t:pos])
        out.append(b if v in chosen else a)
        t = pos + len(a)
    out.append(ref[t:])
    return "".join(out)


def random_case(rng):
    n = rng.randint(4, 16)
    ref = "".join(rng.choice("ACGT") for _ in range(n))
    variants, x = [], 1 + rng.randint(0, 2)
    while x < n - 1 and len(variants) < 4:
        la = rng.randint(0, min(3, n - 1 - x))
        lb = rng.randint(0, 3)
        a = ref[x:x + la]
        b = "".join(rng.choice("ACGT") for _ in range(lb))
        if a != b:
            variants.append((x, a, b))
            x += la + 1 + rng.randint(0, 2)
        else:
            x += 1
    return ref, variants


def test_example_graph():
    g = build(EXAMPLE_REF, EXAMPLE_VARIANTS)
    assert g.seq == ["CT", "A", "G", "GG", "AT", "CC", "TT", "AGT"]
    assert g.succ == [[1, 2], [3], [3], [4, 5], [5], [6, 7], [7], []]
    assert g.paths["ref"] == [0, 1, 3, 4, 5, 7]
    assert spell(g, g.paths["ref"]) == EXAMPLE_REF
    assert spell(g, haplotype_path(g, [0, 1, 2])) == "CTGGGCCTTAGT"
    assert len(walks(g)) == 8


def test_example_find():
    g = build(EXAMPLE_REF, EXAMPLE_VARIANTS)
    # This read needs the deletion and the insertion; it is not in the reference.
    assert find(g, "AGGCCTTA") == [(1, 0)]
    assert "AGGCCTTA" not in EXAMPLE_REF
    # A read of the reference is found at its reference place.
    assert find(g, "GGATCC") == [(3, 0)]
    # GG starts in two places: at the start of node 3, and in node 2 across the edge to node 3.
    assert find(g, "GG") == [(2, 0), (3, 0)]
    assert find(g, "GGGG") == []


def test_ids_are_a_topological_order():
    rng = random.Random(11)
    for _ in range(300):
        ref, vs = random_case(rng)
        g = build(ref, vs)
        for u, out in enumerate(g.succ):
            assert all(w > u for w in out)
        assert all(g.seq)


def test_paths_are_the_haplotypes():
    rng = random.Random(12)
    for _ in range(300):
        ref, vs = random_case(rng)
        g = build(ref, vs)
        assert spell(g, g.paths["ref"]) == ref
        subsets = [c for r in range(len(vs) + 1) for c in itertools.combinations(range(len(vs)), r)]
        paths = []
        for c in subsets:
            p = haplotype_path(g, c)
            assert spell(g, p) == apply(ref, vs, set(c))
            paths.append(p)
        # Each walk is the path of exactly one subset of the variants.
        assert sorted(paths) == walks(g)
        assert len(walks(g)) == 2 ** len(vs)


def brute_find(g, s):
    starts = set()
    for w in walks(g):
        owner = [(i, k) for i in w for k in range(len(g.seq[i]))]
        text = spell(g, w)
        for p in range(len(text) - len(s) + 1):
            if text[p:p + len(s)] == s:
                starts.add(owner[p])
    return sorted(starts)


def test_find_against_all_walks():
    rng = random.Random(13)
    checked = 0
    for _ in range(200):
        ref, vs = random_case(rng)
        g = build(ref, vs)
        hap = apply(ref, vs, {v for v in range(len(vs)) if rng.random() < 0.5})
        for _ in range(4):
            if rng.random() < 0.7:
                i = rng.randrange(len(hap))
                s = hap[i:i + rng.randint(1, 8)]
            else:
                s = "".join(rng.choice("ACGT") for _ in range(rng.randint(1, 5)))
            got = find(g, s)
            assert got == brute_find(g, s)
            checked += bool(got)
    assert checked > 300


def test_rejects_bad_variants():
    for vs in ([(0, "C", "G")], [(11, "T", "A")], [(2, "A", "G"), (3, "G", "C")],
               [(2, "A", "A")], [(2, "G", "C")], [(2, "A", "G"), (2, "", "T")]):
        try:
            build(EXAMPLE_REF, vs)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {vs}")
