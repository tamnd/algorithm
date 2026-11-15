# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-pass-in-memory-indexing/. The authors are listed in prov/8P8GD3.jsonl.

import heapq
from typing import Iterable

Postings = list[tuple[int, int]]  # (document id, term frequency), increasing ids
Block = list[tuple[str, Postings]]  # (term, postings), increasing terms


def write_block(dictionary: dict[str, Postings]) -> Block:
    """Sort the terms of one block and return the block as it goes to disk. Cost O(v log v) for v terms."""
    return [(w, dictionary[w]) for w in sorted(dictionary)]  # @line L11


def merge_blocks(blocks: list[Block]) -> dict[str, Postings]:
    """Merge blocks by term with a min-heap keyed on (term, block number).

    The lists of one term come out in block order, which is document order.
    If a block boundary cut a document, the first posting of the later list
    has the same id as the last posting of the earlier one, and the two
    frequencies are added. Cost O(v log k + P) for v block terms, k blocks and
    P postings.
    """
    heap: list[tuple[str, int, int]] = []
    for i, block in enumerate(blocks):  # @line L12
        if block:
            heap.append((block[0][0], i, 0))
    heapq.heapify(heap)
    out: list[tuple[str, Postings]] = []
    while heap:  # @line L13
        w, i, pos = heapq.heappop(heap)  # @line L14
        if pos + 1 < len(blocks[i]):
            heapq.heappush(heap, (blocks[i][pos + 1][0], i, pos + 1))
        plist = blocks[i][pos][1]
        if out and out[-1][0] == w:  # @line L15
            acc = out[-1][1]
            start = 0
            if acc[-1][0] == plist[0][0]:
                acc[-1] = (acc[-1][0], acc[-1][1] + plist[0][1])
                start = 1
            acc.extend(plist[start:])
        else:
            out.append((w, list(plist)))  # @line L16
    return dict(out)  # @line L17


def spimi(docs: Iterable[tuple[int, list[str]]], block_size: int) -> tuple[dict[str, Postings], list[Block]]:
    """Single-pass in-memory indexing.

    docs gives (doc id, tokens) in strictly increasing doc id order. block_size
    is M, the number of tokens that one block may take in before it is written,
    M >= 1. Returns the index (term -> list of (doc id, tf)) and the blocks that
    the merge read. Cost O(T) expected time for the inversion of T tokens, plus
    the sort of the terms of each block and the merge.
    """
    if block_size < 1:
        raise ValueError("block_size must be at least 1")
    blocks: list[Block] = []  # @line L1
    dictionary: dict[str, Postings] = {}
    used = 0
    for d, tokens in docs:  # @line L2
        for w in tokens:
            if w not in dictionary:  # @line L3
                dictionary[w] = []
            plist = dictionary[w]  # @line L4
            if plist and plist[-1][0] == d:  # @line L5
                plist[-1] = (d, plist[-1][1] + 1)
            else:
                plist.append((d, 1))  # @line L6
            used += 1  # @line L7
            if used == block_size:  # @line L8
                blocks.append(write_block(dictionary))
                dictionary = {}
                used = 0
    if dictionary:  # @line L9
        blocks.append(write_block(dictionary))
    return merge_blocks(blocks), blocks  # @line L10
