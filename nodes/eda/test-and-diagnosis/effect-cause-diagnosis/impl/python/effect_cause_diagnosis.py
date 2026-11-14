# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/effect-cause-diagnosis/. The authors are listed in prov/4MRNNQ.jsonl.
"""Effect-cause diagnosis of a single stuck-at fault, with no fault dictionary.

The input is a circuit, the tests applied on the tester and the output vector
the chip gave on each test. The algorithm starts from the effects (the failing
outputs) and reasons back to the causes:

1. simulate the good circuit and find the failing outputs of every test;
2. a fault that explains the data must reach every failing output, so it sits
   in the intersection of the fan-in cones of all failing outputs;
3. it must be excited on every failing test, so its stuck value is the
   complement of the good value of its line, and that good value must be the
   same on all failing tests;
4. simulate only the surviving candidates and keep those whose response equals
   the observed response.

The result is exactly the set of single stuck-at faults whose response equals
the observed one: the set a full-response fault dictionary would return.
Cost: O(T (L + P)) for the good simulation and the cones, plus O(C T (L + P))
to verify C candidates, against O(2L T (L + P)) to simulate every fault.
"""

from __future__ import annotations

from typing import Sequence

from td3net import Circuit, Fault


def fanin_cone(circuit: Circuit, line: int) -> set[int]:
    """All lines with a path to `line`, the line included. O(L + P)."""
    seen = {line}
    stack = [line]
    while stack:
        u = stack.pop()
        for v in circuit.fanin[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def diagnose(
    circuit: Circuit,
    tests: Sequence[Sequence[int]],
    responses: Sequence[Sequence[int]],
) -> tuple[list[Fault], int]:
    """Single stuck-at faults that reproduce the observed responses, and the number simulated.

    Precondition: one response (a 0/1 vector over the primary outputs) per test.
    Returns ([], 0) when no test fails: a passing chip gives nothing to explain.
    """
    if len(tests) != len(responses):
        raise ValueError("one response per test")
    good = [circuit.simulate(t) for t in tests]  # @line L1
    failing_outputs = [
        {k for k, o in enumerate(circuit.po) if g[o] != r[k]} for g, r in zip(good, responses)
    ]
    fail = [j for j, d in enumerate(failing_outputs) if d]  # @line L2
    if not fail:
        return [], 0
    suspects = set(range(circuit.n_lines))  # @line L3
    for k in set().union(*(failing_outputs[j] for j in fail)):  # @line L4
        suspects &= fanin_cone(circuit, circuit.po[k])  # @line L5
    candidates: list[Fault] = []
    for line in sorted(suspects):  # @line L6
        values = {good[j][line] for j in fail}
        if len(values) == 1:
            candidates.append((line, 1 - values.pop()))
    kept: list[Fault] = []
    for f in candidates:  # @line L7
        if all(circuit.outputs(t, f) == tuple(r) for t, r in zip(tests, responses)):  # @line L8
            kept.append(f)
    return kept, len(candidates)  # @line L9
