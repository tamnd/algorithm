---
title: WEAT computes the exact permutation p-value, and its effect size is at most 2
proves: [correctness]
status: full
---

We use the pseudocode of the page. The target sets $X$ and $Y$ have $n \ge 1$ vectors each, $A$ and $B$ are nonempty, and every vector is nonzero. Write $s_w = s(w, A, B)$ for $w \in X \cup Y$, which line L1 computes, and $T = \sum_{w \in X \cup Y} s_w$ (line L2). We treat $X \cup Y$ as a list of $2n$ positions, so a word that occurs twice counts twice.

**Lemma 1 (the partition identity).** For every split of the $2n$ positions into $X_i$ and $Y_i$ with $|X_i| = n$, $s(X_i, Y_i, A, B) = 2 \sum_{w \in X_i} s_w - T$.

*Proof.* $s(X_i, Y_i, A, B) = \sum_{X_i} s_w - \sum_{Y_i} s_w$, and $\sum_{Y_i} s_w = T - \sum_{X_i} s_w$. $\square$

So line L3 computes the statistic $S = s(X, Y, A, B)$ and line L8 the statistic of each split.

**Theorem 1 (the p-value).** Line L11 returns $p = |\{X_i : s(X_i, Y_i, A, B) > S\}| / \binom{2n}{n}$, the p-value of Caliskan, Bryson and Narayanan 2017. It is also the fraction of the $(2n)!$ orders of the $2n$ positions for which the first $n$ positions give a statistic larger than $S$.

*Proof.* Line L7 visits each subset of $n$ of the $2n$ positions exactly once, so the loop runs $\binom{2n}{n}$ times and line L10 counts them. By Lemma 1, line L9 adds 1 exactly for the subsets whose statistic is larger than $S$. For the second statement, each subset of size $n$ is the set of the first $n$ positions of exactly $n! \, n!$ orders, the same number for every subset, so the two fractions are equal. $\square$

With "$\ge$" in line L9 (strict = False in the code), the observed split itself counts, so the p-value is at least $1 / \binom{2n}{n}$. For $n = 4$ this is $1/70$, and for $n = 8$ it is $1/12870$.

**Theorem 2 (validity).** Suppose that, under the null hypothesis, the labels $X$ and $Y$ are given to the $2n$ fixed vectors by a uniform random choice of the $n$ positions called $X$. Then the version with "$\ge$" satisfies $\Pr[p \le \alpha] \le \alpha$ for every $\alpha \in [0, 1]$. The version with "$>$" is never larger, so it can only reject more often.

*Proof.* Let $v_1 \ge v_2 \ge \cdots \ge v_K$ be the statistics of the $K = \binom{2n}{n}$ splits. Under the null, the observed statistic $S$ is $v_J$ for a uniform random index $J$. The "$\ge$" p-value of the split $j$ is $p_j = |\{k : v_k \ge v_j\}| / K$, which is at least $j / K$. So $p_J \le \alpha$ implies $J \le \alpha K$, and $\Pr[J \le \alpha K] \le \alpha$. The strict version counts a subset of the same splits. $\square$

**Theorem 3 (the effect size).** Let $m_X$ and $m_Y$ be the means of $s_w$ over $X$ and $Y$, and let $\sigma$ be the population standard deviation of the $2n$ values $s_w$ (ddof = 0, line L4). If $\sigma > 0$, then $|d| = |m_X - m_Y| / \sigma \le 2$, with equality if and only if $s_w$ is constant on $X$ and constant on $Y$. With the sample standard deviation (ddof = 1), $|d| < 2$.

*Proof.* Let $\sigma_X^2$ and $\sigma_Y^2$ be the population variances inside $X$ and inside $Y$. The two sets have the same size, so the overall mean is $(m_X + m_Y)/2$, and the decomposition of the variance into a within part and a between part gives

$$\sigma^2 = \frac{\sigma_X^2 + \sigma_Y^2}{2} + \left(\frac{m_X - m_Y}{2}\right)^2 \ge \left(\frac{m_X - m_Y}{2}\right)^2.$$

Take square roots: $|m_X - m_Y| \le 2 \sigma$. Equality holds if and only if $\sigma_X = \sigma_Y = 0$. The sample standard deviation is $\sigma \sqrt{2n / (2n - 1)} > \sigma$, so the bound becomes strict. $\square$

**Symmetry.** Swapping $X$ and $Y$, or $A$ and $B$, changes the sign of every $s_w$ or of every label, so it negates $S$ and $d$. The multiset of split statistics is symmetric about 0, since the splits $(X_i, Y_i)$ and $(Y_i, X_i)$ have opposite values. So the p-value for $(Y, X)$ is the share of splits below $S$, and the two one-sided p-values add up to 1 minus the share of splits whose statistic equals $S$. $\blacksquare$
