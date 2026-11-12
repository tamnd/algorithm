---
title: The alignment error is a trace form whose bottom eigenvectors give the coordinates
proves: [correctness]
status: full
---

Fix a neighborhood $N_i$ with $s$ points. Let $X$ be the centered $s \times d$ matrix of line L2, $g_1, \dots, g_m$ its top $m$ left singular vectors, $\Theta_i = [g_1, \dots, g_m]^\top \in \mathbb{R}^{m \times s}$, and $G_i = [\mathbf{1}/\sqrt s, g_1, \dots, g_m]$. Let $J_s = I - \frac1s\mathbf{1}\mathbf{1}^\top$.

**Lemma 1 ($G_i$ has orthonormal columns).** Each $g_l$ is orthogonal to $\mathbf{1}$, so $G_i^\top G_i = I$, and $W_i = I - G_iG_i^\top$ is the orthogonal projection onto the complement of the span of $\mathbf{1}, g_1, \dots, g_m$.

*Proof.* The columns of $X$ sum to 0, so $\mathbf{1}^\top X = 0$ and $\mathbf{1}$ is in the null space of $XX^\top$. Each $g_l$ is an eigenvector of $XX^\top$. If its eigenvalue is positive, then $g_l = XX^\top g_l/\sigma_l^2$ is in the column space of $X$, which is orthogonal to $\mathbf{1}$. If $m$ exceeds the rank of $X$, the eigensolver can still return a $g_l$ with eigenvalue 0 that is not orthogonal to $\mathbf{1}$; we assume $m \le \operatorname{rank}(X)$, as the method requires. Singular vectors are orthonormal, so $G_i^\top G_i = I$, and then $W_i^2 = W_i = W_i^\top$. $\square$

**Lemma 2 (the local fit).** For a fixed row vector $t \in \mathbb{R}^{1 \times s}$, $\min_{c, \ell} \|t - c\mathbf{1}^\top - \ell\Theta_i\|^2 = \|tW_i\|^2$, with $c \in \mathbb{R}$ and $\ell \in \mathbb{R}^{1 \times m}$. The same holds row by row for a matrix $T_i$, which gives $\min \|T_iJ_s - L_i\Theta_i\|_F^2 = \|T_iW_i\|_F^2$.

*Proof.* The rows $c\mathbf{1}^\top + \ell\Theta_i$ are exactly the row space of $G_i^\top$, and the closest point of a subspace is the orthogonal projection, so the residual is $t(I - G_iG_i^\top) = tW_i$. For the form with $J_s$, $tJ_s = t - \bar t\mathbf{1}^\top$, so minimizing over $\ell$ alone with $tJ_s$ in place of $t$ is the same as minimizing over $c$ and $\ell$ with $t$. $\square$

**Lemma 3 (the global form).** Let $B = \sum_i S_iW_iS_i^\top$, where $S_i \in \mathbb{R}^{n \times s}$ selects the points of $N_i$. Then $B$ is symmetric positive semidefinite, $B\mathbf{1} = 0$, and for $T \in \mathbb{R}^{m \times n}$, $\sum_i \|T_iW_i\|_F^2 = \operatorname{tr}(TBT^\top)$ with $T_i = TS_i$.

*Proof.* $\|T_iW_i\|_F^2 = \operatorname{tr}(T_iW_iW_i^\top T_i^\top) = \operatorname{tr}(TS_iW_iS_i^\top T^\top)$, because $W_iW_i^\top = W_i$. Sum over $i$. Each term is a symmetric positive semidefinite matrix. $S_i^\top\mathbf{1}_n = \mathbf{1}_s$ and $W_i\mathbf{1}_s = 0$, because $\mathbf{1}_s/\sqrt s$ is a column of $G_i$, so $B\mathbf{1} = 0$. $\square$

**Theorem 1 (the minimizer).** Let $\mu_1 \le \dots \le \mu_{n-1}$ be the eigenvalues of $B$ on $\mathbf{1}^\perp$, with orthonormal eigenvectors $u_1, \dots, u_{n-1}$. Over $T$ with $TT^\top = I$ and $T\mathbf{1} = 0$, the minimum of $\operatorname{tr}(TBT^\top)$ is $\mu_1 + \dots + \mu_m$, attained by $T = [u_1, \dots, u_m]^\top$.

*Proof.* $B$ maps $\mathbf{1}^\perp$ to itself, since it is symmetric and $B\mathbf{1} = 0$. The rows of $T$ are an orthonormal $m$-frame in $\mathbf{1}^\perp$, and Ky Fan's minimum principle on that subspace gives the bound and the minimizer. The implementation finds $u_1, \dots, u_m$ as the $m$ smallest eigenvectors of $B + \frac cn\mathbf{1}\mathbf{1}^\top$ with $c = \operatorname{tr}(B) + 1$. This matrix agrees with $B$ on $\mathbf{1}^\perp$ and has the eigenvalue $c$, larger than all $\mu_l$, on $\mathbf{1}$. $\square$

**Theorem 2 (exact recovery on flat data).** Suppose that for each $i$ there are an invertible $m \times m$ matrix $P_i$ and a vector $q_i$ with $\theta_j = P_i\Theta_i[\cdot, j] + q_i$ for the points $j$ of $N_i$, where $\theta_j \in \mathbb{R}^m$ are the true coordinates. Then every row $f$ of $\Theta^{\text{true}} = [\theta_1, \dots, \theta_n]$ satisfies $Bf^\top = 0$. If the null space of $B$ has dimension $m + 1$, the output $T$ has the same row space as the centered true coordinates, so $\tau_j = G\theta_j + h$ for an invertible $G$ and a vector $h$.

*Proof.* On $N_i$, each true coordinate is $c\mathbf{1}^\top + \ell\Theta_i$ for some $c$ and $\ell$, so by Lemma 2 its residual $fS_iW_i$ is 0. By Lemma 3, $f B f^\top = 0$, and $Bf^\top = 0$ because $B$ is positive semidefinite. If the null space is the span of $\mathbf{1}$ and the $m$ true coordinate rows, then the eigenvalues $\mu_1, \dots, \mu_m$ are 0, and their eigenvectors span the projections of the true coordinate rows onto $\mathbf{1}^\perp$, which are the centered coordinates. $\square$

On a flat region, local PCA finds an orthonormal basis of the plane through each neighborhood, so the tangent coordinates are a rotation of the true coordinates, scaled column by column by the singular values: the assumption holds. The test suite checks this on the non-convex L-shaped region, and the example on the page checks it on a line, where the null space is spanned by $\mathbf{1}$ and $(0, 1, 2, 3, 4)$.
