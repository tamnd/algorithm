# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qsim/. The authors are listed in prov/9H896N.jsonl.

import random
from itertools import product

from qsim import _arity, constraint_ok, qsim, successors, transitions

BALL_VARS = ["Y", "V", "A"]
BALL_QS = {"Y": ["minf", "0", "inf"], "V": ["minf", "0", "v0", "inf"], "A": ["minf", "g", "0", "inf"]}
BALL_CONS = [("DERIV", "Y", "V"), ("DERIV", "V", "A"), ("CONSTANT", "A")]
BALL_INIT = {"Y": ("0", "inc"), "V": ("v0", "dec"), "A": ("g", "std")}

SPRING_VARS = ["X", "V", "A"]
SPRING_QS = {"X": ["minf", "0", "inf"], "V": ["minf", "0", "v0", "inf"], "A": ["minf", "0", "inf"]}
SPRING_CONS = [("DERIV", "X", "V"), ("DERIV", "V", "A"), ("M-", "A", "X", [("0", "0")])]
SPRING_INIT = {"X": ("0", "inc"), "V": ("v0", "std"), "A": ("0", "dec")}

# Damped spring: F = -k X, D = -c V, A = F + D.
DAMP_VARS = ["X", "V", "A", "F", "D"]
DAMP_QS = {"X": ["minf", "0", "x0", "inf"], "V": ["minf", "0", "inf"],
           "A": ["minf", "a0", "0", "inf"], "F": ["minf", "f0", "0", "inf"],
           "D": ["minf", "0", "inf"]}
DAMP_CONS = [("DERIV", "X", "V"), ("DERIV", "V", "A"), ("M-", "X", "F", [("0", "0")]),
             ("M-", "V", "D", [("0", "0")]), ("ADD", "F", "D", "A", [("0", "0", "0")])]
DAMP_INIT = {"X": ("x0", "std"), "V": ("0", "dec"), "A": ("a0", "inc"),
             "F": ("f0", "std"), "D": ("0", "inc")}


def project(qs_initial, qs, value):
    """Map a value to the initial landmarks: a new landmark becomes the
    initial interval that contains it."""
    if isinstance(value, tuple):
        lo, hi = value
    elif value in qs_initial:
        return value
    else:
        lo = hi = value
    i = qs.index(lo)
    while qs[i] not in qs_initial:
        i -= 1
    j = qs.index(hi)
    while qs[j] not in qs_initial:
        j += 1
    return (qs[i], qs[j])


def compress(seq):
    out = []
    for s in seq:
        if not out or out[-1] != s:
            out.append(s)
    return out


def qsim_runs(variables, qs0, behaviors):
    """Projected, compressed sequences of interval states of each behavior."""
    runs = []
    for states, status in behaviors:
        seq = []
        for st in states:
            if not st.at_point:
                seq.append(tuple((project(qs0[v], st.qspace[v], st.values[v][0]), st.values[v][1])
                                 for v in variables))
        runs.append((compress(seq), status))
    return runs


def sgn(x):
    return (x > 0) - (x < 0)


def qual(landmarks, x):
    """Qualitative value of a number against named numeric landmarks."""
    names = [n for n, _ in landmarks]
    vals = [v for _, v in landmarks]
    for n, v in landmarks:
        if x == v:
            return n
    i = sum(1 for v in vals if v < x)
    return (names[i - 1], names[i])


DIR = {1: "inc", 0: "std", -1: "dec"}


def euler_run(lms, rhs, x, h, steps, variables):
    """Simple Euler; the qualitative state of each sample after t0."""
    seq = []
    for _ in range(steps):
        dx = rhs(x)
        x = [a + h * b for a, b in zip(x, dx)]
        full, dirs = rhs(x, full=True)
        st = tuple((qual(lms[v], val), DIR[sgn(d)]) for v, val, d in zip(variables, full, dirs))
        # A sample that sits on a landmark while moving is a time point, not an interval.
        if any(not isinstance(q, tuple) and d != "std" for q, d in st):
            continue
        seq.append(st)
    return compress(seq)


def matches(num, runs, m):
    """The first m numeric interval states are a prefix of some behavior."""
    num = num[:m]
    return any(seq[:len(num)] == num for seq, _ in runs)


def test_ball_trace():
    (states, status), = qsim(BALL_VARS, BALL_QS, BALL_CONS, BALL_INIT, max_states=12)
    assert status == "end"
    assert [s.via for s in states[1:]] == [("P4", "P6", "P1"), ("I8", "I6", "I1"),
                                           ("P3", "P6", "P1"), ("I6", "I7", "I1"),
                                           ("P6", "P7", "P1")]
    top = states[2]
    assert top.values["Y"] == ("Y3", "std") and top.values["V"] == ("0", "dec")
    assert top.qspace["Y"] == ("minf", "0", "Y3", "inf")


def test_table1_counts():
    qs = ("minf", "0", "l", "inf")
    assert len(transitions(qs, "0", "std", True)) == 3
    assert [t[0] for t in transitions(qs, ("0", "l"), "inc", False)] == ["I2", "I3", "I4", "I8"]
    assert [t[0] for t in transitions(qs, ("0", "l"), "dec", False)] == ["I5", "I6", "I7", "I9"]
    # No Divergence removes the moves to infinity.
    assert [t[0] for t in transitions(qs, ("l", "inf"), "inc", False)] == ["I4", "I8"]


def test_spring_three_branches_and_spurious():
    bs = qsim(SPRING_VARS, SPRING_QS, SPRING_CONS, SPRING_INIT, max_states=10)
    assert len(bs) == 3
    statuses = sorted(s for _, s in bs)
    assert statuses == ["cut", "cut", "cycle"]
    spurious = 0
    for states, _ in bs:
        for st in states[1:]:
            if not st.at_point:
                continue
            x, v = st.values["X"][0], st.values["V"][0]
            qv = st.qspace["V"]
            low = v[0] if isinstance(v, tuple) else v
            pos_v = qv.index(low) >= qv.index("0") and v != "0"
            # Energy is conserved: X = 0 with V > 0 forces V = v0, and V = v0 forces X = 0.
            if (x == "0" and pos_v and v != "v0") or (v == "v0" and x != "0"):
                spurious += 1
                break
    assert spurious == 2


def brute_successors(variables, constraints, st):
    cand = {v: transitions(st.qspace[v], st.values[v][0], st.values[v][1], st.at_point) for v in variables}
    out = set()
    for combo in product(*[range(len(cand[v])) for v in variables]):
        pick = dict(zip(variables, combo))
        ok = True
        for i, con in enumerate(constraints):
            args = con[1:1 + _arity(con)]
            vals = [(cand[a][pick[a]][1], cand[a][pick[a]][2]) for a in args]
            if not constraint_ok(con, st.qspace, st.corr[i], vals):
                ok = False
                break
        if ok:
            out.add(tuple(cand[v][pick[v]][0] for v in variables))
    return out


def test_waltz_and_search_lose_nothing():
    rng = random.Random(1986)
    behaviors = qsim(DAMP_VARS, DAMP_QS, DAMP_CONS, DAMP_INIT, max_states=10)
    states = [st for b, _ in behaviors for st in b]
    rng.shuffle(states)
    for st in states[:500]:
        got = {s.via for s in successors(DAMP_VARS, DAMP_CONS, st)}
        assert got == brute_successors(DAMP_VARS, DAMP_CONS, st)


def test_soundness_ball():
    rng = random.Random(7)
    runs = qsim_runs(BALL_VARS, BALL_QS, qsim(BALL_VARS, BALL_QS, BALL_CONS, BALL_INIT, max_states=12))
    for _ in range(40):
        v0 = rng.uniform(1.0, 5.0)
        g = -rng.uniform(1.0, 10.0)
        lms = {"Y": [("0", 0.0)], "V": [("0", 0.0), ("v0", v0)], "A": [("g", g), ("0", 0.0)]}
        lms = {v: [("minf", float("-inf"))] + lms[v] + [("inf", float("inf"))] for v in lms}

        def rhs(s, full=False, g=g):
            y, v = s
            if full:
                return [y, v, g], [v, g, 0.0]
            return [v, g]

        num = euler_run(lms, rhs, [0.0, v0], 1e-3, int(3 * v0 / -g / 1e-3), BALL_VARS)
        assert len(num) == 3
        assert matches(num, runs, len(num))


def test_soundness_damped_spring():
    rng = random.Random(11)
    runs = qsim_runs(DAMP_VARS, DAMP_QS, qsim(DAMP_VARS, DAMP_QS, DAMP_CONS, DAMP_INIT, max_states=12))
    for _ in range(20):
        k = rng.uniform(0.5, 4.0)
        c = rng.uniform(0.2, 5.0)
        x0 = rng.uniform(0.5, 2.0)
        lms = {"X": [("0", 0.0), ("x0", x0)], "V": [("0", 0.0)], "A": [("a0", -k * x0), ("0", 0.0)],
               "F": [("f0", -k * x0), ("0", 0.0)], "D": [("0", 0.0)]}
        lms = {v: [("minf", float("-inf"))] + lms[v] + [("inf", float("inf"))] for v in lms}

        def rhs(s, full=False, k=k, c=c):
            x, v = s
            a = -k * x - c * v
            if full:
                return [x, v, a, -k * x, -c * v], [v, a, -k * v - c * a, -k * v, -c * a]
            return [v, a]

        num = euler_run(lms, rhs, [x0, 0.0], 2e-3, 3000, DAMP_VARS)
        assert matches(num, runs, 6)
