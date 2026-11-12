---
title: Isomap recovers flat coordinates when the graph distances are Euclidean
proves: [correctness]
status: full
---

Let $D_G$ be the matrix of graph distances from lines L1 to L4, and suppose the graph is connected, so all entries are finite.

**Lemma 1 (the graph distances form a metric).** $D_G$ is symmetric, has a zero diagonal and positive entries off the diagonal for distinct points, and satisfies the triangle inequality.

*Proof.* Line L1 adds each edge in both directions with the same weight, so a path from $s$ to $t$ reversed is a path from $t$ to $s$ of the same length. The empty path gives $D_G[s, s] = 0$, and every edge between distinct points has a positive weight. If $P$ is a shortest path from $s$ to $u$ and $Q$ one from $u$ to $t$, the walk $P$ then $Q$ has length $D_G[s, u] + D_G[u, t]$ and contains a path from $s$ to $t$ that is no longer, so $D_G[s, t] \le D_G[s, u] + D_G[u, t]$. Dijkstra's algorithm returns these distances because all weights are non-negative. $\square$

**Lemma 2 (graph distances bound the true distance from above on a convex sheet).** Let the points be $x_i = \phi(z_i)$ for a map $\phi$ from a convex set $C \subset \mathbb{R}^m$ onto the manifold that keeps the lengths of curves, and suppose each graph edge $\{i, j\}$ has $\|x_i - x_j\| \ge \|z_i - z_j\|$. Then $D_G[i, j] \ge \|z_i - z_j\|$ for all pairs.

*Proof.* The image under $\phi$ of the segment from $z_i$ to $z_j$ lies on the manifold, because $C$ is convex, and has length $\|z_i - z_j\|$. Any curve on the manifold from $x_i$ to $x_j$ is the image of a curve in $C$ of the same length, which is at least $\|z_i - z_j\|$. The straight segment from $x_i$ to $x_j$ in $\mathbb{R}^d$ is no longer than any such curve, so in general $\|x_i - x_j\| \le \|z_i - z_j\|$, and the assumption makes this an equality on the edges. For a graph path $i = p_0, p_1, \dots, p_r = j$, the triangle inequality in $\mathbb{R}^m$ gives $\sum_s \|x_{p_{s-1}} - x_{p_s}\| = \sum_s \|z_{p_{s-1}} - z_{p_s}\| \ge \|z_i - z_j\|$. Take the minimum over paths. $\square$

The assumption of Lemma 2 holds exactly when each edge lies on a straight piece of the manifold, as on a flat sheet folded along lines, and approximately for short edges on a smooth manifold. The lower bound of Bernstein, de Silva, Langford and Tenenbaum (2000) makes the approximate version precise, and their upper bound $D_G \le (1 + \lambda_2) d_{\mathcal{M}}$ uses a dense sample: a geodesic can be followed by a chain of short graph edges whose total length is close to its own.

**Theorem (exact recovery).** If $D_G[i, j] = \|z_i - z_j\|$ for all pairs, for some points $z_1, \dots, z_n \in \mathbb{R}^m$, then lines L5 to L7 return points $y_i$ with $\|y_i - y_j\| = \|z_i - z_j\|$ for all pairs. So $y_i = Q z_i + c$ for an orthogonal $Q$ and a vector $c$.

*Proof.* Let $Z$ be the $n \times m$ matrix with rows $z_i$ and $\bar Z = JZ$ its centered form. Expanding $\|z_i - z_j\|^2 = \|z_i\|^2 + \|z_j\|^2 - 2z_i^\top z_j$ and applying $J$ on both sides removes the terms that depend on $i$ only or on $j$ only, so $B = -\frac12 J D_G^{(2)} J = \bar Z \bar Z^\top$. This matrix is positive semidefinite with rank at most $m$, so its eigenvalues are $\lambda_1 \ge \dots \ge \lambda_m \ge 0$ and then zeros, and $B = \sum_{l \le m} \lambda_l v_l v_l^\top$. Line L7 builds $Y = V_m \Lambda_m^{1/2}$, so $YY^\top = B = \bar Z \bar Z^\top$. Two configurations with the same Gram matrix have the same pairwise distances, because $\|y_i - y_j\|^2 = (YY^\top)_{ii} + (YY^\top)_{jj} - 2(YY^\top)_{ij}$. Points in $\mathbb{R}^m$ with the same pairwise distances differ by a rigid motion. $\square$

**Corollary (the example).** For points along a path with graph distance $D_G[i, j] = |t_i - t_j|$, as in the U example and the arc test, the theorem applies with $m = 1$ and $z_i = t_i$. Isomap returns $t_i$ up to a shift and a sign, and all other eigenvalues of $B$ are 0.

**Failure without connectivity.** If the graph has two components, some $D_G[s, t]$ is infinite, and $B$ is not defined. Line L4 stops in this case, so the algorithm never returns coordinates computed from infinite values.
