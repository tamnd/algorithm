# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/urban-nominal-unification/. The authors are listed in prov/5H4NV6.jsonl.
"""Nominal unification after Urban, Pitts and Gabbay (2004).

Nominal terms:
    ("atom", a)            an atom (a name)
    ("susp", pi, X)        a suspension pi.X of the variable X
    ("abs", a, t)          the abstraction [a]t
    ("fn", f, (t1, ...))   a function symbol applied to terms (tuples and unit are function symbols)

A permutation pi is a tuple of swappings ((a1, b1), ..., (an, bn)). It acts on an
atom by applying the swappings from the right to the left, so that the action
of pi1 + pi2 is pi1 after pi2.

unify(eqs, fresh) takes a list of equations (t, u) and of freshness problems
(a, t). It returns (nabla, sigma), where nabla is a set of pairs (a, X) that
mean a # X and sigma maps variables to terms, or None if there is no solution.
"""


def perm_atom(pi, a):
    for x, y in reversed(pi):
        if a == x:
            a = y
        elif a == y:
            a = x
    return a


def inverse(pi):
    return tuple(reversed(pi))


def act(pi, t):
    """The permutation action pi . t."""
    if not pi:
        return t
    kind = t[0]
    if kind == "atom":
        return ("atom", perm_atom(pi, t[1]))
    if kind == "susp":
        return ("susp", tuple(pi) + tuple(t[1]), t[2])
    if kind == "abs":
        return ("abs", perm_atom(pi, t[1]), act(pi, t[2]))
    return ("fn", t[1], tuple(act(pi, s) for s in t[2]))


def disagreement(pi1, pi2):
    """ds(pi1, pi2): the atoms on which the two permutations differ."""
    atoms = {a for sw in tuple(pi1) + tuple(pi2) for a in sw}
    return {a for a in atoms if perm_atom(pi1, a) != perm_atom(pi2, a)}


def variables(t, out=None):
    out = set() if out is None else out
    if t[0] == "susp":
        out.add(t[2])
    elif t[0] == "abs":
        variables(t[2], out)
    elif t[0] == "fn":
        for s in t[2]:
            variables(s, out)
    return out


def subst(sigma, t):
    """Apply a substitution. It is not capture avoiding: sigma(pi.X) = pi . sigma(X)."""
    kind = t[0]
    if kind == "atom":
        return t
    if kind == "susp":
        return act(t[1], sigma[t[2]]) if t[2] in sigma else t
    if kind == "abs":
        return ("abs", t[1], subst(sigma, t[2]))
    return ("fn", t[1], tuple(subst(sigma, s) for s in t[2]))


def unify(eqs, fresh=()):
    sigma = {}  # @line L1
    eqs = list(eqs)
    fresh = list(fresh)
    while eqs:  # @line L2
        t, u = eqs.pop()  # @line L3
        if t[0] != "susp" and u[0] == "susp":
            t, u = u, t
        if t[0] == "atom" and u[0] == "atom":  # @line L4
            if t[1] != u[1]:
                return None  # @line L5
        elif t[0] == "fn" and u[0] == "fn":
            if t[1] != u[1] or len(t[2]) != len(u[2]):
                return None
            eqs.extend(zip(t[2], u[2]))  # @line L6
        elif t[0] == "abs" and u[0] == "abs" and t[1] == u[1]:
            eqs.append((t[2], u[2]))  # @line L7
        elif t[0] == "abs" and u[0] == "abs":
            a, b = t[1], u[1]
            eqs.append((t[2], act(((a, b),), u[2])))  # @line L8
            fresh.append((a, u[2]))
        elif t[0] == "susp" and u[0] == "susp" and t[2] == u[2]:
            fresh.extend((a, ("susp", (), t[2])) for a in disagreement(t[1], u[1]))  # @line L9
        elif t[0] == "susp" and t[2] not in variables(u):
            x = t[2]
            rho = {x: act(inverse(t[1]), u)}  # @line L10
            eqs = [(subst(rho, p), subst(rho, q)) for p, q in eqs]
            fresh = [(a, subst(rho, q)) for a, q in fresh]
            sigma = {y: subst(rho, v) for y, v in sigma.items()}
            sigma[x] = rho[x]
        else:
            return None  # @line L11
    nabla = set()  # @line L12
    while fresh:  # @line L13
        a, t = fresh.pop()
        if t[0] == "atom":
            if t[1] == a:
                return None  # @line L14
        elif t[0] == "abs":
            if t[1] == a:
                continue  # @line L15
            fresh.append((a, t[2]))  # @line L16
        elif t[0] == "fn":
            fresh.extend((a, s) for s in t[2])  # @line L17
        else:
            nabla.add((perm_atom(inverse(t[1]), a), t[2]))  # @line L18
    return nabla, sigma  # @line L19
