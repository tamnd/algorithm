---
tag: B9JWWG
kind: algorithm
slug: buddy-system
name: Buddy system
aliases:
- binary buddy system
- buddy allocator
area: systems/memory-allocation
level: core
summary: "Keep free blocks of size 2^k on one list per k. Split a block in halves to allocate, and merge a freed block with its buddy at address addr XOR 2^k."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {m: "the order of the heap, which has 2^m words", n: the requested size in words}
  time: {worst: O(m), best: O(1)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1965
  people: [Kenneth C. Knowlton]
  note: Knowlton published the binary buddy system in 1965. Knuth reports that H. Markowitz used the same idea in the Simscript system around 1963.
prereqs: [free-list, coalescing, internal-fragmentation]
see_also: [fibonacci-buddy-system, lazy-buddy-system, segregated-free-lists, size-classes, slab-allocator, tlsf, external-fragmentation, robson-bound]
sources:
  - paper: doi:10.1145/365628.365655
    title: Kenneth C. Knowlton, A fast storage allocator, Communications of the ACM 8(10), 623-624, 1965
    locator: the whole paper (blocks of size 2^k, the split and the recombination of buddies)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, Algorithm R (buddy system reservation) and Algorithm S (buddy system liberation)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986
    locator: Section 3.7, Buddy systems, and Section 4.1 (Knowlton 1965 and Knuth's analysis)
  - paper: doi:10.1145/359605.359626
    title: James L. Peterson and Theodore A. Norman, Buddy systems, Communications of the ACM 20(6), 421-431, 1977
    locator: the general definition of a buddy system and the comparison of binary, Fibonacci and weighted buddies
---

The buddy system is an [allocator](/allocator/) for a heap of $2^m$ words that hands out only blocks of $2^k$ words, each at an address that is a multiple of $2^k$. It keeps one [free list](/free-list/) for each $k$. To allocate, it splits a larger free block in halves until it has a block of the right size. To free, it merges the block with its *buddy*, the other half of the same parent, at address $a \oplus 2^k$, while the buddy is free and whole. Both operations take $O(m)$ time, and the price is [internal fragmentation](/internal-fragmentation/) of almost one half of a block in the worst case.

## In plain words

Think of the memory as one long bar. You may only cut a piece exactly in half. To serve a request, take the smallest free piece that is large enough, and cut it in halves again and again. Keep one half and put the other half aside, until the piece you keep is the smallest size that still holds the request.

Each piece has exactly one partner: the other half of the cut that made it. When you give a piece back and its partner is also free and not cut, you glue the two halves together. Then you try again with the bigger piece and its own partner. The partner is easy to find, because its position follows from the position and size of the piece with one quick bit operation.

## The problem

The heap has $H = 2^m$ words with the addresses $0, 1, \ldots, 2^m - 1$. The program calls malloc$(n)$ with $n \ge 1$ and gets an address $p$ of $n$ free words, or a failure. Later it calls free$(p)$ with an address that malloc returned. The allocator must not move a block, and two live blocks must not overlap. This is the [online memory allocation](/online-memory-allocation/) problem. What we measure is the time of each call and the memory lost to [internal](/internal-fragmentation/) and [external fragmentation](/external-fragmentation/).

A *block of order $k$* is a range $[a, a + 2^k)$ with $a$ a multiple of $2^k$. These blocks form a complete binary tree: the root is $[0, 2^m)$, and a block of order $k \ge 1$ has the two halves of order $k - 1$ as its children. The *buddy* of a block of order $k < m$ is its sibling in this tree.

**Lemma (the buddy address).** If $a$ is a multiple of $2^k$ and $k < m$, the buddy of the block $[a, a + 2^k)$ starts at $a \oplus 2^k$, where $\oplus$ is the bitwise exclusive or.

*Proof.* The parent starts at $q = a - (a \bmod 2^{k+1})$, a multiple of $2^{k+1}$, and its halves start at $q$ and $q + 2^k$. Because $a$ is a multiple of $2^k$, the bits $0$ to $k-1$ of $a$ are zero, and bit $k$ tells which half $a$ is. If bit $k$ is 0, then $a = q$, and $a \oplus 2^k = q + 2^k$. If bit $k$ is 1, then $a = q + 2^k$, and $a \oplus 2^k = q$. In both cases the result is the other half. $\square$

## The algorithm

The allocator keeps AVAIL$[k]$, the set of free blocks of order $k$, for $k = 0, \ldots, m$, and for each allocated block its order KVAL. At the start, AVAIL$[m] = \{0\}$ and the other sets are empty. This is Knuth's Algorithm R (lines L1 to L8) and Algorithm S (lines L9 to L15).

```pseudo id=main
BUDDY-MALLOC(n)                            ▷ returns an address or FAIL
L1  k ← ⌈lg n⌉                             ▷ the order of the block
L2  j ← the least j with k ≤ j ≤ m and AVAIL[j] not empty
L3  if there is no such j then return FAIL
L4  L ← remove a block from AVAIL[j]
L5  while j > k do
L6      j ← j − 1
L7      add L + 2^j to AVAIL[j]            ▷ the upper half stays free
L8  KVAL[L] ← k; return L

BUDDY-FREE(L)
L9  k ← KVAL[L]
L10 while k < m do
L11     P ← L xor 2^k                      ▷ the buddy of L
L12     if P is not in AVAIL[k] then exit the loop
L13     remove P from AVAIL[k]
L14     L ← min(L, P); k ← k + 1           ▷ the merged block starts at the lower half
L15 add L to AVAIL[k]
```

Line L2 looks for the smallest free block that is large enough. Lines L5 to L7 cut it in halves: the lower half is cut again, and the upper half goes to the free list of its order. Line L12 is the test for a free *and whole* buddy: the buddy must be on the list of order $k$, not only partly free. A buddy that is cut into smaller pieces, or that is in use, stops the merge.

In memory, each free block holds the links of its list, a tag bit that says "free", and its order. Then the test of line L12 reads the tag and the order at address $P$, and the lists are doubly linked so that line L13 takes $O(1)$ time. The order of an allocated block comes from a header, or the caller passes the size to free.

## Example

Take $m = 4$, so the heap has 16 words. The program asks for 3, 5 and 2 words, then frees the three blocks.

| step | call | what happens | free blocks (address of order k) |
|---|---|---|---|
| 0 | start | | 0 of order 4 |
| 1 | A = malloc(3) | $k = 2$; split 0 of order 4 twice; A = 0 | 8 of order 3, 4 of order 2 |
| 2 | B = malloc(5) | $k = 3$; take 8 from AVAIL[3]; B = 8 | 4 of order 2 |
| 3 | C = malloc(2) | $k = 1$; split 4 of order 2; C = 4 | 6 of order 1 |
| 4 | free(A) | buddy $0 \oplus 4 = 4$ is not on AVAIL[2] | 6 of order 1, 0 of order 2 |
| 5 | free(C) | buddy 6 is free: merge to 4 of order 2; buddy 0 is free: merge to 0 of order 3; buddy 8 is in use | 0 of order 3 |
| 6 | free(B) | buddy 0 is free: merge to 0 of order 4 | 0 of order 4 |

The program asked for $3 + 5 + 2 = 10$ words and got blocks of $4 + 8 + 2 = 14$ words. Block B alone loses 3 of its 8 words. There are 3 splits and 3 merges in total, and the last free gives back the whole heap.

## Correctness

Call a state *legal* when (T) the free and the allocated blocks are tree blocks that tile $[0, 2^m)$ with no gap and no overlap, and (B) no two free blocks are buddies. Each call keeps both. Line L4 and the splits replace one tree block with tree blocks that tile it. Lines L10 to L14 merge two buddies into their parent, which is a tree block, and they stop only when the buddy is not a free block of the same order, so (B) holds after line L15.

A stronger fact makes the buddy system easy to test: in a legal state, the free blocks are exactly the *maximal* tree blocks that hold no allocated word. So the free lists depend only on the set of allocated blocks, not on the order of the past calls. It follows that malloc$(n)$ fails only when no aligned block of $2^{\lceil \lg n \rceil}$ words is free, and that after all blocks are freed the heap is one free block of order $m$. The full proof is in the [correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/), with a word of at least $m + 1$ bits, so that an address and $2^k$ fit in one word.

- **malloc.** Line L2 checks at most $m + 1$ lists, and the loop of line L5 runs $j - k \le m$ times. So the time is $O(m)$ in the worst case. With a bitmap of the orders whose list is not empty, line L2 is one mask and one [trailing zero count](/trailing-zero-count/), and the time is $O(1 + j - k)$.
- **free.** Each pass of the loop of line L10 raises $k$ by one, so there are at most $m - k$ passes, each of $O(1)$ time. The time is $O(m)$ in the worst case.
- **Best case.** A request whose list is not empty and a free whose buddy is in use take $O(1)$ time.
- **Space.** The $m + 1$ list heads, and in each block a tag bit and the order, which needs $\lceil \lg(m+1) \rceil$ bits.

**Internal fragmentation.** A request of $n$ words gets $2^k$ words with $k = \lceil \lg n \rceil$. If $k \ge 1$, then $n > 2^{k-1}$, so the waste $2^k - n$ is less than $2^{k-1}$, that is, less than one half of the block. The bound is tight: a request of $2^{k-1} + 1$ words wastes $2^{k-1} - 1$ words. So the total size of the blocks is less than twice the total of the requests.

**External fragmentation.** A free block cannot merge with a free neighbor that is not its buddy. For example, if blocks 4 of order 2 and 8 of order 2 are free in a heap of 16 words, there are 8 free words in a row, but no block of order 3 is free. The worst case of any non-moving allocator is the subject of the [Robson bound](/robson-bound/).

## Properties

- **Aligned blocks.** Each block of $2^k$ words starts at a multiple of $2^k$. Kernels use this for page frames.
- **Canonical state.** The free lists are a function of the set of allocated blocks (see Correctness).
- **No search for a neighbor.** The merge needs only the XOR of line L11, not [boundary tags](/boundary-tags/) or an address-ordered list.
- **Immediate coalescing.** Each free merges as far as possible. The [lazy buddy system](/lazy-buddy-system/) delays some merges.

## Variants and improvements

- **Fibonacci buddies.** Block sizes follow a Fibonacci-like sequence, so the classes are closer together and less memory is lost to rounding. See the [Fibonacci buddy system](/fibonacci-buddy-system/).
- **Weighted and generalized buddies.** Peterson and Norman (1977) define a general class of buddy systems that includes the binary, the Fibonacci and the weighted buddy systems, and compare them by simulation.
- **Lazy buddies.** Keep some freed blocks unmerged on their list, so that a later request of the same size does not split again. See the [lazy buddy system](/lazy-buddy-system/) and [deferred coalescing](/deferred-coalescing/).
- **Buddy under a slab layer.** Many kernels use a buddy system for pages and a [slab allocator](/slab-allocator/) for small objects on top of it.

## When to use it

Use the buddy system when blocks must be aligned to their size, when the sizes are close to powers of two, and when a bounded time per call matters more than memory use. Page-frame allocators in kernels are the classic case. For small objects of many sizes, [segregated free lists](/segregated-free-lists/) with closer [size classes](/size-classes/), or a [slab allocator](/slab-allocator/), lose less memory. For real-time code that needs $O(1)$ calls and closer classes, use [TLSF](/tlsf/).

## Pitfalls

- **Merging with a split buddy.** Line L12 must check that the buddy is free with order exactly $k$. A test of only "the first word of the buddy is free" merges a block with a buddy that is cut into pieces, some of which are in use.
- **Wrong merged address.** Line L14 must take $\min(L, P)$. Keeping $L$ when $L$ is the upper half gives a block that is not aligned to its new size.
- **Forgetting the header.** If the allocator stores the order in a header inside the block, the usable size is $2^k$ minus the header. A request of exactly $2^k$ words then needs a block of order $k + 1$ and wastes almost one half.
- **Heap size not a power of two.** The algorithm needs a heap of $2^m$ words that starts at an aligned address. For other sizes, cover the heap with several buddy trees, one for each bit of the size.

## Implementations

## History

Knowlton published the binary buddy system in 1965. Knuth reports that H. Markowitz used the same idea in the Simscript system around 1963. Knuth gave the method as Algorithms R and S in Volume 1 of *The Art of Computer Programming* (1968) and suggested Fibonacci block sizes in an exercise, which Hirschberg developed in 1973. Peterson and Norman described the general class of buddy systems in 1977.

## References
