---
title: The filter stops, and a round with large bad mass removes more bad weight than good weight
proves: [correctness]
status: full
---

This proof covers the deterministic part of the filter: the stopping of the loop and the removal lemma. The error bound $O(\varepsilon\sqrt{\log(1/\varepsilon)})$ for Gaussian data is a theorem of Diakonikolas, Kamath, Kane, Li, Moitra and Stewart (2019). It is cited on the main page and is not proved here.

**Notation.** The points are $x_1, \ldots, x_N \in \mathbb R^d$, and the weights are $w_i \ge 0$ with $W = \sum_i w_i > 0$. Put $\mu_w = \frac1W\sum_i w_i x_i$ and $\Sigma_w = \frac1W\sum_i w_i(x_i - \mu_w)(x_i - \mu_w)^{\mathsf T}$. In a round, $v$ is a unit vector and $\lambda = v^{\mathsf T}\Sigma_w v$; power iteration returns such a pair, with $\lambda$ the Rayleigh quotient of $v$. Put $\tau_i = (v^{\mathsf T}(x_i - \mu_w))^2$, and let $\tau_{\max}$ be the largest $\tau_i$ over the indices with $w_i > 0$. Let $\theta \ge 0$ be the threshold.

**Lemma 1 (the weighted mean of $\tau$ is $\lambda$).** $\frac1W\sum_i w_i\tau_i = \lambda$.

*Proof.* $\tau_i = v^{\mathsf T}(x_i - \mu_w)(x_i - \mu_w)^{\mathsf T}v$. Sum with weights $w_i/W$ and use the definition of $\Sigma_w$. $\square$

**Lemma 2 (the update).** In a round that reaches line L8, every new weight $w_i' = w_i(1 - \tau_i/\tau_{\max})$ satisfies $0 \le w_i' \le w_i$. At least one index with $w_i > 0$ gets $w_i' = 0$, and at least one keeps $w_i' > 0$.

*Proof.* Line L7 did not return, so the indices with $w_i > 0$ do not all have $\tau_i = \tau_{\max}$. So $\tau_{\max} > 0$, because $\tau_{\max}$ is at least every such $\tau_i \ge 0$ and one of them is smaller. For $w_i > 0$, $0 \le \tau_i \le \tau_{\max}$, so $0 \le 1 - \tau_i/\tau_{\max} \le 1$. For $w_i = 0$, $w_i' = 0$. An index with $w_i > 0$ and $\tau_i = \tau_{\max}$ gets $w_i' = 0$. An index with $w_i > 0$ and $\tau_i < \tau_{\max}$ keeps $w_i' > 0$. $\square$

**Theorem 1 (termination).** The loop returns after at most $N$ rounds, and $W > 0$ in every round, so $\mu_w$ and $\Sigma_w$ are always defined.

*Proof.* At the start every weight is $1/N > 0$. By Lemma 2, each round that does not return keeps a positive weight, so $W > 0$ holds again, and it lowers the number of positive weights by at least 1. Weights that are 0 stay 0. The number of positive weights starts at $N$ and stays at least 1, so at most $N - 1$ rounds can update the weights. The next round returns at line L5 or L7. $\square$

**Lemma 3 (removal).** Let the indices be split into good ones $G$ and bad ones $B$. In a round that reaches line L8, the weight removed from $G$ is $\frac{1}{\tau_{\max}}\sum_{i \in G} w_i\tau_i$, and the weight removed from $B$ is $\frac{1}{\tau_{\max}}\sum_{i \in B} w_i\tau_i$. So if
$$\sum_{i \in G} w_i\tau_i \le \sum_{i \in B} w_i\tau_i,$$
then the round removes at most as much weight from $G$ as from $B$.

*Proof.* For $w_i > 0$, $w_i - w_i' = w_i\tau_i/\tau_{\max}$, and for $w_i = 0$ both sides are 0. Sum over $G$ and over $B$. $\square$

By Lemma 1, the condition of Lemma 3 says that the bad points carry at least half of the weighted mean $\lambda$ of $\tau$.

**Corollary 1 (the good weight is kept).** Suppose $|B| \le \varepsilon N$ and the condition of Lemma 3 holds in every round that updates the weights. Then at the end
$$\sum_{i \in G}\Bigl(\frac1N - w_i\Bigr) \le \sum_{i \in B}\Bigl(\frac1N - w_i\Bigr) \le \varepsilon, \qquad\text{so}\qquad \sum_{i \in G} w_i \ge 1 - 2\varepsilon.$$

*Proof.* Add the inequality of Lemma 3 over the rounds. The total weight removed from $B$ is at most the initial weight $|B|/N \le \varepsilon$ of $B$. The good points start with weight $|G|/N \ge 1 - \varepsilon$. $\square$

**What is cited.** For an $\varepsilon$-corrupted sample of $N(\mu, I_d)$ with $N$ of order $d/\varepsilon^2$ up to logarithmic factors, the good points satisfy, with high probability, a deterministic stability condition. Under it, two facts hold (Diakonikolas et al. 2019; Diakonikolas and Kane 2023). First, while $\lambda$ is above a threshold of the form $1 + C\varepsilon\log(1/\varepsilon)$, the bad points carry most of the weighted $\tau$, so Lemma 3 applies. Second, when $\lambda$ is below the threshold and the good weight is at least $1 - 2\varepsilon$, the weighted mean satisfies $\|\mu_w - \mu\| = O(\varepsilon\sqrt{\log(1/\varepsilon)})$. With Corollary 1 these give the error bound. The constant $C$, and whether the condition of Lemma 3 holds in a given finite run, are not proved here. The tests measure them.
