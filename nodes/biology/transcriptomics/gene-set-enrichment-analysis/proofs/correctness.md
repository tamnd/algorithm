---
title: The GSEA running sum is a weighted Kolmogorov-Smirnov walk, and the absolute permutation p-value is valid
proves: [correctness]
status: full
---

We prove four facts. The running sum starts and ends at 0 and stays in $[-1, 1]$ (Lemma 1). With weight exponent $p = 0$, the enrichment score is the signed two-sample [Kolmogorov-Smirnov](/kolmogorov-smirnov-test/) statistic of the positions of the members against the positions of the other genes (Theorem 2). The p-value p_abs from label permutations is valid when the sample labels are exchangeable under the null hypothesis, both with full enumeration (Theorem 3) and with random shuffles (Theorem 4). The GSEA p-value p_sign, which compares a score only with null scores of the same sign, has no such guarantee, and we do not claim one. That the signal-to-noise ratio is a good gene score is a heuristic.

**Setting.** There are $N$ genes with scores $r_1, \dots, r_N$. Line L1 sorts them by decreasing score with a stable sort, so genes with equal scores keep their input order. Let $g_1, \dots, g_N$ be the genes in this order. The set $S$ has $N_H$ members, with $0 < N_H < N$. Line L2 sets the member weights $w_j = |r_{g_j}|^p$ and $N_R = \sum_{g_j \in S} w_j$; if $N_R = 0$ the code uses $w_j = 1$. Lines L3 to L6 compute
$$P(i) = \sum_{j \le i,\ g_j \in S}\frac{w_j}{N_R} - \sum_{j \le i,\ g_j \notin S}\frac{1}{N - N_H}, \qquad i = 0, \dots, N,$$
and line L7 keeps $\mathrm{ES} = P(i^*)$ for the first $i^*$ with the largest $|P(i)|$.

**Lemma 1 (range of the walk).** $P(0) = 0$, $P(N) = 0$, and $-1 \le P(i) \le 1$ for every $i$. So $-1 \le \mathrm{ES} \le 1$.

*Proof.* Write $P(i) = H(i) - M(i)$, where $H(i)$ is the first sum and $M(i)$ the second. Both are sums of nonnegative terms that grow with $i$, so $0 \le H(i) \le H(N)$ and $0 \le M(i) \le M(N)$. Here $H(N) = \sum_{g_j \in S} w_j/N_R = 1$, and $M(N) = (N - N_H)/(N - N_H) = 1$. So $P(N) = 0$ and $P(i) \in [-1, 1]$. $\square$

So ES is positive when the members gather at the top of the list, and negative when they gather at the bottom. In floating point, $P(N)$ can differ from 0 by a rounding error.

**Theorem 2 (the case p = 0).** With $p = 0$, $\mathrm{ES} = \pm D$, where $D = \max_x |F_S(x) - F_{\bar S}(x)|$ is the two-sample Kolmogorov-Smirnov statistic of the positions $\{j : g_j \in S\}$ against the positions $\{j : g_j \notin S\}$, with $F_S$ and $F_{\bar S}$ their empirical distribution functions. The sign is that of $F_S - F_{\bar S}$ at a point where the maximum is reached.

*Proof.* With $p = 0$, every $w_j = 1$ and $N_R = N_H$. So $H(i) = \#\{j \le i : g_j \in S\}/N_H = F_S(i)$ and $M(i) = F_{\bar S}(i)$. Both functions are step functions that change only at the integers $1, \dots, N$, so the supremum of $|F_S(x) - F_{\bar S}(x)|$ over all real $x$ is reached at an integer $i \in \{0, \dots, N\}$. Line L7 takes the value with the largest absolute value over exactly these $i$. $\square$

When the largest value $\max_i P(i)$ and the smallest value $\min_i P(i)$ have the same absolute value, the code keeps the one that comes first. The test file accepts either sign in this case. With $p = 1$, the steps of the members are proportional to $|r|$, so the walk is a weighted version of the same statistic, and its null distribution is no longer the Kolmogorov-Smirnov law. This is why GSEA uses permutations.

**Ties in the scores.** The walk depends on the order of the genes, and so on the order of genes with equal scores. The code keeps the input order. Another tie rule can give another ES. This is a choice, not a theorem.

**The permutation null.** Let $X$ be the expression matrix with $n$ sample columns, and let $L$ be the observed vector of labels with $n_A$ ones. For a labelling $\ell$, let $T(\ell, X)$ be the ES of $S$ when the genes are scored by the signal-to-noise ratio under $\ell$. The null hypothesis is exchangeability: for every permutation $\sigma$ of the samples, the matrix $X^\sigma$ with its columns permuted by $\sigma$ has the same law as $X$. Permuting the columns of the data and permuting the labels have the same effect on $T$: $T(L, X^\sigma) = T(L^{\sigma^{-1}}, X)$, where $L^{\sigma^{-1}}$ is $L$ with its entries moved by $\sigma^{-1}$.

**Theorem 3 (exact enumeration).** Let $\mathcal G$ be the set of all $M = \binom{n}{n_A}$ labellings with $n_A$ ones. With exact set to True, the code computes
$$p_{\text{abs}} = \frac{1 + \#\{\ell \in \mathcal G,\ \ell \ne L : |T(\ell, X)| \ge |T(L, X)|\}}{1 + (M - 1)} = \frac{\#\{\ell \in \mathcal G : |T(\ell, X)| \ge |T(L, X)|\}}{M}.$$
Under exchangeability, $P(p_{\text{abs}} \le u) \le u$ for every $u \in [0, 1]$.

*Proof.* The first equality is what the code does, since it skips $L$ in the loop over $\mathcal G$. For the second, add $L$ itself to the count.

For a fixed matrix $x$, write $\pi(\ell, x) = \#\{\ell' \in \mathcal G : |T(\ell', x)| \ge |T(\ell, x)|\}/M$, and let $A_u(x) = \{\ell \in \mathcal G : \pi(\ell, x) \le u\}$. If $A_u(x)$ is not empty, take $\ell^*$ in it with the smallest $|T(\ell^*, x)|$. Every $\ell \in A_u(x)$ has $|T(\ell, x)| \ge |T(\ell^*, x)|$, so $|A_u(x)| \le M\pi(\ell^*, x) \le Mu$.

Now let $\sigma$ be a uniformly random permutation of the samples, independent of $X$. By exchangeability, $X$ has the same law as $X^\sigma$, so $P(\pi(L, X) \le u) = P(\pi(L, X^\sigma) \le u)$. Permuting the columns of $x$ permutes the labellings in $\mathcal G$, so $\pi(L, X^\sigma) = \pi(L^{\sigma^{-1}}, X)$. Given $X$, the labelling $L^{\sigma^{-1}}$ is uniform on $\mathcal G$, because every labelling with $n_A$ ones is reached by the same number $n_A!(n - n_A)!$ of permutations. So
$$P(p_{\text{abs}} \le u) = E\left[\frac{|A_u(X)|}{M}\right] \le u. \qquad \square$$

**Theorem 4 (random shuffles).** With exact set to False, the code draws labellings $L_1, \dots, L_B$ by shuffling with the given random generator, and computes $p_{\text{abs}} = (1 + \#\{b : |T(L_b, X)| \ge |T(L, X)|\})/(1 + B)$. If each shuffle is a uniform permutation independent of the others and of $X$, then $P(p_{\text{abs}} \le u) \le u$ under exchangeability.

*Proof.* An in-place shuffle that is uniform gives a uniform arrangement whatever the starting order, so $L_b = L^{\sigma_b}$ for independent uniform permutations $\sigma_b$ (up to the side on which they act, which does not change the argument). Let $\rho$ be one more uniform permutation, independent of all the others, and let $Y = X^\rho$, which has the law of $X$ under the null hypothesis. Then $T(L, X) = T(L^{\tau_0}, Y)$ and $T(L_b, X) = T(L^{\tau_b}, Y)$ with $\tau_0 = \rho$ and $\tau_b = \sigma_b\rho$ in the matching order. Given $\rho$, the $\tau_b$ are independent and uniform, so $\tau_0, \tau_1, \dots, \tau_B$ are independent uniform permutations, independent of $Y$ in law. Hence the $B + 1$ values $|T(L, X)|, |T(L_1, X)|, \dots, |T(L_B, X)|$ are exchangeable. The rank argument of Theorem 3, applied to these $B + 1$ values, shows that the probability that the first one is among the values that give $p_{\text{abs}} \le u$ is at most $u$. $\square$

The added 1 in the numerator and the denominator is what makes Theorem 4 hold. Without it, $p$ can be 0 and the test is too liberal.

**The same-sign p-value.** GSEA compares a positive ES only with the nonnegative null scores, and a negative ES only with the negative ones. The number of null scores of each sign is random, and the comparison is not a rank among a fixed exchangeable collection, so the argument above does not apply. The code reports p_sign for comparison with the GSEA software and labels it as a convention. The normalized score NES, the ES divided by the mean absolute null score of the same sign, is a heuristic for comparing sets of different sizes.

**Phenotype against gene permutation.** Permuting sample labels keeps the correlation between genes, so the null includes the effect of coexpressed members. Permuting gene labels instead treats the members as a random set of genes. That null is too narrow when the members are correlated, and the p-values are then too small. This is a property of the model, not a theorem proved here.

**What the tests check.** The test file checks the page example, compares the walk with a brute force that recomputes $H(i)$ and $M(i)$ from their definitions, checks Theorem 2 against the Kolmogorov-Smirnov statistic computed from the two empirical distribution functions, checks the extreme cases $\mathrm{ES} = 1$ and $\mathrm{ES} = -1$, and checks the signal-to-noise ratio. It checks Theorem 3 by measurement: over 300 null data sets with exact enumeration, the fraction of p_abs values at or below $u$ must not exceed $u$ by more than a sampling tolerance.

**Complexity.** One enrichment score takes $O(N\log N)$ time for the sort and $O(N)$ for the walk. Scoring all genes takes $O(Nn)$. With $B$ permutations and $m$ sets, the total is $O(B(Nn + m N\log N))$; the sort can be shared between the sets, which gives $O(B(Nn + N\log N + mN))$. The extra space is $O(N + mB)$.
