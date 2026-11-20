---
title: Ensemble Kalman inversion stays in the span of the initial ensemble, and its square root form gives the exact posterior for a linear forward model
proves: [correctness, termination]
status: full
---

**Setting.** The ensemble has $N \ge 2$ members $u_1, \ldots, u_N \in \mathbb R^d$. The data are $y \in \mathbb R^p$, the noise covariance $\Gamma$ is symmetric positive definite and the step size is $h > 0$. One step of line L1 computes $g_i = G(u_i)$ (line L2), the means $\bar u$ and $\bar g$, the unscaled perturbation matrices $U$ ($d \times N$) and $Y$ ($p \times N$), and the sample covariances $C^{ug} = UY^\top/(N - 1)$ and $C^{gg} = YY^\top/(N - 1)$ (line L3). With $S = C^{gg} + \Gamma/h$, line L5 sets

$$u_i \leftarrow u_i + C^{ug}S^{-1}(y_i - g_i),$$

where the target $y_i$ of line L4 is $y$ (mode "none") or $y + \eta_i$ with $\eta_i \sim N(0, \Gamma/h)$ (mode "perturbed"). Mode "sqrt" uses the ETKF weights with the observation error covariance $\Gamma/h$:

$$\tilde P = \bigl((N - 1)I + Y^\top(\Gamma/h)^{-1}Y\bigr)^{-1}, \quad \bar w = \tilde PY^\top(\Gamma/h)^{-1}(y - \bar g), \quad W = \sqrt{N - 1}\,\tilde P^{1/2},$$

and sets $u_i \leftarrow \bar u + U(\bar w + W_i)$, where $W_i$ is column $i$ of $W$. $\mathbf 1$ is the vector of $N$ ones, so $U\mathbf 1 = 0$ and $Y\mathbf 1 = 0$.

**Lemma 1 (subspace property).** In every mode and for every $G$, after any number of steps each member lies in the affine space $\bar u^0 + \operatorname{span} U^0$ of the initial ensemble. In particular it lies in the linear span of the initial members.

*Proof.* In modes "none" and "perturbed", $C^{ug}S^{-1}(y_i - g_i) = U c_i$ with $c_i = Y^\top S^{-1}(y_i - g_i)/(N - 1)$, so a step adds to each member a combination of the current perturbations. In mode "sqrt", the new member $\bar u + U(\bar w + W_i)$ is the current mean plus a combination of the current perturbations. Let $V = \operatorname{span} U^0$. Suppose that all current members lie in $\bar u^0 + V$. Then the current mean lies there, the current perturbations are differences of points of $\bar u^0 + V$ and so lie in $V$, and in all modes the new members lie in $\bar u^0 + V$ again. Induction on the number of steps completes the proof. The point $\bar u^0 = \tfrac1N\sum_j u^0_j$ and $V$ are both in the span of the initial members. $\square$

So the ensemble can never leave a space of dimension at most $N - 1$ around the initial mean, whatever $G$ is.

**Lemma 2 (the square root step is Gaussian conditioning on the sample moments).** Let $G(u) = Au$ be linear, and let $m$ and $P$ be the sample mean and covariance before a step of mode "sqrt". After the step the sample mean and covariance are

$$m + PA^\top(APA^\top + \Gamma/h)^{-1}(y - Am), \qquad P - PA^\top(APA^\top + \Gamma/h)^{-1}AP.$$

*Proof.* This is Lemma 2 of the proof on the page of the [ensemble Kalman smoother](/ensemble-kalman-smoother/), with $s = x = u$, $H = A$ and $R = \Gamma/h$: the weights satisfy $W\mathbf 1 = \mathbf 1$, so the new mean is $\bar u + U\bar w$ and the new perturbations are $UW$, and the Woodbury identity turns $U\tilde PU^\top$ into the right side. $\square$

The right sides are the moments of $u$ given $y$ when $u \sim N(m, P)$ and $y = Au + e$ with $e \sim N(0, \Gamma/h)$. As a function of $u$, the Gaussian density of $N(m, P)$ times $\exp\bigl(-\tfrac h2|\Gamma^{-1/2}(y - Au)|^2\bigr)$ is proportional to the density with these moments.

**Theorem 3 (tempering is exact in mode "sqrt").** Let $G(u) = Au$, let the prior be $N(m_0, P_0)$, and let the initial ensemble have the sample mean $m_0$ and the sample covariance $P_0$ exactly. After $k$ steps of mode "sqrt" with the step $h$, the ensemble has the mean and the covariance of the Gaussian density proportional to

$$\exp\Bigl(-\tfrac12|P_0^{-1/2}(u - m_0)|^2 - \tfrac{kh}{2}|\Gamma^{-1/2}(y - Au)|^2\Bigr).$$

With $kh = 1$ these are the moments of the posterior of the [Bayesian inverse problem](/bayesian-inverse-problem/) $y = Au + e$, $e \sim N(0, \Gamma)$.

*Proof.* By induction on $k$. For $k = 0$ this is the assumption. Suppose that after $k$ steps the sample moments are those of the density $\pi_k$ above, which is Gaussian. By Lemma 2 the next step gives the moments of the Gaussian density proportional to $\pi_k(u)\exp(-\tfrac h2|\Gamma^{-1/2}(y - Au)|^2)$. The exponents add, so this is $\pi_{k + 1}$. $\square$

The data $y$ is the same at every step. The steps do not use $y$ more than once in the Bayesian sense: each step uses the fraction $h$ of the likelihood, and the fractions add up to one when $kh = 1$.

**Proposition 4 (mode "none" underestimates the spread).** Let $G(u) = Au$, let $m$ and $P$ be the sample moments before a step of mode "none", and let $K = PA^\top(APA^\top + \Gamma/h)^{-1}$. The new sample mean is the Kalman mean $m + K(y - Am)$, and the new sample covariance is

$$(I - KA)P(I - KA)^\top = (I - KA)P - K(\Gamma/h)K^\top.$$

*Proof.* Here $g_i = Au_i$, so $Y = AU$, $C^{ug} = PA^\top$, $S = APA^\top + \Gamma/h$ and $C^{ug}S^{-1} = K$. Each member becomes $u_i + K(y - Au_i) = (I - KA)u_i + Ky$. The map is affine and the same for all members, so the mean becomes $(I - KA)m + Ky$ and the covariance $(I - KA)P(I - KA)^\top$. Expand it: $(I - KA)P(I - KA)^\top = (I - KA)P - PA^\top K^\top + KAPA^\top K^\top$. From $KS = PA^\top$ follows $KAPA^\top K^\top = PA^\top K^\top - K(\Gamma/h)K^\top$, which gives the second form. $\square$

$(I - KA)P$ is the Kalman covariance, so mode "none" removes $K(\Gamma/h)K^\top$ more spread than conditioning would at every step. The perturbations of the targets in mode "perturbed" add this term back in expectation, as on the page of the [ensemble Kalman filter](/ensemble-kalman-filter/).

**Remark (small steps).** Since $S^{-1} = h(hC^{gg} + \Gamma)^{-1}$, a step of mode "none" is $u_i \leftarrow u_i + h\,C^{ug}\Gamma^{-1}(y - G(u_i)) + O(h^2)$ for fixed members. For a linear $G = A$ this is an Euler step of $\dot u_i = -C(u)A^\top\Gamma^{-1}(Au_i - y)$, a gradient flow of $\tfrac12|\Gamma^{-1/2}(y - Au)|^2$ with the ensemble covariance $C(u)$ as the preconditioner. Schillings and Stuart (2017) study this limit, and the collapse of the ensemble and the convergence of the misfit for linear $G$. Their results are not proved here.

The check value of the page group: with two members $\mp 1/\sqrt 2$, $G = 1$, $y = 1$, $\Gamma = 1$ and one step of size $h = 1$, mode "sqrt" gives the mean $1/2$ and the variance $1/2$ (Theorem 3), and mode "none" gives the mean $1/2$ and the variance $1 - 1/2 - 1/4 = 1/4$ (Proposition 4).

**What is not proved.** For a nonlinear $G$ the step is a linear regression of $u$ on $G(u)$ over the ensemble, and the result is not the posterior. Mode "perturbed" gives the posterior only as $N \to \infty$ for a linear $G$, and only in distribution; this is not shown here. Convergence of the misfit for a nonlinear $G$ is measured on the page, not proved.

**Termination.** The loop of line L1 runs a fixed number of times. $S = C^{gg} + \Gamma/h$ is the sum of a positive semidefinite and a positive definite matrix, so it is positive definite and the solve of line L5 has a unique solution. In mode "sqrt" the matrix $(N - 1)I + Y^\top(\Gamma/h)^{-1}Y$ has all eigenvalues at least $N - 1 > 0$, and the Jacobi method has a fixed upper limit on its sweeps. The algorithm returns at line L6. $\blacksquare$
