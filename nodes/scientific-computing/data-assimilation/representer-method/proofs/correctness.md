---
title: The representer expansion gives the exact minimizer of the linear weak-constraint cost
proves: [correctness, termination]
status: full
---

**Setting.** The window has the time levels $0, \ldots, K$, and the model is linear, $x_k = M_k x_{k-1} + \eta_k$. Write $M_{k \leftarrow j} = M_k M_{k-1} \cdots M_{j+1}$ for $j \le k$, with $M_{k \leftarrow k} = I$, and $C_0 = B$, $C_j = Q_j$ for $j \ge 1$. There are $p$ scalar observations $y_i = h_i^\top x_{k_i} + \epsilon_i$, with $\epsilon \sim N(0, R)$, and $R$, $B$ and all $Q_j$ are symmetric positive definite. The cost is

$$J(x_0, \eta) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{j=1}^K \tfrac12 \eta_j^\top Q_j^{-1}\eta_j + \tfrac12 (y - \mathcal H x)^\top R^{-1}(y - \mathcal H x),$$

where $(\mathcal H x)_i = h_i^\top x_{k_i}$. Give the control the prior $x_0 \sim N(x^b, B)$ and $\eta_j \sim N(0, Q_j)$, all independent. Then $x_k = M_{k \leftarrow 0} x_0 + \sum_{j=1}^k M_{k \leftarrow j}\eta_j$, so

$$E[x_k] = M_{k \leftarrow 0} x^b = x^f_k, \qquad \mathrm{Cov}(x_k, x_l) = \sum_{j=0}^{\min(k, l)} M_{k \leftarrow j} C_j M_{l \leftarrow j}^\top .$$

$x^f$ is the first guess of line L1.

**Lemma 1 (a representer is a covariance).** Lines L3 and L4 for observation $i$ compute $r_i(k) = \mathrm{Cov}(x_k, x_{k_i})\, h_i$ for every $k$.

*Proof.* The backward sweep of line L3 starts from zero, adds $h_i$ at time $k_i$ and applies $M_j^\top$ from time $j$ to time $j - 1$. So $\lambda_j = M_{k_i \leftarrow j}^\top h_i$ for $j \le k_i$ and $\lambda_j = 0$ for $j > k_i$. The forward sweep of line L4 starts from $r(0) = B\lambda_0$ and sets $r(k) = M_k r(k-1) + Q_k\lambda_k$, so $r(k) = \sum_{j=0}^{k} M_{k \leftarrow j} C_j \lambda_j$. Only the terms with $j \le k_i$ are not zero, which gives $\sum_{j=0}^{\min(k, k_i)} M_{k \leftarrow j} C_j M_{k_i \leftarrow j}^\top h_i = \mathrm{Cov}(x_k, x_{k_i}) h_i$. $\square$

**Corollary 2.** Line L5 gives $P_{ji} = h_j^\top r_i(k_j) = \mathrm{Cov}(h_j^\top x_{k_j}, h_i^\top x_{k_i})$, so $P = \mathrm{Cov}(\mathcal H x)$. It is symmetric positive semidefinite, and $P + R$ is positive definite, so line L7 has a unique solution.

**Lemma 3 (the combined sweep).** Lines L8 and L9 compute $\hat x_k = x^f_k + \sum_i \beta_i r_i(k)$.

*Proof.* The backward sweep is linear in the forcing, so the forcing $\sum_i \beta_i h_i$ at the times $k_i$ gives $\lambda = \sum_i \beta_i \lambda^{(i)}$. The forward sweep from $x^b$ is the forward sweep from $0$ plus the model run from $x^b$, which is $x^f$, and the forward sweep from $0$ is linear in $\lambda$, which gives $\sum_i \beta_i r_i$. $\square$

**Theorem 4.** The trajectory $\hat x$ returned by line L10 is the trajectory of the unique minimizer of $J$, and $\hat x_k = E[x_k \mid y]$ for every $k$.

*Proof.* The map from the control $z = (x_0, \eta_1, \ldots, \eta_K)$ to the trajectory is linear and invertible, and the prior density of $z$ times the likelihood of $y$ is proportional to $e^{-J(z)}$. $J$ is a strictly convex quadratic, so the posterior of $z$ is Gaussian, its mean is the unique minimizer of $J$, and the trajectory of the minimizer is $E[x \mid y]$. For jointly Gaussian $x$ and $y = \mathcal H x + \epsilon$, with $\epsilon$ independent of $x$,

$$E[x_k \mid y] = E[x_k] + \mathrm{Cov}(x_k, y)\,\mathrm{Cov}(y)^{-1}(y - E[y]) .$$

Here $E[y] = \mathcal H x^f$, so $y - E[y] = d$ of line L6; $\mathrm{Cov}(y) = P + R$ by Corollary 2; and column $i$ of $\mathrm{Cov}(x_k, y)$ is $\mathrm{Cov}(x_k, x_{k_i}) h_i = r_i(k)$ by Lemma 1. So $E[x_k \mid y] = x^f_k + \sum_i r_i(k) \beta_i$ with $(P + R)\beta = d$, which is $\hat x_k$ by Lemma 3. $\square$

**Remark (the Euler-Lagrange form).** At the minimizer, $\beta = R^{-1}(y - \mathcal H\hat x)$, $\hat x_0 = x^b + B\lambda_0$ and $\hat\eta_k = Q_k\lambda_k$, where $\lambda$ is the adjoint of the weighted residuals. This is the form in which Bennett (2002) derives the method, and it follows from Theorem 4: $y - \mathcal H\hat x = d - P\beta = R\beta$.

**Termination.** The algorithm runs $p + 1$ backward sweeps and $p + 1$ forward sweeps of $K$ steps, plus the first guess, and one dense solve of size $p$. It always stops.

**Summary.** Each representer is the prior covariance of the trajectory with one observed quantity, the representer matrix is the prior covariance of the observations, and the representer expansion with the coefficients from $(P + R)\beta = d$ is the Gaussian conditional mean, which is the minimizer of the weak-constraint cost. The tests check this with exact rational arithmetic against a direct conditioning of the stacked trajectory, and in floating point against a Kalman filter and smoother with model error. $\blacksquare$
