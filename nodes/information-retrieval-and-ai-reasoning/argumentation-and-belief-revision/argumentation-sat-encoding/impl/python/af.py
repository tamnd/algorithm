# SPDX-License-Identifier: MIT
# Shared helper of the argumentation pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Finite abstract argumentation frameworks, for the argumentation pages.

A framework is a pair (args, attacks). args is a set of arguments, and attacks
is a set of pairs (a, b), read "a attacks b", with a and b in args. An argument
is any hashable value that sorts with the other arguments, for example a small
int or a short string. A self-attack (a, a) is allowed.

The functions are the plain definitions of Dung (1995), Caminada (2006) and
Baroni, Caminada and Giacomin (2018), written for clarity and checked by the
tests of each page. The enumerators look at all 2^n subsets of the arguments,
so they accept at most MAX_ARGS arguments. The algorithms of the pages live in
their own files, not here.
"""

from itertools import combinations

MAX_ARGS = 10


def check_framework(args, attacks):
    """Raise ValueError when an attack names an argument that is not in args."""
    for a, b in attacks:
        if a not in args or b not in args:
            raise ValueError(f"attack {(a, b)!r} names an argument outside args")


def attackers(attacks, a):
    """The set of the arguments that attack a."""
    return frozenset(x for x, y in attacks if y == a)


def attacked_by(attacks, s):
    """The set S+ of the arguments that some member of s attacks."""
    return frozenset(y for x, y in attacks if x in s)


def range_of(attacks, s):
    """The range S u S+ of the set s."""
    return frozenset(s) | attacked_by(attacks, s)


def conflict_free(attacks, s):
    """True when no member of s attacks a member of s."""
    return not any(x in s and y in s for x, y in attacks)


def defends(attacks, s, a):
    """True when s attacks every attacker of a (a is acceptable with respect to s)."""
    hit = attacked_by(attacks, s)
    return all(b in hit for b in attackers(attacks, a))


def characteristic(args, attacks, s):
    """The characteristic function F(s): the set of the arguments that s defends."""
    hit = attacked_by(attacks, s)
    return frozenset(a for a in args if all(b in hit for b in attackers(attacks, a)))


def is_admissible(args, attacks, s):
    """Conflict-free, and s defends each of its members."""
    return conflict_free(attacks, s) and frozenset(s) <= characteristic(args, attacks, s)


def is_complete(args, attacks, s):
    """Conflict-free, and s is a fixed point of the characteristic function."""
    return conflict_free(attacks, s) and frozenset(s) == characteristic(args, attacks, s)


def is_stable(args, attacks, s):
    """Conflict-free, and s attacks every argument outside s."""
    return conflict_free(attacks, s) and range_of(attacks, s) == frozenset(args)


def subsets(args):
    """All subsets of args as frozensets, smallest first. At most MAX_ARGS arguments."""
    items = sorted(args)
    if len(items) > MAX_ARGS:
        raise ValueError(f"brute force accepts at most {MAX_ARGS} arguments")
    for k in range(len(items) + 1):
        for c in combinations(items, k):
            yield frozenset(c)


def _maximal(sets):
    """The members of sets that are maximal under set inclusion."""
    return [s for s in sets if not any(s < t for t in sets)]


def _key(s):
    return (len(s), sorted(s))


def admissible_sets(args, attacks):
    return sorted((s for s in subsets(args) if is_admissible(args, attacks, s)), key=_key)


def complete_extensions(args, attacks):
    return sorted((s for s in subsets(args) if is_complete(args, attacks, s)), key=_key)


def grounded_extension(args, attacks):
    """The complete extension that is a subset of every complete extension."""
    comp = complete_extensions(args, attacks)
    least = [s for s in comp if all(s <= t for t in comp)]
    assert len(least) == 1
    return least[0]


def preferred_extensions(args, attacks):
    """The admissible sets that are maximal under set inclusion."""
    return sorted(_maximal(admissible_sets(args, attacks)), key=_key)


def stable_extensions(args, attacks):
    return sorted((s for s in subsets(args) if is_stable(args, attacks, s)), key=_key)


def semi_stable_extensions(args, attacks):
    """The complete extensions whose range is maximal under set inclusion."""
    comp = complete_extensions(args, attacks)
    rng = {s: range_of(attacks, s) for s in comp}
    return sorted((s for s in comp if not any(rng[s] < rng[t] for t in comp)), key=_key)


def labelling(args, attacks, s):
    """The labelling of the set s: in for s, out for S+, undec for the rest."""
    hit = attacked_by(attacks, s)
    return {a: "in" if a in s else "out" if a in hit else "undec" for a in args}
