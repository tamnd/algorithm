# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pctl-model-checking/. The authors are listed in prov/7T9702.jsonl.

"""PCTL model checking on a finite discrete-time Markov chain, with exact
rational arithmetic.

A chain is a dict with
  "P": a list of dicts, P[s][t] the probability (a Fraction) of s -> t,
       each row summing to 1;
  "L": a list of sets of atomic propositions, one per state.

State formulas are tuples:
  ("true",)  ("ap", a)  ("not", f)  ("and", f, g)  ("P", op, p, path)
with op in "<", "<=", ">=", ">" and p a Fraction. Path formulas are
  ("X", f)  ("U", f, g)  ("BU", f, g, k)    (BU is the bounded until U<=k).
"""

from fractions import Fraction

OPS = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    ">": lambda a, b: a > b,
}


def predecessors(chain):
    n = len(chain["P"])
    pre = [set() for _ in range(n)]
    for s, row in enumerate(chain["P"]):
        for t, p in row.items():
            if p > 0:
                pre[t].add(s)
    return pre


def backward(pre, targets, allowed):
    """States in allowed that can reach targets through allowed states
    (targets themselves included)."""
    seen = set(targets)
    stack = list(targets)
    while stack:
        t = stack.pop()
        for s in pre[t]:
            if s not in seen and s in allowed:
                seen.add(s)
                stack.append(s)
    return seen


def solve(a, b):
    """Solve (I - A) x = b by Gaussian elimination over the rationals.
    a is a dict-of-dicts square matrix on the index list, b a dict."""
    idx = sorted(b)
    pos = {s: i for i, s in enumerate(idx)}
    m = len(idx)
    rows = []
    for s in idx:
        row = [Fraction(0)] * (m + 1)
        row[pos[s]] += 1
        for t, p in a[s].items():
            row[pos[t]] -= p
        row[m] = b[s]
        rows.append(row)
    for c in range(m):
        piv = next(r for r in range(c, m) if rows[r][c] != 0)
        rows[c], rows[piv] = rows[piv], rows[c]
        inv = 1 / rows[c][c]
        rows[c] = [v * inv for v in rows[c]]
        for r in range(m):
            if r != c and rows[r][c] != 0:
                f = rows[r][c]
                rows[r] = [v - f * w for v, w in zip(rows[r], rows[c])]
    return {s: rows[pos[s]][m] for s in idx}


def prob_until(chain, sat_phi, sat_psi):
    """x[s] = Pr_s(phi U psi) for every state, as exact Fractions."""
    n = len(chain["P"])
    pre = predecessors(chain)
    s_no = set(range(n)) - backward(pre, sat_psi, sat_phi)  # @line L1
    s_yes = set(range(n)) - backward(pre, s_no, sat_phi - sat_psi)  # @line L2
    rest = set(range(n)) - s_no - s_yes  # @line L3
    a = {s: {t: p for t, p in chain["P"][s].items() if t in rest} for s in rest}  # @line L4
    b = {s: sum((p for t, p in chain["P"][s].items() if t in s_yes), Fraction(0)) for s in rest}  # @line L5
    sol = solve(a, b) if rest else {}  # @line L6
    x = [Fraction(1) if s in s_yes else Fraction(0) for s in range(n)]  # @line L7
    for s, v in sol.items():
        x[s] = v  # @line L8
    return x  # @line L9


def prob_bounded_until(chain, sat_phi, sat_psi, k):
    """x[s] = Pr_s(phi U<=k psi), by k matrix-vector products."""
    n = len(chain["P"])
    x = [Fraction(1) if s in sat_psi else Fraction(0) for s in range(n)]
    live = sat_phi - sat_psi
    for _ in range(k):
        x = [
            sum((p * x[t] for t, p in chain["P"][s].items()), Fraction(0)) if s in live else x[s]
            for s in range(n)
        ]
    return x


def prob_next(chain, sat_phi):
    return [sum((p for t, p in row.items() if t in sat_phi), Fraction(0)) for row in chain["P"]]


def probabilities(chain, path, sat):
    """The probability vector of a path formula; sat computes Sat(f)."""
    kind = path[0]
    if kind == "X":
        return prob_next(chain, sat(path[1]))
    if kind == "U":
        return prob_until(chain, sat(path[1]), sat(path[2]))
    if kind == "BU":
        return prob_bounded_until(chain, sat(path[1]), sat(path[2]), path[3])
    raise ValueError(f"unknown path formula {path!r}")


def check(chain, formula):
    """Sat(formula): the set of states that satisfy a PCTL state formula.
    Each subformula is handled once, bottom up."""
    n = len(chain["P"])
    memo = {}

    def sat(f):
        if f in memo:
            return memo[f]
        kind = f[0]
        if kind == "true":
            res = set(range(n))
        elif kind == "ap":
            res = {s for s in range(n) if f[1] in chain["L"][s]}
        elif kind == "not":
            res = set(range(n)) - sat(f[1])
        elif kind == "and":
            res = sat(f[1]) & sat(f[2])
        elif kind == "P":
            _, op, p, path = f
            x = probabilities(chain, path, sat)
            res = {s for s in range(n) if OPS[op](x[s], p)}
        else:
            raise ValueError(f"unknown state formula {f!r}")
        memo[f] = res
        return res

    return sat(formula)
