# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invitation-algorithm/. The authors are listed in prov/2ZVXPK.jsonl.

import random

from invitation_algorithm import Invitation, groups, safety_violations


def run(n, events, horizon, seed, slow=0.0):
    sim = Invitation(n, seed, slow)
    bad: list[str] = []

    def check(s):
        bad.extend(safety_violations(s))

    sim.run(events, horizon, check)
    return sim, bad


def one_group(sim) -> bool:
    g = groups(sim)
    return len(g) == 1 and all(isinstance(k[0], int) for k in g)


def test_page_example() -> None:
    sim = Invitation(6, 0)
    done: list[bool] = []
    sim.run([], 400, lambda s: done.append(len(groups(s)) == 1))
    assert done.index(True) == 29
    assert sim.merges == 1
    assert [sim.counts[k] for k in ("INVITE", "ACCEPT", "READY")] == [5, 5, 5]
    assert groups(sim) == {(2, 5): [0, 1, 2, 3, 4, 5]}


def test_singletons_merge() -> None:
    for n in range(1, 8):
        for seed in range(5):
            sim, bad = run(n, [], 400, seed)
            assert not bad
            assert one_group(sim)


def test_partition_and_heal() -> None:
    n = 6
    events = [
        (150, "partition", [0, 0, 0, 1, 1, 1]),
        (400, "partition", [0] * n),
    ]
    sim, bad = run(n, events, 1000, seed=3)
    assert not bad and one_group(sim)


def test_groups_inside_parts() -> None:
    # during a partition there is one group in each part, not one leader overall
    n = 6
    sim, bad = run(n, [(0, "partition", [0, 1, 0, 1, 0, 1])], 500, seed=1)
    assert not bad
    g = groups(sim)
    assert sorted(sorted(v) for v in g.values()) == [[0, 2, 4], [1, 3, 5]]


def test_seeded_crash_patterns() -> None:
    rng = random.Random(77)
    for trial in range(40):
        n = rng.randrange(2, 7)
        events = []
        t = 0
        for _ in range(rng.randrange(1, 5)):
            t += rng.randrange(10, 80)
            kind = rng.choice(["crash", "recover", "partition"])
            if kind == "partition":
                events.append((t, kind, [rng.randrange(2) for _ in range(n)]))
            else:
                events.append((t, kind, rng.randrange(n)))
        t += 10
        events.append((t, "partition", [0] * n))
        events.append((t, "recover", 0))
        sim, bad = run(n, events, t + 600, seed=trial)
        assert not bad, bad[:3]
        assert one_group(sim), groups(sim)


def test_safety_with_slow_messages() -> None:
    # timeouts fire wrongly, groups split and merge, the assertion still holds
    rng = random.Random(9)
    for trial in range(30):
        n = rng.randrange(2, 7)
        events = [(rng.randrange(200), "crash", rng.randrange(n)), (300, "recover", 0)]
        sim, bad = run(n, events, 500, seed=trial, slow=0.2)
        assert not bad, bad[:3]
