---
title: Worst fit returns the largest free block when it fits and keeps the heap invariants
proves: [correctness]
status: full
---

We use the heap model of the page and the invariants of [first-fit allocation](/first-fit-allocation/): (T) the blocks tile $[0, H)$ with matching header and footer; (L) the free list holds each free block exactly once, with consistent links; (C) no two free blocks are adjacent; (P) each live pointer lies in a used block that is large enough.

**Lemma 1 (the scan).** Let $L = (b_0, \ldots, b_{F-1})$ be the free list in order. Lines L2 to L6 return NIL if no block has $SIZE \ge need$. Otherwise they return the first block in $L$ whose size is the largest size on the list.

*Proof.* Before the loop visits $b_j$, $best$ is NIL if none of $b_0, \ldots, b_{j-1}$ fits, and otherwise it is the first block among them with the largest fitting size. This holds for $j = 0$. At $b_j$, line L4 replaces $best$ only when $b_j$ fits and is strictly larger, so ties keep the earlier block, and the claim holds for $j + 1$. For $j = F$ the claim gives the first block of the largest fitting size. The largest block on the list fits if any block fits, so the largest fitting size is the largest size on the list. $\square$

**Theorem.** After any sequence of worst-fit malloc and free calls with valid pointers, (T), (L), (C) and (P) hold. Each malloc$(n)$ returns the payload of a largest free block, the one of lowest address when the list is address ordered, or NIL when that block has fewer than $\max(MIN, n + 2)$ words.

*Proof.* Worst fit uses the same split and the same free as first fit, and the proofs of (T), (L), (C) and (P) on the first-fit page do not depend on which fitting block the search returns. The choice is the one of Lemma 1. Induction on the number of calls completes the proof. $\square$

**Remark (no policy dominates).** On the heap with free blocks of 8 and 12 words, the needs 4, 12 succeed under best fit and fail under worst fit, and the needs 4, 8, 8 fail under best fit and succeed under worst fit. So neither policy serves every sequence that the other serves.
