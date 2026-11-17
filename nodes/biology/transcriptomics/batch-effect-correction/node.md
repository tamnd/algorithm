---
tag: 7DKM06
kind: problem
slug: batch-effect-correction
name: Batch effect correction
aliases:
- batch correction
- single-cell data integration
area: biology/transcriptomics
level: core
summary: Remove differences between samples caused by processing batches while keeping the biological differences between conditions.
prereqs: [single-cell-rna-sequencing, linear-regression, nearest-neighbor-graph]
see_also: [combat, mnn-batch-correction, empirical-bayes, linear-mixed-model, variational-autoencoder, principal-component-analysis, umap, canonical-correlation-analysis]
sources:
  - paper: doi:10.1038/nrg2825
    title: Jeffrey T. Leek et al., Tackling the widespread and critical impact of batch effects in high-throughput data, Nature Reviews Genetics 11(10), 733 to 739 (2010)
    locator: the definition of batch effects, the examples in published data, and the advice on study design and confounding
  - paper: doi:10.1093/biostatistics/kxj037
    title: W. Evan Johnson, Cheng Li and Ariel Rabinovic, Adjusting batch effects in microarray expression data using empirical Bayes methods, Biostatistics 8(1), 118 to 127 (2007)
    locator: the location and scale model of batch effects and its empirical Bayes fit
  - paper: doi:10.1038/nbt.4091
    title: Laleh Haghverdi, Aaron T. L. Lun, Michael D. Morgan and John C. Marioni, Batch effects in single-cell RNA-sequencing data are corrected by matching mutual nearest neighbors, Nature Biotechnology 36(5), 421 to 427 (2018)
    locator: the three assumptions of the method and the comparison with methods that assume the same cell type mix in each batch
  - paper: doi:10.1038/s41592-019-0619-0
    title: Ilya Korsunsky et al., Fast, sensitive and accurate integration of single-cell data with Harmony, Nature Methods 16(12), 1289 to 1296 (2019)
    locator: the Harmony algorithm of soft clustering and correction per cluster
  - paper: doi:10.1186/s13059-019-1850-9
    title: Hoa Thi Nhu Tran et al., A benchmark of batch-effect correction methods for single-cell RNA sequencing data, Genome Biology 21, article 12 (2020)
    locator: the comparison of 14 methods and the recommendation of Harmony, LIGER and Seurat 3
---

Batch effect correction removes the differences between groups of samples that come from how they were processed: the day, the lab, the reagent lot or the machine. It must keep the biological differences, such as cell types or the effect of a treatment. In single-cell data, a batch effect moves all cells of one run, so cells of one type from two runs can form two clusters. The known methods either fit a shift of location and scale per gene and batch, or match cells across batches by their nearest neighbors, under the assumption that the batches share cell types. No method can separate a batch effect from biology when the two are confounded; that is a limit of the design, not of the method.

## In plain words

Two people weigh the same kinds of fruit, but one scale reads a little heavy. If both people weighed apples and pears, you can compare their apples, find out how much heavier the second scale reads, and subtract it. If one person weighed only apples and the other only pears, you cannot tell whether pears are heavier or the second scale is wrong. Batch correction is the first case: use what the batches have in common to learn the error of each batch, then remove it.

## Definition

**Input.** An expression matrix of cells (or samples) by genes, a batch label for each cell, and optionally known covariates such as the condition.

**Output.** A corrected matrix, or a corrected low dimensional embedding, or a corrected neighbor graph, in which cells of the same type from different batches are mixed and cells of different types stay apart.

**A model.** Write the expression of gene $g$ in cell $i$ of batch $b$ as $x_{ig} = f_g(z_i) + \gamma_{bg} + \delta_{bg}\varepsilon_{ig}$, where $z_i$ is the biological state of the cell, $\gamma_{bg}$ a shift and $\delta_{bg}$ a scale of the batch. The goal is to estimate $f_g(z_i)$ up to a common shift. ComBat assumes that $f_g$ depends only on known covariates; nearest neighbor methods let $z_i$ be unknown but assume that some states occur in more than one batch.

**Identifiability (a theorem).** If every value of a covariate occurs in only one batch, then batch and covariate are confounded, and the effect of the covariate cannot be estimated. *Proof.* Let batch 1 hold only the controls and batch 2 only the treated cells. The data distribution under a treatment effect $\theta$ and a batch shift $\gamma$ depends on them only through $\theta + \gamma$ for every gene, so any pair with the same sum fits the data equally well. $\square$ The same holds for cell types: a type found in only one batch cannot be told apart from a batch effect by the data alone.

## Variants

- **Bulk samples with known groups.** Few samples, many genes, the condition known for each sample; the location and scale model applies.
- **Single cells with unknown types.** Many cells, types unknown and in different proportions per batch; methods must match cells.
- **Output space.** Some methods correct the genes, others only an embedding or a graph, which is enough for clustering and display but not for tests per gene.
- **Reference mapping.** Map new cells onto a fixed, corrected reference instead of correcting all batches together.
- **Broader integration.** Joining data of different technologies or of different kinds of measurement, such as RNA and chromatin, uses the same ideas with weaker shared structure.

## Examples

**A balanced design.** One gene, two batches, each with two controls and two treated samples. Batch 1 reads 1, 1 for the controls and 3, 3 for the treated; batch 2 reads 3, 3 and 5, 5. A model with a batch term and a condition term fits exactly with a batch shift of 2 and a treatment effect of 2, and subtracting the batch shift leaves 1, 1, 3, 3 in both batches.

**A confounded design.** Batch 1 holds the controls, which read 1, 1, and batch 2 the treated, which read 5, 5. The difference 4 could be a treatment effect of 4, a batch shift of 4, or any split of the two. By the theorem above, no method can choose. Correcting the batch here would remove the treatment effect.

**Different mixes of cell types.** Batch 1 holds mostly type A and batch 2 mostly type B. Moving batch 2 by the difference of the batch means mixes the two types; the example on the [MNN page](/mnn-batch-correction/) shows such a shift going wrong, while matching mutual nearest neighbors finds the right shift.

## Known algorithms

- **Regression on the batch.** Fit a linear model per gene with batch terms and subtract them, as in the removeBatchEffect function of limma; a [linear model](/linear-regression/) with known covariates.
- **[ComBat](/combat/)** (Johnson, Li and Rabinovic 2007). A location and scale shift per gene and batch, with the shifts shrunk across genes by [empirical Bayes](/empirical-bayes/). Exact for its model, and good for bulk data and for single cells with the same mix of types in each batch.
- **[MNN correction](/mnn-batch-correction/)** (Haghverdi et al. 2018). Pairs of cells that are mutual nearest neighbors across batches give local correction vectors. It needs only one shared population.
- **Seurat anchors** (Stuart et al. 2019). Mutual nearest neighbors in a space from [canonical correlation analysis](/canonical-correlation-analysis/), scored and used as anchors.
- **Harmony** (Korsunsky et al. 2019). Alternates soft clustering of all cells with a correction per cluster in a space of [principal components](/principal-component-analysis/).
- **Deep generative models.** A [variational autoencoder](/variational-autoencoder/) with the batch as an input learns a latent space of the cells without the batch.

## Bounds

There is no general guarantee: the problem is not identifiable when batches and biology are confounded, and the methods differ in what they assume. Under their own models some results are exact: ComBat's location and scale step removes a shift and scale per gene and batch exactly when the model holds, and MNN correction removes a translation exactly when it is shorter than half the smallest distance between reference cells and $k = 1$ (both proved on their pages). Everything else is measured. The benchmark of Tran and co-authors (2020) compared 14 methods on several data sets by how well batches mix and cell types stay apart, and recommended Harmony, LIGER and Seurat 3.

## Reductions

- To regression: with known covariates and a shared mix of types, correction is the fit of batch terms in a linear model, or in a [linear mixed model](/linear-mixed-model/) with the batch as a random effect.
- To matching: with unknown types, correction needs a matching of cells across batches, found from a [nearest neighbor graph](/nearest-neighbor-graph/).
- To clustering: Harmony turns correction into rounds of clustering and of a regression per cluster.

## Applications

- Joining single-cell data from several donors, runs or labs before clustering and display on [UMAP](/umap/).
- Building cell atlases from many studies.
- Comparing conditions measured in different runs, when the design is balanced.
- Removing known technical effects from bulk expression data before a test of [differential expression](/differential-expression-analysis/), or better, putting the batch into the model of the test.

## References
