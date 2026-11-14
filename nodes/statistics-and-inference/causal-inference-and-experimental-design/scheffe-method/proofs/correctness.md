---
title: Scheffe's intervals cover all contrasts at once with probability exactly 1 - alpha, and the F-test rejects exactly when some contrast is significant
proves: [correctness, termination]
status: full
---

We prove that the largest squared standardized contrast of the group means is $SSB/MSE = (k - 1)F$, attained at the contrast with coefficients $n_i(\bar y_i - \bar y)$. It follows that Scheffé's intervals cover every contrast at once with probability exactly $1 - \alpha$, for equal or unequal group sizes, that the contrast tests control the family-wise error rate in the strong sense, and that the [one-way ANOVA](/one-way-anova/) F-test rejects exactly when some contrast interval excludes 0. The model is $y_{ij} = \mu_i + e_{ij}$, $i = 1, \dots, k$, $j = 1, \dots, n_i \ge 1$, with iid $N(0, \sigma^2)$ errors, $N = \sum n_i > k$, $\nu = N - k$, $MSE = SSW/\nu$ and $\bar y = \sum n_i\bar y_i/N$. A contrast is a nonzero $c \in \mathbb R^k$ with $\sum_i c_i = 0$; it estimates $\psi_c = \sum c_i\mu_i$ by $\hat\psi_c = \sum c_i\bar y_i$, with $\widehat{\mathrm{se}}_c^2 = MSE\sum c_i^2/n_i$.

**Lemma 1 (the largest contrast).** Let $d_1, \dots, d_k$ be any numbers and $\bar d = \sum n_id_i/N$. For every contrast $c$,

$$\frac{\big(\sum_i c_id_i\big)^2}{\sum_i c_i^2/n_i} \le \sum_i n_i(d_i - \bar d)^2,$$

with equality when $c_i = n_i(d_i - \bar d)$, which is a contrast whenever the $d_i$ are not all equal.

*Proof.* Because $\sum c_i = 0$, $\sum c_id_i = \sum c_i(d_i - \bar d) = \sum_i \frac{c_i}{\sqrt{n_i}}\cdot\sqrt{n_i}(d_i - \bar d)$. The Cauchy-Schwarz inequality gives $(\sum c_id_i)^2 \le \sum c_i^2/n_i\cdot\sum n_i(d_i - \bar d)^2$. Equality holds when the two vectors are proportional, $c_i/\sqrt{n_i} \propto \sqrt{n_i}(d_i - \bar d)$, that is $c_i \propto n_i(d_i - \bar d)$. These coefficients sum to $\sum n_id_i - N\bar d = 0$, so they form a contrast if they are not all 0. $\square$

With $d_i = \bar y_i$ the right side is $SSB$, so $\sup_c\hat\psi_c^2/\widehat{\mathrm{se}}_c^2 = SSB/MSE = (k - 1)F$, where $F$ is the one-way ANOVA statistic. The supremum over the infinite set of contrasts is attained, and `best_contrast` returns the maximizer.

**Lemma 2 (the pivot).** For every $\mu$ and $\sigma$,

$$\max_c \frac{(\hat\psi_c - \psi_c)^2}{\widehat{\mathrm{se}}_c^2} \sim (k - 1)F_{k-1,\nu}.$$

*Proof.* Put $d_i = \bar y_i - \mu_i$, the mean of the errors of group $i$. Then $\hat\psi_c - \psi_c = \sum c_id_i$, and Lemma 1 gives the maximum $\sum n_i(d_i - \bar d)^2/MSE$. The numerator is $SSB$ computed from the errors $e = y - \mu$ in place of $y$. $MSE$ is the same for $y$ and for $e$, because $\mu$ is constant within each group. The errors satisfy the one-way null hypothesis (all their means are 0), so by Lemma 3 of the [one-way ANOVA](/one-way-anova/) proof, $SSB(e)/\sigma^2 \sim \chi^2_{k-1}$ independent of $SSW/\sigma^2 \sim \chi^2_\nu$, and their ratio scaled by the degrees of freedom is $F_{k-1,\nu}$. $\square$

**Lemma 3 (exact simultaneous coverage).** Let $M = \sqrt{(k - 1)F_{(k-1,\nu,1-\alpha)}}$. Then

$$P\big(\psi_c \in [\hat\psi_c - M\widehat{\mathrm{se}}_c,\ \hat\psi_c + M\widehat{\mathrm{se}}_c] \text{ for every contrast } c\big) = 1 - \alpha .$$

*Proof.* All intervals cover if and only if $(\hat\psi_c - \psi_c)^2/\widehat{\mathrm{se}}_c^2 \le M^2$ for every $c$, which holds if and only if the maximum in Lemma 2 is at most $M^2$. By Lemma 2 this has probability $P(F_{k-1,\nu} \le F_{(k-1,\nu,1-\alpha)}) = 1 - \alpha$, since the F law is continuous. $\square$

The intervals are invariant under scaling of $c$: $\hat\psi_{tc} = t\hat\psi_c$ and $\widehat{\mathrm{se}}_{tc} = |t|\widehat{\mathrm{se}}_c$. So the family is really indexed by the directions of contrasts, a sphere of dimension $k - 2$.

**Lemma 4 (the code).** L1 returns the sizes, the means, $MSE$ and $\nu$, with the group means subtracted before squaring. L2 sets $M$. For each contrast, L4 and L5 compute $\hat\psi_c$ and $\widehat{\mathrm{se}}_c$, L6 computes $f_c = \hat\psi_c^2/((k - 1)\widehat{\mathrm{se}}_c^2)$, and L7 returns $p_c = P(F_{k-1,\nu} > f_c)$ and the interval $\hat\psi_c \pm M\widehat{\mathrm{se}}_c$. The interval excludes 0 if and only if $f_c > F_{(k-1,\nu,1-\alpha)}$, if and only if $p_c < \alpha$.

*Proof.* Each line is its formula. The interval excludes 0 if and only if $|\hat\psi_c| > M\widehat{\mathrm{se}}_c$; square both sides and divide by $(k - 1)\widehat{\mathrm{se}}_c^2$. The upper tail of $F$ is strictly decreasing, which gives the p-value form. The code rejects vectors that do not sum to 0, the zero vector, $N \le k$ and $MSE = 0$. $\square$

**Lemma 5 (equivalence with the F-test).** The F-test at level $\alpha$ rejects, $F > F_{(k-1,\nu,1-\alpha)}$, if and only if the Scheffé interval of some contrast excludes 0. The contrast $c_i = n_i(\bar y_i - \bar y)$ is such a contrast whenever one exists, and its Scheffé p-value equals the F-test p-value. For every contrast, $p_c \ge p_F$.

*Proof.* By Lemma 1, $f_c \le SSB/((k-1)MSE) = F$ for every contrast, with equality at $c_i = n_i(\bar y_i - \bar y)$. If some interval excludes 0, then $F \ge f_c > F_{(k-1,\nu,1-\alpha)}$ by Lemma 4. Conversely, if $F > F_{(k-1,\nu,1-\alpha)}$, then the means are not all equal, the maximizing coefficients form a contrast, its $f_c = F$, and its interval excludes 0. The p-values follow because $P(F_{k-1,\nu} > \cdot)$ is decreasing. $\square$

**Lemma 6 (strong family-wise error control).** Reject $H_c: \psi_c = 0$ when $p_c < \alpha$. For every $\mu$, the probability of rejecting at least one true $H_c$, over all contrasts at once, is at most $\alpha$. Under $\mu_1 = \dots = \mu_k$ it is exactly $\alpha$.

*Proof.* If $H_c$ is true and rejected, the interval of $c$ excludes $0 = \psi_c$, so it misses. By Lemma 3 some interval misses with probability exactly $\alpha$. Under the complete null every $H_c$ is true, and some $H_c$ is rejected exactly when the F-test rejects (Lemma 5), which has probability $\alpha$. $\square$

Nothing in Lemmas 1 to 6 needs equal group sizes. The same argument works for any $q$-dimensional space of estimable linear functions $a^\top b$ in a linear model $y = Xb + e$ with $n$ rows and $k$ columns: the supremum of the squared standardized estimates is $q$ times the [regression F](/regression-f-test/) statistic of the hypothesis that all of them are 0, and the multiplier is $\sqrt{qF_{(q,n-k,1-\alpha)}}$.

**Termination.** L1 makes two passes over the $N$ observations. L2 doubles an upper bracket until the F upper tail falls below $\alpha$, which happens because the tail tends to 0, and then bisects at most 400 times. Each contrast costs $O(k)$ operations and one F tail, which is a continued fraction with a fixed cap of iterations.

**Theorem.** Under the normal model with a common variance and any group sizes, the intervals returned by the code cover all contrasts of the group means simultaneously with probability exactly $1 - \alpha$, the contrast tests control the family-wise error rate in the strong sense with error exactly $\alpha$ under the complete null, and the F-test of one-way ANOVA rejects exactly when the interval of some contrast excludes 0, the contrast $c_i = n_i(\bar y_i - \bar y)$ being one such contrast.

*Proof.* Lemmas 1 to 6. $\blacksquare$
