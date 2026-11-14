---
title: The leave-one-out identity, and what PSIS-LOO computes
proves: [correctness]
status: full
---

We use the pseudocode of the page. The model has $p(y \mid \theta) = \prod_i p(y_i \mid \theta)$, a prior $p(\theta)$, and posterior $p(\theta \mid y) \propto p(\theta) p(y \mid \theta)$. Write $y_{-i}$ for the data without point $i$.

**Claim 1 (the identity).** Assume $p(y_i \mid \theta) > 0$ for every $\theta$ in the support of $p(\theta \mid y_{-i})$. Then

$$\mathbb{E}\Big[\frac{1}{p(y_i \mid \theta)} \,\Big|\, y\Big] = \frac{1}{p(y_i \mid y_{-i})}.$$

*Proof.* Conditional independence gives $p(y \mid \theta) = p(y_i \mid \theta)\, p(y_{-i} \mid \theta)$. By Bayes's theorem applied twice,

$$p(\theta \mid y) = \frac{p(\theta)\, p(y_{-i} \mid \theta)\, p(y_i \mid \theta)}{p(y)} = \frac{p(\theta \mid y_{-i})\, p(y_i \mid \theta)}{p(y_i \mid y_{-i})},$$

because $p(\theta)p(y_{-i} \mid \theta) = p(\theta \mid y_{-i}) p(y_{-i})$ and $p(y)/p(y_{-i}) = p(y_i \mid y_{-i})$. Multiply by $1/p(y_i \mid \theta)$ and integrate over $\theta$:

$$\int \frac{p(\theta \mid y)}{p(y_i \mid \theta)}\, d\theta = \frac{1}{p(y_i \mid y_{-i})} \int p(\theta \mid y_{-i})\, d\theta = \frac{1}{p(y_i \mid y_{-i})}.$$

The positivity assumption makes the division valid on the support of $p(\theta \mid y_{-i})$, and $p(\theta \mid y)$ is zero wherever $p(y_i \mid \theta) = 0$. $\square$

The same computation with a function $g$ gives the importance sampling identity

$$\mathbb{E}[g(\theta) \mid y_{-i}] = \frac{\mathbb{E}[g(\theta)\, r_i(\theta) \mid y]}{\mathbb{E}[r_i(\theta) \mid y]}, \qquad r_i(\theta) = \frac{1}{p(y_i \mid \theta)},$$

so $r_i$ is the importance ratio from the proposal $p(\theta \mid y)$ to the target $p(\theta \mid y_{-i})$, up to a constant.

**Claim 2 (raw importance sampling is consistent).** Let $\theta^1, \theta^2, \ldots$ be independent draws from $p(\theta \mid y)$. Then $S / \sum_{s=1}^S r_i(\theta^s) \to p(y_i \mid y_{-i})$ almost surely.

*Proof.* By Claim 1, $\mathbb{E}[r_i(\theta) \mid y] = 1/p(y_i \mid y_{-i})$, which is finite and positive. The strong law of large numbers gives $\frac1S \sum_s r_i(\theta^s) \to 1/p(y_i \mid y_{-i})$ almost surely, and $x \mapsto 1/x$ is continuous at a positive limit. $\square$

With raw weights $\tilde w_s = r_i(\theta^s)$, line L8 computes $\log \sum_s r_i(\theta^s) p(y_i \mid \theta^s) - \log \sum_s r_i(\theta^s) = \log S - \log \sum_s r_i(\theta^s)$, which is this estimate. For an ergodic Markov chain the ergodic theorem replaces the law of large numbers. Claim 2 says nothing about the variance: $\mathbb{E}[r_i^2 \mid y]$ can be infinite, and then the central limit theorem fails and the error decreases more slowly than $1/\sqrt S$. This is the reason for the smoothing.

**Claim 3 (the code is Algorithm 1).** Line L1 computes $M = \lfloor \min(0.2 S, 3\sqrt S) \rfloor$. Line L3 computes $\rho_s = \log r_i(\theta^s) - \max_t \log r_i(\theta^t)$, so $\exp(\rho_s) = r_i(\theta^s)/\max_t r_i(\theta^t)$; a common factor cancels in L8. Line L4 sorts and sets $u$ to the ratio of rank $S - M$, so the $M$ draws of ranks $S - M + 1, \ldots, S$ form the tail and $\exp(\rho) - u \ge 0$ on the tail. Line L5 fits the generalized Pareto law to these exceedances. Line L6 gives the draw of rank $S - M + z$ the weight $\min(u + F^{-1}((z - 1/2)/M), 1)$, and $1$ is the largest raw ratio after the shift. Line L9 uses the threshold $\min(1 - 1/\log_{10} S, 0.7)$. These are the steps of Algorithm 1 and Eq. 13 of Vehtari, Simpson, Gelman, Yao and Gabry (2024). Line L10 sums the pointwise values, L11 computes $\sqrt{n}$ times their sample standard deviation, and L12 computes $p_{\mathrm{loo}} = \mathrm{lppd} - \mathrm{elpd}_{\mathrm{loo}}$ with $\mathrm{lppd} = \sum_i \log \frac1S \sum_s p(y_i \mid \theta^s)$. $\square$

**Claim 4 (order and cap).** After L6 and L7, the $S - M$ smallest weights are unchanged, and the $M$ tail weights are nondecreasing in the rank and lie in $[u, 1]$.

*Proof.* Lines L6 and L7 change only the draws of ranks $S - M + 1$ to $S$. For $k \ne 0$ and $\sigma > 0$ the function $p \mapsto F^{-1}(p; k, \sigma) = \sigma((1 - p)^{-k} - 1)/k$ has derivative $\sigma (1 - p)^{-k - 1} > 0$ on $[0, 1)$, and $F^{-1}(0) = 0$; the case $k = 0$ is $-\sigma \log(1 - p)$, also increasing with value $0$ at $0$. The points $(z - 1/2)/M$ increase with $z$ and lie in $(0, 1)$. So $u + F^{-1}((z - 1/2)/M)$ is at least $u$ and increases with $z$, and the minimum with $1$ keeps both facts and adds the upper bound. The draw of rank $S - M + z$ gets the $z$-th value, so the order of the draws is kept. Since the largest raw ratio is $1$ and $u \le 1$, every weight lies in $[0, 1]$. $\square$

As a consequence, no single draw can get a weight above the largest raw ratio, and the weights of the body of the distribution are exactly the raw ones.

**Claim 5 (L15 is the profile log-likelihood).** The generalized Pareto law with location $0$, shape $k \ne 0$ and scale $\sigma > 0$ has density $\frac1\sigma (1 + kx/\sigma)^{-1/k - 1}$ on its support. For exceedances $x_1, \ldots, x_M$ and fixed $\theta = -k/\sigma$ with $1 - \theta x_t > 0$ for all $t$ and $\kappa(\theta) \ne 0$, the maximum of the log-likelihood over $k$ is $M(\log(-\theta/\kappa(\theta)) - \kappa(\theta) - 1)$, attained at $k = \kappa(\theta) = \frac1M \sum_t \log(1 - \theta x_t)$.

*Proof.* With $\sigma = -k/\theta$ we have $1 + kx/\sigma = 1 - \theta x$, so the log-likelihood is

$$\ell(k) = -M \log\Big(-\frac{k}{\theta}\Big) - \Big(\frac1k + 1\Big) M \kappa(\theta).$$

Here $k$ and $\theta$ have opposite signs because $\sigma > 0$. The derivative in $k$ is $-M/k + M\kappa(\theta)/k^2$, which is zero only at $k = \kappa(\theta)$. On the side of $0$ where $k\theta < 0$ the second term dominates near $0$ and the first term dominates at infinity, so this point is the maximum. Substituting $k = \kappa(\theta)$ gives $-M\log(-\kappa/\theta) - M - M\kappa = M(\log(-\theta/\kappa) - \kappa - 1)$. $\square$

The grid of L14 satisfies $\theta_j < 1/x_M$, because $\sqrt{m/(j - 1/2)} > 1$ for $j \le m$. So $1 - \theta_j x_t > 0$ for every exceedance, and L15 is defined. Lines L16 and L17 average $\theta$ with weights proportional to the profile likelihood, which is the estimate of Zhang and Stephens (2009) with their grid and prior, and L18 is the shrinkage of Appendix G of Vehtari et al. (2024).

**What is not proved here.** Vehtari et al. (2024, Section 3) argue that the PSIS estimate has finite variance and is consistent as $S \to \infty$, and that its error is small when the true tail shape is below about $0.7$. These statements rest on the asymptotic theory of the generalized Pareto approximation to a tail and on simulation. This page cites them. The tests measure the error against exact leave-one-out in a conjugate normal model, and check Claims 1, 3 and 4 directly.
