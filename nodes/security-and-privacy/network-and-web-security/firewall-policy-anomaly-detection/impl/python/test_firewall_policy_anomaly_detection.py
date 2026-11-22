# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/firewall-policy-anomaly-detection/. The authors are listed in prov/MRZ666.jsonl.

import functools
import itertools
import random

import pytest

from firewall_policy_anomaly_detection import (
    Anomaly,
    Rule,
    anomalies,
    decide,
    is_dead,
    prefix,
    relation,
    rule,
    subtract,
)

# The rules only use documentation addresses (RFC 5737 and RFC 3849). The
# code reads rule lists and never touches a network.

# A small universe: protocol 0..1 and four other fields 0..3, 512 packets.
SIZES = [2, 4, 4, 4, 4]
PACKETS = list(itertools.product(*[range(s) for s in SIZES]))
ACTIONS = ["allow", "deny"]


@functools.lru_cache(maxsize=None)
def packet_set(box) -> int:
    """The packets of a box as a bit mask over PACKETS."""
    mask = 0
    for i, p in enumerate(PACKETS):
        if all(lo <= v <= hi for (lo, hi), v in zip(box, p)):
            mask |= 1 << i
    return mask


def random_box(rng: random.Random):
    out = []
    for s in SIZES:
        a, b = sorted((rng.randrange(s), rng.randrange(s)))
        if rng.random() < 0.3:
            a, b = 0, s - 1
        out.append((a, b))
    return tuple(out)


def random_policy(rng: random.Random, m: int) -> list:
    return [Rule(random_box(rng), rng.choice(ACTIONS)) for _ in range(m)]


def oracle_anomalies(rules: list) -> list:
    """The same classes, decided on explicit packet sets."""
    sets = [packet_set(r.box) for r in rules]
    out = []
    for x, y in itertools.combinations(range(len(rules)), 2):
        sx, sy = sets[x], sets[y]
        same = rules[x].action == rules[y].action
        if sx & sy == 0:
            continue
        if sy & ~sx == 0:
            out.append(Anomaly("redundancy-later" if same else "shadowing", x + 1, y + 1, y + 1 if same else None))
        elif sx & ~sy == 0:
            if not same:
                out.append(Anomaly("generalization", x + 1, y + 1, None))
            elif not any(sets[z] & sx and rules[z].action != rules[x].action for z in range(x + 1, y)):
                out.append(Anomaly("redundancy-earlier", x + 1, y + 1, x + 1))
        elif not same:
            out.append(Anomaly("correlation", x + 1, y + 1, None))
    return out


def decisions(rules: list) -> list:
    return [decide(rules, p) for p in PACKETS]


def test_relation_against_sets() -> None:
    rng = random.Random(2004)
    for _ in range(1500):
        a, b = random_box(rng), random_box(rng)
        sa, sb = packet_set(a), packet_set(b)
        if sa & sb == 0:
            expected = "disjoint"
        elif sa == sb:
            expected = "equal"
        elif sa & ~sb == 0:
            expected = "subset"
        elif sb & ~sa == 0:
            expected = "superset"
        else:
            expected = "correlated"
        assert relation(a, b) == expected


def test_anomalies_against_oracle() -> None:
    rng = random.Random(7)
    found = set()
    for _ in range(300):
        rules = random_policy(rng, rng.randint(1, 8))
        got = anomalies(rules)
        assert sorted(got) == sorted(oracle_anomalies(rules))
        found |= {a.kind for a in got}
    assert found == {"shadowing", "redundancy-later", "generalization", "redundancy-earlier", "correlation"}


def test_meaning_of_the_classes() -> None:
    """A shadowed or later redundant rule never decides a packet, and removing
    a redundant rule leaves every decision as it was."""
    rng = random.Random(11)
    checked = 0
    for _ in range(160):
        rules = random_policy(rng, rng.randint(2, 7))
        before = decisions(rules)
        for a in anomalies(rules):
            if a.kind in ("shadowing", "redundancy-later"):
                assert is_dead(rules, a.y)
            if a.removable is not None:
                rest = rules[: a.removable - 1] + rules[a.removable :]
                assert decisions(rest) == before
                checked += 1
    assert checked > 50


def test_published_redundancy_condition_is_not_enough() -> None:
    """R2 lies inside R1 with another action. It is shadowed by R1, not in a
    generalization or correlation with it, but removing R1 still changes the
    decision of R2's packets. The check of line L9 sees R2 and keeps R1."""
    r1 = Rule(((0, 1), (0, 1), (0, 3), (0, 3), (0, 3)), "allow")
    r2 = Rule(((0, 1), (0, 0), (0, 3), (0, 3), (0, 3)), "deny")
    r3 = Rule(((0, 1), (0, 3), (0, 3), (0, 3), (0, 3)), "allow")
    rules = [r1, r2, r3]
    kinds = {(a.kind, a.x, a.y) for a in anomalies(rules)}
    assert ("shadowing", 1, 2) in kinds
    assert ("redundancy-earlier", 1, 3) not in kinds
    assert decisions([r2, r3]) != decisions(rules)


def test_union_shadowing_needs_more_than_pairs() -> None:
    r1 = Rule(((0, 1), (0, 1), (0, 3), (0, 3), (0, 3)), "deny")
    r2 = Rule(((0, 1), (2, 3), (0, 3), (0, 3), (0, 3)), "deny")
    r3 = Rule(((0, 1), (0, 3), (0, 3), (0, 0), (0, 3)), "allow")
    rules = [r1, r2, r3]
    # R3 meets R1 and R2 but lies inside neither, so the pairs only show correlation.
    assert {a.kind for a in anomalies(rules)} == {"correlation"}
    assert is_dead(rules, 3)
    assert not is_dead(rules, 2)


def test_is_dead_and_subtract_against_sets() -> None:
    rng = random.Random(3)
    for _ in range(300):
        a, b = random_box(rng), random_box(rng)
        pieces = subtract(a, b)
        masks = [packet_set(p) for p in pieces]
        union = 0
        for mk in masks:
            assert mk & union == 0  # the pieces are disjoint
            union |= mk
        assert union == packet_set(a) & ~packet_set(b)
    for _ in range(120):
        rules = random_policy(rng, rng.randint(1, 7))
        for y in range(1, len(rules) + 1):
            covered = 0
            for r in rules[: y - 1]:
                covered |= packet_set(r.box)
            assert is_dead(rules, y) == (packet_set(rules[y - 1].box) & ~covered == 0)


PAGE_POLICY = [
    rule("tcp", "198.51.100.0/25", "any", "203.0.113.10/32", "80", "allow"),
    rule("tcp", "198.51.100.0/24", "any", "203.0.113.10/32", "80", "deny"),
    rule("tcp", "198.51.100.200/32", "any", "203.0.113.10/32", "80", "allow"),
    rule("tcp", "198.51.100.128/26", "any", "203.0.113.0/24", "any", "allow"),
    rule("udp", "192.0.2.53/32", "53", "203.0.113.0/24", "any", "allow"),
    rule("udp", "192.0.2.0/24", "53", "203.0.113.0/24", "any", "allow"),
    rule("udp", "192.0.2.10/32", "53", "203.0.113.5/32", "53", "allow"),
]


def test_page_example() -> None:
    got = [(a.kind, a.x, a.y, a.removable) for a in anomalies(PAGE_POLICY)]
    assert got == [
        ("generalization", 1, 2, None),
        ("shadowing", 2, 3, None),
        ("correlation", 2, 4, None),
        ("redundancy-earlier", 5, 6, 5),
        ("redundancy-later", 6, 7, 7),
    ]
    assert is_dead(PAGE_POLICY, 3)
    assert not is_dead(PAGE_POLICY, 4)
    src, dst = prefix("198.51.100.150/32")[0], prefix("203.0.113.10/32")[0]
    assert decide(PAGE_POLICY, (6, src, 40000, dst, 80)) == "deny"  # R2 takes it from R4
    assert decide(PAGE_POLICY, (6, src, 40000, dst + 1, 80)) == "allow"  # R4
    assert prefix("2001:db8::/32") == (0x20010DB8 << 96, (0x20010DB8 << 96) + (1 << 96) - 1)


def test_bad_rules() -> None:
    with pytest.raises(ValueError):
        prefix("192.0.2.1/24")  # host bits set
    with pytest.raises(ValueError):
        relation(((0, 1),), ((0, 1), (0, 1)))
