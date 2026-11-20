# SPDX-License-Identifier: MIT
# Shared helper of the algorithmic game theory pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Preference profiles, majority relations and brute force axiom checkers.

The candidates are 0, ..., m - 1. A ranking is a tuple of all m candidates, best first:
(2, 0, 1) means that 2 is preferred to 0 and 0 to 1. A profile is a tuple of n rankings,
one per voter. An approval ballot is a frozenset of candidates, and an approval profile is
a tuple of n ballots.

A rule is a function rule(profile, m). A resolute rule returns one candidate (an int); a
correspondence returns a nonempty frozenset of candidates. The checkers accept both: they
turn an int w into frozenset({w}).

Each checker takes the rule, m and n, and by default tries every profile of all_profiles(m,
n). Pass profiles= to check a given list of profiles instead (for example approval profiles,
or a random sample when the full domain is too large). Each checker returns None when the
property holds on every profile it tried, and else a counterexample tuple.

There is no voting rule in this module. Every count is an exact integer.
"""

from itertools import permutations, product


# ---------------------------------------------------------------- rankings and profiles


def all_rankings(m):
    """Return the list of the m! rankings of 0, ..., m - 1, in lexicographic order."""
    return list(permutations(range(m)))


def all_profiles(m, n):
    """Yield every profile of n rankings of m candidates: (m!)^n profiles, voters ordered."""
    return product(all_rankings(m), repeat=n)


def random_profile(rng, m, n):
    """Return a profile of n rankings drawn uniformly and independently (impartial culture)."""
    return tuple(tuple(rng.sample(range(m), m)) for _ in range(n))


def position(r, a):
    """Return the position of candidate a in ranking r: 0 for the top."""
    return r.index(a)


def prefers(r, a, b):
    """Return True if ranking r puts a above b."""
    return r.index(a) < r.index(b)


def pairwise(profile, m):
    """Return the m by m matrix N with N[a][b] the number of voters who rank a above b."""
    N = [[0] * m for _ in range(m)]
    for r in profile:
        for i, a in enumerate(r):
            for b in r[i + 1:]:
                N[a][b] += 1
    return N


def margins(profile, m):
    """Return the m by m matrix of margins N[a][b] - N[b][a]."""
    N = pairwise(profile, m)
    return [[N[a][b] - N[b][a] for b in range(m)] for a in range(m)]


def condorcet_winner(profile, m):
    """Return the candidate with a positive margin over every other candidate, or None."""
    M = margins(profile, m)
    for a in range(m):
        if all(M[a][b] > 0 for b in range(m) if b != a):
            return a
    return None


def weak_condorcet_winners(profile, m):
    """Return the frozenset of candidates whose margin over every other candidate is >= 0."""
    M = margins(profile, m)
    return frozenset(a for a in range(m) if all(M[a][b] >= 0 for b in range(m) if b != a))


def kendall_tau(r1, r2):
    """Return the number of pairs of candidates that r1 and r2 order differently."""
    pos = {a: i for i, a in enumerate(r2)}
    seq = [pos[a] for a in r1]
    return sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])


def is_single_peaked_on(profile, axis):
    """Return True if every ranking of the profile is single-peaked on the axis.

    axis is a tuple of all candidates, left to right. A ranking is single-peaked on the axis
    exactly when, for each k, its k best candidates form a contiguous block of the axis.
    """
    where = {a: i for i, a in enumerate(axis)}
    for r in profile:
        lo = hi = where[r[0]]
        for a in r[1:]:
            p = where[a]
            if p == lo - 1:
                lo = p
            elif p == hi + 1:
                hi = p
            else:
                return False
    return True


def lex_tiebreak(candidates):
    """Return the candidate with the smallest index: the default tie-breaking rule."""
    return min(candidates)


def random_approval_profile(rng, m, n, p):
    """Return n approval ballots; each voter approves each candidate with probability p."""
    return tuple(frozenset(a for a in range(m) if rng.random() < p) for _ in range(n))


def permute_profile(profile, pi):
    """Rename the candidates: candidate a becomes pi[a]. Works for rankings and approval ballots."""
    out = []
    for ballot in profile:
        if isinstance(ballot, (set, frozenset)):
            out.append(frozenset(pi[a] for a in ballot))
        else:
            out.append(tuple(pi[a] for a in ballot))
    return tuple(out)


# ---------------------------------------------------------------- axiom checkers


def _as_set(result):
    if isinstance(result, (set, frozenset)):
        return frozenset(result)
    return frozenset([result])


def _domain(m, n, profiles):
    return all_profiles(m, n) if profiles is None else profiles


def _candidate_generators(m):
    """A transposition and an m-cycle: together they generate every permutation of the candidates."""
    gens = []
    if m >= 2:
        swap = list(range(m))
        swap[0], swap[1] = 1, 0
        gens.append(tuple(swap))
    if m >= 3:
        gens.append(tuple((a + 1) % m for a in range(m)))
    return gens


def check_anonymity(rule, m, n, profiles=None):
    """Check that permuting the voters does not change the result.

    It tries the swap of voters 0 and 1 and the cyclic shift of the voters. These generate all
    permutations, so on the full domain this is a complete test. Returns None or
    (profile, permuted_profile).
    """
    for P in _domain(m, n, profiles):
        P = tuple(P)
        if len(P) < 2:
            continue
        base = _as_set(rule(P, m))
        others = [(P[1], P[0]) + P[2:], P[1:] + P[:1]]
        for Q in others:
            if _as_set(rule(Q, m)) != base:
                return (P, Q)
    return None


def check_neutrality(rule, m, n, profiles=None):
    """Check that renaming the candidates by pi renames the result by pi.

    It tries a transposition and an m-cycle of the candidates, which generate all permutations.
    A resolute rule with a fixed tie-breaking order usually fails this test; test its
    correspondence instead. Returns None or (profile, pi).
    """
    gens = _candidate_generators(m)
    for P in _domain(m, n, profiles):
        P = tuple(P)
        base = _as_set(rule(P, m))
        for pi in gens:
            if _as_set(rule(permute_profile(P, pi), m)) != frozenset(pi[a] for a in base):
                return (P, pi)
    return None


def check_pareto(rule, m, n, profiles=None):
    """Check that no candidate b wins when every voter ranks some a above b.

    Returns None or (profile, a, b).
    """
    for P in _domain(m, n, profiles):
        P = tuple(P)
        W = _as_set(rule(P, m))
        N = pairwise(P, m)
        for b in W:
            for a in range(m):
                if a != b and N[a][b] == len(P):
                    return (P, a, b)
    return None


def check_condorcet_consistency(rule, m, n, profiles=None):
    """Check that a Condorcet winner, when one exists, is the unique winner.

    Returns None or (profile, condorcet_winner).
    """
    for P in _domain(m, n, profiles):
        P = tuple(P)
        c = condorcet_winner(P, m)
        if c is not None and _as_set(rule(P, m)) != frozenset([c]):
            return (P, c)
    return None


def _raise_once(r, w):
    """Return r with w moved up one place, or None if w is already on top."""
    i = r.index(w)
    if i == 0:
        return None
    s = list(r)
    s[i - 1], s[i] = s[i], s[i - 1]
    return tuple(s)


def check_monotonicity(rule, m, n, profiles=None):
    """Check that a winner stays a winner when one voter moves it up one place.

    Every raise of w, with no other change in the relative order of the others, is a chain of
    such one-place moves, so on the full domain this is a complete test. For a correspondence
    the test is that w stays in the winning set. Returns None or (profile, raised_profile, w).
    """
    for P in _domain(m, n, profiles):
        P = tuple(P)
        for w in _as_set(rule(P, m)):
            for i, r in enumerate(P):
                s = _raise_once(r, w)
                if s is None:
                    continue
                Q = P[:i] + (s,) + P[i + 1:]
                if w not in _as_set(rule(Q, m)):
                    return (P, Q, w)
    return None


def find_manipulation(rule, m, n, profiles=None):
    """Search for a voter who gets a strictly better winner by a false ranking.

    The rule must be resolute (a correspondence must return one winner on every profile it
    is called on). Returns None or (profile, voter, false_ranking): with the false ranking in
    place of the voter's true one, the winner is one that the true ranking strictly prefers.
    """
    rankings = all_rankings(m)
    for P in _domain(m, n, profiles):
        P = tuple(P)
        w = _single(rule(P, m))
        for i, r in enumerate(P):
            if r[0] == w:
                continue
            for s in rankings:
                if s == r:
                    continue
                Q = P[:i] + (s,) + P[i + 1:]
                if prefers(r, _single(rule(Q, m)), w):
                    return (P, i, s)
    return None


def _single(result):
    W = _as_set(result)
    if len(W) != 1:
        raise ValueError("find_manipulation needs a resolute rule")
    return next(iter(W))
