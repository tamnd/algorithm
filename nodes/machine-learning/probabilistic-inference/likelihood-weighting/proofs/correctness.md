---
title: Likelihood weighting is unbiased for P(e) and consistent for the posterior
proves: [correctness]
status: full
---

Number the variables in the order $\pi$ of line L1, so that each parent of $X_i$ has an index less than $i$. Let $E$ be the set of observed variables with the values $e$, and let $Z$ be the other variables. For an assignment $z$ of $Z$, write $x = (z, e)$ and $f_i(x) = P(x_i \mid x_{\mathrm{Pa}(i)})$.

**Lemma 1 (the sampling distribution).** One pass of lines L4 to L8 returns $z$ with the probability
$$q(z) = \prod_{X_i \in Z} f_i(x),$$
and $q$ is a probability distribution on the assignments of $Z$.

*Proof.* The loop visits $X_1, \ldots, X_m$ in order. At an observed $X_i$, line L7 sets a fixed value and uses no randomness. At a free $X_i$, line L8 draws $x_i$ with probability $f_i(x)$, given the values set before, which include the parents. Multiplying these conditional probabilities over the free variables gives $q(z)$. To see that $q$ sums to 1, sum out the free variables in the reverse order of $\pi$: the last free variable occurs only in its own factor, because no later free variable has it as a parent and the factors of the observed variables are not part of $q$, and each row sums to 1. $\square$

**Lemma 2 (the weight).** The weight after line L8 is $w(z) = \prod_{X_i \in E} f_i(x)$, and $q(z)\, w(z) = P(z, e)$.

*Proof.* Line L4 sets $w = 1$. Line L7 multiplies $w$ by $f_i(x)$ at each observed $X_i$, and the parent values are set because they come earlier. Nothing else changes $w$. The product $q(z) w(z)$ is the product of $f_i(x)$ over all $i$, which is the joint $P(x) = P(z, e)$ by the factorization of the network. $\square$

**Theorem 1 (unbiased estimates).** Let $(z_t, w_t)$ for $t = 1, \ldots, s$ be the samples and their weights. Then for every $s \ge 1$,
$$\mathbb{E}\Big[\frac{1}{s} \sum_t w_t\Big] = P(e), \qquad \mathbb{E}\Big[\frac{1}{s} \sum_t w_t [x_{t,Q} = q]\Big] = P(Q = q, e).$$

*Proof.* The samples are i.i.d. with the distribution $q$, by Lemma 1 and the fresh uniform numbers of each pass. By linearity it suffices to take one sample. By Lemma 2, $\mathbb{E}_q[w] = \sum_z q(z) w(z) = \sum_z P(z, e) = P(e)$, and $\mathbb{E}_q[w\,[x_Q = q]] = \sum_{z : z_Q = q} P(z, e) = P(Q = q, e)$. $\square$

**Theorem 2 (consistency).** If $P(e) > 0$, then the estimate $W[q] / \sum_{q'} W[q']$ of line L10 converges to $P(Q = q \mid e)$ almost surely as $s \to \infty$.

*Proof.* The weights are bounded: $0 \le w \le 1$, since each factor is a probability. So the strong law of large numbers applies to both averages of Theorem 1: $\frac1s \sum_t w_t \to P(e)$ and $\frac1s \sum_t w_t [x_{t,Q} = q] \to P(q, e)$ almost surely. The estimate of line L10 is the ratio of the second average to the first. Because $P(e) > 0$, the denominator is positive for all large $s$ on this event, and the ratio converges to $P(q, e) / P(e) = P(q \mid e)$ by the continuity of division away from 0. $\square$

**Support.** The proposal $q$ is positive at each $z$ with $P(z, e) > 0$: if $P(z, e) > 0$ then each factor $f_i(x)$ is positive, so $q(z) > 0$. This is the condition that importance sampling needs. A $z$ with $q(z) > 0$ and $P(z, e) = 0$ gets $w = 0$ and adds nothing.

**The estimate is biased.** The ratio of two unbiased estimates need not be unbiased. For $s = 1$ the weight cancels, the estimate is $[x_{1,Q} = q]$, and its mean is $q(Q = q)$, the probability under the mutilated network. In the sprinkler network with the evidence $W = 1$, this is $0.5$, while $P(R = 1 \mid W = 1) = 509/719$.
