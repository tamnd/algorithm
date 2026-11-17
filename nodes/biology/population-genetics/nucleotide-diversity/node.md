---
tag: SPH0ZW
kind: definition
slug: nucleotide-diversity
name: Nucleotide diversity
aliases:
- Tajima's pi
- mean pairwise difference
area: biology/population-genetics
level: core
summary: The average number of differences per site between two sequences drawn from a sample, an estimator of theta under neutrality.
history:
  year: 1979
  people: [Masatoshi Nei, Wen-Hsiung Li]
  note: Nei and Li defined nucleotide diversity in 1979 as the average number of nucleotide differences per site between two randomly chosen sequences.
prereqs: [infinite-sites-model, kingman-coalescent]
see_also: [watterson-estimator, site-frequency-spectrum, tajimas-d, fixation-index, allele-frequency, coalescent-simulation, jukes-cantor-model]
sources:
  - paper: doi:10.1073/pnas.76.10.5269
    title: Masatoshi Nei and Wen-Hsiung Li, Mathematical model for studying genetic variation in terms of restriction endonucleases, Proceedings of the National Academy of Sciences USA 76(10), 1979
    locator: pp. 5269-5273 (the definition of nucleotide diversity as the mean number of differences per site between two sequences)
  - paper: doi:10.1093/genetics/105.2.437
    title: Fumio Tajima, Evolutionary relationship of DNA sequences in finite populations, Genetics 105(2), 1983
    locator: pp. 437-460 (the mean and the variance of the average number of pairwise differences in a sample)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 4 (pairwise differences and estimators of theta)
---

Nucleotide diversity is the average number of differences between two sequences drawn at random from a sample, per site of the aligned region or per locus. Nei and Li defined it in 1979, and it is the most common measure of genetic variation in DNA data. Under the neutral [infinite sites model](/infinite-sites-model/), the per-locus value is an unbiased estimator of $\theta = 4N\mu$ (Tajima 1983). It weights each segregating site by how evenly its two alleles split the sample, so it gives a different view of the same data than [Watterson's estimator](/watterson-estimator/), and [Tajima's D](/tajimas-d/) compares the two.

## Definition

Take $n \ge 2$ aligned sequences of $m$ sites each. Let $d_{jk}$ be the number of sites at which sequences $j$ and $k$ carry different bases. The **mean pairwise difference** of the sample is

$$\hat\pi = \binom{n}{2}^{-1} \sum_{j < k} d_{jk},$$

and the **nucleotide diversity per site** is $\hat\pi / m$. Both are called $\pi$ in the literature; a value below 1, such as $0.001$, is per site, and a value such as $3$ is per locus. This page writes $\hat\pi$ for the per-locus value.

Nei and Li stated the population version with haplotype frequencies. If haplotype $i$ has frequency $x_i$ and haplotypes $i$ and $j$ differ at a fraction $\pi_{ij}$ of the sites, then $\pi = \sum_{i, j} x_i x_j \pi_{ij}$, the expected fraction of differing sites between two copies drawn with replacement. The sample version with the sample frequencies is multiplied by $n / (n - 1)$, to count pairs of two distinct copies. That gives the formula above, divided by $m$.

**As a sum over sites.** A site where $c$ of the $n$ sequences carry one allele and $n - c$ the other separates exactly $c(n - c)$ pairs. So

$$\hat\pi = \binom{n}{2}^{-1} \sum_{\text{sites}} c_j (n - c_j) = \binom{n}{2}^{-1} \sum_{i=1}^{n-1} i (n - i)\, \xi_i,$$

where $\xi_i$ is the [site frequency spectrum](/site-frequency-spectrum/). This takes $O(n m)$ time from the counts, against $O(n^2 m)$ for the sum over pairs, and it does not need to know which allele is ancestral, because $i(n - i)$ is the same for $i$ and $n - i$.

**Expectation (Tajima 1983).** Under the neutral infinite sites model with constant size, $E[\hat\pi] = \theta$.

*Proof.* Each $d_{jk}$ is the number of mutations on the path between $j$ and $k$ in the [Kingman coalescent](/kingman-coalescent/) tree. The two lineages coalesce at rate 1, so the path has two branches of mean length $1$ in units of $2N$ generations, and mutations fall at rate $\theta/2$ per branch. So $E[d_{jk}] = 2 \cdot 1 \cdot \theta / 2 = \theta$, and the mean of the $\binom{n}{2}$ terms has the same expectation. $\square$

The same result follows from the spectrum: $\binom{n}{2}^{-1} \sum_i i(n - i) \theta / i = \binom{n}{2}^{-1} \theta \sum_{i=1}^{n-1} (n - i) = \theta$.

**Variance (Tajima 1983).** Without recombination,

$$\operatorname{Var}[\hat\pi] = \frac{n + 1}{3(n - 1)} \theta + \frac{2(n^2 + n + 3)}{9 n (n - 1)} \theta^2.$$

For $n = 2$ this is $\theta + \theta^2$, the variance of the geometric law of the number of differences between two sequences. As $n \to \infty$ it tends to $\theta/3 + 2\theta^2/9$, not to 0: all pairs share one genealogy, and more sequences do not remove the randomness of the deep branches. For $\theta = 5$ the variance is $11.667$ at $n = 5$, $9.012$ at $n = 10$ and $7.524$ at $n = 50$. Watterson's estimator has the variance $\theta / a_n + \theta^2 b_n / a_n^2$, which is $10.600$, $6.577$ and $3.141$ at the same sample sizes and does tend to 0, slowly. So $\hat\pi$ has the larger variance, and it is the less efficient estimator of $\theta$ under the neutral model. Recombination lowers both variances, because sites then have partly independent trees.

## Examples and non-examples

**A sample of five.** The matrix of the [infinite sites model](/infinite-sites-model/) page,

| copy | s1 | s2 | s3 | s4 | s5 | s6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 1 | 1 | 1 | 0 |

has these pairwise differences:

| pair | 1,2 | 1,3 | 1,4 | 1,5 | 2,3 | 2,4 | 2,5 | 3,4 | 3,5 | 4,5 |
|---|---|---|---|---|---|---|---|---|---|---|
| $d_{jk}$ | 1 | 4 | 4 | 5 | 3 | 3 | 4 | 2 | 3 | 1 |

The sum is 30, so $\hat\pi = 30 / 10 = 3$. By sites, the counts $(2, 1, 2, 3, 1, 1)$ give $c(5 - c) = (6, 4, 6, 6, 4, 4)$, again a sum of 30. If the six sites lie in a region of $m = 1000$ aligned bases, the nucleotide diversity per site is $0.003$. Watterson's estimate from the same data is $6 / a_5 = 2.88$.

**Scale.** In humans, nucleotide diversity per site is about $0.001$: two copies of a genome differ at about one site in a thousand.

**Non-examples.**
- The number of segregating sites $S$ is not $\hat\pi$. A singleton adds $1$ to $S$ and only $2/n$ to $\hat\pi$; a site with a 50:50 split adds $1$ to $S$ and about $1/2 \cdot n/(n - 1)$ to $\hat\pi$.
- The fraction of sites that differ between two sequences of two species is a divergence, not a diversity. Under a [substitution model](/substitution-model/) it needs a correction for multiple hits, such as [Jukes-Cantor](/jukes-cantor-model/), before it estimates a distance. Within a species the per-site values are small, and the correction is usually skipped.
- Gene diversity (expected heterozygosity) $1 - \sum_i x_i^2$ counts whether two copies differ at all at a locus, not at how many sites. It belongs to the [infinite alleles model](/infinite-alleles-model/).

## Related definitions

- **Watterson's estimator** $S / a_n$, another unbiased estimator of $\theta$; see [Watterson's estimator](/watterson-estimator/).
- **Tajima's D** is $(\hat\pi - S / a_n)$ divided by an estimate of its standard deviation; see [Tajima's D](/tajimas-d/). A deficit of intermediate-frequency sites makes $\hat\pi$ small next to $S / a_n$ and $D$ negative.
- **Between-population diversity** $d_{XY}$: the mean number of differences per site between one sequence from population $X$ and one from population $Y$. With the within-population values it gives measures of differentiation such as the [fixation index](/fixation-index/).
- **Per-site values with missing data.** When some sequences have no base at some sites, a common definition sums, over the sites, the fraction of differing pairs among the pairs with data at that site, and divides by the number of sites with data. Tools differ in which sites they count in the denominator (all sites of the region, or only the sites with data), and the two choices give different values.

## References
