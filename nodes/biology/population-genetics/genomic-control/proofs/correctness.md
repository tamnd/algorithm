---
title: The trend statistic is N r squared, and genomic control is consistent under a constant inflation
proves: [correctness]
status: full
---

There are two claims. The first is an identity for the statistic of line L1. The second says what the estimate of line L3 does under the model of Devlin and Roeder (1999).

**Lemma 1.** Let $N$ individuals have dosages $x_i \in \{0, 1, 2\}$ and status $y_i \in \{0, 1\}$, with $R$ cases and $S = N - R$ controls, both positive, and with the $x_i$ not all equal. Let $r_k$ and $s_k$ be the numbers of cases and controls with dosage $k$, and $n_k = r_k + s_k$. Then the Cochran-Armitage trend statistic with the scores $0, 1, 2$,

$$T = \frac{N \bigl[\sum_k k (S r_k - R s_k)\bigr]^2}{R S \bigl[N \sum_k k^2 n_k - (\sum_k k n_k)^2\bigr]},$$

equals $N r^2$, where $r$ is the Pearson correlation of $x$ and $y$, and also

$$N r^2 = \frac{N (N S_{xy} - S_x S_y)^2}{(N S_{xx} - S_x^2)(N S_y - S_y^2)},$$

with $S_x = \sum x_i$, $S_{xx} = \sum x_i^2$, $S_y = \sum y_i = R$ and $S_{xy} = \sum x_i y_i$.

*Proof.* The second form is the definition of $r^2$, multiplied by $N$, with numerator and denominator of $r$ both multiplied by $N$. Now $\sum_k k r_k = S_{xy}$ and $\sum_k k s_k = S_x - S_{xy}$, so

$$\sum_k k (S r_k - R s_k) = S S_{xy} - R (S_x - S_{xy}) = N S_{xy} - R S_x = N S_{xy} - S_x S_y.$$

Also $\sum_k k n_k = S_x$, $\sum_k k^2 n_k = S_{xx}$, and $R S = R (N - R) = N S_y - S_y^2$ since $y_i^2 = y_i$. Putting these into $T$ gives the second form. $\square$

So line L1 computes the trend test from five integer sums in one pass over the $N$ individuals.

**The model.** Devlin and Roeder model a null SNP $j$ in a structured or cryptically related sample as $T_j = \lambda Z_j$, where $Z_j$ follows the chi-squared law with 1 degree of freedom and $\lambda \ge 1$ is the same for all SNPs. Assume that $Z_1, \ldots, Z_M$ are identically distributed, and that the sample median of $T_1, \ldots, T_M$ converges in probability to the population median as $M \to \infty$ (for example, the SNPs are independent or weakly dependent, as unlinked SNPs are).

**Lemma 2.** The chi-squared law with 1 degree of freedom has the median $\mu = \Phi^{-1}(3/4)^2 = 0.454936\ldots$, where $\Phi$ is the standard normal distribution function.

*Proof.* If $Z = U^2$ with $U$ standard normal, then $\Pr(Z \le x) = \Pr(|U| \le \sqrt x) = 2 \Phi(\sqrt x) - 1$. This equals $1/2$ when $\Phi(\sqrt x) = 3/4$. $\square$

**Theorem.** Under the model, $\hat\lambda = \max(1, \operatorname{median}(T) / \mu)$ from line L3 converges in probability to $\lambda$, and for each fixed $j$ the corrected statistic $T_j / \hat\lambda$ of line L4 converges in law to the chi-squared law with 1 degree of freedom. So the p-values of line L5 are asymptotically uniform under the null.

*Proof.* The law of $T_j = \lambda Z_j$ has the median $\lambda \mu$, because scaling by $\lambda > 0$ keeps the order. Its distribution function is continuous and strictly increasing near $\lambda\mu$, so the population median is unique and, by assumption, the sample median converges in probability to $\lambda \mu$. Dividing by the constant $\mu$ gives $\operatorname{median}(T)/\mu \to \lambda$. The map $t \mapsto \max(1, t)$ is continuous and equals $t$ at $t = \lambda \ge 1$, so $\hat\lambda \to \lambda$ in probability by the continuous mapping theorem. Then $T_j / \hat\lambda = Z_j \cdot (\lambda / \hat\lambda)$, and $\lambda / \hat\lambda \to 1$ in probability, so by Slutsky's theorem $T_j / \hat\lambda$ converges in law to $Z_j$. If $Z$ is chi-squared with 1 degree of freedom, $\Pr(\text{chi2\_sf}(Z) \le \alpha) = \alpha$, which gives the last claim. $\square$

**Remark.** The theorem needs the model. If some SNPs have real effects, the median moves only a little as long as these SNPs are a small fraction of all SNPs, because the median ignores the size of the large values. If the inflation differs between SNPs, for example because it grows with the difference in allele frequency between populations, then one constant cannot correct every SNP. If many SNPs each have a small real effect, the median grows with $N$ and genomic control removes real signal. These are the limits listed on the page.
