---
title: The least eigenvector of the neighbor covariance is the normal of the least squares plane, and the surface variation lies in [0, 1/3] and is 0 exactly for coplanar points
proves: [correctness]
status: full
---

Fix one point and its neighborhood $Q = \{q_1, \ldots, q_k\}$ from line L2, with $k \ge 3$. Line L3 computes the centroid $c = \frac1k \sum_j q_j$, and line L4 the covariance

$$C = \frac1k \sum_{j=1}^{k} (q_j - c)(q_j - c)^\top.$$

$C$ is symmetric, and $x^\top C x = \frac1k \sum_j (x \cdot (q_j - c))^2 \ge 0$ for every $x$, so $C$ is positive semidefinite. By the spectral theorem it has real eigenvalues $0 \le \lambda_0 \le \lambda_1 \le \lambda_2$ with orthonormal eigenvectors $v_0, v_1, v_2$, which line L5 returns.

For a unit vector $n$ and a number $d$, the plane $\{x : n \cdot x = d\}$ has the squared distance sum

$$E(n, d) = \sum_{j=1}^{k} (n \cdot q_j - d)^2.$$

**Lemma 1 (the plane passes through the centroid).** For a fixed unit $n$, $E(n, d)$ is least at $d = n \cdot c$, and $E(n, n \cdot c) = k\, n^\top C n$.

*Proof.* Write $n \cdot q_j - d = n \cdot (q_j - c) + (n \cdot c - d)$. Expanding the square and using $\sum_j (q_j - c) = 0$, the cross term vanishes, so

$$E(n, d) = \sum_j (n \cdot (q_j - c))^2 + k (n \cdot c - d)^2.$$

The second term is zero exactly at $d = n \cdot c$, and the first term is $k\, n^\top C n$. $\square$

**Theorem 1 (line L6 gives the least squares plane).** The unit vector $v_0$ minimizes $E(n, n \cdot c)$ over all unit $n$, and the least value is $k \lambda_0$. If $\lambda_0 < \lambda_1$, the minimizers are exactly $\pm v_0$.

*Proof.* Write a unit $n$ as $n = \sum_i \alpha_i v_i$ with $\sum_i \alpha_i^2 = 1$. Then $n^\top C n = \sum_i \lambda_i \alpha_i^2 \ge \lambda_0 \sum_i \alpha_i^2 = \lambda_0$, with equality at $n = v_0$. If $\lambda_0 < \lambda_1$, equality forces $\alpha_1 = \alpha_2 = 0$, so $n = \pm v_0$. With Lemma 1, the plane through $c$ with normal $v_0$ minimizes $E(n, d)$ over all planes. $\square$

So the normal of line L6 is the normal of the total least squares plane of the neighborhood, the plane that minimizes the sum of squared orthogonal distances. When $\lambda_0 = \lambda_1$, for example on a line of points or a symmetric blob, every unit vector of the span of $v_0$ and $v_1$ is equally good, and the normal is not defined by the data.

**Theorem 2 (surface variation).** Let $\sigma = \lambda_0 / (\lambda_0 + \lambda_1 + \lambda_2)$ as at line L7, defined when the points are not all equal. Then $0 \le \sigma \le 1/3$, $\sigma = 0$ exactly when the $k$ points lie in one plane, and $\sigma = 1/3$ exactly when $\lambda_0 = \lambda_1 = \lambda_2$.

*Proof.* The sum $\lambda_0 + \lambda_1 + \lambda_2 = \mathrm{trace}(C) = \frac1k \sum_j \|q_j - c\|^2$ is positive when the points are not all equal. Since $\lambda_0 \ge 0$, $\sigma \ge 0$. Since $\lambda_0$ is the least of three numbers, $3\lambda_0 \le \lambda_0 + \lambda_1 + \lambda_2$, so $\sigma \le 1/3$, with equality exactly when the three are equal. Finally $\lambda_0 = 0$ holds exactly when $v_0^\top C v_0 = \frac1k \sum_j (v_0 \cdot (q_j - c))^2 = 0$, that is, when every $q_j$ lies on the plane through $c$ with normal $v_0$; and if the points lie on any plane, Lemma 1 and Theorem 1 give $k \lambda_0 \le E = 0$. $\square$

**Theorem 3 (rigid motions and the viewpoint).** If every point is moved by $x \mapsto R x + t$ with $R$ a rotation, the neighborhoods do not change, the normal becomes $\pm R v_0$, and $\sigma$ does not change. With a viewpoint $o$, line L8 returns the one of $\pm v_0$ with $n \cdot (o - p) \ge 0$.

*Proof.* Distances do not change, so line L2 picks the same indices (ties are broken by index). The centroid becomes $R c + t$, and the covariance becomes $R C R^\top$, which has the same eigenvalues and the eigenvectors $R v_i$. Line L8 flips $n$ exactly when $n \cdot (o - p) < 0$, and the flipped vector has $-n \cdot (o - p) > 0$. $\square$

Each neighborhood is processed in a fixed number of steps once the eigenvectors are found, and the Jacobi method of the helper stops after at most 100 sweeps, so the procedure terminates. The eigenvectors are computed in floating point, so in practice the results hold up to rounding. $\blacksquare$
