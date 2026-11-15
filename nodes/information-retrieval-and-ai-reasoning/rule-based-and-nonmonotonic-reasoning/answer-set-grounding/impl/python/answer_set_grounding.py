# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/answer-set-grounding/. The authors are listed in prov/JQHNQC.jsonl.
"""A grounder for safe normal programs with variables, by semi-naive evaluation.

An atom is a tuple (predicate, t1, ..., tk) of strings. A term that starts
with an upper-case letter is a variable; every other term is a constant. There
are no function symbols. A rule is (head, pos, neg) with pos and neg tuples of
atoms. A rule is safe when every variable of the head and of neg occurs in pos.

ground(program) returns a ground program in the format of lp.py, whose atoms
are the ground tuples. It has the same stable models as the instantiation of
the program over all constants (the Herbrand universe).

1. Semi-naive evaluation of the positive parts of the rules computes the
   domain D, an overestimate of the atoms that some stable model can contain,
   and emits each rule instance whose positive body lies in D exactly once.
2. Simplification removes what the domain and the definite part decide:
   a rule with not c, where c is derived by the definite rules alone, is
   deleted; a literal not c with c outside D is true and is deleted; a
   positive body atom derived by the definite rules alone is deleted.
"""

import lp


def is_var(term):
    return term[:1].isupper()


def variables(atoms):
    return {t for atom in atoms for t in atom[1:] if is_var(t)}


def check_safe(rule):
    head, pos, neg = rule
    unsafe = variables((head,) + tuple(neg)) - variables(pos)
    if unsafe:
        raise ValueError(f"unsafe variables {sorted(unsafe)} in rule {rule}")


def match(pattern, fact, theta):
    """Extend the substitution theta so that pattern becomes fact, or return None."""
    if pattern[0] != fact[0] or len(pattern) != len(fact):
        return None
    out = dict(theta)
    for p, f in zip(pattern[1:], fact[1:]):
        if is_var(p):
            if out.setdefault(p, f) != f:
                return None
        elif p != f:
            return None
    return out


def subst(atom, theta):
    return (atom[0],) + tuple(theta.get(t, t) for t in atom[1:])


def index(atoms):
    """Atoms grouped by (predicate, arity)."""
    out = {}
    for a in atoms:
        out.setdefault((a[0], len(a)), []).append(a)
    return out


def joins(pos, sources, theta=None, i=0):
    """All substitutions that map pos[i] into sources[i] for every i."""
    if theta is None:
        theta = {}
    if i == len(pos):
        yield theta
        return
    for fact in sources[i].get((pos[i][0], len(pos[i])), ()):
        nxt = match(pos[i], fact, theta)
        if nxt is not None:
            yield from joins(pos, sources, nxt, i + 1)


def instantiate(program, stats=None):
    """Semi-naive evaluation. Return the domain and the list of rule instances with positive body in the domain."""
    for rule in program:
        check_safe(rule)  # @line L1
    instances = []
    seen = set()

    def emit(rule, theta):
        head, pos, neg = rule
        inst = (subst(head, theta), tuple(subst(b, theta) for b in pos), tuple(subst(c, theta) for c in neg))
        if stats is not None:
            stats["emitted"] = stats.get("emitted", 0) + 1
        if inst not in seen:
            seen.add(inst)
            instances.append(inst)
        return inst[0]

    old = set()
    delta = set()
    for rule in program:
        if not rule[1]:
            delta.add(emit(rule, {}))  # @line L2
    rounds = 0
    while delta:  # @line L3
        rounds += 1
        new_atoms = set()  # @line L4
        old_ix, delta_ix, all_ix = index(old), index(delta), index(old | delta)
        for rule in program:
            pos = rule[1]
            for j in range(len(pos)):  # @line L5
                # The first atom from the last round is at position j: earlier ones are old, later ones any.
                sources = [old_ix] * j + [delta_ix] + [all_ix] * (len(pos) - j - 1)
                for theta in joins(pos, sources):  # @line L6
                    new_atoms.add(emit(rule, theta))  # @line L7
        old |= delta
        delta = new_atoms - old  # @line L8
    if stats is not None:
        stats["rounds"] = rounds
    return old, instances


def simplify(domain, instances):
    """Remove what the domain and the definite instances decide. Duplicates are removed; the order is kept."""
    certain = lp.least_model([(h, pos, ()) for h, pos, neg in instances if not neg])  # @line L9
    out = []
    seen = set()
    for h, pos, neg in instances:  # @line L10
        if any(c in certain for c in neg):  # @line L11
            continue
        rule = (h, tuple(b for b in pos if b not in certain), tuple(c for c in neg if c in domain))  # @line L12
        if rule not in seen:
            seen.add(rule)
            out.append(rule)
    return out  # @line L13


def ground(program, stats=None):
    """The simplified ground program."""
    domain, instances = instantiate(program, stats)
    return simplify(domain, instances)
