---
title: Merge path computes the stable merge
proves: [correctness]
status: full
---

Let $C$ be the stable merge of the sorted arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$, in which $u$ comes before $v$ if $u$ has a smaller key, or the keys are equal and $u$ is in $A$ and $v$ in $B$, or both are in the same array and $u$ has the smaller index.

## Lemma 1. Co-ranks exist and are unique

For each $k$ with $0 \le k \le m + n$, there is exactly one pair $(i, j)$ with $i + j = k$ such that the first $k$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$. Moreover $\max(0, k - n) \le i \le \min(k, m)$.

*Proof.* The stable order lists the items of $A$ in index order, so the items of $A$ among the first $k$ items of $C$ are a prefix $A[0 \ldots i-1]$, and the same holds for $B$ with some $j$. Since there are $k$ items in all, $i + j = k$, and the pair is fixed by $C$. From $0 \le i \le m$, $0 \le j \le n$ and $j = k - i$ follows the range of $i$. $\square$

## Lemma 2. The test on line L4

Let $\max(0, k - n) \le i < \min(k, m)$. Then $B[k - i - 1] < A[i]$ holds exactly when $A[i]$ is not among the first $k$ items of $C$.

*Proof.* The bounds give $0 \le k - i - 1 \le n - 1$, so $B[k-i-1]$ exists. The items before $A[i]$ in $C$ are $A[0], \ldots, A[i-1]$ and the items of $B$ with key less than $A[i]$, as items of $B$ with equal key come after $A[i]$. So $A[i]$ is at position $i + q$, where $q$ is the number of items of $B$ less than $A[i]$. It is among the first $k$ items when $i + q < k$, that is, $q \le k - i - 1$. Since $B$ is sorted, $q \ge k - i$ holds exactly when $B[k - i - 1] < A[i]$. $\square$

## Lemma 3. CO-RANK returns the co-rank

*Proof.* Let $(i^*, j^*)$ be the co-rank of $k$. By Lemma 1, $A[i]$ is among the first $k$ items of $C$ exactly when $i < i^*$. So by Lemma 2, for $i$ in the search range with $i < \min(k, m)$, the test on line L4 is false for $i < i^*$ and true for $i \ge i^*$. The loop keeps the invariant $lo \le i^* \le hi$: it holds at the start by Lemma 1; if the test is true at $i$ then $i^* \le i$ and setting $hi = i$ keeps it; if it is false then $i^* > i$ and setting $lo = i + 1$ keeps it. Each round makes $hi - lo$ smaller, and the loop ends with $lo = hi = i^*$. So line L5 returns $(i^*, k - i^*) = (i^*, j^*)$. $\square$

## Theorem. MERGE-PATH writes C

*Proof.* Let $k_t = \lfloor t(m+n)/p \rfloor$, so $0 = k_0 \le k_1 \le \cdots \le k_p = m + n$, and let $(i_t, j_t)$ be the co-rank of $k_t$. By Lemma 1, $i_t \le i_{t+1}$ and $j_t \le j_{t+1}$, because the first $k_t$ items of $C$ are among the first $k_{t+1}$. The items of $C[k_t \ldots k_{t+1} - 1]$ are the first $k_{t+1}$ items without the first $k_t$, that is, $A[i_t \ldots i_{t+1} - 1]$ and $B[j_t \ldots j_{t+1} - 1]$. They appear in $C$ in the stable order, and the stable order of a subset is the stable order restricted to it, so they appear as the stable merge of these two pieces. Line L8 computes exactly this merge and writes it to $C[i_t + j_t \ldots i_{t+1} + j_{t+1} - 1] = C[k_t \ldots k_{t+1} - 1]$. The ranges for different $t$ are disjoint and cover $C$, so the processors write $C$ without conflicts. $\square$
