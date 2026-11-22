# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/control-flow-integrity/. The authors are listed in prov/EYC3KG.jsonl.

import random
from collections import deque

import pytest

from control_flow_integrity import CFILabels, CFIViolation, run_transfers

EXAMPLE = {"s1": {"f", "g"}, "s2": {"g", "h"}, "s3": {"k"}}


def bipartite(allowed: dict) -> dict:
    adj: dict = {}
    for s, ts in allowed.items():
        adj.setdefault(("site", s), set())
        for t in ts:
            adj[("site", s)].add(("target", t))
            adj.setdefault(("target", t), set()).add(("site", s))
    return adj


def reach(adj: dict, start) -> set:
    seen = {start}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


def oracle_components(allowed: dict) -> dict:
    """Map each site to the set of targets in its connected component, by BFS."""
    adj = bipartite(allowed)
    return {
        s: frozenset(name for kind, name in reach(adj, ("site", s)) if kind == "target")
        for s in allowed
    }


def oracle_component_count(allowed: dict) -> int:
    adj = bipartite(allowed)
    seen: set = set()
    count = 0
    for u in adj:
        if u not in seen:
            count += 1
            seen |= reach(adj, u)
    return count


def random_graph(rng: random.Random) -> dict:
    n_sites = rng.randint(1, 5)
    n_targets = rng.randint(1, 6)
    targets = [f"t{j}" for j in range(n_targets)]
    return {f"s{i}": set(rng.sample(targets, rng.randint(0, min(3, n_targets)))) for i in range(n_sites)}


def test_example_of_the_page() -> None:
    labels = CFILabels(EXAMPLE)
    trace = [("s1", "g"), ("s2", "h"), ("s1", "h"), ("s3", "f"), ("s3", "k")]
    assert run_transfers(labels, trace) == (["g", "h", "h"], 3)
    assert labels.effective_targets("s1") == frozenset({"f", "g", "h"})
    assert labels.effective_targets("s3") == frozenset({"k"})
    assert labels.number_of_labels() == 2


def test_no_false_alarm_on_allowed_edges() -> None:
    labels = CFILabels(EXAMPLE)
    for s, ts in EXAMPLE.items():
        for t in ts:
            assert labels.check(s, t) == t


def test_unknown_site_or_target_faults() -> None:
    labels = CFILabels(EXAMPLE)
    with pytest.raises(CFIViolation):
        labels.check("s9", "f")
    with pytest.raises(CFIViolation):
        labels.check("s1", "data")


def test_site_with_no_targets_always_faults() -> None:
    labels = CFILabels({"s1": set(), "s2": {"f"}})
    with pytest.raises(CFIViolation):
        labels.check("s1", "f")
    assert labels.effective_targets("s1") == frozenset()


def test_precise_when_sets_are_disjoint_or_equal() -> None:
    allowed = {"a": {"f", "g"}, "b": {"f", "g"}, "c": {"h"}, "d": {"k", "m"}}
    labels = CFILabels(allowed)
    for s, ts in allowed.items():
        assert labels.effective_targets(s) == frozenset(ts)
    assert labels.number_of_labels() == 3


def test_random_graphs_against_bfs_oracle() -> None:
    rng = random.Random(4011)
    for _ in range(700):
        allowed = random_graph(rng)
        labels = CFILabels(allowed)
        comps = oracle_components(allowed)
        all_targets = {t for ts in allowed.values() for t in ts} | {"t_none"}
        for s in allowed:
            assert set(allowed[s]) <= comps[s]
            assert labels.effective_targets(s) == comps[s]
            for t in all_targets:
                accepted = True
                try:
                    labels.check(s, t)
                except CFIViolation:
                    accepted = False
                assert accepted == (t in comps[s])


def test_label_count_equals_components() -> None:
    rng = random.Random(77)
    for _ in range(500):
        allowed = random_graph(rng)
        labels = CFILabels(allowed)
        assert labels.number_of_labels() == oracle_component_count(allowed)


def test_random_transfer_sequences() -> None:
    rng = random.Random(1305)
    for _ in range(600):
        allowed = random_graph(rng)
        labels = CFILabels(allowed)
        comps = oracle_components(allowed)
        sites = list(allowed)
        targets = sorted({t for ts in allowed.values() for t in ts} | {"x"})
        trace = [(rng.choice(sites), rng.choice(targets)) for _ in range(rng.randint(0, 8))]
        expected_reached = []
        expected_index = None
        for i, (s, t) in enumerate(trace):
            if t in comps[s]:
                expected_reached.append(t)
            else:
                expected_index = i
                break
        assert run_transfers(labels, trace) == (expected_reached, expected_index)
