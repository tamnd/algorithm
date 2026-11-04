---
title: Hoare partition stays in range, stops, and splits the range correctly
proves: [correctness, termination]
status: full
---

Let $lo < hi$ and let $x = A[lo]$ at the call. A *round* is one pass through lines L4 to L7. Each change of $A$ is an exchange of two items of $A[lo \ldots hi]$, so the multiset of the range never changes, and no item outside the range changes. These are the three properties of CLRS, Problem 7-1.

**Claim.** (a) Lines L4 and L5 read only indices in $[lo, hi]$. (b) The call stops and returns $j$ with $lo \le j < hi$. (c) At the return, each item of $A[lo \ldots j]$ is at most $x$, and each item of $A[j+1 \ldots hi]$ is at least $x$. So each item of $A[lo \ldots j]$ is at most each item of $A[j+1 \ldots hi]$.

**The first round.** The scan of line L4 starts at $j = hi$ and moves left. $A[lo] = x \le x$, so it stops at some $j_1 \ge lo$. The scan of line L5 starts at $i = lo$, and $A[lo] = x \ge x$ (the exchange of this round has not happened yet), so it stops at once with $i_1 = lo$. Both scans read only indices in $[lo, hi]$. If $i_1 \ge j_1$, then $j_1 = lo$, and line L7 returns $lo$, which is less than $hi$. The items $A[j_1+1 \ldots hi]$ were passed by the scan of $j$, so they are greater than $x$, and $A[lo] = x$. So (c) holds. Otherwise $lo = i_1 < j_1$, and line L6 exchanges $A[lo]$ and $A[j_1]$. After it, $A[lo]$ is the old $A[j_1] \le x$, and $A[j_1]$ is $x$.

**Invariant.** At the start of each round after the first, with the current $i$ and $j$:

> **(P)** $lo \le i < j \le hi$. Each item of $A[lo \ldots i]$ is at most $x$, and each item of $A[j \ldots hi]$ is at least $x$.

*Initialization.* After the first round with an exchange, $i = lo$ and $j = j_1$. $A[lo] \le x$. The items $A[j_1+1 \ldots hi]$ are greater than $x$, and $A[j_1] = x$. So (P) holds.

*A round.* Assume (P). The scan of line L4 starts at $j - 1 \ge i$ and moves left. The item $A[i]$ is at most $x$, so the scan stops at some $j' \ge i$. It passed the items $A[j'+1 \ldots j-1]$, which are greater than $x$. So each item of $A[j'+1 \ldots hi]$ is at least $x$, and $j' + 1 \le j \le hi$. The scan of line L5 starts at $i + 1 \le j' + 1$ and moves right. The item $A[j'+1]$ is at least $x$, so the scan stops at some $i' \le j' + 1 \le hi$. It passed the items $A[i+1 \ldots i'-1]$, which are less than $x$. So each item of $A[lo \ldots i'-1]$ is at most $x$. Both scans read only indices in $[lo, hi]$, which proves (a) for this round.

If $i' < j'$, line L6 exchanges $A[i']$ and $A[j']$. Before the exchange $A[i'] \ge x$ and $A[j'] \le x$, so after it $A[i'] \le x$ and $A[j'] \ge x$. So $A[lo \ldots i']$ is at most $x$ and $A[j' \ldots hi]$ is at least $x$, with $lo \le i' < j' \le hi$, and (P) holds for the next round.

If $i' \ge j'$, line L7 returns $j'$. Then $j' \le i' - 1$ or $j' = i'$. In both cases each item of $A[lo \ldots j']$ is at most $x$: the items up to $i' - 1$ by the scan of $i$, and $A[j']$ itself because the scan of $j$ stopped there. Each item of $A[j'+1 \ldots hi]$ is at least $x$, as shown above. So (c) holds. Also $j' \ge i \ge lo$, and $j' < j \le hi$, so $lo \le j' < hi$, which is (b) in this case.

**Termination.** In each round with an exchange, $i$ grows by at least 1 and $j$ drops by at least 1, so $j - i$ drops by at least 2. While (P) holds, $j - i \ge 1$. So after at most $\lceil (hi - lo)/2 \rceil + 1$ rounds, the test of line L6 fails, and the call returns. $\blacksquare$

**Consequence for quicksort.** Since $lo \le j < hi$, both ranges $[lo, j]$ and $[j+1, hi]$ are not empty and are strictly shorter than $[lo, hi]$. By (c) and induction on the length, quicksort that sorts both ranges sorts $A[lo \ldots hi]$.
