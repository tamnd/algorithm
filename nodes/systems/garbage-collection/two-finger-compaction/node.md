---
tag: JTB830
kind: algorithm
slug: two-finger-compaction
name: Two-finger compaction
aliases:
- Edwards two-finger algorithm
- two-pointer compaction
area: systems/garbage-collection
level: advanced
summary: "Compact a heap of equal-size cells in two passes. A finger from the bottom finds holes, a finger from the top finds live cells, and each live cell moved leaves its new address behind."
solves: [automatic-memory-reclamation]
variant_of: mark-compact
model: word-ram
complexity:
  vars: {n: the number of cells in the heap, k: the number of fields in a cell, L: the number of live cells, r: the number of roots}
  time: {worst: O(n + k L + r)}
  space: {extra: O(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1964
  people: [Daniel J. Edwards]
  note: Edwards's algorithm for the LISP system of the Q-32 computer is described by Saunders in the book of Berkeley and Bobrow on LISP; the Garbage Collection Handbook cites the 1974 printing.
prereqs: [mark-compact]
see_also: [mark-compact, lisp2-compaction, heap-compaction, mark-and-sweep, copying-collection, memory-compaction, bump-pointer-allocation]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 3, Section 3.1 (two-finger compaction, Algorithm 3.1)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 5, mark-compact garbage collection (the two-finger algorithm)
  - paper: Robert A. Saunders, The LISP system for the Q-32 computer, in E. C. Berkeley and D. G. Bobrow (eds.), The Programming Language LISP, Its Operation and Applications, Information International, 1964 (reprinted 1974)
    locator: the compacting garbage collector of the Q-32 LISP system, credited to Edwards
---

Two-finger compaction is a [mark-compact](/mark-compact/) algorithm for a heap of cells that all have the same size. After the mark phase, one finger moves up from the bottom of the heap to find free cells, and another moves down from the top to find live cells; each live cell found at the top is copied into the lowest hole, and its old place keeps its new address. A second pass replaces every pointer to a moved cell with that address. The live cells then fill one block at the bottom of the heap, in two passes and with constant extra space. The algorithm is due to Edwards, as described by Saunders for LISP on the Q-32. It does not keep the order of the cells.

## In plain words

Think of a shelf of equal boxes, some full and some empty. You want all the full boxes at the left end. Put your left hand on the first empty box from the left, and your right hand on the first full box from the right. Move the full box into the empty place, and leave a note in the old place that says where it went. Then move each hand on to the next empty box and the next full box. Stop when the hands meet.

Now the full boxes are at the left, but some boxes still point to old places. So go once more over the full boxes: when a pointer leads to a place at the right of where the hands met, read the note there and use the new place.

## The problem

**Heap model.** The heap has $n$ cells with the addresses $0$ to $n-1$. Every cell has the same size, with $k$ pointer fields (an address or nil) and a mark bit. The mutator holds its references in $r$ root slots and is stopped during the collection. A mark phase, as in [mark-and-sweep](/mark-and-sweep/), has marked exactly the $L$ cells reachable from the roots.

**Task.** Move the live cells so that they occupy the addresses $0$ to $L-1$, and update every root and every field so that the graph of live cells is the same as before, only at new addresses. The free space $L$ to $n-1$ is then one block, and the allocator can use a [bump pointer](/bump-pointer-allocation/). This is [heap compaction](/heap-compaction/) for cells of one size.

**What is measured.** The number of passes over the heap, the time, the extra space, and the number of cells moved.

## The algorithm

```pseudo id=main
TWO-FINGER(H)                                   ▷ after the mark phase
L1  free ← 0, live ← n − 1
L2  loop                                        ▷ pass 1: move cells
L3      while free < n and free is marked do free ← free + 1
L4      while live ≥ 0 and live is unmarked do live ← live − 1
L5      if free > live then exit the loop
L6      copy the fields of live into free, mark free
L7      unmark live, field 0 of live ← free      ▷ the forwarding address
L8      free ← free + 1, live ← live − 1
L9  top ← free                                  ▷ the cells 0 .. top − 1 are the live cells
L10 for each root slot s, and each field s of the cells 0 .. top − 1 do    ▷ pass 2
L11     if s ≠ nil and s ≥ top then s ← field 0 of cell s
L12 clear the marks of the cells 0 .. top − 1; the free area is top .. n − 1
```

Line L3 moves the *free finger* up over live cells to the next hole, and line L4 moves the *live finger* down over garbage to the next live cell. Lines L6 and L7 move one cell from the top to the hole and store its new address in the old place, which is now garbage, so no extra word is needed. When the fingers cross, every cell below $\mathit{top}$ is live and every cell from $\mathit{top}$ up is free. A pointer to a cell below $\mathit{top}$ points to a cell that never moved; a pointer to a cell at or above $\mathit{top}$ points to a moved cell, whose field 0 holds the new address. That is the whole test of line L11.

## Example

The heap has $n = 8$ cells with $k = 2$ fields, and the root is $3$. The fields are $0 \to (2, \text{nil})$, $1 \to (\text{nil}, 6)$, $2 \to (5, \text{nil})$, $3 \to (7, 1)$, $4 \to (\text{nil}, \text{nil})$, $5 \to (0, \text{nil})$, $6 \to (3, 4)$ and $7 \to (6, \text{nil})$. The mark phase marks the live cells $1, 3, 4, 6, 7$, so $L = 5$; the cells $0, 2, 5$ form a garbage cycle.

| pass 1 | free finger stops at | live finger stops at | action |
|---|---|---|---|
| iteration 1 | 0 | 7 | move 7 to 0; cell 7 now holds 0 |
| iteration 2 | 2 | 6 | move 6 to 2; cell 6 now holds 2 |
| iteration 3 | 5 | 4 | the fingers crossed: $\mathit{top} = 5$ |

In pass 2, every value $s \ge 5$ is replaced by field 0 of cell $s$:

| cell | fields after pass 1 | fields after pass 2 |
|---|---|---|
| 0 (was 7) | (6, nil) | (2, nil) |
| 1 | (nil, 6) | (nil, 2) |
| 2 (was 6) | (3, 4) | (3, 4) |
| 3 | (7, 1) | (0, 1) |
| 4 | (nil, nil) | (nil, nil) |

The root $3$ did not move. The live graph is the same, with 7 renamed to 0 and 6 renamed to 2, and the cells $5$ to $7$ are free. Two cells moved. The live cells were in the address order $1, 3, 4, 6, 7$; the same objects are now in the order $7, 1, 6, 3, 4$.

## Correctness

Pass 1 keeps four facts at line L5: exactly $L$ cells are marked; the cells below the free finger are marked and the cells above the live finger are not; every move went from a cell above the live finger to a cell below the free finger; and the marked cells are the new places of the live cells, each with the original fields, while each vacated cell holds the new address in field 0. When the fingers cross, the marked cells are exactly $0$ to $L - 1$. Every source of a move is at least $L$ and every destination is below $L$, so no cell moves twice and no forwarding address is overwritten. Pass 2 then maps each pointer $v$ to the new place of $v$. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above; the mark phase is extra, $O(r + kL)$.

- **Pass 1.** The two fingers together move over at most $n + 1$ positions, and each move copies $k$ fields. At most $\min(L, n - L)$ cells move. So pass 1 takes $O(n + kL)$ time.
- **Pass 2.** It visits the $r$ roots and the $kL$ fields of the live cells: $O(r + kL)$.
- **Total.** $O(n + kL + r)$ in the worst case, in two passes over the heap after marking.
- **Space.** The two fingers; the forwarding addresses live in the vacated cells. So $O(1)$ extra space beside the mark bits.

## Properties

- **Not order preserving.** Cells from the top of the heap land in holes near the bottom, in reverse order. Cells that the program allocated together, and often uses together, are pulled apart. This order is called *arbitrary* in the classification of [mark-compact](/mark-compact/) orders.
- **Equal sizes only.** A hole and a moved cell must have the same size. With objects of many sizes, a hole can be too small for the cell at the top, and the method breaks; the usual fix is a separate area for each size.
- **In place.** No second space and no side table.
- **Cells below the meeting point do not move.** Only the cells above $L$ move, so a heap with few holes near the bottom moves little.

## Variants and improvements

- **Size classes.** Run the algorithm separately in regions that each hold one size of cell.
- **Sliding compaction.** [LISP 2 compaction](/lisp2-compaction/) slides all live objects down in address order, which keeps the order and allows any sizes, at the price of a third pass and a forwarding word per object.
- **Threading.** Jonkers (1979), after Fisher and Morris (1978), threads the pointers to each object into a list, and compacts in two passes in order, with no forwarding word.
- **Copying.** A [copying collector](/copying-collection/) does the move and the update in one pass over the live data, but needs a second space as large as the live data.

## When to use it

Use two-finger compaction for a heap or region of equal-size cells (for example cons cells, or the cells of one size class) when the free space must be one block and the order of the cells does not matter. When objects have many sizes, or the locality of the program depends on the allocation order, use a sliding compactor such as [LISP 2](/lisp2-compaction/). When memory for a second space is available, [copying collection](/copying-collection/) is often faster, because it never visits garbage.

## Pitfalls

- **Forwarding without the boundary test.** Line L11 must test $s \ge \mathit{top}$. A cell below $\mathit{top}$ that never moved holds a real field 0, not a forwarding address; reading it as one gives a wrong pointer.
- **Updating before the fingers meet.** The value of $\mathit{top}$ is known only after pass 1 ends, at line L9. Pass 2 cannot run inside pass 1.
- **Clearing the fields of the vacated cell first.** Line L7 must write the forwarding address after line L6 has copied the fields, or the copy reads the forwarding address in place of field 0.
- **Moving cells of different sizes.** If a cell at the top is larger than the hole, line L6 overwrites the next live cell.

## Implementations

## History

The two-finger algorithm was written by Edwards for the LISP system of the Q-32 computer, and Saunders described that system in the book on LISP edited by Berkeley and Bobrow. The Garbage Collection Handbook presents it as the first mark-compact algorithm, before the LISP 2 algorithm and threaded compaction.

## References
