# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-bruijn-assembly/. The authors are listed in prov/0WN504.jsonl.

"""De Bruijn graph assembly of error-free or filtered reads on one strand.

The graph is edge-centric: the vertices are the (k-1)-mers and each distinct
k-mer x is one edge from x[:-1] to x[1:]. The contigs are the strings spelled
by the maximal non-branching paths (the unitigs) of the graph.
"""

from collections.abc import Callable


def count_kmers(reads: list[str], k: int) -> dict[str, int]:
    """Return the number of occurrences of each k-mer in the reads."""
    counts: dict[str, int] = {}
    for r in reads:  # @line L2
        for i in range(len(r) - k + 1):  # @line L3
            x = r[i : i + k]
            counts[x] = counts.get(x, 0) + 1
    return counts


def build_graph(kmers: list[str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Return (out, inn): for each vertex, the sorted k-mers that leave it and enter it."""
    out: dict[str, list[str]] = {}
    inn: dict[str, list[str]] = {}
    for x in sorted(set(kmers)):  # @line L5
        u, v = x[:-1], x[1:]
        out.setdefault(u, []).append(x)
        inn.setdefault(u, [])
        inn.setdefault(v, []).append(x)
        out.setdefault(v, [])
    return out, inn


def unitig_paths(kmers: list[str]) -> list[list[str]]:
    """Return the maximal non-branching paths of the graph, as lists of k-mers.

    Each k-mer is in exactly one path. A path starts at an edge whose tail is
    not a vertex with in-degree 1 and out-degree 1; a cycle of such vertices
    is returned as one path that starts at its smallest k-mer.
    """
    out, inn = build_graph(kmers)

    def simple(v: str) -> bool:
        return len(inn[v]) == 1 and len(out[v]) == 1

    used: set[str] = set()
    paths: list[list[str]] = []
    for u in sorted(out):  # @line L7
        if simple(u):
            continue
        for e in out[u]:  # @line L8
            path = [e]
            used.add(e)
            w = e[1:]
            while simple(w):  # @line L9
                e = out[w][0]
                path.append(e)
                used.add(e)
                w = e[1:]
            paths.append(path)
    for e in sorted(set(kmers)):  # @line L10
        if e in used:
            continue
        start = e  # e lies on an isolated cycle
        path = [e]
        used.add(e)
        w = e[1:]
        while out[w][0] != start:
            e = out[w][0]
            path.append(e)
            used.add(e)
            w = e[1:]
        paths.append(path)
    return paths


def spell(path: list[str]) -> str:
    """Return the string spelled by a walk given as its list of k-mers."""
    return path[0] + "".join(x[-1] for x in path[1:])


def de_bruijn_assembly(
    reads: list[str],
    k: int,
    min_count: int = 1,
    simplify: Callable[[list[str]], list[str]] | None = None,
) -> list[str]:
    """Return the contigs (unitig strings) of the reads, in sorted order.

    Only the k-mers that occur at least min_count times are kept. With
    min_count = 1 and error-free reads, every k-mer of the reads is kept.
    If simplify is given, it maps the kept k-mers to the k-mers of the
    simplified graph, for example by tip removal or bubble popping.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    counts = count_kmers(reads, k)  # @line L1
    solid = [x for x, c in counts.items() if c >= min_count]  # @line L4
    if simplify is not None:
        solid = simplify(solid)  # @line L6
    return sorted(spell(p) for p in unitig_paths(solid))  # @line L11
