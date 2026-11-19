---
title: Katz backoff gives every history a distribution over the vocabulary, and its discounts take away exactly N_1 counts
proves: [correctness]
status: full
---

Fix the padded training text and the vocabulary $V$, the set of predicted training tokens. For a history $h$, $c(h w)$ is the number of times $h$ is followed by $w$, $c(h) = \sum_w c(h w)$, $S(h) = \{w : c(h w) > 0\}$, and $h'$ is $h$ without its first token. For an order $m$ and $1 \le r$, $d_r \in (0, 1]$ is the discount ratio of the m-grams seen $r$ times, with $d_r = 1$ for $r > k$ or when the order is left undiscounted. If $S(h) = V$, the history keeps its undiscounted estimates: we then write $d = 1$ for all its words and $\alpha(h) = 0$, as the implementation does.

**Lemma 1 (the discounted mass).** Let $N_r$ be the number of m-grams seen $r$ times, with $N_1 > 0$ and $\mu = (k+1) N_{k+1}/N_1 < 1$. For each $1 \le r \le k$ with $N_r > 0$ let $r^* = (r+1) N_{r+1}/N_r$ and $d_r = (r^*/r - \mu)/(1 - \mu)$, and assume that all these $d_r$ lie in $(0, 1]$, which is the test that the implementation makes before it uses them. Then $N_r > 0$ for every $1 \le r \le k + 1$, and

$$\sum_{r=1}^{k} N_r \, r \, (1 - d_r) = N_1 .$$

*Proof.* First, the counts of counts have no gap up to $k + 1$. Suppose $N_r > 0$ for some $r \le k$. If $N_{r+1} = 0$, then $r^* = 0$ and $d_r = -\mu/(1 - \mu) \le 0$, which is not in $(0, 1]$. So $N_{r+1} > 0$. Since $N_1 > 0$, induction on $r$ gives $N_r > 0$ for $r = 1, 2, \ldots, k + 1$.

Next, $1 - d_r = (1 - r^*/r)/(1 - \mu)$, so

$$N_r \, r \, (1 - d_r) = \frac{r N_r - N_r r^*}{1 - \mu} = \frac{r N_r - (r+1) N_{r+1}}{1 - \mu}.$$

Summed over $r = 1, \ldots, k$, the numerators telescope to $N_1 - (k+1) N_{k+1} = N_1 (1 - \mu)$, and dividing by $1 - \mu$ gives $N_1$. $\square$

**Theorem 2 (a proper distribution).** For every history $h$, $P_{K}(w \mid h) \ge 0$ for $w \in V$ and $\sum_{w \in V} P_K(w \mid h) = 1$. If $c(h w) > 0$, then $P_K(w \mid h) > 0$.

*Proof.* By induction on the length of $h$.

*Length 0.* Line L1 gives $c(w)/N \ge 0$, and $\sum_{w \in V} c(w) = N$ because $V$ is the set of predicted tokens. If $c(w) > 0$ the value is positive.

*Length $\ell \ge 1$, $c(h) = 0$.* Line L2 returns the row of $h'$, which has the properties by the induction hypothesis. No $w$ has $c(h w) > 0$.

*Length $\ell \ge 1$, $c(h) > 0$, $S(h) = V$.* Every word gets $c(h w)/c(h)$, and these sum to 1.

*Length $\ell \ge 1$, $c(h) > 0$, $S(h) \ne V$.* For $w \in S(h)$, line L4 gives $d_{c(h w)} c(h w)/c(h) > 0$, since $d > 0$. Line L5 gives $\beta(h) = 1 - \sum_{v \in S(h)} d_{c(h v)} c(h v)/c(h) \ge 1 - \sum_{v \in S(h)} c(h v)/c(h) = 0$, since $d \le 1$. Line L6 gives $\gamma(h) = 1 - \sum_{v \in S(h)} P_K(v \mid h') = \sum_{w \notin S(h)} P_K(w \mid h')$, by the induction hypothesis for $h'$. If $\gamma(h) > 0$, line L7 gives $\alpha(h) = \beta(h)/\gamma(h) \ge 0$ and

$$\sum_{w \in V} P_K(w \mid h) = (1 - \beta(h)) + \alpha(h) \sum_{w \notin S(h)} P_K(w \mid h') = 1 - \beta(h) + \frac{\beta(h)}{\gamma(h)} \gamma(h) = 1.$$

If $\gamma(h) = 0$, the lower order gives all its mass to the words of $S(h)$, and the implementation treats $h$ as in the case $S(h) = V$, with the undiscounted estimates, whose sum over $S(h)$ is 1, and with 0 for the other words. $\blacksquare$

**Remark.** The weight $\alpha(h)$ can exceed 1, since $\gamma(h)$ can be smaller than $\beta(h)$. It is a scale factor, not a probability. Lemma 1 shows that, per order, the counts taken away sum to the Good-Turing estimate $N_1$ of the total count of the unseen m-grams; Theorem 2 shows that the backoff weights then pass exactly the mass $\beta(h)$ of each history to its unseen words.
