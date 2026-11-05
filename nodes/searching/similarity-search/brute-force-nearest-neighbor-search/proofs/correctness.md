---
title: The brute-force scan returns the k nearest points
proves: [correctness]
status: full
---

Let $P[0 \ldots n-1]$ be the points, $q$ the query and $k \ge 1$. For $j < n$ let $e_j = (\delta(q, P[j]), j)$, compared in lexicographic order. The indices are distinct, so the $e_j$ are distinct and totally ordered. For $0 \le i \le n$ let $B_i$ be the set of the $\min(k, i)$ smallest elements of $\{e_0, \ldots, e_{i-1}\}$.

**Invariant (H).** At the start of the iteration of line L2 with index $i$, and after the last iteration with $i = n$, the heap $H$ holds exactly the elements of $B_i$.

*Initialization.* Before the first iteration, $i = 0$, line L1 made $H$ empty, and $B_0 = \emptyset$.

*Maintenance.* Assume (H) at the start of iteration $i < n$. Line L3 computes $e_i$.

- If $|H| < k$, then $|B_i| = \min(k, i) < k$, so $i < k$ and $B_i = \{e_0, \ldots, e_{i-1}\}$. Then $B_{i+1}$ is all of $\{e_0, \ldots, e_i\}$, since $i + 1 \le k$. Line L4 inserts $e_i$, so $H = B_{i+1}$.
- Else $|H| = k$ and $i \ge k$. Let $t$ be the largest element of $B_i$, which is TOP$(H)$ by the max-heap property. Each element of $\{e_0, \ldots, e_{i-1}\} \setminus B_i$ is larger than $t$.
  - If $e_i < t$, then $e_i$ is among the $k$ smallest of $\{e_0, \ldots, e_i\}$: at most $k - 1$ elements of $B_i$ are below it, and no other element is. The element $t$ now has $k$ smaller elements ($B_i \setminus \{t\}$ and $e_i$), so it leaves. So $B_{i+1} = (B_i \setminus \{t\}) \cup \{e_i\}$, which is what line L5 makes.
  - If $e_i > t$, then the $k$ elements of $B_i$ are smaller than $e_i$, so $e_i \notin B_{i+1}$ and $B_{i+1} = B_i$. Line L5 does nothing.

  The case $e_i = t$ cannot occur, because the elements are distinct.

In each case (H) holds at the start of iteration $i + 1$.

*Termination.* The loop runs for $i = 0, 1, \ldots, n-1$, so it stops after $n$ iterations, with $H = B_n$.

**Theorem.** Line L6 returns a list $s_1 < s_2 < \cdots < s_m$ of $m = \min(k, n)$ pairs, and the set $S$ of their points is a correct answer to the $k$-nearest neighbor query: $\delta(q, s) \le \delta(q, p)$ for each $s \in S$ and $p \in P \setminus S$.

*Proof.* By (H), line L6 sorts $B_n$, which has $\min(k, n)$ elements. Let $s \in S$ and $p \in P \setminus S$, with pairs $e_s$ and $e_p$. Since $e_p \notin B_n$ and $B_n$ is the set of the smallest elements, $e_s < e_p$. The first component of a pair is the distance, so lexicographic order gives $\delta(q, s) \le \delta(q, p)$. $\blacksquare$

**Ties.** When several points have the distance of the $m$-th result, $B_n$ takes those with the smallest indices, because the second component decides between pairs of equal distance.
