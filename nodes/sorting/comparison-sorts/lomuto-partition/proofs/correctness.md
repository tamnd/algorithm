---
title: The Lomuto partition puts the pivot at its place and keeps the items
proves: [correctness]
status: full
---

**Claim.** Let $hi - lo = m \ge 1$, let $S$ be the multiset of the items of $A[lo \ldots hi-1]$ at the start, and let $x$ be the old $A[hi - 1]$. Then LOMUTO-PARTITION$(A, lo, hi)$ stops after $m - 1$ steps of its loop and returns an index $p$ with $lo \le p \le hi - 1$. After the call, $A[lo \ldots hi-1]$ holds $S$, $A[p] = x$, each item of $A[lo \ldots p-1]$ is at most $x$, and each item of $A[p+1 \ldots hi-1]$ is larger than $x$. No item outside the range changes.

*Proof.* Lines L1 and L2 set $x = A[hi - 1]$ and $i = lo$. We prove this invariant of the loop of line L3, before the step for $j$, for $j = lo, lo + 1, \ldots, hi - 1$:

> **(L)** $lo \le i \le j$. Each item of $A[lo \ldots i-1]$ is at most $x$. Each item of $A[i \ldots j-1]$ is larger than $x$. $A[hi-1] = x$. The range holds $S$, and nothing outside it has changed.

1. *Start.* For $j = lo$, we have $i = j = lo$, so both parts are empty. No line has changed the array.
2. *A large item.* Assume (L) for $j \le hi - 2$ and $A[j] > x$. The test of line L4 fails, and nothing changes. Now $A[i \ldots j]$ holds only items larger than $x$, so (L) holds for $j + 1$.
3. *A small item.* Assume (L) for $j \le hi - 2$ and $A[j] \le x$. If $i = j$, line L5 swaps $A[j]$ with itself, and after line L6 the left part $A[lo \ldots j]$ holds only items at most $x$, while the large part $A[j + 1 \ldots j]$ is empty. If $i < j$, then $A[i]$ is in the large part, so $A[i] > x$. Line L5 swaps $A[i]$ and $A[j]$, so now $A[i] \le x$ and $A[j] > x$. After line L6, the left part is $A[lo \ldots i]$ with the old $i$, all at most $x$, and the large part is $A[i + 1 \ldots j]$, all larger than $x$. In both cases (L) holds for $j + 1$. The swap uses indices $i \le j \le hi - 2$, so it does not touch $A[hi - 1]$ or any index outside the range.
4. *End.* The loop of line L3 runs for $j = lo, \ldots, hi - 2$, so it stops after exactly $m - 1$ steps, with (L) for $j = hi - 1$. So $A[lo \ldots i-1] \le x$, $A[i \ldots hi-2] > x$ and $A[hi - 1] = x$, with $lo \le i \le hi - 1$.
5. *The last swap.* Line L7 swaps $A[i]$ and $A[hi - 1]$. If $i = hi - 1$, nothing changes. If $i < hi - 1$, the old $A[i]$ is larger than $x$ and goes to index $hi - 1$, which is in $A[i+1 \ldots hi-1]$. In both cases, after the swap $A[i] = x$, $A[lo \ldots i-1] \le x$ and $A[i+1 \ldots hi-1] > x$.

Line L8 returns $p = i$. Each change was a swap of two indices in the range, so the range still holds $S$ and nothing outside it changed. $\blacksquare$

**Rank of the pivot.** The claim gives exactly $p - lo$ items at most $x$ other than $x$ itself. So when the items are distinct, $x$ has rank $p - lo + 1$ in the range, and $A[p]$ is the item that a sort of the range puts at index $p$.
