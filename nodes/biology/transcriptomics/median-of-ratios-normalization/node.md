---
tag: NF2283
kind: algorithm
slug: median-of-ratios-normalization
name: Median-of-ratios normalization
aliases:
- DESeq size factors
area: biology/transcriptomics
level: core
summary: Take as the size factor of a sample the median over genes of its count divided by the geometric mean count of that gene across samples.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples}
  time: {worst: Θ(n m log n), best: Θ(n m log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Simon Anders, Wolfgang Huber]
  note: Anders and Huber defined the size factors of DESeq in Genome Biology in 2010. DESeq2 (Love, Huber and Anders 2014) kept them as its default.
prereqs: [library-size-normalization]
see_also: [library-size-normalization, tmm-normalization, quantile-normalization, pooling-size-factors, differential-expression-analysis, negative-binomial-count-model, trimmed-mean, selection-problem]
sources:
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the size factor estimator, the median over genes of the ratio of a count to the geometric mean of its gene over all samples
  - paper: doi:10.1186/s13059-014-0550-8
    title: Michael I. Love, Wolfgang Huber and Simon Anders, Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2, Genome Biology 15(12) (2014), article 550
    locator: the size factors as offsets of the negative binomial GLM, and the gene-specific normalization factors
  - paper: doi:10.1186/gb-2010-11-3-r25
    title: Mark D. Robinson and Alicia Oshlack, A scaling normalization method for differential expression analysis of RNA-seq data, Genome Biology 11(3) (2010), article R25
    locator: the composition effect that makes the total count a poor size factor
---

Median-of-ratios normalization finds the size factors of RNA-seq samples, the numbers by which the counts of each sample are divided to make samples comparable. For each gene, it computes the geometric mean of its counts over all samples, a pseudo-reference sample. The size factor of a sample is then the median, over genes, of the ratio of its count to this pseudo-reference. If more than half of the genes do not change between samples, their ratios all point to the true factor, and the median ignores the rest. Anders and Huber (2010) introduced it in DESeq, and it is the default of DESeq2. It is one solution of the [library size normalization](/library-size-normalization/) problem; [TMM](/tmm-normalization/) solves the same problem with a weighted trimmed mean against one real sample in place of the median against a pseudo-reference.

## In plain words

Make an average sample by taking, for each gene, the typical count of that gene across all your samples. Now compare each real sample with this average, one gene at a time. If a sample was sequenced twice as deeply, most of its genes will show about twice the average. A few genes will show something else, because they really changed. Take the middle value of all these per-gene comparisons. The genes that changed sit at the ends of the list, so the middle value tells you the depth. Genes that are missing from any sample are left out, because the comparison makes no sense for them.

## The problem

**Input.** A matrix of counts $K_{gj} \ge 0$, genes $g = 1, \dots, n$ in rows and samples $j = 1, \dots, m$ in columns.

**Output.** Size factors $\hat s_1, \dots, \hat s_m > 0$, such that $K_{gj}/\hat s_j$ is comparable across samples.

**Assumption.** $E[K_{gj}] = s_jq_{gj}$, and $q_{gj} = q_g$ for more than half of the genes that have a positive count in every sample. The factors are defined only up to a common constant. The estimator fixes it so that the factors have geometric mean 1 when the counts are exactly proportional.

## The algorithm

```pseudo id=main
MEDIAN-OF-RATIOS(K)                         ▷ K: n genes by m samples, counts ≥ 0
L1  for each gene g do                       ▷ the log of the pseudo-reference
L2      if K[g][j] > 0 for every sample j then
L3          ℓ_g ← (1/m) Σ_j ln K[g][j]   else ℓ_g ← -∞
L4  G ← {g : ℓ_g is finite}                  ▷ genes with no zero count
L5  if G is empty then fail
L6  for j ← 1 to m do
L7      r ← [ln K[g][j] - ℓ_g for g in G with K[g][j] > 0]
L8      ŝ_j ← exp(median(r))                 ▷ median of the log ratios
L9  return ŝ_1, …, ŝ_m
```

Lines L1 to L3 compute the log of the geometric mean of each gene, $\ell_g = \frac1m\sum_j\ln K_{gj}$. A gene with a zero in any sample gets $-\infty$, since its geometric mean is 0 and no ratio to it is defined. Line L4 keeps the other genes. Line L7 forms the log ratios $\ln(K_{gj}/e^{\ell_g})$ of sample $j$. The test $K_{gj} > 0$ there matters only when the reference $\ell$ comes from other samples, as in the fixed-reference variant below. Line L8 takes the median on the log scale. For an odd number of genes this is the log of the median ratio. For an even number it is the mean of the two middle log ratios, so $\hat s_j$ is the geometric mean of the two middle ratios. DESeq2 does the same.

The factors enter the analysis in two ways. For plots and clustering, the normalized counts are $K_{gj}/\hat s_j$. In the [negative binomial model](/negative-binomial-count-model/) of DESeq2, the raw counts stay as they are and $\ln\hat s_j$ is an offset in the log-linear model of the mean.

## Example

Five genes in three samples. Samples 1 and 3 have the same depth, and sample 2 is twice as deep. Gene 4 is 10 times higher in sample 3, and gene 5 has a zero.

| gene | $K_{g1}$ | $K_{g2}$ | $K_{g3}$ | geometric mean | ratio 1 | ratio 2 | ratio 3 |
|---|---|---|---|---|---|---|---|
| 1 | 100 | 200 | 100 | 125.99 | 0.7937 | 1.5874 | 0.7937 |
| 2 | 50 | 100 | 50 | 63.00 | 0.7937 | 1.5874 | 0.7937 |
| 3 | 20 | 40 | 20 | 25.20 | 0.7937 | 1.5874 | 0.7937 |
| 4 | 300 | 600 | 3000 | 814.33 | 0.3684 | 0.7368 | 3.684 |
| 5 | 0 | 10 | 5 | 0 | | | |

Gene 5 is dropped at line L4. Each sample has four ratios, and three of them are equal, so the median is that value: $\hat s = (0.7937, 1.5874, 0.7937)$, which is $(2^{-1/3}, 2^{2/3}, 2^{-1/3})$. The product is 1. The ratio $\hat s_2/\hat s_1 = 2$ is the true depth ratio, and $\hat s_3/\hat s_1 = 1$.

| gene | normalized 1 | normalized 2 | normalized 3 |
|---|---|---|---|
| 1 | 126.0 | 126.0 | 126.0 |
| 4 | 378.0 | 378.0 | 3779.8 |

The library sizes are 470, 950 and 3175. Dividing by them would make sample 3 look 6.8 times as deep as sample 1, and gene 1 would look 6.8 times lower in sample 3. Gene 4 alone holds 94 percent of the reads of sample 3. This is the composition effect.

## Correctness

The [proof](proofs/correctness.md) shows three facts in exact arithmetic. If $K_{gj} = s_jq_g$ for every usable gene, the estimator returns $s_j/\bar s$, where $\bar s$ is the geometric mean of the true factors, because every log ratio of sample $j$ equals $\ln(s_j/\bar s)$. If this holds only for a set $S$ of genes with $|S| > |G|/2$, the answer is the same, because more than half of the log ratios of each sample are equal, and then both middle positions of the sorted list hold that value. The bound $|S| > |G|/2$ cannot be improved. Last, multiplying one sample by $c$ multiplies its factor relative to every other sample by $c$. That real data have a majority of unchanged genes is an assumption, and with Poisson or negative binomial counts the estimate has an error that the tests measure but the proof does not bound.

## Complexity

On a [real RAM](/real-ram/), lines L1 to L4 read each count once, which takes $\Theta(nm)$ time. The medians at line L8 take $O(|G|\log|G|)$ time per sample with sorting, so the total is $\Theta(nm\log n)$ in the worst case. A linear-time [selection](/selection-problem/) such as [quickselect](/quickselect/) or [median of medians](/median-of-medians/) lowers this to $O(nm)$. The extra space is $\Theta(n)$ for the $\ell_g$ and one list of ratios.

## Properties

- **Robust to a minority of changed genes.** Up to half of the usable genes, less one, can change by any amount without moving the factors. This is the breakdown point of the median.
- **Scale equivariant.** Doubling all counts of one sample doubles its factor relative to the others.
- **Symmetric in the samples.** The pseudo-reference uses all samples equally, so the result does not depend on the order of the samples or on the choice of a reference sample.
- **Normalized to geometric mean 1.** In the exact case the factors multiply to 1. With real counts they are close to that.
- **Uses only genes seen in every sample.** This makes it unusable when most counts are 0, as in single-cell data.

## Variants and improvements

- **Fixed reference.** Compute $\ell_g$ once from a reference set of samples and pass it in, so that new samples get factors on the same scale without changing the old ones. The code accepts this as an argument.
- **Control genes.** Compute the medians only over genes known not to change, such as spike-ins or housekeeping genes. DESeq2 has an argument for this.
- **Positive counts.** For data with many zeros, DESeq2 has a type "poscounts", which takes the geometric mean over the positive counts only, so that fewer genes are dropped.
- **Pooling.** For single cells, [pooling size factors](/pooling-size-factors/) sums cells into pools, applies median of ratios to the pools, and solves for the cell factors.
- **Gene-specific factors.** When length or GC bias differs between samples, DESeq2 takes a matrix of normalization factors $s_{gj}$ in place of the vector.
- **Trimmed mean.** [TMM](/tmm-normalization/) replaces the median by a weighted [trimmed mean](/trimmed-mean/) of the log ratios, and the pseudo-reference by one real sample.

## When to use it

Use it on bulk RNA-seq counts when you expect most genes not to change, and when most genes have positive counts in every sample. It is the default of DESeq2, and the factors are meant for its model. For single-cell data use pooling. When you expect a global shift, such as a general loss of transcription in one condition, no method of this kind can see it; use spike-ins. When you need the whole distribution to match, as for microarrays, use [quantile normalization](/quantile-normalization/), which makes a stronger assumption.

## Pitfalls

- **Dropping too many genes.** One zero in one sample removes a gene. With many samples, or with low depth, few genes may be left, and the factors become noisy.
- **Many changes in one direction.** If 40 percent of the genes go up in one condition, the median is still right in exact arithmetic, but with noise it moves toward the changed genes. Check the plot of log ratios against the mean: the unchanged genes should form a band at the line of the factor.
- **Normalized counts as input.** DESeq2 and edgeR need raw counts. Passing them $K_{gj}/\hat s_j$ breaks the variance model, because the variance of a count depends on its size.
- **Size factor is not library size.** The factors are relative and have geometric mean about 1. They are not the number of reads. Mixing them with the total counts of another method gives wrong offsets.
- **Low-count genes.** Genes with counts of 1 or 2 have very noisy ratios. They rarely move the median, but filtering them first does no harm.

## Implementations

## History

Anders and Huber (2010) introduced the size factors in DESeq, with the motivation that the total count is dominated by a few highly expressed genes. In the same year, Robinson and Oshlack (2010) described the composition effect and proposed TMM. Love, Huber and Anders (2014) kept median of ratios as the default of DESeq2 and allowed gene-specific factors in its place.

## References
