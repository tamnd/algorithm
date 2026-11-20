---
title: The sample mean of marginal contributions is unbiased, efficient and concentrated
proves: [correctness]
status: full
---

The game is $(N, v)$ with $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$. For an order $\pi$ of $N$, let $P_i^\pi$ be the set of players that come before $i$ in $\pi$, and let $\Delta_i(\pi) = v(P_i^\pi \cup \{i\}) - v(P_i^\pi)$ be the marginal contribution of $i$ in $\pi$. The Shapley value is
$$\varphi_i(v) = \frac{1}{n!} \sum_{\pi} \Delta_i(\pi),$$
the mean of $\Delta_i(\pi)$ over all $n!$ orders.

**Lemma (one order).** In one pass of the loop of line L2 with the order $\pi$, lines L4 to L9 add $\Delta_i(\pi)$ to $total[i]$ for each player $i$, and nothing else. The values added in the pass sum to $v(N)$.

*Proof.* We use this invariant for the loop of line L5: before the $t$-th player of $\pi$ is handled, $members$ holds the first $t - 1$ players of $\pi$ and $prev = v(members)$. Line L4 makes it true for $t = 1$, since $members = \emptyset$ and $v(\emptyset) = 0$. When the $t$-th player $i$ is handled, $members = P_i^\pi$. Line L6 adds $i$, line L7 sets $cur = v(P_i^\pi \cup \{i\})$, line L8 adds $cur - prev = \Delta_i(\pi)$ to $total[i]$, and line L9 sets $prev = v(members)$, so the invariant holds for $t + 1$. Each player appears once in $\pi$, so each $total[i]$ gets exactly one term. The terms telescope: their sum is $v(N) - v(\emptyset) = v(N)$. $\square$

**Theorem (unbiased and efficient).** Let $\hat\varphi_i$ be the value that line L10 returns for player $i$. If line L3 gives independent orders, each uniform over the $n!$ orders, then $\mathbb{E}[\hat\varphi_i] = \varphi_i(v)$ for each $i$. For every outcome of the random orders, $\sum_i \hat\varphi_i = v(N)$.

*Proof.* By the lemma, $\hat\varphi_i = \frac{1}{m} \sum_{k=1}^m \Delta_i(\pi_k)$, where $\pi_1, \ldots, \pi_m$ are the orders of the passes. For a uniform $\pi$, $\mathbb{E}[\Delta_i(\pi)] = \frac{1}{n!} \sum_\pi \Delta_i(\pi) = \varphi_i(v)$. By linearity of expectation, $\mathbb{E}[\hat\varphi_i] = \varphi_i(v)$. Each pass adds a total of $v(N)$ by the lemma, so $\sum_i total[i] = m\, v(N)$ and $\sum_i \hat\varphi_i = v(N)$. $\square$

**Theorem (Hoeffding bound).** Assume that for each player $i$ there are numbers $a_i \le b_i$ with $b_i - a_i \le r$ and $a_i \le \Delta_i(\pi) \le b_i$ for every order $\pi$. Then for each $\varepsilon > 0$ and each player $i$,
$$\Pr\big[|\hat\varphi_i - \varphi_i(v)| \ge \varepsilon\big] \le 2 \exp\!\left(-\frac{2 m \varepsilon^2}{r^2}\right).$$
If $m \ge \frac{r^2 \ln(2n/\delta)}{2 \varepsilon^2}$, then with probability at least $1 - \delta$ every player has $|\hat\varphi_i - \varphi_i(v)| < \varepsilon$.

*Proof.* For a fixed $i$, the values $\Delta_i(\pi_1), \ldots, \Delta_i(\pi_m)$ are independent, since the orders are independent, and each lies in $[a_i, b_i]$. Their mean is $\hat\varphi_i$ and its expected value is $\varphi_i(v)$ by the theorem above. Hoeffding's inequality for the mean of $m$ independent variables with values in intervals of length at most $r$ gives the first bound. With the stated $m$, the bound is at most $2 \exp(-\ln(2n/\delta)) = \delta / n$ for each player. By the union bound over the $n$ players, the probability that some player is off by $\varepsilon$ or more is at most $\delta$. $\blacksquare$

**Remark on the source of randomness.** The theorems assume uniform independent orders. The function `samples_needed` computes the $m$ of the theorem, and `hoeffding_failure_bound` computes the bound for one player. A pseudo-random generator only approximates this assumption. Python's `random.shuffle` is the Fisher-Yates shuffle, which gives a uniform order when its random numbers are uniform. For large $n$, the generator's period is smaller than $n!$, so most orders can never appear, but the bounds are about the mean of $m$ samples and do not need every order to be possible.
