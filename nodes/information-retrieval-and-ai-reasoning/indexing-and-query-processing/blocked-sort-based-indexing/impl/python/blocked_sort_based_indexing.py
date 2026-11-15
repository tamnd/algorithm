# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-sort-based-indexing/. The authors are listed in prov/7YJRVM.jsonl.

import heapq
from typing import Iterable

Triple = tuple[int, int, int]  # (term id, document id, term frequency)


def invert(block: list[tuple[int, int]]) -> list[Triple]:
    """Sort one block of (term id, doc id) pairs and group equal pairs.

    Returns the run: the triples (t, d, f) in increasing order of (t, d), where f
    is the number of times the pair (t, d) occurs in the block. Cost O(m log m)
    for a block of m pairs.
    """
    block.sort()  # @line L8
    run: list[Triple] = []
    for t, d in block:  # @line L9
        if run and run[-1][0] == t and run[-1][1] == d:
            run[-1] = (t, d, run[-1][2] + 1)
        else:
            run.append((t, d, 1))
    return run  # @line L10


def merge_runs(runs: list[list[Triple]], term_of: list[str]) -> dict[str, list[tuple[int, int]]]:
    """Merge sorted runs into one index with a min-heap, as a k-way merge.

    Equal (t, d) keys from two runs, which come from a document cut by a block
    boundary, are joined by adding their frequencies. Returns a map from each
    term to its list of (doc id, tf) in increasing doc id order.
    Cost O(P log k) for P triples in k runs.
    """
    heap: list[tuple[int, int, int, int, int]] = []
    for r, run in enumerate(runs):  # @line L11
        if run:
            t, d, f = run[0]
            heap.append((t, d, r, 0, f))
    heapq.heapify(heap)
    out: list[Triple] = []
    while heap:  # @line L12
        t, d, r, pos, f = heapq.heappop(heap)  # @line L13
        if pos + 1 < len(runs[r]):
            t2, d2, f2 = runs[r][pos + 1]
            heapq.heappush(heap, (t2, d2, r, pos + 1, f2))
        if out and out[-1][0] == t and out[-1][1] == d:  # @line L14
            out[-1] = (t, d, out[-1][2] + f)
        else:
            out.append((t, d, f))  # @line L15
    index: dict[str, list[tuple[int, int]]] = {}
    for t, d, f in out:  # @line L16
        index.setdefault(term_of[t], []).append((d, f))
    return index


def bsbi(docs: Iterable[tuple[int, list[str]]], block_size: int) -> tuple[dict[str, list[tuple[int, int]]], list[list[Triple]]]:
    """Blocked sort-based indexing.

    docs gives (doc id, tokens) in strictly increasing doc id order. block_size is
    M, the number of (term id, doc id) pairs that fit in memory, M >= 1.
    Returns the index (term -> list of (doc id, tf)) and the list of sorted runs
    that the merge read. Cost O(T log M + P log k) time for T tokens, P triples
    in the runs and k = ceil(T / M) runs.
    """
    if block_size < 1:
        raise ValueError("block_size must be at least 1")
    termid: dict[str, int] = {}  # @line L1
    term_of: list[str] = []
    runs: list[list[Triple]] = []
    block: list[tuple[int, int]] = []
    for d, tokens in docs:  # @line L2
        for w in tokens:
            if w not in termid:  # @line L3
                termid[w] = len(term_of)
                term_of.append(w)
            block.append((termid[w], d))  # @line L4
            if len(block) == block_size:  # @line L5
                runs.append(invert(block))
                block = []
    if block:  # @line L6
        runs.append(invert(block))
    return merge_runs(runs, term_of), runs  # @line L7
