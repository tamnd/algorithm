---
title: The one-way ANOVA statistic has the F distribution with (k - 1, N - k) degrees of freedom under the normal null
proves: [correctness, termination]
status: full
---

We prove that the total sum of squares splits into the between and within parts, that the two parts are independent scaled chi-square variables under the normal model, that the F statistic computed by the code has the $F_{k-1, N-k}$ law under $H_0$ for every sample size, and that with two groups it is the square of the pooled two-sample t statistic. The data are $y_{ij}$ for groups $i = 1, \dots, k$ and units $j = 1, \dots, n_i$, with $N = \sum n_i > k$. Write $\bar y_i$ for the group means, $\bar y = \frac1N\sum_{i,j} y_{ij}$ for the grand mean, $SSB = \sum_i n_i(\bar y_i - \bar y)^2$, $SSW = \sum_{i,j}(y_{ij} - \bar y_i)^2$ and $SST = \sum_{i,j}(y_{ij} - \bar y)^2$. The model is $y_{ij} = \mu_i + e_{ij}$ with the $e_{ij}$ iid $N(0, \sigma^2)$.

**Lemma 1 (the decomposition).** $SST = SSB + SSW$. In vector form, let $V_0 \subset \mathbb R^N$ be the span of the all-ones vector and $V_1$ the span of the $k$ group indicator vectors, with orthogonal projections $P_0$ and $P_1$. Then $P_1 y$ is the vector that holds $\bar y_i$ at every unit of group $i$, $P_0 y = \bar y\,\mathbf 1$, $SSB = \|(P_1 - P_0)y\|^2$, $SSW = \|(I - P_1)y\|^2$, and $P_1 - P_0$ and $I - P_1$ are orthogonal projections onto orthogonal subspaces of dimensions $k - 1$ and $N - k$.

*Proof.* Write $y_{ij} - \bar y = (y_{ij} - \bar y_i) + (\bar y_i - \bar y)$ and square. The cross term is $2\sum_i(\bar y_i - \bar y)\sum_j(y_{ij} - \bar y_i) = 0$, because the inner sum is $n_i\bar y_i - n_i\bar y_i = 0$. This gives $SST = SSW + SSB$. For the vector form: the group indicators are orthogonal, the $i$-th has squared norm $n_i$, so projecting $y$ on $V_1$ gives the coefficient $\langle y, \mathbf 1_i\rangle/n_i = \bar y_i$ on each indicator. In the same way $P_0 y = \bar y\mathbf 1$. Because $V_0 \subset V_1$, we have $P_1P_0 = P_0P_1 = P_0$, so $(P_1 - P_0)^2 = P_1 - P_0$ and $(P_1 - P_0)^\top = P_1 - P_0$: it is the orthogonal projection onto $V_1 \ominus V_0$, of dimension $k - 1$. $I - P_1$ projects onto $V_1^\perp$, of dimension $N - k$, and $(P_1 - P_0)(I - P_1) = P_1 - P_1 - P_0 + P_0 = 0$. The squared norms are the two sums by the coordinate formulas above. $\square$

**Lemma 2 (projections of a normal vector).** Let $Y \sim N(\mu, \sigma^2 I_N)$ and let $P$ and $Q$ be orthogonal projections with $PQ = 0$, of ranks $r$ and $s$. Then $\|PY\|^2/\sigma^2$ and $\|QY\|^2/\sigma^2$ are independent, with noncentral chi-square laws on $r$ and $s$ degrees of freedom and noncentralities $\|P\mu\|^2/\sigma^2$ and $\|Q\mu\|^2/\sigma^2$. If $P\mu = 0$, the first is central $\chi^2_r$.

*Proof.* The ranges of $P$ and $Q$ are orthogonal, because $\langle Pu, Qv\rangle = \langle u, PQv\rangle = 0$. Choose an orthonormal basis $h_1, \dots, h_N$ of $\mathbb R^N$ whose first $r$ vectors span the range of $P$ and whose next $s$ vectors span the range of $Q$. Let $H$ have these rows and set $U = HY$. $H$ is orthogonal, so $U \sim N(H\mu, \sigma^2 I_N)$: its coordinates are independent normal variables with variance $\sigma^2$. Now $\|PY\|^2 = \sum_{l \le r}U_l^2$ and $\|QY\|^2 = \sum_{r < l \le r+s}U_l^2$ are functions of disjoint sets of independent coordinates, so they are independent. A sum of $r$ squares of independent $N(m_l, \sigma^2)$ variables, divided by $\sigma^2$, is noncentral $\chi^2_r$ with noncentrality $\sum m_l^2/\sigma^2$, and here $\sum_{l \le r}m_l^2 = \|P\mu\|^2$. When the noncentrality is 0 the law is central. $\square$

This is the projection form of Cochran's theorem. The [hat matrix](/hat-matrix/) of the one-way model is $P_1$.

**Lemma 3 (the null law).** Under the model, $SSW/\sigma^2 \sim \chi^2_{N-k}$ for every $\mu$, and $SSB$ is independent of $SSW$ with $SSB/\sigma^2$ noncentral $\chi^2_{k-1}$ with noncentrality $\lambda = \sum_i n_i(\mu_i - \bar\mu)^2/\sigma^2$, where $\bar\mu = \sum n_i\mu_i/N$. Under $H_0: \mu_1 = \dots = \mu_k$, $\lambda = 0$ and

$$F = \frac{SSB/(k - 1)}{SSW/(N - k)} \sim F_{k-1, N-k}.$$

*Proof.* The mean vector $\mu$ lies in $V_1$, so $(I - P_1)\mu = 0$, and $(P_1 - P_0)\mu$ holds $\mu_i - \bar\mu$ at the units of group $i$. Lemma 2 with $P = P_1 - P_0$ and $Q = I - P_1$ (Lemma 1) gives the two laws and the independence. Under $H_0$, $\mu \in V_0$, so $\lambda = 0$. The ratio of two independent chi-square variables, each divided by its degrees of freedom, is $F$ by definition, and $\sigma^2$ cancels. $\square$

**Lemma 4 (the code computes $F$).** Line L1 sets $N = \sum n_i$. L2 sets $\bar y_i$. L3 sets $\sum n_i\bar y_i/N$, which is $\bar y$ because $n_i\bar y_i$ is the sum of group $i$. L4 and L5 compute $SSB$ and $SSW$ by their definitions, the second with the group mean subtracted before squaring. L6 forms $F$ with the degrees of freedom $k - 1$ and $N - k$, and L7 returns $p = P(F_{k-1, N-k} > F)$.

*Proof.* Each line is the formula it names, evaluated with exact summation of the terms up to floating point rounding (`math.fsum`). The code rejects $N \le k$ and $SSW = 0$, where $F$ is not defined. $\square$

**Lemma 5 (size).** Under $H_0$ the p-value of L7 is uniform on $[0, 1]$, so the test "reject when $p \le \alpha$", which is the test "reject when $F \ge F_{(k-1, N-k, 1-\alpha)}$", has size exactly $\alpha$. The power is $P(F' > F_{(k-1, N-k, 1-\alpha)})$ for a noncentral $F'$ with noncentrality $\lambda$, which increases with $\lambda$.

*Proof.* $F$ has a continuous law with distribution function $G$ under $H_0$ (Lemma 3), and $p = 1 - G(F)$. The probability integral transform makes $G(F)$ uniform. The two rules are the same event because $1 - G$ is strictly decreasing. The power formula is Lemma 3 under $H_1$. A noncentral chi-square variable with noncentrality $\lambda$ is stochastically increasing in $\lambda$: it is $(Z + \sqrt\lambda)^2 + W$ with $Z \sim N(0,1)$ and $W \sim \chi^2_{r-1}$ independent, and $P(|Z + \sqrt\lambda| > c)$ increases with $\lambda \ge 0$ for each $c > 0$, because the normal density is symmetric and unimodal. $\square$

**Lemma 6 ($F = t^2$ for two groups).** If $k = 2$, then $F = T^2$, where $T = (\bar y_1 - \bar y_2)/(S_p\sqrt{1/n_1 + 1/n_2})$ is the pooled [Student t](/student-t-test/) statistic with $S_p^2 = SSW/(N - 2)$. The p-values of the two-sided t-test and of the F-test are equal.

*Proof.* Let $d = \bar y_1 - \bar y_2$ and $N = n_1 + n_2$. Then $\bar y = (n_1\bar y_1 + n_2\bar y_2)/N$, so $\bar y_1 - \bar y = n_2 d/N$ and $\bar y_2 - \bar y = -n_1 d/N$. So $SSB = n_1n_2^2d^2/N^2 + n_2n_1^2d^2/N^2 = n_1n_2d^2/N$. With $k - 1 = 1$ and $SSW/(N - 2) = S_p^2$,

$$F = \frac{n_1n_2d^2}{N S_p^2} = \frac{d^2}{S_p^2(1/n_1 + 1/n_2)} = T^2,$$

because $1/n_1 + 1/n_2 = N/(n_1n_2)$. If $T \sim t_\nu$ then $T^2 \sim F_{1, \nu}$, and $P(F_{1,\nu} > t^2) = P(|T| > |t|)$, which is the two-sided p-value. $\square$

**Termination.** The code makes one pass to count, one pass for the group sums, one pass over the $k$ means, and one pass for the within-group squares, so it stops after $O(N)$ arithmetic operations. The F tail is the incomplete beta continued fraction of the shared helper, which stops at a relative change below $10^{-16}$ or after a fixed cap of iterations.

**Theorem.** For $k \ge 2$ groups of normal data with a common variance and $N > k$, the one-way ANOVA code returns $F = \frac{SSB/(k-1)}{SSW/(N-k)}$, with $SST = SSB + SSW$, and $F \sim F_{k-1, N-k}$ under $H_0: \mu_1 = \dots = \mu_k$ for every set of sample sizes, so the test has size exactly $\alpha$. With two groups $F$ is the square of the pooled t statistic and the two tests agree.

*Proof.* Lemmas 1 to 6. $\blacksquare$

The Welch variant in the same file is not covered by this theorem. Its $F$ law with estimated degrees of freedom is an approximation, and its size on the page is measured by simulation, not proved.
