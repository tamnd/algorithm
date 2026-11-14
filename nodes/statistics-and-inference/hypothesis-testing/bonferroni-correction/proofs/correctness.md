---
title: The Bonferroni correction controls the family-wise error rate strongly under any dependence, and the bound is attained
proves: [correctness]
status: full
---

We prove that BONFERRONI controls the family-wise error rate at $(m_0/m)\alpha$ for every set of true nulls and every joint law of the p-values, that the bound cannot be improved without assumptions on the dependence, and that the two forms of the output agree. We also prove that the Šidák level gives an error rate of exactly $\alpha$ under independence. All results here are proved; the tests check them by exact counting on grids and by simulation.

**Setting.** $H_1, \dots, H_m$ are hypotheses with p-values $p_1, \dots, p_m$, and $I_0 \subseteq \{1, \dots, m\}$ is the set of true nulls, with $m_0 = |I_0|$. For each $i \in I_0$, $p_i$ is valid: $P(p_i \le u) \le u$ for all $u \in [0, 1]$. $V = |\{i \in I_0 : H_i \text{ rejected}\}|$ is the number of false rejections.

**Lemma 1 (what the lines compute).** BONFERRONI rejects $H_i$ if and only if $p_i \le \alpha/m$, and for $\alpha < 1$ this holds if and only if $\tilde p_i = \min(1, mp_i) \le \alpha$.

*Proof.* Line L1 sets $c = \alpha/m$ and line L3 sets $\text{reject}_i$ to the truth value of $p_i \le c$. For the second claim: if $p_i \le \alpha/m$ then $mp_i \le \alpha$, so $\min(1, mp_i) \le \alpha$. Conversely, if $\min(1, mp_i) \le \alpha < 1$, the minimum is not 1, so it equals $mp_i$, and $mp_i \le \alpha$ gives $p_i \le \alpha/m$. $\square$

At $\alpha = 1$ every capped value satisfies $\tilde p_i \le 1$, while $p_i \le 1/m$ can fail; this is why the equivalence needs $\alpha < 1$, and why the level is in $(0, 1)$ in practice.

**Theorem 1 (strong control).** For every $I_0$ and every joint law of $(p_1, \dots, p_m)$ with valid null p-values,
$$P(V \ge 1) \le E[V] \le \frac{m_0}{m}\alpha \le \alpha.$$

*Proof.* By Lemma 1, $V = \sum_{i \in I_0}\mathbf 1\{p_i \le \alpha/m\}$. By linearity of expectation, which needs no independence,
$$E[V] = \sum_{i \in I_0}P(p_i \le \alpha/m) \le \sum_{i \in I_0}\frac{\alpha}{m} = \frac{m_0}{m}\alpha,$$
where the inequality is the validity of each null p-value at $u = \alpha/m$. Since $V$ takes values in $\{0, 1, 2, \dots\}$, $\mathbf 1\{V \ge 1\} \le V$, and taking expectations gives $P(V \ge 1) \le E[V]$. Finally $m_0 \le m$. $\square$

The first inequality is Markov's inequality at 1, and the whole chain is the union bound $P(\bigcup_{i \in I_0}A_i) \le \sum_{i \in I_0}P(A_i)$ with $A_i = \{p_i \le \alpha/m\}$. Because $I_0$ is arbitrary, the control is strong, not only under the global null $I_0 = \{1, \dots, m\}$.

**Theorem 2 (the bound is attained).** Let $m_0 = m$ and $0 < \alpha \le 1$. There is a joint law in which every $p_i$ is uniform on $(0, 1)$ and $P(V \ge 1) = \alpha$ exactly.

*Proof.* Let $U$ be uniform on $(0, 1)$ and $p_i = (U + i/m) \bmod 1$ for $i = 1, \dots, m$. Each $p_i$ is a rotation of $U$ on the circle of length 1, so it is uniform. The event $A_i = \{p_i \le \alpha/m\}$ is the event that $U$ lies in the arc $[-i/m, -i/m + \alpha/m]$ taken modulo 1. These arcs have length $\alpha/m \le 1/m$ and start at the $m$ distinct points $-i/m$, which are $1/m$ apart, so they overlap at most at their end points, a set of probability zero. So $P(\bigcup_i A_i) = \sum_i P(A_i) = m \cdot \alpha/m = \alpha$. $\square$

So no procedure that uses the threshold $c > \alpha/m$ on every test can control the family-wise error rate at $\alpha$ under arbitrary dependence: on this law, it has error rate $\min(1, mc) > \alpha$. Bonferroni is the best single-step procedure with a common threshold when nothing is known about the dependence. The tests check Theorem 2 by exact counting, on a grid of $N$ values of $U$ with $N$ a multiple of $m$, where each $p_i$ is uniform on $\{1/N, \dots, N/N\}$.

**Theorem 3 (Šidák under independence).** If the null p-values are independent and uniform, and every $H_i$ is tested at $c_S = 1 - (1 - \alpha)^{1/m}$, then $P(V \ge 1) = 1 - (1 - \alpha)^{m_0/m} \le \alpha$, with equality when $m_0 = m$. Also $c_S \ge \alpha/m$.

*Proof.* By independence, $P(V = 0) = \prod_{i \in I_0}P(p_i > c_S) = (1 - c_S)^{m_0} = (1 - \alpha)^{m_0/m}$. This is at least $1 - \alpha$, with equality when $m_0 = m$. For the last claim, by Bernoulli's inequality $(1 - \alpha/m)^m \ge 1 - \alpha$, so $1 - \alpha/m \ge (1 - \alpha)^{1/m}$, which is $c_S \ge \alpha/m$. $\square$

Under dependence Theorem 3 can fail. Šidák (1967) proved that for a normal vector with mean zero and any covariance, $P(|X_i| \le c_i \text{ for all } i) \ge \prod_i P(|X_i| \le c_i)$, which makes the two-sided tests based on such a vector valid at the Šidák level. We cite this result and do not prove it.

**Termination and cost.** The loop runs $m$ times and does a constant amount of work each time.
