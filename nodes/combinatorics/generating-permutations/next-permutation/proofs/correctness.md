---
title: Next permutation returns the lexicographic successor
proves: [correctness]
status: full
---

Fix $n \ge 0$ and a multiset $M$ of $n$ items from a total order. Let $S(M)$ be the set of sequences of length $n$ whose items form $M$. Two sequences $x \ne y$ of the same length satisfy $x < y$ in lexicographic order when $x_k < y_k$ at the first index $k$ with $x_k \ne y_k$. This is a total order on $S(M)$. We write $A$ for the input and $A'$ for the array after the call.

**Lemma 1 (greatest and least order).** Among the sequences of $S(M')$, for any multiset $M'$, the greatest is the non-increasing one and the least is the non-decreasing one.

*Proof.* Let $x \in S(M')$ be non-increasing and let $y \in S(M')$ with $y \ne x$. Let $k$ be the first index with $x_k \ne y_k$. The items $y_k, \ldots, y_{m-1}$ form the same multiset as $x_k, \ldots, x_{m-1}$, and $x_k$ is the largest of these. So $y_k \le x_k$, and $y_k \ne x_k$ gives $y_k < x_k$, so $y < x$. The proof for the least sequence is the same with the order reversed. $\square$

**Lemma 2 (the scans).** After line L2, $i$ is the largest index in $\{0, \ldots, n-2\}$ with $A[i] < A[i+1]$, or $i = -1$ if there is no such index. In both cases the suffix $A[i+1 \ldots n-1]$ is non-increasing. If $i \ge 0$, line L7 stops with $j$ the largest index in $\{i+1, \ldots, n-1\}$ with $A[j] > A[i]$.

*Proof.* The loop of line L2 keeps the invariant: $A[t] \ge A[t+1]$ for each $t$ with $i < t \le n-2$. It is true at the start with $i = n-2$, because the range is empty, and each step that decreases $i$ has just checked $A[i] \ge A[i+1]$. Each step lowers $i$ by exactly 1, so the loop stops after at most $n - 1$ steps. When it stops, either $i = -1$, or $A[i] < A[i+1]$, and the invariant shows that no larger index has this property. The invariant also says that the suffix after $i$ is non-increasing.

If $i \ge 0$, then $A[i+1] > A[i]$, so the set of indices $j > i$ with $A[j] > A[i]$ is not empty. The loop of line L7 starts at $n - 1$, lowers $j$ by 1 at each step, and stops at the first index from the right with $A[j] > A[i]$. That is the largest such index, and the loop stops before $j$ reaches $i$. $\square$

**Theorem.** If $A$ is not the greatest sequence of $S(M)$, the call returns true and $A'$ is the least sequence of $S(M)$ that is greater than $A$. If $A$ is the greatest sequence, the call returns false and $A'$ is the least sequence of $S(M)$. In both cases $A' \in S(M)$.

*Proof.* Each change of the array is an exchange or a reversal, so the items of $A'$ form $M$.

*Case $i = -1$.* By Lemma 2 the whole array is non-increasing, so by Lemma 1 it is the greatest sequence of $S(M)$. Line L4 reverses it, so $A'$ is non-decreasing, and by Lemma 1 it is the least sequence. The call returns false.

*Case $i \ge 0$.* Let $T = A[i+1 \ldots n-1]$, a non-increasing suffix by Lemma 2, and let $v = A[j]$ with $j$ from Lemma 2. First, $A$ is not the greatest sequence: exchanging $A[i]$ and $A[i+1]$ gives a sequence that agrees with $A$ before index $i$ and is larger at index $i$.

We show that $A'$ is the least $y \in S(M)$ with $y > A$. Take any $y \in S(M)$ with $y > A$, and let $k$ be the first index with $y_k \ne A[k]$, so $y_k > A[k]$.

- $k > i$ is impossible. Then $y$ agrees with $A$ on $0, \ldots, i$, so $y_{i+1} \ldots y_{n-1}$ is an arrangement of the items of $T$. By Lemma 1, $T$ is the greatest such arrangement, so $y \le A$, a contradiction.
- So $k \le i$. If $k < i$, then $y$ and $A'$ differ first at index $k$ or later. The array $A'$ agrees with $A$ on $0, \ldots, i-1$, and $y_k > A[k] = A'[k]$, so $y > A'$.
- If $k = i$, then $y$ agrees with $A$ and $A'$ on $0, \ldots, i-1$, and $y_i > A[i]$. The item $y_i$ comes from the multiset of $A[i], T$, and it is greater than $A[i]$, so it is an item of $T$ that is greater than $A[i]$. The item $v$ is the smallest item of $T$ greater than $A[i]$: by Lemma 2 each item of $T$ to the right of $j$ is at most $A[i]$, and each item to the left of $j$ is at least $v$ because $T$ is non-increasing. So $y_i \ge v = A'[i]$. If $y_i > v$, then $y > A'$. If $y_i = v$, then the rest $y_{i+1} \ldots y_{n-1}$ and the rest of $A'$ are arrangements of the same multiset, namely $T$ with one copy of $v$ replaced by $A[i]$. We show next that the rest of $A'$ is non-decreasing. Then by Lemma 1 it is the least arrangement, so $y \ge A'$.

After the exchange of line L8, the position $j$ holds $A[i]$. The items to the left of $j$ in the suffix are at least $v > A[i]$, and the items to the right of $j$ are at most $A[i]$. So the suffix is still non-increasing, and line L9 makes it non-decreasing.

Finally $A' > A$, because they agree before index $i$ and $A'[i] = v > A[i]$. So $A'$ is in the set of $y$ with $y > A$, and it is at most each such $y$. It is the least one. The call returns true. $\blacksquare$

**Corollary (listing).** Let $N = |S(M)|$. Start with $A$ non-decreasing and call NEXT-PERMUTATION until it returns false. Then the arrays seen before each call are the $N$ sequences of $S(M)$, each once, in increasing order, and the final array is non-decreasing.

*Proof.* $S(M)$ is a finite totally ordered set $s_1 < s_2 < \cdots < s_N$. By Lemma 1 the start is $s_1$. By the theorem, a call on $s_t$ with $t < N$ returns true and leaves $s_{t+1}$, and the call on $s_N$ returns false and leaves $s_1$. So the calls see $s_1, \ldots, s_N$ in this order, and stop after the call on $s_N$. $\blacksquare$
