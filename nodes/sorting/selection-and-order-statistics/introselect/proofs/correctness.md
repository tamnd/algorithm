---
title: Introselect returns the k-th smallest item and stops
proves: [correctness, termination]
status: full
---

Let $S$ be the multiset of the input items and $s_0 \le s_1 \le \cdots \le s_{n-1}$ its sorted order. The claim is: for $1 \le k \le n$, INTROSELECT$(A, k)$ stops and returns $s_{k-1}$. We use two facts proved on their own pages: MOM-SELECT$(L, r)$ stops and returns the item of rank $r$ of a list $L$ ([median of medians](/median-of-medians/)), and PARTITION3$(B, lo, hi, x)$ permutes $B[lo \ldots hi-1]$, changes no other entry, and returns $(p, q)$ with $lo \le p \le q \le hi$, each item of $B[lo \ldots p-1]$ less than $x$, each item of $B[p \ldots q-1]$ equal to $x$, and each item of $B[q \ldots hi-1]$ greater than $x$ (the three-way template of [partition around a pivot](/partition-around-pivot/)).

**Invariant.** At each test of line L2:

> **(I)** $B$ is a permutation of $S$; $lo \le t < hi$; each item of $B[0 \ldots lo-1]$ is at most each item of $B[lo \ldots hi-1]$; and each item of $B[lo \ldots hi-1]$ is at most each item of $B[hi \ldots n-1]$.

*Consequence.* Under (I), a sorted order of $B$ is: a sorted order of $B[0 \ldots lo-1]$, then the sorted block $D$ of $B[lo \ldots hi-1]$, then a sorted order of $B[hi \ldots n-1]$. So $s_t = D[t - lo]$, the item of rank $t - lo + 1$ of the block.

1. *Initialization.* Line L1 sets $B$ to a copy of $A$, $lo = 0$, $hi = n$ and $t = k - 1$, so $0 \le t < n$ and the outer parts are empty.
2. *Maintenance.* Assume (I) and $hi - lo > 1$, and that lines L3 and L6 do not return. Line L4 picks $x$ among three items of the block, so $x$ is an item of the block. Line L5 gives $(p, q)$ as above, and since $x$ is in the block, $p < q$. Line L6 did not return, so $t < p$ or $t \ge q$. If $t < p$, line L8 sets $hi \leftarrow p$: then $lo \le t < p$, and the items now to the right of the block are $B[p \ldots hi-1]$ of the old block, which are at least $x$ and so at least each item of $B[lo \ldots p-1]$, together with the old right part, which (I) bounds below by each item of the old block. If $t \ge q$, line L8 sets $lo \leftarrow q$, and the argument is the mirror one. Line L9 changes only the counter. So (I) holds again.
3. *Termination.* Each pass that does not return replaces $[lo, hi)$ by $[lo, p)$ or $[q, hi)$, which leaves out the $q - p \ge 1$ copies of $x$. So $hi - lo$ drops by at least $1$, and the loop runs at most $n - 1$ passes.

**Conclusion.** The run ends in one of three ways.

- *Line L3 returns* MOM-SELECT$(B[lo \ldots hi-1], t - lo + 1)$. By (I), $1 \le t - lo + 1 \le hi - lo$, so the rank is valid, and the call stops and returns $D[t - lo]$, which is $s_t$ by the consequence of (I).
- *Line L6 returns $x$* with $p \le t < q$. After line L5 the block is $B[lo \ldots p-1] < x$, then $q - p$ copies of $x$, then $B[q \ldots hi-1] > x$, so the sorted block $D$ has $D[i - lo] = x$ for $p \le i < q$. The partition kept (I) true, since it only permuted the block, so by the consequence of (I), $s_t = D[t - lo] = x$.
- *The loop stops with $hi - lo = 1$ and line L10 returns $B[lo]$.* By (I), $lo \le t < lo + 1$, so $t = lo$ and $D = [B[lo]]$; by the consequence of (I), $s_t = B[lo]$.

In each case the result is $s_t = s_{k-1}$. $\blacksquare$
