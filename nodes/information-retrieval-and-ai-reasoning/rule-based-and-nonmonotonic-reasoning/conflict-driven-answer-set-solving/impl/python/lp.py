# SPDX-License-Identifier: MIT
# Shared helper of the logic program pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Ground normal logic programs, for the logic program pages.

A program is a list of rules (head, pos, neg). The head is an atom, and pos and
neg are tuples of atoms: the rule is head <- pos[0], ..., not neg[0], ....
An atom is any hashable value that can be sorted with the other atoms, for
example a small int or a short string. A rule with pos and neg empty is a fact.
A program with every neg empty is definite.

The functions are the plain definitions, written for clarity and checked by
the tests of each page. The brute force enumerator accepts at most MAX_ATOMS
atoms. The algorithms of the pages live in their own files, not here.
"""

from itertools import combinations

MAX_ATOMS = 12


def atoms(program):
    """The sorted list of the atoms that occur in the program."""
    out = set()
    for head, pos, neg in program:
        out.add(head)
        out.update(pos)
        out.update(neg)
    return sorted(out)


def tp(program, interp):
    """The immediate consequence operator: the heads of the rules whose body is true in the set interp."""
    return frozenset(h for h, pos, neg in program if all(b in interp for b in pos) and not any(c in interp for c in neg))


def least_model(program):
    """The least model of a definite program, as the limit of tp from the empty set."""
    if any(neg for _, _, neg in program):
        raise ValueError("least_model needs a definite program")
    model = frozenset()
    while True:
        nxt = tp(program, model)
        if nxt == model:
            return model
        model = nxt


def reduct(program, m):
    """The Gelfond-Lifschitz reduct of the program by the set m."""
    return [(h, tuple(pos), ()) for h, pos, neg in program if not any(c in m for c in neg)]


def is_stable(program, m):
    """True when m is the least model of the reduct of the program by m."""
    return least_model(reduct(program, m)) == frozenset(m)


def stable_models(program):
    """All stable models, by brute force over every subset of the atoms, sorted by size and then by content."""
    universe = atoms(program)
    if len(universe) > MAX_ATOMS:
        raise ValueError(f"the brute force accepts at most {MAX_ATOMS} atoms")
    found = []
    for k in range(len(universe) + 1):
        for subset in combinations(universe, k):
            if is_stable(program, frozenset(subset)):
                found.append(frozenset(subset))
    return found


def random_program(rng, n_atoms, n_rules, max_pos=2, max_neg=2):
    """A random ground normal program over the atoms 0 .. n_atoms - 1, drawn with the random.Random rng."""
    program = []
    for _ in range(n_rules):
        head = rng.randrange(n_atoms)
        pos = tuple(rng.sample(range(n_atoms), rng.randint(0, min(max_pos, n_atoms))))
        neg = tuple(rng.sample(range(n_atoms), rng.randint(0, min(max_neg, n_atoms))))
        program.append((head, pos, neg))
    return program
