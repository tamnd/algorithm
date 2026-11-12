---
title: LPP is Laplacian eigenmaps restricted to linear functions
proves: [correctness]
status: full
---

Let $X \in \mathbb{R}^{n \times d}$ have the points as rows, let $W$ be a symmetric weight matrix with $W_{ij} \ge 0$, $D$ its degree matrix and $L = D - W$. Put $P = X^\top LX$ and $Q = X^\top DX$.

**Lemma 1 (the cost).** For $a \in \mathbb{R}^d$ and $f = Xa$, $\frac12\sum_{i,j}W_{ij}(a^\top x_i - a^\top x_j)^2 = a^\top Pa \ge 0$ and $a^\top Qa = \sum_iD_{ii}(a^\top x_i)^2$.

*Proof.* The entries of $f$ are $f_i = a^\top x_i$. The graph Laplacian satisfies $f^\top Lf = \frac12\sum_{i,j}W_{ij}(f_i - f_j)^2$ (expand the square and use the symmetry of $W$), and $f^\top Lf = a^\top X^\top LXa$. The second identity is $f^\top Df$. $\square$

**Lemma 2 ($Q$ is positive definite).** If $X$ has full column rank and $D_{ii} > 0$ for all $i$, then $Q$ is positive definite.

*Proof.* $a^\top Qa = \sum_iD_{ii}f_i^2 \ge (\min_iD_{ii})\|Xa\|^2$, which is positive for $a \ne 0$ because $X$ has full column rank. $\square$

**Lemma 3 (the reduction).** Let $Q = RR^\top$ with $R$ lower triangular and invertible, and $M = R^{-1}PR^{-\top}$. Then $Mz = \lambda z$ if and only if $a = R^{-\top}z$ satisfies $Pa = \lambda Qa$, and $a^\top Qa' = z^\top z'$.

*Proof.* $Pa = \lambda Qa$ with $a = R^{-\top}z$ reads $PR^{-\top}z = \lambda RR^\top R^{-\top}z = \lambda Rz$; multiply on the left by $R^{-1}$. Also $a^\top Qa' = z^\top R^{-1}RR^\top R^{-\top}z' = z^\top z'$. Since $P$ is symmetric, $M = R^{-1}(R^{-1}P)^\top$ is symmetric, which is how the implementation forms it. $\square$

**Theorem 1 (the minimizer).** Suppose $Q$ is positive definite, and let $\lambda_0 \le \dots \le \lambda_{d-1}$ be the eigenvalues of $Pa = \lambda Qa$ with $Q$-orthonormal eigenvectors $a_0, \dots, a_{d-1}$. Over $A \in \mathbb{R}^{d \times m}$ with $A^\top QA = I$, the minimum of $\operatorname{tr}(A^\top PA)$ is $\lambda_0 + \dots + \lambda_{m-1}$, attained by $A = [a_0, \dots, a_{m-1}]$.

*Proof.* Put $Z = R^\top A$. Then $Z^\top Z = A^\top QA = I$ and $\operatorname{tr}(A^\top PA) = \operatorname{tr}(Z^\top MZ)$. By Ky Fan's minimum principle for the symmetric matrix $M$, the minimum over orthonormal $m$-frames is the sum of the $m$ smallest eigenvalues of $M$, attained by their eigenvectors. By Lemma 3 these are $\lambda_0, \dots, \lambda_{m-1}$, and the eigenvectors map back to $a_l = R^{-\top}z_l$. $\square$

**Theorem 2 (identity features).** If $n = d$ and $X = I_n$, and every vertex has positive degree, then LPP solves $Ly = \lambda Dy$, the problem of Laplacian eigenmaps, and the embedding of point $i$ is $y_i = a^\top e_i = a_i$.

*Proof.* $P = L$ and $Q = D$, which is positive definite. Theorem 1 gives the solutions of $La = \lambda Da$, and $f = Xa = a$. $\square$

In this case $\lambda_0 = 0$ with the constant eigenvector, which Laplacian eigenmaps discards, so the LPP solutions $a_1, a_2, \dots$ are the Laplacian eigenmaps coordinates $y_1, y_2, \dots$. The test suite checks this on a path, where they are $\cos(\pi kj/(n-1))$, and on a random heat kernel graph.

**Theorem 3 (comparison with Laplacian eigenmaps).** Let $\mu_0 \le \dots \le \mu_{n-1}$ be the eigenvalues of $Ly = \lambda Dy$, with $D$ positive definite. Under the assumptions of Theorem 1, $\lambda_l \ge \mu_l$ for $l = 0, \dots, d-1$.

*Proof.* With $g = D^{1/2}f$, the quotient $f^\top Lf / f^\top Df$ becomes the Rayleigh quotient of $N = D^{-1/2}LD^{-1/2}$, and by Lemma 1 the LPP quotient $a^\top Pa / a^\top Qa$ is the same quotient on the $d$-dimensional subspace $V = \{D^{1/2}Xa\}$. By the Courant-Fischer theorem, $\lambda_l = \min_{U \subseteq V, \dim U = l + 1}\max_{g \in U \setminus 0}g^\top Ng / g^\top g$. Restricting the subspaces $U$ to lie in $V$ can only raise the minimum, so $\lambda_l \ge \mu_l$. $\square$

So a linear projection can never keep neighbors closer than the free embedding of Laplacian eigenmaps; the price of a map for new points is a larger cost.
