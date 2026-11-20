---
title: The multifidelity estimator is unbiased and its allocation minimizes the variance at a fixed cost
proves: [correctness]
status: full
---

We assume exact arithmetic and exact random numbers. The models $f_1, \ldots, f_k$ are square integrable functions of one random input $z$. Let $\sigma_i^2 = \mathrm{Var}(f_i(z))$, $\rho_i = \mathrm{Corr}(f_1(z), f_i(z))$ with $\rho_1 = 1$ and $\rho_{k+1} = 0$, and let $w_i > 0$ be the cost of one run of model $i$. The sample counts are integers or reals with $1 \le m_1 \le m_2 \le \cdots \le m_k$. For independent draws $z_1, \ldots, z_{m_k}$ and $m \le m_k$ write $\bar{f}_i^{(m)} = \frac{1}{m} \sum_{j=1}^{m} f_i(z_j)$, the mean over the first $m$ draws. The estimator is

$$\widehat{s} = \bar{f}_1^{(m_1)} + \sum_{i=2}^{k} \alpha_i \big(\bar{f}_i^{(m_i)} - \bar{f}_i^{(m_{i-1})}\big).$$

The weights $\alpha_i$ and the counts $m_i$ are fixed before the draws. In the algorithm they come from a pilot run with its own draws, so they are independent of $z_1, \ldots, z_{m_k}$, and the statements below hold conditionally on the pilot.

**Lemma 1 (unbiased).** $\mathbb{E}[\widehat{s}] = \mathbb{E}[f_1(z)]$ for all weights and counts.

*Proof.* Both means of $f_i$ in a correction have the mean $\mathbb{E}[f_i(z)]$, so each correction has mean zero. $\square$

**Lemma 2 (covariance of nested means).** $\mathrm{Cov}(\bar{f}_i^{(m)}, \bar{f}_j^{(n)}) = \mathrm{Cov}(f_i, f_j) / \max(m, n)$.

*Proof.* Only the pairs with the same draw are correlated, and there are $\min(m, n)$ of them. So the covariance is $\min(m, n)\, \mathrm{Cov}(f_i, f_j) / (m n) = \mathrm{Cov}(f_i, f_j) / \max(m, n)$. $\square$

**Lemma 3 (the variance).** With $\Delta_i = 1/m_{i-1} - 1/m_i \ge 0$,

$$\mathrm{Var}(\widehat{s}) = \frac{\sigma_1^2}{m_1} + \sum_{i=2}^{k} \Delta_i \big(\alpha_i^2 \sigma_i^2 - 2 \alpha_i \rho_i \sigma_1 \sigma_i\big).$$

*Proof.* Let $D_i = \bar{f}_i^{(m_i)} - \bar{f}_i^{(m_{i-1})}$. By Lemma 2, $\mathrm{Var}(D_i) = \sigma_i^2 (1/m_i + 1/m_{i-1} - 2/m_i) = \sigma_i^2 \Delta_i$. The covariance of $\bar{f}_1^{(m_1)}$ with $D_i$ is $\rho_i \sigma_1 \sigma_i (1/m_i - 1/m_{i-1}) = -\rho_i \sigma_1 \sigma_i \Delta_i$, because $m_1 \le m_{i-1} \le m_i$. For $2 \le i < j$, the four terms of $\mathrm{Cov}(D_i, D_j)$ have the maxima $m_j, m_{j-1}, m_j, m_{j-1}$ with signs $+, -, -, +$, because $m_{i-1} \le m_i \le m_{j-1} \le m_j$, so $\mathrm{Cov}(D_i, D_j) = 0$. Adding the variances and twice the covariances gives the formula. $\square$

**Lemma 4 (the best weights).** For fixed counts with $\Delta_i > 0$, the variance is smallest at $\alpha_i = \rho_i \sigma_1 / \sigma_i$, and then

$$\mathrm{Var}(\widehat{s}) = \sigma_1^2 \sum_{i=1}^{k} \frac{\rho_i^2 - \rho_{i+1}^2}{m_i}.$$

*Proof.* The term of $\alpha_i$ is the quadratic $\Delta_i (\alpha_i^2 \sigma_i^2 - 2 \alpha_i \rho_i \sigma_1 \sigma_i)$, with its minimum $-\Delta_i \rho_i^2 \sigma_1^2$ at $\alpha_i = \rho_i \sigma_1 / \sigma_i$. So the variance is $\sigma_1^2 \big(1/m_1 - \sum_{i \ge 2} \rho_i^2 (1/m_{i-1} - 1/m_i)\big)$. Collect the factor of each $1/m_i$: it is $1 - \rho_2^2$ for $i = 1$, $\rho_i^2 - \rho_{i+1}^2$ for $2 \le i < k$, and $\rho_k^2$ for $i = k$. With $\rho_1 = 1$ and $\rho_{k+1} = 0$ this is the formula. $\square$

**Theorem (optimal allocation).** Assume $|\rho_1| > |\rho_2| > \cdots > |\rho_k|$ and

$$\frac{w_{i-1}}{w_i} > \frac{\rho_{i-1}^2 - \rho_i^2}{\rho_i^2 - \rho_{i+1}^2}, \qquad i = 2, \ldots, k.$$

Among all real counts with $m_1 \le \cdots \le m_k$ and cost $\sum_i w_i m_i = p$, and all weights, the smallest variance is $\frac{\sigma_1^2}{p} \big(\sum_{i=1}^{k} \sqrt{w_i (\rho_i^2 - \rho_{i+1}^2)}\big)^2$. It is reached by $\alpha_i = \rho_i \sigma_1 / \sigma_i$ and $m_i = m_1 r_i$ with

$$r_i = \sqrt{\frac{w_1 (\rho_i^2 - \rho_{i+1}^2)}{w_i (1 - \rho_2^2)}}, \qquad m_1 = \frac{p}{\sum_i w_i r_i}.$$

*Proof.* Let $a_i = \rho_i^2 - \rho_{i+1}^2$, which is positive by the first assumption. For every admissible choice of counts, Lemma 3 and Lemma 4 give $\mathrm{Var}(\widehat{s}) \ge \sigma_1^2 \sum_i a_i / m_i$: if $\Delta_i > 0$ this is Lemma 4, and if $\Delta_i = 0$ the term of $\alpha_i$ is zero, which is also the value of the minimum in Lemma 4. By the Cauchy-Schwarz inequality,

$$\Big(\sum_i \sqrt{a_i w_i}\Big)^2 = \Big(\sum_i \sqrt{a_i / m_i}\, \sqrt{w_i m_i}\Big)^2 \le \Big(\sum_i \frac{a_i}{m_i}\Big) \Big(\sum_i w_i m_i\Big) = p \sum_i \frac{a_i}{m_i},$$

so every admissible choice has variance at least the stated value. Equality holds when $w_i m_i$ is a fixed multiple of $a_i / m_i$, that is $m_i \propto \sqrt{a_i / w_i}$, which is $m_i = m_1 r_i$, and the cost constraint fixes $m_1$. It remains to show that these counts are admissible: $m_{i-1} < m_i$ holds if and only if $a_{i-1} / w_{i-1} < a_i / w_i$, which is the second assumption. Then $\Delta_i > 0$ and Lemma 4 gives the weights. $\blacksquare$

**Corollary (the gain over plain Monte Carlo).** Plain Monte Carlo with the budget $p$ uses $p / w_1$ runs of $f_1$ and has the variance $\sigma_1^2 w_1 / p$. The ratio of the optimal multifidelity variance to it is

$$\Big(\sum_{i=1}^{k} \sqrt{\frac{w_i}{w_1} (\rho_i^2 - \rho_{i+1}^2)}\Big)^2.$$

The assumptions of the theorem do not make this ratio smaller than 1. For $k = 2$, $\rho_2^2 = 0.01$ and $w_2 = w_1 / 100$, the cost condition holds ($100 > 99$), but the ratio is $(\sqrt{0.99} + \sqrt{0.0001})^2 = 1.0100$. So the ratio is a separate test: use the cheap model only when the ratio is below 1.

**The algorithm.** Line L1 estimates $\sigma_i$ and $\rho_i$ from pilot runs. Line L2 tests the two assumptions and stops if they fail; then a model must be removed or reordered. Lines L3 to L5 compute $r_i$, $m_1$ and $\alpha_i$ by the theorem. The code rounds the counts down, keeps them in order and keeps $m_1 \ge 2$. Lines L6 to L9 compute $\widehat{s}$ with nested draws. By Lemma 1 the result is unbiased for any counts and weights, and Lemma 3 gives its variance for the rounded counts.

**What is not proved.** With estimated $\sigma_i$ and $\rho_i$, the counts and weights are near the optimum, not at it. The variance formula of the theorem then holds with the true statistics in Lemma 3 and the used weights, and it can be larger than the stated minimum. If the pilot runs are also used in the estimate, the weights depend on the samples and Lemma 1 holds only approximately. The estimator gives the mean of $f_1$; the error of $f_1$ against the real system is a modeling error outside the method.
