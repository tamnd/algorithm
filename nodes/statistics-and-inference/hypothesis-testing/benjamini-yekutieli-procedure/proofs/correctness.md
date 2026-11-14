---
title: The Benjamini-Yekutieli procedure controls the FDR at (m_0/m) q under any dependence, and the harmonic factor is sharp
proves: [correctness]
status: full
---

We prove that any step-up procedure with thresholds $t_1 \le \dots \le t_m$ has false discovery rate at most $m_0\big(\sum_{j=1}^m t_j/(j(j+1)) + t_m/(m+1)\big)$ under any dependence (Theorem 1). For the Benjamini-Yekutieli thresholds this is $(m_0/m)q$ (Corollary 2). Then we build a joint law of valid null p-values under which Benjamini-Hochberg at $q$ has FDR exactly $qc_m$ and Benjamini-Yekutieli at $q$ has FDR exactly $q$ (Theorem 3). Everything here is proved; the tests check Corollary 2 exactly on random dependence structures and Theorem 3 exactly for $m \le 5$.

**Setting.** P-values $p_1, \dots, p_m$ with any joint law. $I_0$ is the set of true nulls, $m_0 = |I_0|$, and each null p-value is valid: $P(p_i \le u) \le u$ for $u \in [0, 1]$. $c_m = \sum_{i=1}^m 1/i$. A step-up procedure with thresholds $0 \le t_1 \le \dots \le t_m \le 1$ sets $R = \max\{k : N(t_k) \ge k\}$, with $N(t) = \#\{j : p_j \le t\}$ and $R = 0$ if there is no such $k$, and rejects $\{i : p_i \le t_R\}$. BH at level $q$ is the case $t_k = kq/m$, and BY at level $q$ is the case $t_k = kq/(mc_m)$, which is what lines L1 to L5 compute (Lemma 1 in the correctness proof of the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) applies with $q/c_m$ in place of $q$).

**Theorem 1.** For every step-up procedure with thresholds $t_1 \le \dots \le t_m$ and every joint law with valid null p-values,
$$\text{FDR} \le m_0\Big(\sum_{j=1}^m \frac{t_j}{j(j+1)} + \frac{t_m}{m+1}\Big).$$

*Proof.* Pointwise, $V/\max(R, 1) = \sum_{i \in I_0}\sum_{k=1}^m \mathbf 1_{A_k^{(i)}}/k$, where $A_k^{(i)}$ is the event that $H_i$ is rejected and $R = k$. Fix $i \in I_0$ and write $A_k = A_k^{(i)}$. The events $A_1, \dots, A_m$ are disjoint, since $R$ takes one value. On $A_k$, $H_i$ is rejected, so $p_i \le t_R = t_k$. Hence for each $j$, $\bigcup_{k \le j}A_k \subseteq \{p_i \le t_j\}$, because $t_k \le t_j$ for $k \le j$, and so
$$P\Big(\bigcup_{k \le j}A_k\Big) \le P(p_i \le t_j) \le t_j.$$
For $1 \le k \le m$ the telescoping sum gives $\frac1k = \sum_{j=k}^m\big(\frac1j - \frac1{j+1}\big) + \frac1{m+1}$. Therefore, exchanging the order of summation and using disjointness,
$$\sum_{k=1}^m \frac{P(A_k)}{k} = \sum_{j=1}^m\Big(\frac1j - \frac1{j+1}\Big)\sum_{k \le j}P(A_k) + \frac1{m+1}\sum_{k=1}^m P(A_k) = \sum_{j=1}^m \frac{P(\bigcup_{k \le j}A_k)}{j(j+1)} + \frac{P(\bigcup_{k \le m}A_k)}{m+1}.$$
Each probability is at most the matching $t_j$, and the coefficients are positive, so the sum is at most $\sum_j t_j/(j(j+1)) + t_m/(m+1)$. Summing over the $m_0$ true nulls gives the theorem. $\square$

No independence or positive dependence was used: only validity at the thresholds and the fact that a step-up rejection of $H_i$ with $R = k$ needs $p_i \le t_k$.

**Corollary 2 (Benjamini-Yekutieli).** For every $q' \in (0, 1]$, the step-up procedure with $t_k = kq'/m$ has $\text{FDR} \le (m_0/m)q'c_m$. In particular BH at $q$ has $\text{FDR} \le (m_0/m)qc_m$, and BY at $q$, which is the case $q' = q/c_m$, has $\text{FDR} \le (m_0/m)q$ under any dependence.

*Proof.* With $t_j = jq'/m$, $t_j/(j(j+1)) = q'/(m(j + 1))$ and $t_m/(m + 1) = (q'/m)\cdot m/(m + 1)$. So the bound of Theorem 1 is
$$m_0\frac{q'}{m}\Big(\sum_{j=2}^{m+1}\frac1j + \frac{m}{m+1}\Big) = m_0\frac{q'}{m}\Big(c_m - 1 + \frac1{m+1} + \frac{m}{m+1}\Big) = \frac{m_0}{m}q'c_m. \qquad\square$$

**Theorem 3 (the factor $c_m$ is sharp).** Let $m \ge 1$ and $q > 0$ with $qc_m \le 1$, and $q < 1$ if $m \ge 2$. Define the joint law $L_q$ of $(p_1, \dots, p_m)$ as follows. For each $k = 1, \dots, m$, with probability $q/k$, choose a set $S$ of $k$ indices uniformly at random, set $p_i = kq/m$ for $i \in S$ and $p_i = 1$ for $i \notin S$. With the remaining probability $1 - qc_m$, set every $p_i = 1$. Then every $p_i$ is a valid p-value with $P(p_i \le kq/m) = kq/m$ for each $k$, and if all $m$ nulls are true, BH at level $q$ has $\text{FDR} = qc_m$.

*Proof.* The probabilities $q/k$ and $1 - qc_m$ are nonnegative and sum to 1. Fix $i$. In case $k$, index $i$ is in $S$ with probability $k/m$, so $P(p_i = kq/m) = (q/k)(k/m) = q/m$ for each $k$, and $P(p_i = 1) = 1 - q$. So $P(p_i \le kq/m) = kq/m$. For $u \in [0, 1)$, let $j$ be the largest $k$ with $kq/m \le u$ (or $j = 0$); then $P(p_i \le u) = jq/m \le u$. For $u = 1$ the probability is 1. So $p_i$ is valid.

In case $k$, exactly $k$ p-values equal $t_k = kq/m$ and the others equal $1 > q \ge t_j$ for all $j$ (for $m = 1$ there are no others). So $N(t_j) = 0 < j$ for $j < k$, $N(t_k) = k$, and $N(t_j) = k < j$ for $j > k$. Hence $R = k$. In the last case $R = 0$. Under the global null every rejection is false, so $V/\max(R, 1) = \mathbf 1\{R \ge 1\}$ and $\text{FDR} = P(R \ge 1) = \sum_{k=1}^m q/k = qc_m$. $\square$

**Corollary 4.** Under the law $L_{q/c_m}$ with all nulls true, BY at level $q \le 1$ has FDR exactly $q$. So the bound of Corollary 2 is attained when $m_0 = m$.

*Proof.* BY at $q$ is BH at $q/c_m$, and $(q/c_m)c_m = q \le 1$, so Theorem 3 applies with level $q/c_m$ and gives $\text{FDR} = (q/c_m)c_m = q$. (For $m \ge 2$, $q/c_m < 1$ since $c_m > 1$.) $\square$

For $m = 2$ the law $L_q$ is the example on the page: with probability $q$ one p-value is $q/2$ and the other is 1, with probability $q/2$ both are $q$, and BH has FDR $3q/2$.

**Adjusted p-values.** Lines L6 and L7 compute $\tilde p_{(r)} = \min_{j \ge r}\min(1, mc_mp_{(j)}/j)$. For $q \le 1$, $\tilde p_{(r)} \le q$ if and only if $mc_mp_{(j)} \le jq$ for some $j \ge r$, which is $R \ge r$, the rejection of rank $r$. The tests check this equivalence on random vectors in exact arithmetic.
