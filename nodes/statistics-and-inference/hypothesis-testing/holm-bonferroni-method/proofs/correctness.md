---
title: Holm's method is closed testing with Bonferroni local tests, and it controls the family-wise error rate strongly under any dependence
proves: [correctness]
status: full
---

We prove three things about HOLM. First, it controls the family-wise error rate at $\alpha$ for every set of true nulls and every joint law of the p-values (Theorem 1, a direct proof). Second, its rejections and its adjusted p-values are exactly those of the closed testing procedure with Bonferroni local tests (Theorem 2), so strong control also follows from the [closed testing principle](/closed-testing-principle/). Third, it rejects every hypothesis that the Bonferroni correction rejects. All results are proved; the tests check Theorem 2 by enumeration of all intersections for $m \le 8$, in exact rational arithmetic.

**Setting.** P-values $p_1, \dots, p_m$, sorted by line L1 as $p_{(1)} \le \dots \le p_{(m)}$, where $(k)$ is the index of rank $k$; ties are broken by the order of the sort and do not change any statement below. $I_0$ is the set of true nulls, $m_0 = |I_0| \ge 1$, and each null p-value is valid: $P(p_i \le u) \le u$. Fix $0 < \alpha < 1$.

**Lemma 1 (what the lines compute).** HOLM rejects $H_{(k)}$ if and only if $(m - j + 1)p_{(j)} \le \alpha$ for every $j \le k$. Its adjusted p-value is $\tilde p_{(k)} = \max_{j \le k}\min(1, (m - j + 1)p_{(j)})$, and $H_{(k)}$ is rejected if and only if $\tilde p_{(k)} \le \alpha$.

*Proof.* The loop at lines L2 to L4 starts at $k = 1$ and increases $k$ while the test holds, so on exit it has rejected exactly the ranks $1, \dots, r$, where $r + 1$ is the first rank that fails, or $r = m$. Rank $k$ is among them exactly when ranks $1, \dots, k$ all pass, which is the first claim. The loop at lines L5 to L7 keeps the running maximum, so $\tilde p_{(k)}$ is as stated. Since $\alpha < 1$, $\min(1, x) \le \alpha$ if and only if $x \le \alpha$, and a maximum is at most $\alpha$ if and only if every term is. $\square$

**Theorem 1 (strong control, direct).** For every $I_0$ and every joint law with valid null p-values, $P(V \ge 1) \le \alpha$.

*Proof.* Let $j^*$ be the smallest rank whose hypothesis is a true null, so $p_{(j^*)} = \min_{i \in I_0}p_i$. By Lemma 1 the rejected set is a prefix of ranks, so if any true null is rejected, the rank $j^*$ is rejected, which needs $(m - j^* + 1)p_{(j^*)} \le \alpha$. The ranks $1, \dots, j^* - 1$ all hold false nulls, so $j^* - 1 \le m - m_0$, that is, $m - j^* + 1 \ge m_0$. Hence a false rejection implies $m_0\min_{i \in I_0}p_i \le \alpha$, and
$$P(V \ge 1) \le P\Big(\min_{i \in I_0}p_i \le \frac{\alpha}{m_0}\Big) \le \sum_{i \in I_0}P\Big(p_i \le \frac{\alpha}{m_0}\Big) \le m_0 \cdot \frac{\alpha}{m_0} = \alpha.$$
The second inequality is the union bound, which needs no independence, and the third is validity. $\square$

The proof uses the random rank $j^*$ only to show that the event $\{V \ge 1\}$ is inside the fixed event $\{\min_{I_0}p_i \le \alpha/m_0\}$; no conditioning on $j^*$ is needed. That event is exactly the rejection of the intersection $H_{I_0}$ by its Bonferroni test, which is the closed testing argument in disguise.

**Closed testing with Bonferroni local tests.** For each nonempty $I \subseteq \{1, \dots, m\}$, the local test rejects $H_I = \bigcap_{i \in I}H_i$ when $|I|\min_{i \in I}p_i \le \alpha$. It has level $\alpha$ under $H_I$, by the union bound as above. The closed procedure rejects $H_i$ when every $H_I$ with $i \in I$ is rejected by its local test. Its adjusted p-value is $\hat p_i = \max_{I \ni i}\min(1, |I|\min_{j \in I}p_j)$, and it rejects $H_i$ exactly when $\hat p_i \le \alpha$.

**Lemma 2 (tails are the worst subsets).** For each rank $j$ let $T_j = \{(j), (j + 1), \dots, (m)\}$, with $|T_j| = m - j + 1$ and $\min_{T_j}p = p_{(j)}$. If $I$ is nonempty and $j$ is the smallest rank in $I$, then $I \subseteq T_j$, $\min_I p = p_{(j)}$, and $|I|\min_I p \le |T_j|\min_{T_j}p$.

*Proof.* Every element of $I$ has rank at least $j$, so $I \subseteq T_j$ and $|I| \le m - j + 1$. The element of rank $j$ is in $I$ and has the smallest p-value among ranks $\ge j$, so $\min_I p = p_{(j)} = \min_{T_j}p$. $\square$

**Theorem 2 (Holm is the closed procedure).** For every rank $k$, $\hat p_{(k)} = \tilde p_{(k)}$. Hence the closed procedure with Bonferroni local tests and HOLM reject the same hypotheses.

*Proof.* Fix $k$. ($\le$) Let $I \ni (k)$, and let $j$ be its smallest rank, so $j \le k$. By Lemma 2, $\min(1, |I|\min_I p) \le \min(1, (m - j + 1)p_{(j)}) \le \tilde p_{(k)}$. Taking the maximum over $I$ gives $\hat p_{(k)} \le \tilde p_{(k)}$. ($\ge$) For each $j \le k$, the tail $T_j$ contains $(k)$, so $\hat p_{(k)} \ge \min(1, |T_j|\min_{T_j}p) = \min(1, (m - j + 1)p_{(j)})$. Taking the maximum over $j \le k$ gives $\hat p_{(k)} \ge \tilde p_{(k)}$. The second claim follows from Lemma 1 and the rule $\hat p_i \le \alpha$. $\square$

So Holm inherits strong control from the closed testing principle, which says that the closed procedure built from level-$\alpha$ local tests controls the family-wise error rate strongly. That principle has a two-line proof: a false rejection needs the local rejection of $H_{I_0}$, which has probability at most $\alpha$. The [closed testing principle](/closed-testing-principle/) page proves it in full. The naive closed procedure checks $2^m - 1$ intersections; Theorem 2 shows that only the $m$ tails matter, which is why a sort suffices.

**Theorem 3 (domination of Bonferroni).** If $mp_i \le \alpha$ then HOLM rejects $H_i$. More precisely, $\tilde p_i \le \min(1, mp_i)$ for every $i$.

*Proof.* Let $i$ have rank $k$. For every $j \le k$, $(m - j + 1)p_{(j)} \le m\,p_{(j)} \le mp_{(k)} = mp_i$, since $m - j + 1 \le m$ and $p_{(j)} \le p_{(k)}$. So $\tilde p_{(k)} \le \min(1, mp_i)$, and the first claim follows by Lemma 1. $\square$

**Termination and cost.** The sort terminates, and each loop runs at most $m$ times with constant work per step.
