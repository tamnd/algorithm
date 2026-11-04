---
title: Quicksort sorts the array and keeps its items
proves: [correctness]
status: full
---

We write $S$ for the multiset of the items of $A[lo \ldots hi-1]$ at the start of a call. Each step of the algorithm changes the array only by a swap, so the multiset of the items of the full array never changes.

**Lemma (PARTITION).** Assume that $hi - lo \ge 2$. Then PARTITION$(A, lo, hi)$ returns an index $p$ with $lo \le p \le hi - 1$. After the call, $A[lo \ldots hi-1]$ holds $S$, $A[p] = x$ (the old $A[hi-1]$), each item of $A[lo \ldots p-1]$ is at most $x$, and each item of $A[p+1 \ldots hi-1]$ is larger than $x$. No item outside $A[lo \ldots hi-1]$ changes.

*Proof.* Line L5 sets $x = A[hi-1]$, and line L6 sets $i = lo$. We use this invariant for the loop of line L7, before the step for $j$:

> **(P)** $lo \le i \le j \le hi - 1$. Each item of $A[lo \ldots i-1]$ is at most $x$. Each item of $A[i \ldots j-1]$ is larger than $x$. $A[hi - 1] = x$.

*Start.* For $j = lo$, both parts are empty and $i = j = lo$. Nothing has moved, so $A[hi-1] = x$.

*Step.* Assume (P) before the step for $j \le hi - 2$. If $A[j] > x$, the step changes nothing, and $A[i \ldots j]$ is a part of items larger than $x$. So (P) holds for $j + 1$. If $A[j] \le x$, line L9 swaps $A[i]$ and $A[j]$. If $i < j$, then $A[i]$ was in the part of larger items, so after the swap $A[i] \le x$ and $A[j] > x$. If $i = j$, the swap changes nothing. In both cases, after line L10, each item of $A[lo \ldots i-1]$ is at most $x$, and each item of $A[i \ldots j]$ is larger than $x$. So (P) holds for $j + 1$. The swap uses indices $i \le j \le hi - 2$, so $A[hi - 1]$ does not change.

*End.* The loop runs once for each $j$ from $lo$ to $hi - 2$, so it stops after $hi - 1 - lo$ steps with $j = hi - 1$. By (P), $A[lo \ldots i-1] \le x$, $A[i \ldots hi-2] > x$ and $A[hi-1] = x$. Line L11 swaps $A[i]$ and $A[hi-1]$. If $i < hi - 1$, the item at $i$ was larger than $x$, and it goes to index $hi - 1$, which is in the right part. If $i = hi - 1$, the swap changes nothing. So with $p = i$, the claim holds. All changes were swaps inside the range, so the range holds $S$ and nothing outside it changed. $\square$

**Theorem.** After QUICKSORT$(A, lo, hi)$, the part $A[lo \ldots hi-1]$ is sorted and holds $S$. No other item of $A$ changes.

*Proof.* By strong induction on $k = hi - lo$.

*Base.* If $k \le 1$, line L1 returns. A part with at most one item is sorted, and nothing changed.

*Step.* Let $k \ge 2$, and assume the claim for all ranges of length less than $k$. By the lemma, line L2 gives $p$ with $lo \le p \le hi - 1$, a left part $A[lo \ldots p-1]$ of items at most $x$, and a right part $A[p+1 \ldots hi-1]$ of items larger than $x$. The ranges of lines L3 and L4 have lengths $p - lo$ and $hi - p - 1$. Both are at most $k - 1$, because the index $p$ is in neither range. By the induction hypothesis, line L3 sorts the left part and changes nothing else, so it does not change $A[p]$ or the right part. It permutes the left part, so all its items are still at most $x$. In the same way, line L4 sorts the right part and keeps its items larger than $x$.

Now $A[lo \ldots p-1]$ is sorted with each item at most $x$, $A[p] = x$, and $A[p+1 \ldots hi-1]$ is sorted with each item larger than $x$. So $A[lo \ldots hi-1]$ is sorted. Each step was a swap inside the range, so it holds $S$. $\blacksquare$

**Termination.** Each call on a range of length $k \ge 2$ makes two calls on ranges of length at most $k - 1$. So the depth of the recursion is at most $n - 1$, and the algorithm stops.
