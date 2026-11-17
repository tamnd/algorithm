---
tag: ZAM7QG
kind: definition
slug: fixation-index
name: Fixation index
aliases:
- FST
- Wright's F-statistics
area: biology/population-genetics
level: core
summary: "The fraction of genetic variance that lies between subpopulations, FST = (HT - HS) / HT, a measure of population differentiation."
history:
  year: 1951
  people: [Sewall Wright, Masatoshi Nei, Bruce S. Weir, C. Clark Cockerham, Richard R. Hudson]
  note: "Wright defined F_ST with F_IS and F_IT in 1951. Nei wrote it with heterozygosities in 1973. Weir and Cockerham (1984) and Hudson, Slatkin and Maddison (1992) gave estimators from samples."
prereqs: [allele-frequency, hardy-weinberg-principle]
see_also: [population-structure-inference, patterson-f-statistics, nucleotide-diversity, genetic-principal-components, linkage-disequilibrium, effective-population-size, coalescent-theory, genetic-drift]
sources:
  - paper: doi:10.1111/j.1469-1809.1949.tb02451.x
    title: Sewall Wright, The genetical structure of populations, Annals of Eugenics 15(1), 1951
    locator: pp. 323-354 (the coefficients F_IS, F_IT and F_ST, the relation between them, and the island model)
  - paper: doi:10.1073/pnas.70.12.3321
    title: Masatoshi Nei, Analysis of gene diversity in subdivided populations, Proceedings of the National Academy of Sciences USA 70(12), 1973
    locator: pp. 3321-3323 (G_ST as (H_T - H_S) / H_T for loci with any number of alleles)
  - paper: doi:10.1111/j.1558-5646.1984.tb05657.x
    title: Bruce S. Weir and C. Clark Cockerham, Estimating F-statistics for the analysis of population structure, Evolution 38(6), 1984
    locator: pp. 1358-1370 (the estimator theta as a ratio of variance components, with corrections for the sample sizes and the number of samples)
  - paper: doi:10.1093/genetics/132.2.583
    title: Richard R. Hudson, Montgomery Slatkin and Wayne P. Maddison, Estimation of levels of gene flow from DNA sequence data, Genetics 132(2), 1992
    locator: pp. 583-589 (F_ST as 1 - H_w / H_b from the mean differences within and between populations)
  - paper: doi:10.1101/gr.154831.113
    title: Gaurav Bhatia, Nick Patterson, Sriram Sankararaman and Alkes L. Price, Estimating and interpreting FST, the impact of rare variants, Genome Research 23(9), 2013
    locator: pp. 1514-1521 (the Hudson estimator with sample size corrections, and the ratio of averages over loci)
---

The fixation index $F_{ST}$ measures how much the allele frequencies of subpopulations differ, as the fraction of the genetic variation of the whole population that lies between the subpopulations. In Nei's form it is $(H_T - H_S)/H_T$, where $H_T$ is the expected heterozygosity of the pooled population and $H_S$ is the mean expected heterozygosity within subpopulations. It is 0 when all subpopulations have the same allele frequencies and 1 when each is fixed for a different allele. Wright introduced it in 1951 with two related coefficients, and it is the most common summary of [population structure](/population-structure-inference/). Several estimators from samples exist, and they do not give the same number on the same data.

## Definition

Take one biallelic locus and $s$ subpopulations with weights $w_1, \ldots, w_s > 0$ that sum to 1 (often equal weights $1/s$, or the relative sizes). Let $p_k$ be the frequency of allele $A$ in subpopulation $k$, and let $\bar p = \sum_k w_k p_k$.

**Heterozygosities.** Under [Hardy-Weinberg](/hardy-weinberg-principle/) proportions inside each subpopulation, the expected heterozygosity in subpopulation $k$ is $2 p_k (1 - p_k)$. Define

$$H_S = \sum_k w_k\, 2 p_k (1 - p_k), \qquad H_T = 2 \bar p (1 - \bar p).$$

**The fixation index.** For $0 < \bar p < 1$,

$$F_{ST} = \frac{H_T - H_S}{H_T} = \frac{\sigma_p^2}{\bar p (1 - \bar p)}, \qquad \sigma_p^2 = \sum_k w_k (p_k - \bar p)^2.$$

The second form follows from $H_T - H_S = 2\big(\sum_k w_k p_k^2 - \bar p^2\big) = 2 \sigma_p^2$. So $F_{ST}$ is the variance of the allele frequency among subpopulations, scaled by its largest possible value $\bar p (1 - \bar p)$, which is reached when each $p_k$ is 0 or 1. Hence $0 \le F_{ST} \le 1$. For a locus with alleles $1, \ldots, r$, Nei (1973) sums the heterozygosities over alleles, $H = 1 - \sum_i p_i^2$, and calls the ratio $G_{ST}$. For many loci, the usual summary is the ratio of the sums of the numerators and the denominators over the loci.

**The three coefficients of Wright.** Wright (1951) defined three coefficients as correlations between uniting gametes. Let $H_I$ be the observed heterozygosity of individuals, averaged over subpopulations. In the heterozygosity form that Nei (1973) used, they are $F_{IS} = 1 - H_I / H_S$ (the departure from Hardy-Weinberg inside subpopulations, for example by inbreeding), $F_{IT} = 1 - H_I / H_T$ and $F_{ST} = 1 - H_S / H_T$. They satisfy

$$1 - F_{IT} = (1 - F_{IS})(1 - F_{ST}),$$

because $H_I / H_T = (H_I / H_S)(H_S / H_T)$.

**A form for sequences.** Hudson, Slatkin and Maddison (1992) define $F_{ST} = 1 - H_w / H_b$, where $H_w$ is the mean number of differences between two sequences from the same subpopulation and $H_b$ between two sequences from different subpopulations. For one biallelic locus and two subpopulations, $H_w = p_1(1 - p_1) + p_2(1 - p_2)$ and $H_b = p_1(1 - p_2) + p_2(1 - p_1)$, so this $F_{ST}$ is $(p_1 - p_2)^2 / H_b$. It is a different quantity from Nei's $F_{ST}$; both are 0 for equal frequencies and 1 for fixed differences.

**Estimators.** Sample frequencies $\hat p_k$ make $\hat\sigma_p^2$ too large on average, because each $\hat p_k$ has its own sampling variance. Weir and Cockerham (1984) estimate $F_{ST}$ as $\theta$, a ratio of variance components from an analysis of variance of the allele indicators, with corrections for the sample sizes and for the number of sampled subpopulations. For two subpopulations with $n_1$ and $n_2$ sampled gene copies, the Hudson estimator of Bhatia and coauthors (2013) is

$$\hat F_{ST} = \frac{(\hat p_1 - \hat p_2)^2 - \frac{\hat p_1 (1 - \hat p_1)}{n_1 - 1} - \frac{\hat p_2 (1 - \hat p_2)}{n_2 - 1}}{\hat p_1 (1 - \hat p_2) + \hat p_2 (1 - \hat p_1)}.$$

The numerator and the denominator are unbiased for $(p_1 - p_2)^2$ and $H_b$: $E[(\hat p_1 - \hat p_2)^2] = (p_1 - p_2)^2 + \mathrm{Var}(\hat p_1) + \mathrm{Var}(\hat p_2)$, $E[\hat p (1 - \hat p)] = p (1 - p)(1 - 1/n)$ for a binomial sample, and $\hat p_1$ and $\hat p_2$ are independent. The ratio itself is not unbiased, and its value can be negative.

## Examples and non-examples

**Two subpopulations.** With equal weights, $p_1 = 0.2$ and $p_2 = 0.8$: $\bar p = 0.5$, $H_T = 0.5$, $H_S = 2 \cdot 0.2 \cdot 0.8 = 0.32$, and $F_{ST} = 0.18 / 0.5 = 0.36$. The variance form gives $0.09 / 0.25 = 0.36$ too. The Hudson form gives $0.36 / (0.04 + 0.64) = 0.529$ for the same frequencies, which shows that the two definitions differ.

**A rare variant.** $p_1 = 0.01$ and $p_2 = 0.03$ give Nei's $F_{ST} = 0.0001 / 0.0196 = 0.0051$. The average of the two single-locus values of these examples is $0.1826$, while the ratio of the sums is $(0.09 + 0.0001)/(0.25 + 0.0196) = 0.3342$. The average of ratios gives too much weight to loci with a small denominator, and Bhatia and coauthors recommend the ratio of averages.

**A sample.** With $n_1 = n_2 = 20$ gene copies and $\hat p_1 = 0.25$, $\hat p_2 = 0.7$, the Hudson estimator is $(0.2025 - 0.009868 - 0.011053)/0.6 = 0.3026$. Without the sample size corrections, the value is $0.3375$.

**Island model.** In Wright's island model with many islands of $N$ diploids each, a migration rate $m$ per generation and $m$ small, the equilibrium value is about $1/(1 + 4 N m)$; for $N m = 1$, this is $0.2$. This is an approximation for one idealized model, and turning an observed $F_{ST}$ into a number of migrants is not reliable for real populations.

**Non-example: no structure.** $p_1 = p_2 = 0.5$ give $H_S = H_T = 0.5$ and $F_{ST} = 0$. A large heterozygosity does not imply differentiation.

**Non-example: inbreeding.** A single random-mating subpopulation that is inbred has fewer heterozygotes than $H_S$, which raises $F_{IS}$, not $F_{ST}$. $F_{ST}$ uses only expected heterozygosities, so it does not see the genotype proportions inside subpopulations.

**Non-example: a monomorphic locus.** If $\bar p = 0$ or 1, then $H_T = 0$ and $F_{ST}$ is not defined for that locus. Summaries over loci skip it, or include it in the sums of numerators and denominators, where it adds 0.

## Related definitions

- **Coalescent view.** With $\bar T$ the mean coalescence time of two gene copies drawn from the whole population and $\bar T_0$ that of two copies from one subpopulation, $F_{ST} = (\bar T - \bar T_0)/\bar T$ under an infinite sites model with low mutation; see [coalescent theory](/coalescent-theory/). This is the Hudson form with expected differences, which are proportional to the times.
- **Drift.** In a subpopulation that splits from an ancestor and drifts for $t$ generations with size $N$, the variance of $p_k$ grows like $\bar p (1 - \bar p)\big(1 - (1 - 1/(2N))^t\big)$, which links $F_{ST}$ to [genetic drift](/genetic-drift/) and to the [effective population size](/effective-population-size/).
- **f-statistics.** The [Patterson f-statistics](/patterson-f-statistics/) use the unscaled quantity $(p_1 - p_2)^2$, which adds along the branches of a tree; $F_{ST}$ does not add, because of its denominator.
- **Diversity.** $H_S$ and $H_T$ for one site are the site versions of [nucleotide diversity](/nucleotide-diversity/) within and across subpopulations.
- **Structure methods.** [Population structure inference](/population-structure-inference/) and [principal components of genotypes](/genetic-principal-components/) look at many loci at once; $F_{ST}$ between the inferred groups is a common summary of their output.

## References
