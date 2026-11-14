# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compiled-code-logic-simulation/. The authors are listed in prov/6EDHZJ.jsonl.

import random

import pytest

from compiled_code_logic_simulation import CombinationalLoop, compile_circuit, levelize, simulate
from logicnet import Circuit, all_vectors, random_circuit

# The page example: y = ab + a'c.
HAZARD = Circuit(
    ["a", "b", "c"],
    [("y", "OR", ["p", "q"]), ("q", "AND", ["na", "c"]), ("p", "AND", ["a", "b"]), ("na", "NOT", ["a"])],
    ["y"],
)


def one_vector(c, vec):
    full = c.direct_eval(vec)
    return {o: full[o] for o in c.outputs}


@pytest.mark.parametrize("seed", range(10))
def test_bit_parallel_equals_one_vector_evaluation(seed):
    rng = random.Random(seed)
    c = random_circuit(rng, rng.randint(1, 10), rng.randint(1, 60), n_outputs=rng.randint(1, 4))
    vectors = list(all_vectors(c.inputs))
    rng.shuffle(vectors)
    for width in (64, 7, 1):
        got = simulate(c, vectors, width)
        assert got == [one_vector(c, v) for v in vectors]


@pytest.mark.parametrize("seed", range(10))
def test_levels_respect_every_gate(seed):
    rng = random.Random(50 + seed)
    c = random_circuit(rng, rng.randint(1, 8), rng.randint(1, 80))
    rng.shuffle(c.gates)
    c = Circuit(c.inputs, c.gates, c.outputs)
    order, level = levelize(c)
    assert sorted(order) == list(range(len(c.gates)))
    pos = {c.gates[g][0]: k for k, g in enumerate(order)}
    for out, op, ins in c.gates:
        assert level[out] == 1 + max(level[n] for n in ins)
        assert all(n in c.inputs or pos[n] < pos[out] for n in ins)
    for k in range(1, len(order)):
        assert level[c.gates[order[k - 1]][0]] <= level[c.gates[order[k]][0]]


def test_one_statement_per_gate():
    rng = random.Random(7)
    c = random_circuit(rng, 5, 30)
    src, _ = compile_circuit(c)
    body = src.splitlines()[1:]
    assert len(body) == len(c.inputs) + len(c.gates) + 1
    assert not any(w in src for w in ("if ", "for ", "while "))


def test_loop_is_rejected():
    latch = Circuit(["s", "r"], [("q", "NOR", ["r", "qn"]), ("qn", "NOR", ["s", "q"])], ["q"])
    with pytest.raises(CombinationalLoop):
        compile_circuit(latch)


def test_page_example():
    src, run = compile_circuit(HAZARD, width=8)
    assert src.splitlines()[4:8] == ["    v5 = v0 & v1", "    v6 = v0 ^ M", "    v4 = v6 & v2", "    v3 = v5 | v4"]
    a, b, c = 0b11110000, 0b11001100, 0b10101010
    assert run([a, b, c]) == [0b11001010]
    vectors = [{"a": (a >> j) & 1, "b": (b >> j) & 1, "c": (c >> j) & 1} for j in range(8)]
    assert simulate(HAZARD, vectors, 8) == [one_vector(HAZARD, v) for v in vectors]
