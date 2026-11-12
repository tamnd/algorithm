---
tag: R8K8RA
kind: algorithm
slug: fibonacci-buddy-system
name: Fibonacci buddy system
aliases:
- Fibonacci buddy
- Fibonacci buddies
area: systems/memory-allocation
level: advanced
summary: "A buddy system whose block sizes are Fibonacci numbers. A block of size F(k) splits into F(k-1) and F(k-2), so the size classes are closer than powers of two."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {m: "the order of the heap, which has S(m) words", n: the requested size in words}
  time: {worst: O(m), best: O(1)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1973
  people: [Daniel S. Hirschberg]
  note: Knuth suggested Fibonacci block sizes in an exercise of TAOCP Volume 1, and Hirschberg designed and tested the Fibonacci buddy system in 1973.
prereqs: [buddy-system, fibonacci-numbers]
see_also: [buddy-system, lazy-buddy-system, size-classes, internal-fragmentation, external-fragmentation, segregated-free-lists]
sources:
  - paper: doi:10.1145/362375.362392
    title: Daniel S. Hirschberg, A class of dynamic memory allocation algorithms, Communications of the ACM 16(10), 615-618, 1973
    locator: the Fibonacci system and its comparison with the binary buddy system
  - paper: doi:10.1145/359605.359626
    title: James L. Peterson and Theodore A. Norman, Buddy systems, Communications of the ACM 20(6), 421-431, 1977
    locator: the general class of buddy systems, which contains the binary, the Fibonacci and the weighted buddy systems
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986
    locator: Section 3.7, Buddy systems (Fibonacci and generalized Fibonacci buddies), and Section 4.1 (Hirschberg 1973, about 25 percent against 38 percent; Knuth's Exercise 2.5.31)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Algorithms R and S (the binary buddy system), and Exercise 31 (Fibonacci block sizes)
---

The Fibonacci buddy system is a [buddy system](/buddy-system/) whose block sizes are the [Fibonacci numbers](/fibonacci-numbers/) $1, 2, 3, 5, 8, 13, \ldots$ instead of powers of two. A block of size $S_k$ splits into two buddies of sizes $S_{k-1}$ and $S_{k-2}$, and two free buddies merge back into their parent. Because consecutive sizes differ by a factor near $1.618$ and not $2$, a request loses less to rounding. The price is that the buddy of a block is no longer at a fixed bit flip of its address, so each block keeps two extra bits to find it.

## In plain words

The binary buddy system cuts a piece of memory into two equal halves. The Fibonacci buddy system cuts it into two unequal parts whose sizes are the two previous numbers of the Fibonacci sequence. So a piece of 13 words gives pieces of 8 and 5, a piece of 8 gives 5 and 3, and so on.

The sizes are closer together than with halves, so a request is rounded up less. When a piece comes back and its partner is free and whole, the two glue back together. Unlike halves, the two parts have different sizes, so a piece must know if it is the left or the right part to find its partner. Two small marks in each piece keep this knowledge across cuts and joins.

## The problem

The heap has $S_m$ words, with addresses $0$ to $S_m - 1$, where

$$S_0 = 1, \quad S_1 = 2, \quad S_k = S_{k-1} + S_{k-2} \ (k \ge 2).$$

So $S_k = F_{k+2}$, the Fibonacci numbers from $1, 2$ on. The program calls malloc$(n)$ and free$(p)$ as in the [online memory allocation](/online-memory-allocation/) problem, and blocks never move.

The possible blocks form a fixed tree. The root is $[0, S_m)$ of order $m$. A block $[a, a + S_k)$ of order $k \ge 2$ has a *left* child $[a, a + S_{k-1})$ of order $k - 1$ and a *right* child $[a + S_{k-1}, a + S_k)$ of order $k - 2$. Blocks of order 0 and 1 are not split. The two children are *buddies*. A block is fixed by its address and order, because the blocks that start at the same address form a chain of left children with different orders.

**Finding the buddy.** A left block of order $k$ has a parent of order $k + 1$, so its buddy is the right block of order $k - 1$ at $a + S_k$. A right block of order $k$ has a parent of order $k + 2$, so its buddy is the left block of order $k + 1$ at $a - S_{k+1}$. So the address, the order and one bit LR (left or right) find the buddy. To know LR of a parent after a merge, each block also keeps an *inheritance bit* IN, with the rule

$$\text{split of } (LR, IN) \to \text{left } (0,\ LR), \ \text{right } (1,\ IN); \qquad \text{merge of left } (0, x) \text{ and right } (1, y) \to (x,\ y).$$

The merge gives back exactly the bits that the split took apart, so the bits are right at each time. This two-bit scheme is the one that course notes and textbooks commonly use, and it is close to the simplified recombination scheme of Cranston and Thomas (1975).

## The algorithm

AVAIL$[k]$ is the set of free blocks of order $k$. Each block holds its order and its two bits. At the start, AVAIL$[m]$ holds the root with bits $(0, 0)$.

```pseudo id=main
FIB-MALLOC(n)
L1  k ← the least k with S[k] ≥ n                ▷ FAIL if S[m] < n
L2  j ← the least j with k ≤ j ≤ m and AVAIL[j] not empty
L3  if there is no such j then return FAIL
L4  a ← remove a block from AVAIL[j]; (LR, IN) ← its bits
L5  while j ≥ 2 and j − 1 ≥ k do                ▷ a child still fits
L6      left ← (a, j − 1, bits 0, LR); right ← (a + S[j − 1], j − 2, bits 1, IN)
L7      if j − 2 ≥ k then add left to AVAIL[j − 1]; continue with right
L8      else add right to AVAIL[j − 2]; continue with left
L9  mark the block (a, j) as allocated; return a

FIB-FREE(a)
L10 (j, LR, IN) ← the order and the bits of the block at a
L11 while j < m do
L12     if LR = 0 then (b, i) ← (a + S[j], j − 1) else (b, i) ← (a − S[j + 1], j + 1)
L13     if b is not in AVAIL[i] then exit the loop
L14     remove b from AVAIL[i]
L15     let x be the IN bit of the left one and y the IN bit of the right one
L16     a ← min(a, b); j ← (order of the left one) + 1; (LR, IN) ← (x, y)
L17 add (a, j) with bits (LR, IN) to AVAIL[j]
```

Lines L5 to L8 walk down the tree. At each split, they keep the smaller child if it still holds the request, and the larger child if only that one holds it. The other child goes to its free list. The loop stops when no child fits, or at order 0 or 1, which cannot be split. Line L12 is the buddy rule above, and line L13 checks that the buddy is free and whole: free with exactly the expected order.

## Example

Take $m = 5$, so the heap has $S_5 = 13$ words. The program asks for 3, 4 and 2 words, then frees the blocks in the order A, B, C.

| step | call | what happens | free blocks (address of order k) |
|---|---|---|---|
| 0 | start | | 0 of order 5 |
| 1 | A = malloc(3) | $k = 2$; split 13 into 8 + 5, keep the right 5 at 8; split 5 into 3 + 2, keep the left 3 at 8 | 0 of order 4, 11 of order 1 |
| 2 | B = malloc(4) | $k = 3$; split 8 at 0 into 5 + 3, keep the left 5 at 0 | 11 of order 1, 5 of order 2 |
| 3 | C = malloc(2) | $k = 1$; take 11 from AVAIL[1] | 5 of order 2 |
| 4 | free(A) | A is a left block of order 2; its buddy 11 of order 1 is in use | 5 and 8 of order 2 |
| 5 | free(B) | B is a left block of order 3; buddy 5 of order 2 is free: merge to 0 of order 4; its buddy 8 of order 3 is not free | 8 of order 2, 0 of order 4 |
| 6 | free(C) | C is a right block of order 1; buddy 8 of order 2 is free: merge to 8 of order 3; buddy 0 of order 4 is free: merge to the root | 0 of order 5 |

After step 4, the blocks 5 and 8 of order 2 are free and next to each other, but they are not buddies, so they do not merge. This is the [external fragmentation](/external-fragmentation/) of every buddy system. Request A of 3 words gets exactly 3 words here; the binary system would give it 4.

## Correctness

The proof follows the one of the binary buddy system. A state is *legal* when the free and the allocated blocks are blocks of the tree that tile the heap, each block carries the bits that the tree gives it, and no two free blocks are buddies. Each call keeps a legal state: a split replaces a block with its two children and sets their bits by the rule, and a merge does the reverse and restores the bits of the parent. In a legal state, the free blocks are exactly the maximal blocks of the tree that hold no allocated word. So the free lists depend only on the set of allocated blocks, malloc fails only when no tree block of a large enough order is free, and freeing all blocks gives back the root. The full proof is in the [correctness proof](proofs/correctness.md).

## Complexity

In the [word RAM](/word-ram/), the order $m$ is about $\log_\varphi S_m$ with $\varphi = (1 + \sqrt 5)/2$, because $S_k = F_{k+2}$ grows as $\varphi^k$. So $m \approx 1.44 \lg S_m$, about 44 percent more classes than the binary system for the same heap.

- **malloc.** Line L1 is a table lookup or a search of $O(m)$ steps, line L2 checks at most $m + 1$ lists, and each pass of line L5 lowers $j$ by at least 1. The time is $O(m)$ in the worst case.
- **free.** Each pass of line L11 merges two buddies into a parent of a higher order, so there are at most $m$ passes, and the time is $O(m)$.
- **Space.** The $m + 1$ list heads, the table of $S_k$, and in each block its order, a free tag and the two bits.

**Internal fragmentation.** Let $n \ge 3$ and let $k$ be the least order with $S_k \ge n$, so $k \ge 2$ and $S_{k-1} < n$. Then the waste is $S_k - n < S_k - S_{k-1} = S_{k-2}$, and

$$\frac{S_{k-2}}{S_k} \le \frac{2}{5} \quad (k \ge 2),$$

with equality at $k = 3$. To see this, write $5 S_{k-2} \le 2 S_k$ as $3 S_{k-2} \le 2 S_{k-1}$. It holds for $k = 2$ ($3 \le 4$) and $k = 3$ ($6 \le 6$). For $k \ge 4$, $S_{k-1} = S_{k-2} + S_{k-3}$ and $S_{k-2} = S_{k-3} + S_{k-4} \le 2 S_{k-3}$, so $2 S_{k-1} = 2 S_{k-2} + 2 S_{k-3} \ge 3 S_{k-2}$. As $k$ grows, the ratio tends to $1/\varphi^2 \approx 0.382$. So the waste is less than 40 percent of the block, against almost 50 percent for powers of two. One edge case remains: a request of 1 word that finds no free block of order 0 gets a block of order 1 and wastes half of it.

## Properties

- **Closer size classes.** The ratio of consecutive sizes tends to $\varphi \approx 1.618$.
- **Canonical state.** As in the binary system, the free lists are a function of the set of allocated blocks.
- **Unequal buddies.** A free block of order $k$ can only merge with a buddy of order $k - 1$ or $k + 1$, so free blocks of the same size next to each other often do not merge (step 4 of the example).
- **No alignment.** Block addresses are not multiples of their sizes, so the scheme does not give the natural alignment that page allocators need.

## Variants and improvements

- **Generalized Fibonacci buddies.** Hirschberg also proposed sizes with $L_i = L_{i-1} + L_{i-k}$ for a fixed $k$. With $k = 1$ this is the binary system, and with $k = 2$ it is the Fibonacci system. Larger $k$ gives closer classes and more unequal splits.
- **Weighted buddies.** Shen and Peterson (1974) mix sizes $2^k$ and $3 \cdot 2^k$. Peterson and Norman (1977) define the general class of buddy systems and compare these variants by simulation.
- **Lazy merging.** As with the binary system, merges can be delayed; see the [lazy buddy system](/lazy-buddy-system/).

## When to use it

Use the Fibonacci buddy system when the bounded time and the simple merge rule of a buddy system are wanted, but powers of two waste too much memory for the sizes of the program. It rarely appears in production allocators today. Allocators that need close classes usually use [size classes](/size-classes/) with [segregated free lists](/segregated-free-lists/), or [TLSF](/tlsf/), whose classes are much closer and whose calls also take $O(1)$ time. In Hirschberg's simulation, as Wilson et al. report it, fragmentation raised memory usage by about 25 percent with Fibonacci buddies and by about 38 percent with binary buddies. Wilson et al. also note a possible disadvantage: when a block is split for a request, the other part has a different size, so it is less useful to a program that allocates many objects of the same size.

## Pitfalls

- **Wrong buddy order.** The buddy of a left block of order $k$ has order $k - 1$, and the buddy of a right block has order $k + 1$ (line L12). Looking for a buddy of the same order $k$, as in the binary system, never finds it.
- **Losing the bits.** The merge of line L16 must take LR from the inheritance bit of the *left* child and IN from the inheritance bit of the *right* child. Swapping them gives a parent that looks for its buddy on the wrong side.
- **Equal sizes at the bottom.** With the classic sequence $1, 1, 2, 3, \ldots$ two orders have the same size, and the order is no longer fixed by the size. The sequence $1, 2, 3, 5, \ldots$ used here avoids this.

## Implementations

## History

Knuth suggested a buddy system with Fibonacci sizes in an exercise of Section 2.5 of *The Art of Computer Programming*, Volume 1. Hirschberg followed the suggestion in 1973: he designed the Fibonacci buddy system, compared it with the binary system in simulations, and proposed the generalization to Fibonacci-like sequences. Cranston and Thomas simplified the recombination step in 1975. Peterson and Norman placed the binary, the Fibonacci and the weighted systems in one general class of buddy systems in 1977.

## References
