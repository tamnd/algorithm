# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/argumentation-sat-encoding/. The authors are listed in prov/RCX19M.jsonl.

"""SAT encodings of argumentation semantics, after Besnard and Doutre (2004).

A framework is (args, attacks) as in af.py. Each argument a gets two
variables: in(a), "a is in the set S", and out(a), "some attacker of a is in
S", which is "a is in S+". A clause is a list of nonzero ints, as in DIMACS:
v means variable v is true and -v means it is false.

out(a) is defined by clauses, so it is a Tseitin variable: in every model it
equals the "or" of in(b) over the attackers b of a. So the models of the
formula are in one to one correspondence with the sets S that the semantics
accepts, and blocking the in part of each model enumerates the extensions.

The solver is a small DPLL procedure with unit propagation. It is meant for
the tests of this page, not for large frameworks.
"""

from af import attackers, check_framework

SEMANTICS = ("conflict-free", "admissible", "complete", "stable")


def variables(args):
    """Map each argument to its pair (in variable, out variable), in sorted order."""
    return {a: (2 * i + 1, 2 * i + 2) for i, a in enumerate(sorted(args))}


def encode(args, attacks, semantics):
    """Return (clauses, var) for the semantics, where var maps a to (in var, out var)."""
    if semantics not in SEMANTICS:
        raise ValueError(f"unknown semantics {semantics!r}")
    args = frozenset(args)
    attacks = frozenset(attacks)
    check_framework(args, attacks)
    var = variables(args)
    clauses = []
    for a in sorted(args):
        ia, oa = var[a]
        att = sorted(attackers(attacks, a))
        # out(a) <-> in(b1) or ... or in(bk)
        clauses.append([-oa] + [var[b][0] for b in att])
        for b in att:
            clauses.append([oa, -var[b][0]])
        # Conflict-free: a and an attacker of a are not both in.
        for b in att:
            clauses.append([-ia, -var[b][0]] if b != a else [-ia])
        if semantics in ("admissible", "complete"):
            # a in S -> every attacker of a is in S+.
            for b in att:
                clauses.append([-ia, var[b][1]])
        if semantics == "complete":
            # Every attacker of a is in S+ -> a in S.
            clauses.append([ia] + [-var[b][1] for b in att])
        if semantics == "stable":
            # a is in S or in S+.
            clauses.append([ia, oa])
    return clauses, var


def dpll(clauses, nvars):
    """Return a model as a dict {variable: bool} for all 1..nvars, or None if there is none."""

    def propagate(assign):
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                free = []
                sat = False
                for lit in clause:
                    v = assign.get(abs(lit))
                    if v is None:
                        free.append(lit)
                    elif v == (lit > 0):
                        sat = True
                        break
                if sat:
                    continue
                if not free:
                    return False  # every literal is false
                if len(free) == 1:
                    assign[abs(free[0])] = free[0] > 0
                    changed = True
        return True

    def search(assign):
        if not propagate(assign):
            return None
        for clause in clauses:
            if any(assign.get(abs(lit)) == (lit > 0) for lit in clause):
                continue
            lit = next(x for x in clause if abs(x) not in assign)
            for value in (lit > 0, lit < 0):
                trial = dict(assign)
                trial[abs(lit)] = value
                found = search(trial)
                if found is not None:
                    return found
            return None
        return assign  # every clause is satisfied

    model = search({})
    if model is None:
        return None
    return {v: model.get(v, False) for v in range(1, nvars + 1)}


def extensions(args, attacks, semantics):
    """All sets of arguments accepted by the semantics, by SAT calls with blocking clauses."""
    clauses, var = encode(args, attacks, semantics)
    clauses = [list(c) for c in clauses]
    nvars = 2 * len(var)
    found = []
    while True:
        model = dpll(clauses, nvars)
        if model is None:
            break
        s = frozenset(a for a in var if model[var[a][0]])
        found.append(s)
        # Block this set: some in variable must take the other value.
        clauses.append([-var[a][0] if a in s else var[a][0] for a in var])
    return sorted(found, key=lambda s: (len(s), sorted(s)))


def preferred_extensions(args, attacks):
    """The maximal admissible sets, by growing one admissible set at a time.

    Find an admissible set S not inside a preferred extension found so far.
    Then ask again and again for an admissible set that strictly contains S,
    until there is none: S is then preferred. Block every subset of S with the
    clause "some argument outside S is in".
    """
    clauses, var = encode(args, attacks, "admissible")
    nvars = 2 * len(var)
    blocks = []
    found = []
    while True:
        model = dpll(clauses + blocks, nvars)
        if model is None:
            break
        s = frozenset(a for a in var if model[var[a][0]])
        while True:
            grow = [[var[a][0]] for a in s] + [[var[a][0] for a in var if a not in s]]
            bigger = dpll(clauses + grow, nvars)
            if bigger is None:
                break
            s = frozenset(a for a in var if bigger[var[a][0]])
        found.append(s)
        blocks.append([var[a][0] for a in var if a not in s])
    return sorted(found, key=lambda s: (len(s), sorted(s)))
