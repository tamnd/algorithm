# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smodels-algorithm/. The authors are listed in prov/NCW1XZ.jsonl.
"""The smodels search of Simons, Niemela and Soininen (2002) for ground programs.

A program has three kinds of rules:
- normal rules (head, pos, neg), as in lp.py: head <- pos, not neg;
- choice rules (heads, pos, neg): {heads} <- pos, not neg, where heads is a tuple of atoms;
- constraints (pos, neg): <- pos, not neg.

A partial assignment is a dict from atoms to True or False. EXPAND closes it
under ATLEAST (the propagation rules of Simons) and ATMOST (the atoms outside
the upper closure are false, as in the well-founded semantics). LOOKAHEAD
tries each open atom both ways and fixes it when one way gives a conflict.
SEARCH branches on one atom and explores both values, so it returns all
stable models. This is the textbook form of the method, with each fixpoint
computed by repeated scans over the rules; the real smodels uses counters
and queues for the same fixpoints.
"""

NORMAL, CHOICE, CONSTRAINT = "normal", "choice", "constraint"


class Conflict(Exception):
    """An atom would get both values."""


class Program:
    """A ground program with normal rules, choice rules and constraints."""

    def __init__(self, normal=(), choice=(), constraints=()):
        self.rules = []
        for head, pos, neg in normal:
            self.rules.append((NORMAL, (head,), tuple(pos), tuple(neg)))
        for heads, pos, neg in choice:
            self.rules.append((CHOICE, tuple(heads), tuple(pos), tuple(neg)))
        for pos, neg in constraints:
            self.rules.append((CONSTRAINT, (), tuple(pos), tuple(neg)))
        found = set()
        for _, heads, pos, neg in self.rules:
            found.update(heads)
            found.update(pos)
            found.update(neg)
        self.atoms = sorted(found)
        self.support = {a: [] for a in self.atoms}
        for i, (kind, heads, _, _) in enumerate(self.rules):
            if kind != CONSTRAINT:
                for h in heads:
                    self.support[h].append(i)


def body_value(rule, a):
    """True, False or None (open) for the body of the rule under the partial assignment a."""
    _, _, pos, neg = rule
    open_seen = False
    for b in pos:
        v = a.get(b)
        if v is False:
            return False
        if v is None:
            open_seen = True
    for c in neg:
        v = a.get(c)
        if v is True:
            return False
        if v is None:
            open_seen = True
    return None if open_seen else True


def set_value(a, atom, value):
    """Assign atom := value. Return True when a changed; raise Conflict on the opposite value."""
    old = a.get(atom)
    if old is None:
        a[atom] = value
        return True
    if old != value:
        raise Conflict(atom)
    return False


def atleast(prog, a):
    """Close a under the four propagation rules. Raise Conflict when they clash."""
    changed = True
    while changed:
        changed = False
        for rule in prog.rules:
            kind, heads, pos, neg = rule
            value = body_value(rule, a)
            # Rule 1: a normal rule with a true body makes its head true.
            if kind == NORMAL and value is True:
                changed |= set_value(a, heads[0], True)  # @line L12
            # Rule 4: the body of a constraint, or of a normal rule with a false head, must not become true.
            if kind == CONSTRAINT or (kind == NORMAL and a.get(heads[0]) is False):  # @line L15
                if value is True:
                    raise Conflict(rule)
                if value is None:
                    open_lits = [(b, True) for b in pos if a.get(b) is None]
                    open_lits += [(c, False) for c in neg if a.get(c) is None]
                    if len(open_lits) == 1:
                        atom, makes_true = open_lits[0]
                        changed |= set_value(a, atom, not makes_true)  # @line L16
        for atom in prog.atoms:
            live = [i for i in prog.support[atom] if body_value(prog.rules[i], a) is not False]
            # Rule 2: an atom with no rule whose body can still be true is false.
            if not live:
                changed |= set_value(a, atom, False)  # @line L13
            # Rule 3: a true atom with one possible rule needs the body of that rule.
            elif len(live) == 1 and a.get(atom) is True:  # @line L14
                _, _, pos, neg = prog.rules[live[0]]
                for b in pos:
                    changed |= set_value(a, b, True)
                for c in neg:
                    changed |= set_value(a, c, False)
    return a


def upper_closure(prog, a):
    """The atoms that some stable model extending a may contain: a least fixpoint over the rules not blocked by a."""
    upper = set()
    changed = True
    while changed:
        changed = False
        for kind, heads, pos, neg in prog.rules:
            if kind == CONSTRAINT or any(a.get(c) is True for c in neg):
                continue
            if all(b in upper for b in pos):
                for h in heads:
                    if h not in upper and a.get(h) is not False:  # @line L8
                        upper.add(h)
                        changed = True
    return upper


def atmost(prog, a):
    """Make every atom outside the upper closure false. Return True when a changed."""
    upper = upper_closure(prog, a)  # @line L7
    changed = False
    for atom in prog.atoms:
        if atom not in upper:
            changed |= set_value(a, atom, False)  # @line L9
    return changed


def expand(prog, a):
    """Alternate ATLEAST and ATMOST until neither changes a. Raise Conflict on a clash."""
    while True:  # @line L5
        atleast(prog, a)  # @line L6
        if not atmost(prog, a):  # @line L10
            return a  # @line L11


def lookahead(prog, a):
    """Fix each open atom whose one value expands to a conflict. Return the expansion sizes of the open atoms."""
    while True:
        scores = {}
        progress = False
        for atom in prog.atoms:  # @line L17
            if atom in a:
                continue
            sizes = []
            for value in (True, False):
                trial = dict(a)
                trial[atom] = value
                try:
                    expand(prog, trial)  # @line L18
                except Conflict:
                    a[atom] = not value  # @line L19
                    expand(prog, a)
                    progress = True
                    break
                sizes.append(len(trial))
            if progress:
                break
            scores[atom] = (min(sizes), max(sizes), sizes[0] >= sizes[1])
        if not progress:
            return scores  # @line L20


def search(prog, a, out, stats, use_lookahead=True, first_only=False):
    """Depth-first search for all stable models that extend a. Append them to out."""
    stats["nodes"] += 1
    try:
        expand(prog, a)  # @line L1
        scores = lookahead(prog, a) if use_lookahead else None
    except Conflict:
        stats["conflicts"] += 1
        return
    if len(a) == len(prog.atoms):  # @line L2
        out.append(frozenset(x for x, v in a.items() if v))
        return
    open_atoms = [x for x in prog.atoms if x not in a]
    if scores:
        atom = max(open_atoms, key=lambda x: scores[x][:2])  # @line L3
        first = scores[atom][2]
    else:
        atom, first = open_atoms[0], True
    for value in (first, not first):  # @line L4
        if first_only and out:
            return
        branch = dict(a)
        branch[atom] = value
        search(prog, branch, out, stats, use_lookahead, first_only)


def stable_models(normal=(), choice=(), constraints=(), use_lookahead=True, stats=None):
    """All stable models of the program, sorted by size and then by content."""
    prog = Program(normal, choice, constraints)
    if stats is None:
        stats = {}
    stats.setdefault("nodes", 0)
    stats.setdefault("conflicts", 0)
    out = []
    search(prog, {}, out, stats, use_lookahead)
    return sorted(out, key=lambda m: (len(m), sorted(m)))


def has_stable_model(normal=(), choice=(), constraints=()):
    """True when the program has a stable model. The search stops at the first one."""
    prog = Program(normal, choice, constraints)
    out = []
    search(prog, {}, out, {"nodes": 0, "conflicts": 0}, True, first_only=True)
    return bool(out)
