---
title: The MAP mean update maximizes the penalized auxiliary function and never lowers the log posterior
proves: [correctness]
status: full
---

We use the notation of the page. The prior model is a mixture of $M$ Gaussians with weights $c_m > 0$, means $\mu^0_m \in \mathbb{R}^n$ and diagonal covariances $\Sigma_m = \mathrm{diag}(\sigma^2_{m,1}, \ldots, \sigma^2_{m,n})$. The weights and the covariances are fixed. The unknown means $\mu = (\mu_1, \ldots, \mu_M)$ have the prior

$$p(\mu) = \prod_{m=1}^{M} \mathcal{N}\big(\mu_m;\ \mu^0_m,\ \Sigma_m / \tau\big), \qquad \tau > 0.$$

The data are the frames $O = o_1, \ldots, o_T$, and $p(O \mid \mu) = \prod_t \sum_m c_m \mathcal{N}(o_t; \mu_m, \Sigma_m)$. MAP estimation maximizes the log posterior up to a constant, $J(\mu) = \log p(O \mid \mu) + \log p(\mu)$. All logs are natural logs.

Fix the current means $\mu^{\mathrm{old}}$. Let $\gamma_m(t)$ be the posterior of Gaussian $m$ at frame $t$ under them (line L3), and let $n_m = \sum_t \gamma_m(t)$ and $s_m = \sum_t \gamma_m(t) o_t$ (line L4). The penalized auxiliary function is

$$\mathcal{F}(\mu) = \sum_{t=1}^{T} \sum_{m=1}^{M} \gamma_m(t) \log\big( c_m \mathcal{N}(o_t; \mu_m, \Sigma_m) \big) + \log p(\mu).$$

**Lemma 1 (the M-step).** $\mathcal{F}$ has the unique maximizer $\mu_m = (\tau \mu^0_m + s_m) / (\tau + n_m)$ for every $m$, the update of line L5.

*Proof.* Collect the terms of $\mathcal{F}$ that depend on coordinate $i$ of $\mu_m$. With diagonal covariances they are

$$f(x) = -\frac{1}{2 \sigma^2_{m,i}} \Big( \sum_t \gamma_m(t) (o_{t,i} - x)^2 + \tau (x - \mu^0_{m,i})^2 \Big),$$

and no other term depends on $x = \mu_{m,i}$. The second derivative is $-(n_m + \tau)/\sigma^2_{m,i} < 0$, so $f$ is strictly concave, and its maximum is where the derivative is zero:

$$\sum_t \gamma_m(t) (o_{t,i} - x) + \tau (\mu^0_{m,i} - x) = 0 \iff x = \frac{\tau \mu^0_{m,i} + s_{m,i}}{\tau + n_m}. \qquad \square$$

**Theorem 2 (MAP-EM is monotone).** Let $\mu^{\mathrm{new}}$ be the means of line L5 computed from the posteriors of $\mu^{\mathrm{old}}$. Then $J(\mu^{\mathrm{new}}) \ge J(\mu^{\mathrm{old}})$.

*Proof.* Write $p(o_t, m \mid \mu) = c_m \mathcal{N}(o_t; \mu_m, \Sigma_m)$, so that $\gamma_m(t) = p(o_t, m \mid \mu^{\mathrm{old}}) / p(o_t \mid \mu^{\mathrm{old}})$ is a distribution over $m$. By Jensen's inequality for the concave log, for any $\mu$,

$$\log \frac{p(o_t \mid \mu)}{p(o_t \mid \mu^{\mathrm{old}})} = \log \sum_m \gamma_m(t) \frac{p(o_t, m \mid \mu)}{p(o_t, m \mid \mu^{\mathrm{old}})} \ge \sum_m \gamma_m(t) \log \frac{p(o_t, m \mid \mu)}{p(o_t, m \mid \mu^{\mathrm{old}})}.$$

Sum over $t$ and add $\log p(\mu) - \log p(\mu^{\mathrm{old}})$ to both sides: $J(\mu) - J(\mu^{\mathrm{old}}) \ge \mathcal{F}(\mu) - \mathcal{F}(\mu^{\mathrm{old}})$. By Lemma 1, $\mathcal{F}(\mu^{\mathrm{new}}) \ge \mathcal{F}(\mu^{\mathrm{old}})$. $\square$

So the iteration of lines L2 to L5 climbs the posterior, and at a fixed point the gradient of $J$ is zero. Like any EM, it can stop at a local maximum.

**Proposition 3 (one Gaussian: the exact posterior).** If $M = 1$, then $\gamma_1(t) = 1$ for every frame, and the update is the mean of the exact posterior distribution of $\mu_1$, which is

$$\mu_1 \mid O \ \sim\ \mathcal{N}\Big( \frac{\tau \mu^0 + \sum_t o_t}{\tau + T},\ \frac{\Sigma}{\tau + T} \Big).$$

*Proof.* The prior is Gaussian and the likelihood of a Gaussian mean with a known covariance is Gaussian in the mean, so the posterior is Gaussian ([conjugate prior](/conjugate-prior/)). Its precision is the sum of the prior precision $\tau \Sigma^{-1}$ and the data precision $T \Sigma^{-1}$, and its mean is the precision weighted average of $\mu^0$ and the sample mean $\bar o$: $(\tau \mu^0 + T \bar o)/(\tau + T)$. One update with $n_1 = T$ and $s_1 = T \bar o$ gives the same value, and further iterations do not change it, because the posteriors stay 1. $\square$

For $M > 1$ the posterior of the means is a mixture over all assignments of frames to Gaussians, and the MAP-EM result is only a mode of it.

**Proposition 4 (the relevance factor form).** With $\alpha_m = n_m / (n_m + r)$ and $E_m = s_m / n_m$ for $n_m > 0$, the form of Reynolds, Quatieri and Dunn, $\hat\mu_m = \alpha_m E_m + (1 - \alpha_m) \mu^0_m$, equals one step of line L5 with $\tau = r$.

*Proof.* $\alpha_m E_m + (1 - \alpha_m) \mu^0_m = \frac{n_m}{n_m + r} \cdot \frac{s_m}{n_m} + \frac{r}{n_m + r} \mu^0_m = \frac{s_m + r \mu^0_m}{n_m + r}$. For $n_m = 0$ both forms give $\mu^0_m$. $\square$

**Remark (what is not claimed).** Gauvain and Lee 1994 also place a Dirichlet prior on the weights and a normal-Wishart prior on the means and precisions jointly, and give EM updates for all of them. The weight and variance updates of Reynolds et al. 2000 are a one-step heuristic with the same form; they are not shown here to be the maximizer of a posterior. The value $r = 16$ is a choice made on development data, not a result.
