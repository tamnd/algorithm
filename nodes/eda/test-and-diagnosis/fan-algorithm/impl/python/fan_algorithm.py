# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-algorithm/. The authors are listed in prov/DJVVW8.jsonl.
"""FAN (Fujiwara and Shimono 1983): test generation for one single stuck-at fault.

FAN keeps the search of PODEM, a depth-first search with forward simulation,
and adds four rules:

- decisions are made on head lines, not on primary inputs, and a head line is
  justified only after a test is found, inside its fanout-free cone;
- multiple backtrace sends all current objectives back at once and counts how
  many of them want 0 and 1 at each line;
- unique sensitization finds the gates through which every path from the
  single D-frontier gate must pass and requires their side inputs to be
  non-controlling;
- these required values prune the search as soon as one of them is
  contradicted, before the D-frontier dies.

In the original, a fanout stem that receives both 0 and 1 counts becomes a
decision of its own. Here the stem keeps the larger count and the backtrace
goes on, so every decision is on a head line (see the page).
"""

from __future__ import annotations

from typing import Optional

from td2net import X, Circuit, Fault, controlling, eval_gate, inversion


def is_effect(g: int, b: int) -> bool:
    """True for D or D': both values known and different."""
    return g != X and b != X and g != b


def bound_and_head_lines(c: Circuit, fault: Fault) -> tuple[list[bool], list[int]]:
    """Bound lines (reached from a fanout branch or from the fault site) and the decision lines.

    The decision lines are the head lines, that is the free lines with a bound
    fanout, and the fault site when it is a primary input.
    """
    site = fault[0]
    bound = [False] * c.n_lines
    for k in range(c.n_lines):  # @line L1
        bound[k] = c.kind[k] == "branch" or k == site or any(bound[j] for j in c.fanin[k])
    heads = [k for k in range(c.n_lines) if not bound[k] and any(bound[w] for w in c.fanout[k])]
    if c.kind[site] == "pi":
        heads.append(site)
    return bound, sorted(heads)


def imply(c: Circuit, fault: Fault, value: dict[int, int]) -> tuple[list[int], list[int]]:
    """Three-valued simulation of the good and the faulty circuit from the head line values."""
    site, s = fault
    good = [X] * c.n_lines
    bad = [X] * c.n_lines
    for k in range(c.n_lines):
        if k in value:
            g = b = value[k]
        elif c.kind[k] == "pi":
            g = b = X
        else:
            ins = c.fanin[k]
            g = eval_gate(c.op[k], [good[j] for j in ins])
            b = eval_gate(c.op[k], [bad[j] for j in ins])
        if k == site:
            b = s
        good[k], bad[k] = g, b
    return good, bad


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


SINK = -1  # the virtual sink that every primary output feeds


def postdominator_tree(c: Circuit) -> list[Optional[int]]:
    """Immediate post-dominator of each line on the way to the outputs.

    The value is SINK for a line whose paths to the outputs share no line,
    and None for a line with no path to an output. One sweep in reverse
    topological order; the meet of two lines walks up the tree, so the
    sweep takes O(L (L + P)) time in the worst case.
    """
    ipdom: list[Optional[int]] = [None] * c.n_lines
    depth = [0] * c.n_lines
    is_po = set(c.po)

    def meet(u: int, w: int) -> int:
        while u != w:
            if u == SINK or w == SINK:
                return SINK
            if depth[u] < depth[w]:
                u, w = w, u
            u = ipdom[u]  # type: ignore[assignment]
        return u

    for k in range(c.n_lines - 1, -1, -1):
        succ = [w for w in c.fanout[k] if ipdom[w] is not None or w in is_po]
        if k in is_po:
            succ.append(SINK)
        if not succ:
            continue
        m = succ[0]
        for w in succ[1:]:
            m = meet(m, w)
        ipdom[k] = m
        depth[k] = 1 if m == SINK else depth[m] + 1
    return ipdom


def dominators(ipdom: list[Optional[int]], g: int) -> list[int]:
    """Lines that lie on every path from line g to a primary output, g included."""
    if ipdom[g] is None:
        return []
    out = []
    d: Optional[int] = g
    while d is not None and d != SINK:
        out.append(d)
        d = ipdom[d]
    return out


def unique_sensitization(
    c: Circuit, fault: Fault, good: list[int], front: list[int], fault_cone: set[int],
    ipdom: list[Optional[int]],
) -> list[tuple[int, int]]:
    """Values that every test extending the current values must have (lines L16 to L20)."""
    site, s = fault
    if good[site] == X or len(front) != 1:  # @line L16
        return []
    req = []  # @line L17
    for d in dominators(ipdom, front[0]):  # @line L18
        cv = controlling(c.op[d]) if c.kind[d] == "gate" else None
        if cv is None:
            continue
        for j in c.fanin[d]:  # @line L19
            if j not in fault_cone:
                req.append((j, 1 - cv))
    return req  # @line L20


def multiple_backtrace(
    c: Circuit, good: list[int], bad: list[int], objectives: list[tuple[int, int]], is_head: list[bool]
) -> tuple[int, int]:
    """Send all objectives back at once with counts; return a head line and its value."""
    n = [[0] * c.n_lines, [0] * c.n_lines]  # @line L21
    for k, v in objectives:
        n[v][k] += 1
    for k in range(c.n_lines - 1, -1, -1):  # @line L22
        if is_head[k] or n[0][k] + n[1][k] == 0:
            continue
        if len(c.fanout[k]) > 1 and n[0][k] and n[1][k]:  # @line L23: conflict at a fanout stem
            n[1 if n[0][k] > n[1][k] else 0][k] = 0
        op = c.op[k]
        xins = [j for j in c.fanin[k] if X in (good[j], bad[j])]
        for v in (0, 1):  # @line L24
            if not n[v][k]:
                continue
            u = v ^ inversion(op)  # @line L25
            cv = controlling(op)
            if op in ("XOR", "XNOR"):
                parity = 0
                for j in c.fanin[k]:
                    if good[j] != X:
                        parity ^= good[j]
                n[u ^ parity][xins[0]] += n[v][k]
            elif cv is not None and u == cv:  # @line L26: one input is enough
                n[u][xins[0]] += n[v][k]
            else:  # @line L27: every input is needed
                for j in xins:
                    n[u][j] += n[v][k]
    best = max(
        (k for k in range(c.n_lines) if is_head[k] and n[0][k] + n[1][k] > 0),
        key=lambda k: (n[0][k] + n[1][k], -k),
    )  # @line L28
    return best, 1 if n[1][best] > n[0][best] else 0


def justify_tree(c: Circuit, k: int, v: int, vec: list[int], pi_pos: dict[int, int]) -> None:
    """Set primary inputs of the fanout-free cone of k so that k gets value v."""
    if c.kind[k] == "pi":
        vec[pi_pos[k]] = v
        return
    op, ins = c.op[k], c.fanin[k]
    u = v ^ inversion(op)
    if op in ("XOR", "XNOR"):
        for j in ins[:-1]:
            justify_tree(c, j, 0, vec, pi_pos)
        justify_tree(c, ins[-1], u, vec, pi_pos)
    elif controlling(op) is not None and u == controlling(op):
        justify_tree(c, ins[0], u, vec, pi_pos)
    else:
        for j in ins:
            justify_tree(c, j, u, vec, pi_pos)


def fan(c: Circuit, fault: Fault, stats: Optional[dict[str, int]] = None) -> Optional[tuple[int, ...]]:
    """Return a test with X for free inputs, or None if the fault is redundant.

    The search tree has one level per decision line, at most n levels for n
    primary inputs, and each node costs O(L + P) time. The post-dominator
    tree for unique sensitization is built once, in O(L (L + P)) time.
    """
    site, s = fault
    _, heads = bound_and_head_lines(c, fault)
    is_head = [False] * c.n_lines
    for h in heads:
        is_head[h] = True
    fault_cone = c.cone(site)
    ipdom = postdominator_tree(c)
    pi_pos = {line: k for k, line in enumerate(c.pi)}
    value: dict[int, int] = {}  # @line L2
    stack: list[list[int]] = []
    steps = backtracks = 0
    while True:  # @line L3
        steps += 1
        good, bad = imply(c, fault, value)  # @line L4
        if any(is_effect(good[o], bad[o]) for o in c.po):  # @line L5
            vec = [X] * len(c.pi)
            for h, u in value.items():  # @line L29
                justify_tree(c, h, u, vec, pi_pos)
            if stats is not None:
                stats.update(steps=steps, backtracks=backtracks)
            return tuple(vec)  # @line L30
        xp = x_paths(c, good, bad)
        front = [g for g in d_frontier(c, good, bad) if xp[g]]
        req = unique_sensitization(c, fault, good, front, fault_cone, ipdom)  # @line L6
        ok = good[site] != s and (good[site] == X or bool(front))  # @line L7
        ok = ok and all(good[k] in (X, v) for k, v in req)
        if ok:
            objs = [(site, 1 - s)] if good[site] == X else []  # @line L8
            objs += [(k, v) for k, v in req if good[k] == X]
            if not objs:  # @line L9
                gate = front[0]
                j = next(j for j in c.fanin[gate] if X in (good[j], bad[j]))
                cv = controlling(c.op[gate])
                objs = [(j, 0 if cv is None else 1 - cv)]
            h, u = multiple_backtrace(c, good, bad, objs, is_head)  # @line L10
            value[h] = u  # @line L11
            stack.append([h, u, 0])
        else:  # @line L12
            while stack and stack[-1][2]:  # @line L13
                del value[stack.pop()[0]]
            if not stack:  # @line L14
                if stats is not None:
                    stats.update(steps=steps, backtracks=backtracks)
                return None
            top = stack[-1]  # @line L15
            top[1], top[2] = 1 - top[1], 1
            value[top[0]] = top[1]
            backtracks += 1
