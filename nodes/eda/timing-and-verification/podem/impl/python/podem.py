# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/podem/. The authors are listed in prov/FHMN9N.jsonl.
"""PODEM (Goel 1981): test generation for one single stuck-at fault by search over primary inputs.

The value of a line is the pair (good value, faulty value), each in {0, 1, X}.
The five values of Roth are 0 = (0, 0), 1 = (1, 1), D = (1, 0), D' = (0, 1),
and X for every pair with an X in it.
"""

from __future__ import annotations

from typing import Optional

from gatenet import X, Circuit, Fault, controlling, eval_gate, inversion


def is_effect(g: int, b: int) -> bool:
    """True for D or D': both values known and different."""
    return g != X and b != X and g != b


def d_frontier(c: Circuit, good: list[int], bad: list[int]) -> list[int]:
    """Gate lines whose value is X and that have an input with D or D'."""
    return [
        k
        for k in range(c.n_lines)
        if c.kind[k] == "gate"
        and X in (good[k], bad[k])
        and any(is_effect(good[j], bad[j]) for j in c.fanin[k])
    ]


def x_paths(c: Circuit, good: list[int], bad: list[int], is_po: list[bool]) -> list[bool]:
    """For each line with value X: True if a path of lines with value X leads from it to a primary output.

    One sweep in reverse topological order, O(L + P) time.
    """
    xp = [False] * c.n_lines
    for k in range(c.n_lines - 1, -1, -1):
        if X in (good[k], bad[k]):
            xp[k] = is_po[k] or any(xp[w] for w in c.fanout[k])
    return xp


def controllability(c: Circuit) -> tuple[list[int], list[int]]:
    """SCOAP combinational controllabilities CC0 and CC1 of every line (Goldstein 1979)."""
    cc0 = [0] * c.n_lines
    cc1 = [0] * c.n_lines
    for k in range(c.n_lines):
        op, ins = c.op[k], c.fanin[k]
        if c.kind[k] == "pi":
            cc0[k], cc1[k] = 1, 1
        elif c.kind[k] == "branch":
            cc0[k], cc1[k] = cc0[ins[0]], cc1[ins[0]]
        elif op in ("NOT", "BUF"):
            a0, a1 = cc0[ins[0]] + 1, cc1[ins[0]] + 1
            cc0[k], cc1[k] = (a1, a0) if op == "NOT" else (a0, a1)
        elif op in ("XOR", "XNOR"):
            e0, e1 = cc0[ins[0]], cc1[ins[0]]  # cost of even and odd parity so far
            for j in ins[1:]:
                e0, e1 = min(e0 + cc0[j], e1 + cc1[j]), min(e0 + cc1[j], e1 + cc0[j])
            cc0[k], cc1[k] = (e0 + 1, e1 + 1) if op == "XOR" else (e1 + 1, e0 + 1)
        else:
            cv = controlling(op)
            one = min((cc0, cc1)[cv][j] for j in ins) + 1  # one input at the controlling value
            alls = sum((cc0, cc1)[1 - cv][j] for j in ins) + 1  # all inputs non-controlling
            out_c = cv ^ inversion(op)  # output value forced by a controlling input
            if out_c == 0:
                cc0[k], cc1[k] = one, alls
            else:
                cc1[k], cc0[k] = one, alls
    return cc0, cc1


def objective(c: Circuit, good: list[int], bad: list[int], fault: Fault, is_po: list[bool]) -> tuple[int, int]:
    """The next goal (line, value): activate the fault, else advance the D-frontier."""
    site, s = fault
    if good[site] == X:  # @line L13
        return site, 1 - s
    xp = x_paths(c, good, bad, is_po)
    for gate in d_frontier(c, good, bad):  # @line L14
        if xp[gate]:
            for j in c.fanin[gate]:  # @line L15
                if X in (good[j], bad[j]):
                    cv = controlling(c.op[gate])
                    return j, 0 if cv is None else 1 - cv  # @line L16
    raise AssertionError("objective called when no test is possible")


def backtrace(
    c: Circuit, good: list[int], bad: list[int], k: int, v: int,
    cc: Optional[tuple[list[int], list[int]]] = None,
) -> tuple[int, int]:
    """Walk from an objective back to an unassigned primary input along lines with value X."""
    while c.kind[k] != "pi":  # @line L17
        op = c.op[k]
        cand = [j for j in c.fanin[k] if X in (good[j], bad[j])]  # @line L18
        u = v ^ inversion(op)  # @line L19: the value wanted at the inputs of k
        if cc is None or len(cand) == 1:
            j = cand[0]
        elif controlling(op) is not None and u == controlling(op):
            j = min(cand, key=lambda t: cc[u][t])  # one input is enough: take the easiest
        else:
            j = max(cand, key=lambda t: cc[u][t])  # all inputs are needed: take the hardest
        k, v = j, u  # @line L20
    return k, v  # @line L21


def test_possible(c: Circuit, good: list[int], bad: list[int], fault: Fault, is_po: list[bool]) -> bool:
    """False only if no completion of the current input values can detect the fault."""
    site, s = fault
    if good[site] == s:
        return False
    if good[site] == X:
        return True
    xp = x_paths(c, good, bad, is_po)
    return any(xp[g] for g in d_frontier(c, good, bad))


def podem(
    c: Circuit,
    fault: Fault,
    guided: bool = False,
    stats: Optional[dict[str, int]] = None,
) -> Optional[tuple[int, ...]]:
    """Return a test for the fault, with X for inputs that may take any value, or None.

    None means that the fault is undetectable (redundant). With guided=True the
    backtrace picks inputs by SCOAP controllability. The search visits at most
    2^(n+1) - 1 nodes for n primary inputs, and each node costs O(L + P) time.
    """
    pi_pos = {line: k for k, line in enumerate(c.pi)}
    is_po = [False] * c.n_lines
    for o in c.po:
        is_po[o] = True
    cc = controllability(c) if guided else None
    assign = [X] * len(c.pi)  # @line L1
    stack: list[list[int]] = []  # entries [input position, value, 1 if both values were tried]
    steps = backtracks = 0
    while True:  # @line L2
        steps += 1
        good = c.simulate(assign)  # @line L3
        bad = c.simulate(assign, fault)
        if any(is_effect(good[o], bad[o]) for o in c.po):  # @line L4
            if stats is not None:
                stats.update(steps=steps, backtracks=backtracks)
            return tuple(assign)
        if test_possible(c, good, bad, fault, is_po):  # @line L5
            k, v = objective(c, good, bad, fault, is_po)  # @line L6
            p, u = backtrace(c, good, bad, k, v, cc)  # @line L7
            assign[pi_pos[p]] = u  # @line L8
            stack.append([pi_pos[p], u, 0])
        else:  # @line L9
            while stack and stack[-1][2]:  # @line L10
                assign[stack.pop()[0]] = X
            if not stack:  # @line L11
                if stats is not None:
                    stats.update(steps=steps, backtracks=backtracks)
                return None
            top = stack[-1]  # @line L12
            top[1], top[2] = 1 - top[1], 1
            assign[top[0]] = top[1]
            backtracks += 1
