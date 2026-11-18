# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-swoosh/. The authors are listed in prov/92B1R4.jsonl.
"""R-Swoosh: generic entity resolution with black-box match and merge functions.

match(r, s) returns a bool and merge(r, s) returns a new record; merge is called
only on records that match. When the two functions have the ICAR properties
(idempotence, commutativity, associativity, representativity), the result is
the set of maximal records of the merge closure of the input.

The module also has a record type for tests and examples: a record is a pair
(values, ids), where values is a frozenset of (attribute, value) pairs and ids
is the frozenset of input record numbers merged into it. union_merge and
rule_match below have the ICAR properties.
"""

from collections import deque


def r_swoosh(records, match, merge):
    """Return (resolved records, number of match calls)."""
    R = deque(records)  # @line L1
    done = []  # @line L1
    calls = 0
    while R:  # @line L2
        r = R.popleft()  # @line L3
        buddy = None  # @line L4
        for k, other in enumerate(done):  # @line L5
            calls += 1
            if match(r, other):  # @line L6
                buddy = k  # @line L6
                break  # @line L6
        if buddy is None:  # @line L7
            done.append(r)  # @line L7
        else:
            other = done.pop(buddy)  # @line L8
            R.append(merge(r, other))  # @line L8
    return done, calls  # @line L9


def comparison_bound(n, j):
    """The worst case number of match calls for n inputs and j outputs: (n-1)^2 - (j-1)(j-2)/2."""
    if n == 0:
        return 0
    return (n - 1) ** 2 - (j - 1) * (j - 2) // 2


def make_record(i, **fields):
    """A record with the input number i and the given attribute values (None means missing)."""
    values = frozenset((a, v) for a, v in fields.items() if v is not None)
    return (values, frozenset([i]))


def union_merge(r, s):
    """Merge by union of the values and of the input numbers."""
    return (r[0] | s[0], r[1] | s[1])


def shares(r, s, attr):
    vr = {v for a, v in r[0] if a == attr}
    return any((attr, v) in s[0] for v in vr)


def rule_match(r, s):
    """Match if the records share an email, or share both a name and a phone."""
    return shares(r, s, "email") or (shares(r, s, "name") and shares(r, s, "phone"))


def dominated(r, s, match, merge):
    """r <= s: r matches s and merging r into s gives s."""
    return match(r, s) and merge(r, s) == s


def merge_closure(records, match, merge, limit=100000):
    """The smallest set that holds the input and is closed under merges of matching records."""
    S = set(records)
    frontier = list(S)
    while frontier:
        new = []
        items = sorted(S, key=repr)
        for x in frontier:
            for y in items:
                if x != y and match(x, y):
                    z = merge(x, y)
                    if z not in S:
                        S.add(z)
                        new.append(z)
                        if len(S) > limit:
                            raise ValueError("closure too large")
        items = None
        frontier = new
    return S


def maximal_records(records, match, merge):
    """ER(I) under ICAR: the records of the merge closure that no other record dominates."""
    S = merge_closure(records, match, merge)
    return {x for x in S if not any(y != x and dominated(x, y, match, merge) for y in S)}
