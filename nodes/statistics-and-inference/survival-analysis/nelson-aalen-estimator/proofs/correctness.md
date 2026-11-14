---
title: The pass computes the Nelson-Aalen sums, and in discrete time the estimate is a martingale estimator with an explicit bias and the MLE of the cumulative hazard
proves: [correctness]
status: full
---

Let the data be $(y_i, \delta_i)$, $i = 1, \ldots, n$, with distinct event times $t_1 < \cdots < t_k$, $n_j = \#\{i : y_i \ge t_j\}$ and $d_j = \#\{i : y_i = t_j, \delta_i = 1\}$.

**Claim 1 (the pass computes the sums).** Every row that line L7 appends is $(t_j, n_j, d_j, \sum_{l \le j} d_l/n_l, \sum_{l \le j} d_l/n_l^2)$, one row for each $j$, in order.

*Proof.* After the sort of line L1, the inner loop of line L6 reads exactly the subjects at the current distinct time $u$, and sets $d$ and $c$ to the numbers of events and censorings at $u$. Invariant: at the start of the group at $u$, $r = \#\{i : y_i \ge u\}$, and $H$ and $V$ hold the two sums over the event times below $u$. It holds at the first group, with $r = n$ and empty sums. Line L7 adds the terms of $u$ if $u$ is an event time, with $r = n_j$ at that moment, and line L8 removes the $d + c$ subjects at $u$, so $r = \#\{i : y_i > u\}$, which is the count at risk at the next distinct time. The same argument covers the binomial sum and the sequential tie rule, which only change the term added in line L7. $\square$

For the remaining claims, fix a time $t$, let the support of $T$ in $(0, t]$ be a finite set $s_1 < \cdots < s_m$, and let $q_j = P(T = s_j \mid T \ge s_j)$ be the discrete hazard. The cumulative hazard of the discrete distribution is $H(t) = \sum_{j \le m} q_j$. Observed event times in $(0, t]$ are among the $s_j$, so $\hat H(t) = \sum_{j \le m} d_j/n_j$, with $d_j = 0$ (and the term $0$) where no event is observed, and the term $0$ when $n_j = 0$. Assume:

1. the subjects are independent;
2. independent censoring in the sequential form: given everything observed before $s_j$ (which determines who is at risk at $s_j$), each subject at risk at $s_j$ has an event at $s_j$ with probability $q_j$, independently of the others.

Condition 2 holds when the pairs $(T_i, C_i)$ are independent and $T_i$ is independent of $C_i$. Let $\mathcal F_j$ be the information observed before $s_j$; then $n_j$ is $\mathcal F_j$-measurable, and $d_j$ given $\mathcal F_j$ is binomial with $n_j$ trials and success probability $q_j$.

**Claim 2 (martingale).** $M_j = \sum_{l \le j}(d_l - q_l n_l)$ is a martingale with respect to $\mathcal F_{j+1}$, and so is $\hat H$ minus its compensator: $W_j = \sum_{l \le j}(d_l/n_l - q_l)1\{n_l > 0\}$.

*Proof.* $d_l - q_l n_l$ and $(d_l/n_l - q_l)1\{n_l > 0\}$ are $\mathcal F_{l+1}$-measurable, bounded, and have conditional mean $0$ given $\mathcal F_l$, because $E[d_l \mid \mathcal F_l] = q_l n_l$. A sum of bounded increments with conditional mean $0$ is a martingale. $\square$

**Claim 3 (bias).** $E[\hat H(t)] = \sum_{j \le m} q_j\,P(n_j > 0)$, so $\hat H(t)$ is unbiased for $H^*(t) = \sum_{j \le m} q_j 1\{n_j > 0\}$ in mean, and

$$H(t) - E[\hat H(t)] = \sum_{j \le m} q_j\,P(n_j = 0) \in \bigl[0,\ H(t)\,P(n_m = 0)\bigr].$$

*Proof.* $E[W_m] = 0$ by Claim 2, and $\hat H(t) = W_m + \sum_j q_j 1\{n_j > 0\}$. Take expectations. For the bound, $n_j \ge n_m$ for $j \le m$, so $P(n_j = 0) \le P(n_m = 0)$. $\square$

**Claim 4 (variance).** $\mathrm{Var}(W_m) = \sum_{j \le m} E\!\left[\frac{q_j(1 - q_j)}{n_j} 1\{n_j > 0\}\right]$, and $\frac{d_j(n_j - d_j)}{n_j^2(n_j - 1)}$ (for $n_j \ge 2$) has conditional mean $\frac{q_j(1 - q_j)}{n_j}$ given $\mathcal F_j$.

*Proof.* Martingale increments are uncorrelated: for $l < j$, the increment at $l$ is $\mathcal F_j$-measurable and the increment at $j$ has conditional mean $0$ given $\mathcal F_j$. So the variance of the sum is the sum of the expected conditional variances, and the conditional variance of $d_j/n_j$ given $\mathcal F_j$ is $q_j(1 - q_j)/n_j$ on $\{n_j > 0\}$. For the second statement, $E[d_j(n_j - d_j) \mid \mathcal F_j] = n_j\cdot n_j q_j - (n_j q_j(1 - q_j) + n_j^2 q_j^2) = n_j(n_j - 1)q_j(1 - q_j)$. Divide by $n_j^2(n_j - 1)$. $\square$

The binomial estimate $\hat\sigma^2_B$ of the code uses $n_j^3$ in place of $n_j^2(n_j - 1)$, and Aalen's $\hat\sigma^2_P = \sum d_j/n_j^2$ has conditional mean $\sum q_j/n_j$, which is the continuous-time limit where $q_j(1 - q_j) \approx q_j$.

**Claim 5 (maximum likelihood).** Under conditions 1 and 2, with noninformative censoring, the likelihood of the hazards is $\prod_j q_j^{d_j}(1 - q_j)^{n_j - d_j}$ times a factor free of $q$ (the [Kaplan-Meier correctness proof](/kaplan-meier-estimator/) derives this product). Each factor is maximized uniquely at $q_j = d_j/n_j$ when $n_j > 0$. By the invariance of maximum likelihood under the map $q \mapsto \sum_{j \le m} q_j$, $\hat H(t)$ is the MLE of $H(t)$ in this model. $\square$

**Cost.** One sort, $\Theta(n \log n)$, and a pass in which each subject advances the index once, $\Theta(n)$. The sequential tie rule adds $d_j$ terms at $t_j$, $O(n)$ in total.
