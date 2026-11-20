---
title: The square root EnKS is the ETKF of the state over the lag window, and is exact for linear models without model noise
proves: [correctness, termination]
status: full
---

**Setting.** The ensemble has $N \ge 2$ members. For an ensemble $s_1, \ldots, s_N$ of any vector, $\bar s$ is its mean and $S$ the matrix of its unscaled perturbations (column $i$ is $s_i - \bar s$). At an observation time $t$ the forecast members $x_i$ give the predicted observations $y_i = H(x_i)$ with perturbations $Y$ ($p \times N$) and the innovation $d = y^o_t - \bar y$. The weights of line L5 are those of the ETKF:

$$\tilde P = \bigl((N - 1)I + Y^\top R^{-1} Y\bigr)^{-1}, \qquad \bar w = \tilde P Y^\top R^{-1} d, \qquad W = \sqrt{N - 1}\,\tilde P^{1/2},$$

and line L6 replaces each stored ensemble by $s^a_i = \bar s + S(\bar w + W_i)$, where $W_i$ is column $i$ of $W$. There is no inflation ($\rho = 1$) in the lemmas.

**Lemma 1 (the smoother is an ETKF of the stacked state).** Let $z_i$ stack the members of all stored ensembles of the window with the current member $x_i$, and let $H_z(z) = H(x)$. One analysis of lines L4 to L6 gives the same members as the ETKF analysis of the ensemble $z_i$ with the operator $H_z$.

*Proof.* The ETKF of $z$ computes its weights from the predicted observations $H_z(z_i) = H(x_i)$ and from $R$ and $y^o_t$ only, so they are the weights $\bar w$ and $W$ of line L5. It then sets $z^a_i = \bar z + Z(\bar w + W_i)$. The mean and the perturbations of a stacked ensemble are the stacked means and perturbations, so this formula acts on each block of $z$ separately, which is line L6. $\square$

**Lemma 2 (one analysis is Gaussian conditioning on the sample moments).** Suppose $H$ is linear. Let $C_{ss} = SS^\top/(N - 1)$, $C_{sx} = SX^\top/(N - 1)$ and $P = XX^\top/(N - 1)$. Then line L6 gives a stored ensemble the mean and the sample covariance

$$\bar s + C_{sx}H^\top(HPH^\top + R)^{-1} d, \qquad C_{ss} - C_{sx}H^\top(HPH^\top + R)^{-1} H C_{sx}^\top,$$

and the same formulas with the stacked state give the joint sample covariance of all blocks.

*Proof.* Here $Y = HX$. Multiply out to get $((N - 1)I + Y^\top R^{-1}Y)\,Y^\top = Y^\top R^{-1}(YY^\top + (N - 1)R)$, so $\tilde P Y^\top R^{-1} = Y^\top (YY^\top + (N - 1)R)^{-1}$. So $S\bar w = SY^\top(YY^\top + (N - 1)R)^{-1}d = C_{sx}H^\top(HPH^\top + R)^{-1}d$. The columns of $W$ sum to $\sqrt{N - 1}\,\tilde P^{1/2}\mathbf 1$, and $\tilde P^{-1}\mathbf 1 = (N - 1)\mathbf 1$ because $Y\mathbf 1 = 0$, so $W\mathbf 1 = \mathbf 1$. Hence the new perturbations are $SW - \tfrac1N SW\mathbf 1\mathbf 1^\top = SW$ (since $S\mathbf 1 = 0$), and the new mean is $\bar s + S\bar w$. The new sample covariance is $SWW^\top S^\top/(N - 1) = S\tilde P S^\top$. By the Woodbury identity $\tilde P = \tfrac{1}{N - 1}\bigl(I - Y^\top(YY^\top + (N - 1)R)^{-1}Y\bigr)$, so $S\tilde PS^\top = C_{ss} - C_{sx}H^\top(HPH^\top + R)^{-1}HC_{sx}^\top$. For two blocks $s$ and $u$ the same steps give the cross covariance $S\tilde P U^\top$. $\square$

These are the formulas for the mean and the covariance of a Gaussian vector after conditioning on a linear observation of a part of it. This is the step that Evensen and van Leeuwen (2000) use with the ensemble cross covariances in time.

**Theorem 3 (exact for linear models without model noise).** Let the model be $x_{t+1} = Ax_t$ with no model noise, let $H$ be linear, $y^o_t = Hx_t + e_t$ with independent $e_t \sim N(0, R)$, and let $x_0 \sim N(m_0, P_0)$. If the initial ensemble has the sample mean $m_0$ and the sample covariance $P_0$ exactly, then for every $s \le T$ the smoothed ensemble of time $s$ has the mean and the covariance of $x_s$ given $y^o_1, \ldots, y^o_{\min(s + L, T)}$, and the filtered ensemble of time $s$ has those of $x_s$ given $y^o_1, \ldots, y^o_s$.

*Proof.* By induction on $t$ we show: after time $t$, the stacked ensemble of the times in the window and time $t$ has the sample mean and the joint sample covariance of these states given $y^o_1, \ldots, y^o_t$, and every time that has left the window has the moments given the data up to the time when it left. For $t = 0$ this is the assumption. At time $t + 1$, line L2 sets $x_i \leftarrow Ax_i$ for each member. The stacked members are then a fixed linear map of the old ones, and $x_{t+1} = Ax_t$ is the same map of the true states, so the sample moments are still the exact moments given $y^o_1, \ldots, y^o_t$. If there is an observation, $y^o_{t+1} = Hx_{t+1} + e_{t+1}$ with $e_{t+1}$ independent of the earlier data and of the states, and the conditional distribution given the earlier data is Gaussian. So conditioning on $y^o_{t+1}$ changes the moments by the formulas of Lemma 2, which line L6 applies to every block. Line L7 removes the times $s$ with $s + L = t + 1$ or less, so a time $s$ leaves the window after it has used the data up to time $s + L$. The filtered ensemble of time $s$ is stored right after the analysis at time $s$. $\square$

With $L \ge T$ the smoothed moments are those of the fixed interval smoother. For a linear Gaussian model the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) computes the same moments (with $Q = 0$).

**Corollary 4 (the members keep the model relation).** In the setting of Theorem 3, and also for any linear model applied member by member, if two times $s < u$ are both in the window, then $u_i = A^{u - s}s_i$ holds for every member and stays true after each analysis, because line L6 applies the same weights to both ensembles and $A^{u - s}(\bar s + S c) = \bar u + U c$.

The check value of the page group: with two members $\mp 1/\sqrt 2$, the model $x_1 = x_0$, $H = 1$, $R = 1$, $y^o_1 = 1$ and $L = 1$, the smoothed ensemble of time $0$ and the filtered ensemble of time $1$ both have the mean $1/2$ and the variance $1/2$, while the filtered ensemble of time $0$ keeps the mean $0$ and the variance $1$.

**What is not proved.** With model noise, the members must be perturbed in the forecast, and then the result is exact only in expectation or as $N \to \infty$; this is not shown here. For a nonlinear model or a nonlinear $H$ the update is a linear regression on the ensemble and is a heuristic. With inflation, the forecast moments of time $t$ are changed by $\rho$, but the stored ensembles are not, so their cross covariances with the forecast no longer match the joint moments; inflation is also a heuristic.

**Termination.** The loop of line L1 runs $T$ times. The window holds at most $L + 1$ ensembles. The matrix $(N - 1)I + Y^\top R^{-1}Y$ has all eigenvalues at least $N - 1 > 0$, so the weights exist. The Jacobi method has a fixed upper limit on its sweeps, and the solve with $R$ needs $R$ positive definite. The algorithm returns at line L8. $\blacksquare$
