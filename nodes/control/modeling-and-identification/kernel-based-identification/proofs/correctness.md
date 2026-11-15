---
title: The kernel-based FIR estimate is the posterior mean at the grid point of largest marginal likelihood
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM. The data are $u_0, \ldots, u_{N-1}$ and $y_0, \ldots, y_{N-1}$, the FIR length is $d < N$, and $\Phi$ is the $N \times d$ regressor of L1 with $\Phi_{k,t} = u_{k-t}$ ($0$ for $k < t$). Write $R = \Phi^T \Phi$ and $r = \Phi^T y$ (L2).

**The Bayesian model.** $g \sim \mathcal{N}(0, K)$ with $K$ positive definite, and $y = \Phi g + e$ with $e \sim \mathcal{N}(0, \sigma^2 I_N)$ independent of $g$ and $\sigma^2 > 0$. Then $y \sim \mathcal{N}(0, Z)$ with $Z = \Phi K \Phi^T + \sigma^2 I_N$.

**Lemma 1 (the TC kernel is positive definite).** For $c > 0$ and $0 < \lambda < 1$, the matrix $K_{ij} = c \lambda^{\max(i, j)}$, $i, j = 1, \ldots, d$, is positive definite.

*Proof.* Let $\mathbf{1}_t \in \mathbb{R}^d$ have entries 1 at the indices $i \le t$ and 0 elsewhere. For $i, j \le d$,

$$\lambda^{\max(i, j)} = \sum_{t = \max(i, j)}^{d-1} (\lambda^t - \lambda^{t+1}) + \lambda^d,$$

so $K = c \sum_{t=1}^{d-1} (\lambda^t - \lambda^{t+1}) \mathbf{1}_t \mathbf{1}_t^T + c \lambda^d \mathbf{1}_d \mathbf{1}_d^T$. All weights are positive. If $v^T K v = 0$, then $\mathbf{1}_t^T v = 0$ for $t = 1, \ldots, d$, so $v_1 = 0$, then $v_2 = 0$, and so on: $v = 0$. $\square$

The DC kernel $c \lambda^{(i+j)/2} \rho^{|i-j|}$ with $|\rho| < 1$ is $c$ times $\operatorname{diag}(\lambda^{i/2})$ times the correlation matrix of a first order autoregressive process times the same diagonal, so it is also positive definite. With $\rho = \sqrt{\lambda}$ it equals the TC kernel, since $\lambda^{(i+j)/2} \lambda^{|i-j|/2} = \lambda^{\max(i,j)}$.

**Lemma 2 (posterior mean and regularized least squares).** The posterior mean of $g$ given $y$ is

$$\hat g = K \Phi^T Z^{-1} y = (R + \sigma^2 K^{-1})^{-1} r,$$

and it is the unique minimizer of $\lVert y - \Phi g \rVert^2 + \sigma^2 g^T K^{-1} g$.

*Proof.* $(g, y)$ is jointly Gaussian with $\operatorname{Cov}(g, y) = K \Phi^T$ and $\operatorname{Cov}(y) = Z$, so $\mathbb{E}[g \mid y] = K \Phi^T Z^{-1} y$. The push-through identity $\Phi^T (\Phi K \Phi^T + \sigma^2 I) = (\Phi^T \Phi K + \sigma^2 I) \Phi^T$ gives $K \Phi^T Z^{-1} = K (R K + \sigma^2 I)^{-1} \Phi^T = (R + \sigma^2 K^{-1})^{-1} \Phi^T$. The criterion is a quadratic with Hessian $2(R + \sigma^2 K^{-1})$, which is positive definite, and its gradient vanishes at $(R + \sigma^2 K^{-1}) g = r$. $\square$

**Lemma 3 (small forms).** Let $K = L L^T$ be the Cholesky factorization and $M = \sigma^2 I_d + L^T R L$. Then

$$\hat g = L M^{-1} L^T r, \qquad y^T Z^{-1} y = \frac{y^T y - r^T L M^{-1} L^T r}{\sigma^2}, \qquad \log \det Z = (N - d) \log \sigma^2 + \log \det M.$$

*Proof.* Put $X = \Phi L$, so $Z = X X^T + \sigma^2 I_N$ and $M = X^T X + \sigma^2 I_d$. The push-through identity gives $X^T Z^{-1} = M^{-1} X^T$, so $\hat g = K \Phi^T Z^{-1} y = L X^T Z^{-1} y = L M^{-1} X^T y = L M^{-1} L^T r$. The Woodbury identity gives $Z^{-1} = \sigma^{-2} (I_N - X M^{-1} X^T)$, which gives the second formula. Sylvester's determinant identity $\det(I_N + X X^T / \sigma^2) = \det(I_d + X^T X / \sigma^2)$ gives $\det Z = \sigma^{2N} \det(I_d + X^T X / \sigma^2) = \sigma^{2N} \sigma^{-2d} \det M$. $\square$

**Lemma 4 (the cost is the marginal likelihood).** The cost of L6 is $y^T Z^{-1} y + \log \det Z = -2 \log p(y \mid \eta) - N \log(2 \pi)$, where $p(y \mid \eta)$ is the Gaussian density of $y$ under the kernel with hyperparameters $\eta$.

*Proof.* $p(y \mid \eta) = (2 \pi)^{-N/2} (\det Z)^{-1/2} \exp(-\tfrac12 y^T Z^{-1} y)$. Take $-2 \log$. By Lemma 3, the code computes exactly these two terms from $R$, $r$ and $y^T y$. $\square$

**Lemma 5 (the noise variance of L3).** If $R$ is nonsingular and the data follow the FIR model with $d$ taps, then $\hat\sigma^2 = \lVert y - \Phi g_{LS} \rVert^2 / (N - d)$ with $g_{LS} = R^{-1} r$ has expectation $\sigma^2$, given $u$.

*Proof.* The residual is $(I - P) e$ with $P = \Phi R^{-1} \Phi^T$, an orthogonal projection of rank $d$. So $\mathbb{E} \lVert (I - P) e \rVert^2 = \sigma^2 \operatorname{tr}(I - P) = \sigma^2 (N - d)$. The code computes $\lVert y - \Phi g_{LS} \rVert^2 = y^T y - 2 g_{LS}^T r + g_{LS}^T R g_{LS}$. $\square$

**Theorem.** KERNEL-FIR returns $\hat\sigma^2$ (or the given $\sigma^2$), the first grid point $\eta^*$ that minimizes $-2 \log p(y \mid \eta)$ over the grid, and the posterior mean of $g$ under the kernel $K(\eta^*)$, which is also the regularized least squares estimate of Lemma 2.

*Proof.* L4 to L7 scan the grid and keep a point only when its cost is strictly smaller, so the kept point is the first minimizer of the cost, which by Lemma 4 is the first maximizer of the marginal likelihood. L8 computes $L M^{-1} L^T r$ for this kernel, which by Lemmas 2 and 3 is the posterior mean. $\blacksquare$

**Remark.** The theorem is about the optimization over the grid only. The marginal likelihood is not convex in the hyperparameters, and a continuous search can stop at a local minimum. Whether the empirical Bayes choice gives a small error $\lVert \hat g - g_0 \rVert$ is a statistical question; the page reports measurements and cites the theory.
