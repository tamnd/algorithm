# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plaisted-greenbaum-transformation/. The authors are listed in prov/KVGY32.jsonl.

import itertools
import random

from plaisted_greenbaum_transformation import NEG, POS, plaisted_greenbaum, polarities


def satisfies(clauses: list[list[int]], val: list[bool]) -> bool:
    return all(any(val[a] if a > 0 else not val[-a] for a in c) for c in clauses)


def evaluate(n: int, gates: list, xs: tuple) -> list[bool]:
    val = [False, *xs]

    def lit(a: int) -> bool:
        return val[a] if a > 0 else not val[-a]

    for op, args in gates:
        if op == "and":
            val.append(all(lit(a) for a in args))
        elif op == "or":
            val.append(any(lit(a) for a in args))
        else:
            val.append(lit(args[0]) != lit(args[1]))
    return val


def tseitin_size(gates: list) -> int:
    return sum(4 if op == "xor" else len(a) + 1 for op, a in gates) + 1


def random_circuit(rng: random.Random, n: int, g: int) -> list:
    gates = []
    for i in range(g):
        op = rng.choice(["and", "or", "or", "and", "xor"])
        k = 2 if op == "xor" else rng.randint(1, 3)
        args = rng.sample(range(1, n + i + 1), min(k, n + i))
        if op == "xor" and len(args) < 2:
            op = "or"
        gates.append((op, [a if rng.random() < 0.5 else -a for a in args]))
    return gates


def test_page_examples() -> None:
    gates = [("and", [1, 2]), ("or", [4, 3])]
    assert plaisted_greenbaum(3, gates, 5) == [[-4, 1], [-4, 2], [-5, 4, 3], [5]]
    models = [b for b in itertools.product([False, True], repeat=5)
              if satisfies(plaisted_greenbaum(3, gates, 5), [False, *b])]
    assert len(models) == 6  # the circuit has 5 satisfying inputs
    neg = [("and", [1, 2]), ("or", [-4, 3])]
    assert plaisted_greenbaum(3, neg, 5) == [[4, -1, -2], [-5, -4, 3], [5]]
    pol = polarities(2, [("and", [1, 2]), ("xor", [3, 1])], 4)
    assert pol[3] == POS | NEG and pol[1] == POS | NEG and pol[2] == POS | NEG


def test_equisatisfiable_and_projection() -> None:
    rng = random.Random(1986)
    for _ in range(300):
        n, g = rng.randint(1, 5), rng.randint(1, 6)
        gates = random_circuit(rng, n, g)
        out = rng.choice([1, -1]) * (n + g)
        cnf = plaisted_greenbaum(n, gates, out)
        assert len(cnf) <= tseitin_size(gates)
        circuit_sat = False
        for xs in itertools.product([False, True], repeat=n):
            val = evaluate(n, gates, xs)
            good = val[abs(out)] == (out > 0)
            circuit_sat |= good
            if good:  # the gate values extend every satisfying input
                assert satisfies(cnf, val)
            for ys in itertools.product([False, True], repeat=g):
                if satisfies(cnf, [False, *xs, *ys]):
                    assert good  # every model projects to a satisfying input
        cnf_sat = any(satisfies(cnf, [False, *b])
                      for b in itertools.product([False, True], repeat=n + g))
        assert cnf_sat == circuit_sat
