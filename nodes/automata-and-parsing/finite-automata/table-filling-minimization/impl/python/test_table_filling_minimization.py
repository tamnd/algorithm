# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/table-filling-minimization/. The authors are listed in prov/ZY1X60.jsonl.

import itertools
import random

from table_filling_minimization import table_filling_minimization


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def run(delta, q, w):
    for a in w:
        q = delta[(q, a)]
    return q


def run_table(table, w):
    s = 0
    for a in w:
        s = table[s][a]
    return s


def reachable(alphabet, delta, start):
    seen, stack = {start}, [start]
    while stack:
        q = stack.pop()
        for a in alphabet:
            t = delta[(q, a)]
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def brute_classes(alphabet, delta, start, accepting):
    """Group the reachable states by their behavior on all words of length <= n - 2.

    Two states of an n-state DFA that differ on some word differ on a word of
    length at most n - 2, so this is the exact equivalence of states.
    """
    reach = reachable(alphabet, delta, start)
    tests = list(words(alphabet, max(len(reach) - 2, 0)))
    groups = {}
    for q in reach:
        sig = tuple(run(delta, q, z) in accepting for z in tests)
        groups.setdefault(sig, set()).add(q)
    return sorted(sorted(g, key=repr) for g in groups.values())


def brute_index(alphabet, delta, start, accepting, n):
    """Number of Myhill-Nerode classes, from strings and suffixes of length <= n."""
    tests = list(words(alphabet, n))
    return len({tuple(run(delta, start, x + z) in accepting for z in tests) for x in words(alphabet, n)})


# The example of the page: "ends in ab" with copies and one unreachable state.
EXAMPLE = {
    (0, "a"): 1, (0, "b"): 3,
    (1, "a"): 4, (1, "b"): 2,
    (2, "a"): 4, (2, "b"): 3,
    (3, "a"): 1, (3, "b"): 0,
    (4, "a"): 1, (4, "b"): 5,
    (5, "a"): 1, (5, "b"): 0,
    (6, "a"): 6, (6, "b"): 2,
}


def test_example_from_the_page():
    blocks, table, final = table_filling_minimization("ab", EXAMPLE, 0, {2, 5})
    assert blocks == [[0, 3], [1, 4], [2, 5]]
    assert table == [{"a": 1, "b": 0}, {"a": 1, "b": 2}, {"a": 1, "b": 0}]
    assert final == {2}
    for w in words("ab", 8):
        assert (run_table(table, w) in final) == w.endswith("ab")


def test_edge_cases():
    # empty language and Sigma*, with extra copies of the single class
    d = {(q, a): (q + 1) % 4 for q in range(4) for a in "ab"}
    assert table_filling_minimization("ab", d, 0, set()) == ([[0, 1, 2, 3]], [{"a": 0, "b": 0}], set())
    assert table_filling_minimization("ab", d, 0, {0, 1, 2, 3}) == ([[0, 1, 2, 3]], [{"a": 0, "b": 0}], {0})
    # a one-state DFA
    assert table_filling_minimization("a", {(7, "a"): 7}, 7, {7}) == ([[7]], [{"a": 0}], {0})
    # a dead state is kept, since the output is complete
    d = {(0, "a"): 1, (0, "b"): 2, (1, "a"): 2, (1, "b"): 2, (2, "a"): 2, (2, "b"): 2}
    blocks, table, final = table_filling_minimization("ab", d, 0, {1})
    assert blocks == [[0], [1], [2]] and final == {1}
    # unreachable states are dropped even when they look equivalent
    d = {(0, "a"): 0, (1, "a"): 0, (2, "a"): 2}
    assert table_filling_minimization("a", d, 0, {0, 2}) == ([[0]], [{"a": 0}], {0})
    # a minimal DFA stays the same: counting modulo 5
    d = {(q, "a"): (q + 1) % 5 for q in range(5)}
    blocks, _, _ = table_filling_minimization("a", d, 0, {0})
    assert blocks == [[0], [1], [2], [3], [4]]
    # the distinguishing word can have length n - 2
    n = 9
    d = {(q, "a"): min(q + 1, n - 1) for q in range(n)}
    blocks, _, _ = table_filling_minimization("a", d, 0, {n - 1})
    assert len(blocks) == n


def random_dfa(rng, n, alphabet):
    delta = {(q, a): rng.randrange(n) for q in range(n) for a in alphabet}
    p = rng.choice([0.0, 0.3, 0.5, 1.0])
    return delta, {q for q in range(n) if rng.random() < p}


def test_random_against_brute_force():
    rng = random.Random(20261106)
    for trial in range(700):
        alphabet = "ab" if trial % 4 else "abc"
        copies = trial % 5 == 0 and alphabet == "ab"
        n = rng.randint(1, 4 if copies else (8 if alphabet == "ab" else 6))
        delta, acc = random_dfa(rng, n, alphabet)
        if copies:  # make copies of the states, so that many merge
            delta = {(q + s * n, a): t + rng.randrange(2) * n for (q, a), t in delta.items() for s in range(2)}
            acc = acc | {q + n for q in acc}
        blocks, table, final = table_filling_minimization(alphabet, delta, 0, acc)
        assert sorted(sorted(b, key=repr) for b in blocks) == brute_classes(alphabet, delta, 0, acc)
        assert 0 in blocks[0]
        for b in blocks:
            for q in b:
                for a in alphabet:
                    assert delta[(q, a)] in blocks[table[blocks.index(b)][a]]
        assert final == {i for i, b in enumerate(blocks) if b[0] in acc}
        for w in words(alphabet, 6 if alphabet == "ab" else 4):
            assert (run_table(table, w) in final) == (run(delta, 0, w) in acc)
        if trial % 10 == 0 and alphabet == "ab":
            assert len(blocks) == brute_index(alphabet, delta, 0, acc, 7)
