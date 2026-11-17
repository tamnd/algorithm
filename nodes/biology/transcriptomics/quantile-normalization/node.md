---
tag: C7FM0S
kind: algorithm
slug: quantile-normalization
name: Quantile normalization
aliases:
- quantile normalisation
area: biology/transcriptomics
level: core
summary: Make the distributions of all samples identical by replacing each value with the mean of the values of the same rank across samples.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples}
  time: {worst: Θ(m n log n), best: Θ(m n log n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2003
  people: [Benjamin M. Bolstad, Rafael A. Irizarry, Magnus Astrand, Terence P. Speed]
  note: Bolstad, Irizarry, Astrand and Speed compared normalization methods for oligonucleotide arrays in Bioinformatics in 2003 and recommended quantile normalization, which became part of the RMA method for Affymetrix arrays.
prereqs: [library-size-normalization, sorting-problem]
see_also: [library-size-normalization, median-of-ratios-normalization, tmm-normalization, batch-effect-correction, differential-expression-analysis, moderated-t-statistic, sorting-problem, prefix-sums]
sources:
  - paper: doi:10.1093/bioinformatics/19.2.185
    title: B. M. Bolstad, R. A. Irizarry, M. Astrand and T. P. Speed, A comparison of normalization methods for high density oligonucleotide array data based on variance and bias, Bioinformatics 19(2) (2003), pages 185 to 193
    locator: the quantile normalization algorithm, its motivation by the quantile-quantile plot, and its comparison with scaling and nonlinear methods
  - paper: doi:10.1186/s13059-015-0679-0
    title: Stephanie C. Hicks and Rafael A. Irizarry, quantro, a data-driven approach to guide the choice of an appropriate normalization method, Genome Biology 16 (2015), article 117
    locator: the assumption that the distributions do not differ between groups, and a test of it before quantile normalization is used
---

Quantile normalization makes the distribution of values the same in every sample. It sorts each sample, averages the sorted samples position by position to get a target distribution, and then gives every value the target value of its rank in its own sample. So the smallest value of every sample becomes the mean of the smallest values, the second smallest becomes the mean of the second smallest values, and so on. Bolstad et al. (2003) proposed it for oligonucleotide microarrays, and it is the normalization step of RMA. Unlike [median of ratios](/median-of-ratios-normalization/) and [TMM](/tmm-normalization/), it is not one scale factor per sample. It is a nonlinear map per sample, and it assumes more: that the whole distribution of expression, not just the typical gene, is the same in every sample.

## In plain words

Line up the values of each sample from smallest to largest. Now look across the samples at the first place in each line, and take the average. Do the same for the second place, the third, and so on. This gives one shared line of values. Then go back to each sample and replace its smallest value with the shared smallest value, its second smallest with the shared second smallest, and so on. Every sample now has exactly the same set of values, and each gene keeps its place in the order inside its own sample. If two values in a sample are equal, they both get the average of the shared values for their places.

## The problem

**Input.** A matrix $x_{gj}$ of expression values, genes $g = 1, \dots, n$ in rows and samples $j = 1, \dots, m$ in columns. For microarrays these are usually log intensities.

**Output.** A matrix $y_{gj}$ in which every column has the same empirical distribution, and the order of the values inside each column is kept.

**Assumption.** The differences between the distributions of the samples are technical. The biological differences affect few genes, or affect them in a way that does not change the distribution.

## The algorithm

```pseudo id=main
QUANTILE-NORMALIZE(x)                         ▷ x: n genes by m samples
L1  sort each column j: x_(1)j ≤ … ≤ x_(n)j
L2  t_i ← (1/m) Σ_j x_(i)j  for i = 1, …, n    ▷ the target distribution
L3  for j ← 1 to m do
L4      for each block of equal values of column j, at sorted positions a, …, b do
L5          give each entry of the block the value (t_a + … + t_b) / (b - a + 1)
L6  return y
```

Lines L1 and L2 build the target. It is the mean of the $m$ sorted columns, so it is a distribution in between the samples. Lines L3 to L5 map each column onto the target by rank. Without ties, a block is one entry and gets $t_a$. With ties, all entries of the block get the mean of the target over their positions, so the result does not depend on how the sort orders equal values. The code finds these means in $O(1)$ each from the [prefix sums](/prefix-sums/) of $t$. This tie rule is one fixed choice; software packages treat ties in other ways, so results on data with many ties can differ between packages.

## Example

Four genes in three samples:

| gene | $x_{g1}$ | $x_{g2}$ | $x_{g3}$ |
|---|---|---|---|
| 1 | 2 | 4 | 7 |
| 2 | 5 | 1 | 3 |
| 3 | 3 | 6 | 9 |
| 4 | 8 | 2 | 5 |

The sorted columns are (2, 3, 5, 8), (1, 2, 4, 6) and (3, 5, 7, 9). Their means by position are the target $t = (2, 10/3, 16/3, 23/3)$. In column 1, gene 1 has rank 1, gene 3 rank 2, gene 2 rank 3 and gene 4 rank 4.

| gene | $y_{g1}$ | $y_{g2}$ | $y_{g3}$ |
|---|---|---|---|
| 1 | 2 | 16/3 | 16/3 |
| 2 | 16/3 | 2 | 2 |
| 3 | 10/3 | 23/3 | 23/3 |
| 4 | 23/3 | 10/3 | 10/3 |

Every column now holds the values 2, 10/3, 16/3 and 23/3. Gene 1, which was the smallest in sample 1 and the third smallest in samples 2 and 3, gets 2 in sample 1 and 16/3 in the others.

**Ties.** For the matrix with rows (1, 10), (1, 20) and (3, 30), the target is $(5.5, 10.5, 16.5)$. In column 1, the two values 1 hold positions 1 and 2, so both get $(5.5 + 10.5)/2 = 8$, and the value 3 gets 16.5. Column 2 has no ties and gets 5.5, 10.5 and 16.5. Both columns sum to 32.5.

## Correctness

The [proof](proofs/correctness.md) shows that the target is sorted, so that a column with no ties gets exactly the values $t_1 \le \dots \le t_n$, and so all such columns have the same distribution. It shows that the order inside a column is kept, with ties or without: a smaller value never gets a larger result, because a mean of a sorted run lies between its first and its last terms. Every output column has the same sum, the mean of the input column sums, also with ties. Without ties the method is idempotent: normalizing the result again changes nothing. That the samples should have the same distribution is an assumption about the data, not something the proof can show.

## Complexity

On a [real RAM](/real-ram/), sorting the $m$ columns at line L1 takes $\Theta(mn\log n)$ time, which is the cost of the [sorting problem](/sorting-problem/). The target at line L2 and the assignment at lines L3 to L5 take $\Theta(mn)$, given the sorted order of each column and the prefix sums of $t$. The extra space is $\Theta(mn)$ for the output and the sorted columns. If the sorted order of each column is kept from line L1, line L3 needs no new sort.

## Properties

- **Same distribution.** Without ties, every column of the output has exactly the target values.
- **Order kept.** Within each column, the order of the values is kept, and equal values stay equal.
- **Same sum and same mean.** Every column of the output has the mean of the input column sums.
- **Idempotent.** Without ties, a second pass changes nothing, in exact arithmetic.
- **Not a scale factor.** The map differs between samples and between parts of the distribution, so it can fix nonlinear differences that a single factor cannot fix.
- **Rank based.** The output depends on each value only through its rank in its column. Two genes with the same rank in every sample get the same values.

## Variants and improvements

- **Fixed target.** Use a target computed from a reference set of samples, so that new samples can be normalized without changing the old ones. The code accepts a target as an argument.
- **Normalization within groups.** When the groups of a study are expected to differ in distribution, normalize within each group only. This keeps the differences between groups, at the price of not removing technical effects that line up with the groups.
- **Median target.** Use the median of the sorted values at each position instead of the mean, which is more robust to one bad sample.
- **Scaling methods.** For RNA-seq counts, the usual choice is a factor per sample, from [median of ratios](/median-of-ratios-normalization/) or [TMM](/tmm-normalization/), which assumes only that most genes do not change.

## When to use it

Use it for microarray data, on the log scale, when the samples come from similar biological material, and before a gene-wise test such as the [moderated t-statistic](/moderated-t-statistic/). Use it when the distributions differ for technical reasons, such as scanner settings or RNA quality, in a nonlinear way. Do not use it when the conditions are expected to differ in their overall distribution, such as different tissues, or a treatment that changes the expression of many genes in one direction. Hicks and Irizarry (2015) give a test of this assumption. For RNA-seq counts in a negative binomial model, use a scale factor instead.

## Pitfalls

- **Removing real differences.** If one condition has globally higher expression of many genes, quantile normalization forces it back to the common distribution and removes the effect.
- **Many ties.** RNA-seq counts have many zeros and small integers, so large tied blocks occur, and the tie rule matters. Packages differ, so results are not always comparable.
- **Counts after normalization.** The output values are not counts, so they cannot go into a count model.
- **Few genes.** With few genes, the target is a poor estimate of a distribution, and the method can create artifacts.
- **Normalizing with batch structure.** Quantile normalization is not [batch effect correction](/batch-effect-correction/). It removes differences in distribution, but not effects that move some genes and not others.

## Implementations

## History

Before 2003, arrays were normalized by a scale factor per array or by smooth curves fitted between pairs of arrays. Bolstad et al. (2003) proposed to make the distributions identical, an idea that comes from the quantile-quantile plot: two samples with the same distribution lie on the diagonal of that plot. They showed that it reduced variance with little bias on spike-in data sets, and it became the normalization step of the RMA method for Affymetrix arrays. Hicks and Irizarry (2015) studied when its assumption fails and gave a test.

## References
