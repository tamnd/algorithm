# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-track/. The authors are listed in prov/MRQ8VT.jsonl.

"""Feature tracks from pairwise matches, by union-find.

A feature is a pair (image, index). A match is a pair of features, one in
each of two images, that are thought to show the same 3D point. A track
is a connected component of the match graph, whose nodes are the
features and whose edges are the matches. A track is consistent if no two
of its features are in the same image; an inconsistent track joins two
different points (or one point seen twice in one image) and must be split
or dropped before reconstruction.
"""

from typing import Dict, Hashable, Iterable, List, Tuple

Feature = Tuple[Hashable, int]
Match = Tuple[Feature, Feature]


class DisjointSet:
    """Union-find with path halving and union by size."""

    def __init__(self) -> None:
        self.parent: Dict[Feature, Feature] = {}
        self.size: Dict[Feature, int] = {}

    def add(self, x: Feature) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1

    def find(self, x: Feature) -> Feature:
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: Feature, b: Feature) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def build_tracks(matches: Iterable[Match]) -> List[Tuple[List[Feature], bool]]:
    """Return the tracks as (sorted list of features, consistent), sorted by
    their first feature. Features that appear in no match give no track."""
    ds = DisjointSet()
    for a, b in matches:  # @line L1
        ds.add(a)  # @line L2
        ds.add(b)
        ds.union(a, b)  # @line L3
    groups: Dict[Feature, List[Feature]] = {}
    for f in ds.parent:  # @line L4
        groups.setdefault(ds.find(f), []).append(f)  # @line L5
    tracks = []
    for members in groups.values():  # @line L6
        images = [img for img, _ in members]
        consistent = len(set(images)) == len(images)  # @line L7
        tracks.append((sorted(members, key=repr), consistent))
    tracks.sort(key=lambda t: repr(t[0][0]))
    return tracks  # @line L8


def split_by_image(track: List[Feature]) -> Dict[Hashable, List[int]]:
    """The features of a track, grouped by image."""
    out: Dict[Hashable, List[int]] = {}
    for img, idx in track:
        out.setdefault(img, []).append(idx)
    return out
