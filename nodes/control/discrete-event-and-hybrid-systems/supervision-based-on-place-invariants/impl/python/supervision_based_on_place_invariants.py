# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supervision-based-on-place-invariants/. The authors are listed in prov/131GMK.jsonl.

"""Supervision based on place invariants (Yamalidou, Moody, Lemmon and Antsaklis 1996).

A Petri net has n places and q transitions. Pre[i][t] is the weight of the arc
from place i to transition t, Post[i][t] the weight of the arc from t to i, and
D = Post - Pre is the incidence matrix. A marking mu is a vector of n
nonnegative integers. Transition t is enabled at mu if mu >= Pre[:, t]; firing
it gives mu + D[:, t].

The specification is c linear constraints L mu <= b, with L an integer c by n
matrix and b an integer vector. The supervisor adds one monitor place per
constraint, with incidence D_c = -L D and initial marking mu_c0 = b - L mu0.
Then L mu + mu_c = b is a place invariant of the closed loop, so mu_c >= 0
gives L mu <= b. When every transition is controllable and observable, the
closed loop blocks a firing only if the firing would break a constraint, so it
is maximally permissive.

All arithmetic is on Python integers, so the result is exact.
"""

from collections import deque

__all__ = [
    "incidence",
    "monitor_places",
    "closed_loop",
    "is_admissible",
    "enabled",
    "fire",
    "reachable_markings",
]


def _shape(pre, post):
    n = len(pre)
    if n == 0 or len(post) != n:
        raise ValueError("Pre and Post must have the same number of rows (places)")
    q = len(pre[0])
    for row in list(pre) + list(post):
        if len(row) != q:
            raise ValueError("Pre and Post must have the same number of columns (transitions)")
        for a in row:
            if not isinstance(a, int) or a < 0:
                raise ValueError("arc weights must be nonnegative integers")
    return n, q


def incidence(pre, post):
    """Return D = Post - Pre, an n by q integer matrix."""
    n, q = _shape(pre, post)
    return [[post[i][t] - pre[i][t] for t in range(q)] for i in range(n)]


def monitor_places(pre, post, mu0, L, b):
    """Return (Pre_c, Post_c, mu_c0) for the constraints L mu <= b.

    Pre_c and Post_c are c by q: row j holds the arcs of monitor place j.
    Raise ValueError if the initial marking mu0 breaks a constraint, because
    then no monitor marking can be nonnegative.
    """
    n, q = _shape(pre, post)
    if len(mu0) != n or any(m < 0 for m in mu0):
        raise ValueError("mu0 must hold n nonnegative integers")
    if any(len(row) != n for row in L) or len(b) != len(L):
        raise ValueError("L must be c by n and b must hold c integers")
    c = len(L)
    D = incidence(pre, post)  # @line L1
    Dc = [[-sum(L[j][i] * D[i][t] for i in range(n)) for t in range(q)] for j in range(c)]  # @line L2
    muc0 = [b[j] - sum(L[j][i] * mu0[i] for i in range(n)) for j in range(c)]  # @line L3
    if any(m < 0 for m in muc0):  # @line L4
        raise ValueError("the initial marking breaks the constraint L mu0 <= b")
    pre_c = [[max(0, -Dc[j][t]) for t in range(q)] for j in range(c)]  # @line L5
    post_c = [[max(0, Dc[j][t]) for t in range(q)] for j in range(c)]  # @line L5
    return pre_c, post_c, muc0  # @line L6


def closed_loop(pre, post, mu0, L, b):
    """Return (Pre', Post', mu0') of the plant with the monitor places appended."""
    pre_c, post_c, muc0 = monitor_places(pre, post, mu0, L, b)
    return ([list(r) for r in pre] + pre_c, [list(r) for r in post] + post_c, list(mu0) + muc0)


def is_admissible(pre, post, L, uncontrollable=(), unobservable=()):
    """Check the conditions of Moody and Antsaklis for the monitor of L mu <= b.

    The monitor never needs to block an uncontrollable transition t when
    (L D)[:, t] <= 0, and it never needs to see an unobservable transition t
    when (L D)[:, t] = 0. Return True when both conditions hold.
    """
    n, q = _shape(pre, post)
    D = incidence(pre, post)
    LD = [[sum(row[i] * D[i][t] for i in range(n)) for t in range(q)] for row in L]
    for t in uncontrollable:
        if any(LD[j][t] > 0 for j in range(len(L))):
            return False
    for t in unobservable:
        if any(LD[j][t] != 0 for j in range(len(L))):
            return False
    return True


def enabled(pre, mu, t):
    """True if transition t is enabled at marking mu."""
    return all(mu[i] >= pre[i][t] for i in range(len(pre)))


def fire(pre, post, mu, t):
    """Return the marking after firing the enabled transition t at mu."""
    if not enabled(pre, mu, t):
        raise ValueError("transition is not enabled")
    return tuple(mu[i] - pre[i][t] + post[i][t] for i in range(len(pre)))


def reachable_markings(pre, post, mu0, allowed=None, limit=100000):
    """Breadth-first search of the reachability graph.

    allowed(mu) -> bool restricts the search to markings where it is True (the
    initial marking must be allowed). Return the set of reached markings as
    tuples. Raise RuntimeError if more than limit markings are found, since an
    unbounded net has an infinite reachability set.
    """
    q = len(pre[0])
    start = tuple(mu0)
    if allowed is not None and not allowed(start):
        return set()
    seen = {start}
    todo = deque([start])
    while todo:
        mu = todo.popleft()
        for t in range(q):
            if enabled(pre, mu, t):
                nxt = fire(pre, post, mu, t)
                if nxt not in seen and (allowed is None or allowed(nxt)):
                    seen.add(nxt)
                    if len(seen) > limit:
                        raise RuntimeError("too many markings; the net may be unbounded")
                    todo.append(nxt)
    return seen
