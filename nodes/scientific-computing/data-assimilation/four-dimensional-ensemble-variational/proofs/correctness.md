---
title: 4DEnVar conditions on all observations of the window with the localized four-dimensional ensemble covariance
proves: [correctness, termination]
status: full
---

**Setting.** The window has the time levels $0, \ldots, K$, and $T$ is the set of observation times. Lines L1 and L2 give the background trajectory $x^b_k$ and the member trajectories $x_i(k)$, $i = 1, \ldots, N$, with $N \ge 2$. Let $x'_i(k) = (x_i(k) - \bar x(k))/\sqrt{N - 1}$, let $X'_k$ be the $n \times N$ matrix with the columns $x'_i(k)$, and let $D_i(k) = \mathrm{diag}(x'_i(k))$. $L = U_LU_L^\top$ is symmetric positive semidefinite (line L3). For $k \in T$, $H_k$ is a $p_k \times n$ matrix, $R_k$ is symmetric positive definite and $d_k = y_k - H_kx^b_k$ (line L4). The control is $\alpha = (\alpha_1, \ldots, \alpha_N) \in \mathbb R^{Nn}$, and line L5 is the linear map

$$U_k\alpha = \sum_{i=1}^N D_i(k)\, U_L\alpha_i .$$

The cost is $J(\alpha) = \tfrac12 |\alpha|^2 + \sum_{k \in T} \tfrac12 (d_k - H_kU_k\alpha)^\top R_k^{-1}(d_k - H_kU_k\alpha)$. Stack the times of $T$: $\mathbf U$ has the block rows $U_k$, $\mathbf H = \mathrm{diag}(H_k)$, $\mathbf R = \mathrm{diag}(R_k)$ and $\mathbf d$ has the blocks $d_k$. Then $J(\alpha) = \tfrac12|\alpha|^2 + \tfrac12(\mathbf d - \mathbf H\mathbf U\alpha)^\top\mathbf R^{-1}(\mathbf d - \mathbf H\mathbf U\alpha)$, and $p = \sum_k p_k$.

**Lemma 1 (the implied four-dimensional covariance).** For all times $k$ and $l$,

$$U_kU_l^\top = L \circ (X'_kX'^\top_l) =: C_{kl} .$$

*Proof.* $U_k$ has the blocks $D_i(k)U_L$, so $U_kU_l^\top = \sum_i D_i(k)\,U_LU_L^\top D_i(l) = \sum_i D_i(k) L D_i(l)$. The entry $(j, m)$ of $D_i(k)LD_i(l)$ is $x'_{ij}(k) L_{jm} x'_{im}(l)$, and the sum over $i$ is $L_{jm}(X'_kX'^\top_l)_{jm}$. $\square$

So the same control $\alpha$ at all times gives increments whose covariance between times $k$ and $l$ is the localized sample covariance of the ensemble between those times. The block matrix $\mathbf C = \mathbf U\mathbf U^\top$ with the blocks $C_{kl}$ is positive semidefinite.

**Theorem 2.** The minimizer $\alpha^\ast$ of $J$ is unique, and the analysis of line L9 is

$$x^a_k = x^b_k + U_k\alpha^\ast = x^b_k + \sum_{l \in T} C_{kl} H_l^\top w_l, \qquad w = (\mathbf H\mathbf C\mathbf H^\top + \mathbf R)^{-1}\mathbf d .$$

This is the conditional mean of the increments at time $k$ given all observations of the window, for a Gaussian prior with the covariance blocks $C_{kl}$.

*Proof.* $J$ is a quadratic with Hessian $A = I + \mathbf U^\top\mathbf H^\top\mathbf R^{-1}\mathbf H\mathbf U$, which is symmetric positive definite, so $\alpha^\ast = A^{-1}\mathbf U^\top\mathbf H^\top\mathbf R^{-1}\mathbf d$ is the unique minimizer. Line L6 computes the right side $b = \mathbf U^\top\mathbf H^\top\mathbf R^{-1}\mathbf d$, and line L7 applies $A$. Expanding both sides gives

$$(I + \mathbf U^\top\mathbf H^\top\mathbf R^{-1}\mathbf H\mathbf U)\,\mathbf U^\top\mathbf H^\top = \mathbf U^\top\mathbf H^\top\mathbf R^{-1}(\mathbf R + \mathbf H\mathbf U\mathbf U^\top\mathbf H^\top).$$

Multiply on the left by $A^{-1}$ and on the right by $(\mathbf R + \mathbf H\mathbf C\mathbf H^\top)^{-1}$: $\mathbf U^\top\mathbf H^\top(\mathbf H\mathbf C\mathbf H^\top + \mathbf R)^{-1} = A^{-1}\mathbf U^\top\mathbf H^\top\mathbf R^{-1}$. So $\alpha^\ast = \mathbf U^\top\mathbf H^\top w$ and $U_k\alpha^\ast = \sum_l U_kU_l^\top H_l^\top w_l = \sum_l C_{kl}H_l^\top w_l$ by Lemma 1. For jointly Gaussian increments $\delta x_k$ with the covariances $C_{kl}$ and observations $\mathbf d = \mathbf H\,\delta\mathbf x + \epsilon$, $\epsilon \sim N(0, \mathbf R)$, the conditional mean of $\delta x_k$ is $\mathrm{Cov}(\delta x_k, \mathbf d)\,\mathrm{Cov}(\mathbf d)^{-1}\mathbf d$, and this is the same expression. $\square$

**Theorem 3 (equivalence with 4D-Var).** Let the model be linear, $x_k = M_kx_{k-1}$, with $M^{(k)} = M_k\cdots M_1$ and $M^{(0)} = I$. Let $L$ be the matrix of ones and let $X'_0X'^\top_0 = B$ be positive definite (this needs $N \ge n + 1$). Then $x^a_0$ is the minimizer of the strong-constraint 4D-Var cost with background covariance $B$, and $x^a_k = M^{(k)}x^a_0$ for every $k$.

*Proof.* The model is linear, so $x_i(k) = M^{(k)}x_i(0)$, $\bar x(k) = M^{(k)}\bar x(0)$ and $X'_k = M^{(k)}X'_0$. With $L$ the matrix of ones, $C_{kl} = M^{(k)}BM^{(l)\top}$. Let $G$ have the block rows $H_kM^{(k)}$, $k \in T$. Then $\mathbf H\mathbf C\mathbf H^\top = GBG^\top$, $\mathbf d = \mathbf y - Gx^b$ and, by Theorem 2,

$$x^a_0 = x^b + BG^\top(GBG^\top + \mathbf R)^{-1}(\mathbf y - Gx^b).$$

The 4D-Var cost $\tfrac12(x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \tfrac12(\mathbf y - Gx_0)^\top\mathbf R^{-1}(\mathbf y - Gx_0)$ is a quadratic in $x_0$, and its minimizer $x^b + (B^{-1} + G^\top\mathbf R^{-1}G)^{-1}G^\top\mathbf R^{-1}(\mathbf y - Gx^b)$ is the same vector by the Sherman-Morrison-Woodbury identity $(B^{-1} + G^\top\mathbf R^{-1}G)^{-1}G^\top\mathbf R^{-1} = BG^\top(GBG^\top + \mathbf R)^{-1}$. Finally $C_{kl} = M^{(k)}C_{0l}$ and $x^b_k = M^{(k)}x^b$, so $x^a_k = M^{(k)}x^a_0$. $\square$

For a nonlinear model, the member trajectories replace the tangent linear model: $X'_k$ is a finite difference estimate of $M^{(k)}$ applied to $X'_0$, and the analysis $x^a_k$ is not in general a model trajectory.

**Termination.** $A - I = \mathbf U^\top\mathbf H^\top\mathbf R^{-1}\mathbf H\mathbf U$ has rank at most $p$, so $A$ has at most $p + 1$ distinct eigenvalues, and the conjugate gradient method of line L8 reaches $\alpha^\ast$ in at most $p + 1$ steps in exact arithmetic. The code also stops after at most $2Nn$ steps. The model runs only forward, $K$ steps for the background and $K$ steps for each member, so line L1 and line L2 call it $(N + 1)K$ times and the minimization does not call it at all.

**Summary.** 4DEnVar gives the analysis of all observations of the window with the localized four-dimensional covariance $L \circ (X'_kX'^\top_l)$ (Theorem 2), and for a linear model without localization and an ensemble with $X'_0X'^\top_0 = B$ it is strong-constraint 4D-Var (Theorem 3). The tests check Theorem 2 to $10^{-8}$ against a direct solve with the stacked covariance for a linear and a nonlinear model, Theorem 3 to $10^{-8}$ against the 4D-Var formula, and the count of $(N + 1)K$ model calls. $\blacksquare$
