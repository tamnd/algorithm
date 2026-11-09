# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-depth-first-search/. The authors are listed in prov/CRQF4Q.jsonl.

import random

from nested_depth_first_search import nested_depth_first_search

EXAMPLE = {0: [1, 3], 1: [2], 2: [2], 3: [4], 4: [5], 5: [3]}


def scc_nonempty(init, succ, accepting) -> bool:
    """Oracle: an accepting state that is reachable and lies in a nontrivial SCC (Kosaraju)."""
    reach, todo = set(init), list(init)
    while todo:
        for t in succ.get(todo.pop(), []):
            if t not in reach:
                reach.add(t)
                todo.append(t)
    order, seen = [], set()
    for r in reach:
        if r in seen:
            continue
        seen.add(r)
        stack = [(r, iter(succ.get(r, [])))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                order.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(succ.get(w, []))))
    pred = {v: [] for v in reach}
    for v in reach:
        for w in succ.get(v, []):
            pred[w].append(v)
    comp = {}
    for r in reversed(order):
        if r in comp:
            continue
        comp[r] = r
        todo = [r]
        while todo:
            v = todo.pop()
            for w in pred[v]:
                if w not in comp:
                    comp[w] = r
                    todo.append(w)
    size = {}
    for v in reach:
        size[comp[v]] = size.get(comp[v], 0) + 1
    return any(
        a in reach and (size[comp[a]] > 1 or a in succ.get(a, [])) for a in accepting
    )


def check_lasso(init, succ, accepting, lasso) -> None:
    stem, cycle = lasso
    path = stem + cycle
    assert path[0] in init
    assert cycle[0] in accepting
    for a, b in zip(path, path[1:] + [cycle[0]]):
        assert b in succ[a]


def test_example() -> None:
    lasso = nested_depth_first_search([0], EXAMPLE, {1, 4})
    assert lasso == ([0, 3], [4, 5, 3])
    assert nested_depth_first_search([0], EXAMPLE, {1}) is None
    assert nested_depth_first_search([0], EXAMPLE, {2}) == ([0, 1], [2])


def test_edges() -> None:
    assert nested_depth_first_search([], {}, set()) is None
    assert nested_depth_first_search([0], {0: []}, {0}) is None
    assert nested_depth_first_search([0], {0: [0]}, {0}) == ([], [0])
    assert nested_depth_first_search([0], {0: [0]}, set()) is None
    # A cycle that is not reachable does not count.
    assert nested_depth_first_search([0], {0: [], 1: [1]}, {1}) is None


def test_flags_are_kept_between_inner_searches() -> None:
    # The inner search from 1 flags 2 and 3; the cycle 4 -> 5 -> 4 is still found.
    succ = {0: [1, 4], 1: [2], 2: [3], 3: [], 4: [5], 5: [4, 2]}
    lasso = nested_depth_first_search([0], succ, {1, 5})
    check_lasso([0], succ, {1, 5}, lasso)


def test_random_against_scc() -> None:
    rng = random.Random(1992)
    found = 0
    for trial in range(1500):
        n = rng.randint(1, 9)
        succ = {v: rng.sample(range(n), rng.randint(0, min(3, n))) for v in range(n)}
        accepting = {v for v in range(n) if rng.random() < 0.3}
        init = rng.sample(range(n), rng.randint(1, min(2, n)))
        expected = scc_nonempty(init, succ, accepting)
        for early in (False, True):
            lasso = nested_depth_first_search(init, succ, accepting, early=early)
            assert (lasso is not None) == expected, (init, succ, accepting, early)
            if lasso is not None:
                check_lasso(init, succ, accepting, lasso)
        found += expected
    assert 300 < found < 1200


def test_long_chain_no_recursion_limit() -> None:
    n = 50_000
    succ = {v: [v + 1] for v in range(n)}
    succ[n] = [0]
    lasso = nested_depth_first_search([0], succ, {n})
    check_lasso([0], succ, {n}, lasso)
    early = nested_depth_first_search([0], succ, {n}, early=True)
    check_lasso([0], succ, {n}, early)
