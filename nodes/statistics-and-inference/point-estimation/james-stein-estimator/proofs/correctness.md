---
title: The James-Stein estimator has risk p - (p - 2)^2 E[1/||X||^2], below p for every theta
proves: [correctness]
status: full
---

We use the pseudocode of the page with target $m = 0$ and $\sigma^2 = 1$; the general case follows by the change of variable $Y = (X - m)/\sigma$, which maps $N_p(\theta, \sigma^2 I)$ to $N_p((\theta - m)/\sigma, I)$ and multiplies every squared error by $\sigma^2$. So let $X \sim N_p(\theta, I_p)$ with $p \ge 3$, and

$$\delta(X) = \Big(1 - \frac{p-2}{\lVert X \rVert^2}\Big) X = X - g(X), \qquad g(x) = \frac{(p-2)\, x}{\lVert x \rVert^2}.$$

**Claim 0 (the code computes $\delta$).** Lines L1 and L2 compute $p$ and $s = \lVert x - m \rVert^2$. Line L3 handles $s = 0$, an event of probability zero, so it does not change the risk. Line L4 sets $k = (p-2)\sigma^2$, and line L6 returns $m_i + d_i - k\, d_i / s = m_i + (1 - k/s)\, d_i$ with $d = x - m$, which is $\delta$. Line L5 is used only by the positive-part variant: when $s \le k$ the factor $1 - k/s$ is at most $0$, and the variant returns $m$. $\square$

**Lemma 1 ($\mathbb{E}[1/\lVert X \rVert^2]$ is finite).** For $p \ge 3$, $\mathbb{E}_\theta[1/\lVert X \rVert^2] \le \mathbb{E}_0[1/\lVert X \rVert^2] = 1/(p-2)$.

*Proof.* Let $W = \lVert X \rVert^2$ and $\lambda = \lVert \theta \rVert^2$. For $t > 0$, the moment generating function of the noncentral chi-squared law gives $\mathbb{E}\, e^{-tW} = (1 + 2t)^{-p/2} \exp(-\lambda t/(1 + 2t))$. Since $1/W = \int_0^\infty e^{-tW}\, dt$, Tonelli's theorem gives

$$\mathbb{E}[1/W] = \int_0^\infty (1 + 2t)^{-p/2} e^{-\lambda t/(1+2t)}\, dt = \int_0^1 w^{p-3}\, e^{-\lambda(1 - w^2)/2}\, dw,$$

with $w = (1 + 2t)^{-1/2}$, $dt = -w^{-3}\, dw$. The integrand is at most $w^{p-3}$, whose integral is $1/(p-2)$ for $p \ge 3$, with equality when $\lambda = 0$. The integrand decreases in $\lambda$, so $\mathbb{E}[1/W]$ decreases in $\lambda$. $\square$

**Lemma 2 (the Poisson series).** $\mathbb{E}[1/W] = \sum_{k \ge 0} e^{-\lambda/2} \frac{(\lambda/2)^k}{k!} \cdot \frac{1}{p - 2 + 2k}$.

*Proof.* Expand $e^{-\lambda(1-w^2)/2} = e^{-\lambda/2}\sum_k (\lambda/2)^k w^{2k}/k!$ in the integral of Lemma 1 and integrate term by term (all terms are nonnegative): $\int_0^1 w^{p-3+2k}\, dw = 1/(p - 2 + 2k)$. $\square$

The function `inverse_moment_noncentral_chi2` sums this series; the tests compare it with Simpson's rule on the integral of Lemma 1.

**Lemma 3 (Stein's identity).** Let $Z \sim N(\mu, 1)$ and let $h : \mathbb R \to \mathbb R$ be absolutely continuous with $\mathbb{E}\lvert h'(Z) \rvert < \infty$. Then $\mathbb{E}[(Z - \mu) h(Z)] = \mathbb{E}[h'(Z)]$.

*Proof.* Let $\varphi$ be the standard normal density, so $\varphi'(u) = -u\varphi(u)$. Write $h(z) = h(\mu) + \int_\mu^z h'(y)\, dy$. Then

$$\mathbb{E}[(Z - \mu)h(Z)] = \int_{-\infty}^{\infty} (z - \mu)\varphi(z - \mu) \int_\mu^z h'(y)\, dy\, dz,$$

because $\mathbb{E}[Z - \mu] = 0$. For $z > \mu$ swap the order of integration (Fubini, justified by $\mathbb{E}\lvert h'(Z) \rvert < \infty$): $\int_\mu^\infty h'(y) \int_y^\infty (z - \mu)\varphi(z - \mu)\, dz\, dy = \int_\mu^\infty h'(y)\varphi(y - \mu)\, dy$. The part $z < \mu$ gives $\int_{-\infty}^\mu h'(y)\varphi(y - \mu)\, dy$ in the same way. The sum is $\mathbb{E}[h'(Z)]$. $\square$

**Lemma 4 (the cross term).** $\mathbb{E}_\theta[(X - \theta)^\top g(X)] = (p - 2)^2\, \mathbb{E}_\theta[1/\lVert X \rVert^2]$.

*Proof.* Fix $i$ and condition on the other coordinates $X_{-i}$. When $X_{-i} \ne 0$, which has probability 1, the map $x_i \mapsto g_i(x) = (p-2)x_i/(x_i^2 + \lVert x_{-i} \rVert^2)$ is smooth and bounded, with

$$\partial_i g_i(x) = (p - 2)\Big(\frac{1}{\lVert x \rVert^2} - \frac{2x_i^2}{\lVert x \rVert^4}\Big), \qquad \lvert \partial_i g_i(x) \rvert \le \frac{p-2}{\lVert x \rVert^2}.$$

So Lemma 3 applies given $X_{-i}$, and then $\mathbb{E}[(X_i - \theta_i) g_i(X)] = \mathbb{E}[\partial_i g_i(X)]$; the expectation is finite by Lemma 1. Summing over $i$,

$$\sum_{i=1}^p \partial_i g_i(x) = (p - 2)\Big(\frac{p}{\lVert x \rVert^2} - \frac{2}{\lVert x \rVert^2}\Big) = \frac{(p-2)^2}{\lVert x \rVert^2}. \qquad \square$$

**Theorem (the risk).** For every $\theta \in \mathbb R^p$,

$$R(\theta, \delta) = \mathbb{E}_\theta \lVert \delta(X) - \theta \rVert^2 = p - (p - 2)^2\, \mathbb{E}_\theta\Big[\frac{1}{\lVert X \rVert^2}\Big] < p = R(\theta, X).$$

*Proof.* Expand $\lVert X - \theta - g(X) \rVert^2$:

$$R(\theta, \delta) = \mathbb{E}\lVert X - \theta \rVert^2 - 2\,\mathbb{E}[(X - \theta)^\top g(X)] + \mathbb{E}\lVert g(X) \rVert^2 = p - 2(p-2)^2\, \mathbb{E}\Big[\frac{1}{\lVert X \rVert^2}\Big] + (p-2)^2\, \mathbb{E}\Big[\frac{1}{\lVert X \rVert^2}\Big],$$

by Lemma 4 and $\lVert g(x) \rVert^2 = (p-2)^2/\lVert x \rVert^2$. All three expectations are finite by Lemma 1. The last term of the result is positive because $1/\lVert X \rVert^2 > 0$ with probability 1. $\blacksquare$

**Corollaries.**

1. *At the target.* For $\theta = 0$, Lemma 1 gives $\mathbb{E}[1/\lVert X \rVert^2] = 1/(p-2)$, so $R(0, \delta) = p - (p - 2) = 2$ for every $p \ge 3$.
2. *Shape.* By Lemma 1 the risk depends on $\theta$ only through $\lambda = \lVert \theta \rVert^2$, increases with $\lambda$, and tends to $p$ as $\lambda \to \infty$ (the integrand of Lemma 1 tends to $0$ for $w < 1$).
3. *Unbiased risk estimate.* The proof shows that $p - (p-2)^2/\lVert X \rVert^2$ has expectation $R(\theta, \delta)$ for every $\theta$. This is Stein's unbiased risk estimate for $\delta$; the function `stein_unbiased_risk_estimate` returns it.
4. *Domination.* Since $R(\theta, X) = p$ for every $\theta$, $\delta$ dominates $X$ under total squared error when $p \ge 3$, so $X$ is inadmissible.

**What is not proved here.** The positive-part variant has risk no larger than the plain estimator at every $\theta$ (Baranchik 1964; Lehmann and Casella, Chapter 5); this note does not prove it, and the tests only check it by simulation at three values of $\theta$. Lindley's variant toward the mean has risk $1 + R_{p-1}(\lVert \theta - \bar\theta \mathbf 1 \rVert^2)$, where $R_{p-1}$ is the plain risk in dimension $p - 1$; this follows from the theorem applied in the subspace orthogonal to $\mathbf 1$, and the tests check its value $3$ at a constant $\theta$ by simulation.

**Floating point.** The code computes $s$ with `math.fsum` and forms $d_i/s$ before the multiplication by $k$, so a tiny $s$ gives a large finite or infinite value but never $0 \cdot \infty$. The exact risk sums the Poisson series over the terms within $40\sqrt{\lambda/2} + 50$ of the Poisson mean; the omitted mass is far below double precision.
