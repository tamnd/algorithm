# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/product-construction/. The authors are listed in prov/2Q2G89.jsonl.

import itertools
import random

from product_construction import product_construction

OPS = {
    "and": lambda x, y: x and y,
    "or": lambda x, y: x or y,
    "diff": lambda x, y: x and not y,
    "xor": lambda x, y: x != y,
}


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def run(delta, start, w):
    q = start
    for a in w:
        q = delta[(q, a)]
    return q


def run_table(table, w):
    s = 0
    for a in w:
        s = table[s][a]
    return s


def min_size(table, final, alphabet):
    """Number of Myhill-Nerode classes of the product DFA, by Moore refinement."""
    cls = [int(i in final) for i in range(len(table))]
    while True:
        sig = [(cls[i],) + tuple(cls[table[i][a]] for a in alphabet) for i in range(len(table))]
        ids = {}
        new = [ids.setdefault(x, len(ids)) for x in sig]
        if len(ids) == len(set(cls)):
            return len(ids)
        cls = new


EVEN_A = {(0, "a"): 1, (0, "b"): 0, (1, "a"): 0, (1, "b"): 1}
HAS_BB = {(0, "a"): 0, (0, "b"): 1, (1, "a"): 0, (1, "b"): 2, (2, "a"): 2, (2, "b"): 2}


def test_example_from_the_page():
    pairs, table, final = product_construction("ab", EVEN_A, 0, {0}, HAS_BB, 0, {2}, OPS["and"])
    assert pairs == [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
    rows = [(pairs[table[i]["a"]], pairs[table[i]["b"]]) for i in range(6)]
    assert rows == [((1, 0), (0, 1)), ((0, 0), (1, 1)), ((1, 0), (0, 2)),
                    ((0, 0), (1, 2)), ((1, 2), (0, 2)), ((0, 2), (1, 2))]
    assert {pairs[i] for i in final} == {(0, 2)}
    sizes = {}
    for name, op in OPS.items():
        _, table, final = product_construction("ab", EVEN_A, 0, {0}, HAS_BB, 0, {2}, op)
        sizes[name] = min_size(table, final, "ab")
        for w in words("ab", 8):
            x, y = w.count("a") % 2 == 0, "bb" in w
            assert (run_table(table, w) in final) == op(x, y)
    assert sizes == {"and": 6, "or": 5, "diff": 5, "xor": 6}


def test_counting_needs_m_times_n_states():
    for m in range(1, 6):
        for n in range(1, 6):
            da = {(i, "a"): (i + 1) % m for i in range(m)} | {(i, "b"): i for i in range(m)}
            db = {(j, "b"): (j + 1) % n for j in range(n)} | {(j, "a"): j for j in range(n)}
            pairs, table, final = product_construction("ab", da, 0, {0}, db, 0, {0}, OPS["and"])
            assert len(pairs) == m * n
            assert min_size(table, final, "ab") == m * n


def test_edge_cases():
    empty = {(0, "a"): 0, (0, "b"): 0}
    for name, op in OPS.items():
        # empty language against Sigma*, both one-state DFAs
        pairs, table, final = product_construction("ab", empty, 0, set(), empty, 0, {0}, op)
        assert len(pairs) == 1
        assert (0 in final) == op(False, True)
    # unreachable and dead states in the inputs are not copied
    d1 = {(0, "a"): 1, (0, "b"): 0, (1, "a"): 1, (1, "b"): 1, (2, "a"): 0, (2, "b"): 2}
    pairs, table, final = product_construction("ab", d1, 0, {0, 2}, EVEN_A, 0, {0}, OPS["and"])
    assert all(p != 2 for p, _ in pairs)
    # string states and a single-letter alphabet
    da = {("x", "a"): "y", ("y", "a"): "x"}
    db = {("u", "a"): "v", ("v", "a"): "w", ("w", "a"): "u"}
    pairs, table, final = product_construction("a", da, "x", {"x"}, db, "u", {"u"}, OPS["and"])
    assert len(pairs) == 6
    assert [k for k in range(13) if run_table(table, "a" * k) in final] == [0, 6, 12]


def random_dfa(rng, n, alphabet):
    delta = {(q, a): rng.randrange(n) for q in range(n) for a in alphabet}
    final = {q for q in range(n) if rng.random() < rng.choice([0.0, 0.4, 1.0])}
    return delta, final


def test_random_against_brute_force():
    rng = random.Random(20261106)
    for trial in range(800):
        alphabet = "ab" if trial % 4 else "abc"
        d1, f1 = random_dfa(rng, rng.randint(1, 6), alphabet)
        d2, f2 = random_dfa(rng, rng.randint(1, 6), alphabet)
        name = rng.choice(sorted(OPS))
        pairs, table, final = product_construction(alphabet, d1, 0, f1, d2, 0, f2, OPS[name])
        assert len(pairs) == len(set(pairs)) <= 36
        for w in words(alphabet, 6 if alphabet == "ab" else 4):
            expected = OPS[name](run(d1, 0, w) in f1, run(d2, 0, w) in f2)
            got = run_table(table, w)
            assert pairs[got] == (run(d1, 0, w), run(d2, 0, w))
            assert (got in final) == expected
