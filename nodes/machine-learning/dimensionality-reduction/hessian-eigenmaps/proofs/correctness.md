---
title: The discrete Hessian form vanishes exactly on affine functions of the tangent coordinates
proves: [correctness]
status: full
---

Fix a neighborhood $N_i$ with $s = k + 1$ points and tangent coordinates $U \in \mathbb{R}^{s \times m}$ from line L3. Let $p = 1 + m + m(m+1)/2$, and let $A \in \mathbb{R}^{s \times p}$ be the matrix of line L4, with the column blocks $A_0 = \mathbf{1}$, $A_1 = U$ and $A_2$, the products $U_a U_b$ for $a \le b$. Assume the columns of $A$ are linearly independent, so $s \ge p$. A function on the data is a vector $f \in \mathbb{R}^n$, and $f_{N_i}$ is its restriction to $N_i$.

**Lemma 1 (the estimator).** Gram-Schmidt on the columns of $A$ in order gives $A = QR$ with orthonormal columns $Q = [Q_0, Q_1, Q_2]$ and an upper triangular $R$ with a positive diagonal. Let $H_i = Q_2^\top$. Then:

1. $H_i g = 0$ for every $g$ in the span of the columns of $A_0$ and $A_1$, the affine functions of the tangent coordinates.
2. If $g = A c$ for a coefficient vector $c = (c_0, c_1, c_2)$, then $H_i g = R_{22}c_2$, where $R_{22}$ is the invertible lower right block of $R$. So $H_i g$ depends only on the second-order coefficients $c_2$, and it is 0 only if $c_2 = 0$.

*Proof.* Gram-Schmidt makes the first $j$ columns of $Q$ span the first $j$ columns of $A$, for each $j$. So the columns of $Q_0$ and $Q_1$ span the columns of $A_0$ and $A_1$, and the columns of $Q_2$ are orthogonal to them, which gives part 1. For part 2, $Q^\top g = Q^\top QRc = Rc$, and the last block row of the upper triangular $R$ is $[0, 0, R_{22}]$, so $Q_2^\top g = R_{22}c_2$. The diagonal of $R_{22}$ is positive, so $R_{22}$ is invertible. $\square$

**Lemma 2 (the global form).** The matrix $H$ of line L6 is symmetric and positive semidefinite, and $f^\top H f = \sum_i \|H_i f_{N_i}\|^2$.

*Proof.* $H = \sum_i S_i^\top H_i^\top H_i S_i$, where $S_i$ selects the rows of $N_i$. Each term is symmetric, and $f^\top S_i^\top H_i^\top H_i S_i f = \|H_i f_{N_i}\|^2 \ge 0$. $\square$

**Theorem 1 (affine functions of the true coordinates are in the null space).** Suppose that for each $i$ the tangent coordinates are an affine image of the true coordinates on $N_i$: $U_{j\cdot} = G_i\theta_j + b_i$ for $j \in N_i$, with $G_i$ an invertible $m \times m$ matrix. Then $Hf = 0$ for $f = \mathbf{1}$ and for each $f = (\theta_1[l], \dots, \theta_n[l])$, $l = 1, \dots, m$.

*Proof.* On $N_i$, $\theta_j = G_i^{-1}(U_{j\cdot} - b_i)$, so each coordinate of $\theta$, restricted to $N_i$, is an affine function of the tangent coordinates, and so is the constant. By Lemma 1, $H_i f_{N_i} = 0$ for each $i$, so $f^\top H f = 0$ by Lemma 2. For a positive semidefinite $H$, $f^\top H f = 0$ implies $Hf = 0$. $\square$

On a flat sheet, the points of $N_i$ lie in an $m$-dimensional affine subspace, local PCA finds an orthonormal basis of it, and the assumption holds with an orthogonal $G_i$. This is the case of the exact tests. On a curved manifold it holds up to an error that goes to 0 as the neighborhoods shrink, which is the setting of the theorem of Donoho and Grimes.

**Theorem 2 (functions with zero Hessian form are affine on a connected sample).** Suppose that for each $i$ the null space of $H_i$ is exactly the set of affine functions of the tangent coordinates on $N_i$, and that the assumption of Theorem 1 holds. Suppose also that any two neighborhoods are joined by a chain in which consecutive neighborhoods share at least $m + 1$ affinely independent points. If $f^\top H f = 0$, then $f$ is one affine function of the true coordinates on all points.

*Proof.* By Lemma 2, $H_i f_{N_i} = 0$ for all $i$, so by the first assumption $f_{N_i}$ is affine in the tangent coordinates on $N_i$, hence affine in $\theta$ with some map $\alpha_i$, by the assumption of Theorem 1. Two affine maps on $\mathbb{R}^m$ that agree on $m + 1$ affinely independent points are equal, so consecutive neighborhoods in a chain have the same map, and the chains make all maps equal. $\square$

The first assumption holds when $s = p$: then the columns of $A$ span $\mathbb{R}^s$, every $g$ is $Ac$ for some $c$, and Lemma 1 part 2 shows that $H_i g = 0$ only if $c_2 = 0$. When $s > p$, the null space of $H_i$ also contains the vectors orthogonal to all columns of $A$, which the local estimator does not see. The overlap of many neighborhoods usually removes them from the null space of $H$, but this is not guaranteed, and the dimension of the null space must be read from the eigenvalues. The test suite checks that the $(m+1)$-st smallest eigenvalue on the vectors orthogonal to the constant is clearly positive.

**Corollary (recovery).** Under the assumptions of Theorems 1 and 2, or whenever the null space of $H$ has dimension $m + 1$ and Theorem 1 applies, the null space of $H$ is exactly the span of $\mathbf{1}$ and the $m$ true coordinate vectors. Line L7 discards the constant (in the implementation, by the shift $c\,\mathbf{1}\mathbf{1}^\top/n$, as for LLE), and the remaining $m$ eigenvectors with eigenvalue 0 span the centered true coordinates. So the output is $y_j = G\theta_j + h$ for an invertible $G$, and the final normalization of line L8 turns $G$ into an orthogonal matrix. The convexity of the parameter region is not used anywhere: only the local affine structure and the chains of overlapping neighborhoods.

**The example.** For $m = 1$ and the neighborhood $u = (-1, 0, 1)$, Gram-Schmidt on $(1,1,1)$, $(-1,0,1)$, $(1,0,1)$ gives $H_i = (1, -2, 1)/\sqrt6$, as on the page. For $g = c_0 + c_1u + c_2u^2 = (c_0 - c_1 + c_2,\ c_0,\ c_0 + c_1 + c_2)$, we get $H_i g = (c_0 - c_1 + c_2 - 2c_0 + c_0 + c_1 + c_2)/\sqrt6 = 2c_2/\sqrt6$. This matches Lemma 1 with $R_{22} = \|u^2 - \frac23\mathbf{1}\| = \sqrt{6}/3 = 2/\sqrt6$, and it vanishes exactly when $c_2 = 0$. Here $s = p = 3$, so the null space of $H_i$ is exactly the affine functions.
