---
tag: PBAHAY
kind: algorithm
slug: combat
name: ComBat
aliases:
- empirical Bayes batch correction
area: biology/transcriptomics
level: core
summary: Remove batch effects by fitting location and scale shifts per gene and batch, shrunk across genes by empirical Bayes.
solves: [batch-effect-correction]
model: real-ram
complexity:
  vars: {G: the number of genes, N: the number of samples, p: the number of design columns, T: the number of iterations}
  time: {worst: O(G (N p^2 + p^3) + G N T)}
  space: {extra: O(G N)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [W. Evan Johnson, Cheng Li, Ariel Rabinovic]
  note: Johnson, Li and Rabinovic (2007) proposed ComBat for microarray batches in Biostatistics. It became the ComBat function of the R package sva.
prereqs: [empirical-bayes, linear-regression, method-of-moments, conjugate-prior]
see_also: [batch-effect-correction, mnn-batch-correction, james-stein-estimator, empirical-bayes, linear-mixed-model, hierarchical-bayesian-model, differential-expression-analysis, principal-component-analysis]
sources:
  - paper: doi:10.1093/biostatistics/kxj037
    title: W. Evan Johnson, Cheng Li and Ariel Rabinovic, Adjusting batch effects in microarray expression data using empirical Bayes methods, Biostatistics 8(1), 118 to 127 (2007)
    locator: the section on the empirical Bayes method, with the location and scale model, the standardization, the priors, the conditional posterior means and the adjustment
  - paper: doi:10.1038/nrg2825
    title: Jeffrey T. Leek et al., Tackling the widespread and critical impact of batch effects in high-throughput data, Nature Reviews Genetics 11(10), 733 to 739 (2010)
    locator: the discussion of batch effects, of their confounding with biology, and of correction methods
---

ComBat removes batch effects from gene expression data: differences between groups of samples that come from processing them on different days, plates or machines. It models each gene in each batch with a shift of the mean and a change of scale, standardizes the data, and estimates the shifts and scales with [empirical Bayes](/empirical-bayes/): the estimates of all genes in one batch give a prior, and each gene's estimate is pulled toward it. Then it removes the shifts and scales. Johnson, Li and Rabinovic (2007) built it for microarrays with small batches, where the plain estimates for each gene are too noisy. It solves the [batch effect correction](/batch-effect-correction/) problem when the batches hold the same kinds of samples or when the biological differences are given as covariates.

## In plain words

Each batch can make a gene read a bit high or a bit low, and a bit more or less spread out. With many samples per batch you could measure this for each gene and undo it. With three samples per batch, each such measurement is noisy. ComBat looks at all genes of a batch together: if most genes read about 1.4 units high in batch A, a gene that seems to read 1.8 units high probably reads less high than that. So it moves each gene's estimate part of the way toward the typical value of its batch, more when the batch is small or noisy. Then it subtracts the estimated shift and divides by the estimated spread. You must tell it which differences are biology, or it removes them too.

## The problem

**Input.** A matrix $Y_{gj}$ of expression values, such as log counts, for $G$ genes and $N$ samples, a batch label for each sample, with at least two samples per batch, and optional covariates $x_j$ to keep.

**Output.** An adjusted matrix $Y^\ast$ of the same shape.

**Model.** For sample $j$ in batch $i$, $Y_{gj} = \alpha_g + x_j\beta_g + \gamma_{ig} + \delta_{ig}\varepsilon_{gj}$, where $\varepsilon_{gj}$ has mean 0 and variance $\sigma_g^2$. The batch shifts $\gamma_{ig}$ and scales $\delta_{ig}$ are the effects to remove.

## The algorithm

```pseudo id=main
COMBAT(Y, batch, x)
L1  for each gene g: fit Y[g] by least squares on batch indicators and x; α_g ← the size-weighted mean of the batch coefficients
L2  σ²_g ← the mean squared residual of gene g
L3  Z[g][j] ← (Y[g][j] - α_g - x_j β_g) / σ_g
L4  γ̂_ig, δ̂²_ig ← the mean and the sample variance of Z[g][j] over the samples j of batch i
L5  γ̄_i, τ²_i ← the mean and the sample variance of γ̂_ig over the genes
L6  D, S² ← the mean and the sample variance of δ̂²_ig over the genes; λ_i ← (D² + 2S²) / S²; θ_i ← (D³ + D S²) / S²
L7  repeat: γ*_ig ← (n_i τ²_i γ̂_ig + δ*²_ig γ̄_i) / (n_i τ²_i + δ*²_ig)
L8          δ*²_ig ← (θ_i + ½ Σ_j (Z[g][j] - γ*_ig)²) / (n_i/2 + λ_i - 1)
L9  until the relative change of γ* and δ*² is below 10^-4      ▷ start from δ*² = δ̂²
L10 Y*[g][j] ← σ_g / δ*_ig · (Z[g][j] - γ*_ig) + α_g + x_j β_g
```

Lines L1 to L3 put all genes on one scale. The fit uses one coefficient per batch, so after line L3 the mean of batch $i$ is the batch shift in units of $\sigma_g$. Line L4 gives the plain estimates of the shift and the scale of each gene and batch. Lines L5 and L6 fit the priors $\gamma_{ig} \sim N(\bar\gamma_i, \tau_i^2)$ and $\delta^2_{ig} \sim \text{InvGamma}(\lambda_i, \theta_i)$ by the [method of moments](/method-of-moments/), over all genes of batch $i$. Line L7 is the posterior mean of the shift for a given scale, and line L8 the posterior mean of the scale for a given shift; both priors are [conjugate](/conjugate-prior/). Lines L7 to L9 alternate the two until they agree. Line L10 removes the shrunk shift and scale and puts the gene back on its own scale.

Without lines L5 to L9, with $\gamma^\ast = \hat\gamma$ and $\delta^\ast = \hat\delta$, this is the plain location and scale adjustment.

## Example

Four genes in two batches of three samples:

| gene | A1 | A2 | A3 | B1 | B2 | B3 |
|---|---|---|---|---|---|---|
| 1 | 1 | 2 | 3 | 4 | 5 | 6 |
| 2 | 2 | 4 | 6 | 5 | 6 | 7 |
| 3 | 3 | 3 | 4 | 7 | 9 | 11 |
| 4 | 5 | 6 | 7 | 6 | 8 | 10 |

For gene 1 the batch means are 2 and 5, so $\alpha_1 = 3.5$, the residuals are $-1, 0, 1$ in each batch, and $\sigma_1^2 = 4/6 = 2/3$. Then $Z = (Y - 3.5)/0.8165$, and batch A has $\hat\gamma_{A1} = -1.837$ and $\hat\delta^2_{A1} = 1.5$. Over the four genes, batch A has shifts $-1.837, -0.775, -2.357, -0.775$ and scales $1.5, 2.4, 0.231, 0.6$. So $\bar\gamma_A = -1.436$, $\tau_A^2 = 0.628$, $\lambda_A = 3.484$ and $\theta_A = 2.938$; the prior mean of the scale is $\theta_A/(\lambda_A - 1) = 1.183$, the mean of the four scales. The iteration moves gene 1 to $\gamma^\ast_{A1} = -1.687$ and $\delta^{\ast2}_{A1} = 1.122$, toward the prior.

| gene 1 | A1 | A2 | A3 | B1 | B2 | B3 |
|---|---|---|---|---|---|---|
| location and scale only | 2.684 | 3.5 | 4.316 | 2.684 | 3.5 | 4.316 |
| ComBat | 2.441 | 3.385 | 4.329 | 2.834 | 3.619 | 4.404 |

Without shrinkage the two batches of gene 1 become the same. With shrinkage a small gap is left, because gene 1 has a larger shift than the typical gene and ComBat treats part of that as noise. With three samples per batch this is usually the better bet: in the tests, with 300 genes and batches of 3, the ComBat output was closer to the batch free data than the plain location and scale output (mean squared error 0.090 against 0.143, and 0.248 before correction). That is a measurement on data drawn from the model, not a theorem.

## Correctness

The [proof](proofs/correctness.md) shows four things. Without shrinkage, the adjusted data of every gene have the same mean and sample variance in every batch. Line L7 is the posterior mean of the shift under a normal prior when the scale is known, and line L8 is the posterior mean of the scale under an inverse gamma prior when the shift is known. Line L6 is the only inverse gamma with the mean and variance of the plain scales. And the iteration converges, because the scale sequence is monotone and bounded. The answer is a fixed point of the two conditional means, not the joint posterior mean. Whether real batch effects follow the model is an assumption.

## Complexity

The least squares fit takes $O(Np^2 + p^3)$ time per gene for $p$ design columns, so $O(G(Np^2 + p^3))$ in all. The priors take $O(GN)$. Each step of the iteration takes $O(GN)$ for all genes and batches, so $T$ steps take $O(GNT)$. The proof shows that the iteration stops but gives no bound on $T$. The space is $O(GN)$ for the standardized data.

## Properties

- **Shrinkage across genes,** like the [James-Stein estimator](/james-stein-estimator/). James-Stein shrinks all means by one common factor and has a theorem: for three or more normal means, it has lower total squared error than the sample means for every parameter value. ComBat shrinks each gene by its own factor $\delta^2/(n\tau^2 + \delta^2)$, uses fitted priors for the shift and for the scale, and has no such theorem.
- **Empirical Bayes, by moments.** The prior comes from the data of all genes, as in [empirical Bayes](/empirical-bayes/), but by matching moments, not by maximizing the marginal likelihood.
- **Equivariant.** Adding a constant to a gene adds it to the output, and scaling all data scales the output.
- **One batch at a time.** The priors of each batch are separate.
- **Not a mixed model.** A [linear mixed model](/linear-mixed-model/) would treat the batch as a random effect in the analysis itself. ComBat cleans the data first and leaves the analysis to other tools.

## Variants and improvements

- **Non-parametric prior.** The paper also gives a version with the prior as the empirical distribution of the other genes' estimates, which is slower.
- **Mean only.** Adjust only the shift, for batches whose spread is the same.
- **Reference batch.** Leave one batch unchanged and move the others onto it.
- **Counts.** ComBat-seq applies the same idea to RNA-seq counts with a negative binomial model.
- **Single cells.** ComBat assumes that each batch holds the same mix of cell types. Methods such as [MNN correction](/mnn-batch-correction/) match cells across batches instead.

## When to use it

Use it on bulk expression data with known batches, especially with small batches, and give the biological groups as covariates. It also works on log normalized single-cell data when every batch holds about the same cell types. When the batches hold different mixes of cell types, or for direct [differential expression](/differential-expression-analysis/) testing, it is better to put the batch in the model of the test, or to use a single-cell method.

## Pitfalls

- **Confounded design.** If the batch and a biological group are the same samples, no method can separate them, and ComBat removes the biology.
- **Leaving out covariates.** In the tests, a group with an effect of 2, unbalanced across two batches, kept a difference of 1.92 with the covariate and only 1.03 without it.
- **Using the corrected data for tests.** The correction uses the data, so tests on the corrected data are too confident, more so with an unbalanced design.
- **Batches with one sample** have no variance and cannot be corrected.
- **Genes with no variance in a batch** break the scale estimate; filter them first.

## Implementations

## History

Batch effects in microarray data were known from the early 2000s. Johnson, Li and Rabinovic (2007) proposed the location and scale model with empirical Bayes priors, aimed at batches too small for the gene by gene estimates of earlier methods. Leek and co-authors (2010) showed how common and how large batch effects are in high-throughput data. ComBat became the most used batch correction for bulk data, and later versions added counts and single-cell data.

## References
