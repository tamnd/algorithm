# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cegar/. The authors are listed in prov/WZ22QB.jsonl.

import random

from cegar import abstract_edges, abstract_path, cegar

# States 0 .. 5, initial state 0, bad state 5. Only 0, 1 and 2 are reachable.
SUCC = {0: [1], 1: [0, 2], 2: [2], 3: [4], 4: [5], 5: [5]}


def reach(succ, init):
    seen, stack = set(init), list(init)
    while stack:
        s = stack.pop()
        for t in succ.get(s, ()):
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def test_example():
    verdict, blocks, rounds = cegar(6, SUCC, {0}, {5})
    assert verdict == "holds" and rounds == 4
    assert sorted(sorted(b) for b in blocks) == [[0], [1], [2], [3, 4], [5]]


def test_bug_found():
    succ = dict(SUCC)
    succ[2] = [2, 3]
    verdict, trace, rounds = cegar(6, succ, {0}, {5})
    assert verdict == "fails" and trace == [0, 1, 2, 3, 4, 5]


def rand_system(rng):
    n = rng.randint(2, 14)
    succ = {s: rng.sample(range(n), rng.randint(0, 2)) for s in range(n)}
    init = set(rng.sample(range(n), rng.randint(1, 2)))
    bad = set(rng.sample(range(n), rng.randint(0, 2)))
    return n, succ, init, bad


def test_random_against_explicit_search():
    rng = random.Random(2000)
    seen = {"holds": 0, "fails": 0}
    for _ in range(400):
        n, succ, init, bad = rand_system(rng)
        verdict, out, rounds = cegar(n, succ, init, bad)
        seen[verdict] += 1
        assert rounds <= n
        if reach(succ, init) & bad:
            assert verdict == "fails"
            assert out[0] in init and out[-1] in bad
            assert all(b in succ[a] for a, b in zip(out, out[1:]))
        else:
            assert verdict == "holds"
            # The final blocks partition the states and keep the bad labels exact.
            assert sorted(s for b in out for s in b) == list(range(n))
            assert all(b <= bad or not (b & bad) for b in out)
            assert abstract_path(out, abstract_edges(out, succ), init, bad) is None
    assert seen["holds"] > 50 and seen["fails"] > 50


def test_abstraction_overapproximates():
    """Each concrete path maps to an abstract path, so abstract safety implies concrete safety."""
    rng = random.Random(3)
    for _ in range(100):
        n, succ, init, bad = rand_system(rng)
        blocks = [frozenset(b) for b in ({s for s in range(n) if rng.random() < 0.5}, ) if b]
        rest = frozenset(range(n)) - (blocks[0] if blocks else frozenset())
        blocks = [b for b in blocks + [rest] if b]
        edges = abstract_edges(blocks, succ)
        where = {s: i for i, b in enumerate(blocks) for s in b}
        for s in range(n):
            for t in succ[s]:
                assert where[t] in edges[where[s]]
