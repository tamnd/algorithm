---
title: TAJIMA-D computes D, and its numerator and squared denominator have the right means
proves: [correctness]
status: full
---

**Setting.** $H$ is an alignment of $n \ge 4$ sequences and $m$ sites without missing data. For sequences $j < k$, $d_{jk}$ is the number of sites where they differ, and $\hat\pi = \binom{n}{2}^{-1} \sum_{j<k} d_{jk}$. $S$ is the number of segregating sites. The constants $a_1, a_2, c_1, c_2, e_1, e_2$ are those of the page.

**Lemma 1.** At a site whose alleles occur $c_1, \ldots, c_r$ times, with $\sum_i c_i = n$, the number of pairs of sequences with different alleles is $(n^2 - \sum_i c_i^2)/2$.

*Proof.* Count ordered pairs $(j, k)$ with $j \ne k$. There are $n^2 - n$ of them, and $\sum_i (c_i^2 - c_i) = \sum_i c_i^2 - n$ have the same allele. So $n^2 - \sum_i c_i^2$ ordered pairs have different alleles, and each unordered pair is counted twice. $\square$

**Lemma 2.** After line L5, $S$ is the number of segregating sites and $\pi = \hat\pi$.

*Proof.* Line L3 adds one exactly for the sites that are not constant. By Lemma 1, line L4 adds to $P$ the number of pairs that differ at site $j$. Summed over the sites, $P = \sum_j \#\{\{a, b\} : a \ne b \text{ differ at } j\} = \sum_{a < b} d_{ab}$, since both sides count the pairs (site, pair of sequences) with a difference. Line L5 divides by the number of pairs. $\square$

By Lemma 2, line L8 returns the value $D$ of the definition when $S > 0$, and line L7 returns undefined when $S = 0$, where the denominator is 0.

For the rest, the sample comes from the null model: a Kingman coalescent tree with time in units of $2N$ generations, and given the tree, mutations as a Poisson process of rate $\theta/2$ on the branches, each at a new site.

**Lemma 3.** $E[\hat\pi] = \theta$.

*Proof.* For two sequences $j$ and $k$, the lineages of the pair alone form a Kingman coalescent of two: they merge after a time $T$ that is exponential with rate 1, so $E[T] = 1$. The path between $j$ and $k$ in the tree has length $2T$. Each mutation on that path, and no other, separates them, and under the infinite sites model each mutation is at its own site. So $d_{jk}$ is Poisson with mean $\theta T$ given $T$, and $E[d_{jk}] = \theta$. The mean over the pairs has the same expectation. $\square$

**Lemma 4.** $E[S] = a_1 \theta$ and $E[S(S - 1)] = (a_1^2 + a_2) \theta^2$.

*Proof.* Given the total branch length $L$, $S$ is Poisson with mean $\theta L / 2$, and $L = \sum_{k=2}^{n} k T_k$ with independent $T_k$ exponential of rate $\binom{k}{2}$. So $E[L] = \sum_k 2/(k-1) = 2 a_1$ and $\operatorname{Var}[L] = \sum_k 4/(k-1)^2 = 4 a_2$. For a Poisson variable with mean $\lambda$, $E[S(S - 1) \mid \lambda] = \lambda^2$. Hence $E[S] = \theta a_1$ and $E[S(S - 1)] = E[(\theta L/2)^2] = (\theta^2/4)(\operatorname{Var}[L] + E[L]^2) = \theta^2 (a_2 + a_1^2)$. $\square$

**Theorem.** Under the null model, the numerator $d = \hat\pi - S / a_1$ has $E[d] = 0$, and the squared denominator has

$$E[e_1 S + e_2 S(S - 1)] = c_1 \theta + c_2 \theta^2.$$

*Proof.* By Lemmas 3 and 4, $E[d] = \theta - a_1 \theta / a_1 = 0$. By Lemma 4 and the definitions $e_1 = c_1 / a_1$ and $e_2 = c_2 / (a_1^2 + a_2)$,

$$E[e_1 S + e_2 S(S - 1)] = \frac{c_1}{a_1} a_1 \theta + \frac{c_2}{a_1^2 + a_2} (a_1^2 + a_2) \theta^2 = c_1 \theta + c_2 \theta^2. \qquad \blacksquare$$

**Remarks.** Tajima (1989) showed that $\operatorname{Var}[d] = c_1 \theta + c_2 \theta^2$ under the null model without recombination, from $\operatorname{Var}[\hat\pi] = b_1 \theta + b_2 \theta^2$ (Tajima 1983), $\operatorname{Var}[S] = a_1 \theta + a_2 \theta^2$ and the covariance of $\hat\pi$ and $S$. Together with the theorem, the squared denominator is an unbiased estimate of $\operatorname{Var}[d]$. That variance is cited here and not proved. The tests check it, the variance of $\hat\pi$ and the theorem on 15000 samples simulated with $n = 10$ and $\theta = 5$, where $\operatorname{Var}[d] = 1.4503$ and $\operatorname{Var}[\hat\pi] = 9.0123$. Lemmas 3 and 4 hold with recombination too, since they use only the tree of one site or one pair at a time; the variance does not.
