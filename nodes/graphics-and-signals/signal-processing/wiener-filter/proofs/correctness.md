---
title: The Wiener-Hopf solution and the DFT gain are linear minimum mean-square error estimators
proves: [correctness]
status: full
---

All random variables are real with finite second moments. For the FIR filter, let $u[n] = (x[n], x[n-1], \ldots, x[n-M+1])^T$ and let $d[n]$ be the desired signal. Assume that $x$ and $d$ are jointly wide-sense stationary, so $E[x[n]\, x[n-k]] = r_x[k]$ and $E[d[n]\, x[n-k]] = r_{dx}[k]$ do not depend on $n$, and $E[d[n]^2] = \sigma_d^2$. Then $R = E[u[n]\, u[n]^T]$ has entries $r_x[|i - j|]$, which is the matrix of line L1, and $p = E[d[n]\, u[n]]$ is the vector of line L2. Assume that $R$ is positive definite. We work in exact real arithmetic, as in the real RAM.

**Lemma 1 (the error surface).** Let $w^\ast$ be the solution of $R w^\ast = p$ (line L3), and for $w \in \mathbb{R}^M$ let $J(w) = E[(d[n] - w^T u[n])^2]$. Then

$$J(w) = J_{\min} + (w - w^\ast)^T R\, (w - w^\ast), \qquad J_{\min} = \sigma_d^2 - p^T w^\ast.$$

So $w^\ast$ is the unique minimizer of $J$, and the minimum is the value of line L4.

*Proof.* Expand the square and use linearity of expectation: $J(w) = \sigma_d^2 - 2 p^T w + w^T R w$. Substitute $p = R w^\ast$. Because $R$ is symmetric, $w^T R w - 2 w^{\ast T} R w = (w - w^\ast)^T R (w - w^\ast) - w^{\ast T} R w^\ast$, and $w^{\ast T} R w^\ast = p^T w^\ast$. This gives the identity. As $R$ is positive definite, the quadratic term is positive for every $w \ne w^\ast$. $\square$

**Lemma 2 (orthogonality).** The error $e^\ast[n] = d[n] - w^{\ast T} u[n]$ satisfies $E[e^\ast[n]\, u[n]] = 0$; conversely, a vector $w$ whose error is uncorrelated with every entry of $u[n]$ is $w^\ast$.

*Proof.* $E[(d[n] - w^T u[n])\, u[n]] = p - R w$, which is zero if and only if $R w = p$. $\square$

**Theorem 1 (FIR Wiener filter).** WIENER-FIR returns the unique tap vector $w^\ast$ that minimizes the mean-square error among all estimates of $d[n]$ of the form $w^T u[n]$, and $J_{\min} = J(w^\ast) \ge 0$. For $n \ge M - 1$, line L6 outputs $\hat d[n] = w^{\ast T} u[n]$, whose mean-square error is $J_{\min}$. If in addition $(d[n], u[n])$ is jointly Gaussian with zero mean, then $\hat d[n] = E[d[n] \mid u[n]]$, so no estimator, linear or not, has a smaller mean-square error.

*Proof.* The first two statements are Lemma 1; $J_{\min} = J(w^\ast)$ is an expected square, so it is not negative. For $n \ge M - 1$, all the samples $x[n-k]$ for $k = 0, \ldots, M-1$ have index at least $0$, so line L6 does not use the zero padding and computes $w^{\ast T} u[n]$; its error is $J(w^\ast)$ by stationarity. In the Gaussian case, $e^\ast[n]$ and $u[n]$ are jointly Gaussian, as linear functions of a Gaussian vector, and uncorrelated by Lemma 2, so they are independent. Then $E[d[n] \mid u[n]] = w^{\ast T} u[n] + E[e^\ast[n] \mid u[n]] = w^{\ast T} u[n] + E[e^\ast[n]] = w^{\ast T} u[n]$, because $E[e^\ast[n]] = E[d[n]] - w^{\ast T} E[u[n]] = 0$. The conditional expectation minimizes the mean-square error over all measurable functions of $u[n]$. $\square$

**Vector form.** Lemma 1 applies to each entry of a vector. Let $x \in \mathbb{R}^N$ and $y \in \mathbb{R}^N$ have zero mean, with $C_y = E[y y^T]$ positive definite and $C_{xy} = E[x y^T]$. Among all matrices $K$, the sum $E\|x - K y\|^2 = \sum_i E[(x_i - k_i^T y)^2]$, where $k_i^T$ is row $i$ of $K$, is minimized row by row, with $C_y k_i = E[x_i\, y]$. So the unique minimizer is $K^\ast = C_{xy} C_y^{-1}$.

**Theorem 2 (the DFT form).** Let $y = x + v$ on one block of length $N$, where $x$ and $v$ are uncorrelated with zero mean and circulant covariances: $E[x_i x_j] = c_x[(i - j) \bmod N]$ and $E[v_i v_j] = c_v[(i-j) \bmod N]$. Let $S_x$ and $S_n$ be the DFTs of $c_x$ and $c_v$, and assume $S_x[m] + S_n[m] > 0$ for every bin $m$. Then lines L7 to L9 return $K^\ast y$, the linear MMSE estimate of $x$ from $y$, and the mean-square error per sample is $\frac{1}{N} \sum_m \frac{S_x[m]\, S_n[m]}{S_x[m] + S_n[m]}$.

*Proof.* Let $\Phi$ be the DFT matrix, $\Phi_{mk} = e^{-2\pi i m k / N}$, so $\Phi^{-1} = \frac{1}{N} \Phi^H$. A circulant matrix $C$ with first column $c$ satisfies $C = \Phi^{-1} \operatorname{diag}(\Phi c)\, \Phi$, because the vector $f_m = (e^{2\pi i m k/N})_k$ is an eigenvector of every circulant matrix: $(C f_m)_j = \sum_k c[(j-k) \bmod N]\, e^{2\pi i m k / N} = e^{2\pi i m j/N} \sum_l c[l]\, e^{-2\pi i m l / N}$, after the change of index $l = (j - k) \bmod N$. So $C_x = \Phi^{-1} D_x \Phi$ and $C_v = \Phi^{-1} D_n \Phi$, with $D_x = \operatorname{diag}(S_x)$ and $D_n = \operatorname{diag}(S_n)$. As $x$ and $v$ are uncorrelated, $C_{xy} = E[x (x + v)^T] = C_x$ and $C_y = C_x + C_v = \Phi^{-1} (D_x + D_n) \Phi$, which is invertible by the assumption on the bins. Then

$$K^\ast = C_x C_y^{-1} = \Phi^{-1} D_x \Phi\, \Phi^{-1} (D_x + D_n)^{-1} \Phi = \Phi^{-1} \operatorname{diag}(H)\, \Phi,$$

with $H[m] = S_x[m] / (S_x[m] + S_n[m])$, the gain of line L7. So $K^\ast y = \Phi^{-1}(H \cdot \Phi y)$, where $\cdot$ is the product bin by bin: $\Phi y$ is the DFT $Y$, line L8 forms $H \cdot Y$, and $\Phi^{-1}$ is the inverse DFT with the factor $1/N$. The vector $K^\ast y$ is real, because $K^\ast = C_x C_y^{-1}$ is a real matrix, so taking the real part in line L9 does not change it. The error covariance is $C_x - K^\ast C_{xy}^T = \Phi^{-1} (D_x - H D_x) \Phi$, whose trace is the sum of its eigenvalues, $\sum_m S_x[m] (1 - H[m]) = \sum_m S_x[m] S_n[m] / (S_x[m] + S_n[m])$; divide by $N$ for the error per sample. $\blacksquare$

**Remarks.** If $S_x[m] = S_n[m] = 0$ in some bin, then $E|Y[m]|^2 = N\,(S_x[m] + S_n[m]) = 0$ and $E|X[m]|^2 = N\, S_x[m] = 0$, so both DFT coefficients are zero almost surely and every gain gives the same estimate; line L7 uses $0$. The covariance $c_x$ is real and even, $c_x[k] = c_x[-k \bmod N]$, so $S_x$ is real and even in $m$, and so is $H$. A stationary process restricted to a block has a Toeplitz covariance, not a circulant one; Theorem 2 is exact for periodic signals and an approximation for others, with an error that comes from the ends of the block.
