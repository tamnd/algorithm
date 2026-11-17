---
tag: 7FGQ3H
kind: problem
slug: library-size-normalization
name: Library size normalization
aliases:
- count normalization
- between-sample normalization
area: biology/transcriptomics
level: core
summary: Find a scale factor for each sample so that counts become comparable across samples with different depth and composition.
prereqs: [rna-sequencing, rpkm-and-fpkm]
see_also: [median-of-ratios-normalization, tmm-normalization, quantile-normalization, pooling-size-factors, transcripts-per-million, differential-expression-analysis, batch-effect-correction]
sources:
  - paper: doi:10.1186/gb-2010-11-3-r25
    title: Mark D. Robinson and Alicia Oshlack, A scaling normalization method for differential expression analysis of RNA-seq data, Genome Biology 11(3) (2010), article R25
    locator: the composition effect, the example of a sample with extra genes, and the TMM factor under the assumption that most genes are not differentially expressed
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the size factors of DESeq as the median of the ratios to the geometric mean over samples
  - paper: doi:10.1093/bioinformatics/19.2.185
    title: B. M. Bolstad, R. A. Irizarry, M. Astrand and T. P. Speed, A comparison of normalization methods for high density oligonucleotide array data based on variance and bias, Bioinformatics 19(2) (2003), pages 185 to 193
    locator: quantile normalization, which matches the whole distribution of each array to a common one
  - paper: doi:10.1186/s13059-015-0679-0
    title: Stephanie C. Hicks and Rafael A. Irizarry, quantro, a data-driven approach to guide the choice of an appropriate normalization method, Genome Biology 16 (2015), article 117
    locator: the assumptions behind global normalization methods and a test of whether the distributions differ between groups
  - paper: doi:10.1186/s13059-014-0550-8
    title: Michael I. Love, Wolfgang Huber and Simon Anders, Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2, Genome Biology 15(12) (2014), article 550
    locator: size factors as offsets in the negative binomial GLM, and gene-specific normalization factors
---

Library size normalization is the problem of finding one positive factor per sample, the size factor, so that the counts of a gene divided by these factors can be compared across samples. Two things make raw counts incomparable. The first is depth: a sample with twice as many reads gives about twice the count for every gene. The second is composition: the reads of a sample are shared among its genes, so when a few genes take a large share, every other gene gets fewer reads. The total count corrects for depth but not for composition. The problem cannot be solved from the counts alone, so every method assumes something, most often that most genes do not change between samples. [Median of ratios](/median-of-ratios-normalization/) and [TMM](/tmm-normalization/) solve it under that assumption. [Quantile normalization](/quantile-normalization/) assumes more: that the whole distribution of expression is the same in every sample.

## In plain words

Two samples of the same tissue are sequenced, one twice as deeply as the other. You must decide how much of the difference in counts is the machine and how much is biology. Dividing by the total number of reads seems right, but it fails when a few genes in one sample are very active. They take up reads, and every other gene looks lower than it is. So you look for a factor that makes the typical gene agree between the samples, and you trust that most genes really do agree. If that trust is wrong, no method can find the right factor from the counts alone.

## Definition

**Input.** A matrix of counts $K_{gj} \ge 0$ for genes $g = 1, \dots, n$ and samples $j = 1, \dots, m$.

**Model.** $E[K_{gj}] = s_j q_{gj}$, where $q_{gj}$ is the expression of gene $g$ in sample $j$ on a common scale and $s_j > 0$ is the size factor of sample $j$. The size factor holds the depth and every other effect that multiplies all genes of a sample by the same amount.

**Question.** Estimate $s_1, \dots, s_m$ up to one common constant, so that $K_{gj}/s_j$ estimates $q_{gj}$ up to that constant.

**Assumption.** The model is not identifiable. For any $c_1, \dots, c_m > 0$, the factors $c_js_j$ and the expressions $q_{gj}/c_j$ give the same expected counts. So a method must restrict $q$. The usual restriction is that a set $S$ of genes, more than half of all genes, does not change: $q_{gj} = q_g$ for $g \in S$ and all $j$. Other restrictions are a known set of control genes (spike-in RNA, housekeeping genes), equal total expression ($\sum_g q_{gj}$ the same in every $j$), or equal distributions of expression.

**Output use.** In a count model for [differential expression analysis](/differential-expression-analysis/), the factors enter as offsets $\log s_j$ in the [generalized linear model](/generalized-linear-model/) of each gene, so the counts are never divided. For plots, clustering and other analyses the normalized counts $K_{gj}/s_j$ are used, often on a log scale.

## Variants

- **Total count.** $s_j \propto N_j = \sum_g K_{gj}$. This is the restriction of equal total expression, and it is the depth correction of [RPKM and FPKM](/rpkm-and-fpkm/), counts per million and [TPM](/transcripts-per-million/). It fails under composition effects.
- **Upper quartile.** $s_j$ proportional to the 75th percentile of the counts of sample $j$ over genes with a count above 0. It ignores the few genes with the largest counts, which are the usual cause of composition effects.
- **Median of ratios.** $s_j$ is the median over genes of $K_{gj}$ divided by the geometric mean of gene $g$ over the samples (Anders and Huber 2010). It is exact when more than half of the usable genes do not change.
- **Trimmed mean of M-values.** Each sample is compared with a reference sample by a weighted mean of the log ratios, after the genes with extreme log ratios or extreme levels are trimmed (Robinson and Oshlack 2010).
- **Distribution matching.** [Quantile normalization](/quantile-normalization/) replaces each value by the mean of the values of the same rank in all samples. It is not a scale factor, but a nonlinear map per sample.
- **Single cells.** Most counts of one cell are 0, so ratios to a geometric mean are undefined for most genes. [Pooling size factors](/pooling-size-factors/) sums cells into pools, normalizes the pools, and solves a linear system for the cell factors.
- **Gene-specific factors.** When a bias depends on the gene, such as GC content or a change in the average transcript length between samples, the factor becomes $s_{gj}$, a matrix of offsets. DESeq2 accepts such a matrix.

## Examples

**Composition.** Two samples have the same depth, $N$ reads. Sample A expresses the same genes as sample B at the same level, and as many genes again that sample B does not express. Then half of the reads of A go to the extra genes, and each shared gene has half the count in A that it has in B. The total count gives $s_A = s_B$, so every shared gene looks two times lower in A. TMM and median of ratios use only genes that both samples express, find the log ratio $-1$ for all of them, and give $s_A/s_B = 1/2$. Robinson and Oshlack (2010) use this example to explain the composition effect.

**Median of ratios at work.** Five genes in three samples:

| gene | sample 1 | sample 2 | sample 3 |
|---|---|---|---|
| 1 | 100 | 200 | 100 |
| 2 | 50 | 100 | 50 |
| 3 | 20 | 40 | 20 |
| 4 | 300 | 600 | 3000 |
| 5 | 0 | 10 | 5 |

The totals are 470, 950 and 3175, so the total count says that sample 3 is 6.8 times as deep as sample 1. But genes 1 to 3 show that samples 1 and 3 are equally deep; gene 4 changed in sample 3, and it holds most of the reads. Median of ratios drops gene 5, which has a 0, and gives $s = (0.794, 1.587, 0.794)$, which is $2^{-1/3}$, $2^{2/3}$ and $2^{-1/3}$. Gene 1 then has the normalized count 126 in every sample, and gene 4 has 378, 378 and 3780: a tenfold change in sample 3 only.

**When the assumption fails.** After a global loss of transcription, for example when most genes drop by half in one condition, every method of this kind sees the unchanged genes as up. Only spike-in RNA added in proportion to the number of cells can show the global change.

## Known algorithms

- [Median of ratios normalization](/median-of-ratios-normalization/): $\Theta(nm)$ time plus the medians, $O(nm\log n)$ with sorting. It is the default of DESeq and DESeq2.
- [TMM normalization](/tmm-normalization/): $O(nm\log n)$ time for $m$ samples against one reference. It is the default of edgeR.
- [Quantile normalization](/quantile-normalization/): $\Theta(mn\log n)$ time. It is the standard for microarrays, as part of RMA.
- [Pooling size factors](/pooling-size-factors/): for single-cell data, with one linear system over pools of cells.
- Upper quartile and total count: $\Theta(nm)$ time with a linear-time [selection](/selection-problem/) of the quartile.

## Bounds

**Non-identifiability (a theorem).** No method that sees only the counts can tell "half of the genes doubled in sample 2" from "the other half halved and sample 2 is twice as deep". Let $A$ and $B$ split the genes in two halves. In the first world, $s = (1, 1)$, and the genes of $A$ have $q_{g2} = 2q_{g1}$, while the genes of $B$ have $q_{g2} = q_{g1}$. In the second world, $s = (1, 2)$, the genes of $A$ have $q_{g2} = q_{g1}$, and the genes of $B$ have $q_{g2} = q_{g1}/2$. In both worlds $E[K_{g2}] = 2q_{g1}$ for $g \in A$ and $q_{g1}$ for $g \in B$, so the counts have the same law. So the assumption that more than half of the genes do not change cannot be weakened to "half" for a method that is right in every such world.

**Breakdown point.** Median of ratios returns the exact factors when the counts are exactly proportional on more than half of the usable genes, whatever the other genes do. This is proved on its page. TMM is exact when the changed genes are few enough to fall in the trimmed tails, about 30 percent at each end by default, and the unchanged genes have exactly the same ratio. With counts, the factors are estimates, and their error falls as the number of unchanged genes and their depth grow. This is a measurement, not a theorem.

## Reductions

- **To a location problem.** On the log scale, $\log K_{gj} - \log K_{gk} \approx \log(s_j/s_k)$ for the unchanged genes, and other values for the changed genes. So the problem is to estimate a location from a sample with outliers. The median and the trimmed mean are the two classic robust answers, and they give median of ratios and TMM.
- **Into differential expression.** A test for [differential expression](/differential-expression-analysis/) puts $\log s_j$ in the model as an offset. Errors in the factors move every log fold change by the same amount.
- **Not batch correction.** [Batch effect correction](/batch-effect-correction/) removes effects that differ between genes, such as a batch that raises some genes and not others. Library size normalization removes one factor per sample, which is the same for all genes. Methods of batch correction expect normalized data as input.

## Applications

The factors are the first step of almost every RNA-seq analysis: differential expression with DESeq2 or edgeR, sample clustering and principal component plots, coexpression networks such as [WGCNA](/weighted-gene-coexpression-network-analysis/), and single-cell analysis after [UMI deduplication](/umi-deduplication/). Hicks and Irizarry (2015) give a test of whether the distributions differ between groups, which helps to decide whether a global method such as quantile normalization is safe.

## References
