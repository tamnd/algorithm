---
tag: C42FG6
kind: data-structure
slug: slotted-page
name: Slotted page
aliases:
- slotted page layout
- slot directory
area: databases/storage-and-indexing
level: intro
summary: "A page layout that keeps an array of slots at one end and variable-length records at the other. A record id is (page, slot), so records can move inside the page."
model: word-ram
complexity:
  vars: {n: the number of slots in the directory, p: the page size in bytes, r: the length of the record}
  time: {worst: "O(n log n + p)", best: "O(1)"}
  space: {extra: "O(n)"}
prereqs: [relational-model]
see_also: [heap-file, buffer-pool, n-ary-storage-model, pax-page-layout, b-plus-tree, compaction, free-list, write-ahead-logging]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: "Chapter 9 (storing data: disks and files), the sections on page formats for fixed-length and variable-length records"
  - paper: "Joseph M. Hellerstein, Michael Stonebraker and James Hamilton, Architecture of a database system, Foundations and Trends in Databases 1(2), 2007, 141 to 259"
    title: Architecture of a database system
    locator: the section on storage management
  - book: isbn:9781492040347
    title: Alex Petrov, Database Internals, O'Reilly (2019)
    locator: the chapter on file formats, the section on slotted pages and cell layout
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann (1993)
    locator: the chapter on the tuple-oriented file system, page and tuple layout
  - url: https://www.postgresql.org/docs/current/storage-page-layout.html
    title: "PostgreSQL documentation, Database page layout"
    locator: the page header, the array of item identifiers and the tuples at the end of the page
---

A slotted page stores variable-length records in a fixed-size page. A small header and an array of slots grow from the start of the page, and the records grow from the end toward them, so the free space is one gap in the middle. Each slot holds the offset and the length of one record. Other parts of the system name a record by its record id, the pair (page id, slot number), and never by its byte offset. This is why the page can move records to close holes, or grow a record, and every record id stays valid. A [heap file](/heap-file/) is a set of such pages; this page is about the layout inside one page, and the heap file is about how the pages of a table are found.

## In plain words

Think of a page as a box with a list taped inside the lid. The things go into the box from the bottom, and each line on the list says where one thing lies and how big it is. When you want something, you ask for "box 7, line 3", read line 3 and go to that spot.

The list grows down from the top, and the things pile up from the bottom. The box is full when they meet.

When you throw something out, you cross out its line, and its space becomes a hole. Later you can push all the things together to close the holes. The positions change, but the line numbers do not, so anyone who wrote down "box 7, line 3" still finds the same thing.

## The abstract type

A slotted page is a map from small integers (slots) to byte strings (records), stored in a page of $p$ bytes.

- `insert(P, r)`: store record $r$ and return a slot $s$ that no live record uses. Fail with *page full* only if $r$ cannot fit even after compaction.
- `get(P, s)`: the record of slot $s$, or nothing if $s$ is free.
- `delete(P, s)`: free slot $s$.
- `update(P, s, r)`: replace the record of slot $s$ by $r$; the slot stays the same.
- `compact(P)`: move the live records together; no slot and no record changes.

The guarantee that matters to the rest of the system is that a slot, once returned, names the same record until that record is deleted. Indexes store record ids, and a record id is (page id, $s$).

## Representation

All numbers below are 2-byte integers, which allows pages up to 64 KB. Real systems use other widths; the layout is the same.

| bytes | contents |
|---|---|
| 0 to 1 | $n$, the number of slots in the directory |
| 2 to 3 | $e$, the offset of the first byte of the record area (free end) |
| $4 + 4s$ to $7 + 4s$ | slot $s$: the offset and the length of its record, or $(0, 0)$ if it is free |
| $4 + 4n$ to $e - 1$ | free space |
| $e$ to $p - 1$ | records, in any order, with holes left by deletes |

The offset 0 marks a free slot, since the header is at offset 0 and no record can start there.

The invariant has four parts.

1. $4 + 4n \le e \le p$: the directory and the record area do not overlap.
2. Every live slot $s$ has an offset $o_s$ and length $\ell_s$ with $e \le o_s$ and $o_s + \ell_s \le p$, and the byte ranges of two live slots are disjoint.
3. If $n > 0$, slot $n - 1$ is live: the directory has no free slots at its end.
4. The bytes at $[o_s, o_s + \ell_s)$ are the last record stored in slot $s$.

The page has two measures of free space. The *contiguous* free space is $e - 4 - 4n$, the gap in the middle. The *total* free space is $p - 4 - 4n - \sum_s \ell_s$ over the live slots, the gap plus the holes. Compaction makes the two equal.

## Operations

```pseudo id=main
INSERT(P, r)                               ▷ returns the slot of r
L1  s ← the least free slot, or n if no slot is free
L2  need ← |r|, plus 4 if s = n            ▷ a new slot entry also takes space
L3  if need > e - 4 - 4n then
L4      if need > the total free space then fail: page full
L5      COMPACT(P)
L6  e ← e - |r|; copy r to bytes [e, e + |r|)
L7  if s = n then n ← n + 1
L8  slot[s] ← (e, |r|)
L9  return s

DELETE(P, s)
L10 slot[s] ← (0, 0)
L11 while n > 0 and slot[n - 1] is free do
L12     n ← n - 1

COMPACT(P)
L13 L ← the live slots, sorted by offset from high to low
L14 e' ← p
L15 for each slot s in L do
L16     e' ← e' - ℓ_s
L17     move bytes [o_s, o_s + ℓ_s) to [e', e' + ℓ_s)
L18     slot[s] ← (e', ℓ_s)
L19 e ← e'
```

`get(P, s)` reads slot $s$ and returns the bytes it points to. `update(P, s, r)` writes $r$ in place when $|r| \le \ell_s$ (the tail of the old record becomes a hole). When $r$ is longer, it frees slot $s$ for a moment, compacts if the gap is too small, and writes $r$ at the free end under the same slot. If $r$ does not fit even then, the record must leave the page; see the pitfalls.

COMPACT moves each record toward the end of the page, never toward the start. The records are taken from the highest offset down, and the bytes placed so far are exactly the records with higher offsets, so $e' \ge o_s$ at line L17. The move is a memory move that is safe when source and target overlap.

## Example

Take $p = 64$. The header uses bytes 0 to 3, and each slot entry 4 bytes.

| step | slots after the step | $n$ | $e$ | gap | total free |
|---|---|---|---|---|---|
| start | none | 0 | 64 | 60 | 60 |
| insert A (10 bytes) | 0: (54, 10) | 1 | 54 | 46 | 46 |
| insert B (6 bytes) | 0: (54, 10), 1: (48, 6) | 2 | 48 | 36 | 36 |
| insert C (12 bytes) | 0: (54, 10), 1: (48, 6), 2: (36, 12) | 3 | 36 | 20 | 20 |
| delete slot 1 | 0: (54, 10), 1: free, 2: (36, 12) | 3 | 36 | 20 | 26 |
| insert D (24 bytes) | 0: (54, 10), 1: (18, 24), 2: (42, 12) | 3 | 18 | 2 | 2 |

The delete leaves a hole of 6 bytes at offsets 48 to 53, and slot 1 stays in the directory because slot 2 after it is live. The insert of D reuses slot 1, so it needs 24 bytes. The gap has only 20, but the total free space is 26, so line L5 compacts: A stays at 54, C moves from 36 to 42, and $e$ becomes 42. D is then written at 18. Slot 2 still names C, at a new offset. A record id (page, 2) stored in an index before the compaction still finds C.

If D had been 27 bytes, it would need 27 bytes against 26 free, and the insert would fail with page full. The heap file would then try another page.

## Correctness

Each operation keeps the four parts of the invariant.

- INSERT writes $r$ at $[e - |r|, e)$, which lies in the gap because line L3 or the compaction at line L5 ensures that the gap holds $need$ bytes. So the new record overlaps no live record and no slot entry, including a new entry at the end of the directory. Other slots do not change.
- DELETE frees one slot, and lines L11 and L12 drop free slots from the end of the directory, which restores part 3.
- COMPACT places the live records next to each other at the end of the page, in the order of their old offsets. Their lengths add up to $p - e'$, so they are disjoint and lie in $[e', p)$. The directory and $n$ do not change, so it keeps parts 1 and 3. A memory move copies the bytes even when the ranges overlap, which keeps part 4.

INSERT fails only when $r$ cannot fit. After COMPACT the gap equals the total free space, and the insert needs exactly $need$ bytes of the gap. So it fails if and only if $need$ is more than the total free space, which is the test at line L4. INSERT returns a free slot by line L1, so no live record loses its slot, and no operation other than DELETE frees a slot. The full proof is below.

## Complexity

The costs are CPU work on a page that is already in memory, in the [word RAM](/word-ram/) with byte moves counted one per byte. The page I/O is the business of the [buffer pool](/buffer-pool/).

| operation | time |
|---|---|
| `get` | $O(1)$ |
| `delete` | $O(1)$ amortized; the trailing free slots are removed once each |
| `insert` without compaction | $O(n + r)$: the scan for a free slot and the copy |
| `compact` | $O(n \log n + p)$: the sort of the live slots and at most $p$ bytes moved |
| `insert` with compaction | $O(n \log n + p)$ |

The scan at line L1 becomes $O(1)$ if the free slots are kept in a [free list](/free-list/) or a bitmap, and the sort at line L13 is not needed if records are compacted in slot order into a second buffer of $p$ bytes. The space overhead is the header and 4 bytes per slot. A free slot keeps its 4 bytes until it is reused or is at the end of the directory.

## Variants

- **Fixed-length records.** When all records have the same length, slot $s$ can be the $s$-th record position, and a bitmap marks the used positions. No offsets are needed. Ramakrishnan and Gehrke call the version that keeps records packed at the start "packed", and the version with a bitmap "unpacked"; only the unpacked version keeps record ids stable after a delete.
- **Forwarding addresses.** When an updated record no longer fits, it moves to another page and its old slot keeps the new record id. A lookup then follows one extra pointer, and the original record id stays valid. If the record moves again, the system updates the first slot and does not make a chain.
- **Item identifiers with flags.** PostgreSQL keeps a 24-byte page header, then an array of 4-byte item identifiers (offset, length and a state of unused, normal, redirect or dead), then free space, then the tuples, and an optional special space at the very end for index pages. The redirect state works as a forwarding address inside the page.
- **Slots in key order.** In the nodes of a [B+ tree](/b-plus-tree/), such as SQLite b-tree pages, the array of cell pointers is kept sorted by key, so a binary search runs on the slots. An insert then shifts the pointers after it, and the slot number is no longer a stable id. The index finds a record by key, not by slot.
- **Column layouts.** [PAX](/pax-page-layout/) keeps the slotted idea for variable-length values but splits the record area of the page into one minipage per attribute. The [N-ary storage model](/n-ary-storage-model/) is the layout of whole records in slotted pages.

## When to use it

Use a slotted page for any page that stores records of variable length and is pointed to by record ids: the pages of a heap file, of a table that secondary indexes point into, and of the overflow pages of hash tables. Use the fixed-length variant when all records have the same size, since it needs no offsets. Inside index nodes, keep the slots in key order and do not hand out slot numbers as ids.

## Pitfalls

- **Reuse of a slot too early.** If slot $s$ of a deleted record is reused while an index still holds (page, $s$), the index now points to a different record. Remove the index entries before the slot is reused, or mark the slot dead and free it only after a cleanup pass.
- **Compaction under a reader.** Compaction moves bytes, so a thread that holds a pointer into the page sees garbage. The page needs an exclusive latch that waits until no one else has the page pinned, as with the cleanup lock of PostgreSQL.
- **Free slots at the end.** Without lines L11 and L12, a page whose last records were deleted keeps their slot entries forever, and the gap never recovers those bytes.
- **Two kinds of free space.** A test for room that uses only the gap rejects records that would fit after compaction. A test that uses only the total free space forgets the 4 bytes of a new slot entry.
- **Offset width.** Offsets of 2 bytes limit a page to 64 KB. The offset 0 is a good marker of a free slot only because the header is at offset 0.
- **A record bigger than a page.** Such a record must be split, or moved out of line into overflow pages, with a pointer in the slotted page.

## Implementations

## History

The layout is part of relational practice from the early systems on, and it appears in the standard texts: Gray and Reuter (1993) in their tuple-oriented file system, Ramakrishnan and Gehrke in their chapter on storing data, and Hellerstein, Stonebraker and Hamilton (2007) in their survey of the architecture of database systems. Ailamaki, DeWitt, Hill and Skounakis (2001) describe the standard row layout as "a.k.a., slotted pages" when they introduce PAX. Today PostgreSQL heap pages and SQLite b-tree pages are slotted pages, and Petrov (2019) explains the layout as the base of the page formats of storage engines.

## References
