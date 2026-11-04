---
title: In-place merge sort returns a stable sorted order
proves: [correctness, termination]
status: full
---

Tag each item with its input position. A sequence is *stably sorted* if it is in non-decreasing order of keys and items with equal keys are in increasing order of their tags. We write $u \preceq v$ for "not $v < u$", that is, the key of $u$ is at most the key of $v$.

**Lemma 1 (ROTATE).** ROTATE$(A, i, m, j)$ replaces $A[i \ldots j-1] = X\,Y$, with $X = A[i \ldots m-1]$ and $Y = A[m \ldots j-1]$, by $Y\,X$, and changes nothing else.

*Proof.* If $X$ or $Y$ is empty, $XY = YX$ and line L16 does nothing. Otherwise, write $Z^R$ for $Z$ reversed. The first two reversals give $X^R Y^R$, and the third gives $(X^R Y^R)^R = (Y^R)^R (X^R)^R = Y X$. $\square$

**Lemma 2 (the searches).** On a sorted range, LOWER-BOUND$(A, lo, hi, x)$ returns the least $i \in [lo, hi]$ such that each item of $A[i \ldots hi-1]$ satisfies not $A[i] < x$, and each item of $A[lo \ldots i-1]$ is less than $x$. UPPER-BOUND returns the least $i$ such that each item of $A[lo \ldots i-1]$ satisfies not $x < A[\cdot]$, and each item of $A[i \ldots hi-1]$ is greater than $x$.

*Proof.* This is binary search on a monotone predicate: the invariant is that every item before $lo$ has the property of the left part and every item from $hi$ on has the property of the right part. Each step keeps it and shrinks $hi - lo$, and the loop ends with $lo = hi$ at the boundary. $\square$

**Lemma 3 (MERGE-IN-PLACE).** Let $A[lo \ldots mid-1] = P$ and $A[mid \ldots hi-1] = Q$ be stably sorted, with every tag in $P$ smaller than every tag in $Q$. Then MERGE-IN-PLACE$(A, lo, mid, hi)$ ends, changes only $A[lo \ldots hi-1]$, and leaves there the stably sorted order of the items of $P$ and $Q$.

*Proof.* By induction on $N = hi - lo$. If one run is empty (line L6), the other run is the answer. If $N = 2$ (line L7), there is one item in each run, and the exchange happens exactly when the right item has the smaller key, so equal keys keep the left item first.

Let $N \ge 3$, with both runs non-empty.

*Case 1: $mid - lo \ge hi - mid$ (line L9).* Then $mid - lo \ge 2$, so $lo < cut1 < mid$. Let $x = A[cut1]$. Split $P = P_1\,P_2$ at $cut1$ and $Q = Q_1\,Q_2$ at $cut2$. By Lemma 2, every item of $Q_1$ is less than $x$, and no item of $Q_2$ is less than $x$. As $P$ is sorted, every item of $P_1$ is $\preceq x$ and $x \preceq$ every item of $P_2$. After line L12, by Lemma 1, the range holds $P_1\,Q_1\,P_2\,Q_2$, and line L13 sets $newmid$ to the boundary between $P_1 Q_1$ and $P_2 Q_2$.

The two calls of lines L14 and L15 get runs $(P_1, Q_1)$ and $(P_2, Q_2)$, each run stably sorted as a part of a stably sorted run, and each with left tags smaller than right tags. They are smaller than $N$: the first has $|P_1| + |Q_1| \le (N-1) - |P_2| < N$ items, and the second lacks the items of $P_1$, which is not empty. So by induction they produce the stably sorted orders $S_1$ of $P_1 \cup Q_1$ and $S_2$ of $P_2 \cup Q_2$.

It remains to show that $S_1\,S_2$ is stably sorted, that is, for $u \in P_1 \cup Q_1$ and $v \in P_2 \cup Q_2$, $u$ belongs before $v$. Every such $u$ is $\preceq x$ and every such $v$ has $x \preceq v$, so $u \preceq v$. If the keys of $u$ and $v$ are equal, then both equal the key of $x$. Then $u \notin Q_1$, because the items of $Q_1$ are less than $x$, so $u \in P_1$. If $v \in P_2$, $u$ comes before $v$ in the stably sorted run $P$, so its tag is smaller. If $v \in Q_2$, the tag of $u \in P$ is smaller than that of $v \in Q$. In both cases $u$ belongs before $v$.

*Case 2: $mid - lo < hi - mid$ (line L11).* Then $hi - mid \ge 2$, so $mid < cut2 < hi$. Let $y = A[cut2]$, the first item of $Q_2$. By Lemma 2, every item of $P_1$ is $\preceq y$, and every item of $P_2$ is greater than $y$. As $Q$ is sorted, every item of $Q_1$ is $\preceq y \preceq$ every item of $Q_2$. The range becomes $P_1\,Q_1\,P_2\,Q_2$ as before. The first call lacks $y$ and the second lacks the items of $Q_1$, which is not empty, so both are smaller than $N$. For $u \in P_1 \cup Q_1$ and $v \in P_2 \cup Q_2$ we get $u \preceq y \preceq v$. If their keys are equal, both equal the key of $y$, so $v \notin P_2$, and $v \in Q_2$. If $u \in Q_1$, it is before $v$ in the stably sorted run $Q$; if $u \in P_1$, its tag is smaller than any tag in $Q$. So $u$ belongs before $v$.

In both cases the result is stably sorted, and only $A[lo \ldots hi-1]$ was changed. $\square$

**Theorem.** IN-PLACE-MERGE-SORT$(A, 0, n)$ ends and leaves $A$ stably sorted.

*Proof.* By induction on $hi - lo$, the call on $[lo, hi)$ ends and stably sorts that range, changing nothing else. If $hi - lo < 2$, line L1 returns, and the range is already stably sorted. Otherwise $lo < mid < hi$, so both calls of lines L3 and L4 are on shorter ranges, and by induction they stably sort $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$. Since neither call moves an item out of its half, every tag in the left half is smaller than every tag in the right half. By Lemma 3, line L5 ends and leaves the stably sorted order of the whole range. $\blacksquare$
