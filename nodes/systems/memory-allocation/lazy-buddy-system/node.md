---
tag: QQ2EAC
kind: algorithm
slug: lazy-buddy-system
name: Lazy buddy system
aliases:
- lazy buddy
- lazy buddy algorithm
area: systems/memory-allocation
level: advanced
summary: "A buddy system that keeps some freed blocks unmerged for quick reuse. A per-class slack count decides when a free must merge, so unmerged blocks never outnumber used ones."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {m: "the order of the heap, which has 2^m words", n: the requested size in words}
  time: {worst: O(m), best: O(1)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1989
  people: [Ronald E. Barkley, T. Paul Lee]
  note: Barkley and Lee presented the lazy buddy system with its slack rule at SOSP 1989, for the kernel memory allocator of UNIX System V.
prereqs: [buddy-system, deferred-coalescing]
see_also: [fibonacci-buddy-system, slab-allocator, coalescing, segregated-free-lists, external-fragmentation]
sources:
  - paper: doi:10.1145/74850.74867
    title: Ronald E. Barkley and T. Paul Lee, A lazy buddy system bounded by two coalescing delays per class, SOSP 1989, Operating Systems Review 23(5), 167-176
    locator: the slack D = N - 2L - G and the lazy, reclaiming and accelerated states of a class
  - book: isbn:9780131019089
    title: Uresh Vahalia, UNIX Internals, The New Frontiers, Prentice Hall, 1996
    locator: Chapter 12, Kernel memory allocation (the lazy buddy algorithm)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986
    locator: Section 3.11, Quick lists and deferred coalescing
---

The lazy buddy system is a [buddy system](/buddy-system/) that does not always merge a freed block with its buddy. A freed block can stay on its free list as a *locally free* block, ready for the next request of the same size, so a program that frees and allocates blocks of one size again and again does no splits and no merges. A count per size class, the *slack*, decides at each free if the block can stay unmerged or if the allocator must merge now. The rule keeps the number of unmerged free blocks of a class at most the number of used blocks of that class.

## In plain words

In the ordinary buddy system, each returned piece of memory is glued back to its partner at once, and the next request of the same size cuts it apart again. This wastes work when a program uses the same size over and over.

The lazy buddy system lets a returned piece wait, unglued, so that the next request takes it at once. But pieces that wait cannot join into larger pieces, so too many of them would block large requests. So each size keeps a count of how many pieces are in use and how many wait. While the waiting pieces are few compared with the used ones, a returned piece can wait. When they are about as many, a returned piece is glued back at once, and sometimes one waiting piece too.

## The problem

The heap has $2^m$ words, the requests are malloc$(n)$ and free$(p)$ as in the [online memory allocation](/online-memory-allocation/) problem, and blocks never move. As in the binary buddy system, each block is a block of the buddy tree: it has $2^k$ words for some order $k$, starts at a multiple of $2^k$, and its buddy starts at $p \oplus 2^k$. The goal is the same as for the buddy system, but with less work for programs that free and allocate blocks of the same size often.

**The state of a class.** For each order $k$, the blocks of size $2^k$ are of three kinds:

- $A_k$ *active* blocks, which the program holds;
- $L_k$ *locally free* blocks, which are free but still count as in use for the buddy logic, so no merge takes them;
- $G_k$ *globally free* blocks, which are free as in the eager buddy system and merge with a free buddy.

Barkley and Lee define the slack of class $k$ as $D_k = N_k - 2 L_k - G_k$, where $N_k = A_k + L_k + G_k$. This is the same as

$$D_k = A_k - L_k.$$

## The algorithm

LOCAL$[k]$ and GLOBAL$[k]$ are the two free lists of class $k$. A request takes a locally free block first, because that block needs no work.

```pseudo id=main
LAZY-MALLOC(n)
L1  k ← ⌈lg n⌉                                  ▷ FAIL if k > m
L2  if LOCAL[k] is not empty then p ← remove a block from LOCAL[k]
L3  else if GLOBAL[k] is not empty then p ← remove a block from GLOBAL[k]
L4  else take a block of the least larger order with a free block, and split it
       down to order k as in the buddy system, each upper half to GLOBAL; FAIL if none
L5  A[k] ← A[k] + 1; return p

LAZY-FREE(p)
L6  k ← the order of p; D ← A[k] − |LOCAL[k]|; A[k] ← A[k] − 1
L7  if D ≥ 2 then add p to LOCAL[k]                       ▷ lazy
L8  else if D = 1 then GLOBAL-FREE(p, k)                  ▷ reclaiming
L9  else q ← remove a block from LOCAL[k]; GLOBAL-FREE(p, k); GLOBAL-FREE(q, k)
                                                          ▷ accelerated

GLOBAL-FREE(p, k)
L10 while k < m and p ⊕ 2^k is in GLOBAL[k] do
L11     remove p ⊕ 2^k from GLOBAL[k]; p ← min(p, p ⊕ 2^k); k ← k + 1
L12 add p to GLOBAL[k]
```

GLOBAL-FREE is the free of the eager buddy system, but it looks only at GLOBAL lists, so a locally free buddy stops the merges. Barkley and Lee name the three cases of a free after the state of the class. With a slack of 2 or more, the class is *lazy* and the block becomes locally free, which lowers $D$ by 2. With a slack of 1, the class is *reclaiming*: the block is freed globally and $D$ becomes 0. With a slack of 0, the class is *accelerated*: the block and one locally free block are freed globally, and $D$ stays 0. In case L9, a slack of 0 means $L_k = A_k \ge 1$, so a locally free block exists.

## Example

Take $m = 2$, a heap of 4 words. The program allocates four blocks of 1 word, at 0, 1, 2 and 3, so $A_0 = 4$ and $D_0 = 4$. Then it frees three of them, asks for 2 words, and frees the last block.

| step | call | $D_0$ before | case | LOCAL[0] | GLOBAL lists |
|---|---|---|---|---|---|
| 1 | free(0) | 4 | lazy | 0 | none |
| 2 | free(1) | 2 | lazy | 0, 1 | none |
| 3 | free(2) | 0 | accelerated: free 2 and the local block 1 globally; 2 has buddy 3 (active) and 1 has buddy 0 (local), so nothing merges | 0 | 1 and 2 of order 0 |
| 4 | malloc(2) | | no block of order 1 or 2 is free: FAIL | 0 | 1 and 2 of order 0 |
| 5 | free(3) | 0 | accelerated: free 3 and the local block 0; 3 merges with 2, then 0 merges with 1 and with the block at 2 | none | 0 of order 2 |

Step 4 shows the price of laziness. The blocks 0 and 1 are free buddies, and an eager buddy system would have merged them at step 2 and served the request. The lazy system fails because block 0 is locally free. The page's implementation has an optional flag that, after a failure, frees all locally free blocks globally and tries once more. This flag is a choice of this page, not a rule of the paper. Step 5 shows that the slack rule still brings all memory back: when the last block is freed, the heap is one block again.

## Correctness

A state is *legal* when (T) the active, the locally free and the globally free blocks are buddy tree blocks that tile the heap, (B) no two globally free blocks are buddies, and (S) $0 \le L_k \le A_k$ for each $k$, that is $D_k \ge 0$. Lines L7 to L9 keep (S): the lazy case needs $D \ge 2$ and lowers $D$ by 2, the reclaiming case lowers $D$ from 1 to 0, and the accelerated case lowers $A_k$ and $L_k$ by 1 each. GLOBAL-FREE keeps (T) and (B) for the same reasons as the free of the buddy system, because it treats locally free blocks as in use. When the program has freed all its blocks, $A_k = 0$ for each $k$, so (S) gives $L_k = 0$: all free blocks are globally free with no free buddies, and by the canonical form of the buddy system the heap is one block. The full proof is in the [correctness proof](proofs/correctness.md).

## Complexity

In the [word RAM](/word-ram/), with the lists as doubly linked lists and a count per class:

- **malloc** takes $O(1)$ time when line L2 or L3 finds a block, and $O(m)$ time when line L4 must split.
- **free** takes $O(1)$ time in the lazy case, and $O(m)$ time in the other cases. The accelerated case calls GLOBAL-FREE twice, so it does at most $2m$ merges.
- **Space.** Two list heads and a count $A_k$ per class, so $\Theta(m)$ words besides the blocks, and one more bit per block to tell local from global.

The worst case is no better than in the eager buddy system. The gain is in the common case. When a program frees and allocates blocks of one size in a steady state, the slack of the class stays high and most calls take the $O(1)$ paths. In a seeded run of the page's test code (20000 calls on a heap of 4096 words, sizes 1 to 16 words, at most 61 live blocks), the lazy system made 1742 merges and the eager system 3045.

## Properties

- **Bounded laziness.** At each time, a class has at most as many locally free blocks as active blocks. When a class has no active blocks, it has no locally free blocks.
- **Full recovery.** When all blocks are freed, the heap is one free block again, as in the eager buddy system.
- **Not canonical.** Unlike the eager buddy system, the free lists depend on the order of the calls, not only on the set of active blocks.
- **Can fail where eager succeeds.** Locally free buddies do not merge, so a large request can fail while enough free buddies exist (step 4 of the example).

## Variants and improvements

- **Watermarks.** Before the slack rule, Barkley and Lee studied a scheme that kept the number of free blocks of each class between a low and a high mark. The slack rule replaces the fixed marks with a mark that follows the demand of each class.
- **Flush on failure.** Free all locally free blocks globally when a request fails, as the page's code does with a flag. Then a request fails only when the eager system would fail with the same active blocks.
- **Per-size caches.** The [slab allocator](/slab-allocator/) and the quick lists of [deferred coalescing](/deferred-coalescing/) use the same idea: keep freed objects of a popular size ready, and give memory back to the general allocator later.

## When to use it

Use the lazy buddy system for a kernel or a system allocator that already uses a buddy system and serves many requests of a few sizes, so that merges and splits that undo each other cost real time. Barkley and Lee designed it for the kernel memory allocator of UNIX System V. When the program has strong peaks of one size followed by large requests, prefer the eager buddy system or add a flush, because locally free blocks can block a large request.

## Pitfalls

- **Merging locally free blocks.** GLOBAL-FREE must look only at GLOBAL lists. If it merges a block with a locally free buddy, the count $L_k$ is wrong and the slack rule breaks.
- **Counting the slack after the change.** Line L6 reads $D$ before it lowers $A_k$. If the code lowers $A_k$ first, every case shifts by one, and the accelerated case can run with an empty LOCAL list.
- **Taking from the wrong list first.** Line L2 takes a locally free block before a globally free one. If a request takes globally free blocks first, locally free blocks stay unmerged for longer, and more large requests fail.

## Implementations

## History

Knowlton's 1965 paper on the buddy system already suggested that merges could be delayed, and many later allocators keep quick lists of recently freed blocks. Barkley and Lee built a buddy allocator for the kernel of UNIX System V with a watermark scheme, and in 1989 they replaced the watermarks with the slack rule, which needs no tuning and bounds the number of unmerged blocks per class. Vahalia's textbook on UNIX internals describes their lazy buddy algorithm next to the slab allocator.

## References
