---
title: The genotype caller returns the posterior of each genotype and its MAP genotype
proves: [correctness]
status: full
---

Fix a biallelic site with reference allele $r$ and alternate allele $a \ne r$ in a diploid sample. The data $D$ are $n$ pairs $(b_i, Q_i)$: the base $b_i$ that read $i$ shows at the site and its Phred quality, with $e_i = 10^{-Q_i/10}$. The genotype $g \in \{0, 1, 2\}$ is the number of chromosomes that carry $a$. The model has three parts.

1. Read $i$ comes from one of the two chromosomes, each with probability $1/2$, independently of the other reads.
2. Given the allele $x$ of that chromosome, the read shows $b_i$ with probability $P(b_i \mid x) = 1 - e_i$ if $b_i = x$ and $e_i / 3$ otherwise.
3. Given $g$, the reads are independent, and $g$ has the prior $\pi = (\pi_0, \pi_1, \pi_2)$ with $\pi_g \ge 0$ and $\sum_g \pi_g = 1$.

We assume $0 < e_i < 1$ in floating point, that is, $Q_i > 0$ and not so large that $e_i$ underflows to 0. Then every factor below has a finite logarithm.

**Lemma 1 (one read).** $P(b_i \mid g) = \frac{g}{2} P(b_i \mid a) + \bigl(1 - \frac{g}{2}\bigr) P(b_i \mid r)$.

*Proof.* Under genotype $g$, $g$ of the two chromosomes carry $a$ and $2 - g$ carry $r$. By part 1 the read comes from a chromosome with $a$ with probability $g/2$, and from one with $r$ with probability $1 - g/2$. The law of total probability over the two cases gives the formula. $\square$

**Lemma 2 (all reads).** $P(D \mid g) = \prod_{i=1}^{n} P(b_i \mid g)$. The same value is the sum, over the $2^n$ maps $c$ from the reads to the two chromosomes, of $\prod_i \frac12 P(b_i \mid x_{c(i)})$, where $x_1, x_2$ are the alleles of the chromosomes.

*Proof.* The first form is part 3 with Lemma 1. For the second form, the sum of a product over independent choices $c(1), \ldots, c(n)$, where factor $i$ depends only on $c(i)$, is the product of the sums: $\sum_c \prod_i f_i(c(i)) = \prod_i \sum_{j \in \{1, 2\}} f_i(j)$. With $f_i(j) = \frac12 P(b_i \mid x_j)$, the inner sum is Lemma 1. $\square$

The brute-force test of the implementation computes the second form.

**Lemma 3 (loop invariant).** After lines L2 to L5 have run for the first $j$ reads, $\mathrm{lp}[g] = \ln \pi_g + \sum_{i \le j} \ln P(b_i \mid g)$ for each $g$, with $\ln 0 = -\infty$.

*Proof.* Line L1 sets $\mathrm{lp}[g] = \ln \pi_g$, which is the claim for $j = 0$. Line L3 computes $e_j$, and line L5 adds $\ln\bigl(\frac g2 P(b_j \mid a) + (1 - \frac g2) P(b_j \mid r)\bigr)$, which is $\ln P(b_j \mid g)$ by Lemma 1. The term is finite: $P(b_j \mid a)$ and $P(b_j \mid r)$ are each $1 - e_j$ or $e_j / 3$, both positive for $0 < e_j < 1$, and the term is a mixture of the two with weights that sum to 1. $\square$

So after the loop, $\mathrm{lp}[g] = \ln\bigl(\pi_g P(D \mid g)\bigr) = \ln P(g, D)$ by Lemma 2.

**Theorem.** Line L7 gives $\mathrm{post}[g] = P(g \mid D)$ for each $g$. Line L8 returns a genotype of largest posterior, the smallest one if several tie. The returned GQ is $-10 \log_{10}\bigl(1 - P(\hat g \mid D)\bigr)$ for the returned genotype $\hat g$, and QUAL is $-10 \log_{10} P(g = 0 \mid D)$.

*Proof.* Line L6 computes $z = \ln \sum_g e^{\mathrm{lp}[g]}$ by the log-sum-exp identity $\ln \sum_g e^{x_g} = m + \ln \sum_g e^{x_g - m}$ with $m = \max_g x_g$, which holds for any real $m$. Since at least one $\pi_g > 0$ and every likelihood is positive, $m$ is finite. So $z = \ln \sum_g P(g, D) = \ln P(D)$, and by [Bayes' theorem](/bayes-theorem/) $e^{\mathrm{lp}[g] - z} = P(g, D) / P(D) = P(g \mid D)$, which is line L7.

The posterior is $e^{\mathrm{lp}[g] - z}$ with the same $z$ for each $g$, and $x \mapsto e^{x - z}$ is increasing, so the order of the posteriors is the order of the values $\mathrm{lp}[g]$. Line L8 takes the largest $\mathrm{lp}[g]$ and breaks ties by the key $-g$, which picks the smallest $g$.

Line L9 computes $w = \ln \sum_{g \ne \hat g} e^{\mathrm{lp}[g]} - z = \ln \sum_{g \ne \hat g} P(g \mid D) = \ln\bigl(1 - P(\hat g \mid D)\bigr)$, and GQ is $-10 w / \ln 10 = -10 \log_{10}(1 - P(\hat g \mid D))$. If every other genotype has prior 0, then $w = -\infty$ and GQ is $+\infty$, the limit of the formula. In the same way QUAL is $-10 (\mathrm{lp}[0] - z) / \ln 10 = -10 \log_{10} P(g = 0 \mid D)$, and $+\infty$ if $\pi_0 = 0$. $\square$

**Numerical range.** The code never forms $P(D \mid g)$ itself. Each $\mathrm{lp}[g]$ is a sum of $n$ logarithms, each between $\ln(e_{\min}/3)$ and 0, so it stays a finite double for any pileup that real data give, and the subtraction of $m$ in log-sum-exp keeps each exponent at most 0. So a pileup of thousands of reads, whose likelihood is below the smallest positive double, still gives correct posteriors.

**Cost.** Each read costs a constant number of operations for the three genotypes, so the time is $\Theta(n)$ and the extra space is $O(1)$.

**Choice of the alternate allele.** `call_site` picks $a$ as the most common base other than $r$ in the pileup, before the posterior is computed. The theorem is about the posterior given that choice. It is not the posterior over all three possible alternate alleles, which would need the ten genotypes of four alleles.
