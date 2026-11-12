# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canopy-clustering/. The authors are listed in prov/3X6R9R.jsonl.

"""Canopy clustering (McCallum, Nigam and Ungar): cover the data with
overlapping canopies using a cheap distance and two thresholds T1 > T2, then
compare with the expensive distance only the pairs that share a canopy."""


def canopies(points, cheap, t1, t2, rng):
    """Return a list of (center index, sorted member indices).

    A point joins the canopy of a center when its cheap distance is below
    t1; it can no longer become a center when its cheap distance is below
    t2. rng is a random.Random used to pick the centers.
    """
    if not t1 > t2 > 0:
        raise ValueError("need t1 > t2 > 0")
    candidates = set(range(len(points)))  # @line L1
    out = []
    while candidates:  # @line L2
        c = rng.choice(sorted(candidates))  # @line L3
        members = []
        for j, p in enumerate(points):
            dj = cheap(points[c], p)
            if dj < t1:  # @line L4
                members.append(j)
            if dj < t2:  # @line L5
                candidates.discard(j)
        candidates.discard(c)
        out.append((c, members))
    return out


def candidate_pairs(canopy_list):
    """Pairs (i, j) with i < j that share at least one canopy: only these
    are compared with the expensive distance."""
    pairs = set()
    for _, members in canopy_list:
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                pairs.add((members[a], members[b]))
    return pairs


def canopy_single_link(points, cheap, expensive, t1, t2, threshold, rng):
    """A second stage: join two points when they share a canopy and their
    expensive distance is at most threshold, and return the connected
    groups (single linkage cut at threshold, inside the canopies)."""
    cl = canopies(points, cheap, t1, t2, rng)
    parent = list(range(len(points)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in sorted(candidate_pairs(cl)):
        if expensive(points[i], points[j]) <= threshold:  # @line L6
            parent[find(i)] = find(j)
    groups = {}
    for i in range(len(points)):
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values())
