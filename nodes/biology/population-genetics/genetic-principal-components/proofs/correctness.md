---
title: The normalized matrix is positive semidefinite with the all-ones vector in its kernel, orthogonal iteration converges to the top eigenspace, and the EIGENSTRAT step is a projection
proves: [correctness]
status: full
---

**Setting.** $M$ is the $n \times m'$ matrix of lines L1 to L3, and $X = M M^{\mathsf T} / m'$ is the matrix of line L4. Let $\lambda_1 \ge \cdots \ge \lambda_n$ be the eigenvalues of $X$ with orthonormal eigenvectors $u_1, \ldots, u_n$. Write $U_1 = (u_1, \ldots, u_k)$, $U_2 = (u_{k+1}, \ldots, u_n)$, $\Lambda_1 = \mathrm{diag}(\lambda_1, \ldots, \lambda_k)$ and $\Lambda_2 = \mathrm{diag}(\lambda_{k+1}, \ldots, \lambda_n)$.

**Lemma 1 (structure of $X$).** $X$ is symmetric and positive semidefinite, $X \mathbf 1 = 0$, and every eigenvector of $X$ with a positive eigenvalue is orthogonal to $\mathbf 1$.

*Proof.* $X^{\mathsf T} = X$ is clear, and $v^{\mathsf T} X v = \lVert M^{\mathsf T} v \rVert^2 / m' \ge 0$. Each column of $M$ is $(g_{\cdot j} - \mu_j \mathbf 1)/s_j$, and its entries sum to $n \mu_j - n \mu_j = 0$, so $M^{\mathsf T} \mathbf 1 = 0$ and $X \mathbf 1 = 0$. If $X v = \lambda v$ with $\lambda > 0$, then $\lambda \mathbf 1^{\mathsf T} v = \mathbf 1^{\mathsf T} X v = (X \mathbf 1)^{\mathsf T} v = 0$, so $\mathbf 1^{\mathsf T} v = 0$. $\square$

So the rank of $X$ is at most $n - 1$, and the eigenvalues sum to the trace, $\frac{1}{m'} \sum_{i, j} M_{ij}^2$.

**Lemma 2 (spans).** Let $Q_0$ be the matrix of line L5 and $Q_t$ the matrix after $t$ rounds of lines L7 and L9. If $X^t Q_0$ has full column rank, then for each $j \le k$ the first $j$ columns of $Q_t$ span the same space as the first $j$ columns of $X^t Q_0$.

*Proof.* Gram-Schmidt on vectors $z_1, \ldots, z_k$ of full rank gives orthonormal $q_1, \ldots, q_k$ with $\mathrm{span}(q_1, \ldots, q_j) = \mathrm{span}(z_1, \ldots, z_j)$ for each $j$; that is, $Z = Q R$ with $R$ upper triangular and invertible. Then $X Q_{t-1} = Q_t R_t$, and by induction $X^t Q_0 = Q_t R_t \cdots R_1$. A product of invertible upper triangular matrices is invertible and upper triangular, which gives the claim. $\square$

**Lemma 3 (the start).** Let the entries of the $n \times k$ matrix $W$ be independent standard Gaussian, and let $Q_0$ come from $W$ by Gram-Schmidt. Then $C_1 = U_1^{\mathsf T} Q_0$ is invertible with probability 1.

*Proof.* $Q_0 = W R^{-1}$ with $R$ invertible (with probability 1 the columns of $W$ are independent). So $C_1$ is invertible exactly when $U_1^{\mathsf T} W$ is. Because $U_1$ has orthonormal columns, the entries of $U_1^{\mathsf T} W$ are independent standard Gaussian, and the determinant of a $k \times k$ Gaussian matrix is a non-zero polynomial in its entries, which is 0 only on a set of measure 0. $\square$

**Theorem 1 (convergence of the subspace).** Suppose $\lambda_k > \lambda_{k+1}$ and $C_1$ is invertible, and let $C_2 = U_2^{\mathsf T} Q_0$. Let $P_t$ be the orthogonal projection onto $\mathrm{span}(Q_t)$ and $P$ the projection onto $\mathrm{span}(U_1)$. Then $\lVert P_t - P \rVert_2 \le \lVert C_2 C_1^{-1} \rVert_2 (\lambda_{k+1} / \lambda_k)^t$.

*Proof.* $Q_0 = U_1 C_1 + U_2 C_2$, so $X^t Q_0 = U_1 \Lambda_1^t C_1 + U_2 \Lambda_2^t C_2$. Multiply on the right by the invertible matrix $C_1^{-1} \Lambda_1^{-t}$ (here $\lambda_k > \lambda_{k+1} \ge 0$, so $\Lambda_1$ is invertible). This does not change the column span, and gives $Y_t = U_1 + U_2 E_t$ with $E_t = \Lambda_2^t C_2 C_1^{-1} \Lambda_1^{-t}$. Since $\lVert \Lambda_2^t \rVert_2 = \lambda_{k+1}^t$ and $\lVert \Lambda_1^{-t} \rVert_2 = \lambda_k^{-t}$, we get $\lVert E_t \rVert_2 \le \lVert C_2 C_1^{-1} \rVert_2 (\lambda_{k+1} / \lambda_k)^t$. In the basis $(U_1, U_2)$, the span of $Y_t$ is the graph of $E_t$. For the graph of a matrix $E$, the distance $\lVert P_E - P \rVert_2$ between the projections equals $\sin \theta$, with $\tan \theta = \lVert E \rVert_2$ the tangent of the largest principal angle, so it is at most $\lVert E \rVert_2$. By Lemma 2, $Y_t$ has the same span as $Q_t$. $\square$

**Lemma 4 (Rayleigh-Ritz).** Let $Q$ have orthonormal columns and let $S = Q^{\mathsf T} X Q = V \Theta V^{\mathsf T}$ be the eigendecomposition of line L11. If $\mathrm{span}(Q)$ is invariant under $X$, then the columns of $Q V$ are eigenvectors of $X$ with eigenvalues $\Theta$. In general, the $c$-th largest Ritz value $\theta_c$ satisfies $\theta_c \le \lambda_c$.

*Proof.* If $X Q = Q S$ for some $S$, then $S = Q^{\mathsf T} X Q$ and $X Q V = Q S V = Q V \Theta$. For the bound, by the Courant-Fischer theorem $\theta_c$ is the maximum over $c$-dimensional subspaces $W$ of $\mathrm{span}(Q)$ of the minimum Rayleigh quotient on $W$, and $\lambda_c$ is the same maximum over all $c$-dimensional subspaces of $\mathbb R^n$. $\square$

With Theorem 1, $\mathrm{span}(Q_t)$ tends to the top eigenspace, so the output of line L11 tends to $\lambda_1, \ldots, \lambda_k$ and to eigenvectors $u_1, \ldots, u_k$, up to sign; the sign rule of the code fixes the sign. When some of $\lambda_1, \ldots, \lambda_k$ are equal, the eigenvectors inside the equal group are any orthonormal basis of its eigenspace. The stopping rule of line L10 tests the change of the Ritz values, which is a heuristic; the theorem bounds the error of the limit process, not of the stop.

**Lemma 5 (singular vectors).** If $M = A \Sigma B^{\mathsf T}$ is a singular value decomposition, then the columns of $A$ are eigenvectors of $X$ with eigenvalues $\sigma_c^2 / m'$.

*Proof.* $X = A \Sigma B^{\mathsf T} B \Sigma A^{\mathsf T} / m' = A (\Sigma^2 / m') A^{\mathsf T}$. $\square$

**Lemma 6 (the EIGENSTRAT step).** Let $v_1, \ldots, v_k$ be orthonormal eigenvectors of $X$ with positive eigenvalues. For any $y \in \mathbb R^n$, the vector $r$ computed by the function residualize is the orthogonal projection of $y$ onto the complement of $\mathrm{span}(\mathbf 1, v_1, \ldots, v_k)$, which is the residual of the least squares regression of $y$ on an intercept and the $k$ axes.

*Proof.* By Lemma 1, $\mathbf 1 / \sqrt n, v_1, \ldots, v_k$ are orthonormal. Removing the mean subtracts the projection on $\mathbf 1 / \sqrt n$. Each later step subtracts $(v_c^{\mathsf T} r) v_c$. For an orthonormal set, subtracting the projections one at a time gives the projection onto the complement of their span, because each step leaves the earlier coefficients at 0. The least squares residual on a set of regressors is this projection. $\square$

So $r$ in the statistic $(n - k - 1) r^2$ is the partial correlation of the genotype and the phenotype given the axes, and $n - k - 1$ is the residual degrees of freedom. That this statistic is close to a chi-square law with 1 degree of freedom under the null is an asymptotic approximation of linear regression, not a fact proved here.
