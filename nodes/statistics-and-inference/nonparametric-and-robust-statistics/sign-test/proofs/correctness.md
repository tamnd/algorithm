---
title: The sign test returns exact binomial tails, and each p-value is valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. $D_1, \ldots, D_N$ are independent, and under $H_0$ each satisfies $P(D_i > 0) = P(D_i < 0)$. Let $Z = \{i : D_i \ne 0\}$ be the random set of nonzero values and $n = \lvert Z \rvert$.

**Claim 1 (the null law).** Under $H_0$, conditional on $Z = z$ with $\lvert z \rvert = n$, the statistic $S = \#\{i \in z : D_i > 0\}$ is $\text{Binomial}(n, 1/2)$.

*Proof.* The events $\{D_i > 0\}$ and $\{D_i \ne 0\}$ depend only on $D_i$, and the $D_i$ are independent. Conditioning on $Z = z$ is conditioning on $\{D_i \ne 0\}$ for $i \in z$ and $\{D_i = 0\}$ for $i \notin z$, so the indicators $\mathbf{1}\{D_i > 0\}$, $i \in z$, stay independent, and each has conditional probability $P(D_i > 0) / (P(D_i > 0) + P(D_i < 0)) = 1/2$. A sum of $n$ independent Bernoulli$(1/2)$ indicators is $\text{Binomial}(n, 1/2)$. $\square$

**Claim 2 (the returned values).** Line L3 sets $w[k] = \binom{n}{k}$: $w[0] = 1$, and $\binom{n}{k + 1} = \binom{n}{k} (n - k)/(k + 1)$, where the division is exact because the result is an integer. Line L4 gives $U = \sum_{k \ge S} \binom{n}{k}$ and $L = \sum_{k \le S} \binom{n}{k}$. So lines L5, L6 and L7 return $P_{hi}(S) = P(B \ge S)$, $P_{lo}(S) = P(B \le S)$ and $\min\{1, 2 \min(P_{lo}, P_{hi})\}$ for $B \sim \text{Binomial}(n, 1/2)$. $\square$

**Claim 3 (validity).** For every $\alpha \in [0, 1]$, $P_{H_0}(p \le \alpha) \le \alpha$ for each of the three p-values.

*Proof.* Condition on $Z = z$; by Claim 1, $S \sim B$. For the "greater" p-value, let $A = \{s : P(B \ge s) \le \alpha\}$. If $A$ is empty the probability is $0$. Otherwise let $s^*$ be its smallest element. Every $s \in A$ has $s \ge s^*$, so $P(S \in A) \le P(B \ge s^*) \le \alpha$. The "less" case is the same with the order reversed. For the two-sided p-value, $p \le \alpha$ forces $P_{hi}(S) \le \alpha/2$ or $P_{lo}(S) \le \alpha/2$, and each event has conditional probability at most $\alpha/2$ by the one-sided argument. So the conditional probability of rejection is at most $\alpha$ for every $z$, and averaging over $Z$ gives the unconditional bound. $\square$

**Claim 4 (the two-sided rule).** Doubling equals the rule that sums the null probabilities of all outcomes at most as likely as $S$.

*Proof.* $b(k) = \binom{n}{k}/2^n$ is symmetric, $b(k) = b(n - k)$, and increases for $k \le n/2$. Take $s \le n/2$ (the other case is symmetric). The outcomes $k$ with $b(k) \le b(s)$ are $k \le s$ and $k \ge n - s$. If $s < n/2$ these sets are disjoint and their probability is $2 P(B \le s) = 2 \min(P_{lo}, P_{hi})$. If $s = n/2$ every outcome qualifies, the sum is $1$, and $2 P(B \le s) \ge 1$, so the minimum with $1$ gives $1$ as well. $\square$

**Cost.** Lines L1 and L2 take one pass. Line L3 does $n$ multiplications and exact divisions, and line L4 at most $2n + 2$ additions. In the real-RAM model with unit-cost arithmetic the time is $\Theta(n)$ and the list takes $\Theta(n)$ space. $\square$
