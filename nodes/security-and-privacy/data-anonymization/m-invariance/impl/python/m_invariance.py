# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/m-invariance/. The authors are listed in prov/DJ2GGT.jsonl.

from collections.abc import Hashable, Sequence

# A release is a list of QI groups. A group is a list of (record id, sensitive value)
# pairs, and a counterfeit tuple has the record id None.
Group = Sequence[tuple[Hashable | None, Hashable]]
Release = Sequence[Group]


def signature(group: Group) -> frozenset[Hashable]:
    """Return the set of distinct sensitive values in a group. Cost: O(|group|)."""
    return frozenset(v for _, v in group)


def is_m_unique(release: Release, m: int) -> bool:
    """Return True if every group has at least m tuples, all with different sensitive values.

    Counterfeit tuples count as tuples. Cost: O(number of tuples in the release).
    """
    for group in release:
        if len(group) < m or len(signature(group)) != len(group):
            return False
    return True


def is_m_invariant(releases: Sequence[Release], m: int) -> bool:
    """Return True if the sequence of releases T*(1), ..., T*(n) is m-invariant.

    Precondition: m >= 1, each record id occurs at most once per release, and the
    releases that contain a record are consecutive (its lifespan). Raises ValueError
    if a record occurs twice in one release.
    Cost: O(N s) expected time with hashing, where N is the total number of tuples
    over all releases and s is the largest group size (one signature comparison
    per tuple).
    """
    sig_of: dict[Hashable, frozenset[Hashable]] = {}  # @line L1
    for release in releases:  # @line L2
        seen: set[Hashable] = set()
        for group in release:  # @line L3
            if len(group) < m or len(signature(group)) != len(group):  # @line L4
                return False
            sig = signature(group)  # @line L5
            for rid, _ in group:  # @line L6
                if rid is None:
                    continue
                if rid in seen:
                    raise ValueError("a record occurs twice in one release")
                seen.add(rid)
                if rid in sig_of and sig_of[rid] != sig:  # @line L7
                    return False
                sig_of[rid] = sig  # @line L8
    return True  # @line L9


def extends_m_invariant(previous: Release, current: Release, m: int) -> bool:
    """Lemma 4 of Xiao and Tao: the incremental test for one more release.

    Given that the releases up to `previous` are m-invariant, the sequence with
    `current` appended is m-invariant exactly when `current` is m-unique and every
    record in both releases has hosting groups with the same signature.
    Precondition: lifespans are consecutive, as in is_m_invariant.
    Cost: O((|previous| + |current|) s) expected time, s the largest group size.
    """
    if not is_m_unique(current, m):
        return False
    before = {rid: signature(g) for g in previous for rid, _ in g if rid is not None}
    for group in current:
        sig = signature(group)
        for rid, _ in group:
            if rid is not None and rid in before and before[rid] != sig:
                return False
    return True


def counterfeits(release: Release) -> list[tuple[int, int]]:
    """Return the auxiliary relation R(j): (group index, number of counterfeits) for each group with any.

    Groups are numbered from 1 in the order given. Cost: O(number of tuples).
    """
    out = []
    for i, group in enumerate(release, start=1):
        c = sum(1 for rid, _ in group if rid is None)
        if c > 0:
            out.append((i, c))
    return out
