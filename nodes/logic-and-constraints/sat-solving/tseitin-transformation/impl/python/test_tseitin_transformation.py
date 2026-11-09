# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tseitin-transformation/. The authors are listed in prov/69B3GH.jsonl.

import itertools
import random

from tseitin_transformation import evaluate, tseitin


def satisfies(clauses: list[list[int]], val: list[bool]) -> bool:
    return all(any(val[a] if a > 0 else not val[-a] for a in c) for c in clauses)


def random_circuit(rng: random.Random, n: int, g: int) -> list:
    gates = []
    for i in range(g):
        top = n + i
        op = rng.choice(["and", "or", "xor"])
        k = 2 if op == "xor" else rng.randint(1, 3)
        args = rng.sample(range(1, top + 1), min(k, top))
        if op == "xor" and len(args) < 2:
            op = "and"
        gates.append((op, [a if rng.random() < 0.5 else -a for a in args]))
    return gates


def test_page_example() -> None:
    gates = [("and", [1, -2]), ("and", [2, 3]), ("or", [4, 5])]
    cnf = tseitin(3, gates, 6)
    assert cnf == [[-4, 1], [-4, -2], [4, -1, 2], [-5, 2], [-5, 3], [5, -2, -3],
                   [6, -4], [6, -5], [-6, 4, 5], [6]]
    models = [b for b in itertools.product([False, True], repeat=6) if satisfies(cnf, [False, *b])]
    assert sorted(m[:3] for m in models) == [(False, True, True), (True, False, False),
                                            (True, False, True), (True, True, True)]


def test_distributive_blowup_example() -> None:
    k = 10
    gates = [("and", [2 * i + 1, 2 * i + 2]) for i in range(k)]
    gates.append(("or", [2 * k + 1 + i for i in range(k)]))
    cnf = tseitin(2 * k, gates, 3 * k + 1)
    assert len(cnf) == 4 * k + 2
    assert sum(map(len, cnf)) == 10 * k + 2


def test_unique_extension_and_size() -> None:
    rng = random.Random(1968)
    for _ in range(300):
        n, g = rng.randint(1, 5), rng.randint(1, 6)
        gates = random_circuit(rng, n, g)
        out = rng.choice([1, -1]) * (n + g)
        cnf = tseitin(n, gates, out)
        defs = cnf[:-1]
        size = sum(4 if op == "xor" else len(a) + 1 for op, a in gates) + 1
        lits = sum(12 if op == "xor" else 3 * len(a) + 1 for op, a in gates) + 1
        assert len(cnf) == size and sum(map(len, cnf)) == lits
        circuit_models = cnf_models = 0
        for xs in itertools.product([False, True], repeat=n):
            val = evaluate(n, gates, list(xs))
            exts = [ys for ys in itertools.product([False, True], repeat=g)
                    if satisfies(defs, [False, *xs, *ys])]
            assert exts == [tuple(val[n + 1:])]
            o = val[abs(out)] if out > 0 else not val[abs(out)]
            circuit_models += o
            cnf_models += sum(satisfies(cnf, [False, *xs, *ys]) for ys in exts)
        assert circuit_models == cnf_models
