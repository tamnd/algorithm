---
title: Each Laplacian smoothing step is the matrix S, it keeps the degree-weighted centroid, and the steps converge to a point on a closed mesh and to the harmonic membrane on a mesh with a fixed border
proves: [correctness, termination]
status: full
---

**Setup.** The mesh has vertices $1, \ldots, n$ with neighbour sets $N(i)$ and valences $d_i = |N(i)| \ge 1$. Let $A$ be the adjacency matrix of the edge graph, $D = \operatorname{diag}(d_i)$, and $P = D^{-1}A$, so that $(Px)_i = c_i$ is the centroid of the neighbours. $F$ is the set of fixed vertices and $R$ the set of free ones. The positions are treated one coordinate at a time, so $x \in \mathbb{R}^n$. The factor satisfies $0 < \lambda < 1$. The algorithm stops after $K$ steps, so termination is clear; the claims are about what the steps compute.

**Lemma 1 (matrix form).** One pass of lines L3 to L7 maps $x$ to $y$ with $y_i = ((1 - \lambda)x + \lambda P x)_i$ for $i \in R$ and $y_i = x_i$ for $i \in F$.

*Proof.* Line L4 computes $c_i = (Px)_i$ from the old array $x$, since $y$ is a separate array and line L7 copies it only after all vertices are done. Line L5 sets $y_i = x_i + \lambda(c_i - x_i) = (1 - \lambda)x_i + \lambda c_i$. Line L6 keeps the fixed vertices. $\square$

**Lemma 2 (affine invariance).** For an affine map $T(p) = Bp + t$ of $\mathbb{R}^3$, smoothing $T(x)$ gives $T$ of the smoothed $x$.

*Proof.* By Lemma 1, each $y_i$ is $\sum_j s_{ij} x_j$ with $\sum_j s_{ij} = (1 - \lambda) + \lambda = 1$, or $y_i = x_i$. An affine map commutes with combinations whose weights sum to 1. $\square$

**Lemma 3 (the weighted centroid is kept).** If $F = \emptyset$, then $\sum_i d_i y_i = \sum_i d_i x_i$.

*Proof.* $\sum_i d_i y_i = (1 - \lambda)\sum_i d_i x_i + \lambda \sum_i \sum_{j \in N(i)} x_j$. Each $x_j$ appears in the double sum once for each neighbour $i$ of $j$, that is $d_j$ times, so the double sum is $\sum_j d_j x_j$, and the total is $\sum_i d_i x_i$. $\square$

**Lemma 4 (spectrum).** $P$ is similar to the symmetric matrix $B = D^{-1/2} A D^{-1/2}$, so it has real eigenvalues and a basis of eigenvectors. Its eigenvalues lie in $[-1, 1]$. If the graph is connected, the eigenvalue 1 is simple, with eigenvector $\mathbf{1}$.

*Proof.* $P = D^{-1/2} B D^{1/2}$, and $B$ is symmetric. For an eigenvector $Pv = \mu v$, take $i$ with $|v_i|$ largest. Then $|\mu||v_i| = |\frac{1}{d_i}\sum_{j \in N(i)} v_j| \le |v_i|$, so $|\mu| \le 1$. If $\mu = 1$ and $v_i$ is largest with $v_i > 0$ (replace $v$ by $-v$ if needed), then $v_i$ is the average of its neighbours, all at most $v_i$, so all are equal to $v_i$. Repeating this along paths shows that $v$ is constant on the connected graph, so the eigenspace of 1 is spanned by $\mathbf{1}$. $\square$

**Theorem 1 (closed mesh).** Let $F = \emptyset$, the edge graph be connected, and $0 < \lambda < 1$. Then after $K$ steps every position tends, as $K \to \infty$, to $\bar x = \sum_i d_i x_i / \sum_i d_i$.

*Proof.* By Lemma 1 the step is $S = (1 - \lambda)I + \lambda P$, and $S$ has the eigenvectors of $P$ with eigenvalues $1 - \lambda + \lambda\mu$. By Lemma 4, $\mu \in [-1, 1]$, so $1 - \lambda + \lambda\mu \in [1 - 2\lambda, 1]$, and $1 - 2\lambda > -1$ since $\lambda < 1$. The value 1 occurs only for $\mu = 1$, whose eigenspace is spanned by $\mathbf{1}$. Every other eigenvalue has absolute value less than 1. Write $x = a\mathbf{1} + r$ with $r$ in the span of the other eigenvectors. Then $S^K x = a\mathbf{1} + S^K r \to a\mathbf{1}$. The eigenvectors of $B$ are orthogonal, so those of $P$ are orthogonal in the inner product $\langle u, v \rangle = \sum_i d_i u_i v_i$, and $r$ is $D$-orthogonal to $\mathbf{1}$, that is, $\sum_i d_i r_i = 0$. Hence $a = \sum_i d_i x_i / \sum_i d_i = \bar x$. This agrees with Lemma 3, which keeps $\sum_i d_i x_i$ along the way. $\square$

So the shrinkage is not a numerical effect: the limit is one point, for every closed connected mesh.

**Lemma 5 (substochastic block).** Suppose every connected part of the edge graph contains a vertex of $F$. Let $P_{RR}$ be the block of $P$ on the free vertices. Every eigenvalue $\mu$ of $P_{RR}$ has $|\mu| < 1$.

*Proof.* $P_{RR} = D_R^{-1} A_{RR}$ is similar to the symmetric $D_R^{-1/2} A_{RR} D_R^{-1/2}$, so its eigenvalues are real. Let $P_{RR} v = \mu v$ with $v \ne 0$ and $|\mu| \ge 1$, and let $m = \max_i |v_i| > 0$ be attained at $i \in R$. Then $|\mu| m = |\frac{1}{d_i}\sum_{j \in N(i) \cap R} v_j| \le \frac{|N(i) \cap R|}{d_i} m$. So $|N(i) \cap R| = d_i$, that is, $i$ has no fixed neighbour, and every neighbour $j$ of $i$ has $|v_j| = m$. Repeating this from each such $j$ reaches every free vertex of the connected part of $i$. That part has a fixed vertex, so some free vertex on a path to it has a fixed neighbour, which contradicts $|N(\cdot) \cap R| = d$. $\square$

**Theorem 2 (open mesh).** Under the hypothesis of Lemma 5 and $0 < \lambda < 1$, the free positions converge, as $K \to \infty$, to the unique solution of $x_i = c_i$ for all $i \in R$, with the fixed positions as given.

*Proof.* By Lemma 1, the free part follows $x_R \leftarrow S_{RR} x_R + \lambda P_{RF} x_F$ with $S_{RR} = (1 - \lambda)I + \lambda P_{RR}$. By Lemma 5, the eigenvalues of $S_{RR}$ are $1 - \lambda + \lambda\mu$ with $|\mu| < 1$, so they lie in $(1 - 2\lambda, 1)$, inside $(-1, 1)$, and $S_{RR}$ is diagonalizable. So the iteration converges for every start to the unique fixed point $x_R^*$ of $x_R = S_{RR} x_R + \lambda P_{RF} x_F$. That equation is $\lambda(I - P_{RR}) x_R = \lambda P_{RF} x_F$, which says $x_i = c_i$ for each free $i$, and $I - P_{RR}$ is invertible because 1 is not an eigenvalue of $P_{RR}$. $\square$

**Claim (fixed points of one step).** A free vertex with $x_i = c_i$ does not move in a step. On the grid of the example, every inner vertex $(i, j)$ has the neighbours $(i \pm 1, j)$, $(i, j \pm 1)$, $(i + 1, j + 1)$, $(i - 1, j - 1)$, which are symmetric about $(i, j)$, so $c_i = x_i$, and the flat grid is a fixed point of every step. This follows directly from line L5.
