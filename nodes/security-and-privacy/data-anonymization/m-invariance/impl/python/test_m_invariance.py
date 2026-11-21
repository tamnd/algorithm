# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/m-invariance/. The authors are listed in prov/DJ2GGT.jsonl.

import random

import pytest

from m_invariance import counterfeits, extends_m_invariant, is_m_invariant, is_m_unique

R1 = [
    [("Bob", "dyspepsia"), ("Carol", "bronchitis")],
    [("Dan", "flu"), ("Eve", "gastritis")],
]
NAIVE_R2 = [
    [("Bob", "dyspepsia"), ("Eve", "gastritis"), ("Gina", "flu")],
    [("Dan", "flu"), ("Frank", "pneumonia")],
]
GOOD_R2 = [
    [("Bob", "dyspepsia"), (None, "bronchitis")],
    [("Dan", "flu"), ("Eve", "gastritis")],
    [("Frank", "pneumonia"), ("Gina", "flu")],
]


def test_example() -> None:
    assert is_m_unique(R1, 2) and is_m_unique(NAIVE_R2, 2) and is_m_unique(GOOD_R2, 2)
    assert not is_m_invariant([R1, NAIVE_R2], 2)
    assert is_m_invariant([R1, GOOD_R2], 2)
    assert not extends_m_invariant(R1, NAIVE_R2, 2)
    assert extends_m_invariant(R1, GOOD_R2, 2)
    assert counterfeits(GOOD_R2) == [(1, 1)]
    assert counterfeits(NAIVE_R2) == []
    # the candidate values of Bob and Dan in the naive pair
    assert {"dyspepsia", "bronchitis"} & {"dyspepsia", "gastritis", "flu"} == {"dyspepsia"}
    assert {"flu", "gastritis"} & {"flu", "pneumonia"} == {"flu"}
    assert not is_m_invariant([R1, GOOD_R2], 3)


def test_edges() -> None:
    assert is_m_invariant([], 3)
    assert is_m_invariant([[]], 3)
    assert is_m_invariant([R1], 2)
    assert not is_m_invariant([R1], 3)
    # repeated sensitive value in a group
    assert not is_m_invariant([[[("a", "x"), ("b", "x"), ("c", "y")]]], 2)
    # a group made only of counterfeits is allowed by the definition
    assert is_m_invariant([[[(None, "x"), (None, "y")]]], 2)
    with pytest.raises(ValueError):
        is_m_invariant([[[("a", "x"), ("b", "y")], [("a", "z"), ("c", "w")]]], 2)


def oracle(releases: list, m: int) -> bool:
    for release in releases:
        for group in release:
            values = [v for _, v in group]
            if len(values) < m or len(set(values)) < len(values):
                return False
    history: dict = {}
    for release in releases:
        for group in release:
            sig = sorted({v for _, v in group})
            for rid, _ in group:
                if rid is not None:
                    history.setdefault(rid, []).append(sig)
    return all(all(s == sigs[0] for s in sigs) for sigs in history.values())


VALUES = "pqrstu"


def random_case(rng: random.Random) -> tuple[list, int, dict]:
    m = rng.randint(1, 3)
    n = rng.randint(1, 4)
    value = {}
    life = {}
    bucket = {}
    for r in range(rng.randint(0, 10)):
        v = rng.choice(VALUES)
        others = [x for x in VALUES if x != v]
        value[r] = v
        bucket[r] = frozenset([v] + rng.sample(others, m - 1 + rng.randint(0, 1)))
        x = rng.randint(1, n)
        life[r] = (x, rng.randint(x, n))
    releases = []
    for j in range(1, n + 1):
        present = [r for r in value if life[r][0] <= j <= life[r][1]]
        release = []
        for sig in sorted({bucket[r] for r in present}, key=sorted):
            lists = {v: [r for r in present if bucket[r] == sig and value[r] == v] for v in sorted(sig)}
            for g in range(max(len(x) for x in lists.values())):
                release.append([(lists[v][g], v) if g < len(lists[v]) else (None, v) for v in sorted(sig)])
        releases.append(release)
    # break the construction in about half of the cases
    if releases and rng.random() < 0.5:
        rel = rng.choice(releases)
        if len(rel) >= 2:
            a, b = rng.sample(range(len(rel)), 2)
            i, k = rng.randrange(len(rel[a])), rng.randrange(len(rel[b]))
            rel[a][i], rel[b][k] = rel[b][k], rel[a][i]
        elif rel and rel[0]:
            i = rng.randrange(len(rel[0]))
            rel[0][i] = (rel[0][i][0], rng.choice(VALUES))
    return releases, m, value


def test_against_oracle() -> None:
    rng = random.Random(41)
    positive = 0
    for _ in range(800):
        releases, m, value = random_case(rng)
        got = is_m_invariant(releases, m)
        assert got == oracle(releases, m)
        positive += got
        # Lemma 4: the incremental test agrees with the full test
        chain = is_m_unique(releases[0], m) if releases else True
        for j in range(1, len(releases)):
            chain = chain and extends_m_invariant(releases[j - 1], releases[j], m)
        assert chain == got
        # the persistent candidate set of each record has at least m values and holds its value
        if got:
            for rid in value:
                hosts = [g for rel in releases for g in rel if any(r == rid for r, _ in g)]
                if hosts:
                    common = frozenset.intersection(*[frozenset(x for _, x in g) for g in hosts])
                    own = {x for g in hosts for r, x in g if r == rid}
                    assert own <= common and len(common) >= m
    assert 200 < positive < 800
