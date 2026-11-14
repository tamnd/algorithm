---
title: A Taubin pass is the product of two Laplacian step matrices, it scales each eigenvector of the uniform Laplacian by (1 - lambda k)(1 - mu k), and this transfer function keeps the low frequencies and damps the others
proves: [correctness, termination]
status: full
---

**Setup.** The mesh graph has vertices $1, \ldots, n$, neighbour sets $N(i)$, valences $d_i \ge 1$, adjacency matrix $A$, $D = \operatorname{diag}(d_i)$ and $P = D^{-1}A$. Let $G = I - P$. $F$ is the set of fixed vertices. The positions are treated one coordinate at a time. The factors satisfy $\lambda > 0$ and $\mu < -\lambda$, which line L1 checks. The loop runs $K$ passes of two steps each, so the algorithm stops; the claims are about what it computes.

**Lemma 1 (matrix form).** For a factor $f$, lines L4 to L6 map $x$ to $S_f x$, where row $i$ of $S_f$ is row $i$ of $I - fG$ for $i \notin F$ and row $i$ of $I$ for $i \in F$. One pass maps $x$ to $S_\mu S_\lambda x$.

*Proof.* Line L4 uses the old array $x$ for every $c_i$, since $y$ is separate until line L6. For $i \notin F$, $y_i = x_i + f(c_i - x_i) = x_i - f(Gx)_i$. Line L5 keeps the fixed rows. Line L3 applies the step with $\lambda$ and then the step with $\mu$. $\square$

**Lemma 2 (the steps commute).** $S_\lambda S_\mu = S_\mu S_\lambda$.

*Proof.* Let $G'$ be $G$ with the rows of $F$ set to zero. Then $S_f = I - fG'$, and two polynomials in the same matrix $G'$ commute. $\square$

**Lemma 3 (spectrum).** $G$ is similar to the symmetric matrix $I - D^{-1/2}AD^{-1/2}$, so it has real eigenvalues and a basis of eigenvectors. The eigenvalues lie in $[0, 2]$, and $0$ has the eigenvector $\mathbf{1}$.

*Proof.* $G = D^{-1/2}(I - D^{-1/2}AD^{-1/2})D^{1/2}$. The eigenvalues of $P$ lie in $[-1, 1]$: for $Pv = \rho v$ and $i$ with $|v_i|$ largest, $|\rho||v_i| \le \frac{1}{d_i}\sum_{j \in N(i)}|v_j| \le |v_i|$. So the eigenvalues $1 - \rho$ of $G$ lie in $[0, 2]$, and $G\mathbf{1} = 0$ because each row of $P$ sums to 1. $\square$

**Theorem 1 (transfer function).** Let $F = \emptyset$. If $Gv = kv$, then one pass maps $v$ to $f(k)v$ with $f(k) = (1 - \lambda k)(1 - \mu k)$. For a general $x = \sum_j a_j v_j$ in an eigenvector basis, $K$ passes give $\sum_j f(k_j)^K a_j v_j$.

*Proof.* With $F = \emptyset$, $S_f = I - fG$, so $S_\lambda v = (1 - \lambda k)v$ and $S_\mu S_\lambda v = (1 - \mu k)(1 - \lambda k)v$. The general case follows by linearity. $\square$

**Theorem 2 (shape of the transfer function).** Let $\lambda > 0$, $\mu < -\lambda$ and $k_{PB} = \frac{1}{\lambda} + \frac{1}{\mu}$. Then:

1. $k_{PB} > 0$, and $f(0) = f(k_{PB}) = 1$.
2. $f(k) > 1$ for $0 < k < k_{PB}$, with the largest value $1 - \frac{(\lambda + \mu)^2}{4\lambda\mu}$ at $k^* = k_{PB}/2$.
3. $f$ is strictly decreasing on $[k^*, \infty)$, so $f(k) < 1$ for $k > k_{PB}$.
4. $|f(k)| < 1$ for all $k \in (k_{PB}, 2]$ if and only if $f(2) > -1$.

*Proof.* $k_{PB} = \frac{\lambda + \mu}{\lambda\mu}$. Both $\lambda + \mu < 0$ and $\lambda\mu < 0$, so $k_{PB} > 0$. Expand $f(k) = 1 - (\lambda + \mu)k + \lambda\mu k^2 = 1 + \lambda\mu\, k (k - k_{PB})$, which gives (1). Since $\lambda\mu < 0$, $f$ is a parabola that opens downward with roots of $f - 1$ at $0$ and $k_{PB}$. So $f > 1$ between them, its top is at the midpoint $k^*$, and $f(k^*) = 1 + \lambda\mu\, k^*(-k^*) = 1 - \lambda\mu\, \frac{(\lambda + \mu)^2}{4\lambda^2\mu^2} = 1 - \frac{(\lambda + \mu)^2}{4\lambda\mu}$. That is (2) and (3). For (4), on $(k_{PB}, 2]$ the function decreases from 1, so its values lie in $[f(2), 1)$, and they all have absolute value less than 1 exactly when $f(2) > -1$. $\square$

**Corollary (low-pass filter).** On a closed mesh with $f(2) > -1$, the parts of $x$ with frequency in $(k_{PB}, 2]$ tend to 0 as $K$ grows, the part with $k = 0$, the weighted centroid, stays, and the parts with $k \in (0, k_{PB})$ grow by at most the factor $f(k^*)^K$. So Taubin smoothing is not a convergent iteration. It is used for a fixed small $K$, and then the low band is kept up to a factor near 1.

*Proof.* Theorems 1 and 2 and Lemma 3. For $k \in (k_{PB}, 2]$, $|f(k)| < 1$, so $f(k)^K \to 0$. $\square$

**Lemma 4 (the weighted centroid).** If $F = \emptyset$, each step keeps $\sum_i d_i x_i$, for any factor $f$.

*Proof.* $\sum_i d_i y_i = (1 - f)\sum_i d_i x_i + f\sum_i \sum_{j \in N(i)} x_j$, and the double sum counts $x_j$ once for each of its $d_j$ neighbours. $\square$

**Lemma 5 (affine invariance).** Each new position is $\sum_j s_{ij}x_j$ with $\sum_j s_{ij} = 1$, so smoothing commutes with every affine map of $\mathbb{R}^3$.

*Proof.* Row $i$ of $S_f$ sums to $(1 - f) + f = 1$ or is a row of $I$, and products of such matrices have rows that sum to 1. $\square$

**What is measured.** The volume changes of the icosphere in the example, $1.0064$ after 10 passes and $1.032$ after 50, are measured. They agree with the corollary: the sphere is mostly made of low frequencies, which are kept or grow slightly.
