---
tag: G56SEJ
kind: data-structure
slug: free-list
name: Free list
aliases:
- free block list
- AVAIL list of free blocks
- explicit free list
area: systems/memory-allocation
level: intro
summary: "A linked list of the free blocks of a heap, with its links stored inside the free blocks, so it needs no other memory."
implements: [allocator]
prereqs: [allocator, linked-list, doubly-linked-list]
see_also: [sequential-fit, first-fit-allocation, coalescing, boundary-tags, segregated-free-lists, slab-allocator, mark-and-sweep, type-stable-memory]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, the AVAIL list of available blocks with SIZE and LINK fields, kept in order of location (Algorithms A and B) or doubly linked with boundary tags (Algorithm C)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.4 (sequential fits on a linear list, and the LIFO, FIFO and address-ordered list) and Section 3.2 (the header fields and boundary tags)
  - paper: doi:10.1145/367177.367199
    title: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4), 1960
    locator: the free-storage list from which cons takes registers, and the garbage collection that returns unreachable registers to it
---

A free list is a [linked list](/linked-list/) of the free blocks of a heap. The allocator stores the links in the free blocks themselves, because a free block holds no user data, so the list needs no memory beyond a head pointer and a tail pointer. A malloc searches the list for a block that fits, by a [sequential fit](/sequential-fit/) policy, and unlinks it or replaces it by the remainder of a split. A free links the block back. With a [doubly linked list](/doubly-linked-list/), unlink is $O(1)$, which is what immediate [coalescing](/coalescing/) needs. The order of the list is a choice: by address, LIFO or FIFO. The order changes which block a policy picks, and so it changes the fragmentation.

## In plain words

An empty room in a hotel is not used, so the hotel can write on its door the number of the next empty room. To find empty rooms, start at the first one written at the desk, and follow the numbers from door to door. No separate book is needed.

When a guest leaves, the room joins the chain. You can put it first, put it last, or put it in the place that keeps the rooms in number order. When a guest arrives, you walk the chain and take a room that is large enough.

## The abstract type

The free list is the mechanism behind the [allocator](/allocator/) interface: it holds the set of free blocks. The operations that the allocator needs are:

- `link(a)`: add the free block $a$, at the place the order asks for.
- `unlink(a)`: remove the block $a$, given a pointer to it.
- `replace(old, new)`: put the block $new$ at the place of $old$, after a split.
- `scan`: visit the blocks in list order, for the search of a fit policy.

## Representation

The heap is the one of [first-fit allocation](/first-fit-allocation/): blocks tile $[0, H)$, and each block has a header and a footer with $2s + u$ for its size $s$ and its used bit $u$. A free block at $a$ keeps NEXT in $mem[a + 1]$ and PREV in $mem[a + 2]$, so each free block needs at least $MIN = 4$ words. The list has a head and a tail, and NIL ends it.

**Invariant.** The NEXT pointers from the head visit each free block exactly once and end at the tail; the PREV pointers visit the same blocks in reverse. For the address order, the addresses increase along the list.

## Operations

```pseudo id=main
BETWEEN(a, p, q)                           ▷ put a between p and q
L1  NEXT(a) ← q; PREV(a) ← p
L2  if p = NIL then head ← a else NEXT(p) ← a
L3  if q = NIL then tail ← a else PREV(q) ← a

LINK(a)
L4  if order = lifo then BETWEEN(a, NIL, head)
L5  else if order = fifo then BETWEEN(a, tail, NIL)
L6  else q ← head                           ▷ address order
L7       while q ≠ NIL and q < a do q ← NEXT(q)
L8       BETWEEN(a, PREV(q) or tail if q = NIL, q)

UNLINK(a)
L9  p ← PREV(a); q ← NEXT(a)
L10 if p = NIL then head ← q else NEXT(p) ← q
L11 if q = NIL then tail ← p else PREV(q) ← p

REPLACE(old, new)                          ▷ new takes the place of old
L12 p ← PREV(old); q ← NEXT(old)
L13 BETWEEN(new, p, q)
```

A split gives out the low part of a block and keeps the high part as the new free block, so REPLACE keeps the address order with no walk.

## Example

Take $H = 64$. Allocate payloads of 10, 2, 6, 2, 14 and 2 words (blocks of 12, 4, 8, 4, 16 and 4 words at 0, 12, 16, 24, 28 and 44), so the only free block is $(48, 16)$. Free the blocks at 0, 16 and 28, in that order, and then serve one first-fit malloc(6), which needs 8 words.

| step | address order | LIFO | FIFO |
|---|---|---|---|
| start | 48 | 48 | 48 |
| free block 0 | 0, 48 | 0, 48 | 48, 0 |
| free block 16 | 0, 16, 48 | 16, 0, 48 | 48, 0, 16 |
| free block 28 | 0, 16, 28, 48 | 28, 16, 0, 48 | 48, 0, 16, 28 |
| malloc(6) | split 0: 8, 16, 28, 48 | split 28: 36, 16, 0, 48 | split 48: 56, 0, 16, 28 |

The same first-fit rule picks three different blocks, because the lists have different orders. In the address-ordered list after the third free, the words are $mem[1] = 16$, $mem[2] = $ NIL, $mem[17] = 28$, $mem[18] = 0$, and so on: the list lives in the free blocks.

## Correctness

Each operation changes only the links of the block it inserts or removes and of that block's two list neighbours, so the rest of the list is untouched. Link words of different free blocks are different words, because blocks do not overlap. LINK puts the block at the front, at the back, or before the first block of higher address, so the order condition holds after it. A split keeps the remainder inside the old block, so the remainder lies between the old neighbours in address order. The full proof is below.

## Complexity

| operation | address order | LIFO or FIFO |
|---|---|---|
| link | $O(F)$, a walk to the place | $O(1)$ |
| unlink | $O(1)$ | $O(1)$ |
| replace | $O(1)$ | $O(1)$ |
| scan | $O(F)$ | $O(F)$ |

Here $F$ is the number of free blocks. The space is two link words in each free block, and none in the used blocks. The [fifty-percent rule](/knuth-fifty-percent-rule/) predicts that, in a steady state with random frees, $F$ is about half the number of used blocks.

## Variants

- **A singly linked list.** Only NEXT, so a block needs fewer words. Unlink then needs the predecessor, which a search can carry along, but a merge on free cannot find it fast. Knuth's Algorithm B frees into a singly linked list kept in address order.
- **Circular with a sentinel.** A [sentinel node](/sentinel-node/) removes the NIL cases from link and unlink.
- **Segregated lists.** One list per size class, as in [segregated free lists](/segregated-free-lists/) and the [slab allocator](/slab-allocator/). For blocks of one size, a LIFO singly linked list gives $O(1)$ malloc and free.
- **Trees instead of lists.** For large heaps, a tree of free blocks indexed by size or by address replaces the list, as on the [best-fit](/best-fit-allocation/) page.
- **Garbage collectors.** A [mark-and-sweep](/mark-and-sweep/) collector builds a free list of the unreachable cells in its sweep phase.

## When to use it

Use an explicit doubly linked free list when blocks have many sizes, the heap is moderate, and free must merge neighbours. Use a LIFO singly linked list for pools of one block size. For large heaps with many free blocks, use segregated lists or trees, since the scan of one long list is slow.

## Pitfalls

- **Small blocks.** A free block must hold its links. Blocks smaller than $MIN$ words cannot be on the list, so a split must not leave such a remainder.
- **Use after free.** The links overwrite the first words of a freed block. A program that writes to a block after it freed it corrupts the list. See [use after free](/use-after-free/).
- **Double free.** Freeing a block twice links it twice and breaks the list. Check the used bit first.
- **Order on a split.** In address order, the remainder must take the old place. Pushing it at the head silently changes the policy.
- **Concurrent access.** A lock-free free list must solve the ABA problem, since a block can leave the list and come back between a read and a compare-and-swap. [Type-stable memory](/type-stable-memory/) is one answer.

## Implementations

## History

Lists of free storage are as old as list processing: McCarthy's LISP of 1960 took each new register from a free-storage list and refilled it by garbage collection. Knuth's Section 2.5 calls the list of free blocks the AVAIL list, gives first fit and liberation on a list sorted by address, and then a doubly linked list with boundary tags, so that a block can be removed and merged in constant time. Wilson, Johnstone, Neely and Boles studied the effect of the list order on fragmentation in their 1995 survey.

## References
