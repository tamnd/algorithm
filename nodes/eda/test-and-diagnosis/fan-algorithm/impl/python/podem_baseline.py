# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-algorithm/. The authors are listed in prov/DJVVW8.jsonl.
"""Plain PODEM (Goel 1981), written only as the baseline for the backtrack counts of FAN.

Decisions are on primary inputs. The objective is to activate the fault, else
to set an X input of the first D-frontier gate with an X-path to its
non-controlling value. The backtrace takes the first input with an X. These
are the same choices that the FAN code makes when it has a free choice, so
the two searches differ only by the FAN rules.
"""

from __future__ import annotations

from typing import Optional

from td2net import X, Circuit, Fault, controlling, inversion


def is_effect(g: int, b: int) -> bool:
    """True for D or D': both values known and different."""
    return g != X and b != X and g != b


def d_frontier(c: Circuit, good: list[int], bad: list[int]) -> list[int]:
    """Gate lines with an X that have an input with D or D'."""
    return [
        k
        for k in range(c.n_lines)
        if c.kind[k] == "gate"
        and X in (good[k], bad[k])
        and any(is_effect(good[j], bad[j]) for j in c.fanin[k])
    ]


def x_paths(c: Circuit, good: list[int], bad: list[int]) -> list[bool]:
    """For each line with an X: True if a path of lines with an X leads to a primary output."""
    is_po = set(c.po)
    xp = [False] * c.n_lines
    for k in range(c.n_lines - 1, -1, -1):
        if X in (good[k], bad[k]):
            xp[k] = k in is_po or any(xp[w] for w in c.fanout[k])
    return xp


def podem(c: Circuit, fault: Fault, stats: Optional[dict[str, int]] = None) -> Optional[tuple[int, ...]]:
    """Return a test with X for free inputs, or None if the fault is redundant."""
    site, s = fault
    pi_pos = {line: k for k, line in enumerate(c.pi)}
    assign = [X] * len(c.pi)
    stack: list[list[int]] = []
    steps = backtracks = 0
    while True:
        steps += 1
        good = c.simulate(assign)
        bad = c.simulate(assign, fault)
        if any(is_effect(good[o], bad[o]) for o in c.po):
            if stats is not None:
                stats.update(steps=steps, backtracks=backtracks)
            return tuple(assign)
        xp = x_paths(c, good, bad)
        front = [g for g in d_frontier(c, good, bad) if xp[g]]
        possible = good[site] != s and (good[site] == X or bool(front))
        if possible:
            if good[site] == X:
                k, v = site, 1 - s
            else:
                gate = front[0]
                k = next(j for j in c.fanin[gate] if X in (good[j], bad[j]))
                cv = controlling(c.op[gate])
                v = 0 if cv is None else 1 - cv
            while c.kind[k] != "pi":
                v ^= inversion(c.op[k])
                k = next(j for j in c.fanin[k] if X in (good[j], bad[j]))
            assign[pi_pos[k]] = v
            stack.append([pi_pos[k], v, 0])
        else:
            while stack and stack[-1][2]:
                assign[stack.pop()[0]] = X
            if not stack:
                if stats is not None:
                    stats.update(steps=steps, backtracks=backtracks)
                return None
            top = stack[-1]
            top[1], top[2] = 1 - top[1], 1
            assign[top[0]] = top[1]
            backtracks += 1
