---
title: Optimal interpolation is the best linear unbiased analysis for its data selection
proves: [correctness, termination]
status: full
---

**Setting.** The state has $n$ components and there are $p$ observations. The background is $x^b = x^t + \varepsilon^b$ and the observations are $y^o = H x^t + \varepsilon^o$, with a linear $p \times n$ matrix $H$. The errors have zero mean, $\mathrm{cov}(\varepsilon^b) = B$, $\mathrm{cov}(\varepsilon^o) = R$ and $\mathrm{cov}(\varepsilon^b, \varepsilon^o) = 0$. $B$ is symmetric positive semidefinite and $R$ is symmetric positive definite. Write $A = H B H^\top + R$ and $d = y^o - H x^b$ (line L1). For a grid point $i$ and a selection $S = S_i$ (line L3), $A_S$ is the submatrix of line L4 and $c = (H B)_{S,i}$ is the vector of line L5.

**Lemma 1 (the systems are solvable).** $A$ is symmetric positive definite, and so is every principal submatrix $A_S$ with $S$ not empty.

*Proof.* For $z \ne 0$, $z^\top A z = (H^\top z)^\top B (H^\top z) + z^\top R z \ge z^\top R z > 0$. For a principal submatrix, take $z$ zero outside $S$. $\square$

**Termination.** Line L2 runs over the $n$ grid points once. Each pass does a finite amount of work: the selection of line L3, the copies of lines L4 and L5, and one linear solve of size $|S|$ in line L6, which succeeds by Lemma 1. So the algorithm stops after $n$ passes and returns at line L9.

**Lemma 2 (error of a linear update).** For any weight vector $w \in \mathbb R^{|S|}$, the estimate $\hat x_i = x^b_i + w^\top d_S$ has the error $\hat x_i - x^t_i = \varepsilon^b_i + w^\top(\varepsilon^o - H\varepsilon^b)_S$, which has zero mean and the variance

$$V(w) = B_{ii} - 2 w^\top c + w^\top A_S w.$$

*Proof.* $d = H x^t + \varepsilon^o - H(x^t + \varepsilon^b) = \varepsilon^o - H\varepsilon^b$, which gives the error formula and the zero mean. Expand the variance: $\mathrm{var}(\varepsilon^b_i) = B_{ii}$, $\mathrm{cov}(\varepsilon^b_i, (\varepsilon^o - H\varepsilon^b)_S) = -(HB)_{S,i} = -c$ because $\varepsilon^b$ and $\varepsilon^o$ are uncorrelated, and $\mathrm{cov}((\varepsilon^o - H\varepsilon^b)_S) = (R + H B H^\top)_{SS} = A_S$. $\square$

**Theorem 3 (optimality for the selection).** Among all estimates $x^b_i + w^\top d_S$, the weights of line L6, $A_S w = c$, give the unique smallest error variance. The value of line L8, $B_{ii} - w^\top c$, is that smallest variance.

*Proof.* $V$ is a quadratic function of $w$ with the Hessian $2A_S$, which is positive definite by Lemma 1. So $V$ has exactly one minimizer, where the gradient $2A_S w - 2c$ is zero. At that point $w^\top A_S w = w^\top c$, so $V(w) = B_{ii} - w^\top c$. Line L7 forms the estimate with this $w$. $\square$

**Corollary 4 (more observations never hurt).** If $S \subseteq S'$, the variance of line L8 for $S'$ is at most the variance for $S$. Both are at most $B_{ii}$, the value for $S$ empty.

*Proof.* An estimate that uses $S$ is an estimate that uses $S'$ with zero weights on $S' \setminus S$, so the minimum over the larger set is not larger. $\square$

An observation outside $S_i$ does not enter lines L4 to L8 for point $i$, so a change in its value does not change $x^a_i$.

**Theorem 5 (global selection is the Kalman update).** If $S_i$ is the set of all observations for every $i$, the output is $x^a = x^b + K d$ with $K = B H^\top A^{-1}$, and the variances are the diagonal of $P^a = (I - K H) B$. If $B$ is also positive definite, then

$$x^a = P\,(B^{-1} x^b + H^\top R^{-1} y^o), \qquad P^a = P, \qquad P = (B^{-1} + H^\top R^{-1} H)^{-1}.$$

*Proof.* With $S$ = all, line L6 gives $w = A^{-1}(HB)_{:,i}$, so $w^\top = (B H^\top A^{-1})_{i,:} = K_{i,:}$ because $A$ and $B$ are symmetric. Line L7 is row $i$ of $x^b + K d$ and line L8 is $B_{ii} - (K H B)_{ii}$.

For the second form, $(B^{-1} + H^\top R^{-1} H) B H^\top = H^\top + H^\top R^{-1} H B H^\top = H^\top R^{-1}(R + H B H^\top) = H^\top R^{-1} A$. Multiply by $P$ on the left and by $A^{-1}$ on the right: $K = P H^\top R^{-1}$. Then $P^{-1}(I - K H) B = P^{-1} B - H^\top R^{-1} H B = I$, so $(I - KH)B = P$. Finally $x^a = x^b + P H^\top R^{-1}(y^o - H x^b)$, and $P^{-1}x^b - H^\top R^{-1} H x^b = B^{-1} x^b$ gives the stated form. $\square$

The second form is the minimizer of the 3D-Var cost $J(x) = \tfrac12 (x - x^b)^\top B^{-1}(x - x^b) + \tfrac12 (y^o - Hx)^\top R^{-1}(y^o - Hx)$, whose gradient $B^{-1}(x - x^b) - H^\top R^{-1}(y^o - Hx)$ is zero exactly there. So global OI, the Kalman update and 3D-Var give the same analysis for a linear $H$. If the errors are also Gaussian, $x^a$ is the mean of the posterior distribution of $x^t$ and $P^a$ is its covariance.

**Summary.** The algorithm stops after $n$ solves of positive definite systems. For each grid point it returns the linear unbiased estimate of smallest error variance among those that use the selected observations, together with that variance. With all observations selected, it returns the Kalman analysis $x^b + K d$ and the diagonal of $(I - KH)B$. $\blacksquare$
