---
tag: H0T260
kind: algorithm
slug: mark-compact
name: Mark-compact collection
aliases:
- mark-compact
- compacting collector
- mark-compact garbage collection
area: systems/garbage-collection
level: core
summary: "A tracing collector that marks the live objects and then moves them together in the same heap, so that the free space becomes one block. Phases: mark, compute locations, update, move."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the number of words in use in the heap, L: the number of live objects, r: the number of roots}
  time: {worst: O(n + r)}
  space: {extra: O(L)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1964
  people: [Daniel J. Edwards]
  note: Edwards's two-finger compactor for the LISP system of the Q-32 is the earliest mark-compact algorithm in the Garbage Collection Handbook; the LISP 2 sliding compactor followed in 1966.
prereqs: [mark-and-sweep, heap-compaction]
see_also: [two-finger-compaction, lisp2-compaction, copying-collection, tracing-garbage-collection, memory-compaction, bump-pointer-allocation, external-fragmentation, gc-space-time-tradeoff]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 3 (mark-compact garbage collection; the arbitrary, linearising and sliding orders; Sections 3.1 to 3.4)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 5, mark-compact garbage collection
  - paper: doi:10.1145/359576.359583
    title: F. Lockwood Morris, A time- and space-efficient garbage compaction algorithm, Communications of the ACM 21(8), 662-665, 1978
    locator: threaded compaction that keeps the order
  - paper: H. B. M. Jonkers, A fast garbage compaction algorithm, Information Processing Letters 9(1), 26-30, 1979
    locator: threaded sliding compaction in two passes
---

Mark-compact collection is a family of [tracing](/tracing-garbage-collection/) garbage collectors that reclaim memory in place. The collector first marks the objects reachable from the roots, as [mark-and-sweep](/mark-and-sweep/) does. Then, in place of a sweep, it moves the live objects together at one end of the heap and rewrites every pointer to them. The free space becomes one block, so allocation is a [bump pointer](/bump-pointer-allocation/) and there is no [fragmentation](/external-fragmentation/). The cost is extra passes over the heap. Members of the family differ in the order in which they place the objects: *arbitrary*, *linearising* or *sliding*. This page gives the general four-phase scheme with the sliding order.

## In plain words

A mark-and-sweep collector leaves the live objects where they are and lists the holes between them. After a while the holes are many and small, and a large object may not fit in any of them, although the total free space is large.

A mark-compact collector does more work to avoid this. After it finds the live objects, it decides a new place for each one at the start of the heap, changes every pointer to use the new places, and then moves the objects there. Now all the free space is one piece at the end, and a new object is simply put at the end of the used part.

## The problem

**Heap model.** The heap is an array of words. Each object has a size word and then its pointer fields, each the address of an object or nil. The objects lie one after another from address 0 to $\mathit{top}$, so the heap uses $n = \mathit{top}$ words; the free space is from $\mathit{top}$ up. The mutator holds its references in $r$ root slots and is stopped while the collector runs ([stop the world](/stop-the-world-collection/)).

**Task.** Keep exactly the objects reachable from the roots, move them into one block at the start of the heap, and update the roots and fields so that the reachable graph is the same up to a renaming of the addresses. This is [heap compaction](/heap-compaction/) done by a garbage collector.

**What is measured.** The time and the number of passes over the heap, the extra space, and the order in which the live objects end.

## The algorithm

The scheme has four phases (Handbook, Chapter 3): mark, compute the new locations, update the references, and relocate. The version below uses a side table $F$ for the new addresses and the sliding order.

```pseudo id=main
MARK-COMPACT(H)
L1  mark every object reachable from the roots          ▷ phase 1, as in mark-and-sweep
L2  F ← empty table; free ← 0                            ▷ phase 2: compute locations
L3  for each marked object a, in address order do
L4      F[a] ← free; free ← free + size(a)
L5  for each root slot s ≠ nil do s ← F[s]               ▷ phase 3: update references
L6  for each marked object a, and each field f ≠ nil of a do f ← F[f]
L7  for each marked object a, in address order do        ▷ phase 4: relocate
L8      copy the size(a) words of a to F[a], from low to high; unmark a
L9  top ← free; the words from top up are free
```

Phase 2 fixes the order: here it gives each live object the sum of the sizes of the live objects below it, which is the sliding order. Phase 3 must read the table before phase 4 moves anything, because a pointer names its target by the old address. Phase 4 is safe in place for the sliding order, because $F[a] \le a$ and the copy runs from low to high, so a move never overwrites a word that has not been read.

**The three orders.**

- **Arbitrary.** Objects are moved with no regard for their old order or for their links. [Two-finger compaction](/two-finger-compaction/) is the example: it fills holes at the bottom with cells from the top, in two passes, but needs cells of one size.
- **Linearising.** Objects are moved so that an object lands next to related objects, for example the objects it points to, as in the order of a [depth-first](/depth-first-search/) or [breadth-first](/breadth-first-search/) traversal. This order is common in [copying collectors](/copying-collection/), which place objects in traversal order anyway.
- **Sliding.** Objects slide towards one end and keep their address order. [Lisp 2 compaction](/lisp2-compaction/), the threaded algorithms of Morris (1978) and Jonkers (1979), and modern one-pass compactors use this order. It is the order of choice, because it keeps the locality that the program had when it allocated the objects.

The variants also differ in where they keep the new address: in a word of each object (Lisp 2), in a side table (as above, and in one-pass compactors), in the vacated cell (two-finger), or nowhere, by threading the pointers into chains (Morris, Jonkers).

## Example

The heap has five objects. The roots are $S$ and $P$.

| object | address | size | fields |
|---|---|---|---|
| $P$ | 0 | 2 | $S$ |
| $Q$ | 2 | 1 | none |
| $R$ | 3 | 3 | $P$, $T$ |
| $S$ | 6 | 2 | $T$ |
| $T$ | 8 | 2 | $R$ |

**Mark.** From $S$ the marker reaches $T$, then $R$, then $P$; the root $P$ is already marked. $Q$ stays unmarked.

**Compute locations.** In address order: $F[P] = 0$, $F[R] = 2$, $F[S] = 5$, $F[T] = 7$, and $\mathit{free} = 9$.

**Update.** The roots become $(5, 0)$. The field of $P$ becomes 5, the fields of $R$ become $(0, 7)$, the field of $S$ becomes 7, and the field of $T$ becomes 2.

**Relocate.** $P$ stays; $R$ moves from 3 to 2; $S$ from 6 to 5; $T$ from 8 to 7. The words $0$ to $8$ are $[2, 5 \mid 3, 0, 7 \mid 2, 7 \mid 2, 2]$ and $\mathit{top} = 9$. The order $P, R, S, T$ is the same as before, and the one free word of $Q$ has joined the free block.

## Correctness

The mark phase marks exactly the reachable set $R$, by the argument of [mark-and-sweep](/mark-and-sweep/), and $R$ is closed under the fields. Let $\varphi(x)$ be the sum of the sizes of the live objects below $x$. Phase 2 stores $\varphi$ in the table. Phase 3 maps each root and each field of a live object through $\varphi$ and does not move anything. In phase 4, $\varphi(x) \le x$ and the targets of the live objects follow each other without overlap, so by induction each move reads an unchanged image and does not disturb the earlier targets or the objects still to be moved. So at the end the live objects sit at $\varphi$ of their old addresses, with every pointer renamed by $\varphi$. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Mark.** $O(r + \text{live words})$, as in mark-and-sweep.
- **Compute locations and relocate.** Each finds the live objects in address order. With a mark bitmap this is a scan of $n$ bits, $O(n)$; the copies move each live word once.
- **Update.** $O(r)$ for the roots and $O(\text{live words})$ for the fields.
- **Total.** $O(n + r)$, with a constant number of passes over the heap. Unlike a [copying collector](/copying-collection/), the cost has a term in the size of the heap, not only in the live data; see [the space-time tradeoff of garbage collection](/gc-space-time-tradeoff/).
- **Space.** The table $F$ has one entry for each of the $L$ live objects. Lisp 2 puts it in a header word, and threaded and one-pass compactors cut it to a few bits for each block.

## Properties

- **In place.** No second space, so a mark-compact collector can use almost all of the heap, unlike a copying collector that keeps half the heap empty.
- **No fragmentation after a collection.** The free space is one block.
- **Moves objects.** Every pointer must be found and rewritten, so the collector must be *precise*: it must know which words are pointers. A [conservative collector](/conservative-garbage-collection/) cannot move an object that an ambiguous word may point to.
- **Several passes.** The sliding order with a side table or forwarding word needs three passes over the heap after marking; threaded compaction needs two, and one-pass compactors use a bitmap and a table of block offsets.
- **Not online.** The mutator is stopped for the whole collection, unless the collector is made incremental or concurrent.

## Variants and improvements

- **[Two-finger compaction](/two-finger-compaction/).** Arbitrary order, cells of one size, two passes, the forwarding address in the vacated cell.
- **[Lisp 2 compaction](/lisp2-compaction/).** Sliding order, any sizes, three passes, one forwarding word in each object.
- **Threaded compaction.** Morris (1978) and Jonkers (1979) link all the references to an object into a chain that starts in the object, and unthread the chain when the new address is known. Sliding order, no forwarding word, two passes.
- **One-pass compaction.** Abuaiadh and others (2004) and the Compressor of Kermany and Petrank (2006) compute new addresses from the mark bitmap and a small offset table for each block of the heap, then update and move in one pass.
- **Partial compaction.** Collectors such as [Immix](/immix-collector/) and [Garbage-First](/garbage-first-collector/) compact only the regions with the most free space, and sweep the rest.

## When to use it

Use mark-compact collection when the heap must be used almost to its full size, so a copying collector's reserve is too costly, and when fragmentation would hurt, for example when objects have many sizes. It is the usual collector for the old generation of a [generational collector](/generational-garbage-collection/), where most objects survive and copying them all to a second space would cost space and time. A mark-and-sweep collector is cheaper when fragmentation is not a problem, and a [copying collector](/copying-collection/) is faster when most objects die and memory is plentiful.

## Pitfalls

- **Moving before updating.** The update phase finds the new address through the old address of the target. If the target has moved and been overwritten, the pointer is lost.
- **Copy direction.** In the sliding order, the old and new places of an object can overlap. The copy must go from low to high addresses.
- **Interior and ambiguous pointers.** A pointer into the middle of an object, or a word that may or may not be a pointer, must be handled, or the object must be pinned in place.
- **Hidden pointers.** Every root must be visible to the collector, including pointers held in registers or in native code. A missed root keeps an old address after the move.

## Implementations

## History

Edwards wrote the two-finger compactor for the LISP system of the Q-32 computer (described by Saunders), and the LISP 2 system of 1966 gave its name to the sliding compactor with a forwarding word. Morris (1978) and Jonkers (1979) found threaded compactors that need no extra word. Jones and Lins (1996) and the Garbage Collection Handbook (2011) describe the family through the three orders and the four phases used here.

## References
