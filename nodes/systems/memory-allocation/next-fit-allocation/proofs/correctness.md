---
title: Next-fit allocation keeps the heap invariants and returns the first fit after the rover
proves: [correctness]
status: full
---

We use the heap model of the page and the invariants of [first-fit allocation](/first-fit-allocation/): (T) the blocks tile $[0, H)$ with matching header and footer; (L) the free list holds each free block exactly once, with consistent links; (C) no two free blocks are adjacent; (P) each live pointer lies in a used block that is large enough. Next fit adds one invariant.

> **(R)** The rover is NIL or a block on the free list.

*Initialization.* The rover starts as NIL, so (R) holds.

**Lemma 1 (search).** Let $L = (b_0, b_1, \ldots, b_{F-1})$ be the free list in order, and let $b_k$ be the rover, or $k = 0$ if the rover is NIL. Lines L2 to L9 return the first block with $SIZE \ge need$ in the cyclic order $b_k, b_{k+1}, \ldots, b_{F-1}, b_0, \ldots, b_{k-1}$, or NIL if no free block has $SIZE \ge need$.

*Proof.* If the list is empty, line L3 returns NIL. Otherwise $start = b_k$, by (R) a list block. Line L7 moves from $b_i$ to $b_{i+1}$, and line L8 moves from $b_{F-1}$ to $b_0$, so the loop visits the blocks in the cyclic order above. Line L5 returns the first visited block that fits. Line L9 stops the loop when it comes back to $start$, which happens after exactly $F$ visits, so each block is tested once and NIL means that no block fits. $\square$

**Lemma 2 (the rover stays on the list).** Each change of the list keeps (R).

*Proof.* The list changes in four ways. (a) A split: the remainder takes the list place of the chosen block, and the procedure that does this moves the rover to the remainder when the rover named the chosen block. Line L6 set the rover to the chosen block, so after a split the rover is the remainder, a list block. (b) A block is unlinked (used whole, or absorbed by a merge): if the rover named it, the rover moves to its successor on the list, which is a list block or NIL. Unlinking another block does not change the rover, and the rover's block stays on the list. (c) A block is linked: the rover does not change, and its block stays on the list. (d) A failed search does not change the list or the rover. In each case (R) holds after the change. $\square$

**Theorem.** After any sequence of next-fit malloc and free calls with valid pointers, (T), (L), (C), (P) and (R) hold, and each malloc$(n)$ returns the payload of the first block with at least $\max(MIN, n + 2)$ words in the cyclic list order that starts at the rover, or NIL when no free block is that large.

*Proof.* Next fit uses the same split and the same free as first fit, so the proofs of (T), (L), (C) and (P) on the first-fit page apply word for word; they do not depend on which free block the search chose, only on its size being at least $need$. (R) holds by Lemma 2, and the choice is the one of Lemma 1. Induction on the number of calls completes the proof. $\square$

**Remark (failure is exact).** By Lemma 1, next fit fails only when no free block has $need$ words, the same condition as first fit, best fit and worst fit on the same heap. On a later request the heaps of the policies differ, so one policy can fail where another succeeds.
