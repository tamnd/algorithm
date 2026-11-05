# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-graph/. The authors are listed in prov/ZCP03V.jsonl.

import itertools
import random
from typing import List

import pytest

from de_bruijn_graph import DeBruijnGraph, complete_graph


def kmers_of(reads: List[str], k: int) -> List[str]:
    return [r[i : i + k] for r in reads for i in range(len(r) - k + 1)]


def test_example():
    g = DeBruijnGraph(3)
    for r in ("ACGTCG", "GTCGAT"):
        g.add_read(r)
    g.check_invariant(kmers_of(["ACGTCG", "GTCGAT"], 3))
    assert g.edges() == {"ACG": 1, "CGT": 1, "GTC": 2, "TCG": 2, "CGA": 1, "GAT": 1}
    assert sorted(g.successors("CG")) == ["GA", "GT"]
    assert sorted(g.predecessors("CG")) == ["AC", "TC"]
    assert g.successors("AT") == [] and g.predecessors("AC") == []
    walk = ["AC", "CG", "GT", "TC", "CG", "GA", "AT"]
    assert g.spell(walk) == "ACGTCGAT"
    assert g.spell(["AC", "CG", "GA", "AT"]) == "ACGAT"
    assert g.spell(g.eulerian_walk()) == "ACGTCGAT"
    b = complete_graph("01", 3)
    circuit = ["00", "00", "01", "10", "01", "11", "11", "10", "00"]
    assert b.spell(circuit) == "0001011100"


def test_edge_cases():
    with pytest.raises(ValueError):
        DeBruijnGraph(1)
    g = DeBruijnGraph(4)
    g.add_read("abc")
    g.add_read("")
    assert g.edges() == {} and g.vertices() == []
    assert g.eulerian_walk() is None
    g.add_read("aaaaa")
    assert g.edges() == {"aaaa": 2}
    assert g.successors("aaa") == ["aaa"]
    assert g.spell(["aaa", "aaa", "aaa"]) == "aaaaa"
    with pytest.raises(ValueError):
        g.spell(["aaa", "aab"])
    with pytest.raises(ValueError):
        g.add_kmer("ab")
    g.check_invariant(["aaaa", "aaaa"])


def is_de_bruijn(s: str, alphabet: str, n: int) -> bool:
    t = s + s[: n - 1]
    return len(s) == len(alphabet) ** n and len({t[i : i + n] for i in range(len(s))}) == len(s)


def test_complete_graphs_give_de_bruijn_sequences():
    for alphabet in ("a", "ab", "abc"):
        for k in range(2, 6 if len(alphabet) < 3 else 5):
            g = complete_graph(alphabet, k)
            g.check_invariant()
            assert len(g.vertices()) == len(alphabet) ** (k - 1)
            for u in g.vertices():
                assert len(g.successors(u)) == len(alphabet) == len(g.predecessors(u))
            walk = g.eulerian_walk()
            s = g.spell(walk)
            assert walk[0] == walk[-1]
            assert is_de_bruijn(s[: len(alphabet) ** k], alphabet, k)


def test_exhaustive_small_spelling():
    # Every string of length <= 6 over {a, b} is spelled by the walk of its
    # K-mers, and every walk of length 3 spells a string with those K-mers.
    for k in (2, 3):
        for n in range(k, 7):
            for t in itertools.product("ab", repeat=n):
                s = "".join(t)
                g = DeBruijnGraph(k)
                g.add_read(s)
                g.check_invariant(kmers_of([s], k))
                walk = [s[i : i + k - 1] for i in range(n - k + 2)]
                assert g.spell(walk) == s


def test_random_against_brute_force():
    rng = random.Random(1946)
    for trial in range(700):
        sigma = rng.choice((1, 2, 3))
        alphabet = "abc"[:sigma]
        k = rng.randint(2, 5)
        reads = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            for _ in range(rng.randint(1, 4))
        ]
        g = DeBruijnGraph(k)
        for r in reads:
            g.add_read(r)
        km = kmers_of(reads, k)
        g.check_invariant(km)
        distinct = set(km)
        vertices = {x[:-1] for x in distinct} | {x[1:] for x in distinct}
        for u in vertices:
            assert sorted(g.successors(u)) == sorted(x[1:] for x in distinct if x[:-1] == u)
            assert sorted(g.predecessors(u)) == sorted(x[:-1] for x in distinct if x[1:] == u)
        if not vertices:
            continue
        # A random walk spells a string whose K-mers are the walk's edges.
        u = rng.choice(sorted(vertices))
        walk = [u]
        for _ in range(rng.randint(0, 8)):
            nxt = g.successors(walk[-1])
            if not nxt:
                break
            walk.append(rng.choice(nxt))
        s = g.spell(walk)
        assert len(s) == k - 1 + len(walk) - 1
        assert [s[i : i + k] for i in range(len(walk) - 1)] == [
            walk[i] + walk[i + 1][-1] for i in range(len(walk) - 1)
        ]
        ew = g.eulerian_walk()
        if ew is not None:
            spelled = g.spell(ew)
            assert sorted(spelled[i : i + k] for i in range(len(spelled) - k + 1)) == sorted(distinct)
