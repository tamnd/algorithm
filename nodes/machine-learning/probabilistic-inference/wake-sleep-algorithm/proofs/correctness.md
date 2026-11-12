---
title: The wake phase follows the ELBO gradient, the sleep phase follows a different objective
proves: [correctness]
status: full
---

We use the Helmholtz machine of the page: generative parameters $\theta = (b, c, W)$ with $p_\theta(h_j = 1) = \sigma(b_j)$ and $p_\theta(v_i = 1 \mid h) = \sigma(c_i + \sum_j W_{ij} h_j)$, and recognition parameters $\phi = (d, R)$ with $q_\phi(h_j = 1 \mid v) = \sigma(d_j + \sum_i R_{ji} v_i)$. All sums over $h$ and $v$ are finite.

**Lemma 1 (the delta rule).** For a bit $y \in \{0, 1\}$ with $P(y = 1) = \sigma(z)$, $\frac{\partial}{\partial z} \log P(y) = y - \sigma(z)$.

*Proof.* $\log P(y) = y \log \sigma(z) + (1 - y) \log(1 - \sigma(z))$. With $\sigma'(z) = \sigma(z)(1 - \sigma(z))$, the derivative is $y(1 - \sigma(z)) - (1 - y)\sigma(z) = y - \sigma(z)$. $\square$

By the chain rule, $\partial \log p_\theta(v, h) / \partial b_j = h_j - \sigma(b_j)$, $\partial / \partial c_i = v_i - \hat v_i$ and $\partial / \partial W_{ij} = (v_i - \hat v_i) h_j$, where $\hat v_i = \sigma(c_i + \sum_k W_{ik} h_k)$. These are the wake updates. In the same way, $\partial \log q_\phi(h \mid v) / \partial d_j = h_j - \hat h_j$ and $\partial / \partial R_{ji} = (h_j - \hat h_j) v_i$ with $\hat h_j = q_\phi(h_j = 1 \mid v)$. These are the sleep updates.

**Theorem 1 (the wake phase).** For a data vector $v$, the expected wake update, with $h \sim q_\phi(\cdot \mid v)$, is $\nabla_\theta \mathcal{L}(\theta, \phi; v)$, where $\mathcal{L}(\theta, \phi; v) = \sum_h q_\phi(h \mid v) [\log p_\theta(v, h) - \log q_\phi(h \mid v)]$ is the ELBO. With $v$ drawn uniformly from the data, the wake update is an unbiased estimate of the gradient in $\theta$ of the average ELBO.

*Proof.* By Lemma 1 the update is $\nabla_\theta \log p_\theta(v, h)$. Its expectation is $\sum_h q_\phi(h \mid v) \nabla_\theta \log p_\theta(v, h) = \nabla_\theta \sum_h q_\phi(h \mid v) \log p_\theta(v, h)$, because $q_\phi$ does not depend on $\theta$ and the sum is finite. The entropy term $-\sum_h q_\phi \log q_\phi$ of $\mathcal{L}$ does not depend on $\theta$, so this is $\nabla_\theta \mathcal{L}$. Averaging over the data gives the second claim. $\square$

**Theorem 2 (the sleep phase).** The expected sleep update, with $(h, v) \sim p_\theta$, is $\nabla_\phi S(\phi)$ with

$$S(\phi) = \sum_{v, h} p_\theta(v, h) \log q_\phi(h \mid v) = -\sum_v p_\theta(v)\, \mathrm{KL}\big(p_\theta(\cdot \mid v) \,\|\, q_\phi(\cdot \mid v)\big) + C,$$

where $C = \sum_{v,h} p_\theta(v, h) \log p_\theta(h \mid v)$ does not depend on $\phi$.

*Proof.* By Lemma 1 the update is $\nabla_\phi \log q_\phi(h \mid v)$, and its expectation under $p_\theta$, which does not depend on $\phi$, is $\nabla_\phi S$. For the second form, write $p_\theta(v, h) = p_\theta(v) p_\theta(h \mid v)$ and add and subtract $\log p_\theta(h \mid v)$. $\square$

**Theorem 3 (the ELBO in $\phi$ is a different objective).** For the data distribution $\hat p(v)$, $\mathbb{E}_{\hat p}\, \mathcal{L}(\theta, \phi; v) = \mathbb{E}_{\hat p} \log p_\theta(v) - \mathbb{E}_{\hat p}\, \mathrm{KL}\big(q_\phi(\cdot \mid v) \,\|\, p_\theta(\cdot \mid v)\big)$. So maximizing the ELBO in $\phi$ minimizes $\mathrm{KL}(q \| p)$ averaged over the data, while the sleep phase minimizes $\mathrm{KL}(p \| q)$ averaged over the model's own samples. The two objectives differ in the direction of the divergence and in the distribution of $v$, and in general they have different maximizers.

*Proof.* The identity is the standard decomposition of the ELBO: $\log p_\theta(v, h) = \log p_\theta(v) + \log p_\theta(h \mid v)$, so $\mathcal{L} = \log p_\theta(v) + \sum_h q_\phi \log (p_\theta(h \mid v) / q_\phi(h \mid v))$. That the maximizers differ in general is shown by an instance: for the fixed generative model on the page (the left pair of pixels driven by both hidden units, data of two bars), exact gradient ascent on $S$ and on the average ELBO from $\phi = 0$ reach points where the respective gradients vanish, and the ELBO at the first point, $-3.0847$, is below the ELBO at the second, $-3.0701$. So at the sleep optimum the ELBO gradient in $\phi$ is not zero. $\square$

**Theorem 4 (exact recognition gives the likelihood gradient).** If $q_\phi(h \mid v) = p_\theta(h \mid v)$ for every $v$, then the expected wake update for $v$ is $\nabla_\theta \log p_\theta(v)$, the exact gradient of the log likelihood.

*Proof.* $\nabla_\theta \log p_\theta(v) = \frac{1}{p_\theta(v)} \sum_h \nabla_\theta p_\theta(v, h) = \sum_h \frac{p_\theta(v, h)}{p_\theta(v)} \nabla_\theta \log p_\theta(v, h) = \sum_h p_\theta(h \mid v) \nabla_\theta \log p_\theta(v, h)$, which by Theorem 1 is the expected wake update when $q_\phi = p_\theta(\cdot \mid v)$. $\square$

**Remark.** A factorial $q_\phi$ can rarely equal $p_\theta(h \mid v)$, because explaining away makes the true posterior correlated. Then the wake phase climbs the ELBO in $\theta$ but the sleep phase does not climb it in $\phi$, so the pair of updates is not gradient ascent on the ELBO, and nothing here guarantees that the likelihood increases or that the iteration converges. The page shows a seeded run in which the enumerated log likelihood does increase.
