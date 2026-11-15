# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qsim/. The authors are listed in prov/9H896N.jsonl.

"""QSIM qualitative simulation (Kuipers 1986), pure algorithm plus the
No Divergence and Quiescence heuristics of its footnote.

A model has variables, a quantity space for each variable (a list of
landmark names from "minf" to "inf" that contains "0"), and constraints:

    ("DERIV", f, g)           g is the time derivative of f
    ("M+", f, g, corr)        f = H(g) with H strictly increasing
    ("M-", f, g, corr)        f = H(g) with H strictly decreasing
    ("ADD", f, g, h, corr)    f + g = h
    ("MINUS", f, g, corr)     f = -g
    ("CONSTANT", f)           f does not change

corr is a list of tuples of corresponding landmark names. A qualitative
value is a landmark name or a pair (lo, hi) of adjacent landmarks; a
direction is "inc", "std" or "dec".
"""

from itertools import product
from typing import Dict, List, Optional, Tuple

QVal = object  # a landmark name (str) or a pair (lo, hi)
QState = Tuple[QVal, str]
SIGN = {"inc": 1, "std": 0, "dec": -1}
NEW = "*new*"  # placeholder for a landmark found by I8 or I9


class State:
    """One qualitative state of the whole system."""

    def __init__(self, values: Dict[str, QState], qspace: Dict[str, Tuple[str, ...]],
                 corr: Dict[int, frozenset], at_point: bool,
                 parent: Optional["State"] = None, via: Tuple[str, ...] = ()):
        self.values = values
        self.qspace = qspace
        self.corr = corr
        self.at_point = at_point
        self.parent = parent
        self.via = via

    def key(self):
        return tuple(sorted(self.values.items(), key=lambda kv: kv[0]))


def _pos(qs: Tuple[str, ...], v) -> float:
    """Position of a value in the quantity space; intervals get half steps."""
    if isinstance(v, tuple):
        return qs.index(v[0]) + 0.5
    return float(qs.index(v))


def _sign_vs(qs: Tuple[str, ...], v, landmark: str) -> int:
    d = _pos(qs, v) - qs.index(landmark)
    return (d > 0) - (d < 0)


def _add_ok(a: int, b: int, c: int) -> bool:
    """Some reals x, y have sign x = a, sign y = b and sign (x + y) = c."""
    if a == b:
        return c == a
    if a == 0:
        return c == b
    if b == 0:
        return c == a
    return True


def transitions(qs: Tuple[str, ...], qval, qdir: str, at_point: bool) -> List[Tuple[str, QVal, str]]:
    """Table 1 of Kuipers (1986): the successors of one variable."""
    out = []
    if at_point:
        if not isinstance(qval, tuple):
            j = qs.index(qval)
            if qdir == "std":
                out.append(("P1", qval, "std"))
                if j + 1 < len(qs):
                    out.append(("P2", (qs[j], qs[j + 1]), "inc"))
                if j > 0:
                    out.append(("P3", (qs[j - 1], qs[j]), "dec"))
            elif qdir == "inc":
                out.append(("P4", (qs[j], qs[j + 1]), "inc"))
            else:
                out.append(("P6", (qs[j - 1], qs[j]), "dec"))
        elif qdir == "inc":
            out.append(("P5", qval, "inc"))
        else:
            out.append(("P7", qval, "dec"))
    else:
        if not isinstance(qval, tuple):
            out.append(("I1", qval, "std"))
        elif qdir == "inc":
            lo, hi = qval
            out += [("I2", hi, "std"), ("I3", hi, "inc"), ("I4", qval, "inc"),
                    ("I8", (NEW, lo, hi), "std")]
        else:
            lo, hi = qval
            out += [("I5", lo, "std"), ("I6", lo, "dec"), ("I7", qval, "dec"),
                    ("I9", (NEW, lo, hi), "std")]
    # No Divergence: never move to an infinite landmark.
    return [t for t in out if t[1] not in ("minf", "inf")]


def _as_interval(v):
    """A new landmark sits strictly inside (lo, hi)."""
    if isinstance(v, tuple) and v[0] == NEW:
        return (v[1], v[2])
    return v


def constraint_ok(con, qspace, corr: frozenset, vals: List[QState]) -> bool:
    """Directions of change and magnitudes after a transition (Appendix B)."""
    kind = con[0]
    args = con[1:1 + len(vals)]
    vs = [_as_interval(v) for v, _ in vals]
    ds = [SIGN[d] for _, d in vals]
    sg = [[_sign_vs(qspace[a], v, lm) for lm in qspace[a]] for a, v in zip(args, vs)]

    def s(i, lm):
        return sg[i][qspace[args[i]].index(lm)]

    if kind == "DERIV":
        return ds[0] == s(1, "0")
    if kind == "CONSTANT":
        return ds[0] == 0
    if kind == "M+":
        return ds[0] == ds[1] and all(s(0, p) == s(1, q) for p, q in corr)
    if kind in ("M-", "MINUS"):
        return ds[0] == -ds[1] and all(s(0, p) == -s(1, q) for p, q in corr)
    if kind == "ADD":
        return _add_ok(*ds) and all(_add_ok(s(0, p), s(1, q), s(2, r)) for p, q, r in corr)
    raise ValueError(kind)


def _arity(con) -> int:
    return {"DERIV": 2, "CONSTANT": 1, "M+": 2, "M-": 2, "MINUS": 2, "ADD": 3}[con[0]]


def initial_state(variables, qspace, constraints, values) -> State:
    qs = {v: tuple(qspace[v]) for v in variables}
    corr = {}
    for i, con in enumerate(constraints):
        base = set(tuple(x) for x in (con[1 + _arity(con)] if len(con) > 1 + _arity(con) else []))
        args = con[1:1 + _arity(con)]
        if con[0] not in ("DERIV", "CONSTANT") and all(not isinstance(values[a][0], tuple) for a in args):
            base.add(tuple(values[a][0] for a in args))
        corr[i] = frozenset(base)
    return State(dict(values), qs, corr, True)


def successors(variables, constraints, st: State) -> List[State]:
    """One QSIM cycle: Steps 2 to 5 of Kuipers (1986), Section 4.2."""
    # @line L4 Table 1 transitions for each variable
    cand = {v: transitions(st.qspace[v], st.values[v][0], st.values[v][1], st.at_point)
            for v in variables}
    # @line L5 constraint filtering of the tuples of each constraint
    tuples = []
    for i, con in enumerate(constraints):
        args = con[1:1 + _arity(con)]
        keep = set()
        for combo in product(*[range(len(cand[a])) for a in args]):
            vals = [(cand[a][c][1], cand[a][c][2]) for a, c in zip(args, combo)]
            if constraint_ok(con, st.qspace, st.corr[i], vals):
                keep.add(combo)
        tuples.append((args, keep))
    # @line L6 Waltz filtering: neighbours must agree on shared variables
    changed = True
    while changed:
        changed = False
        for i, (args, keep) in enumerate(tuples):
            for j, (args2, keep2) in enumerate(tuples):
                if i == j:
                    continue
                for pos, a in enumerate(args):
                    if a not in args2:
                        continue
                    pos2 = args2.index(a)
                    allowed = {t[pos2] for t in keep2}
                    bad = {t for t in keep if t[pos] not in allowed}
                    if bad:
                        keep -= bad
                        changed = True
    # @line L7 global interpretations by depth-first search
    order = list(variables)
    interps: List[Dict[str, int]] = []

    def dfs(k: int, chosen: Dict[str, int]) -> None:
        if k == len(order):
            interps.append(dict(chosen))
            return
        v = order[k]
        for c in range(len(cand[v])):
            chosen[v] = c
            ok = True
            for args, keep in tuples:
                if v in args and all(a in chosen for a in args):
                    if tuple(chosen[a] for a in args) not in keep:
                        ok = False
                        break
            if ok:
                dfs(k + 1, chosen)
            del chosen[v]

    dfs(0, {})
    # @line L8 build the new states, with new landmarks and corresponding values
    out = []
    for it in interps:
        qspace = dict(st.qspace)
        values = {}
        for v in variables:
            name, qv, qd = cand[v][it[v]]
            if isinstance(qv, tuple) and qv[0] == NEW:
                lm = v + str(len(qspace[v]))
                qs = list(qspace[v])
                qs.insert(qs.index(qv[2]), lm)
                qspace[v] = tuple(qs)
                qv = lm
            values[v] = (qv, qd)
        corr = {}
        for i, con in enumerate(constraints):
            args = con[1:1 + _arity(con)]
            c = st.corr[i]
            if con[0] not in ("DERIV", "CONSTANT") and all(not isinstance(values[a][0], tuple) for a in args):
                c = c | {tuple(values[a][0] for a in args)}
            corr[i] = c
        via = tuple(cand[v][it[v]][0] for v in variables)
        out.append(State(values, qspace, corr, not st.at_point, st, via))
    return out


def qsim(variables: List[str], qspace: Dict[str, List[str]], constraints: list,
         init: Dict[str, QState], max_states: int = 20) -> List[Tuple[List[State], str]]:
    """Return every behavior as (states, status). status is "cycle",
    "quiescent", "end" (no consistent successor) or "cut" (length limit).

    Precondition: the initial values are landmarks or intervals of their
    quantity spaces and satisfy the constraints. Cost: each cycle is
    O(c * 4^3) for the tuples plus the interpretations, which can be
    exponential in the number of variables (Kuipers 1986, Section 4.9).
    """
    # @line L1 the initial state at time-point t0
    root = initial_state(variables, qspace, constraints, init)
    behaviors = []
    # @line L2
    active = [(root, 1)]
    while active:
        # @line L3
        st, depth = active.pop()
        if depth >= max_states:
            behaviors.append((_path(st), "cut"))
            continue
        kids = []
        for nxt in successors(variables, constraints, st):
            # @line L9 No Change filter
            if not st.at_point and all(t in ("I1", "I4", "I7") for t in nxt.via):
                continue
            # @line L10 Cycle filter
            if nxt.at_point and _repeats(nxt):
                behaviors.append((_path(nxt), "cycle"))
                kids.append(nxt)
                continue
            # @line L11 Quiescence
            if nxt.at_point and all(d == "std" for _, d in nxt.values.values()):
                behaviors.append((_path(nxt), "quiescent"))
                kids.append(nxt)
                continue
            # @line L12
            kids.append(nxt)
            active.append((nxt, depth + 1))
        # @line L13
        if not kids:
            behaviors.append((_path(st), "end"))
    return behaviors


def _repeats(st: State) -> bool:
    k = st.key()
    p = st.parent
    while p is not None:
        if p.at_point and p.key() == k:
            return True
        p = p.parent
    return False


def _path(st: State) -> List[State]:
    out = []
    while st is not None:
        out.append(st)
        st = st.parent
    return out[::-1]
