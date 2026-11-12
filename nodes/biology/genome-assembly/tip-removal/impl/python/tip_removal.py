# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tip-removal/. The authors are listed in prov/W7590Z.jsonl.

"""Tip removal in an edge-centric de Bruijn graph, in the style of Velvet.

The graph is given as a map from each k-mer (an edge from its prefix to its
suffix) to its count in the reads. A tip is a unitig that hangs from a
junction and ends in a dead end. It is removed when it has fewer than max_len
edges and its edge at the junction has a smaller count than another edge on
the same side of the junction. Tips are removed one at a time, the one with
the smallest count first, and the unitigs are computed again after each one.
"""


def _degrees(edges: dict[str, int]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    out: dict[str, list[str]] = {}
    inn: dict[str, list[str]] = {}
    for x in sorted(edges):
        out.setdefault(x[:-1], []).append(x)
        inn.setdefault(x[:-1], [])
        inn.setdefault(x[1:], []).append(x)
        out.setdefault(x[1:], [])
    return out, inn


def _unitigs(out: dict[str, list[str]], inn: dict[str, list[str]]) -> list[list[str]]:
    """Return the maximal non-branching paths that start at a non-simple vertex."""

    def simple(v: str) -> bool:
        return len(inn[v]) == 1 and len(out[v]) == 1

    paths = []
    for u in sorted(out):
        if simple(u):
            continue
        for e in out[u]:
            path = [e]
            while simple(path[-1][1:]):
                path.append(out[path[-1][1:]][0])
            paths.append(path)
    return paths  # isolated cycles have no dead end, so they are never tips


def find_tips(counts: dict[str, int], max_len: int) -> list[tuple[int, list[str]]]:
    """Return (count at the junction, path) for each tip that may be removed."""
    out, inn = _degrees(counts)
    tips = []
    for p in _unitigs(out, inn):  # @line L3
        start, end = p[0][:-1], p[-1][1:]
        if len(inn[start]) == 0 and len(inn[end]) >= 2:  # @line L4
            a, others = p[-1], [x for x in inn[end] if x != p[-1]]
        elif len(out[end]) == 0 and len(out[start]) >= 2:  # @line L5
            a, others = p[0], [x for x in out[start] if x != p[0]]
        else:
            continue  # @line L6
        if len(p) < max_len and counts[a] < max(counts[x] for x in others):  # @line L7
            tips.append((counts[a], p))
    return tips


def tip_removal(counts: dict[str, int], k: int, max_len: int | None = None) -> dict[str, int]:
    """Return a copy of counts without the removable tips. The default max_len is 2k edges."""
    if max_len is None:
        max_len = 2 * k
    g = dict(counts)
    while True:  # @line L1
        tips = find_tips(g, max_len)  # @line L2
        if not tips:
            return g  # @line L8
        _, p = min(tips, key=lambda t: (t[0], t[1]))
        for x in p:  # @line L9
            del g[x]
