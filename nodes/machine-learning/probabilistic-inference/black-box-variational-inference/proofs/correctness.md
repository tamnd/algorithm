---
title: The BBVI gradient estimates are unbiased
proves: [correctness]
status: full
---

We use the ELBO $\mathcal{L}(\lambda) = \mathbb{E}_{q(z; \lambda)}[\log p(x, z) - \log q(z; \lambda)]$, the mean-field family $q(z; \lambda) = \prod_i q_i(z_i; \lambda_i)$, and the estimators of the page. We assume that $q$ is differentiable in $\lambda$, that its support does not depend on $\lambda$, and that the expected values below are finite and allow differentiation under the integral sign (as they do for the Gaussian family and the Gaussian target of the tests, by dominated convergence).

**Lemma 1 (the score has mean zero).** $\mathbb{E}_{q}[\nabla_\lambda \log q(z; \lambda)] = 0$.

*Proof.* $\mathbb{E}_q[\nabla_\lambda \log q] = \int q\, \frac{\nabla_\lambda q}{q}\, dz = \nabla_\lambda \int q\, dz = \nabla_\lambda 1 = 0$. $\square$

**Theorem 1 (the score function gradient).** $\nabla_\lambda \mathcal{L} = \mathbb{E}_q[\nabla_\lambda \log q(z; \lambda)\, (\log p(x, z) - \log q(z; \lambda))]$, so the average of $S$ independent samples of the quantity in brackets is an unbiased estimate.

*Proof.* Write $\mathcal{L} = \int q(z; \lambda)\, w(z, \lambda)\, dz$ with $w = \log p(x, z) - \log q(z; \lambda)$. By the product rule, $\nabla_\lambda \mathcal{L} = \int (\nabla_\lambda q)\, w\, dz + \int q\, \nabla_\lambda w\, dz$. The first term is $\mathbb{E}_q[\nabla_\lambda \log q \cdot w]$, because $\nabla_\lambda q = q \nabla_\lambda \log q$. The second term is $-\mathbb{E}_q[\nabla_\lambda \log q] = 0$ by Lemma 1. $\square$

**Theorem 2 (Rao-Blackwellization).** Let $\log p_i(x, z)$ be the sum of the terms of $\log p(x, z)$ that depend on $z_i$, so that $\log p(x, z) = \log p_i(x, z) + r_i(x, z_{-i})$, where $r_i$ does not depend on $z_i$. Then

$$\nabla_{\lambda_i} \mathcal{L} = \mathbb{E}_q\big[\nabla_{\lambda_i} \log q_i(z_i; \lambda_i)\, (\log p_i(x, z) - \log q_i(z_i; \lambda_i))\big].$$

*Proof.* In Theorem 1, $\nabla_{\lambda_i} \log q = \nabla_{\lambda_i} \log q_i(z_i)$, because the other factors do not depend on $\lambda_i$. Write $w = (\log p_i - \log q_i(z_i)) + (r_i(z_{-i}) - \sum_{k \ne i} \log q_k(z_k))$. The second bracket is a function $g(z_{-i})$ only. Under the mean-field $q$, $z_i$ is independent of $z_{-i}$, so $\mathbb{E}_q[\nabla_{\lambda_i} \log q_i(z_i)\, g(z_{-i})] = \mathbb{E}_{q_i}[\nabla_{\lambda_i} \log q_i] \cdot \mathbb{E}[g] = 0$, by Lemma 1 for the family $q_i$. $\square$

The removed terms contribute zero in expected value but add noise to each sample, so dropping them keeps the mean and usually lowers the variance. Ranganath, Gerrish and Blei derive this form by Rao-Blackwellization, hence the name.

**Theorem 3 (the control variate keeps the estimate unbiased).** Let $f_s$ be the Rao-Blackwellized summand for factor $i$ at sample $s$ and $h_s = \nabla_{\lambda_i} \log q_i(z_{i,s})$. Let $a_s$ be any function of the samples other than $s$ (in the implementation, the coefficient $\sum_d \mathrm{Cov}(f_d, h_d) / \sum_d \mathrm{Var}(h_d)$ estimated from the other $S - 1$ samples). Then $\frac{1}{S} \sum_s (f_s - a_s h_s)$ is unbiased for $\nabla_{\lambda_i} \mathcal{L}$.

*Proof.* The samples are independent, so $a_s$ is independent of $h_s$ and $\mathbb{E}[a_s h_s] = \mathbb{E}[a_s]\, \mathbb{E}[h_s] = 0$ by Lemma 1. The $f_s$ are unbiased by Theorem 2. $\square$

If the coefficient is computed from all $S$ samples, including sample $s$, as in Ranganath, Gerrish and Blei, the estimate has a bias of order $1/S$; the leave-one-out form removes it.

**Theorem 4 (the reparameterization gradient).** If $z = \mu + \sigma \odot \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, I)$, $\sigma_i = e^{\omega_i}$, and $\log p(x, \cdot)$ is differentiable, then $\nabla_{\mu} \mathcal{L} = \mathbb{E}_\varepsilon[\nabla_z \log p(x, z)]$ and $\partial \mathcal{L} / \partial \omega_i = \mathbb{E}_\varepsilon[(\nabla_z \log p(x, z))_i\, \sigma_i \varepsilon_i] + 1$.

*Proof.* The entropy of $q$ is $\sum_i \omega_i + \frac{n}{2}(1 + \log 2\pi)$, so its derivative in $\omega_i$ is $1$ and in $\mu$ is $0$. The other part is $\mathbb{E}_\varepsilon[\log p(x, \mu + \sigma \odot \varepsilon)]$, whose distribution of $\varepsilon$ does not depend on $\lambda$; differentiate under the integral sign and use the chain rule, with $\partial z_i / \partial \mu_i = 1$ and $\partial z_i / \partial \omega_i = \sigma_i \varepsilon_i$. $\square$

**Remark (the optimization).** With unbiased gradient estimates of finite variance and step sizes $\rho_t$ with $\sum \rho_t = \infty$ and $\sum \rho_t^2 < \infty$, stochastic gradient ascent converges to a stationary point of a smooth $\mathcal{L}$ under the usual conditions of stochastic approximation (Robbins and Monro 1951). That theory is not repeated here. AdaGrad step sizes do not have this exact form; the page states what the tests observe.
