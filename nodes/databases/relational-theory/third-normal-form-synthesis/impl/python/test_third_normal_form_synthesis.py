# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/third-normal-form-synthesis/. The authors are listed in prov/NWV2WW.jsonl.

import random
from itertools import combinations

from third_normal_form_synthesis import closure, fd, is_lossless, minimal_cover, synthesize


def subsets(s: frozenset) -> list[frozenset]:
    xs = sorted(s)
    return [frozenset(c) for n in range(len(xs) + 1) for c in combinations(xs, n)]


def projection(fds: list, r: frozenset) -> list:
    """The FDs Z -> (Z+ intersect R) for each Z inside R: a cover of F projected on R."""
    return [(z, closure(fds, z) & r) for z in subsets(r)]


def is_3nf_brute_force(r: frozenset, fds: list) -> bool:
    """3NF of schema R under the projection of fds, by the definition."""
    proj = projection(fds, r)
    keys = []
    for z, c in proj:
        if c >= r and not any(k <= z for k in keys):
            keys.append(z)
    prime = frozenset().union(*keys)
    return all(c >= r or (c - z) <= prime for z, c in proj)


def preserves(fds: list, schemas: list) -> bool:
    union = [d for r in schemas for d in projection(fds, r)]
    return all(rhs <= closure(union, lhs) for lhs, rhs in fds)


def names(schemas: list) -> list[str]:
    return sorted("".join(sorted(s)) for s in schemas)


def random_fds(rng: random.Random, attrs: str) -> list:
    return [fd(rng.sample(attrs, rng.randint(0, 3)), rng.sample(attrs, rng.randint(1, 2))) for _ in range(rng.randint(0, 6))]


def random_instance(rng: random.Random, attrs: str, fds: list) -> set:
    """A random relation, then values merged column by column until it satisfies fds."""
    rows = [{a: rng.randrange(3) for a in attrs} for _ in range(rng.randint(1, 6))]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            for t in rows:
                for u in rows:
                    if all(t[a] == u[a] for a in lhs):
                        for a in rhs:
                            if t[a] != u[a]:
                                old, new = u[a], t[a]
                                for w in rows:
                                    if w[a] == old:
                                        w[a] = new
                                changed = True
    return {tuple(t[a] for a in attrs) for t in rows}


def join_of_projections(attrs: str, rel: set, schemas: list) -> set:
    out = {()}
    cols: list[str] = []
    for s in schemas:
        pos = [attrs.index(a) for a in sorted(s)]
        proj = {tuple(t[p] for p in pos) for t in rel}
        new_cols = cols + [a for a in sorted(s) if a not in cols]
        joined = set()
        for left in out:
            for right in proj:
                row = dict(zip(cols, left))
                if all(row.get(a, v) == v for a, v in zip(sorted(s), right)):
                    row.update(zip(sorted(s), right))
                    joined.add(tuple(row[a] for a in new_cols))
        out, cols = joined, new_cols
    return {tuple(dict(zip(cols, t))[a] for a in attrs) for t in out}


def test_course_schema() -> None:
    f = [fd("C", "T"), fd("HR", "C"), fd("HT", "R"), fd("CS", "G"), fd("HS", "R")]
    s = synthesize("CTHRSG", f)
    assert names(s) == ["CGS", "CHR", "CT", "HRS", "HRT"]
    assert is_lossless("CTHRSG", s, f)


def test_key_schema_added() -> None:
    # A -> B, C -> D: no schema holds a key, so the key AC is added.
    f = [fd("A", "B"), fd("C", "D")]
    s = synthesize("ABCD", f)
    assert names(s) == ["AB", "AC", "CD"]
    assert is_lossless("ABCD", s, f)
    assert not is_lossless("ABCD", [frozenset("AB"), frozenset("CD")], f)


def test_city_street_zip() -> None:
    f = [fd("CS", "Z"), fd("Z", "C")]
    assert names(synthesize("CSZ", f)) == ["CSZ"]


def test_edges() -> None:
    assert names(synthesize("ABC", [])) == ["ABC"]
    assert names(synthesize("AB", [fd("A", "B")])) == ["AB"]
    assert names(synthesize("AB", [fd("", "A")])) == ["A", "B"]


def test_random_properties() -> None:
    rng = random.Random(8)
    attrs = "ABCDEF"
    for _ in range(150):
        f = random_fds(rng, attrs)
        schemas = synthesize(attrs, f)
        assert frozenset().union(*schemas) == frozenset(attrs)
        assert not any(s < t for s in schemas for t in schemas)
        assert all(is_3nf_brute_force(s, f) for s in schemas)
        assert preserves(f, schemas)
        assert is_lossless(attrs, schemas, f)
        assert is_lossless(attrs, schemas, minimal_cover(f))
        for _ in range(3):
            rel = random_instance(rng, attrs, f)
            assert join_of_projections(attrs, rel, schemas) == rel


def test_chase_against_instances() -> None:
    # A lossy decomposition shows up on some instance; a lossless one never does.
    rng = random.Random(12)
    attrs = "ABCD"
    seen_loss = 0
    for _ in range(150):
        f = random_fds(rng, attrs)
        schemas = [frozenset(rng.sample(attrs, rng.randint(1, 3))) for _ in range(rng.randint(1, 3))]
        if frozenset().union(*schemas) != frozenset(attrs):
            continue
        lossless = is_lossless(attrs, schemas, f)
        for _ in range(20):
            rel = random_instance(rng, attrs, f)
            joined = join_of_projections(attrs, rel, schemas)
            assert joined >= rel
            if lossless:
                assert joined == rel
            elif joined != rel:
                seen_loss += 1
    assert seen_loss > 0
