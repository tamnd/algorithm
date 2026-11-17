---
tag: GAQA42
kind: algorithm
slug: tajimas-d
name: Tajima's D
aliases:
- Tajima's D test
area: biology/population-genetics
level: core
summary: A neutrality test from the scaled difference between nucleotide diversity and Watterson's estimate. Selection or growth shifts its sign.
model: real-ram
complexity:
  vars: {n: the number of sequences, m: the number of aligned sites}
  time: {worst: Θ(n m), average: Θ(n m), best: Θ(n m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1989
  people: [Fumio Tajima]
  note: Tajima proposed in 1989 to test the neutral model by the scaled difference of two estimators of theta, the mean pairwise difference and S / a_n.
prereqs: [watterson-estimator, nucleotide-diversity, site-frequency-spectrum]
see_also: [infinite-sites-model, coalescent-simulation, mcdonald-kreitman-test, extended-haplotype-homozygosity, kingman-coalescent, effective-population-size]
sources:
  - paper: doi:10.1093/genetics/123.3.585
    title: Fumio Tajima, Statistical method for testing the neutral mutation hypothesis by DNA polymorphism, Genetics 123(3), 1989
    locator: pp. 585-595 (the statistic D, its constants, the bounds of D and the beta approximation for critical values)
  - paper: doi:10.1093/genetics/105.2.437
    title: Fumio Tajima, Evolutionary relationship of DNA sequences in finite populations, Genetics 105(2), 1983
    locator: pp. 437-460 (the variance of the mean pairwise difference)
  - paper: doi:10.1016/0040-5809(75)90020-9
    title: G. A. Watterson, On the number of segregating sites in genetical models without recombination, Theoretical Population Biology 7(2), 1975
    locator: pp. 256-276 (the mean and the variance of the number of segregating sites)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 4 (tests of the neutral model based on the site frequency spectrum)
---

Tajima's D tests whether a sample of DNA sequences fits the neutral model of a population of constant size. It compares two estimators of $\theta = 4N\mu$ that have the same mean under that model: the [mean pairwise difference](/nucleotide-diversity/) $\hat\pi$, and [Watterson's estimator](/watterson-estimator/) $S / a_n$ from the number of segregating sites $S$. Their difference, divided by an estimate of its standard deviation, is $D$. A value far below 0 means an excess of rare variants, which a recent selective sweep or population growth can cause; a value far above 0 means an excess of intermediate-frequency variants, which balancing selection, structure or a decline can cause. Like every test of this kind, it rejects the null model, not a specific cause.

## In plain words

Two numbers measure how much variation a sample has. One counts the places where the sequences are not all the same. The other takes two sequences at a time and counts how many places they differ, then averages over all pairs. A rare variant, carried by one sequence, counts fully in the first number but adds little to the second, because few pairs differ at it. A variant that splits the sample in half counts once in the first number and in many pairs in the second.

In a neutral population of steady size, the two numbers agree on average after a known correction. Tajima's D is their difference, put on a scale where about 0 is normal and values beyond about 2 in size are rare. The sign says which kind of variant is in excess.

## The problem

**Input.** A sample of $n \ge 4$ aligned sequences of $m$ sites each, without missing data.

**Output.** The statistic

$$D = \frac{\hat\pi - S / a_1}{\sqrt{e_1 S + e_2 S (S - 1)}},$$

where $S$ is the number of segregating sites, $\hat\pi$ is the mean number of pairwise differences, and $a_1$, $e_1$, $e_2$ depend only on $n$:

$$a_1 = \sum_{i=1}^{n-1} \frac{1}{i}, \qquad a_2 = \sum_{i=1}^{n-1} \frac{1}{i^2}, \qquad b_1 = \frac{n + 1}{3(n - 1)}, \qquad b_2 = \frac{2(n^2 + n + 3)}{9 n (n - 1)},$$

$$c_1 = b_1 - \frac{1}{a_1}, \qquad c_2 = b_2 - \frac{n + 2}{a_1 n} + \frac{a_2}{a_1^2}, \qquad e_1 = \frac{c_1}{a_1}, \qquad e_2 = \frac{c_2}{a_1^2 + a_2}.$$

$D$ is not defined when $S = 0$. For $n = 3$ every segregating site splits the sample 1 to 2 or 2 to 1, so $\hat\pi = S / a_1$ always and $c_1 = c_2 = 0$; the test needs $n \ge 4$.

**The null model.** Neutral mutations under the [infinite sites model](/infinite-sites-model/), a constant population size, random mating, no structure, and no recombination inside the region (the variance formula assumes one tree).

## The algorithm

```pseudo id=main
TAJIMA-D(H)
L1  S ← 0; P ← 0
L2  for each site j = 1, ..., m do
L3      if column j is not all equal then S ← S + 1
L4      P ← P + the number of pairs of sequences that differ at site j
L5  π ← P / (n(n − 1)/2)
L6  compute a_1, e_1 and e_2 from n
L7  if S = 0 then return undefined
L8  return (π − S / a_1) / sqrt(e_1 S + e_2 S (S − 1))
```

Line L4 does not look at pairs. If the alleles of column $j$ occur $c_1, \ldots, c_r$ times, with $\sum c = n$, the number of differing pairs is $(n^2 - \sum_i c_i^2)/2$; for two alleles this is $c(n - c)$. So one pass over the alignment gives both $S$ and $\hat\pi$.

Tajima suggested comparing $D$ with a beta distribution on the interval $[D_{\min}, D_{\max}]$ of possible values, with mean 0 and variance 1. Many programs use the standard normal instead, and others get the null distribution by [coalescent simulation](/coalescent-simulation/). The implementation returns $D$ and the limits of $D_{\min}$ and $D_{\max}$, and leaves the choice of null distribution to the caller.

## Example

The sample of the [infinite sites model](/infinite-sites-model/) page has $n = 5$:

| copy | s1 | s2 | s3 | s4 | s5 | s6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 1 | 1 | 1 | 0 |

The derived counts are $(2, 1, 2, 3, 1, 1)$, so $S = 6$, and line L4 adds $c(5 - c) = 6, 4, 6, 6, 4, 4$, a total of $P = 30$. Line L5 gives $\hat\pi = 30/10 = 3$.

For $n = 5$ the constants are $a_1 = 25/12 = 2.083333$, $a_2 = 1.423611$, $b_1 = 0.5$, $b_2 = 0.366667$, $c_1 = 0.02$, $c_2 = 0.022667$, $e_1 = 0.0096$ and $e_2 = 0.0039325$. The numerator is $3 - 2.88 = 0.12$. The denominator is $\sqrt{0.0096 \cdot 6 + 0.0039325 \cdot 30} = \sqrt{0.175576} = 0.419018$. So $D = 0.2864$, well inside the range of the null model: the sample has slightly more intermediate variants than expected, and six sites are far too few to say more.

A second case: $n = 10$, $S = 10$ and $\hat\pi = 3$, where $S / a_1 = 3.5349$. With $e_1 = 0.0190605$ and $e_2 = 0.00494893$, $D = -0.5349 / \sqrt{0.190605 + 0.445404} = -0.6707$.

## Correctness

Lines L2 to L4 add, for each site, one to $S$ if it segregates and the number of differing pairs to $P$. A pair of sequences differs at $d_{jk}$ sites, so $P = \sum_{j < k} d_{jk}$, and line L5 gives the mean pairwise difference. Line L8 is the formula.

The test is valid because of three facts under the null model. First, $E[\hat\pi] = \theta$ (Tajima 1983) and $E[S / a_1] = \theta$ (Watterson 1975), so the numerator $d = \hat\pi - S / a_1$ has mean 0. Second, $\operatorname{Var}[d] = c_1 \theta + c_2 \theta^2$. This comes from $\operatorname{Var}[\hat\pi] = b_1 \theta + b_2 \theta^2$, $\operatorname{Var}[S] = a_1 \theta + a_2 \theta^2$, and the covariance of $\hat\pi$ and $S$. Third, since $E[S] = a_1 \theta$ and $E[S(S - 1)] = (a_1^2 + a_2)\theta^2$, the square of the denominator, $e_1 S + e_2 S(S - 1)$, has mean exactly $c_1 \theta + c_2 \theta^2$. So $D$ is $d$ divided by an unbiased estimate of its variance, under the root. The proofs of the first and third facts are below; the second is Tajima's computation, which the tests check by simulation.

$D$ itself has mean close to 0 and variance close to 1, but not exactly, because the denominator is random and depends on $S$.

## Complexity

- **Time.** Lines L3 and L4 read every character once and count the alleles of a column, so the time is $\Theta(n m)$ in every case. Line L6 takes $O(n)$ time.
- **Space.** A few counters and the allele counts of one column: $\Theta(1)$ for a fixed alphabet.
- **From a VCF file.** Only the variant sites matter, so the work is linear in the size of the genotype matrix of the variants.
- **Windows.** Genome scans compute $D$ in sliding windows. With prefix sums of the per-site values of $S$ and $P$, every window costs $O(1)$ after one pass.

## Properties

- **Scaled.** Division by the estimated standard deviation puts $D$ on a common scale, so values from regions with different mutation rates can be compared roughly.
- **Bounded.** For a given $n$, $D$ is smallest when all sites are singletons ($\hat\pi = 2S / n$) and largest when every site splits the sample as evenly as possible. As $S \to \infty$ these bounds tend to $(2/n - 1/a_1)/\sqrt{e_2}$ and $(h_n - 1/a_1)/\sqrt{e_2}$, with $h_n = n/(2(n-1))$ for even $n$ and $(n+1)/(2n)$ for odd $n$. For $n = 5$ the limits are $-1.276$ and $1.914$; for $n = 10$, $-2.182$ and $2.872$; for $n = 50$, $-3.011$ and $4.714$. With small samples, values beyond $\pm 2$ cannot occur at all.
- **Not exactly normal or beta.** The beta approximation and the normal approximation are both approximations; with few sites, the true null distribution is discrete and skewed.
- **No outgroup needed.** Both $\hat\pi$ and $S$ are the same whichever allele is ancestral.
- **Conservative with recombination.** Recombination makes the sites partly independent and shrinks the true variance of $d$, while the formula assumes one tree. So the test rejects less often than its nominal level.

## Variants and improvements

- **Fu and Li's D and F.** They compare the number of singletons (or external mutations) with $S$ or $\hat\pi$. They need an outgroup for the unfolded version.
- **Fay and Wu's H.** Compares $\hat\pi$ with an estimator that weights high-frequency derived variants, which a sweep leaves near the selected site. It needs the ancestral state.
- **Normalized versions.** Zeng and coauthors normalized $H$ and proposed the joint use of $D$ and $H$, which separates sweeps from demography better than either alone.
- **Simulated null distributions.** Instead of a fixed approximation, simulate the null with [coalescent simulation](/coalescent-simulation/), with recombination and with a demographic model fitted to the genome-wide data. Then $D$ tests selection against that demography and not against constant size.
- **Per-window scans.** Compute $D$ in windows along the genome and look for outliers relative to the genome-wide distribution, which removes most of the shared effect of demography.

## When to use it

Use it as a first check of whether a gene or region fits the neutral model, and in genome scans to find candidate regions under selection, compared with the genome-wide distribution. It needs only aligned sequences and no outgroup. For a test of positive selection in coding genes that uses divergence from another species, use the [McDonald-Kreitman test](/mcdonald-kreitman-test/). For recent, incomplete sweeps that are not yet visible in the frequency spectrum, use haplotype statistics such as [extended haplotype homozygosity](/extended-haplotype-homozygosity/).

## Pitfalls

- **Demography mimics selection.** Population growth gives negative $D$ genome-wide, and a bottleneck or structure in the sample can give positive $D$. A significant $D$ under the constant-size null model does not prove selection.
- **Sequencing errors.** False singletons push $D$ down. Low coverage, which misses rare variants, pushes it up.
- **Missing data.** The formula assumes the same $n$ at every site. Drop or impute missing calls first, or use a version with per-site sample sizes.
- **Sample size.** $n$ is the number of sequences (twice the number of diploid individuals), not the number of individuals.
- **Small $S$.** With few segregating sites the test has little power, and the null distribution is far from any continuous approximation.
- **Pooled samples.** Samples from several populations have an excess of intermediate variants, and $D > 0$ then reflects the sampling scheme.

## Implementations

## History

Tajima published the test in Genetics in 1989, building on his 1983 result for the variance of the mean pairwise difference and on Watterson's 1975 results for the number of segregating sites. It was the first widely used neutrality test based on the frequency spectrum, and Fu and Li (1993) and Fay and Wu (2000) followed with tests that use the frequencies more directly. Most population genetics toolkits compute it.

## References
