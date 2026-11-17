---
tag: 20WZPC
kind: technique
slug: dispersion-shrinkage
name: Dispersion shrinkage
aliases:
- empirical Bayes dispersion estimation
area: biology/transcriptomics
level: advanced
summary: Shrink each gene's dispersion estimate toward a trend over mean expression, to stabilize tests when there are few replicates.
prereqs: [negative-binomial-count-model, empirical-bayes]
see_also: [negative-binomial-count-model, moderated-t-statistic, empirical-bayes, james-stein-estimator, differential-expression-analysis, maximum-likelihood-estimation, conjugate-prior]
sources:
  - paper: doi:10.1093/bioinformatics/btm453
    title: Mark D. Robinson and Gordon K. Smyth, Moderated statistical tests for assessing differences in tag abundance, Bioinformatics 23(21) (2007), pages 2881 to 2887
    locator: the weighted likelihood that combines the likelihood of one gene with the common likelihood of all genes to moderate the dispersion
  - paper: doi:10.1093/nar/gks042
    title: Davis J. McCarthy, Yunshun Chen and Gordon K. Smyth, Differential expression analysis of multifactor RNA-Seq experiments with respect to biological variation, Nucleic Acids Research 40(10) (2012), pages 4288 to 4297
    locator: the common, trended and gene-wise dispersions estimated by the Cox-Reid adjusted profile likelihood, with the gene-wise values shrunk toward the trend
  - paper: doi:10.1186/s13059-014-0550-8
    title: Michael I. Love, Wolfgang Huber and Simon Anders, Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2, Genome Biology 15(12) (2014), article 550
    locator: the trend of the dispersion over the mean, the log-normal prior around it with a variance estimated from the genes, the maximum a posteriori dispersion, and the handling of dispersion outliers
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the variance modelled as a smooth function of the mean, and the use of the larger of the fitted and the gene-wise value
  - paper: doi:10.2202/1544-6115.1027
    title: Gordon K. Smyth, Linear models and empirical Bayes methods for assessing differential expression in microarray experiments, Statistical Applications in Genetics and Molecular Biology 3(1) (2004), Article 3
    locator: the same shrinkage for residual variances of a normal model, with a scaled inverse chi-squared prior estimated from all genes
---

Dispersion shrinkage is the technique of estimating the dispersion of each gene in a [negative binomial model](/negative-binomial-count-model/) by combining the gene's own estimate with the estimates of all other genes. With two or three replicates per condition, the gene-wise estimate of the dispersion is very noisy. If a test uses it, genes whose dispersion is underestimated by chance give false positives, and genes whose dispersion is overestimated lose power. The technique fits a trend of the dispersion against the mean expression over all genes, treats the trend as the center of a prior, estimates the spread of the true dispersions around the trend, and moves each gene-wise estimate toward the trend by an amount that depends on how noisy it is. This is [empirical Bayes](/empirical-bayes/) in the sense of Robbins: the prior is estimated from the data of the many parallel problems. edgeR and DESeq2 use it. The [moderated t-statistic](/moderated-t-statistic/) of limma applies the same idea to the residual variances of a normal model.

## In plain words

You have ten thousand genes, but only three samples per group. For each gene you want to know how much its counts vary between replicates. Three samples are too few to measure that well for one gene alone. But genes with similar expression levels tend to vary by similar amounts, and you have thousands of them. So you work out what a typical gene at each level looks like, and then pull each gene's own noisy value toward that typical value. You pull hard when the gene's own value is unreliable, and gently when there is enough data to trust it. A gene that is far more variable than the rest is left alone, because pulling it in would make it look more certain than it is.

## When it applies

- **Many parallel estimates.** Thousands of genes, each with its own dispersion, measured in the same experiment.
- **Few degrees of freedom per gene.** The residual degrees of freedom $m - p$, the number of samples less the number of coefficients, are small, often 2 to 10.
- **A shared structure.** The true dispersions are similar for genes of similar mean, so a smooth trend plus a spread describes them. Biologically, this holds roughly: low-count genes have larger dispersions, and the dispersion levels off at high counts.
- **A test that depends on the dispersion.** The Wald test and the [likelihood ratio test](/likelihood-ratio-test/) of a negative binomial GLM both depend on $\alpha_g$ through the variance of the counts.

It does not apply when each gene has many replicates; then the gene-wise estimate is good and shrinkage does little. It does not help when the dispersions do not follow a common pattern, for example when a few genes are hugely more variable for biological reasons.

## The template

```pseudo id=main
SHRINK-DISPERSIONS(K, X, s)                   ▷ counts, design, size factors
L1  for each gene g do
L2      α̂_g ← gene-wise estimate, maximizing the Cox-Reid adjusted profile likelihood
L3  fit a trend α_tr(μ̄) of α̂_g against the mean normalized count μ̄_g
L4  v ← observed variance of ln α̂_g - ln α_tr(μ̄_g);  σ² ← v less its expected sampling variance
L5  for each gene g do
L6      α̃_g ← the maximizer of (adjusted log likelihood of α) + (log prior: ln α ~ N(ln α_tr(μ̄_g), σ²))
L7      if ln α̂_g - ln α_tr(μ̄_g) > 2√v then α̃_g ← α̂_g     ▷ dispersion outlier: do not shrink
L8  return α̃
```

Line L2 is the estimate of one gene alone. The Cox-Reid adjustment subtracts $\frac12\ln\det(X^\top WX)$ from the profile log likelihood, which removes most of the downward bias of the plain maximum likelihood estimate when $p$ coefficients are fitted from few samples. Line L3 fits the trend. DESeq2 fits $\alpha_{\text{tr}}(\bar\mu) = a_0 + a_1/\bar\mu$ by a gamma-family GLM of the gene-wise estimates, and edgeR fits a smooth curve. Line L4 estimates how widely the true dispersions spread around the trend: the observed spread of the log residuals includes sampling noise, and the expected sampling variance of $\ln\hat\alpha_g$ is subtracted. Line L6 is the maximum a posteriori estimate. Its result lies between $\hat\alpha_g$ and the trend: close to the trend when $m - p$ is small or $\sigma^2$ is small, and close to $\hat\alpha_g$ when $m - p$ is large. Line L7 follows DESeq2: a gene more than two standard deviations of the observed log residuals above the trend keeps its own estimate, so that shrinkage never makes a truly variable gene look stable.

**How much to shrink.** A normal approximation shows the weights. For a normal model, the estimate of a variance from $d$ degrees of freedom has $\operatorname{Var}(\ln\hat\sigma^2) = \psi'(d/2)$, the trigamma function. Suppose $\ln\hat\alpha_g$ behaves the same way, with $\tau^2 = \psi'(d/2)$. Then the posterior mode of $\ln\alpha$ is close to
$$\ln\tilde\alpha_g = \frac{\ln\hat\alpha_g/\tau^2 + \ln\alpha_{\text{tr}}/\sigma^2}{1/\tau^2 + 1/\sigma^2}.$$
Take $\hat\alpha_g = 0.4$, $\alpha_{\text{tr}} = 0.1$ and $\sigma^2 = 0.25$. With $d = 4$, $\tau^2 = \psi'(2) = 0.645$, the weights are 1.55 and 4, and $\tilde\alpha_g = 0.147$: most of the way to the trend. With $d = 20$, $\tau^2 = \psi'(10) = 0.105$, the weights are 9.5 and 4, and $\tilde\alpha_g = 0.265$: closer to the gene's own value. This is an illustration with a normal approximation, not the exact DESeq2 computation.

## Classic examples

- **[Moderated t-statistic](/moderated-t-statistic/).** limma shrinks the residual variance $s_g^2$ of each gene toward a prior value $s_0^2$ with prior degrees of freedom $d_0$, both estimated from all genes. There the prior is conjugate and the posterior has a closed form, and the null distribution of the resulting statistic is exactly $t$ with $d_0 + d$ degrees of freedom. Dispersion shrinkage is the same idea for a negative binomial dispersion, where no conjugate form exists.
- **edgeR weighted likelihood.** Robinson and Smyth (2007) maximized the gene's likelihood plus a weight times the likelihood shared by all genes. McCarthy, Chen and Smyth (2012) replaced the common value by a trend over the mean, with the Cox-Reid adjusted profile likelihood for GLMs.
- **DESeq2.** Love, Huber and Anders (2014) put a log-normal prior around the fitted trend, estimated its variance from the genes, and took the maximum a posteriori dispersion, as in the template. DESeq2 shrinks the log fold changes as well, with a separate prior.
- **The [James-Stein estimator](/james-stein-estimator/).** For three or more normal means, shrinking all estimates toward a common point lowers the total squared error, whatever the true means are. Dispersion shrinkage has the same flavour, but it shrinks on the log scale toward a fitted trend, and its gain is measured in simulations rather than proved.
- **DESeq.** Anders and Huber (2010) fitted the variance as a smooth function of the mean and used the larger of the fitted and the gene-wise value. This is a conservative form of sharing information without a prior.

## Variations

- **Common dispersion.** One value for all genes. It is the strongest shrinkage, and it is wrong when low-count genes have larger dispersions.
- **Trended dispersion.** The trend value alone, with no gene-wise part.
- **Quasi-likelihood dispersion.** edgeR's quasi-likelihood pipeline fixes the negative binomial dispersion at the trend and puts a second, gene-wise factor on the variance, which it shrinks as limma shrinks variances. Its tests use an F distribution with the prior degrees of freedom added.
- **Robust priors.** limma and edgeR offer robust estimation of the prior, so that a few outlying genes do not inflate $\sigma^2$ or the prior degrees of freedom.
- **Fold change shrinkage.** The same empirical Bayes idea applied to $\hat\beta_g$ instead of $\hat\alpha_g$, used to rank genes by effect size. It is a separate step and does not change the test.

## Pitfalls

- **Shrinking an outlier.** A gene with a true dispersion far above the trend, if shrunk, looks much more stable than it is, and gives a false positive. DESeq2 does not shrink such genes; other tools use robust priors.
- **A poor trend.** With few genes, or a strong dependence of the dispersion on something other than the mean (such as GC content), the trend is wrong, and so is the center of the prior. Plot $\hat\alpha_g$, the trend and $\tilde\alpha_g$ against the mean before trusting the tests.
- **Differences between groups.** The model has one dispersion per gene. When one condition is much more variable than the other, the shared value misstates both, and shrinkage cannot fix that.
- **Treating the shrunk value as known.** The tests use $\tilde\alpha_g$ as if it were the true value. This ignores its uncertainty, which is one reason the quasi-likelihood F tests of edgeR hold their level better with very few replicates.
- **Few genes.** The prior variance in line L4 is a difference of two quantities and can be negative or unstable with few genes. Then it is set to a small positive floor, which amounts to strong shrinkage.

## Exercises

1. Show that, for a normal model with residual variance $s_g^2$ on $d$ degrees of freedom and the prior $1/\sigma_g^2 \sim \chi^2_{d_0}/(d_0s_0^2)$, the posterior mean of $1/\sigma_g^2$ is $(d_0 + d)/(d_0s_0^2 + ds_g^2)$. This is the formula of the [moderated t-statistic](/moderated-t-statistic/).
2. In the normal approximation above, find the number of degrees of freedom $d$ at which the gene-wise estimate and the trend get equal weight when $\sigma^2 = 0.25$, by solving $\psi'(d/2) = 0.25$.
3. Explain why subtracting the expected sampling variance in line L4 is needed, by computing what $\sigma^2$ would be if all genes had exactly the trend dispersion.

## References
