---
tag: FHEFFC
kind: technique
slug: highly-variable-gene-selection
name: Highly variable gene selection
aliases:
- HVG selection
area: biology/transcriptomics
level: core
summary: Keep the genes whose variance exceeds the trend expected from their mean, as features for dimension reduction and clustering of cells.
history:
  year: 2013
  people: [Philip Brennecke, Simon Anders, Jong Kyoung Kim, Marcus G. Heisler]
  note: Brennecke and co-authors (2013) fitted the technical noise of single-cell counts as a function of the mean and kept the genes above it. Later methods changed the trend and the score.
prereqs: [single-cell-rna-sequencing, poisson-distribution, negative-binomial-count-model]
see_also: [principal-component-analysis, pooling-size-factors, shared-nearest-neighbor-clustering, library-size-normalization, linear-regression, kernel-density-estimation, method-of-moments, differential-expression-analysis]
sources:
  - paper: doi:10.1038/nmeth.2645
    title: Philip Brennecke et al., Accounting for technical noise in single-cell RNA-seq experiments, Nature Methods 10(11), 1093 to 1095 (2013)
    locator: the fit of the squared coefficient of variation against the mean of spike-in genes, and the test for genes with more variation than the technical noise
  - paper: doi:10.1016/j.cell.2019.05.031
    title: Tim Stuart et al., Comprehensive integration of single-cell data, Cell 177(7), 1888 to 1902 (2019)
    locator: the selection of variable features by a fitted trend of variance on mean and the variance of the standardized values
  - paper: doi:10.1186/s13059-019-1861-6
    title: F. William Townes, Stephanie C. Hicks, Martin J. Aryee and Rafael A. Irizarry, Feature selection and dimension reduction for single-cell RNA-Seq based on a multinomial model, Genome Biology 20, article 295 (2019)
    locator: the ranking of genes by their deviance from a multinomial model of constant expression
  - paper: doi:10.15252/msb.20188746
    title: "Malte D. Luecken and Fabian J. Theis, Current best practices in single-cell RNA-seq analysis: a tutorial, Molecular Systems Biology 15(6), e8746 (2019)"
    locator: the section on feature selection in the standard workflow
---

Highly variable gene (HVG) selection keeps a few thousand of the genes of a single-cell data set before [principal component analysis](/principal-component-analysis/) and clustering. A gene is useful when its expression changes between cells more than sampling noise alone would make it change. The noise depends on the mean: a gene with few counts varies a lot from cell to cell just because of small numbers. So the technique fits a trend of variance against mean over all genes, or takes it from a model, and scores each gene by how far its variance lies above that trend. Brennecke and co-authors (2013) did this with spike-in genes of known amount; later methods fit the trend to all genes or use a count model.

## In plain words

Imagine you want to tell apart groups of people by their answers to many questions. A question that everyone answers the same way does not help. A question with random answers does not help either, even though the answers vary. You want the questions whose answers vary more than chance would make them vary. For genes, chance depends on how many copies of a gene a cell has: rare genes look noisy just because the numbers are small. So compare each gene with the noise that is normal for genes with the same average, and keep the genes that are noisier than normal.

## When it applies

- The data are counts or normalized counts of many genes in many cells, with size factors from [library size normalization](/library-size-normalization/) or [pooling size factors](/pooling-size-factors/).
- The next step uses distances between cells, such as PCA, a neighbor graph or clustering, and the many genes that do not vary would add only noise to those distances.
- Most genes are not informative about the cell types, so that a trend fitted to all genes describes the noise. If most genes differed between cell types, the trend would include biology.

## The template

1. Normalize the counts of each cell by its size factor.
2. For each gene $g$, compute the mean $\mu_g$ and the variance $\sigma_g^2$ over the cells, on counts or on log values.
3. Get the expected variance $f(\mu)$ of a gene with no biological variation: from a model, from spike-in genes, or by fitting a smooth curve of $\sigma_g^2$ against $\mu_g$ over all genes.
4. Score each gene by its excess, for example $\sigma_g^2/f(\mu_g)$ or $\sigma_g^2 - f(\mu_g)$, or by a test of $\sigma_g^2 > f(\mu_g)$.
5. Keep the genes with the highest scores; a fixed number such as 2000 is a common convention, not a derived value.

**Why the trend has this shape (a theorem).** Suppose the count of a gene in a cell is Poisson with a mean $m$ that is itself random across cells with mean $\mu$ and variance $\phi\mu^2$, for example gamma, which gives the [negative binomial model](/negative-binomial-count-model/). By the law of total variance, $\mathrm{Var}(x) = \mathbb{E}[m] + \mathrm{Var}(m) = \mu + \phi\mu^2$, so the squared coefficient of variation is
$$\mathrm{CV}^2 = \frac{\mathrm{Var}(x)}{\mu^2} = \frac{1}{\mu} + \phi.$$
With no biological variation ($\phi = 0$) it is $1/\mu$, the Poisson noise, which is large for small $\mu$. The trend $a_1/\mu + a_0$ that Brennecke and co-authors fitted to spike-in genes has this form, with $a_0$ for extra technical noise.

## Classic examples

**Three genes in six cells.** Assume equal size factors.

| gene | counts | mean | variance | variance / mean | $\mathrm{CV}^2$ |
|---|---|---|---|---|---|
| A | 0, 1, 0, 2, 1, 0 | 0.667 | 0.667 | 1.00 | 1.50 |
| B | 0, 0, 0, 6, 5, 7 | 3.0 | 11.2 | 3.73 | 1.24 |
| C | 6, 13, 9, 14, 8, 10 | 10.0 | 9.2 | 0.92 | 0.092 |

The variances use the divisor $n - 1$. Under the Poisson trend $f(\mu) = \mu$, only gene B is above the trend: it is low in three cells and high in three, which is the pattern of two cell types. Ranking by variance alone would also keep gene C, whose variance is what Poisson noise gives at its mean. Ranking by $\mathrm{CV}^2$ alone would put gene A first, although its $\mathrm{CV}^2$ equals the Poisson value $1/\mu = 1.5$ exactly.

**Brennecke et al. (2013).** Fit $\mathrm{CV}^2 = a_1/\mu + a_0$ to spike-in genes added in the same amount to each cell, then keep the genes whose $\mathrm{CV}^2$ is significantly above the fitted technical noise.

**Dispersion in bins of the mean.** Early versions of the Seurat package put genes into bins by mean, computed the dispersion $\sigma^2/\mu$ of each gene, and standardized it within its bin, so that each gene is compared with genes of a similar mean.

**Variance stabilizing selection (Stuart et al. 2019).** Fit a smooth curve of $\log\sigma^2$ against $\log\mu$, standardize the values of each gene with the variance from the curve, clip large values, and rank the genes by the variance of the standardized values.

**Deviance (Townes et al. 2019).** Fit a multinomial model in which each gene has the same share of the counts in every cell, and rank the genes by their deviance from that model. This works on raw counts with no log transform.

**Fitted trend on log values.** Fit the variance of the log values against their mean over all genes and keep the genes with the largest biological part, the variance minus the trend, as in the modelGeneVar function of the scran package.

## Variations

- **Per batch.** Select the genes in each batch and keep the genes selected in many batches, so that a batch effect does not pick the genes.
- **Fixed number or threshold.** Keep the top $N$ genes, or the genes whose excess passes a test at a set false discovery rate.
- **With known markers.** Add known marker genes to the selected set.
- **No selection.** Use all genes with a count model, such as a [variational autoencoder](/variational-autoencoder/), which down-weights noisy genes on its own.

## Pitfalls

- **Raw variance or raw $\mathrm{CV}^2$.** Both depend on the mean, as the example shows. Always compare with a trend.
- **Normalization first.** Differences in depth between cells add variance to every gene; divide by size factors before computing the variance.
- **Log of counts.** The log transform changes the mean-variance relation, and the trend must be fitted on the same scale as the variance.
- **Batch effects.** A gene that differs between batches looks highly variable; select within batches.
- **Cell cycle and stress genes** can be highly variable for reasons that are not of interest; check the selected list.
- **The number of genes.** Results of clustering change with the number of genes kept; test a few values.

## Exercises

1. Show that for a Poisson count with mean $\mu$, $\mathrm{CV}^2 = 1/\mu$.
2. Use the law of total variance to derive $\mathrm{CV}^2 = 1/\mu + \phi$ for the negative binomial model.
3. In the example, compute $\sigma^2 - \mu$ for the three genes and rank them.
4. A gene has the same mean in two cell types of equal size and differs only in its variance. Will the template find it? Why?
5. Explain why the selection should be done after normalization by size factors and not before.

## References
