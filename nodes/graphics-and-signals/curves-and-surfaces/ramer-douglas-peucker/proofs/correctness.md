---
title: RDP keeps both ends, and every removed point lies within the tolerance of the output segment over it
proves: [correctness, termination, hausdorff-bound]
status: full
---

We use the pseudocode of the page. The input is $P_0, \dots, P_{n-1}$ in $\mathbb{R}^d$ with $n \ge 3$ and a tolerance $\varepsilon \ge 0$. For $n \le 2$ the algorithm returns the input, and all claims hold trivially. We write $\delta(m; i, j)$ for the distance from $P_m$ to the closed segment $P_i P_j$, and $K$ for the set of indices with $keep$ true. Two indices $a < b$ of $K$ are *consecutive* when no index strictly between them is in $K$.

**Invariant (I).** Each time line L3 tests the stack $S$:

1. $0, n - 1 \in K$, and each pair on $S$ is a pair of consecutive indices of $K$;
2. each pair of consecutive indices of $K$ is on $S$ exactly once, or it is *finished*: $\delta(m; a, b) \le \varepsilon$ for all $a < m < b$.

*Initialization.* Line L1 makes $K = \{0, n - 1\}$, and line L2 puts the only consecutive pair $(0, n - 1)$ on $S$. So (I) holds.

*Maintenance.* Line L4 pops a pair $(i, j)$. By (I) it is a consecutive pair of $K$, and after the pop it is on $S$ zero times. Line L5 computes $k$ and $d_{\max} = \delta(k; i, j) = \max_{i < m < j} \delta(m; i, j)$, or finds no index when $j = i + 1$.

- If there is no index or $d_{\max} \le \varepsilon$, then every $m$ with $i < m < j$ has $\delta(m; i, j) \le d_{\max} \le \varepsilon$, so the pair $(i, j)$ is finished. Nothing else changes, and (I) holds.
- Otherwise $i < k < j$ and $k \notin K$, because $i$ and $j$ are consecutive. Line L7 adds $k$ to $K$. The pair $(i, j)$ stops being consecutive, and the new consecutive pairs are $(i, k)$ and $(k, j)$. Line L8 puts each of them on $S$ once. All other consecutive pairs and their status do not change. So (I) holds.

*Termination.* Each pass of the second kind adds a new index to $K$, and $K$ only grows inside $\{0, \dots, n-1\}$. So there are at most $n - 2$ such passes, and they push at most $2(n - 2)$ pairs. Each pass pops one pair, so the loop runs at most $2n - 3$ times and stops.

**Theorem.** The output is the subsequence $P_{k_0}, \dots, P_{k_r}$ with $K = \{k_0 < \dots < k_r\}$, $k_0 = 0$ and $k_r = n - 1$. For each removed index $m$, with $k_{s} < m < k_{s+1}$, we have $\delta(m; k_s, k_{s+1}) \le \varepsilon$.

*Proof.* When the loop stops, $S$ is empty. By part 2 of (I) every consecutive pair of $K$ is finished. Each removed index $m$ lies between exactly one consecutive pair $(k_s, k_{s+1})$, and the finished condition is the claim. Line L9 returns the points of $K$ in index order, and part 1 of (I) gives the two ends. $\blacksquare$

**Corollary (Hausdorff bound).** Let $C$ be the input polyline and $C'$ the output polyline, as point sets. Then each point of $C$ is within $\varepsilon$ of $C'$, and each point of $C'$ is within $\varepsilon$ of $C$.

*Proof.* Fix a consecutive pair $a = k_s$, $b = k_{s+1}$, and let $T$ be the set of points within $\varepsilon$ of the segment $P_a P_b$. $T$ is convex, because it is the sum of a segment and a ball. By the theorem, $P_a, \dots, P_b$ lie in $T$, so each input segment $P_m P_{m+1}$ with $a \le m < b$ lies in $T$. This gives the first claim. For the second, write $\pi(x)$ for the parameter of the orthogonal projection of $x$ onto the line $P_a P_b$, scaled so that $\pi(P_a) = 0$ and $\pi(P_b) = 1$. The input path from $P_a$ to $P_b$ is connected and $\pi$ is continuous, so for each point $q$ of the segment with $\pi(q) = \lambda \in [0, 1]$ some point $x$ of the path has $\pi(x) = \lambda$. Then $q$ is the point of the segment nearest to $x$, so $|x - q| \le \varepsilon$ because $x \in T$. $\blacksquare$

**Remark (the order of the stack).** The test of line L6 for a pair $(i, j)$ depends only on $P_i, \dots, P_j$, and the pairs on $S$ have disjoint open index ranges. So the final set $K$ does not depend on the order in which line L4 pops the pairs. In particular it equals the result of the recursive form, which handles $(i, k)$ before $(k, j)$, when both use the same rule for ties in line L5.

**Remark (the segment distance).** The proof uses only that line L5 measures $\delta$ to the closed segment. If line L5 used the distance to the infinite line, the theorem would hold with that distance instead, and a removed point could be far from the output: for $P_0 = (0, 0)$, $P_1 = (5, 0)$, $P_2 = (-10, 0)$ the line distance of $P_1$ is $0$, the version with the line removes it for every $\varepsilon$, and its distance to the output segment is $5$.
