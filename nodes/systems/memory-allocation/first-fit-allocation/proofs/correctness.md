---
title: First-fit allocation keeps the heap invariants and returns the first block that fits
proves: [correctness]
status: full
---

We use the heap model and the pseudocode of the page. The heap is $mem[0 \ldots H-1]$ with $H \ge 4$. A block at $a$ with $s$ words has the tag $2s + u$ in $mem[a]$ and in $mem[a+s-1]$, where $u = 1$ for a used block and $u = 0$ for a free block. $MIN = 4$.

**Invariants.** Between two operations these hold:

> **(T)** Tiling. The walk $a_0 = 0$, $a_{i+1} = a_i + SIZE(a_i)$ reaches $H$ exactly. Each block has $SIZE \ge MIN$ and equal header and footer. So the blocks do not overlap and their sizes add up to $H$.
>
> **(L)** List. Following NEXT from $h.head$ visits each free block exactly once and no other address. PREV is the inverse of NEXT, and $h.tail$ is the last block. With the address order, the list is sorted by address.
>
> **(C)** Coalesced. No two adjacent blocks are both free.
>
> **(P)** Payloads. Each live pointer $p$ from an earlier malloc$(n)$ satisfies: the block at $p - 1$ is used and has at least $n + 2$ words.

*Initialization.* The constructor writes one free block $[0, H)$ and links it as the only list node. (T), (L) and (C) hold, and (P) holds because there is no live pointer.

**Lemma 1 (search).** Lines L2 to L4 return the first block in list order with $SIZE \ge need$, or NIL if no free block has $SIZE \ge need$.

*Proof.* Each iteration of line L3 either returns the current block $a$, which has $SIZE(a) \ge need$, or moves to $NEXT(a)$. The blocks before $a$ in the list were each tested and are too small. By (L) the walk visits each free block once and stops at NIL after at most $F$ steps, where $F$ is the length of the list. So the loop returns the first fit, or NIL when there is none. $\square$

With the address order, list order is address order, so first fit returns the free block of lowest address with $SIZE \ge need$.

**Lemma 2 (malloc keeps the invariants).** Let line L2 to L4 return $a$ with $s = SIZE(a) \ge need$.

- *Split* ($s - need \ge MIN$, lines L8 and L9). The words $[a, a+s)$ become two blocks, $[a, a+need)$ used and $[a+need, a+s)$ free, each with $SIZE \ge MIN$ and fresh tags at both ends. The walk of (T) now steps $a \to a + need \to a + s$, so (T) holds. The remainder takes the list place of $a$, with the same PREV and NEXT, so (L) holds; with the address order it is still sorted, because the remainder lies inside the old block, after its start and before the next free block. (C) holds: the remainder has the same right neighbour as the old free block, which was used by (C), and its left neighbour is the new used block.
- *No split* ($s - need < MIN$, line L10). The block is unlinked and its tags get $u = 1$. (T) holds with the same sizes. (L) holds because a used block left the list. (C) holds because a free block became used.

In both cases the returned block has at least $need \ge n + 2$ words, so (P) holds for the new pointer. Other used blocks are not changed. $\square$

**Lemma 3 (free keeps the invariants).** Let $p$ be live and $a = p - 1$. The block $[a, e)$ with $e = a + SIZE(a)$ is used. If $e < H$ and the block at $e$ is free, it is unlinked and $e$ grows by its size. If $a > 0$ and the footer $mem[a-1]$ has $u = 0$, then by (T) it is the footer of the block that ends at $a$; that block is unlinked and $a$ moves to its start. The words $[a, e)$ get one free tag and are linked.

(T) holds: the merged range is the union of adjacent whole blocks. (L) holds: each absorbed block was unlinked once, and the new block was linked once, in its address place for the address order. (C) holds: by (C) before the call, the block left of the merged range and the block right of it are used, because each was adjacent to a free block that we absorbed, or adjacent to the used block we freed and was tested. The only exception is a heap end, which has no neighbour. (P) holds for the other live pointers, because their blocks were not touched. $\square$

**Theorem.** After any sequence of first-fit malloc and free calls with valid pointers, (T), (L), (C) and (P) hold, and each malloc$(n)$ returns the payload of the first block in list order with at least $\max(MIN, n + 2)$ words, or NIL when no free block is that large.

*Proof.* By induction on the number of calls, with the initialization as the base and Lemmas 1 to 3 as the step. $\square$

**Failure is real.** When malloc returns NIL, no single free block has $need$ words. The total free space can still be larger than $need$; that is [external fragmentation](/external-fragmentation/), not an error of the search.
