---
title: Quickselect returns the k-th smallest item
proves: [correctness, termination]
status: full
---

Let $S$ be the multiset of the items of the input, and let $s_0 \le s_1 \le \cdots \le s_{n-1}$ be $S$ in sorted order. The claim is: for $1 \le k \le n$, QUICKSELECT$(A, k)$ stops and returns $s_{k-1}$, and at the end $A$ is a permutation of $S$ with $A[k-1] = s_{k-1}$, each item of $A[0 \ldots k-2]$ at most $s_{k-1}$, and each item of $A[k \ldots n-1]$ at least $s_{k-1}$.

**Lemma (PARTITION).** Assume $hi - lo \ge 1$, and let $x$ be the item $A[hi-1]$ at the start. PARTITION$(A, lo, hi)$ permutes $A[lo \ldots hi-1]$, changes no other entry, and returns $p$ with $lo \le p < hi$, $A[p] = x$, each item of $A[lo \ldots p-1]$ at most $x$, and each item of $A[p+1 \ldots hi-1]$ greater than $x$.

*Proof.* Line L10 sets $x$. The loop of line L12 keeps this invariant at the start of the iteration for $j$: $lo \le i \le j$, each item of $A[lo \ldots i-1]$ is at most $x$, each item of $A[i \ldots j-1]$ is greater than $x$, and $A[hi-1] = x$.

1. *Initialization.* Line L11 sets $i = lo$ and the first value is $j = lo$, so both parts are empty.
2. *Maintenance.* If $A[j] > x$, the loop only increases $j$, so $A[j]$ joins the part of the greater items. If $A[j] \le x$, line L14 swaps $A[j]$ with $A[i]$, which is the first item of the greater part (or $A[j]$ itself if that part is empty). Then $A[i] \le x$ and the greater part moves one place to the right, so after line L15 both statements hold for $j + 1$. The index $j$ stays below $hi - 1$, so $A[hi - 1]$ does not change.
3. *Termination.* The loop runs for $j = lo, \ldots, hi - 2$, so it ends with $j = hi - 1$. Then $A[lo \ldots i-1] \le x$ and $A[i \ldots hi-2] > x$. Line L16 swaps $A[i]$ with $A[hi-1] = x$. If $i < hi - 1$, the item moved to $hi - 1$ is greater than $x$, so $A[i+1 \ldots hi-1] > x$. If $i = hi - 1$, the swap does nothing. In both cases the lemma holds with $p = i$.

Each step is a swap of two entries of $A[lo \ldots hi-1]$, so the range is permuted and no other entry changes. $\square$

**Invariant of the main loop.** At each test of line L2:

> **(Q)** $A$ is a permutation of $S$; $lo \le t < hi$; each item of $A[0 \ldots lo-1]$ is at most each item of $A[lo \ldots hi-1]$; and each item of $A[lo \ldots hi-1]$ is at most each item of $A[hi \ldots n-1]$.

*Consequence of (Q).* Let $B$ be the sorted list of the items of $A[lo \ldots hi-1]$. Exactly $lo$ items lie before the block and each is at most each item of $B$, and the $n - hi$ items after the block are at least each item of $B$. So the sorted order of $A$ is: a sorted order of $A[0 \ldots lo-1]$, then $B$, then a sorted order of $A[hi \ldots n-1]$. Hence $s_t = B[t - lo]$, the item of rank $t - lo + 1$ of the block.

1. *Initialization.* Line L1 sets $lo = 0$, $hi = n$ and $t = k - 1$, so $0 \le t < n$ and the outer parts are empty.
2. *Maintenance.* Assume (Q) and $hi - lo > 1$. Lines L3 and L4 swap two entries of the block. By the lemma, line L5 permutes the block and returns $p$ with $A[lo \ldots p-1] \le A[p] < A[p+1 \ldots hi-1]$. If $t = p$, line L6 returns; this case is treated below. If $t < p$, line L7 sets $hi \leftarrow p$. Then $lo \le t < p$. The items now right of the block are $A[p \ldots hi-1]$ of the old block, which are at least $A[p]$, which is at least each item of $A[lo \ldots p-1]$, and the old part $A[hi \ldots n-1]$, which (Q) bounds below by each item of the old block. So (Q) holds. If $t > p$, line L8 sets $lo \leftarrow p + 1$, and the argument is the mirror one: $A[lo \ldots p]$ of the old block is at most each item of $A[p+1 \ldots hi-1]$.
3. *Termination.* In each pass that does not return, the new range is a part of $[lo, hi)$ that does not hold $p$, so $hi - lo$ drops by at least 1. It starts at $n$, so the loop ends after at most $n - 1$ passes.

**Conclusion.** The run ends in one of two ways.

- *Line L6 returns $A[p]$ with $p = t$.* Write $lo, hi$ for the range of this pass. By the lemma, exactly $p - lo$ items of the block are at most $A[p]$ and lie before it, and the others are greater. So $A[p]$ is $B[p - lo] = B[t - lo]$, and by the consequence of (Q) it is $s_t$. The items before index $t$ are at most $s_t$ by (Q) and the lemma, and the items after it are at least $s_t$.
- *The loop stops with $hi - lo = 1$ and line L9 returns $A[lo]$.* By (Q), $lo \le t < hi = lo + 1$, so $t = lo$ and the block is $B = [A[t]]$. By the consequence of (Q), $A[t] = B[0] = s_t$, and (Q) gives the order of the other items.

In both cases the result is $s_t = s_{k-1}$, and $A$ is a permutation of $S$ because each step is a swap. The proof does not use the values of the random indices of line L3, so it holds for every sequence of random choices. $\blacksquare$
