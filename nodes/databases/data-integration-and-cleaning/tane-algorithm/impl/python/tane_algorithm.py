# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tane-algorithm/. The authors are listed in prov/HRXFKG.jsonl.
"""TANE: levelwise discovery of the minimal functional dependencies of a relation.

A relation is a list of rows, each row a tuple of hashable values, and the
attributes are the column numbers 0 .. k - 1. An attribute set is a frozenset of
column numbers. A dependency is a pair (X, A) that stands for X -> A, with A not
in X. The function tane returns the minimal non-trivial dependencies in sorted
order. With eps > 0 it returns the minimal approximate dependencies, those with
a g3 error of at most eps.

The error e(X) of the page is the integer ||p|| - |p| of the stripped
partition p of X: the number of tuples in its classes minus the number of
classes. The paper divides it by |r|; the integer form also works for |r| = 0.
"""

from fractions import Fraction


def single_partition(rows, a):
    """The stripped partition of the one attribute a: classes of size >= 2."""
    groups = {}
    for t, row in enumerate(rows):
        groups.setdefault(row[a], []).append(t)
    return [g for g in groups.values() if len(g) > 1]


def partition_of(rows, attrs):
    """The stripped partition of a set of attributes, computed from the rows."""
    order = sorted(attrs)
    groups = {}
    for t, row in enumerate(rows):
        groups.setdefault(tuple(row[a] for a in order), []).append(t)
    return [g for g in groups.values() if len(g) > 1]


def stripped_product(p1, p2, n):
    """The stripped partition of X union Y from those of X and Y, in linear time."""
    owner = [None] * n
    for i, c in enumerate(p1):
        for t in c:
            owner[t] = i
    bucket = [[] for _ in p1]
    out = []
    for c in p2:
        for t in c:
            if owner[t] is not None:
                bucket[owner[t]].append(t)
        for t in c:
            i = owner[t]
            if i is not None:
                if len(bucket[i]) >= 2:
                    out.append(bucket[i])
                bucket[i] = []
    return out


def error_count(p):
    """e(X) as an integer: ||p|| - |p|. It is 0 if and only if X is a superkey."""
    return sum(len(c) for c in p) - len(p)


def g3_count(p_lhs, p_both):
    """The least number of tuples to delete so that X -> A holds (g3 times |r|)."""
    size = {}
    for c in p_both:
        for t in c:
            size[t] = len(c)
    removed = 0
    for c in p_lhs:
        removed += len(c) - max(size.get(t, 1) for t in c)
    return removed


def tane(rows, k, eps=0, key_pruning=None):
    """Return the sorted list of minimal dependencies (X, A) of the relation.

    Key pruning (lines L15 to L17) is on for exact dependencies only. With
    eps > 0 it can lose minimal approximate dependencies, so it is off by
    default; pass key_pruning=True to get the literal version of the paper.
    """
    n = len(rows)
    R = frozenset(range(k))
    limit = Fraction(eps) * n
    exact = eps == 0
    if key_pruning is None:
        key_pruning = exact
    part = {frozenset(): [list(range(n))] if n >= 2 else []}  # @line L1
    cplus = {frozenset(): R}  # @line L1
    singles = {a: single_partition(rows, a) for a in range(k)}
    for a in range(k):
        part[frozenset([a])] = singles[a]  # @line L2
    level = [frozenset([a]) for a in range(k)]  # @line L2
    fds = []

    def get_part(Y):
        if Y not in part:
            base = max(Y)
            part[Y] = stripped_product(get_part(Y - {base}), singles[base], n)
        return part[Y]

    def holds(lhs, a):
        both = lhs | {a}
        if exact:
            return error_count(get_part(lhs)) == error_count(get_part(both))
        return g3_count(get_part(lhs), get_part(both)) <= limit

    ell = 1  # @line L3
    while level:  # @line L4
        # COMPUTE-DEPENDENCIES
        for X in level:  # @line L5
            c = R
            for a in X:
                c = c & cplus[X - {a}]  # @line L8
            cplus[X] = c
        for X in level:
            for a in sorted(X & cplus[X]):  # @line L9
                if holds(X - {a}, a):  # @line L10
                    fds.append((X - {a}, a))  # @line L11
                    cplus[X] = cplus[X] - {a}  # @line L12
                    if exact or error_count(part[X - {a}]) == error_count(part[X]):
                        cplus[X] = cplus[X] - (R - X)  # @line L12
        # PRUNE
        kept = []
        for X in level:  # @line L6
            if not cplus[X]:  # @line L13
                continue  # @line L14
            if key_pruning and error_count(part[X]) == 0:  # @line L15
                for a in sorted(cplus[X] - X):
                    ok = True
                    for b in sorted(X):
                        Y = (X - {b}) | {a}
                        if Y in cplus:
                            inside = a in cplus[Y]  # @line L16
                        else:
                            # Y was never generated; then a is in C+(Y) exactly
                            # when X - {b} -> a fails (see the Pitfalls section).
                            inside = not holds(X - {b}, a)  # @line L16
                        if not inside:
                            ok = False
                            break
                    if ok:
                        fds.append((X, a))  # @line L16
                continue  # @line L17
            kept.append(X)
        # GENERATE-NEXT-LEVEL
        kept_set = set(kept)
        blocks = {}
        for X in sorted(tuple(sorted(X)) for X in kept):
            blocks.setdefault(X[:-1], []).append(X)
        nxt = []
        for prefix in sorted(blocks):  # @line L7
            block = blocks[prefix]
            for i in range(len(block)):
                for j in range(i + 1, len(block)):  # @line L18
                    Y, Z = frozenset(block[i]), frozenset(block[j])
                    X = Y | Z  # @line L19
                    if all(X - {a} in kept_set for a in X):  # @line L19
                        part[X] = stripped_product(part[Y], part[Z], n)  # @line L19
                        nxt.append(X)
        level = nxt  # @line L7
        ell += 1  # @line L7
    return sorted(fds, key=lambda d: (len(d[0]), sorted(d[0]), d[1]))


def format_fd(fd, names=None):
    """Write (X, A) as a string such as 'AB -> C'."""
    lhs, a = fd
    if names is None:
        names = [chr(ord("A") + i) for i in range(max(list(lhs) + [a]) + 1)]
    left = "".join(names[i] for i in sorted(lhs)) or "{}"
    return left + " -> " + names[a]
