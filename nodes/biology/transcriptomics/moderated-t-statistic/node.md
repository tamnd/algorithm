---
tag: SC6381
kind: algorithm
slug: moderated-t-statistic
name: Moderated t-statistic
aliases:
- limma moderated t-test
area: biology/transcriptomics
level: core
summary: A t-test whose gene-wise variance is shrunk toward a common prior by empirical Bayes, which gains power with few samples.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples}
  time: {worst: Θ(n m + n log n), best: Θ(n m + n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Gordon K. Smyth]
  note: Smyth defined the moderated t-statistic for linear models of microarray data in Statistical Applications in Genetics and Molecular Biology in 2004, with a closed-form estimate of the prior and an exact t distribution under the null hypothesis. It is the core of the limma package.
prereqs: [student-t-test, empirical-bayes, linear-regression]
see_also: [empirical-bayes, james-stein-estimator, dispersion-shrinkage, differential-expression-analysis, student-t-test, benjamini-hochberg-procedure, conjugate-prior, quantile-normalization]
sources:
  - paper: doi:10.2202/1544-6115.1027
    title: Gordon K. Smyth, Linear models and empirical Bayes methods for assessing differential expression in microarray experiments, Statistical Applications in Genetics and Molecular Biology 3(1) (2004), Article 3
    locator: the hierarchical model with a scaled inverse chi-squared prior on the variances, the posterior variance, the moderated t with d0 + d degrees of freedom, and the estimation of the prior from the moments of the log variances
  - paper: doi:10.1186/gb-2014-15-2-r29
    title: Charity W. Law, Yunshun Chen, Wei Shi and Gordon K. Smyth, voom, precision weights unlock linear model analysis tools for RNA-seq read counts, Genome Biology 15(2) (2014), article R29
    locator: log counts per million with precision weights from the mean-variance trend, analysed with the moderated t-statistic
  - paper: doi:10.1214/16-AOAS920
    title: Belinda Phipson, Stanley Lee, Ian J. Majewski, Warren S. Alexander and Gordon K. Smyth, Robust hyperparameter estimation protects against hypervariable genes and improves power to detect differential expression, Annals of Applied Statistics 10(2) (2016), pages 946 to 963
    locator: the robust estimation of the prior degrees of freedom and the prior variance, and the trend of the prior variance over the mean expression
---

The moderated t-statistic is a t-test for one gene among thousands, in which the sample variance of the gene is replaced by a weighted mean of that variance and a prior variance estimated from all genes. With three samples per group, the sample variance of one gene has only 4 degrees of freedom, so it is often far too small or far too large, and the ordinary [t-test](/student-t-test/) ranks genes poorly. Smyth (2004) put a scaled inverse chi-squared prior on the gene variances, estimated its two parameters from the variances of all genes, and showed that, with the prior known, the statistic has an exact $t$ distribution with $d_0 + d$ degrees of freedom under the null hypothesis, where $d_0$ is the prior degrees of freedom. This is [empirical Bayes](/empirical-bayes/) with a [conjugate prior](/conjugate-prior/). It is the core of limma, for microarrays and, with voom weights, for RNA-seq. [Dispersion shrinkage](/dispersion-shrinkage/) applies the same idea to the dispersion of a negative binomial model, where there is no conjugate prior and no exact null distribution.

## In plain words

To decide whether a gene changed, you compare the difference between the groups with the spread of the gene's values. With three samples per group, that spread is a poor guess: by chance it can come out almost zero, which makes a tiny difference look very significant, or very large, which hides a real change. The moderated t-test also looks at how much a typical gene spreads, using all the genes. It then uses a mix of the gene's own spread and the typical spread. The fewer samples you have, the more the typical value counts. Because the mix contains more information, the test also counts it as if it had more samples, which gives it more power.

## The problem

**Input.** For each gene $g = 1, \dots, n$, its values in two groups of samples, $m$ samples in all, on a log scale such as log intensities or log counts per million.

**Output.** For each gene, a statistic $\tilde t_g$ and a two-sided p-value, and the prior parameters $d_0$ and $s_0^2$.

**Model.** The difference of the group means is $\hat\beta_g \sim N(\beta_g, v\sigma_g^2)$, with $v = 1/m_A + 1/m_B$. The pooled sample variance is $s_g^2 \sim \sigma_g^2\chi^2_d/d$, with $d = m - 2$, independent of $\hat\beta_g$. The prior is $1/\sigma_g^2 \sim \chi^2_{d_0}/(d_0s_0^2)$. In limma the same holds for any coefficient or contrast of a linear model per gene.

## The algorithm

```pseudo id=main
MODERATED-T(A, B)                             ▷ values of each gene in groups A and B
L1  for each gene g: β̂_g ← mean_A - mean_B;  s²_g ← pooled variance on d = m - 2 df;  v ← 1/m_A + 1/m_B
L2  e_g ← ln s²_g - ψ(d/2) + ln(d/2)                                   ▷ ψ: digamma
L3  ē ← mean of e;  w ← sample variance of e - ψ'(d/2)                  ▷ ψ': trigamma
L4  if w > 0 then d₀ ← 2 ψ'⁻¹(w);  s₀² ← exp(ē + ψ(d₀/2) - ln(d₀/2))
L5  else d₀ ← ∞;  s₀² ← mean of s²
L6  for each gene g: s̃²_g ← (d₀ s₀² + d s²_g) / (d₀ + d)               ▷ s₀² if d₀ = ∞
L7      t̃_g ← β̂_g / (s̃_g √v)
L8      p_g ← 2 P(T > |t̃_g|), with T ~ t on min(d₀ + d, n d) df
L9  return t̃, p, d₀, s₀²
```

Line L1 computes the usual statistics of each gene. Lines L2 to L5 estimate the prior by the method of moments on the log variances, as limma's fitFDist does without a covariate. Under the model, $\ln s_g^2 = \ln s_0^2 + \ln(\chi^2_d/d) - \ln(\chi^2_{d_0}/d_0)$, whose mean and variance are given by the digamma and trigamma functions. Line L2 removes the known mean of the $\chi^2_d$ part, and line L3 removes its known variance, so what is left of the variance belongs to the prior, and $\psi'(d_0/2) = w$ fixes $d_0$. If the observed variance of the $e_g$ is no larger than the sampling variance alone, the data are consistent with one common variance, and line L5 sets $d_0 = \infty$. Line L6 is the posterior variance, a weighted mean of $s_0^2$ and $s_g^2$ with weights $d_0$ and $d$. Lines L7 and L8 form the statistic and its p-value. The cap $nd$ on the degrees of freedom at line L8 follows limma: the prior cannot carry more information than all genes together. Before the logs, the code raises each $s_g^2$ to at least $10^{-5}$ times their median, so that a zero variance does not give $\ln 0$.

## Example

Three genes, three samples per group, so $d = 4$ and $v = 2/3$. Take the prior as given, $d_0 = 4$ and $s_0^2 = 0.05$, as if it had been estimated from many genes. The total degrees of freedom are 8.

| gene | group A | group B | $\hat\beta_g$ | $s_g^2$ | $\tilde s_g^2$ | t | p | $\tilde t_g$ | $\tilde p_g$ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5.1, 5.3, 5.2 | 4.6, 4.7, 4.8 | 0.5 | 0.01 | 0.03 | 6.12 | 0.0036 | 3.54 | 0.0077 |
| 2 | 7, 8, 9 | 6, 7.5, 6.6 | 1.3 | 0.785 | 0.4175 | 1.80 | 0.147 | 2.46 | 0.0391 |
| 3 | 3, 3.05, 2.95 | 2.6, 2.7, 2.65 | 0.35 | 0.0025 | 0.02625 | 8.57 | 0.0010 | 2.65 | 0.0294 |

For gene 1, $\tilde s_1^2 = (4 \cdot 0.05 + 4 \cdot 0.01)/8 = 0.03$ and $\tilde t_1 = 0.5/\sqrt{0.03 \cdot 2/3} = 3.54$. The ordinary t-test ranks gene 3 first, because its values happen to be very close; its variance of 0.0025 is a twentieth of the prior. The moderated test raises it to 0.02625 and ranks gene 3 below gene 1. Gene 2 has a large variance, which the prior lowers, so its p-value falls from 0.147 to 0.039. Each moderated p-value uses 8 degrees of freedom instead of 4.

## Correctness

The [proof](proofs/correctness.md) shows that, given the data of a gene, the precision $1/\sigma_g^2$ has a gamma posterior whose mean is $1/\tilde s_g^2$, which is the formula of line L6. It then proves the main theorem: when $\beta_g = 0$ and the prior parameters are the true ones, $\tilde t_g$ has a $t$ distribution with $d_0 + d$ degrees of freedom, for every $d_0 > 0$. So the p-values of line L8 are exact under the hierarchical model with a known prior. As $d_0 \to 0$ the statistic becomes the ordinary t, and as $d_0 \to \infty$ it becomes a z-like statistic with the common variance $s_0^2$. The proof also derives the moment equations that lines L2 to L4 solve. With an estimated prior, the $t_{d_0+d}$ law is an approximation, good when $n$ is large; this is a heuristic backed by Smyth's asymptotic argument and by simulation, not an exact result.

## Complexity

On a [real RAM](/real-ram/), line L1 reads every value once, which takes $\Theta(nm)$ time. The median used for the floor takes $O(n\log n)$ by sorting, and $O(n)$ with linear-time selection. Lines L2 to L8 take $O(1)$ time per gene, counting each special function as $O(1)$ for a fixed accuracy: the digamma and trigamma functions use a recurrence and an asymptotic series, the inverse trigamma uses Newton's method, and the $t$ tail uses a continued fraction for the incomplete beta function. The extra space is $\Theta(n)$.

## Properties

- **Exact under the model.** With a known prior, the null distribution is $t_{d_0+d}$, not an approximation.
- **More degrees of freedom.** The test behaves as if it had $d_0 + d$ degrees of freedom, so its critical values are smaller than those of the ordinary t-test, and its power is higher when the prior fits.
- **Between two extremes.** It interpolates between the gene-wise t-test ($d_0 = 0$) and a test with one common variance ($d_0 = \infty$), and the data choose the point.
- **Robust to tiny variances.** A gene with a variance near zero cannot get a huge statistic, since $\tilde s_g^2 \ge d_0s_0^2/(d_0 + d)$.
- **Order not kept.** The ranking by $\tilde t_g$ differs from the ranking by the ordinary t and from the ranking by fold change; it is a compromise between the two.

## Variants and improvements

- **Moderated F.** For several coefficients at once, the same posterior variance gives an F statistic with $d_0 + d$ denominator degrees of freedom.
- **Trended prior.** The prior variance $s_0^2$ is a smooth function of the mean expression of each gene, instead of a constant. This helps for RNA-seq log counts and for arrays where low intensities are noisier.
- **Robust prior.** Phipson et al. (2016) estimate $d_0$ and $s_0^2$ in a way that a few hypervariable genes cannot spoil, and give those genes a smaller prior weight.
- **voom.** Law et al. (2014) transform RNA-seq counts to log counts per million and give each value a precision weight from the trend of the variance over the mean. The weighted linear model then uses the moderated t.
- **Fudge factor.** Older methods, such as SAM, add a constant to the standard error of each gene. It has the same aim, but no null distribution in closed form, so they use permutations.
- **Count models.** For counts, [dispersion shrinkage](/dispersion-shrinkage/) in a negative binomial GLM replaces the variance shrinkage; edgeR's quasi-likelihood F test shrinks a second, gene-wise variance factor in the same way as limma.

## When to use it

Use it for microarray data after [quantile normalization](/quantile-normalization/), for other continuous omics data on a log scale, and for RNA-seq with voom, especially when there are few samples. It works best when the variances of the genes look like draws from one distribution, maybe with a trend over the mean. For raw counts with very low means, a negative binomial model is closer to the data. Correct the p-values for multiple testing with the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/), as part of [differential expression analysis](/differential-expression-analysis/).

## Pitfalls

- **Counts without a transformation.** The model assumes normal values with a variance that does not depend on the mean. Raw counts break both assumptions; use voom or a count model.
- **Too few genes.** The prior is estimated from the spread of the gene variances. With tens of genes, $d_0$ is very uncertain, and the exact null distribution no longer holds.
- **A prior that fits badly.** If a group of genes has much larger variances than the rest, a constant prior shrinks them too much and gives false positives. Use the robust or the trended prior.
- **Filtering after the fit.** The prior should be estimated from the genes that are tested. Removing many genes after the fit, or fitting on a selected set, changes $d_0$ and $s_0^2$.
- **Unequal variances between groups.** The pooled variance assumes the same variance in both groups, like the ordinary t-test and unlike the [Welch t-test](/welch-t-test/).

## Implementations

## History

Smyth (2004) built on earlier regularized and Bayesian t-tests for microarrays. His contribution was the general setting of linear models with any contrast, the closed-form estimate of the prior from the moments of the log variances, and the proof that the statistic has an exact $t$ distribution with augmented degrees of freedom. The method became the core of the limma package. Law et al. (2014) extended it to RNA-seq with voom, and Phipson et al. (2016) made the prior robust to hypervariable genes.

## References
