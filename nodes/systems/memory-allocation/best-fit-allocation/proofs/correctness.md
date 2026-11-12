---
title: Best-fit allocation returns the smallest block that fits and keeps the heap invariants
proves: [correctness]
status: full
---

We use the heap model of the page and the invariants of [first-fit allocation](/first-fit-allocation/): (T) the blocks tile $[0, H)$ with matching header and footer; (L) the free list holds each free block exactly once, with consistent links; (C) no two free blocks are adjacent; (P) each live pointer lies in a used block that is large enough.

**Lemma 1 (the list scan).** Let $L = (b_0, \ldots, b_{F-1})$ be the free list in order. Lines L2 to L7 return NIL if no $b_i$ has $SIZE(b_i) \ge need$. Otherwise they return the first block in $L$ whose size is the least size $m$ among the blocks that fit.

*Proof.* Consider the loop before it visits $b_j$. Claim: $best$ is NIL if none of $b_0, \ldots, b_{j-1}$ fits, and otherwise it is the first block among them with the least fitting size. This holds for $j = 0$. At $b_j$, line L4 replaces $best$ only when $b_j$ fits and is strictly smaller than $best$, so ties keep the earlier block and the claim holds for $j + 1$. If the loop runs to the end, the claim for $j = F$ is the lemma. If line L6 stops the loop at $b_j$, then $SIZE(b_j) = need$. No fitting block is smaller than $need$, so $m = need$, and by the claim no earlier block had size $need$, so $b_j$ is the first block of size $m$. $\square$

With an address-ordered list, the result of Lemma 1 is the fitting block with the least size and, among those, the lowest address.

**Lemma 2 (the index).** In IndexedHeap, between operations the index is the sorted list of the pairs $(SIZE(a), a)$ over the free blocks $a$.

*Proof.* The free list changes only through link, unlink and replace, and each of them updates the index at the same time. At each call the header of the block named holds its current size: link is called after the new block is tagged; unlink is called before the block is retagged; replace is called after the remainder is tagged and before the old block is retagged. So the pair added or removed is the correct one, and insertion in sorted position keeps the order. $\square$

**Lemma 3 (the indexed search).** The binary search returns the second component of the first pair $(s, a)$ in the index with $s \ge need$, or NIL if there is none. This is the fitting block with the least size and, among those, the lowest address.

*Proof.* The index is sorted by Lemma 2, so the pairs with $s < need$ form a prefix. The loop keeps the condition that every pair before $lo$ has $s < need$ and every pair from $hi$ on has $s \ge need$; it ends with $lo = hi$ at the end of the prefix. Pairs are ordered by size first and address second, so the first pair after the prefix has the least fitting size and the lowest address among the blocks of that size. $\square$

**Theorem.** After any sequence of best-fit malloc and free calls with valid pointers, (T), (L), (C) and (P) hold. Each malloc$(n)$ returns the payload of a free block with the least size $m \ge \max(MIN, n + 2)$, the lowest address among those when the list is address ordered or the index is used, or NIL when no free block is large enough.

*Proof.* Best fit uses the same split and the same free as first fit, and the proofs of (T), (L), (C) and (P) on the first-fit page do not depend on which fitting block the search returns. The choice is the one of Lemma 1 or Lemma 3. Induction on the number of calls completes the proof. $\square$
