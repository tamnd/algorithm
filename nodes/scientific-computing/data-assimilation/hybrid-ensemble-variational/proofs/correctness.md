---
title: The alpha control variable minimizes the 3D-Var cost with the hybrid covariance
proves: [correctness, termination]
status: full
---

**Setting.** $B_c = U_cU_c^\top$ and $L = U_LU_L^\top$ are symmetric positive semidefinite $n \times n$ matrices, $x'_1, \ldots, x'_N$ are the scaled ensemble perturbations of line L1, $D_i = \mathrm{diag}(x'_i)$, $\beta_c^2, \beta_e^2 \ge 0$, $H$ is a $p \times n$ matrix, $R$ is symmetric positive definite and $d = y - Hx^b$. The control is $w = (v_c, \alpha_1, \ldots, \alpha_N) \in \mathbb R^{n(N+1)}$, and line L4 is the linear map

$$Uw = \beta_c U_c v_c + \beta_e \sum_{i=1}^N D_i U_L \alpha_i .$$

The cost is $J(w) = \tfrac12 |w|^2 + \tfrac12 (d - HUw)^\top R^{-1}(d - HUw)$.

**Lemma 1 (the implied covariance).**

$$UU^\top = \beta_c^2 B_c + \beta_e^2\, L \circ \Big(\sum_{i=1}^N x'_i x'^\top_i\Big) =: B_h .$$

*Proof.* The blocks of $U$ are $\beta_c U_c$ and $\beta_e D_iU_L$, so $UU^\top = \beta_c^2 U_cU_c^\top + \beta_e^2 \sum_i D_i U_LU_L^\top D_i = \beta_c^2 B_c + \beta_e^2 \sum_i D_i L D_i$. The entry $(j, k)$ of $D_iLD_i$ is $x'_{ij} L_{jk} x'_{ik}$, so $\sum_i D_iLD_i = L \circ \sum_i x'_ix'^\top_i$. $\square$

In particular $B_h$ is positive semidefinite, which is the Schur product theorem for $L$ and the sample covariance $X'X'^\top$.

**Theorem 2.** The minimizer $w^\ast$ of $J$ is unique, and

$$x^b + Uw^\ast = x^b + B_hH^\top (HB_hH^\top + R)^{-1} d ,$$

which is the minimizer of the 3D-Var cost with background covariance $B_h$ when $B_h$ is positive definite, and the best linear unbiased estimate with that covariance in every case.

*Proof.* $J$ is a quadratic with Hessian $A = I + U^\top H^\top R^{-1} HU$, which is symmetric positive definite, so $w^\ast = A^{-1} U^\top H^\top R^{-1} d$ is the unique minimizer. The identity

$$(I + U^\top H^\top R^{-1}HU)\, U^\top H^\top = U^\top H^\top R^{-1}(R + HUU^\top H^\top)$$

holds by expanding both sides. Multiply it by $A^{-1}$ on the left and by $(R + HUU^\top H^\top)^{-1}$ on the right: $U^\top H^\top (HB_hH^\top + R)^{-1} = A^{-1}U^\top H^\top R^{-1}$, using Lemma 1. So $w^\ast = U^\top H^\top (HB_hH^\top + R)^{-1} d$ and $Uw^\ast = B_hH^\top (HB_hH^\top + R)^{-1} d$. If $B_h$ is positive definite, this is the 3D-Var minimizer $x^b + B_hH^\top (HB_hH^\top + R)^{-1}d$ (the Kalman gain form of the 3D-Var normal equations). $\square$

**Termination.** $A - I = U^\top H^\top R^{-1}HU$ has rank at most $p$, so $A$ has at most $p + 1$ distinct eigenvalues, and the conjugate gradient method of line L7 reaches $w^\ast$ in at most $p + 1$ steps in exact arithmetic. The code also stops after at most $2n(N + 1)$ steps.

**Limits.** With $\beta_e = 0$ the result is 3D-Var with $\beta_c^2B_c$. With $\beta_c = 0$ and $L$ the matrix of ones it is the analysis with the raw sample covariance, whose increment $B_hH^\top(\cdot)$ lies in the span of the perturbations.

**Summary.** The alpha control variable gives the same analysis as 3D-Var with the hybrid covariance $\beta_c^2B_c + \beta_e^2 L \circ X'X'^\top$ (Wang, Snyder and Hamill 2007), and it never forms that matrix. The tests check the analysis to $10^{-8}$ against a direct solve with the hybrid covariance on random problems, and the two limits. $\blacksquare$
