# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-simulation/. The authors are listed in prov/9Z1Y7X.jsonl.
"""Ternary simulation with the values 0, 1 and X, and Eichelberger's two phases.

Every gate output is a state variable, and the gates may form loops. The
delay model is arbitrary: each gate and each wire may have any finite
delay, and ternary simulation gives results that hold for all of them.
F(u, s) evaluates every gate once with Kleene's tables, with the primary
inputs at u and the gate outputs at s.

Phase A starts from a stable state s0 under the old inputs a, with every
input that changes set to X, and iterates F upwards to a fixed point.
Phase B then sets the new inputs b and iterates F downwards to a fixed point.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from logicnet import X, Circuit, eval3

Vec = Dict[str, int]


def lub(u: int, v: int) -> int:
    """Least upper bound in the information order: equal values stay, different ones give X."""
    return u if u == v else X


def leq(u: Vec, v: Vec) -> bool:
    """u is below v in the information order: v agrees with u wherever v is not X."""
    return all(v[k] == X or v[k] == u[k] for k in v)


def step(c: Circuit, inputs: Vec, state: Vec) -> Vec:
    """F(inputs, state): every gate evaluated once on the present values."""
    val = dict(state)
    val.update(inputs)
    return {out: eval3(op, [val[n] for n in ins]) for out, op, ins in c.gates}


def settle(c: Circuit, inputs: Vec, state: Vec) -> Tuple[Vec, int]:
    """Iterate F(inputs, .) from state until it stops changing. Returns the fixed point and the step count."""
    s = dict(state)
    steps = 0
    while True:
        nxt = step(c, inputs, s)
        if nxt == s:
            return s, steps
        s = nxt
        steps += 1
        if steps > 3 * len(c.gates) + 3:
            raise RuntimeError("no fixed point; the start state was not monotone for this input")


def evaluate(c: Circuit, inputs: Vec) -> Vec:
    """Ternary value of every gate output of a loop-free circuit, from the all-X state."""
    s, _ = settle(c, inputs, {g[0]: X for g in c.gates})
    return s


def eichelberger(c: Circuit, a: Vec, b: Vec, s0: Vec) -> Tuple[Vec, Vec, int, int]:
    """Phases A and B for the input change from a to b. s0 must be stable under a.

    Returns (sA, tB, steps of phase A, steps of phase B).
    """
    a_hat = {n: lub(a[n], b[n]) for n in c.inputs}  # @line L1
    s = dict(s0)  # @line L2
    steps_a = 0
    while True:  # @line L3
        nxt = step(c, a_hat, s)  # @line L4
        done = nxt == s  # @line L5
        s = nxt
        if done:  # @line L6
            break
        steps_a += 1
    t = dict(s)  # @line L7
    steps_b = 0
    while True:  # @line L8
        nxt = step(c, b, t)  # @line L9
        done = nxt == t
        t = nxt
        if done:  # @line L10
            break
        steps_b += 1
    return s, t, steps_a, steps_b  # @line L11


def report(s0: Vec, s_a: Vec, t_b: Vec) -> Dict[str, List[str]]:
    """Read the result of the two phases.

    static_hazard: the net has the same binary value before and after, but X after phase A.
    undetermined: X after phase B, so the final value depends on the delays (a critical race or an oscillation).
    changes: the net goes from one binary value to the other; ternary simulation cannot say if it does so cleanly.
    """
    out: Dict[str, List[str]] = {"static_hazard": [], "undetermined": [], "changes": []}
    for n in s0:
        if t_b[n] == X:
            out["undetermined"].append(n)
        elif t_b[n] == s0[n] and s_a[n] == X:
            out["static_hazard"].append(n)
        elif t_b[n] != s0[n]:
            out["changes"].append(n)
    return out
