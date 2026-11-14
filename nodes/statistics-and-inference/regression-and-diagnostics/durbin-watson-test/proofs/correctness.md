---
title: The Durbin-Watson statistic lies in (0, 4), its null law depends only on X and not on b or sigma, and the bounds d_L and d_U bracket it
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is a fixed real $n \times p$ matrix of rank $p < n$ whose columns include the constant $\mathbf 1$, $M = I - X(X^\top X)^{-1}X^\top$, and $e = My \ne 0$. Let $A$ be the $n \times n$ tridiagonal matrix with diagonal $(1, 2, \dots, 2, 1)$ and $-1$ next to the diagonal, so that

$$e^\top Ae = \sum_{t=2}^n(e_t - e_{t-1})^2, \qquad d = \frac{e^\top Ae}{e^\top e}, \qquad r_1 = \frac{\sum_{t=2}^ne_te_{t-1}}{e^\top e}.$$

Lines L2 to L4 compute exactly these sums, and line L1 computes $e = y - Q_1Q_1^\top y$ with $Q_1$ an orthonormal basis of the columns of $X$, which is $My$.

**Lemma 1 (identity and range).** $d = 2(1 - r_1) - (e_1^2 + e_n^2)/e^\top e$, and $0 < d < 4$.

*Proof.* Expanding the squares, $\sum_{t=2}^n(e_t - e_{t-1})^2 = 2e^\top e - e_1^2 - e_n^2 - 2\sum_{t=2}^ne_te_{t-1}$; divide by $e^\top e$. For the upper bound, $(a - b)^2 \le 2a^2 + 2b^2$ gives $e^\top Ae \le 4e^\top e - 2e_1^2 - 2e_n^2 \le 4e^\top e$, with equality only if $e_t = -e_{t-1}$ for all $t$ and $e_1 = e_n = 0$, that is $e = 0$. For the lower bound, $d = 0$ only if all $e_t$ are equal; since $\mathbf 1$ is a column of $X$, $\mathbf 1^\top e = 0$, so they would all be 0. $\square$

**Lemma 2 (the eigenvalues of A).** $A$ has the eigenvalues $\lambda_j = 2 - 2\cos(\pi j/n)$, $j = 0, \dots, n - 1$, with eigenvectors $v^{(j)}_t = \cos(\pi j(t - \frac12)/n)$. In particular $\lambda_0 = 0$ with eigenvector $\mathbf 1$.

*Proof.* Let $\theta = \pi j/n$ and $a_t = \theta(t - \frac12)$. For $2 \le t \le n - 1$, $2v_t - v_{t-1} - v_{t+1} = 2\cos a_t - 2\cos a_t\cos\theta = (2 - 2\cos\theta)v_t$. For $t = 1$, $v_1 - v_2 = \cos\frac\theta2 - \cos\frac{3\theta}2$, and $(2 - 2\cos\theta)\cos\frac\theta2 = 2\cos\frac\theta2 - \cos\frac{3\theta}2 - \cos\frac\theta2$, the same. For $t = n$, $v_n - v_{n-1} = (2 - 2\cos\theta)v_n$ follows in the same way, because $\cos(\pi j + \frac\theta2) = \cos(\pi j - \frac\theta2)$. The $\lambda_j$ are distinct, so these are all the eigenvalues. $\square$

**Lemma 3 (the null law does not depend on b or sigma).** For $a \ne 0$ and $c \in \mathbb R^p$, the statistic of $ay + Xc$ equals that of $y$. Under $H_0$, $y = Xb + \sigma\varepsilon_0$ with $\varepsilon_0 \sim N(0, I_n)$, so

$$d = \frac{\varepsilon_0^\top MAM\varepsilon_0}{\varepsilon_0^\top M\varepsilon_0},$$

whose law depends only on $X$. Hence the Monte Carlo p-value $(1 + \#\{d^* \le d\})/(1 + B)$ of lines L5 to L7, with $d^*$ computed from standard normal vectors, has $P(p \le \alpha) = \alpha$ under $H_0$ whenever $\alpha(B + 1)$ is an integer.

*Proof.* $M(ay + Xc) = aMy = ae$, and $d$ is unchanged when $e$ is multiplied by $a \ne 0$. With $y = Xb + \sigma\varepsilon_0$, $e = \sigma M\varepsilon_0$, and $\sigma$ cancels. The observed $d$ and the $B$ simulated $d^*$ are then independent with the same continuous law, so they are exchangeable and have no ties with probability 1. The rank of $d$ among the $B + 1$ values is uniform on $\{1, \dots, B + 1\}$, and $p \le \alpha$ exactly when that rank is at most $\alpha(B + 1)$. $\square$

**Lemma 4 (the bounds).** Let $\nu_1 \le \dots \le \nu_{n-p}$ be the eigenvalues of $A$ restricted to the orthogonal complement $W$ of the columns of $X$. Then under $H_0$, $d$ has the law of $\sum_i\nu_i\xi_i^2/\sum_i\xi_i^2$ with $\xi_1, \dots, \xi_{n-p}$ independent standard normal, and

$$\lambda_i \le \nu_i \le \lambda_{i+p-1}, \qquad i = 1, \dots, n - p.$$

So with $d_L = \sum_i\lambda_i\xi_i^2/\sum_i\xi_i^2$ and $d_U = \sum_i\lambda_{i+p-1}\xi_i^2/\sum_i\xi_i^2$ built from the same $\xi$, $d_L \le d \le d_U$, and $P(d_U \le c) \le P(d \le c) \le P(d_L \le c)$ for every $c$.

*Proof.* Let $U$ be an $n \times (n - p)$ matrix whose orthonormal columns span $W$ and diagonalize $U^\top AU = \operatorname{diag}(\nu)$. Then $M = UU^\top$, and with $\xi = U^\top\varepsilon_0 \sim N(0, I_{n-p})$, $\varepsilon_0^\top M\varepsilon_0 = \xi^\top\xi$ and $\varepsilon_0^\top MAM\varepsilon_0 = \xi^\top U^\top AU\xi = \sum_i\nu_i\xi_i^2$. Since $\mathbf 1$ is an eigenvector of the symmetric $A$, the space $\mathbf 1^\perp$ is invariant, and $A$ on it has the eigenvalues $\lambda_1 \le \dots \le \lambda_{n-1}$ by Lemma 2. $W$ is a subspace of $\mathbf 1^\perp$ of codimension $p - 1$, so the Cauchy interlacing theorem (a consequence of the Courant-Fischer minimax characterization) gives $\lambda_i \le \nu_i \le \lambda_{i+p-1}$. Each ratio is a weighted mean of its eigenvalues with the same weights $\xi_i^2/\sum\xi^2$, so the order carries over to $d_L \le d \le d_U$, and then to the distribution functions. $\square$

The laws of $d_L$ and $d_U$ depend only on $n$ and $p$, which is why they could be tabulated once; Durbin and Watson (1950, 1951) proved this bounding result.

**What is cited, not proved.** The exact distribution function $P(\sum_i(\nu_i - c)\xi_i^2 \le 0)$ can be computed by the numerical inversion of Imhof (1961); this is not done here. When the errors follow a stationary AR(1) process with coefficient $\rho$ and the design is regular, $r_1 \to \rho$ and $d \to 2(1 - \rho)$ in probability; this is a standard consequence of the ergodic theorem and is not proved here. The size of the Monte Carlo test under non-normal errors, and the power, are measured on the page.

**Termination.** Line L1 is a Householder factorization with $p$ steps and one projection, lines L2 to L4 are three sums, and the loop of lines L5 and L6 runs $B$ times with $\Theta(np)$ work each: $\Theta(np^2 + Bnp)$ operations.
