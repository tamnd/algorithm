---
title: The posterior update, probability matching and the Bayesian regret of Thompson sampling
proves: [correctness]
status: full
---

**Setting.** There are $K$ arms. The mean $\mu_i$ of arm $i$ has the prior $\mathrm{Beta}(a, b)$ with $a, b > 0$, and the means are independent under the prior. Given the means, the rewards are independent, and a pull of arm $i$ pays 1 with probability $\mu_i$ and 0 otherwise. Let $\mathcal{F}_{t-1}$ be the data before round $t$: the pulls $A_1, \ldots, A_{t-1}$ and their rewards. Write $\Pr_{t-1}$ and $\mathbb{E}_{t-1}$ for probability and expectation given $\mathcal{F}_{t-1}$.

**Claim 1 (posterior).** Given $\mathcal{F}_{t-1}$, the means are independent, and $\mu_i$ has the law $\mathrm{Beta}(\alpha_i, \beta_i)$, where $\alpha_i = a + s_i$, $\beta_i = b + f_i$, and $s_i$, $f_i$ are the numbers of successes and failures of arm $i$ in $\mathcal{F}_{t-1}$.

*Proof.* The choice $A_r$ depends only on $\mathcal{F}_{r-1}$ and on fresh random bits of the policy, which do not depend on the means. So the likelihood of the data, as a function of $\mu = (\mu_1, \ldots, \mu_K)$, is

$$L(\mu) = c \prod_{r < t} \mu_{A_r}^{X_r}(1-\mu_{A_r})^{1-X_r} = c \prod_{i=1}^{K} \mu_i^{s_i}(1-\mu_i)^{f_i},$$

where $c$ holds the probabilities of the policy's own choices and does not depend on $\mu$. By [Bayes' theorem](/bayes-theorem/), the posterior density is proportional to the prior density times $L$:

$$\prod_{i=1}^{K} \mu_i^{a-1}(1-\mu_i)^{b-1} \cdot \mu_i^{s_i}(1-\mu_i)^{f_i} = \prod_{i=1}^{K} \mu_i^{\alpha_i - 1}(1-\mu_i)^{\beta_i - 1}.$$

This is a product of $\mathrm{Beta}(\alpha_i, \beta_i)$ densities, up to a constant. So the means are independent given the data, with those laws. Lines L1 and L6 keep exactly these counts, by induction on $t$. $\blacksquare$

**Claim 2 (probability matching).** Let $A^* = \arg\max_i \mu_i$, with ties broken as in line L4. Then $\Pr_{t-1}[A_t = i] = \Pr_{t-1}[A^* = i]$ for each $i$.

*Proof.* Line L3 draws $\theta_i \sim \mathrm{Beta}(\alpha_i, \beta_i)$ independently. By Claim 1, given $\mathcal{F}_{t-1}$, the vector $\theta$ has the same law as the vector $\mu$. Line L4 applies to $\theta$ the same map $\arg\max$ that defines $A^*$ from $\mu$. So $A_t$ and $A^*$ have the same law given $\mathcal{F}_{t-1}$. $\blacksquare$

**Claim 3 (Bayesian regret).** Let $\mathrm{BR}_n = \mathbb{E}\big[\sum_{t=1}^n (\mu_{A^*} - \mu_{A_t})\big]$, where the expectation is over the prior, the rewards and the policy. For $n \ge 2$,

$$\mathrm{BR}_n \le K + 4\sqrt{2Kn\ln n} + \frac{4K}{n^2}.$$

*Proof.* This follows Lattimore and Szepesvari, Theorem 36.1, with explicit constants for rewards in $[0,1]$.

*Step 1 (an upper confidence bound).* For each round $t$ and arm $i$, let $N = T_i(t-1)$ and let

$$U_t(i) = \min\Big(1,\ \hat\mu_i + \sqrt{2\ln n / N}\Big) \text{ if } N \ge 1, \qquad U_t(i) = 1 \text{ if } N = 0,$$

where $\hat\mu_i$ is the mean reward of arm $i$ in $\mathcal{F}_{t-1}$. Then $U_t(i)$ is a function of $\mathcal{F}_{t-1}$.

*Step 2 (the key identity).* Since $U_t$ is fixed given $\mathcal{F}_{t-1}$, Claim 2 gives

$$\mathbb{E}_{t-1}[U_t(A^*)] = \sum_i \Pr_{t-1}[A^* = i]\,U_t(i) = \sum_i \Pr_{t-1}[A_t = i]\,U_t(i) = \mathbb{E}_{t-1}[U_t(A_t)].$$

Take expectations, and add and subtract $U_t$ in each term of $\mathrm{BR}_n$:

$$\mathrm{BR}_n = \sum_{t=1}^{n}\mathbb{E}[\mu_{A^*} - U_t(A^*)] + \sum_{t=1}^{n}\mathbb{E}[U_t(A_t) - \mu_{A_t}].$$

*Step 3 (a good event).* Use the reward table model: for each arm $i$, the rewards of its pulls are the first terms of an i.i.d. sequence $Y_{i,1}, Y_{i,2}, \ldots$ with mean $\mu_i$, and $\hat\mu_{i,s}$ is the mean of the first $s$ terms. Let $G$ be the event that $|\hat\mu_{i,s} - \mu_i| < \sqrt{2\ln n / s}$ for all $i \le K$ and $s \le n$. Given the means, the [Hoeffding inequality](/hoeffding-inequality/) gives, for each $i$ and $s$, probability at most $2e^{-2s \cdot 2\ln n / s} = 2n^{-4}$ for the opposite. A [union bound](/union-bound/) over $Kn$ pairs gives $\Pr[G^c] \le 2Kn^{-3}$, for each value of the means, so also under the prior.

*Step 4 (off the good event).* Each term $\mu_{A^*} - U_t(A^*)$ and $U_t(A_t) - \mu_{A_t}$ is in $[-1, 1]$, so the part of the two sums on $G^c$ is at most $2n\Pr[G^c] \le 4Kn^{-2}$.

*Step 5 (the first sum on $G$).* On $G$, $U_t(i) \ge \mu_i$ for all $t$ and $i$: if $N = 0$ then $U_t(i) = 1 \ge \mu_i$, and if $N \ge 1$ then $\hat\mu_i + \sqrt{2\ln n/N} > \mu_i$ and $1 \ge \mu_i$. So each term $\mu_{A^*} - U_t(A^*)$ is at most 0 on $G$.

*Step 6 (the second sum on $G$).* On $G$, if $N = T_{A_t}(t-1) \ge 1$ then $U_t(A_t) - \mu_{A_t} \le \hat\mu_{A_t} + \sqrt{2\ln n/N} - \mu_{A_t} < 2\sqrt{2\ln n / N}$, and if $N = 0$ the term is at most 1. Group the rounds by the arm pulled. Arm $i$ is pulled with $N = 0, 1, \ldots, T_i(n) - 1$, so

$$\sum_{t=1}^{n}(U_t(A_t) - \mu_{A_t}) \le \sum_{i=1}^{K}\Big(1 + \sum_{s=1}^{T_i(n)-1} 2\sqrt{\frac{2\ln n}{s}}\Big) \le K + 4\sqrt{2\ln n}\sum_{i=1}^{K}\sqrt{T_i(n)},$$

using $\sum_{s=1}^{m} s^{-1/2} \le 2\sqrt{m}$. By the Cauchy-Schwarz inequality, $\sum_i \sqrt{T_i(n)} \le \sqrt{K\sum_i T_i(n)} = \sqrt{Kn}$.

*Step 7.* Add Steps 4, 5 and 6. $\blacksquare$

**Remarks.**

- Claim 3 averages over the prior. It does not bound the regret for a fixed set of means, which is the frequentist question.
- The frequentist bounds are longer. Agrawal and Goyal (COLT 2012, Theorems 1 and 2) bound the regret for fixed Bernoulli means by $O(\ln n/\Delta + 1/\Delta^3)$ for two arms and by $O\big((\sum_{i:\Delta_i>0}\Delta_i^{-2})^2\ln n\big)$ for $K$ arms. Kaufmann, Korda and Munos (ALT 2012, Theorem 1) show that with the uniform prior, $\mathbb{E}[T_i(n)] \le (1+\varepsilon)\ln n/\mathrm{kl}(\mu_i, \mu^*) + o(\ln n)$ for each $\varepsilon > 0$. Lattimore and Szepesvari (Theorem 36.2) give a general tool for such proofs: a bound on $\mathbb{E}[T_i(n)]$ in terms of the chance that the sample of the best arm is nearly optimistic and the chance that the sample of arm $i$ is large.
- The proof of Claim 3 never uses the Beta form. It holds for any prior and any reward law on $[0,1]$, as long as the policy samples from the true posterior.
