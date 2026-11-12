---
tag: ANR9PV
kind: algorithm
slug: lisp2-compaction
name: Lisp 2 compaction
aliases:
- Lisp 2 compactor
- LISP 2 mark-compact algorithm
area: systems/garbage-collection
level: advanced
summary: "A mark-compact collector that makes three passes after marking: compute a forwarding address for each live object, update every pointer, then slide the objects down in order."
solves: [automatic-memory-reclamation]
variant_of: mark-compact
model: word-ram
complexity:
  vars: {m: the number of objects in the heap, L: the number of words in live objects, r: the number of roots}
  time: {worst: O(m + L + r)}
  space: {extra: O(m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1966
  people: [Paul W. Abrahams]
  note: The algorithm takes its name from the LISP 2 system; Jones and Lins and the Garbage Collection Handbook credit it to Abrahams et al. 1966.
prereqs: [mark-compact]
see_also: [mark-compact, two-finger-compaction, heap-compaction, mark-and-sweep, copying-collection, memory-compaction, bump-pointer-allocation]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 3, Section 3.2 (the Lisp 2 algorithm, Algorithm 3.2)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 5, mark-compact garbage collection (the Lisp 2 algorithm)
  - paper: Paul W. Abrahams and others, The LISP2 programming language and system, Proceedings of the AFIPS Fall Joint Computer Conference, 1966
    locator: the LISP 2 system to which the compactor is credited
  - paper: H. B. M. Jonkers, A fast garbage compaction algorithm, Information Processing Letters 9(1), 26-30, 1979
    locator: threaded compaction in two passes, the main alternative to a forwarding word
---

Lisp 2 compaction is the classic *sliding* [mark-compact](/mark-compact/) algorithm. After the mark phase it makes three passes over the heap in address order. The first pass gives each live object a forwarding address, the sum of the sizes of the live objects below it. The second pass replaces every pointer by the forwarding address of its target. The third pass slides each object down to its new address. The live objects end in one block at the bottom of the heap, in their old order, and objects can have any size. The cost is one extra word in each object. The algorithm takes its name from the LISP 2 system of Abrahams and others (1966).

## In plain words

Think of a row of books of different widths, with gaps between them, and some books marked to keep. You want the kept books pushed to the left with no gaps, in the same order.

First walk along the row with a counter that starts at zero. For each kept book, write the counter on a slip in the book: that is where the book will start. Then add its width to the counter.

Then walk again. Each book has notes that refer to other books by position. Change each note to the number on the slip of the book it refers to.

Then walk a third time and move each kept book left to the place on its slip. A book never moves right, so it never covers a book you have not moved yet.

## The problem

**Heap model.** The heap is an array of words. Each object has a header of two words, its size and a forwarding word, and then its pointer fields, each the address of an object or nil. The objects lie one after another from address 0 to $\mathit{top}$, so a scan can step from one object to the next by the size. The heap has $m$ objects, and the live ones take $L$ words. The mutator holds its references in $r$ root slots and is stopped. A mark phase, as in [mark-and-sweep](/mark-and-sweep/), has marked exactly the reachable objects, with mark bits in a side table.

**Task.** Move the live objects so that they fill the words $0$ to $L - 1$ in the same address order as before, and update every root and every field. The free space is then one block from $L$ up, ready for a [bump pointer](/bump-pointer-allocation/). This is [heap compaction](/heap-compaction/) with the sliding order.

**What is measured.** The time, the passes over the heap, and the extra space.

## The algorithm

```pseudo id=main
LISP2-COMPACT(H)                                ▷ after the mark phase
L1  free ← 0
L2  for each object a, in address order do      ▷ pass 1: forwarding addresses
L3      if a is marked then
L4          forward(a) ← free; free ← free + size(a)
L5  for each root slot s ≠ nil do s ← forward(s)        ▷ pass 2: update
L6  for each marked object a, in address order do
L7      for each field f of a with f ≠ nil do f ← forward(f)
L8  for each object a, in address order do      ▷ pass 3: move
L9      if a is marked then unmark a
L10         copy the size(a) words of a to forward(a), from low to high
L11 top ← free; the words from top up are free
```

Pass 1 is a running sum, so the forwarding addresses keep the order of the objects. Pass 2 must come before pass 3: it reads the forwarding word of each target at the old address of the target, and pass 3 destroys the old addresses. Pass 3 is safe in place because $\mathit{forward}(a) \le a$ for every live $a$ (the live objects below $a$ fit below $a$), and the copy goes from low to high words, so it never overwrites a word that it has not read yet, even when the old and new places overlap.

## Example

The heap has five objects, with the root $A$. Sizes count the two header words.

| object | address | size | fields | live |
|---|---|---|---|---|
| $A$ | 0 | 3 | $C$ | yes |
| $B$ | 3 | 2 | none | no |
| $C$ | 5 | 4 | $A$, $E$ | yes |
| $D$ | 9 | 3 | $C$ | no |
| $E$ | 12 | 3 | nil | yes |

The mark phase marks $A$, $C$ and $E$. The object $D$ points to $C$, but nothing points to $D$.

**Pass 1.** The counter starts at 0. $A$ gets 0 and the counter becomes 3; $B$ is skipped; $C$ gets 3 and the counter becomes 7; $D$ is skipped; $E$ gets 7 and the counter ends at 10.

**Pass 2.** The root $A$ becomes $0$. The field of $A$ changes from 5 to 3. The fields of $C$ change from $(0, 12)$ to $(0, 7)$. The field of $E$ is nil. The fields of $D$ are not touched, because $D$ is not marked.

**Pass 3.** $A$ stays at 0. $C$ moves from 5 to 3; the old and new places overlap in the words 5 and 6, and the copy from low to high is still correct. $E$ moves from 12 to 7.

The words $0$ to $9$ are now $[3, 0, 3 \mid 4, 3, 0, 7 \mid 3, 7, \text{nil}]$: $A$ points to $C$ at 3, $C$ points to $A$ at 0 and to $E$ at 7, and $\mathit{top} = 10$. The order $A, C, E$ is the same as before.

## Correctness

Let $x_1 < \cdots < x_k$ be the live objects and $\varphi(x_i)$ the sum of the sizes of $x_1, \ldots, x_{i-1}$. Pass 1 writes only forwarding words, and leaves $\varphi(x_i)$ in each one. Pass 2 writes only fields and roots, and maps each pointer $v$ to $\varphi(v)$, reading forwarding words that it never writes. Pass 3 keeps two facts: the objects already moved sit at their targets, and every word at or above the scan is unchanged. Both hold because $\varphi(x_i) \le x_i$ and the targets do not overlap. So the scan still reads correct sizes, and each copy reads its source before it overwrites it. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above; the mark phase is extra.

- **Pass 1.** One step for each of the $m$ objects: $O(m)$.
- **Pass 2.** The $r$ roots, a step for each object, and each field of a live object: $O(m + L + r)$.
- **Pass 3.** A step for each object, and a copy of each live word: $O(m + L)$.
- **Total.** $O(m + L + r)$ in the worst case, with three passes over the whole heap after marking. Since $m$ counts the dead objects too, the cost grows with the size of the heap, not only with the live data.
- **Space.** One forwarding word in each object, so $O(m)$ words that the heap layout must reserve, and no other space beside the mark bits.

## Properties

- **Order preserving (sliding).** The live objects keep their address order. Objects allocated together stay together, which is good for the cache and for paging.
- **Any object sizes.** Unlike [two-finger compaction](/two-finger-compaction/), the objects need not have the same size.
- **In place.** No second space; only the forwarding word in each header.
- **Three passes over the whole heap.** Each pass visits the dead objects as well as the live ones, so the method is slower than two-finger compaction and than [copying collection](/copying-collection/) when the heap is mostly garbage.
- **Moves the objects below the first hole not at all.** Every object below the first dead object has $\varphi(a) = a$, so a heap with its garbage near the top moves little.

## Variants and improvements

- **Threaded compaction.** Jonkers (1979), after Fisher and Morris (1978), links all pointers to an object into a chain through the object, and needs no forwarding word, with two passes.
- **Side tables.** One-pass algorithms, such as those of Abuaiadh et al. and the Compressor of Kermany and Petrank, keep the forwarding addresses in a small table for each block of the heap and compute them from the mark bitmap, so that the update and the move can share one pass.
- **Skipping the dense prefix.** A collector can leave in place the part at the bottom of the heap that has almost no garbage, and slide only the rest.
- **Parallel sliding.** The heap is split into regions; each thread computes the forwarding addresses of a region from the sum of the live sizes of the regions below it.

## When to use it

Use LISP 2 compaction when objects have many sizes, the order of the objects matters for locality, and there is no memory for a second space. It is a common choice for the old generation of a [generational collector](/generational-garbage-collection/), where most objects survive and a copying collector would need too much space. If the cells all have the same size and the order does not matter, [two-finger compaction](/two-finger-compaction/) is simpler and uses no extra word. If memory is plentiful and most objects die, a [copying collector](/copying-collection/) is faster.

## Pitfalls

- **Moving before updating.** If pass 3 runs before pass 2, the forwarding word of a target may already be overwritten by the object slid onto it.
- **Copying from high to low.** When the old and new places of an object overlap, a copy from the high end overwrites words that it has not read yet. Copy from the low end, as a `memmove` does.
- **Losing the heap parse.** Pass 3 reads the size of each object from its header. A copy must never write at or above the start of the next object, which holds because $\mathit{forward}(a) + \mathit{size}(a) \le a + \mathit{size}(a)$.
- **Reading forwarding words of dead objects.** Only live objects get a forwarding address in pass 1. A field of a dead object can hold anything, so pass 2 must update the fields of marked objects only.

## Implementations

## History

The algorithm is named after the LISP 2 system, and Jones and Lins and the Garbage Collection Handbook credit it to Abrahams and others (1966). It is the standard example of a sliding compactor with a forwarding word, and later algorithms are often described by how they avoid one of its three passes or its extra word: Morris (1978) and Jonkers (1979) thread the pointers instead, and modern one-pass compactors keep the forwarding information in side tables.

## References
