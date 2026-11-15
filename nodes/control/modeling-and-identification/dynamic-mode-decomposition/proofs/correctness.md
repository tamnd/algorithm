---
title: Exact DMD returns eigenpairs of the least squares operator, and of A for linear data
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM, and assume that the SVD and the eigenvalue computation are exact. The snapshots are $x_0, \ldots, x_M \in \mathbb{R}^q$. Let $X = (x_0, \ldots, x_{M-1})$ and $X' = (x_1, \ldots, x_M)$, both $q \times M$ (L1). Let $X = U \Sigma V^T$ be the SVD of L2, let $r$ be the rank chosen in L3, and let $U_r$, $S_r$, $V_r$ be the first $r$ left singular vectors, singular values and right singular vectors, with $S_r$ nonsingular. Then L4 computes

$$\tilde A = U_r^T X' V_r S_r^{-1},$$

and for an eigenpair $\tilde A w = \lambda w$ with $\lambda \ne 0$, L6 computes the exact DMD mode $\varphi = \lambda^{-1} X' V_r S_r^{-1} w$.

Write $X_r = U_r S_r V_r^T$ for the truncated SVD and $X_r^{+} = V_r S_r^{-1} U_r^T$ for its pseudoinverse.

**Lemma 1 (the least squares operator).** Among all $q \times q$ matrices $B$ that minimize $\lVert X' - B X_r \rVert_F$, the one of smallest Frobenius norm is $A_r = X' X_r^{+}$. If $r = \operatorname{rank} X$, then $X_r = X$ and $A_r = X' X^{+}$.

*Proof.* The minimization splits into independent least squares problems, one for each row $b^T$ of $B$: minimize $\lVert x'^T - b^T X_r \rVert$, where $x'^T$ is the matching row of $X'$. The minimum norm solution is $b^T = x'^T X_r^{+}$, a standard property of the pseudoinverse. If $r$ is the rank of $X$, the discarded singular values are zero, so $X_r = X$. $\square$

**Lemma 2 (the compressed operator).** $\tilde A = U_r^T A_r U_r$. So $\tilde A$ is the matrix of $A_r$ restricted and projected to the range of $U_r$.

*Proof.* $U_r^T A_r U_r = U_r^T X' V_r S_r^{-1} U_r^T U_r = U_r^T X' V_r S_r^{-1}$, because $U_r^T U_r = I_r$. $\square$

**Theorem 1 (Tu et al. 2014).** If $\tilde A w = \lambda w$ with $w \ne 0$ and $\lambda \ne 0$, then $\varphi = \lambda^{-1} X' V_r S_r^{-1} w$ is nonzero and $A_r \varphi = \lambda \varphi$. In particular, for $r = \operatorname{rank} X$, $(\lambda, \varphi)$ is an eigenpair of $X' X^{+}$.

*Proof.* First, $U_r^T \varphi = \lambda^{-1} U_r^T X' V_r S_r^{-1} w = \lambda^{-1} \tilde A w = w \ne 0$, so $\varphi \ne 0$. Then

$$A_r \varphi = X' V_r S_r^{-1} U_r^T \varphi = X' V_r S_r^{-1} w = \lambda \varphi.$$

The last case follows from Lemma 1. $\square$

**Lemma 3 (invariant range).** Suppose $x_{k+1} = A x_k$ for $k = 0, \ldots, M-1$ and some $q \times q$ matrix $A$, so $X' = A X$. Then the range of $X$ is invariant under $A$ if and only if $x_M$ lies in the range of $X$.

*Proof.* The range of $X$ is spanned by $x_0, \ldots, x_{M-1}$. For $k < M - 1$, $A x_k = x_{k+1}$ is one of these vectors. So the range is invariant if and only if $A x_{M-1} = x_M$ lies in it. $\square$

**Theorem 2 (linear data).** Let $X' = A X$, let $r = \operatorname{rank} X$, and let the range of $X$ be invariant under $A$. Then $A U_r = U_r \tilde A$. Every eigenvalue $\lambda$ of $\tilde A$ is an eigenvalue of $A$, and for $\lambda \ne 0$ the exact DMD mode is $\varphi = U_r w$ and satisfies $A \varphi = \lambda \varphi$.

*Proof.* With $r = \operatorname{rank} X$, $X V_r S_r^{-1} = U_r$. So $X' V_r S_r^{-1} = A X V_r S_r^{-1} = A U_r$ and $\tilde A = U_r^T A U_r$. The columns of $U_r$ span the range of $X$, which is invariant, so $A U_r = U_r C$ for some $r \times r$ matrix $C$, and $C = U_r^T A U_r = \tilde A$. If $\tilde A w = \lambda w$ with $w \ne 0$, then $A U_r w = U_r \tilde A w = \lambda U_r w$ and $U_r w \ne 0$, so $\lambda$ is an eigenvalue of $A$ with eigenvector $U_r w$. For $\lambda \ne 0$, $\varphi = \lambda^{-1} A U_r w = \lambda^{-1} U_r \tilde A w = U_r w$. $\square$

**Theorem (correctness of DMD).** Let L3 choose $r = \operatorname{rank} X$. For every nonzero eigenvalue $\lambda$ of $\tilde A$, DMD returns $\lambda$ and a nonzero vector $\varphi$ with $X' X^{+} \varphi = \lambda \varphi$. If the snapshots satisfy $x_{k+1} = A x_k$ and $x_M$ lies in the span of $x_0, \ldots, x_{M-1}$, then every returned $\lambda$ is an eigenvalue of $A$ and every returned $\varphi$ is an eigenvector of $A$ for it.

*Proof.* L5 returns the eigenvalues of $\tilde A$, the inverse iteration of L6 returns an eigenvector $w$ for each, and the mode is $\lambda^{-1} X' V_r S_r^{-1} w$. Theorem 1 gives the first statement. Lemma 3 and Theorem 2 give the second. $\blacksquare$

**Remark 1 (which eigenvalues are found).** In the setting of Theorem 2, the eigenvalues of $\tilde A$ are those of $A$ restricted to the range of $X$, the smallest $A$-invariant subspace that contains $x_0$. An eigenvalue whose mode is not excited by $x_0$ is not found. If $A$ is diagonalizable and $x_0 = \sum_l b_l v_l$ with eigenvectors $v_l$ and all $b_l \ne 0$ for distinct eigenvalues, then this subspace is spanned by the $v_l$, and $M$ at least equal to their number is enough.

**Remark 2 (truncation and noise).** If L3 chooses $r$ smaller than the rank of $X$, Theorem 1 still holds for the truncated operator $A_r$ of Lemma 1, but Theorem 2 does not apply. With noise in the snapshots, $X' = A X$ fails and the least squares operator is biased; the page reports the effect as a measurement.
