---
tag: K0DCNX
kind: data-structure
slug: memory-pool
name: Memory pool
aliases:
- object pool
- fixed-size block allocator
- fixed-size memory pool
area: systems/memory-allocation
level: intro
summary: "Allocator for many blocks of one fixed size. The free blocks form a list linked through the blocks, so alloc and free take O(1) time with no search."
implements: [allocator]
model: word-ram
complexity:
  vars: {n: the number of blocks, b: the block size in words}
  time: {alloc: O(1), free: O(1), create: O(1)}
  space: {extra: O(1)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [free-list]
see_also: [slab-allocator, segregated-free-lists, arena-allocation, bump-pointer-allocation, type-stable-memory, use-after-free, singly-linked-list, stack]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.3, the AVAIL stack of free nodes of one size, and the variant that takes nodes never used before from a pool pointer
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.6, simple segregated storage (one size per area, no splitting and no coalescing)
  - paper: "Jeff Bonwick, The slab allocator, an object-caching kernel memory allocator, USENIX Summer 1994 Technical Conference"
    locator: the object cache, which keeps freed objects of one type for reuse
---

A *memory pool* is an allocator for blocks of one fixed size. It takes one array of $n$ blocks of $b$ words, and it keeps the free blocks on a [singly linked list](/singly-linked-list/) whose links are stored in the free blocks themselves. To allocate, it pops the first block of the list; to free, it pushes the block back. Both take $O(1)$ time, need no search, and cause no [external fragmentation](/external-fragmentation/), because every free block fits every request. The price is that the pool serves one size only.

## In plain words

Think of a parking lot where every space has the same size. You never need to look for a space that fits, because each one fits each car. The guard keeps a list of empty spaces. The trick is that the list is written in the empty spaces themselves: each empty space has a note with the number of the next empty space, and the guard only needs to remember the first one.

When a car arrives, it takes the first empty space, and the guard reads its note to learn the new first space. When a car leaves, its space gets a note with the old first space, and it becomes the new first space. No walking is needed for either step.

## The abstract type

The memory pool implements the [allocator](/allocator/) interface for one block size:

- `alloc()` returns the address of a free block of $b$ words, which becomes allocated, or FAIL when all $n$ blocks are in use.
- `free(p)` gives back the block at $p$, which an earlier `alloc` returned.

There is no size parameter: every request asks for exactly one block. A program that needs several sizes uses one pool per size, which is [simple segregated storage](/segregated-free-lists/).

## Representation

- **MEM** is an array of $n b$ words. Block $i$ covers the words $i b$ to $i b + b - 1$, and its address is $i b$.
- **HEAD** is the address of the first free block on the list, or NIL.
- **Links.** For a free block at $p$ on the list, MEM$[p]$ holds the address of the next free block, or NIL. So the list uses the first word of each free block, and a block needs $b \ge 1$.
- **FRESH** counts the blocks that were handed out at least once. The blocks FRESH to $n - 1$ were never used and are not on the list. This lets the pool start in $O(1)$ time, without a pass that links all $n$ blocks.

## Operations

```pseudo id=main
POOL-ALLOC()
L1  if HEAD ≠ NIL then p ← HEAD; HEAD ← MEM[p]; return p
L2  if FRESH < n then p ← FRESH · b; FRESH ← FRESH + 1; return p
L3  return FAIL

POOL-FREE(p)
L4  MEM[p] ← HEAD
L5  HEAD ← p
```

The list is a [stack](/stack/): the last block freed is the next block allocated. This order is good for caches, because the block was used recently. Line L2 runs only when no freed block is waiting, so the pool hands out each block for the first time in address order, like a [bump pointer](/bump-pointer-allocation/).

## Example

A pool with $n = 4$ blocks of $b = 2$ words, so MEM has 8 words and the addresses are 0, 2, 4 and 6.

| step | call | result | HEAD | links | FRESH |
|---|---|---|---|---|---|
| 0 | create | | NIL | | 0 |
| 1 | A = alloc() | 0 | NIL | | 1 |
| 2 | B = alloc() | 2 | NIL | | 2 |
| 3 | C = alloc() | 4 | NIL | | 3 |
| 4 | free(A) | | 0 | MEM[0] = NIL | 3 |
| 5 | free(C) | | 4 | MEM[4] = 0 | 3 |
| 6 | alloc() | 4 | 0 | | 3 |
| 7 | alloc() | 0 | NIL | | 3 |
| 8 | alloc() | 6 | NIL | | 4 |
| 9 | alloc() | FAIL | NIL | | 4 |

At step 6 the pool gives back the block that was freed last. At step 8 the list is empty, so the pool takes the last block that was never used. At step 9 all four blocks are in use.

## Correctness

Call a block *listed* if it is on the list from HEAD, *fresh* if its index is at least FRESH, and *live* if the program holds it. The invariant is that each block is in exactly one of these three groups, and that the list is finite with no repeat. POOL-ALLOC moves one block from listed or fresh to live, and POOL-FREE moves one live block to the front of the list. So `alloc` never returns a live block, and it fails only when all $n$ blocks are live. The full proof is in the [correctness proof](proofs/correctness.md). The proof needs the program to free only live blocks: a double free puts a block twice on the list, and then two later calls of `alloc` return the same block.

## Complexity

In the [word RAM](/word-ram/):

| operation | time | why |
|---|---|---|
| create | $O(1)$ | set HEAD to NIL and FRESH to 0; with no FRESH counter, linking all blocks takes $\Theta(n)$ |
| alloc | $O(1)$ | one read and one write, or one counter step |
| free | $O(1)$ | two writes |

The extra space is two words, HEAD and FRESH, besides the $n b$ words of the blocks. There is no header per block: a live block does not need to store its size, because all blocks have the same size. There is no internal fragmentation when the objects are exactly $b$ words, and no external fragmentation at all.

## Variants

- **Growing pools.** When the array is full, get a new chunk of blocks from a general allocator and add it. The [slab allocator](/slab-allocator/) does this with slabs, and also gives back chunks that are wholly free.
- **Object pools.** Keep objects that are already built, so that a reused object skips its constructor. This is the *object pool* design pattern, and the object cache of the slab allocator. The memory pool on this page manages raw memory only.
- **Pools of several sizes.** One pool per [size class](/size-classes/) gives simple segregated storage.
- **Thread-local pools.** One pool per thread needs no lock. Freeing a block from another thread needs care, for example a second list that the owner drains.
- **Debug pools.** Fill freed blocks with a pattern, or keep a set of live blocks as the page's code does with its check flag, to catch double frees and [use after free](/use-after-free/).

## When to use it

Use a memory pool when a program allocates and frees many objects of one size, such as list nodes, tree nodes, network buffers or game entities, and when it needs fast calls with a fixed bound. Kernels and embedded systems use pools because they need no search and their memory is known in advance. Do not use one pool for objects of very different sizes: rounding all of them up to the largest wastes memory. If the objects are all freed at the same time, an [arena](/arena-allocation/) is simpler.

## Pitfalls

- **Double free.** Freeing a block twice links it twice, and the list can then return one block to two owners. The pool cannot see this without extra checks.
- **Use after free.** The first word of a freed block holds a link. A program that writes to a freed block breaks the list, and a later `alloc` can return an address outside the pool.
- **Blocks smaller than a link.** The block must hold at least one address. Round the block size up to the size and alignment of a pointer.
- **Alignment.** If the array is not aligned for the object type, every block is misaligned. Align the array and round $b$ up to the alignment.
- **Memory held for ever.** A pool keeps its memory even when all blocks are free, unless it gives back whole chunks.

## Implementations

## History

Fixed-size nodes with a stack of free nodes are as old as list processing. Knuth's *The Art of Computer Programming*, Section 2.2.3, uses an AVAIL stack of free nodes, linked through the nodes, and a pool pointer for nodes not yet used, which is the FRESH counter of this page. Wilson et al. (1995) call the general scheme with one size per area simple segregated storage. Bonwick's slab allocator (1994) extended pools with object caching, and many standard libraries and kernels provide pool allocators.

## References
