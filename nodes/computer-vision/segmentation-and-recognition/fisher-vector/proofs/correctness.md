---
title: The Fisher vector lines compute the log-likelihood gradient whitened by the exact Fisher information of the hard-assignment model
proves: [correctness]
status: full
---

We use the notation of the page. The mixture density is $u(x) = \sum_{k=1}^{K} w_k\, \mathcal{N}(x; \mu_k, \sigma_k)$ on $\mathbb{R}^D$ with diagonal covariances, where
$$\log \mathcal{N}(x; \mu_k, \sigma_k) = -\frac12 \sum_{i=1}^{D} \Big[ \log(2\pi) + 2 \log \sigma_{k,i} + \frac{(x_i - \mu_{k,i})^2}{\sigma_{k,i}^2} \Big].$$
The weights are $w_k = e^{\alpha_k} / \sum_j e^{\alpha_j}$. The posterior is $\gamma_x(k) = w_k \mathcal{N}(x; \mu_k, \sigma_k)/u(x)$, so $\sum_k \gamma_x(k) = 1$. We write $r_{k,i}(x) = (x_i - \mu_{k,i})/\sigma_{k,i}$.

## Part 1: the gradients

**Lemma 1.** For one descriptor $x$,
$$\frac{\partial \log u(x)}{\partial \alpha_k} = \gamma_x(k) - w_k, \qquad \frac{\partial \log u(x)}{\partial \mu_{k,i}} = \gamma_x(k) \frac{r_{k,i}(x)}{\sigma_{k,i}}, \qquad \frac{\partial \log u(x)}{\partial \sigma_{k,i}} = \gamma_x(k) \frac{r_{k,i}(x)^2 - 1}{\sigma_{k,i}}.$$

*Proof.* Let $p_k = \mathcal{N}(x; \mu_k, \sigma_k)$. For a parameter $\theta$ of component $k$ only, $\partial_\theta \log u = \frac{w_k \partial_\theta p_k}{u} = \frac{w_k p_k}{u} \partial_\theta \log p_k = \gamma_x(k)\, \partial_\theta \log p_k$. From the formula for $\log p_k$, $\partial \log p_k / \partial \mu_{k,i} = (x_i - \mu_{k,i})/\sigma_{k,i}^2 = r_{k,i}/\sigma_{k,i}$ and $\partial \log p_k / \partial \sigma_{k,i} = -1/\sigma_{k,i} + (x_i - \mu_{k,i})^2/\sigma_{k,i}^3 = (r_{k,i}^2 - 1)/\sigma_{k,i}$. For the weights, $\partial w_j / \partial \alpha_k = w_j(\delta_{jk} - w_k)$, so $\partial_{\alpha_k} \log u = \frac{1}{u} \sum_j p_j w_j (\delta_{jk} - w_k) = \gamma_x(k) - w_k \sum_j \gamma_x(j) = \gamma_x(k) - w_k$. $\square$

These are the formulas of Sanchez et al. (2013, Section 2.2). The gradient of the average $\frac1n \sum_t \log u(x_t)$ is the average of these terms.

**Lemma 2 (the loop).** After lines L1 to L4, $S_{0,k} = \sum_t \gamma_t(k)$, $S_{1,k,i} = \sum_t \gamma_t(k) r_{k,i}(x_t)$ and $S_{2,k,i} = \sum_t \gamma_t(k) (r_{k,i}(x_t)^2 - 1)$.

*Proof.* Line L1 sets the sums to 0, and each pass of the loop adds the term of one descriptor, computed in line L3 and line L4 from the definitions. By induction over the passes the sums hold the stated values. $\square$

**Corollary 1.** Lines L5 to L7 give
$$\mathcal{G}_{\alpha_k} = \frac{1}{\sqrt{w_k}} \cdot \frac1n \sum_t \frac{\partial \log u(x_t)}{\partial \alpha_k}, \quad \mathcal{G}_{\mu_{k,i}} = \frac{\sigma_{k,i}}{\sqrt{w_k}} \cdot \frac1n \sum_t \frac{\partial \log u(x_t)}{\partial \mu_{k,i}}, \quad \mathcal{G}_{\sigma_{k,i}} = \frac{\sigma_{k,i}}{\sqrt{2 w_k}} \cdot \frac1n \sum_t \frac{\partial \log u(x_t)}{\partial \sigma_{k,i}}.$$

*Proof.* By Lemma 2, $S_{0,k} - n w_k = \sum_t (\gamma_t(k) - w_k)$, $S_{1,k,i} = \sigma_{k,i} \sum_t \gamma_t(k) r_{k,i}/\sigma_{k,i}$ and $S_{2,k,i} = \sigma_{k,i} \sum_t \gamma_t(k)(r_{k,i}^2 - 1)/\sigma_{k,i}$. Compare with Lemma 1 and divide by the factors of lines L5 to L7. $\square$

So the vector is the average gradient with each coordinate multiplied by a positive factor. Part 2 shows that these factors are the inverse square roots of the Fisher information under the stated assumption.

## Part 2: the Fisher information under hard assignment

The Fisher information is $F = \mathbb{E}_{x \sim u}[g(x) g(x)^\top]$, with $g = \nabla_\lambda \log u$. It is hard to compute exactly for a mixture. Sanchez et al. (Appendix A) assume that the posterior of each $x$ drawn from $u$ is sharply peaked. We state this as an exact assumption.

**Assumption H.** Let $c$ be the component that generated $x$ (so $\Pr[c = k] = w_k$ and $x \mid c = k \sim \mathcal{N}(\mu_k, \sigma_k)$). Then $\gamma_x(k) = [c = k]$ for all $k$, with probability 1.

This holds in the limit of components whose means move apart while the variances stay fixed. It is also exactly the Fisher information of the complete-data model in which the component label is observed.

**Theorem 1.** Under Assumption H, the Fisher information $F$ in the parameters $(\alpha, \mu, \sigma)$ is block diagonal with
1. $\mathbb{E}[g_{\mu_{k,i}}^2] = w_k / \sigma_{k,i}^2$,
2. $\mathbb{E}[g_{\sigma_{k,i}}^2] = 2 w_k / \sigma_{k,i}^2$,
3. the block of $\alpha$ equal to $\mathrm{diag}(w) - w w^\top$,
and every other entry 0.

*Proof.* Under H, $g_{\mu_{k,i}} = [c = k]\, r_{k,i}/\sigma_{k,i}$ and $g_{\sigma_{k,i}} = [c = k] (r_{k,i}^2 - 1)/\sigma_{k,i}$. Given $c = k$, the variables $r_{k,1}, \ldots, r_{k,D}$ are independent standard normal, so $\mathbb{E}[r] = 0$, $\mathbb{E}[r^2] = 1$, $\mathbb{E}[r^3] = 0$ and $\mathbb{E}[r^4] = 3$.

Item 1: $\mathbb{E}[g_{\mu_{k,i}}^2] = w_k \mathbb{E}[r^2]/\sigma_{k,i}^2 = w_k/\sigma_{k,i}^2$. Item 2: $\mathbb{E}[(r^2 - 1)^2] = \mathbb{E}[r^4] - 2\mathbb{E}[r^2] + 1 = 2$, so $\mathbb{E}[g_{\sigma_{k,i}}^2] = 2 w_k / \sigma_{k,i}^2$. Item 3: $g_\alpha = e_c - w$, where $e_c$ is the one-hot vector of $c$, so $\mathbb{E}[g_\alpha g_\alpha^\top] = \mathrm{Cov}(e_c) = \mathrm{diag}(w) - w w^\top$.

Off-diagonal entries. A product of a term of component $k$ and a term of component $j \ne k$ contains $[c = k][c = j] = 0$. Inside one component, for $i \ne l$: $\mathbb{E}[r_i r_l] = 0$, $\mathbb{E}[r_i (r_l^2 - 1)] = 0$ and $\mathbb{E}[(r_i^2 - 1)(r_l^2 - 1)] = 0$ by independence, and for the same $i$: $\mathbb{E}[r (r^2 - 1)] = \mathbb{E}[r^3] - \mathbb{E}[r] = 0$. Between $\alpha$ and the component terms: $\mathbb{E}[([c = j] - w_j)[c = k]\, r] = \mathbb{E}[([c=j] - w_j)[c=k]]\, \mathbb{E}[r \mid c = k] = 0$, and in the same way with $r^2 - 1$, whose conditional mean is 0. $\square$

**Corollary 2 (the normalizers).** Under Assumption H, the mean and sigma part of $F^{-1/2} \frac1n \sum_t g(x_t)$ is exactly what lines L6 and L7 compute: the factors $\sigma_{k,i}/\sqrt{w_k}$ and $\sigma_{k,i}/\sqrt{2 w_k}$ are $(w_k/\sigma_{k,i}^2)^{-1/2}$ and $(2 w_k / \sigma_{k,i}^2)^{-1/2}$. For a single descriptor ($n = 1$) each of these normalized entries has mean 0 and variance 1 under $u$.

*Proof.* The inverse square root of a positive diagonal block is the diagonal of the inverse square roots; Corollary 1 gives the factors. For the moments: $\mathbb{E}[g] = 0$ because each component term has a factor $r$ or $r^2 - 1$ with conditional mean 0, and the variance is the diagonal entry times the square of the factor, which is 1. $\square$

**The weight part.** The block $\mathrm{diag}(w) - w w^\top$ has the null vector $(1, \ldots, 1)$, because the soft-max parameters are defined only up to a common shift. It has no inverse. Line L5 uses $1/\sqrt{w_k}$, the inverse square root of the diagonal $\mathrm{diag}(w)$ alone, as Sanchez et al. do (Eq. 16). With this factor a normalized weight entry of one descriptor has variance $(w_k - w_k^2)/w_k = 1 - w_k$, not 1. The tests check this value.

**Without Assumption H.** When components overlap, $\gamma_x(k)$ is strictly between 0 and 1, and the entries of Theorem 1 change; the off-diagonal entries are no longer 0. Then lines L5 to L7 are the diagonal approximation of Sanchez et al., not the exact whitening. Lemma 1, Lemma 2 and Corollary 1 hold without the assumption.

## Part 3: the normalization steps

Line L9 maps each entry $t$ to $\mathrm{sign}(t)|t|^\rho$, which is zero exactly when $t = 0$ and keeps the sign. Line L10 divides a nonzero vector by its norm, so the output has norm 1 or is zero. The result is a function of the multiset $X$ only, since every statistic of Lemma 2 is a sum over $X$.

**What is not claimed.** That the Fisher vector classifies or ranks images well is a benchmark result, not a consequence of these facts.
