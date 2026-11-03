---
title: Merge sort sorts the array and keeps its items
proves: [correctness]
status: full
---

We write $S$ for the multiset of the items of $A[lo \ldots hi-1]$ at the start of a call.

**Lemma (MERGE).** Assume that $lo \le mid \le hi$, and that $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$ are sorted. Then after MERGE$(A, lo, mid, hi)$, $A[lo \ldots hi-1]$ is sorted and holds $S$. No other item of $A$ changes.

*Proof.* Let $m = mid - lo$. Line L6 makes $B = A[lo \ldots mid-1]$, so $|B| = m$. Line L7 sets $i = 0$, $j = mid$ and $k = lo$. We use this invariant for the loops of lines L8 and L12:

> **(M)** $k = lo + i + (j - mid)$. The part $A[lo \ldots k-1]$ holds $B[0 \ldots i-1]$ and the old $A[mid \ldots j-1]$, in sorted order. Each item of $A[lo \ldots k-1]$ is at most each item of $B[i \ldots m-1]$ and at most each item of $A[j \ldots hi-1]$. The part $A[j \ldots hi-1]$ is not changed.

At the start, $k = lo$ and the part is empty, so (M) is true. The first equation gives $k - j = lo + i - mid \le lo + m - mid = 0$, so $k \le j$. A write to $A[k]$ therefore never changes an item at an index of $j$ or more, before it is read.

In a step of line L8, both $B[i]$ and $A[j]$ exist. By (M) and because both parts are sorted, the smallest item that is not yet placed is $B[i]$ or $A[j]$. Line L9 or line L10 writes the smaller one to $A[k]$, so $A[lo \ldots k]$ is sorted and the third statement stays true. Line L11 and the update of $i$ or $j$ keep the first equation. If both items are equal, line L9 takes $B[i]$, which comes from the left half.

The loop of line L8 stops when $i = m$ or $j = hi$. If $i = m$, then $k = j$ and the loop of line L12 does not run. The items $A[j \ldots hi-1]$ are in place: they are not changed, they are sorted, and by (M) they are at least each placed item. If $j = hi$, the loop of line L12 copies $B[i \ldots m-1]$ to $A[k \ldots hi-1]$ in order, and each of these items is at least each placed item. In both cases $A[lo \ldots hi-1]$ is sorted, and it holds all of $B$ and all of the old right half, so it holds $S$. $\square$

**Theorem.** After MERGE-SORT$(A, lo, hi)$, the part $A[lo \ldots hi-1]$ is sorted and holds $S$. No other item of $A$ changes.

*Proof.* By strong induction on $k = hi - lo$. If $k \le 1$, line L1 returns, and a part with at most one item is sorted. If $k \ge 2$, line L2 gives $lo < mid < hi$, so both calls of lines L3 and L4 have a shorter range. By the induction hypothesis, they sort $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$, and each call changes only its own part. The lemma then shows that line L5 makes $A[lo \ldots hi-1]$ sorted, with the items of $S$. $\blacksquare$

**Stability.** Equal items in the same half keep their order by the induction hypothesis. For equal items in different halves, line L9 places the item of the left half first.
