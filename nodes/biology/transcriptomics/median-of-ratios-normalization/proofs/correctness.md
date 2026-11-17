---
title: Median-of-ratios size factors recover the true factors when more than half of the genes do not change
proves: [correctness]
status: full
---

We prove what the median-of-ratios estimator gets right in exact arithmetic. If the counts are exactly proportional, it returns the true size factors divided by their geometric mean (Lemma 1). It keeps this answer when fewer than half of the usable genes change in any way (Theorem 2). It also scales correctly: multiplying one sample by $c$ multiplies its factor relative to every other sample by $c$ (Lemma 3). The claim that real data satisfy the assumption of Theorem 2 is a modelling assumption. It is not proved here, and the page labels it as such.

**Setting.** Counts $K_{gj} \ge 0$ for genes $g = 1, \dots, n$ and samples $j = 1, \dots, m$. Let $G = \{g : K_{gj} > 0 \text{ for all } j\}$ be the usable genes, and assume $G$ is not empty. For $g \in G$, let $\ell_g = \frac1m\sum_{k=1}^m \ln K_{gk}$ be the log of the geometric mean, and let $\rho_{gj} = \ln K_{gj} - \ell_g$ be the log ratio. The algorithm returns $\hat s_j = \exp(\operatorname{median}_{g \in G}\rho_{gj})$, where the median of an even number of values is the mean of the two middle ones.

**Lemma 1 (exact proportional counts).** Suppose $K_{gj} = s_j q_g$ with $s_j > 0$ and $q_g > 0$ for every $g \in G$ and every $j$. Then $\hat s_j = s_j / \bar s$, where $\bar s = (\prod_k s_k)^{1/m}$ is the geometric mean of the true factors.

*Proof.* For $g \in G$, $\ell_g = \ln q_g + \frac1m\sum_k \ln s_k = \ln q_g + \ln\bar s$. So $\rho_{gj} = \ln s_j + \ln q_g - \ln q_g - \ln\bar s = \ln(s_j/\bar s)$. This does not depend on $g$, so every value in the median at line L8 equals $\ln(s_j/\bar s)$, and so does the median. $\square$

The factors are identified only up to one common constant. This is unavoidable, because the counts $K_{gj} = s_j q_g$ do not change when every $s_j$ is multiplied by $c$ and every $q_g$ is divided by $c$. The estimator fixes the constant by making the factors have geometric mean 1 in the exact case.

**Theorem 2 (robustness to a minority of changed genes).** Let $S \subseteq G$ be a set of genes with $K_{gj} = s_j q_g$ for $g \in S$ and all $j$, and suppose $|S| > |G|/2$. The other genes of $G$ may have any positive counts. Then $\hat s_j = s_j/\bar s$ for every $j$.

*Proof.* For $g \in S$ the computation of Lemma 1 holds gene by gene, because it uses only the counts of $g$: $\rho_{gj} = \ln(s_j/\bar s)$. So for each sample $j$, more than half of the values $\rho_{gj}$, $g \in G$, are equal to the same number $c_j = \ln(s_j/\bar s)$.

Now use a fact about medians. Let $x_{(1)} \le \dots \le x_{(N)}$ be sorted values, and suppose more than $N/2$ of them equal $c$. The values equal to $c$ fill one block of consecutive positions $a, \dots, b$ with $b - a + 1 > N/2$. Fewer than $N/2$ positions lie before the block and fewer than $N/2$ lie after it, so $a - 1 < N/2$ and $N - b < N/2$. If $N$ is odd, these give $a \le (N+1)/2 \le b$, so the middle position is in the block. If $N$ is even, they give $a \le N/2$ and $b \ge N/2 + 1$, so both middle positions are in the block. In both cases the median is $c$.

Hence $\operatorname{median}_{g \in G}\rho_{gj} = c_j$ and $\hat s_j = s_j/\bar s$ for every $j$. $\square$

So the constant is the same as in Lemma 1: the changed genes change neither the relative factors $\hat s_j/\hat s_k = s_j/s_k$ nor their common scale. The bound $|S| > |G|/2$ is the breakdown point of the median, and it cannot be improved in general: if exactly half of the genes are changed, they can all have $\rho_{gj}$ equal to a value $c_j' \ne c_j$, and the median of an even number of values is then $(c_j + c_j')/2$.

**Lemma 3 (scale equivariance).** Let $K'$ be $K$ with sample $j_0$ multiplied by $c > 0$, and let $\hat s'$ be the factors of $K'$. Then $\hat s'_{j_0}/\hat s'_k = c\,\hat s_{j_0}/\hat s_k$ for every $k \ne j_0$.

*Proof.* The set $G$ does not change, because $c > 0$. For $g \in G$, $\ell'_g = \ell_g + \frac1m\ln c$. So $\rho'_{gj} = \rho_{gj} - \frac1m\ln c$ for $j \ne j_0$, and $\rho'_{gj_0} = \rho_{gj_0} + \ln c - \frac1m\ln c$. Subtracting a constant from every value subtracts it from the median, so $\ln\hat s'_k = \ln\hat s_k - \frac1m\ln c$ and $\ln\hat s'_{j_0} = \ln\hat s_{j_0} + (1 - \frac1m)\ln c$. The difference is $\ln\hat s'_{j_0} - \ln\hat s'_k = \ln\hat s_{j_0} - \ln\hat s_k + \ln c$. $\square$

So sequencing a sample twice as deeply doubles its factor relative to the others, which is what a size factor must do.

**What the lines compute.** Lines L1 to L3 compute $\ell_g$ for $g \in G$, and the code marks the other genes with $-\infty$. Line L4 forms $G$, and line L5 fails when $G$ is empty, since then no ratio is defined. Lines L6 to L8 compute $\hat s_j$. The median at line L8 is the median of the log ratios, so for an even $|G|$ it is the log of the geometric mean of the two middle ratios. This is the definition used in the proofs above, and it equals the median of the ratios themselves when $|G|$ is odd, because $\exp$ is increasing.

**Complexity.** Lines L1 to L4 read each count once, which is $\Theta(nm)$ time. Line L8 uses a sort, so the medians take $O(m\,|G|\log|G|)$ time; a linear-time [selection](/selection-problem/) such as [quickselect](/quickselect/) makes this $O(m\,|G|)$ expected. The extra space is $\Theta(n)$.

**What the tests check.** The test file checks Lemma 1 on random factors, Theorem 2 with up to $|S| - 1$ changed genes of random size, Lemma 3 with four scale constants, and the page example. It also compares the code with a brute force that works on the plain ratio scale and sorts, and it measures the error on Poisson counts. That last check is a measurement, not a theorem.
