# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-algorithm/. The authors are listed in prov/C6DBQN.jsonl.
"""The D-algorithm (Roth 1966) for one single stuck-at fault.

Each line holds a pair (good value, faulty value), each in {0, 1, X}. Roth's
five values are 0 = (0, 0), 1 = (1, 1), D = (1, 0), D' = (0, 1) and X. The
search assigns values to internal lines, not only to primary inputs. It
propagates the fault effect through the D-frontier, then justifies the values
of the J-frontier, and backtracks on a conflict.

The gate types are AND, OR, NAND, NOR, NOT and BUF. Rewrite XOR and XNOR into
these types first.
"""

from __future__ import annotations

from typing import Optional

from gatenet import X, Circuit, Fault, controlling, eval_gate, inversion

GOOD, BAD = 0, 1


class _State:
    """Values of all lines in the good (val[0]) and the faulty (val[1]) circuit."""

    def __init__(self, c: Circuit, fault: Fault) -> None:
        self.c = c
        self.site, self.s = fault
        self.val = [[X] * c.n_lines, [X] * c.n_lines]

    def copy(self) -> list[list[int]]:
        return [self.val[0][:], self.val[1][:]]

    def restore(self, saved: list[list[int]]) -> None:
        self.val = [saved[0][:], saved[1][:]]

    def set(self, m: int, k: int, v: int) -> Optional[bool]:
        """Assign v to line k in circuit m. True if new, False if already so, None on a conflict."""
        cur = self.val[m][k]
        if cur == X:
            self.val[m][k] = v
            return True
        return False if cur == v else None

    def fixed(self, m: int, k: int) -> bool:
        """The faulty value of the fault site does not depend on the inputs of the site."""
        return m == BAD and k == self.site


def _imply_line(st: _State, k: int) -> Optional[bool]:
    """Apply the forward and the backward rules at line k. Returns None on a conflict."""
    c, val = st.c, st.val
    changed = False

    def put(m: int, j: int, v: int) -> bool:
        nonlocal changed
        r = st.set(m, j, v)
        if r is None:
            return False
        changed = changed or r
        return True

    if c.kind[k] == "pi":
        if k != st.site:  # a primary input has the same value in both circuits
            for m in (GOOD, BAD):
                if val[m][k] != X and not put(1 - m, k, val[m][k]):
                    return None
        return changed
    for m in (GOOD, BAD):
        if st.fixed(m, k):
            continue
        ins = c.fanin[k]
        out = eval_gate(c.op[k], [val[m][j] for j in ins])
        if out != X and not put(m, k, out):  # forward
            return None
        w = val[m][k]
        if w == X:
            continue
        op = c.op[k]
        u = w ^ inversion(op)  # the value of the gate before its inversion
        if op in ("NOT", "BUF"):
            if not put(m, ins[0], u):
                return None
            continue
        cv = controlling(op)
        if u == 1 - cv:  # the output is not forced: every input is non-controlling
            for j in ins:
                if not put(m, j, 1 - cv):
                    return None
        else:  # some input must be controlling; if only one can be, it is
            if cv in [val[m][j] for j in ins]:
                continue
            free = [j for j in ins if val[m][j] == X]
            if not free:
                return None
            if len(free) == 1 and not put(m, free[0], cv):
                return None
    return changed


def imply_and_check(st: _State) -> bool:
    """Apply all implications until nothing changes. False on a conflict."""
    while True:
        changed = False
        for k in range(st.c.n_lines):
            r = _imply_line(st, k)
            if r is None:
                return False
            changed = changed or r
        if not changed:
            return True


def _effect(st: _State, k: int) -> bool:
    g, b = st.val[GOOD][k], st.val[BAD][k]
    return g != X and b != X and g != b


def d_frontier(st: _State) -> list[int]:
    """Gate lines that are not fully known and have an input with D or D'."""
    c, val = st.c, st.val
    return [
        k for k in range(c.n_lines)
        if c.kind[k] == "gate" and X in (val[GOOD][k], val[BAD][k])
        and any(_effect(st, j) for j in c.fanin[k])
    ]


def j_frontier(st: _State) -> list[tuple[int, int]]:
    """Pairs (gate line, circuit) whose value is known but not implied by the inputs."""
    c, val = st.c, st.val
    out = []
    for k in range(c.n_lines - 1, -1, -1):
        if c.kind[k] != "gate":
            continue
        for m in (GOOD, BAD):
            if not st.fixed(m, k) and val[m][k] != X and eval_gate(c.op[k], [val[m][j] for j in c.fanin[k]]) == X:
                out.append((k, m))
    return out


def _d_alg(st: _State, stats: dict[str, int]) -> bool:
    stats["calls"] += 1
    if not imply_and_check(st):  # @line L1
        return False
    c = st.c
    if not any(_effect(st, o) for o in c.po):  # @line L2
        frontier = d_frontier(st)
        if not frontier:  # @line L3
            return False
        for gate in frontier:  # @line L4
            cv = controlling(c.op[gate])
            if cv is None:
                continue
            saved = st.copy()
            ok = True
            for j in c.fanin[gate]:  # @line L5
                if not _effect(st, j):  # every input without D or D' gets the non-controlling value
                    for m in (GOOD, BAD):
                        if st.set(m, j, 1 - cv) is None:
                            ok = False
            if ok and _d_alg(st, stats):  # @line L6
                return True
            st.restore(saved)  # @line L7
            stats["backtracks"] += 1
        return False  # @line L8
    jf = j_frontier(st)
    if not jf:  # @line L9
        return True
    gate, m = jf[0]  # @line L10
    cv = controlling(c.op[gate])
    for j in [j for j in c.fanin[gate] if st.val[m][j] == X]:  # @line L11
        saved = st.copy()
        st.val[m][j] = cv  # @line L12
        if _d_alg(st, stats):  # @line L13
            return True
        st.restore(saved)  # @line L14
        st.val[m][j] = 1 - cv  # every test below this node has the other value on j
        stats["backtracks"] += 1
    return False  # @line L15


def d_algorithm(c: Circuit, fault: Fault, stats: Optional[dict[str, int]] = None) -> Optional[tuple[int, ...]]:
    """Return a test for the fault, with X for free inputs, or None if the fault is undetectable.

    Every completion of the X entries detects the fault. The search depth is at
    most 2L, since each call fixes at least one more of the 2L values.
    """
    for op in c.op:
        if op in ("XOR", "XNOR"):
            raise ValueError("rewrite XOR and XNOR into AND, OR and NOT first")
    st = _State(c, fault)
    site, s = fault
    st.val[BAD][site] = s  # the faulty circuit has the stuck value at the site
    st.val[GOOD][site] = 1 - s  # activate the fault: D or D' at the site
    counts = {"calls": 0, "backtracks": 0}
    ok = _d_alg(st, counts)
    if stats is not None:
        stats.update(counts)
    if not ok:
        return None
    return tuple(st.val[GOOD][p] for p in c.pi)
