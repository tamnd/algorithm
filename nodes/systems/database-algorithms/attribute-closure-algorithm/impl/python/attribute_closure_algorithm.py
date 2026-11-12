# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attribute-closure-algorithm/. The authors are listed in prov/VZN265.jsonl.

"""The closure X+ of a set of attributes X under a set F of functional dependencies.

linear_closure is the algorithm of Beeri and Bernstein (1979): one counter for
each FD and one list of FDs for each attribute, so each attribute occurrence in
F is looked at a constant number of times. naive_closure is the plain fixpoint
loop, kept as the reference that the tests compare against.

An FD is a pair (lhs, rhs) of frozensets of attribute names.
"""

from collections import deque
from collections.abc import Hashable, Iterable, Sequence

FD = tuple[frozenset, frozenset]


def fd(lhs: Iterable[Hashable], rhs: Iterable[Hashable]) -> FD:
    """Build an FD. fd("AB", "C") is AB -> C when the attributes are letters."""
    return (frozenset(lhs), frozenset(rhs))


def linear_closure(fds: Sequence[FD], x: Iterable[Hashable], stats: dict | None = None) -> frozenset:
    """Return X+ under fds in time linear in |X| plus the total size of fds.

    If stats is a dict, the counts of queue pushes and counter decrements are
    stored in it, so that a test can check the linear bound.
    """
    count = [len(lhs) for lhs, _ in fds]  # @line L1
    users: dict[Hashable, list[int]] = {}
    for i, (lhs, _) in enumerate(fds):  # @line L2
        for a in lhs:
            users.setdefault(a, []).append(i)
    closure = set(x)  # @line L3
    queue = deque(closure)
    pushes, decrements = len(closure), 0

    def add(rhs: frozenset) -> None:
        nonlocal pushes
        for b in rhs:  # @line L11
            if b not in closure:  # @line L12
                closure.add(b)
                queue.append(b)
                pushes += 1

    for i, (_, rhs) in enumerate(fds):  # @line L4
        if count[i] == 0:
            add(rhs)
    while queue:  # @line L5
        a = queue.popleft()  # @line L6
        for i in users.get(a, ()):  # @line L7
            count[i] -= 1  # @line L8
            decrements += 1
            if count[i] == 0:  # @line L9
                add(fds[i][1])
    if stats is not None:
        stats["pushes"] = pushes
        stats["decrements"] = decrements
    return frozenset(closure)  # @line L10


def naive_closure(fds: Sequence[FD], x: Iterable[Hashable], stats: dict | None = None) -> frozenset:
    """Return X+ by the plain fixpoint: scan F until a full pass adds nothing."""
    closure = set(x)
    passes = 0
    changed = True
    while changed:
        changed = False
        passes += 1
        for lhs, rhs in fds:
            if lhs <= closure and not rhs <= closure:
                closure |= rhs
                changed = True
    if stats is not None:
        stats["passes"] = passes
    return frozenset(closure)


def semantic_closure(universe: Iterable[Hashable], fds: Sequence[FD], x: Iterable[Hashable]) -> frozenset:
    """Return the set of attributes A such that F implies X -> A, by brute force.

    F implies X -> A if and only if each two-tuple relation that satisfies F
    and whose tuples agree on X also has its tuples agree on A. A two-tuple
    relation is given by its agree set S, and it satisfies V -> W if and only
    if V is not a subset of S or W is a subset of S. Exponential in |U|.
    """
    u = sorted(set(universe), key=repr)
    xs = frozenset(x)
    result = set(u)
    for mask in range(1 << len(u)):
        s = frozenset(u[i] for i in range(len(u)) if mask >> i & 1)
        if xs <= s and all(not lhs <= s or rhs <= s for lhs, rhs in fds):
            result &= s
    return frozenset(result)
