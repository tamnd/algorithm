---
title: Neville's recurrence and the in-place loop compute the interpolant at t
proves: [correctness, termination]
status: full
---

**Setting.** The nodes $x_0, \ldots, x_n$ are distinct, $y_0, \ldots, y_n$ are the data, and $t$ is a number. For $0 \le i \le j \le n$, $p_{i,j}$ denotes the polynomial of degree at most $j - i$ with $p_{i,j}(x_m) = y_m$ for $i \le m \le j$.

**Lemma 1 (existence and uniqueness).** $p_{i,j}$ exists and is unique.

*Proof.* Uniqueness: the difference of two such polynomials has degree at most $j - i$ and $j - i + 1$ distinct zeros, so it is 0. Existence: the Lagrange form $\sum_{m=i}^{j} y_m \prod_{l \ne m} (x - x_l)/(x_m - x_l)$, with $l$ ranging over $i, \ldots, j$, has degree at most $j - i$ and takes the value $y_m$ at $x_m$. $\square$

**Lemma 2 (Neville recurrence).** For $i < j$ and every $t$,
$$p_{i,j}(t) = \frac{(t - x_i)\, p_{i+1,j}(t) - (t - x_j)\, p_{i,j-1}(t)}{x_j - x_i}.$$

*Proof.* Call the right side $R(t)$; the denominator is not 0 since the nodes are distinct. $p_{i+1,j}$ and $p_{i,j-1}$ have degree at most $j - i - 1$, so $R$ is a polynomial of degree at most $j - i$. We check $R(x_m) = y_m$ for $i \le m \le j$.

- $m = i$: the first term vanishes and $p_{i,j-1}(x_i) = y_i$ (as $i \le j - 1$), so $R(x_i) = -(x_i - x_j) y_i/(x_j - x_i) = y_i$.
- $m = j$: the second term vanishes and $p_{i+1,j}(x_j) = y_j$ (as $i + 1 \le j$), so $R(x_j) = (x_j - x_i) y_j/(x_j - x_i) = y_j$.
- $i < m < j$: then $i + 1 \le m \le j$ and $i \le m \le j - 1$, so both sub-interpolants take the value $y_m$, and $R(x_m) = y_m \big((x_m - x_i) - (x_m - x_j)\big)/(x_j - x_i) = y_m$.

By Lemma 1, $R = p_{i,j}$. $\square$

**Lemma 3 (loop invariant).** Consider the in-place loop of lines L1 to L5. Before round $k$ of line L2 ($1 \le k \le n$), and after the last round with $k = n + 1$:

(I) $P[i] = p_{i, i+k-1}(t)$ for $0 \le i \le n - k + 1$.

Within round $k$, just before the update of line L4 for index $i$:

(J) $P[l] = p_{l, l+k}(t)$ for $0 \le l < i$, and $P[l] = p_{l, l+k-1}(t)$ for $i \le l \le n - k + 1$.

*Proof.* Before round 1, line L1 gives $P[i] = y_i = p_{i,i}(t)$ for all $i$, which is (I) for $k = 1$. At the start of round $k$, (J) with $i = 0$ is (I). Assume (J) before the update at $i \le n - k$. Line L4 reads $P[i] = p_{i,i+k-1}(t)$ and $P[i + 1] = p_{i+1,i+k}(t)$; the second is still at level $k - 1$ because $i + 1 > i$ has not been updated in this round, and $i + 1 \le n - k + 1$. By Lemma 2 with $j = i + k$, the new value is $p_{i,i+k}(t)$, and no other entry changes. So (J) holds for $i + 1$. After the last index $i = n - k$, (J) with $i = n - k + 1$ gives $P[l] = p_{l,l+k}(t)$ for $0 \le l \le n - k$, which is (I) for $k + 1$. $\square$

**Theorem (correctness and termination).** NEVILLE$(x, y, t)$ performs exactly $n(n+1)/2$ updates and returns $p_n(t) = p_{0,n}(t)$.

*Proof.* The loops are bounded, with $\sum_{k=1}^{n} (n - k + 1) = n(n+1)/2$ executions of line L4. When the outer loop ends, (I) with $k = n + 1$ gives $P[0] = p_{0,n}(t)$, which line L5 returns. For $n = 0$ the loop body never runs and $P[0] = y_0 = p_{0,0}(t)$. $\square$

**Corollary (exactness and order independence).** If $y_m = q(x_m)$ for a polynomial $q$ of degree at most $n$, then $p_{0,n} = q$ by Lemma 1, and the algorithm returns $q(t)$ in exact arithmetic. Since $p_{0,n}$ depends only on the set of pairs $(x_m, y_m)$, permuting the nodes and data does not change the result.
