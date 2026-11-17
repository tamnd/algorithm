---
tag: MQGC1J
kind: algorithm
slug: genomic-control
name: Genomic control
aliases:
- genomic inflation factor correction
- lambda GC correction
area: biology/population-genetics
level: core
summary: "Divides the association statistics of a scan by the inflation factor lambda, the median observed chi-squared over its null median 0.4549, to correct for stratification."
model: real-ram
complexity:
  vars: {M: the number of SNPs, N: the number of individuals}
  time: {worst: Θ(M N + M log M), average: Θ(M N + M log M), best: Θ(M N + M log M)}
  space: {extra: Θ(M)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1999
  people: [Bernie Devlin, Kathryn Roeder]
  note: "Devlin and Roeder proposed in 1999 to estimate the inflation of association statistics from many markers and to divide it out."
prereqs: [chi-squared-test-of-independence, p-value]
see_also: [genome-wide-association-study, ld-score-regression, mixed-model-association, genetic-principal-components, population-structure-inference, quickselect, order-statistic, multiple-comparisons-problem]
sources:
  - paper: doi:10.1111/j.0006-341X.1999.00997.x
    title: Bernie Devlin and Kathryn Roeder, Genomic control for association studies, Biometrics 55(4), 1999
    locator: pp. 997-1004 (the trend test, the inflation of its variance under structure and cryptic relatedness, and the estimate of lambda from the median)
  - paper: doi:10.2307/3001775
    title: Peter Armitage, Tests for linear trends in proportions and frequencies, Biometrics 11(3), 1955
    locator: pp. 375-386 (the test for a linear trend in proportions)
  - paper: doi:10.1038/ejhg.2011.39
    title: Jian Yang and coworkers, Genomic inflation factors under polygenic inheritance, European Journal of Human Genetics 19(7), 2011
    locator: pp. 807-812 (lambda grows with the sample size under polygenic inheritance without any structure)
  - paper: doi:10.1038/ng.3211
    title: Brendan K. Bulik-Sullivan and coworkers, LD Score regression distinguishes confounding from polygenicity in genome-wide association studies, Nature Genetics 47(3), 2015
    locator: pp. 291-295 (the LD score intercept as a measure of confounding, compared with lambda GC)
---

Genomic control corrects the test statistics of a [genome-wide association study](/genome-wide-association-study/) for population stratification and cryptic relatedness. These effects make the null statistics larger than a chi-squared law with 1 degree of freedom predicts, roughly by one common factor $\lambda$. Genomic control estimates $\lambda$ as the median of all $M$ statistics divided by 0.454936, the median of that chi-squared law, and divides every statistic by $\hat\lambda$. It uses only the statistics, so it costs nothing beyond the scan.

## In plain words

In a scan of a million genetic markers, almost all markers have nothing to do with the disease. Their test results should look like pure chance. If cases and controls come from groups of different ancestry, many markers look a little linked to the disease only because their frequency differs between the groups. Then the whole set of results is shifted upward. Genomic control compares the middle result of the scan with the middle result that pure chance gives. If the middle result is 30 percent too large, it shrinks every result by 30 percent. The middle is used because a few real hits at the top do not move it.

## The problem

**Input.** Genotypes of $N$ individuals at $M$ SNPs, as dosages $x_{ij} \in \{0, 1, 2\}$, and case status $y_i \in \{0, 1\}$. Or directly a list of $M$ statistics that are chi-squared with 1 degree of freedom under the null.

**Model.** For a null SNP, the statistic is $T_j = \lambda Z_j$, with $Z_j$ chi-squared with 1 degree of freedom and the same $\lambda \ge 1$ for all SNPs (Devlin and Roeder 1999). Most SNPs are null.

**Output.** The estimate $\hat\lambda$, the corrected statistics $T_j / \hat\lambda$ and their p-values.

For a case-control study, the statistic is the Cochran-Armitage trend test, which equals $N r_j^2$, where $r_j$ is the correlation of the dosage at SNP $j$ with the case status. It is the score test of a logistic or linear regression of status on dosage, and it does not assume [Hardy-Weinberg proportions](/hardy-weinberg-principle/), unlike the allele-count [chi-squared test](/chi-squared-test-of-independence/).

## The algorithm

```pseudo id=main
GENOMIC-CONTROL(x, y)
L1  for j ← 1 to M do T_j ← N r_j^2, the trend statistic of SNP j
L2  m ← median of T_1, ..., T_M
L3  λ ← max(1, m / 0.454936)
L4  for j ← 1 to M do T_j ← T_j / λ
L5      p_j ← P(χ²_1 > T_j)
L6  return λ, T, p
```

Line L1 needs five integer sums per SNP: $N (N S_{xy} - S_x S_y)^2 / ((N S_{xx} - S_x^2)(N S_y - S_y^2))$. The median of line L2 can come from a sort or from [quickselect](/quickselect/). The floor at 1 in line L3 keeps a scan with less spread than chance from being made larger.

## Example

**One SNP.** Take 100 cases with dosages 0, 1, 2 in the counts 20, 50, 30, and 100 controls with the counts 35, 45, 20. So $N = 200$, $S_x = 195$, $S_{xx} = 295$, $S_y = 100$ and $S_{xy} = 110$. Then $N S_{xy} - S_x S_y = 2500$, $N S_{xx} - S_x^2 = 20975$ and $N S_y - S_y^2 = 10000$, so

$$T = \frac{200 \cdot 2500^2}{20975 \cdot 10000} = \frac{5000}{839} = 5.9595,$$

with a p-value of 0.0146.

**A small scan.** Take five statistics $0.10, 0.30, 0.62, 0.95, 2.40$. The median is $0.62$, so $\hat\lambda = 0.62 / 0.454936 = 1.3628$. The corrected statistics are $0.0734, 0.2201, 0.4549, 0.6971, 1.7610$. The largest one had the p-value 0.121 and now has 0.184. A real scan has far more SNPs; five values only show the arithmetic.

## Correctness

Line L1 is right because the Armitage statistic on the $2 \times 3$ table, with the scores 0, 1, 2, reduces to $N r^2$ when the cell counts are written as sums over individuals. Under the model, the median of $\lambda Z$ is $\lambda \cdot 0.454936$, because $0.454936 = \Phi^{-1}(3/4)^2$ is the median of the chi-squared law with 1 degree of freedom. The sample median of many SNPs converges to this value, so $\hat\lambda \to \lambda$, and by Slutsky's theorem the corrected statistics are chi-squared with 1 degree of freedom in the limit. The median, unlike the mean, changes little when a small share of the SNPs have real effects. The full proof is below.

## Complexity

- **Time.** Line L1 is one pass over the $N M$ genotypes. The median costs $\Theta(M \log M)$ by sorting or $\Theta(M)$ by selection. The rest is $\Theta(M)$.
- **Space.** $\Theta(M)$ for the statistics. The genotypes can be streamed one SNP at a time.
- **From summary statistics.** If only the $M$ statistics or p-values are given, the method costs $\Theta(M)$ with selection and needs no genotypes. This is why it is easy to use in a meta-analysis.

## Properties

- **One factor for all SNPs.** Every statistic is divided by the same $\hat\lambda$, so the ranking of SNPs does not change.
- **Robust to a few hits.** The median ignores the size of the largest values. A small fraction of real associations moves $\hat\lambda$ only a little.
- **Conservative for real signal.** Dividing by $\hat\lambda$ also shrinks the statistics of real hits, so power goes down.
- **Works for any 1-df test.** The method applies to any test that is chi-squared with 1 degree of freedom under the null, for example a Wald test in a regression. For a test with $k$ degrees of freedom, use the median of that law.
- **Reported as a quality measure.** Studies report $\hat\lambda$ with the results. A value near 1 means little inflation of the bulk of the statistics.

## Variants and improvements

- **Scale to a fixed sample size.** $\hat\lambda$ grows with $N$ for the same structure, so studies also report $\lambda_{1000} = 1 + (\hat\lambda - 1)(1/N_{\text{cases}} + 1/N_{\text{controls}}) / (1/1000 + 1/1000)$, the value for 1000 cases and 1000 controls.
- **Principal components.** Adding the top [genetic principal components](/genetic-principal-components/) as covariates corrects each SNP by its own pattern of frequency differences, instead of one factor for all.
- **Mixed models.** [Mixed model association](/mixed-model-association/) models structure and relatedness with a random effect whose covariance is the genetic relationship matrix.
- **LD score regression.** The intercept of [LD score regression](/ld-score-regression/) measures confounding, while $\hat\lambda$ mixes confounding with real polygenic signal.
- **Second round.** In a meta-analysis, genomic control is applied to each study and then again to the combined result.

## When to use it

- As a check of every GWAS: report $\hat\lambda$, and look at a quantile-quantile plot of the statistics.
- To correct a scan of modest size with mild structure, when genotypes for a better method are not available, for example in a meta-analysis of summary statistics.
- For candidate gene studies with a set of null markers typed only to estimate $\lambda$, which was the original design of Devlin and Roeder.

## Pitfalls

- **Polygenic inflation is not confounding.** With many causal variants of small effect, the median statistic grows with $N$ even without any structure (Yang and coworkers 2011). Genomic control then removes real signal. LD score regression separates the two.
- **Differential inflation.** Structure inflates SNPs with large frequency differences between populations more than others. One constant over-corrects some SNPs and under-corrects others.
- **Biased SNP sets.** Estimate $\hat\lambda$ from all SNPs or from a random set. A set chosen for a candidate region, or filtered by p-value, gives a wrong median.
- **Deflation.** A $\hat\lambda$ below 1 suggests an error, such as over-correction upstream or a wrong test. The floor at 1 hides it.
- **Multiple testing.** Genomic control does not replace the genome-wide threshold of the [multiple comparisons problem](/multiple-comparisons-problem/).

## Implementations

## History

Bernie Devlin and Kathryn Roeder (1999) showed that population structure and cryptic relatedness inflate the variance of the Armitage trend test by a factor that is roughly the same at every marker, and that this factor can be estimated from markers unlinked to the trait. They proposed the median for robustness. The method became a standard check and correction in genome-wide association studies. Later work showed that the inflation factor also grows under polygenic inheritance, and LD score regression (2015) gave a way to tell the two apart.

## References
