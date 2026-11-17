---
tag: TKHD07
kind: algorithm
slug: tmm-normalization
name: Trimmed mean of M-values
aliases:
- TMM normalization
area: biology/transcriptomics
level: core
summary: Scale samples by a weighted trimmed mean of log fold changes against a reference, assuming most genes are not differentially expressed.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples}
  time: {worst: Θ(n m log n), best: Θ(n m log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Mark D. Robinson, Alicia Oshlack]
  note: Robinson and Oshlack described the composition effect and the TMM factor in Genome Biology in 2010. It is the default normalization of edgeR.
prereqs: [library-size-normalization, trimmed-mean]
see_also: [library-size-normalization, median-of-ratios-normalization, quantile-normalization, pooling-size-factors, differential-expression-analysis, negative-binomial-count-model, delta-method, trimmed-mean]
sources:
  - paper: doi:10.1186/gb-2010-11-3-r25
    title: Mark D. Robinson and Alicia Oshlack, A scaling normalization method for differential expression analysis of RNA-seq data, Genome Biology 11(3) (2010), article R25
    locator: the M and A values, the trim of 30 percent of the M values and 5 percent of the A values at each end, the weights from the delta method, and the example of a sample with extra genes
  - paper: doi:10.1093/bioinformatics/btp616
    title: Mark D. Robinson, Davis J. McCarthy and Gordon K. Smyth, edgeR, a Bioconductor package for differential expression analysis of digital gene expression data, Bioinformatics 26(1) (2010), pages 139 to 140
    locator: the effective library size, the library size times the normalization factor, as the offset of the negative binomial model
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the median-of-ratios size factors, the other common answer to the same problem
---

The trimmed mean of M-values (TMM) finds a normalization factor for each RNA-seq sample by comparing it with a reference sample. For each gene, M is the log ratio of the two samples' count shares and A is the mean log share. TMM removes the genes with the most extreme M values (30 percent at each end) and the most extreme A values (5 percent at each end), and takes a weighted mean of the M values that remain. The weights are the inverse of an approximate variance, so genes with more reads count more. If most genes do not change, the remaining M values all estimate the same log ratio, which is the composition effect between the samples. Robinson and Oshlack (2010) proposed it, and it is the default of edgeR. It solves the [library size normalization](/library-size-normalization/) problem, like [median of ratios](/median-of-ratios-normalization/), but it compares each sample with one real sample, it trims instead of taking a median, and it weights the genes.

## In plain words

Pick one sample as the yardstick. For every gene, ask how much bigger its share of reads is in your sample than in the yardstick, on a log scale. Most genes did not change, so most answers are about the same number. A few genes really changed and give extreme answers. Throw away the most extreme 30 percent at the top and at the bottom, and also the genes with the very highest and very lowest counts. Average what is left, and trust the genes with many reads more than the genes with few. The result tells you how much the shares differ for an ordinary gene, and so how to rescale the sample.

## The problem

**Input.** The counts $o_g$ of a sample and $r_g$ of a reference sample for genes $g = 1, \dots, n$, with library sizes $N_o = \sum_g o_g$ and $N_r = \sum_g r_g$, and the trim fractions $\theta_M = 0.3$ and $\theta_A = 0.05$.

**Output.** A factor $f > 0$ such that $N_of$ and $N_r$ are comparable library sizes: for an unchanged gene, $o_g/(N_of) \approx r_g/N_r$. For $m$ samples, the factors of all samples against one reference, rescaled to have product 1.

**Assumption.** Most genes do not change, and the genes that change are few enough that their M values fall in the trimmed tails.

## The algorithm

```pseudo id=main
TMM(o, r, N_o, N_r, θ_M = 0.3, θ_A = 0.05)          ▷ sample o against reference r
L1  keep the genes with o_g > 0 and r_g > 0, and let n be their number
L2  M_g ← log2((o_g / N_o) / (r_g / N_r))             ▷ log ratio of the shares
L3  A_g ← (log2(o_g / N_o) + log2(r_g / N_r)) / 2     ▷ mean log share
L4  v_g ← (N_o - o_g)/(N_o o_g) + (N_r - r_g)/(N_r r_g)   ▷ approximate variance of M_g
L5  λ_M ← ⌊n θ_M⌋ + 1;  λ_A ← ⌊n θ_A⌋ + 1
L6  rank the M_g and the A_g, with average ranks for ties
L7  K ← {g : λ_M ≤ rank(M_g) ≤ n + 1 - λ_M and λ_A ≤ rank(A_g) ≤ n + 1 - λ_A}
L8  f ← (Σ_{g ∈ K} M_g / v_g) / (Σ_{g ∈ K} 1 / v_g)
L9  return 2^f
```

Line L1 drops genes with a zero in either sample, because their log ratio is not defined. Lines L2 and L3 put each gene at a point $(A_g, M_g)$ of the MA plot. Line L4 is the [delta method](/delta-method/) variance of $M_g$ when each count is binomial given its library size: $\operatorname{Var}(\ln\hat p) \approx (1-p)/(Np)$ for a share $\hat p$ of $N$ reads, and the constant $(\ln 2)^2$ is the same for all genes, so it drops out of the weights. Lines L5 to L7 keep the genes whose M rank lies inside $[\lambda_M, n + 1 - \lambda_M]$ and whose A rank lies inside $[\lambda_A, n + 1 - \lambda_A]$. Both intervals are symmetric. Line L8 is the weighted mean of the kept M values. The code returns 1 when no gene is kept or when every $|M_g| < 10^{-6}$, as edgeR does.

For $m$ samples, edgeR picks as the reference the sample whose upper quartile share (the 75th percentile of its counts divided by its library size) is closest to the mean of these shares. It computes the factor of every sample against that reference, the reference getting 1, and divides all factors by their geometric mean. The effective library size $N_jf_j$ is then the offset of the [negative binomial model](/negative-binomial-count-model/).

## Example

Ten genes, a sample o with $N_o = 2503$ and a reference r with $N_r = 1260$. Genes 5 and 10 are much higher in o, and gene 7 is lower. With $n = 10$, $\lambda_M = \lfloor 3\rfloor + 1 = 4$, so the M ranks 4 to 7 are kept, and $\lambda_A = \lfloor 0.5\rfloor + 1 = 1$, so no gene is trimmed by A.

| gene | $o_g$ | $r_g$ | $M_g$ | $A_g$ | $v_g$ | M rank | kept |
|---|---|---|---|---|---|---|---|
| 1 | 120 | 100 | -0.727 | -4.019 | 0.01714 | 6.5 | yes |
| 2 | 300 | 260 | -0.784 | -2.669 | 0.00599 | 5 | yes |
| 3 | 45 | 40 | -0.820 | -5.387 | 0.04603 | 3 | no |
| 4 | 80 | 70 | -0.798 | -4.569 | 0.02559 | 4 | yes |
| 5 | 900 | 300 | 0.595 | -1.773 | 0.00325 | 9 | no |
| 6 | 60 | 50 | -0.727 | -5.019 | 0.03547 | 6.5 | yes |
| 7 | 15 | 60 | -2.990 | -5.887 | 0.08214 | 1 | no |
| 8 | 250 | 200 | -0.668 | -2.990 | 0.00781 | 8 | no |
| 9 | 33 | 30 | -0.853 | -5.819 | 0.06244 | 2 | no |
| 10 | 700 | 150 | 1.232 | -2.454 | 0.00690 | 10 | no |

Genes 1 and 6 both have the count ratio $6/5$, so their M values tie and share the rank 6.5. The weighted mean of the four kept M values is $f = -0.769$, and the factor is $2^{-0.769} = 0.587$. The unweighted mean gives 0.591. The raw library sizes say that o is 1.99 times as deep as r. The effective sizes $2503 \cdot 0.587$ and $1260$ say 1.17 times, which matches the count ratios $o_g/r_g$ of the kept genes, 1.14 to 1.2. After the rescaling to product 1, the two factors are 0.766 and 1.305, and the effective library sizes are 1917.5 and 1644.8.

## Correctness

The [proof](proofs/correctness.md) shows that swapping the two samples turns $f$ into $-f$, because the average ranks of $-M$ are $n + 1$ minus those of $M$ and the kept interval is symmetric. It shows that genes with M values below $m_-$ or above $m_+$ cannot be kept if there are at most $\lambda_M - 1$ of each, so the factor stays in $[2^{m_-}, 2^{m_+}]$. And it shows that if all other genes share exactly the same M value $m$, the factor is exactly $2^m$, because the tied block of the unchanged genes has a rank inside the kept interval and is too large to be removed by the A trim. The example of Robinson and Oshlack, a sample with as many extra genes as shared genes, gives the factor $1/2$ by this result. That the weights $1/v_g$ are good weights is a heuristic based on the delta method, and that real data have enough unchanged genes is an assumption.

## Complexity

On a [real RAM](/real-ram/), lines L1 to L4 take $\Theta(n)$ time, and the two rankings at line L6 take $\Theta(n\log n)$. So one factor costs $\Theta(n\log n)$, and the factors of $m$ samples against one reference cost $\Theta(nm\log n)$, plus $\Theta(nm\log n)$ for the upper quartiles that choose the reference. The extra space is $\Theta(n)$.

## Properties

- **Antisymmetric.** The factor of r against o is the inverse of the factor of o against r, in exact arithmetic.
- **Robust to changed genes in the tails.** Up to $\lambda_M - 1$ genes at each end of the M ranking, about 30 percent, can change by any amount without moving the factor out of the range of the other M values.
- **Exact for a common ratio.** If the unchanged genes have exactly the same ratio, the factor is that ratio.
- **Depends on the reference.** The factors of $m$ samples are computed against one sample, so a poor reference sample, for example one with low depth, adds noise to all factors.
- **Weighted.** Genes with many reads have small $v_g$ and large weight.

## Variants and improvements

- **Unweighted TMM.** Take the plain mean of the kept M values. It is less efficient when the counts differ much between genes.
- **Other trims.** The trims $\theta_M$ and $\theta_A$ are arguments. Larger trims are more robust and less efficient.
- **Upper quartile and RLE.** edgeR also offers the upper quartile factor and "RLE", which is [median of ratios](/median-of-ratios-normalization/).
- **Many zeros.** edgeR has a version, TMMwsp, that pairs the genes with a zero in one sample to use more of them. For single-cell data, [pooling size factors](/pooling-size-factors/) is the usual choice.
- **Median instead of mean.** With $\theta_M$ close to 0.5, the trimmed mean becomes the median of the M values against one reference sample, close in spirit to median of ratios.

## When to use it

Use TMM for bulk RNA-seq counts in edgeR or limma-voom, when most genes do not change and the changes are not all in one direction. It handles samples with a few very highly expressed genes well, which is the case it was made for. With strongly unbalanced changes, or a global shift in expression, use spike-ins. With single cells, use pooling.

## Pitfalls

- **Rounding can split a tie and return 1.** When the unchanged genes have exactly the same count ratio that is not a power of 2, rounding in $\log_2$ can give two blocks of M values that differ in the last bit. Each block gets its own average rank, and with few genes both can fall outside the kept interval, so that no gene is kept and the factor is 1. The tests contain such a case. Real data rarely have exact ties among many genes, but small toy examples often do.
- **The factor is not the size factor.** In edgeR, the offset is the library size times the factor. Dividing counts by the factor alone leaves the depth in.
- **Genes with a zero.** Line L1 drops them. When the two samples express quite different sets of genes, this is right, as in the example of Robinson and Oshlack; but with low depth it can drop most genes.
- **Assuming symmetry.** If 40 percent of the genes go up and none go down, the trimmed mean is pulled toward the changed genes, because they are not all in the trimmed upper tail.

## Implementations

## History

Robinson and Oshlack (2010) showed that RNA-seq counts are relative, so that a few very highly expressed genes in one sample lower the counts of all other genes. They proposed the weighted trimmed mean of M-values as the fix, with the trims of 30 and 5 percent. edgeR (Robinson, McCarthy and Smyth 2010) uses the factors to form the effective library sizes. In the same year, Anders and Huber (2010) proposed median of ratios for DESeq, which assumes the same thing in another way.

## References
