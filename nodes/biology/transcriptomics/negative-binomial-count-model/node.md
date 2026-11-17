---
tag: 2AJH92
kind: model
slug: negative-binomial-count-model
name: Negative binomial model for read counts
aliases:
- negative binomial GLM for RNA-seq
area: biology/transcriptomics
level: core
summary: Model the count of a gene as negative binomial with a mean from a log-linear model of the design and a gene-wise dispersion.
history:
  year: 2007
  people: [Mark D. Robinson, Gordon K. Smyth]
  note: Robinson and Smyth modelled tag counts as negative binomial with a moderated dispersion in 2007. Anders and Huber (DESeq, 2010) and McCarthy, Chen and Smyth (edgeR GLMs, 2012) made it the standard model for RNA-seq counts.
prereqs: [generalized-linear-model, poisson-distribution, rna-sequencing]
see_also: [differential-expression-analysis, dispersion-shrinkage, library-size-normalization, iteratively-reweighted-least-squares, likelihood-ratio-test, wald-test, maximum-likelihood-estimation, moderated-t-statistic]
sources:
  - paper: doi:10.1093/bioinformatics/btm453
    title: Mark D. Robinson and Gordon K. Smyth, Moderated statistical tests for assessing differences in tag abundance, Bioinformatics 23(21) (2007), pages 2881 to 2887
    locator: the negative binomial model for tag counts with the variance mu + phi mu^2, and the weighted likelihood that moderates the dispersion
  - paper: doi:10.1093/biostatistics/kxm030
    title: Mark D. Robinson and Gordon K. Smyth, Small-sample estimation of negative binomial dispersion, with applications to SAGE data, Biostatistics 9(2) (2008), pages 321 to 332
    locator: the conditional maximum likelihood estimate of the dispersion and the exact test for two groups
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the negative binomial model with size factors and a variance that is a smooth function of the mean
  - paper: doi:10.1093/nar/gks042
    title: Davis J. McCarthy, Yunshun Chen and Gordon K. Smyth, Differential expression analysis of multifactor RNA-Seq experiments with respect to biological variation, Nucleic Acids Research 40(10) (2012), pages 4288 to 4297
    locator: the negative binomial GLM with a design matrix and offsets, the biological coefficient of variation, and the Cox-Reid adjusted profile likelihood for the dispersion
  - paper: doi:10.1186/s13059-014-0550-8
    title: Michael I. Love, Wolfgang Huber and Simon Anders, Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2, Genome Biology 15(12) (2014), article 550
    locator: the model K_ij ~ NB(mu_ij, alpha_i) with mu_ij = s_j q_ij and log2 q_ij = x_j beta_i, and the Wald test
---

The negative binomial model for read counts says that the count $K_{gj}$ of gene $g$ in sample $j$ has a negative binomial distribution with mean $\mu_{gj}$ and dispersion $\alpha_g$, so that $\operatorname{Var}(K_{gj}) = \mu_{gj} + \alpha_g\mu_{gj}^2$. The mean is the size factor of the sample times the expression of the gene, and the log of the expression is a linear function of the design, as in a [generalized linear model](/generalized-linear-model/). The term $\mu$ is the Poisson noise of sampling reads, and the term $\alpha\mu^2$ is the extra variation between biological replicates. Robinson and Smyth (2007) used this model for tag counts, and it is the model of edgeR and DESeq2. It is the model behind [differential expression analysis](/differential-expression-analysis/) of RNA-seq counts; with few replicates the dispersion is estimated by [dispersion shrinkage](/dispersion-shrinkage/). The [moderated t-statistic](/moderated-t-statistic/) is the other main route: it works on log counts with a normal model instead of on the counts.

## The machine

**Data.** A matrix of counts $K_{gj} \ge 0$ for genes $g = 1, \dots, n$ and samples $j = 1, \dots, m$, and a design matrix $X$ with one row $x_j$ per sample and $p$ columns (an intercept, the condition, a batch, and so on). The counts are the raw numbers of reads or fragments assigned to the gene, not normalized values.

**Distribution.** Given the parameters, the counts are independent and
$$K_{gj} \sim \operatorname{NB}(\mu_{gj}, \alpha_g), \qquad P(K = k) = \frac{\Gamma(k + 1/\alpha)}{\Gamma(1/\alpha)\,k!}\left(\frac{1}{1 + \alpha\mu}\right)^{1/\alpha}\left(\frac{\alpha\mu}{1 + \alpha\mu}\right)^k, \quad k = 0, 1, 2, \dots$$
With $r = 1/\alpha$ this is the negative binomial law with size $r$ and success probability $r/(r + \mu)$.

**Mean.** $\mu_{gj} = s_jq_{gj}$, with $\log_2 q_{gj} = x_j^\top\beta_g$. The size factors $s_j$ come from [library size normalization](/library-size-normalization/) and are fixed, so $\ln s_j$ is an offset. The coefficients $\beta_g$ are log2 fold changes: for a design with an intercept and a 0 or 1 indicator of the treatment, $\beta_{g1}$ is the log2 ratio of the expression in the treated group to that in the control group.

**Dispersion.** $\alpha_g \ge 0$ is the same for all samples of a gene. It has no unit. Its square root is the biological coefficient of variation (BCV): the coefficient of variation that the true expression would have between replicates if the depth were infinite.

**Standing assumptions.** The samples are independent. The design captures every systematic difference between them. The size factors are known. The dispersion does not depend on the condition. The model does not describe reads that map to many genes, and it does not by itself model excess zeros.

**The gamma-Poisson mixture.** The model is what one gets from two stages. The true expression of the gene in the sample is $\lambda \sim \operatorname{Gamma}(\text{shape } 1/\alpha, \text{scale } \alpha\mu)$, with mean $\mu$ and variance $\alpha\mu^2$. Given $\lambda$, the count is [Poisson](/poisson-distribution/) with mean $\lambda$. Integrating over $\lambda$ gives the negative binomial law above.

## What it counts

The model gives the probability of each count, and so a likelihood for the parameters of each gene:
$$\ell_g(\beta, \alpha) = \sum_{j=1}^m \left[\ln\Gamma(k_j + r) - \ln\Gamma(r) - \ln k_j! + r\ln\frac{r}{r + \mu_j} + k_j\ln\frac{\mu_j}{r + \mu_j}\right], \quad r = 1/\alpha.$$
From it come the [maximum likelihood](/maximum-likelihood-estimation/) estimates $\hat\beta_g$, their standard errors, the [Wald test](/wald-test/) of DESeq2 and the [likelihood ratio test](/likelihood-ratio-test/) of a reduced design. It also predicts the spread of counts: the squared coefficient of variation of a count is
$$\frac{\operatorname{Var}(K)}{\mu^2} = \frac1\mu + \alpha,$$
the sum of a technical part that falls with depth and a biological part that does not.

**A worked case.** For $\mu = 100$ and $\alpha = 0.1$, the variance is $100 + 0.1 \cdot 100^2 = 1100$ and the standard deviation is 33.2, against 10 for a Poisson count with the same mean. The BCV is $\sqrt{0.1} = 0.32$, so the true expression varies by about 32 percent between replicates. Sequencing ten times as deeply, with $\mu = 1000$, lowers the squared coefficient of variation only from 0.11 to 0.101. More replicates help; more depth beyond this point helps little.

**Small values by hand.** For $\mu = 2$ and $\alpha = 0.5$, the size is $r = 2$ and the success probability is $1/2$, so $P(K = k) = (k + 1)/2^{k+2}$: $P(0) = 0.25$, $P(1) = 0.25$, $P(2) = 0.1875$. The Poisson law with mean 2 gives $P(0) = 0.135$. The negative binomial law puts more mass at 0 and in the tail.

## Relation to other models

- **[Poisson distribution](/poisson-distribution/).** The case $\alpha = 0$. Counts from technical replicates of the same library are close to Poisson. Biological replicates are not, and a Poisson test on them finds far too many changes.
- **[Generalized linear model](/generalized-linear-model/).** For a fixed $\alpha$, the negative binomial law is an exponential family in $\mu$, so the model is a GLM with a log link and an offset, and it is fitted by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/). The log link is not the canonical link of this family.
- **Normal model on log counts.** limma-voom models $\log_2$ counts per million as normal, with precision weights from the trend of the variance against the mean, and then uses the [moderated t-statistic](/moderated-t-statistic/). In published benchmarks the two routes give similar results; voom is faster and allows the tools of linear models.
- **Quasi-likelihood.** edgeR also fits a quasi-negative binomial model, in which a second, gene-wise factor multiplies the variance and is shrunk by empirical Bayes. Its tests keep the error rate closer to the nominal level when the dispersion is uncertain.
- **Zero-inflated models.** For single-cell data, some authors add a point mass at 0. For UMI counts, several studies report that the plain negative binomial model fits well without it. This is a measurement on data, not a result of the model.
- **Beta-binomial model.** For counts of two kinds of reads at one site, such as allele-specific expression, the analogue of the gamma-Poisson mixture is a beta-binomial mixture.

## Known results in the model

**Mean and variance.** $E[K] = \mu$ and $\operatorname{Var}(K) = \mu + \alpha\mu^2$.

*Proof.* With $\lambda$ gamma and $K \mid \lambda$ Poisson, $E[K] = E[\lambda] = \mu$. By the law of total variance, $\operatorname{Var}(K) = E[\operatorname{Var}(K \mid \lambda)] + \operatorname{Var}(E[K \mid \lambda]) = E[\lambda] + \operatorname{Var}(\lambda) = \mu + \alpha\mu^2$. $\square$

**Concave in the coefficients.** For a fixed $\alpha$, $\ell_g$ is a concave function of $\beta_g$. If $X$ has full column rank and $\mu_j > 0$, it is strictly concave, so any stationary point is the unique maximum.

*Proof.* Write $\eta_j = \ln\mu_j = \ln s_j + (\ln 2)x_j^\top\beta$, which is affine in $\beta$. As a function of $\eta_j$, the term of sample $j$ is $k_j\eta_j - (k_j + r)\ln(r + e^{\eta_j})$ plus a constant. Its second derivative is $-(k_j + r)re^{\eta_j}/(r + e^{\eta_j})^2 < 0$. A concave function of an affine map is concave, and a sum of concave functions is concave. With full column rank, the Hessian $-(\ln 2)^2X^\top DX$, with $D$ diagonal and positive, is negative definite. $\square$

So IRLS, which is Fisher scoring for this model, has only one maximum to find. It can still fail to converge without step control when some counts are 0 and $\hat\beta$ goes to infinity, as when a gene has no reads in one group.

**Fisher information.** For a fixed $\alpha$, the expected information for $\beta$ (in natural log units) is $X^\top WX$ with $w_j = \mu_j/(1 + \alpha\mu_j)$.

*Proof.* The score of $\eta_j$ is $k_j - (k_j + r)\mu_j/(r + \mu_j) = r(k_j - \mu_j)/(r + \mu_j) = (k_j - \mu_j)/(1 + \alpha\mu_j)$. Its variance is $\operatorname{Var}(K_j)/(1 + \alpha\mu_j)^2 = \mu_j/(1 + \alpha\mu_j)$. The chain rule through the affine map gives $X^\top WX$, times $(\ln 2)^2$ for log2 units. $\square$

The weight $w_j$ tends to $1/\alpha$ as $\mu_j$ grows: beyond a certain depth a sample gives no more information about the fold change, because the biological variation dominates. This is the formal form of the worked case above.

**Two groups with equal size factors.** If all $s_j$ are equal to $s$ and the design is one mean per group, the maximum likelihood estimate of the mean of a group is $\bar k/s$, the mean count of the group divided by $s$, for any fixed $\alpha$. This follows by setting the score $\sum_j (k_j - \mu)/(1 + \alpha\mu)$ to 0. With unequal size factors there is no closed form, and IRLS is used.

**Exact test.** For two groups with equal library sizes and a known $\alpha$, the sum of the counts of a group of $c$ samples is negative binomial with mean $c\mu$ and size $c/\alpha$. Robinson and Smyth (2008) build an exact test from the conditional law of one group's sum given the total. It removes the unknown common mean by conditioning, in the same way as the [Fisher exact test](/fisher-exact-test/) conditions on the margins of a table. edgeR uses it after it adjusts the counts to equal library sizes.

**Estimating the dispersion.** The maximum likelihood estimate of $\alpha$ is biased downward with few replicates, because it ignores the degrees of freedom used by $\beta$. The Cox-Reid adjusted profile likelihood, used by edgeR and DESeq2, corrects for this (McCarthy, Chen and Smyth 2012). With 2 or 3 replicates per group, a gene-wise estimate is still very noisy, which is why [dispersion shrinkage](/dispersion-shrinkage/) borrows information across genes.

## References
