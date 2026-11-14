---
title: The Benjamini-Hochberg procedure has FDR exactly (m_0/m) q for independent uniform null p-values
proves: [correctness]
status: full
---

We prove that BH rejects the set described on the page (Lemma 1), that this set is the largest self-consistent set (Proposition 2), and that its false discovery rate is at most $(m_0/m)q$ when every null p-value is valid and independent of all the other p-values, with equality when the null p-values are uniform on the thresholds (Theorem 4). As a corollary, the Simes global test has size exactly $q$. Control under positive dependence (PRDS) is due to Benjamini and Yekutieli (2001) and is only cited here; the tests measure it by Monte Carlo in one PRDS model.

**Setting.** P-values $p_1, \dots, p_m \in [0, 1]$ and a level $q \in (0, 1]$. For $t \ge 0$ let $N(t) = \#\{j : p_j \le t\}$, and write $t_k = kq/m$. $I_0$ is the set of true nulls, $m_0 = |I_0|$, $V$ is the number of rejected true nulls and $R$ the number of rejections.

**Lemma 1 (what the lines compute).** Let $R = \max\{k \in \{1, \dots, m\} : N(t_k) \ge k\}$, or $R = 0$ if there is no such $k$. Then lines L2 and L3 end with $k = R$, line L4 rejects exactly the set $\{i : p_i \le t_R\}$, and this set has exactly $R$ elements. (For $R = 0$ the set is empty.)

*Proof.* For any $k$ and $t$, $p_{(k)} \le t$ if and only if at least $k$ of the p-values are at most $t$, that is, $N(t) \ge k$. So the test at line L2 fails, $mp_{(k)} \le kq$, exactly when $N(t_k) \ge k$. The loop starts at $k = m$ and goes down while the test holds, so it stops at the largest $k$ with $N(t_k) \ge k$, or at 0. Next, $N(t_R) = R$: if $N(t_R) = n > R$, then $n \le m$ and $N(t_n) \ge N(t_R) = n$, because $t_n > t_R$, which contradicts the choice of $R$. So exactly $R$ p-values are at most $t_R$. They are the $R$ smallest, so they are the hypotheses of ranks $1, \dots, R$ for any order of ties, which is what line L4 rejects. $\square$

**Proposition 2 (self-consistency).** Call a set $S$ self-consistent if $p_i \le |S|q/m$ for all $i \in S$. The BH set $S^* = \{i : p_i \le t_R\}$ is self-consistent, and it contains every self-consistent set. So it is the largest one.

*Proof.* $|S^*| = R$ by Lemma 1, so $S^*$ is self-consistent. If $S$ is self-consistent with $s = |S| \ge 1$, then $S \subseteq \{i : p_i \le t_s\}$, so $N(t_s) \ge s$ and $s \le R$. Then $S \subseteq \{i : p_i \le t_s\} \subseteq \{i : p_i \le t_R\} = S^*$. $\square$

The test file uses Proposition 2 as a brute force: it searches all subsets for the largest self-consistent one, for $m \le 8$, and compares the result with BH.

**Lemma 3 (leave one out).** Fix $i$. Let $p^{(i)}$ be the vector $p$ with $p_i$ replaced by 0, and let $R^{(i)} \ge 1$ be the number of rejections of BH on $p^{(i)}$. Then for each $k \in \{1, \dots, m\}$,
$$\{H_i \text{ rejected and } R = k\} = \{p_i \le t_k\} \cap \{R^{(i)} = k\}.$$

*Proof.* $R^{(i)} \ge 1$ because the replaced value 0 is at most $t_1$. Write $N^{(i)}$ for the count on $p^{(i)}$, so $N^{(i)}(t) = N(t) + \mathbf 1\{p_i > t\}$, and let $k_0 = R^{(i)}$.

Case $p_i \le t_{k_0}$. For every $k \ge k_0$, $p_i \le t_k$, so $N(t_k) = N^{(i)}(t_k)$. Hence $N(t_{k_0}) = N^{(i)}(t_{k_0}) \ge k_0$, and $N(t_k) = N^{(i)}(t_k) < k$ for $k > k_0$. By Lemma 1, $R = k_0$, and $H_i$ is rejected since $p_i \le t_{k_0} = t_R$.

Case $p_i > t_{k_0}$. Since $N(t) \le N^{(i)}(t)$ for all $t$, every $k$ with $N(t_k) \ge k$ also has $N^{(i)}(t_k) \ge k$, so $R \le k_0$. Then $p_i > t_{k_0} \ge t_R$, and $H_i$ is not rejected.

So $H_i$ is rejected exactly when $p_i \le t_{R^{(i)}}$, and then $R = R^{(i)}$. For a fixed $k$, the event "$H_i$ rejected and $R = k$" is therefore the event "$R^{(i)} = k$ and $p_i \le t_k$". $\square$

The point of Lemma 3 is that $R^{(i)}$ is a function of the other $m - 1$ p-values only.

**Theorem 4 (FDR of BH).** Suppose that for each $i \in I_0$, $p_i$ is independent of $(p_j)_{j \ne i}$ and $P(p_i \le t_k) \le t_k$ for $k = 1, \dots, m$. Then
$$\text{FDR} = E\left[\frac{V}{\max(R, 1)}\right] \le \frac{m_0}{m}q.$$
If moreover $P(p_i \le t_k) = t_k$ for all $i \in I_0$ and all $k$, as for continuous uniform null p-values, then $\text{FDR} = (m_0/m)q$ exactly, for every law of the non-null p-values.

*Proof.* Pointwise, $V/\max(R, 1) = \sum_{i \in I_0}\mathbf 1\{H_i \text{ rejected}\}/\max(R, 1)$. When $H_i$ is rejected, $R \ge 1$, so by Lemma 3
$$\frac{\mathbf 1\{H_i \text{ rejected}\}}{\max(R, 1)} = \sum_{k=1}^m \frac1k\mathbf 1\{p_i \le t_k\}\mathbf 1\{R^{(i)} = k\}.$$
Take expectations. Since $R^{(i)}$ depends only on $(p_j)_{j \ne i}$, which is independent of $p_i$,
$$E\left[\frac{\mathbf 1\{H_i \text{ rejected}\}}{\max(R, 1)}\right] = \sum_{k=1}^m \frac1k P(p_i \le t_k)P(R^{(i)} = k) \le \sum_{k=1}^m \frac1k\cdot\frac{kq}{m}P(R^{(i)} = k) = \frac qm\sum_{k=1}^m P(R^{(i)} = k) = \frac qm.$$
The last step holds because $R^{(i)}$ takes a value in $\{1, \dots, m\}$. With $P(p_i \le t_k) = t_k$ the inequality is an equality. Summing over the $m_0$ true nulls gives the claim. $\square$

The proof needs each null p-value to be independent of all the other p-values, null and non-null, but it puts no condition on the joint law of the non-null p-values among themselves. It uses validity only at the $m$ points $t_k$. This is why the exact test in the code works: on the grid $\{1/10, \dots, 1\}$ with $m = 4$ and $q = 2/5$, every $t_k = k/10$ is a grid point, so a null p-value uniform on the grid has $P(p_i \le t_k) = t_k$, and Theorem 4 gives $\text{FDR} = m_0/10$ exactly. The test computes this sum over all $10^{m_0}$ null configurations in rational arithmetic and finds equality for $m_0 = 1, \dots, 4$.

**Corollary 5 (Simes).** If all $m$ nulls are true and the p-values are independent and uniform, then $P(\exists j : p_{(j)} \le jq/m) = q$.

*Proof.* The event is $\{R \ge 1\}$ by Lemma 1. Under the global null $V = R$, so $V/\max(R, 1) = \mathbf 1\{R \ge 1\}$, and Theorem 4 with $m_0 = m$ gives $P(R \ge 1) = q$. $\square$

**Proposition 6 (monotone).** If $p'_j \le p_j$ for all $j$, then BH on $p'$ rejects every hypothesis that BH on $p$ rejects.

*Proof.* $N'(t) \ge N(t)$ for all $t$, so $R' \ge R$ by Lemma 1, and $t_{R'} \ge t_R$. If $p_i \le t_R$ then $p'_i \le p_i \le t_R \le t_{R'}$. $\square$

**Adjusted p-values.** Let $\tilde p_{(r)} = \min_{j \ge r}\min(1, mp_{(j)}/j)$, which lines L5 to L7 compute (the running value starts at 1). For $q \le 1$, $\tilde p_{(r)} \le q$ if and only if some $j \ge r$ has $mp_{(j)} \le jq$, that is, if and only if $R \ge r$, which by Lemma 1 is the rejection of rank $r$. So $H_i$ is rejected at level $q$ exactly when $\tilde p_i \le q$, and the adjusted p-values give the decisions at every level at once.

**What is cited, not proved.** Benjamini and Yekutieli (2001) show that $\text{FDR} \le (m_0/m)q$ when the p-values are PRDS on the subset of true nulls, and that $\text{FDR} \le (m_0/m)q\sum_{i=1}^m 1/i$ under any dependence. The second bound is proved on the [Benjamini-Yekutieli](/benjamini-yekutieli-procedure/) page. The first is checked only by simulation in the tests, with equicorrelated one-sided normal statistics.
