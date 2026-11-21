---
title: The ordered earth mover's distance has a closed form, merging keeps t-closeness, and the test is exact
proves: [correctness]
status: full
---

Let $P = (p_1, \ldots, p_m)$ and $W = (w_1, \ldots, w_m)$ be distributions over the ordered values $v_1 < \cdots < v_m$, with $m \ge 2$, and let the ground distance be $d_{ij} = |i - j| / (m - 1)$. A flow is a matrix $f \ge 0$ with row sums $p_i$ and column sums $w_j$. Its work is $\sum_{i,j} d_{ij} f_{ij}$, and $D[P, W]$ is the least work. Write $R_k = \sum_{j \le k} (p_j - w_j)$ for $k = 0, \ldots, m$, so $R_0 = R_m = 0$.

**Claim 1 (closed form).** $D[P, W] = \frac{1}{m - 1} \sum_{k=1}^{m-1} |R_k|$.

*Proof of the lower bound.* Fix a flow $f$ and a gap $k$ between $v_k$ and $v_{k+1}$, $1 \le k \le m - 1$. Since $|i - j|$ is the number of gaps $k$ with $\min(i, j) \le k < \max(i, j)$,
$$\sum_{i,j} |i - j|\, f_{ij} = \sum_{k=1}^{m-1} \Big( \sum_{i \le k < j} f_{ij} + \sum_{j \le k < i} f_{ij} \Big).$$
The mass of $P$ on $v_1, \ldots, v_k$ is $\sum_{i \le k} p_i = \sum_{i \le k} \sum_j f_{ij}$, and the mass of $W$ there is $\sum_{j \le k} w_j = \sum_{j \le k} \sum_i f_{ij}$. Subtract: $R_k = \sum_{i \le k < j} f_{ij} - \sum_{j \le k < i} f_{ij}$. Both sums are non-negative, so their sum is at least $|R_k|$. Hence the work of $f$ is at least $\frac{1}{m-1} \sum_k |R_k|$.

*Proof of the upper bound.* Build a flow on the path $v_1, v_2, \ldots, v_m$ that sends $R_k$ units across gap $k$, to the right if $R_k > 0$ and to the left if $R_k < 0$. At node $i$ the net amount sent away is $R_i - R_{i-1} = p_i - w_i$, so node $i$ starts with $p_i$ and ends with $w_i$. Split this flow on the path into paths from a node with $p_i > w_i$ to a node with $w_j > p_j$, by the standard decomposition of a flow without cycles; on a path graph, a path from $i$ to $j$ crosses exactly $|i - j|$ gaps. The matrix of these paths, with the mass $\min(p_i, w_i)$ that stays at each node on the diagonal, is a flow $f$ whose work is $\frac{1}{m - 1} \sum_k |R_k|$. With the lower bound, this is the minimum. $\square$

**Claim 2 (merging).** For any ground distance, $D[\lambda P_1 + (1 - \lambda) P_2, W] \le \lambda D[P_1, W] + (1 - \lambda) D[P_2, W]$ for $0 \le \lambda \le 1$.

*Proof.* Let $f^1$ and $f^2$ be optimal flows for $(P_1, W)$ and $(P_2, W)$. The matrix $f = \lambda f^1 + (1 - \lambda) f^2$ is non-negative, has row sums $\lambda p^1_i + (1 - \lambda) p^2_i$ and column sums $\lambda w_j + (1 - \lambda) w_j = w_j$. So it is a flow for the mixture, and its work is $\lambda D[P_1, W] + (1 - \lambda) D[P_2, W]$. The minimum is at most this. $\square$

If blocks $E_1$ and $E_2$ are merged, the distribution of the result is the mixture with $\lambda = |E_1| / (|E_1| + |E_2|)$. If both blocks are within $t$ of $W$, so is the merged block. By induction, every table whose blocks are unions of the blocks of a t-close table is t-close.

**Claim 3 (the test).** T-CLOSE returns true if and only if every block has $D[P, W] \le t$ under the ordered distance.

*Proof.* Line L1 computes $W$ from all rows. The blocks of line L2 are the groups of rows with equal values on $Q$, and line L3 computes the distribution $P$ of a block. The loop of lines L5 to L7 keeps the invariant: before the iteration for $i$, $run = R_{i-1}$ and $d = \sum_{k < i} |R_k|$. It holds at the start by line L4, and line L6 adds $p_i - w_i$ to make $run = R_i$, then line L7 adds $|R_i|$. After the loop, $d = \sum_{k=1}^{m-1} |R_k|$, so by Claim 1 line L8 compares $D[P, W]$ with $t$ and returns false exactly for a block that is not within $t$. If no block fails, line L9 returns true. With exact fractions, no rounding enters. $\blacksquare$

**Cost.** Lines L1 to L3 read each row a constant number of times with a hash table, and the loop costs $O(m)$ per block, so the time is $O(n + g m)$ for $n$ rows and $g$ blocks.
