---
title: "Temperature sampling draws from softmax(z / T), its entropy grows with T, and its limits are greedy and uniform"
proves: [correctness]
status: full
---

We use the notation of the page. The logits are $z_1, \ldots, z_n$, with at least one finite value; a logit of $-\infty$ marks a token that is not allowed. The temperature is $T > 0$, and we write $\beta = 1 / T$. The distribution is

$$q_T(i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}},$$

with $e^{-\infty} = 0$. All logs are natural logs.

**Lemma 1 (the draw).** TEMPERATURE-SAMPLE returns each token $i$ with probability $q_T(i)$, and never returns a token with $z_i = -\infty$.

*Proof.* Let $m = \max_i z_i$ (line L1), which is finite. Line L2 computes $w_i = e^{(z_i - m)/T} = e^{z_i / T} e^{-m/T}$, so the $w_i$ are the numerators of $q_T$ times the same positive constant, and $w_i / \sum_j w_j = q_T(i)$. Each $w_i$ lies in $[0, 1]$, so no exponential overflows, and the token of largest logit has $w_i = 1$, so the sum $Z$ of line L3 is at least 1. Lines L4 and L5 are inverse transform sampling with $r = uZ$ uniform on $[0, Z)$: the walk returns $i$ when $r$ falls in an interval of length $w_i$, which happens with probability $w_i / Z = q_T(i)$. A token with $z_i = -\infty$ has $w_i = 0$ and an empty interval. $\square$

**Lemma 2 (the power form).** Let $p = q_1$ be the distribution at $T = 1$. Then $q_T(i) = p_i^{1/T} / \sum_j p_j^{1/T}$.

*Proof.* $p_i = e^{z_i} / S$ with $S = \sum_j e^{z_j}$, so $p_i^{1/T} = e^{z_i / T} S^{-1/T}$. The factor $S^{-1/T}$ is the same for all $i$ and cancels in the ratio. $\square$

**Lemma 3 (shift).** Adding the same constant $c$ to every logit does not change $q_T$.

*Proof.* Every numerator and the denominator are multiplied by $e^{c/T}$. $\square$

**Theorem 4 (the entropy grows with the temperature).** Let $H(T)$ be the entropy of $q_T$. Then $H$ does not decrease in $T$, and it is strictly increasing unless all the finite logits are equal.

*Proof.* Restrict to the tokens of finite logit; the others have probability 0 at every $T$. Write $q_\beta(i) = e^{\beta z_i} / A(\beta)$ with $A(\beta) = \sum_j e^{\beta z_j}$. Then

$$H = -\sum_i q_\beta(i) (\beta z_i - \log A(\beta)) = \log A(\beta) - \beta \, \mathbb{E}_\beta[z],$$

where $\mathbb{E}_\beta$ is the mean under $q_\beta$. Since $\frac{d}{d\beta} \log A(\beta) = \mathbb{E}_\beta[z]$ and $\frac{d}{d\beta} \mathbb{E}_\beta[z] = \operatorname{Var}_\beta(z)$,

$$\frac{dH}{d\beta} = \mathbb{E}_\beta[z] - \mathbb{E}_\beta[z] - \beta \operatorname{Var}_\beta(z) = -\beta \operatorname{Var}_\beta(z) \le 0.$$

So $H$ does not increase in $\beta$, and since $\beta = 1/T$ decreases as $T$ grows, $H$ does not decrease in $T$. The variance is 0 only when $z$ is constant on the support, which is the case where $q_T$ is uniform for every $T$; otherwise it is positive for every $\beta > 0$ and $H$ is strictly increasing in $T$. $\square$

The family $q_\beta$ is an [exponential family](/exponential-family-distribution/) with the logits as the sufficient statistic, and Theorem 4 is the standard fact that the derivative of its mean is its variance.

**Theorem 5 (the limits).** Let $M = \{i : z_i = m\}$ and $F = \{i : z_i > -\infty\}$. As $T \to 0$, $q_T$ tends to the uniform distribution on $M$. As $T \to \infty$, $q_T$ tends to the uniform distribution on $F$.

*Proof.* Use the weights $w_i = e^{(z_i - m)/T}$ of Lemma 1. For $i \in M$, $w_i = 1$ at every $T$. For $i \notin M$ with $z_i$ finite, $z_i - m < 0$ and $w_i \to 0$ as $T \to 0$. So $Z \to |M|$ and $q_T(i) \to 1/|M|$ on $M$ and 0 elsewhere. As $T \to \infty$, $w_i \to e^0 = 1$ for every $i \in F$ and $w_i = 0$ outside $F$, so $q_T(i) \to 1/|F|$ on $F$. $\square$

So a small temperature gives the argmax of [greedy decoding](/greedy-decoding/) when the largest logit is unique, and a uniform choice among the tied tokens otherwise; a large temperature gives the uniform distribution over the allowed tokens, whatever the model says. The tests check Lemma 1 by sampling and by a second method, the [Gumbel-max trick](/gumbel-max-trick/), Lemma 2 and Lemma 3 numerically, Theorem 4 on a fine grid of temperatures, and Theorem 5 at $T = 0.01$ and $T = 10^6$.
