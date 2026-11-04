---
title: Cocktail shaker sort sorts the array and stops
proves: [correctness, termination]
status: full
---

Each change of $A$ is an exchange of two items of $A$, so $A$ always holds a permutation of the input. It remains to show that the loop stops and that $A$ is then in non-decreasing order.

**Invariant.** At the test of line L2:

> **(I)** $A[0 \ldots lo-1]$ and $A[hi+1 \ldots n-1]$ are sorted. Each item of $A[0 \ldots lo-1]$ is at most each item of $A[lo \ldots n-1]$, and each item of $A[0 \ldots hi]$ is at most each item of $A[hi+1 \ldots n-1]$.

*Initialization.* $lo = 0$ and $hi = n - 1$, so both outer parts are empty, and (I) holds.

**Lemma 1 (the pass to the right).** Assume (I) and $lo < hi$ before line L3. After line L7, $A[hi+1 \ldots n-1]$ is sorted, with the new $hi$, and each item of $A[0 \ldots hi]$ is at most each item of $A[hi+1 \ldots n-1]$. The other parts of (I) still hold.

*Proof.* Let $h$ be the value of $hi$ before the pass. The loop of line L4 has this invariant: before the step for $j$, $A[j]$ is a maximum of $A[lo \ldots j]$. It holds for $j = lo$. If $A[j] > A[j+1]$, line L6 exchanges them, and then $A[j+1]$ is the old $A[j]$, a maximum of $A[lo \ldots j+1]$. If not, $A[j+1] \ge A[j]$ is a maximum. So it holds for $j + 1$.

Let $t$ be the final value of $last$. No exchange happened at a step $j > t$, so for each $j$ with $t < j < h$, the step found $A[j] \le A[j+1]$, and later steps did not touch $A[j]$. So $A[t+1 \ldots h]$ is sorted. After the step for $j = t$, $A[t+1]$ is a maximum of $A[lo \ldots t+1]$, and the later steps do not change $A[lo \ldots t+1]$. So each item of $A[lo \ldots t]$ is at most $A[t+1]$, which is at most each item of $A[t+1 \ldots h]$. The pass changes only $A[lo \ldots h]$, a permutation of its old items. By (I), these items are at most each item of $A[h+1 \ldots n-1]$, which is sorted. So $A[t+1 \ldots n-1]$ is sorted, and each item of $A[0 \ldots t]$ is at most each item of it: the items of $A[lo \ldots t]$ by the argument above, and the items of $A[0 \ldots lo-1]$ by (I). Line L7 sets $hi = t$. The left part $A[0 \ldots lo-1]$ did not change, and its items are at most each item of $A[lo \ldots n-1]$, because that part holds the same items as before. $\square$

**Lemma 2 (the pass to the left).** After line L12, (I) holds with the new $lo$ and $hi$.

*Proof.* This is the mirror image of Lemma 1. Let $h$ be the value of $hi$ after line L7. The loop of line L9 has the invariant: before the step for $j$, $A[j+1]$ is a minimum of $A[j+1 \ldots h]$. Let $t$ be the final value of $last$, so the last exchange was at $(t - 1, t)$, or $t = h$ if there was none. No exchange happened at a step $j < t - 1$, so $A[lo \ldots t-1]$ is sorted, and after the step for $j = t - 1$, $A[t-1]$ is a minimum of $A[t-1 \ldots h]$, which the later steps do not change. So $A[0 \ldots t-1]$ is sorted, and each of its items is at most each item of $A[t \ldots n-1]$. The pass changes only $A[lo \ldots h]$, so the right part of Lemma 1 still holds. If there was no exchange, $t = h$, and the claim is that $A[lo \ldots h-1]$ is sorted with each item at most $A[h]$: this holds because each step found $A[j] \le A[j+1]$. Line L12 sets $lo = t$. $\square$

By Lemmas 1 and 2, (I) holds at each test of line L2.

**Termination.** In a round with $lo < hi$, the pass to the right sets $hi$ to a value of $last$ in $[lo, hi-1]$, so $hi$ drops by at least 1. The pass to the left sets $lo$ to a value in $[lo, hi]$ with the new $hi$, so $lo$ does not drop. So $hi - lo$ drops by at least 1 in each round, and the loop stops after at most $n - 1$ rounds.

**Correctness at the end.** Line L12 sets $lo$ to a value of at most $hi$, so after a round $lo \le hi$. So when the loop stops, $lo = hi$, or $n = 0$ and there is nothing to sort. If $lo = hi$, the array is $A[0 \ldots lo-1]$, then $A[lo]$, then $A[lo+1 \ldots n-1]$. The two outer parts are sorted by (I). Each item of $A[0 \ldots lo-1]$ is at most each item to its right, and each item of $A[0 \ldots lo]$ is at most each item of $A[lo+1 \ldots n-1]$. So $A$ is sorted. $\blacksquare$
