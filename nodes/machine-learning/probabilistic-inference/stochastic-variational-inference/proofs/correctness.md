---
title: The SVI step is an unbiased natural gradient step, and its fixed points are those of CAVI
proves: [correctness]
status: full
---

We use the conditionally conjugate model of the page: global variables $\beta$, local pairs $(z_n, x_n)$ for $n = 1, \ldots, N$, and the complete conditional of $\beta$ in the exponential family,

$$p(\beta \mid x, z) = h(\beta) \exp\big(\eta_g(x, z)^\top t(\beta) - a_g(\eta_g(x, z))\big), \qquad \eta_g(x, z) = \alpha + \sum_{n=1}^N t(x_n, z_n),$$

where $\alpha$ is the natural parameter of the prior and $t(x_n, z_n)$ are the sufficient statistics of one data point. The family is $q(\beta; \lambda) = h(\beta) \exp(\lambda^\top t(\beta) - a_g(\lambda))$ times local factors $q(z_n; \phi_n)$. Write $\hat\lambda = \alpha + \sum_n \mathbb{E}_{\phi_n}[t(x_n, z_n)]$.

**Lemma 1.** $\mathbb{E}_{q(\beta; \lambda)}[t(\beta)] = \nabla a_g(\lambda)$, and the Fisher information of $q(\beta; \lambda)$ in $\lambda$ is $\nabla^2 a_g(\lambda)$, the covariance of $t(\beta)$.

*Proof.* Differentiate $\int h(\beta) \exp(\lambda^\top t(\beta) - a_g(\lambda))\, d\beta = 1$ once and twice under the integral sign, as allowed inside the open natural parameter space. The first derivative gives $\mathbb{E}[t] - \nabla a_g = 0$. The score is $t(\beta) - \nabla a_g(\lambda)$, so the Fisher information is its covariance, $\mathrm{Cov}(t)$; the second derivative gives $\mathbb{E}[(t - \nabla a_g)(t - \nabla a_g)^\top] - \nabla^2 a_g = 0$. $\square$

**Theorem 1 (the natural gradient; Hoffman, Blei, Wang and Paisley 2013).** With the local factors $\phi$ held fixed, $\nabla_\lambda \mathcal{L} = \nabla^2 a_g(\lambda)\, (\hat\lambda - \lambda)$, so the natural gradient is $\hat\lambda - \lambda$.

*Proof.* Write $\log p(x, z, \beta) = \log p(\beta \mid x, z) + \log p(x, z)$; the second term does not depend on $\beta$. So the terms of $\mathcal{L} = \mathbb{E}_q[\log p(x, z, \beta) - \log q(\beta) - \log q(z)]$ that depend on $\lambda$ are

$$\mathbb{E}_q[\log p(\beta \mid x, z)] - \mathbb{E}_q[\log q(\beta; \lambda)] = \mathbb{E}_\phi[\eta_g(x, z)]^\top \nabla a_g(\lambda) - \lambda^\top \nabla a_g(\lambda) + a_g(\lambda) + c,$$

where $c$ does not depend on $\lambda$: the $\log h(\beta)$ terms cancel, $\mathbb{E}_\phi[a_g(\eta_g)]$ does not depend on $\lambda$, and $\mathbb{E}_q[t(\beta)] = \nabla a_g(\lambda)$ by Lemma 1, with $\beta$ and $z$ independent under $q$. The expected natural parameter is $\mathbb{E}_\phi[\eta_g] = \hat\lambda$, because $\eta_g$ is linear in the statistics $t(x_n, z_n)$. Differentiate: $\nabla^2 a_g\, \hat\lambda - \nabla a_g - \nabla^2 a_g\, \lambda + \nabla a_g = \nabla^2 a_g(\lambda)(\hat\lambda - \lambda)$. Multiplying by the inverse Fisher information of Lemma 1 gives $\hat\lambda - \lambda$. $\square$

So the update $\lambda \leftarrow (1 - \rho)\lambda + \rho \hat\lambda = \lambda + \rho(\hat\lambda - \lambda)$ is a natural gradient step of size $\rho$, and with $\rho = 1$ it is the coordinate ascent update $\lambda \leftarrow \hat\lambda$.

**Theorem 2 (the minibatch estimate is unbiased).** Let the local factors be set to their optimum given $\lambda$, $\phi_n = \phi_n^\ast(\lambda, x_n)$, which depends only on $\lambda$ and $x_n$. Let $B$ be a uniformly random subset of size $b$ of $\{1, \ldots, N\}$, and $\hat\lambda_B = \alpha + \frac{N}{b} \sum_{n \in B} \mathbb{E}_{\phi_n}[t(x_n, z_n)]$. Then $\mathbb{E}_B[\hat\lambda_B] = \hat\lambda$, so $\hat\lambda_B - \lambda$ is an unbiased estimate of the natural gradient at $\lambda$ with all local factors optimal.

*Proof.* Each $n$ lies in $B$ with probability $b/N$. By linearity, $\mathbb{E}_B[\frac{N}{b} \sum_{n \in B} g_n] = \frac{N}{b} \sum_n \frac{b}{N} g_n = \sum_n g_n$ for $g_n = \mathbb{E}_{\phi_n}[t(x_n, z_n)]$. Because $\phi_n$ depends only on $\lambda$ and $x_n$, the value $g_n$ is the same whether $n$ is in a minibatch or in the full data. $\square$

**Corollary (fixed points).** The expected step $\mathbb{E}_B[\hat\lambda_B] - \lambda$ is zero exactly when $\lambda = \hat\lambda(\lambda)$, that is, at the fixed points of batch coordinate ascent (CAVI). At these points, by Theorem 1 with the local factors optimal, the gradient of the ELBO in $\lambda$ is zero, and the local factors are optimal by construction.

**Remark (convergence).** Theorem 2 makes SVI a stochastic approximation scheme with unbiased steps. With step sizes $\sum_t \rho_t = \infty$ and $\sum_t \rho_t^2 < \infty$, such as $\rho_t = (t + \tau)^{-\kappa}$ with $\kappa \in (0.5, 1]$, Hoffman et al. rely on the theory of stochastic approximation (Robbins and Monro 1951) for convergence to a local optimum; that theory is not repeated here.
