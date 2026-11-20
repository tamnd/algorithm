---
title: The local analysis of the LETKF is an exact ETKF analysis with localized observation errors
proves: [correctness, termination]
status: full
---

**Setting.** There are $N \ge 2$ forecast members $x_1, \ldots, x_N \in \mathbb R^n$ and $p$ observations $y^o$ with independent errors of variances $r_k > 0$. $X$ is the $n \times N$ matrix with columns $x_i - \bar x$ and $Y$ is the $p \times N$ matrix with columns $h(x_i) - \bar y$ (lines L1 and L2). These are unscaled perturbations, so the sample covariance is $P^f = X X^\top/(N - 1)$. Fix a grid point $j$ (line L3) and its local observations $L$ with weights $w_k > 0$ (line L4). Write $\tilde R = \mathrm{diag}(r_k / w_k)_{k \in L}$, so $S = \tilde R^{-1/2} Y_L$ and $d = \tilde R^{-1/2}(y^o - \bar y)_L$ (line L5). Let $\gamma = (N - 1)/\rho$ with the inflation $\rho > 0$, and

$$\tilde P = (\gamma I + S^\top S)^{-1}, \qquad \bar w = \tilde P S^\top d, \qquad W = \sqrt{N - 1}\,\tilde P^{1/2},$$

where $\tilde P^{1/2}$ is the symmetric positive definite square root. Lines L7 to L9 claim to return $x^a_{j,i} = \bar x_j + X_j(\bar w + W_i)$, where $X_j$ is row $j$ of $X$ and $W_i$ is column $i$ of $W$.

**Lemma 1 (the dual eigenpairs).** Let $S S^\top = V \Sigma V^\top$ with orthonormal $v_m$ (line L6), and for each $\sigma_m > 0$ let $u_m = S^\top v_m / \sqrt{\sigma_m}$. Then the $u_m$ are orthonormal, $S^\top S = \sum_m \sigma_m u_m u_m^\top$, and for every function $f$ on $(0, \infty)$

$$f(\gamma I + S^\top S) = f(\gamma) I + \sum_m \bigl(f(\gamma + \sigma_m) - f(\gamma)\bigr) u_m u_m^\top.$$

*Proof.* $u_m^\top u_l = v_m^\top S S^\top v_l / \sqrt{\sigma_m \sigma_l} = \sigma_l v_m^\top v_l/\sqrt{\sigma_m\sigma_l} = \delta_{ml}$. $S^\top S u_m = S^\top (S S^\top v_m)/\sqrt{\sigma_m} = \sigma_m u_m$. A vector $z$ orthogonal to all $u_m$ has $S z = 0$: indeed $S z = \sum_m v_m v_m^\top S z$ over the $v_m$ with $\sigma_m > 0$ (the other $v_m$ have $\|S^\top v_m\|^2 = \sigma_m = 0$, so $v_m^\top S z = 0$), and $v_m^\top S z = \sqrt{\sigma_m}\, u_m^\top z = 0$. So $\gamma I + S^\top S$ has the eigenvalue $\gamma + \sigma_m$ on $u_m$ and $\gamma$ on the orthogonal complement, which gives the formula. $\square$

With $f(t) = 1/t$, line L7 computes $\bar w = \tilde P (S^\top d)$. With $f(t) = \sqrt{(N - 1)/t}$, for which $f(\gamma) = \sqrt\rho$, line L8 computes the row vector $X_j W$. So line L9 returns the stated $x^a_{j,i}$.

**Lemma 2 (push-through identity).** For any $p_l \times N$ matrix $Y_L$ and $\tilde R$ positive definite,

$$Y_L^\top (Y_L Y_L^\top + \gamma \tilde R)^{-1} = (Y_L^\top \tilde R^{-1} Y_L + \gamma I)^{-1} Y_L^\top \tilde R^{-1}.$$

*Proof.* $(Y_L^\top \tilde R^{-1} Y_L + \gamma I) Y_L^\top = Y_L^\top \tilde R^{-1}(Y_L Y_L^\top + \gamma \tilde R)$. Both factors in brackets are invertible. Multiply on the left and on the right by their inverses. $\square$

**Theorem 3 (exact local Kalman moments).** Let $h$ be linear, $h(x) = H x$, and write $P = \rho P^f$ for the inflated sample covariance. Then the mean and the sample covariance of the values $x^a_{j,1}, \ldots, x^a_{j,N}$ are component $j$ of

$$\bar x + K (y^o - H\bar x)_L \quad\text{and}\quad \bigl[(I - K H_L) P\bigr]_{jj}, \qquad K = P H_L^\top (H_L P H_L^\top + \tilde R)^{-1}.$$

In words: grid point $j$ gets the Kalman analysis of its local observations with the error variances $r_k / w_k$ and the inflated ensemble covariance.

*Proof.* $S^\top S = Y_L^\top \tilde R^{-1} Y_L$ and $Y_L = H_L X$, so $\tilde P = (Y_L^\top \tilde R^{-1} Y_L + \gamma I)^{-1}$. Since $P = X X^\top/\gamma$, $K = X Y_L^\top (Y_L Y_L^\top + \gamma \tilde R)^{-1}$, and by Lemma 2 $K = X \tilde P Y_L^\top \tilde R^{-1}$. Hence $K (y^o - H\bar x)_L = X \tilde P S^\top d = X \bar w$.

The vector of ones $\mathbf 1$ satisfies $Y_L \mathbf 1 = 0$, so $\tilde P \mathbf 1 = \mathbf 1/\gamma$ and $W \mathbf 1 = \sqrt{(N - 1)/\gamma}\,\mathbf 1 = \sqrt\rho\,\mathbf 1$. So $\sum_i X_j W_i = \sqrt\rho\, X_j \mathbf 1 = 0$, and the mean of the $x^a_{j,i}$ is $\bar x_j + X_j \bar w$, the first claim.

The perturbations are $X_j W_i - X_j W \mathbf 1/N = X_j W_i$, so the sample covariance is $X_j W W^\top X_j^\top/(N - 1) = X_j \tilde P X_j^\top$. On the other side, $(I - K H_L) P = (X X^\top - X \tilde P Y_L^\top \tilde R^{-1} Y_L X^\top)/\gamma = X \tilde P (\tilde P^{-1} - Y_L^\top \tilde R^{-1} Y_L) X^\top/\gamma = X \tilde P X^\top$, whose entry $(j, j)$ is the same. $\square$

The same computation shows that the full matrix $X W$ has the covariance $X \tilde P X^\top$, so without localization (every weight 1, so one $\tilde P$ serves all points) the output is an ensemble whose mean and covariance are the Kalman analysis $\bar x + K d$ and $(I - KH)\rho P^f$. This is the global ETKF, and with $N = 2$, $x = (-1/\sqrt 2, 1/\sqrt 2)$, $y^o = 1$ and $r = 1$ it gives the mean $1/2$ and the variance $1/2$.

**Corollary 4 (no local observations).** If $L$ is empty, then $x^a_{j,i} = \bar x_j + \sqrt\rho\,(x_{i,j} - \bar x_j)$.

*Proof.* There are no $u_m$, so $\bar w = 0$ and $X_j W = \sqrt\rho\, X_j$ by Lemma 1. $\square$

**What is not proved.** Different grid points use different $\tilde R$ and therefore different $\tilde P$, so the analysis ensemble as a whole is not the Kalman analysis for any single covariance. The cross covariance between two grid points is not controlled by Theorem 3, and the localized update is not a Bayes update of any joint prior. The gain in accuracy from localization is a measurement, not a theorem. For a nonlinear $h$ the use of $Y$ in place of $H X$ is the usual linearization of the ensemble methods and is a heuristic.

**Termination.** Lines L1 and L2 are finite loops. The loop of line L3 runs $n$ times. In each pass, line L6 runs the cyclic Jacobi method on a $p_l \times p_l$ matrix, which the code stops after at most a fixed number of sweeps (the method converges quadratically, so the limit is never reached in practice). The other lines are finite sums. So the algorithm returns at line L10. $\blacksquare$
