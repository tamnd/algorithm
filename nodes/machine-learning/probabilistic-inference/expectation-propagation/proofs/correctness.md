---
title: The EP update is the KL(p||q) projection of the tilted distribution, and EP is exact for Gaussian sites
proves: [correctness]
status: full
---

We use the clutter model, the sites, the cavity and the tilted distribution of the page. A Gaussian $q$ is written $\mathcal{N}(m, v)$, and its natural parameters are $(1/v, m/v)$, the coefficients of $-\theta^2/2$ and $\theta$ in $\log q$.

**Lemma 1 (projection is moment matching).** Let $\hat p$ be a density on $\mathbb{R}$ with finite mean $\hat m$ and variance $\hat v > 0$. Among all Gaussians $q$, $\mathrm{KL}(\hat p \,\|\, q)$ is smallest exactly for $q = \mathcal{N}(\hat m, \hat v)$.

*Proof.* $\mathrm{KL}(\hat p \| q) = \mathbb{E}_{\hat p}[\log \hat p] - \mathbb{E}_{\hat p}[\log q]$, and only the second term depends on $q$. For $q = \mathcal{N}(m, v)$,

$$-\mathbb{E}_{\hat p}[\log q] = \tfrac12 \log(2\pi v) + \frac{\mathbb{E}_{\hat p}[(\theta - m)^2]}{2v} = \tfrac12 \log(2\pi v) + \frac{\hat v + (\hat m - m)^2}{2v}.$$

For each $v$ this is smallest at $m = \hat m$. Then $g(v) = \tfrac12 \log v + \hat v/(2v)$ has $g'(v) = \frac{1}{2v} - \frac{\hat v}{2v^2}$, which is negative for $v < \hat v$ and positive for $v > \hat v$, so the unique minimum is at $v = \hat v$. $\square$

**Lemma 2 (the tilted moments of the clutter site).** Let the cavity be $\mathcal{N}(m_c, v_c)$ with $v_c > 0$, and let $\hat p(\theta) \propto t(\theta)\, \mathcal{N}(\theta; m_c, v_c)$ with $t(\theta) = (1 - w)\mathcal{N}(x; \theta, 1) + w \mathcal{N}(x; 0, a)$. With $d = x - m_c$,

$$Z = (1 - w)\mathcal{N}(x; m_c, v_c + 1) + w \mathcal{N}(x; 0, a), \qquad r = \frac{(1 - w)\mathcal{N}(x; m_c, v_c + 1)}{Z},$$

$$\hat m = m_c + \frac{r v_c d}{v_c + 1}, \qquad \hat v = v_c - \frac{r v_c^2}{v_c + 1} + \frac{r(1 - r) v_c^2 d^2}{(v_c + 1)^2}.$$

*Proof.* The product $\mathcal{N}(x; \theta, 1)\, \mathcal{N}(\theta; m_c, v_c)$ equals $\mathcal{N}(x; m_c, v_c + 1)\, \mathcal{N}(\theta; \mu_1, \sigma_1^2)$ with $\sigma_1^2 = v_c/(v_c + 1)$ and $\mu_1 = m_c + v_c d/(v_c + 1)$: both sides are the joint density of $(\theta, x)$ with $\theta \sim \mathcal{N}(m_c, v_c)$ and $x \mid \theta \sim \mathcal{N}(\theta, 1)$, written once as prior times likelihood and once as marginal of $x$ times posterior of $\theta$. So $t(\theta) \mathcal{N}(\theta; m_c, v_c)$ is a mixture of $\mathcal{N}(\mu_1, \sigma_1^2)$ with weight $(1 - w)\mathcal{N}(x; m_c, v_c + 1)$ and $\mathcal{N}(m_c, v_c)$ with weight $w \mathcal{N}(x; 0, a)$. Its total mass is $Z$, and the normalized weights are $r$ and $1 - r$. The mean of a mixture is $r \mu_1 + (1 - r) m_c = m_c + r(\mu_1 - m_c)$, which is $\hat m$. Its variance is the mean of the component variances plus the variance of the component means: $r \sigma_1^2 + (1 - r) v_c + r(1 - r)(\mu_1 - m_c)^2$. Substituting $\sigma_1^2 = v_c - v_c^2/(v_c + 1)$ and $\mu_1 - m_c = v_c d/(v_c + 1)$ gives $\hat v$. $\square$

So the step that sets $q \leftarrow \mathcal{N}(\hat m, \hat v)$ is the projection $\arg\min_q \mathrm{KL}(\hat p \| q)$ over Gaussians, by Lemma 1, and the new site is $q$ divided by the cavity, in natural parameters a subtraction. Note that $\hat v > 0$: $\hat v \ge r \sigma_1^2 + (1 - r) v_c > 0$.

**Theorem 1 (Gaussian sites are exact).** If $w = 0$, then after the first sweep $q$ is the exact posterior, and the second sweep changes nothing.

*Proof.* With $w = 0$, $t_n(\theta) = \mathcal{N}(x_n; \theta, 1) \propto \exp(-\theta^2/2 + x_n \theta)$, a Gaussian site with natural parameters $(1, x_n)$. When site $n$ is updated, the cavity has precision at least $1/b > 0$, the tilted distribution $t_n q_{\setminus n}$ is Gaussian, and by Lemma 1 the projection returns it unchanged. So the new site is $t_n$ itself, exactly, and each site gets its exact value at its first visit. After the first sweep, $q = p(\theta) \prod_n t_n(\theta)$ normalized, which is the posterior. In the second sweep, each cavity times $t_n$ is again $q$, whose projection is $q$, so no site changes. $\square$

**Theorem 2 (what a fixed point means).** If a sweep changes no site and skips none, then for every $n$, $q$ has the same mean and variance as the tilted distribution $\hat p_n \propto t_n(\theta)\, q(\theta) / \tilde t_n(\theta)$.

*Proof.* When site $n$ is updated without change, the new $q$, which is the projection of $\hat p_n$, equals the old $q$; by Lemma 1 it has the moments of $\hat p_n$. $\square$

**Remark.** Theorem 2 is the EP fixed-point condition; Minka (2001) and later Heskes and others related such fixed points to stationary points of an approximate free energy. Nothing here proves that EP converges, or that the moments of $q$ at a fixed point equal those of the posterior; on the page they are compared with numerical integration, and one seeded data set makes EP fail to converge.
