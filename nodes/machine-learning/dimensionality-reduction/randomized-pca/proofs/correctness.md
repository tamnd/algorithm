---
title: Randomized PCA is exact on the projected data, and exact when the rank is at most k + p
proves: [correctness]
status: full
---

**Setup.** $X_c$ is the centered $n \times d$ data matrix. In exact arithmetic, L3 to L6 return an $n \times \ell'$ matrix $Q$ with orthonormal columns, $\ell' \le \ell$, whose range is the range of $Y = (X_c X_c^T)^q X_c \Omega$. Let $B = Q^T X_c$ and let $B = \tilde U \operatorname{diag}(s) V^T$ be its thin SVD, with $s_1 \ge s_2 \ge \cdots$.

**Lemma 1 (the range of Q).** For each $i$, the range of $Q$ after the $i$-th pass of L5 and L6 is the range of $(X_c X_c^T)^i X_c \Omega$.

*Proof.* By induction on $i$. For $i = 0$ it is L3. Suppose $\operatorname{range} Q = \operatorname{range} Z$ with $Z = (X_c X_c^T)^{i-1} X_c \Omega$. Then $Q = Z G$ and $Z = Q H$ for some matrices $G$ and $H$. L5 gives $\operatorname{range} \hat Q = \operatorname{range} X_c^T Q$, and L6 gives $\operatorname{range} Q' = \operatorname{range} X_c \hat Q = \operatorname{range} X_c X_c^T Q$. Since $X_c X_c^T Q = (X_c X_c^T Z) G$ and $X_c X_c^T Z = (X_c X_c^T Q) H$, the two ranges $\operatorname{range} X_c X_c^T Q$ and $\operatorname{range} X_c X_c^T Z$ are equal. The second one is $\operatorname{range} (X_c X_c^T)^i X_c \Omega$. $\square$

**Lemma 2 (exact PCA of the projection).** The rows $v_j^T$ of $V^T$ are orthonormal, and $Q Q^T X_c = (Q \tilde U) \operatorname{diag}(s) V^T$ is a thin SVD of $Q Q^T X_c$. So $v_1, \ldots, v_k$ are principal directions of the rows of $Q Q^T X_c$, and $s_j^2 / n$ are its covariance eigenvalues.

*Proof.* $Q Q^T X_c = Q B = Q \tilde U \operatorname{diag}(s) V^T$, and $(Q \tilde U)^T (Q \tilde U) = \tilde U^T \tilde U = I$. So this is a thin SVD. The rows of $Q Q^T X_c$ have mean zero: by Lemma 1 every column of $Q$ is in the range of $X_c$, and $\mathbf{1}^T X_c = 0$, so $\mathbf{1}^T Q = 0$ and $\mathbf{1}^T Q Q^T X_c = 0$. Hence the covariance of these rows is $\frac1n (QQ^TX_c)^T (QQ^TX_c) = V \operatorname{diag}(s^2/n) V^T$, and the columns of $V$ are its eigenvectors with the eigenvalues $s_j^2/n$. $\square$

**Theorem.** If $X_c$ has rank $r \le \ell = \min(k + p, n, d)$ and $\Omega$ has independent standard Gaussian entries, then with probability 1 the output is exact: $Q Q^T X_c = X_c$, the values $s_j^2 / n$ for $j \le k$ are the $k$ largest eigenvalues of the covariance $X_c^T X_c / n$, and $v_1, \ldots, v_k$ are corresponding orthonormal eigenvectors (each unique up to sign when the eigenvalue is simple).

*Proof.* Write the thin SVD $X_c = U_r \Sigma_r V_r^T$ with $\Sigma_r$ invertible. Then $(X_c X_c^T)^q X_c \Omega = U_r \Sigma_r^{2q+1} G$ with $G = V_r^T \Omega$, an $r \times \ell$ matrix.

The entries of $G$ are independent standard Gaussians, because $V_r$ has orthonormal columns and the Gaussian distribution of each column of $\Omega$ is invariant under rotation. The set of $r \times \ell$ matrices of rank less than $r$ is the zero set of the sum of squares of all $r \times r$ minors, a nonzero polynomial (it is nonzero at a matrix with the identity in its first $r$ columns). The zero set of a nonzero polynomial has Lebesgue measure zero, so $G$ has rank $r$ with probability 1.

Then $U_r \Sigma_r^{2q+1} G$ has the range of $U_r$, which is the range of $X_c$. By Lemma 1, $\operatorname{range} Q = \operatorname{range} X_c$, so $Q Q^T X_c = X_c$, since $QQ^T$ is the orthogonal projection on its range. By Lemma 2, $X_c = (Q\tilde U) \operatorname{diag}(s) V^T$ is a thin SVD of $X_c$. So $X_c^T X_c / n = V \operatorname{diag}(s^2 / n) V^T$, and the columns of $V$ are eigenvectors with the eigenvalues $s_j^2 / n$ in decreasing order. Every vector orthogonal to the columns of $V$ is in the null space of $X_c$, so all the nonzero eigenvalues appear among the $s_j^2 / n$. Hence the first $k$ columns of $V$ are the top $k$ principal directions, and when $k > r$ the extra values are 0. $\blacksquare$

**Remark (full rank).** When $X_c$ has rank above $\ell$, Lemma 2 still holds for every $\Omega$: the output is the exact PCA of the projection $Q Q^T X_c$, and $\|X_c - Q Q^T X_c\|_2$ measures the loss. The bounds on its expected size are Theorems 10.5 and 10.6 and Corollary 10.10 of Halko, Martinsson and Tropp (2011), which we cite and do not reprove.
