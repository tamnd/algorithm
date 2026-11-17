---
tag: EQZ9B0
kind: algorithm
slug: pooling-size-factors
name: Pooled size factor deconvolution
aliases:
- scran pooling normalization
area: biology/transcriptomics
level: advanced
summary: Sum counts over pools of cells, compute size factors for the pools, and solve a linear system for the size factor of each cell.
solves: [library-size-normalization]
model: real-ram
complexity:
  vars: {n: the number of cells, m: the number of genes, q: the number of pool sizes, w: the largest pool size}
  time: {worst: O(q n m (w + log m) + q n w^2 + n^3)}
  space: {extra: O(n^2 + m n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Aaron T. L. Lun, Karsten Bach, John C. Marioni]
  note: Lun, Bach and Marioni (2016) proposed the pools and the deconvolution in Genome Biology. It is the computeSumFactors function of the R package scran.
prereqs: [median-of-ratios-normalization, least-squares-problem]
see_also: [library-size-normalization, median-of-ratios-normalization, tmm-normalization, single-cell-rna-sequencing, least-squares-problem, gaussian-elimination, highly-variable-gene-selection, umi-deduplication]
sources:
  - paper: doi:10.1186/s13059-016-0947-7
    title: Aaron T. L. Lun, Karsten Bach and John C. Marioni, Pooling across cells to normalize single-cell RNA sequencing data with many zero counts, Genome Biology 17 (2016), article 75
    locator: the sections on summation and deconvolution with linear equations, on constructing the linear system by selecting cell pools, on obtaining sensible least-squares solutions, and on clustering to weaken the non-DE assumption
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the median-of-ratios size factor applied to each pool
---

Pooled size factor deconvolution finds a size factor for each cell of a single-cell RNA-seq experiment, the number by which its counts are divided to make cells comparable. Bulk methods such as [median of ratios](/median-of-ratios-normalization/) fail on single cells, because most counts of a cell are 0 and the median of its ratios is often 0. Lun, Bach and Marioni (2016) sum the cells into pools, where counts are large, and compute a median-of-ratios factor for each pool against an average cell. The factor of a pool is the sum of the unknown factors of its cells, so many overlapping pools give a linear system, and its least squares solution gives the factor of each cell. It solves the [library size normalization](/library-size-normalization/) problem for single cells. It differs from scaling by the library size, the total count of the cell, in that it does not assume that all genes keep their share of the total.

## In plain words

You want to know how much each cell was sampled, but each cell has too few reads: most genes show zero, so the usual trick of comparing gene by gene gives nothing. So add cells together. A group of twenty cells has enough reads, and comparing the group with an average cell, gene by gene, gives a good number for the group. That number is the sum of the numbers of its cells. Make many groups that overlap: line the cells up in a ring and slide windows of several widths along it. Each window gives one sum. With enough sums you can solve for each cell, as in a puzzle where you know the sums of many rows of a grid. Cells of similar size go into the same windows, so the sums are not dominated by a few large cells.

## The problem

**Input.** A matrix of counts $Y_{gj} \ge 0$ for $m$ genes and $n$ cells, a set $W$ of pool sizes (20, 40, 60, 80 and 100 in the paper), and optionally a clustering of the cells.

**Output.** Size factors $\hat\theta_1, \dots, \hat\theta_n > 0$, scaled to mean 1.

**Model.** $E[Y_{gj}] = \theta_j\lambda_{gj}$, and $\lambda_{gj} = \lambda_g$ for more than half of the genes: most genes do not change between cells, the same assumption as for bulk data. Within a cluster this needs to hold only inside the cluster.

## The algorithm

```pseudo id=main
POOLED-SIZE-FACTORS(Y, W)          ▷ Y: m genes by n cells; W: pool sizes
L1  t_j ← Σ_g Y[g][j];  Z[g][j] ← Y[g][j] / t_j
L2  U[g] ← (1/n) Σ_j Z[g][j]                     ▷ the average cell
L3  sort the cells by t; put odd ranks up one side of a ring and even ranks down the other
L4  for each w in W and each start s on the ring do S ← the w cells from s on
L5      f_S ← median over g with U[g] > 0 of (Σ_{j∈S} Z[g][j]) / U[g]
L6  add the equation Σ_{j∈S} x_j = f_S for each pool S, with weight 1
L7  add the equation x_j = median over g of Z[g][j] / U[g] for each cell j, with weight 10^-6
L8  x ← the weighted least squares solution of all equations
L9  θ_j ← x_j t_j
L10 with clusters, run L1 to L9 in each cluster, then scale each cluster by a median ratio to a reference
L11 return θ divided by its mean
```

Line L1 divides each cell by its library size. The unknown is then $x_j = \theta_j/t_j$, which corrects the library size for genes that take a larger or smaller share in that cell; line L9 multiplies the library size back. Line L2 is the reference: an average cell, so every pool is compared with the same profile. Line L5 is the median-of-ratios factor of the pool against this reference. Line L3 makes the pools: the ring alternates the ranks, so that a window of consecutive cells holds cells of similar library size. With all window sizes, each cell is in $20 + 40 + 60 + 80 + 100 = 300$ pools. Lines L6 to L8 solve the system by least squares; the code forms the normal equations and solves them by [Gaussian elimination](/gaussian-elimination/). Line L7 adds one weak equation per cell, the single-cell median of ratios, with a tiny weight. It changes the answer very little when the pool equations determine it, and it fixes the answer when they do not.

With clusters, each cluster is normalized on its own, so the genes need to be stable only inside a cluster. The clusters are then put on one scale by the median ratio of their average normalized profiles to that of a reference cluster. The code takes the largest cluster as the reference.

## Example

Four cells and three genes. The true factors are $1, 2, 1, 4$, and gene 3 is six times higher in cell 4.

| gene | cell 1 | cell 2 | cell 3 | cell 4 |
|---|---|---|---|---|
| 1 | 10 | 20 | 10 | 40 |
| 2 | 6 | 12 | 6 | 24 |
| 3 | 4 | 8 | 4 | 96 |
| $t_j$ | 20 | 40 | 20 | 160 |

The library sizes say that cell 4 is 8 times cell 1, but the truth is 4. Dividing by $t_j$ gives $Z = (0.5, 0.3, 0.2)$ for cells 1 to 3 and $(0.25, 0.15, 0.6)$ for cell 4, so $U = (0.4375, 0.2625, 0.3)$. Sorted by size the cells are 1, 3, 2, 4, and the ring is 1, 2, 4, 3. With pool sizes 2 and 3 there are 8 pools. For the pool $\{2, 4\}$, $V = (0.75, 0.45, 0.8)$ and $V/U = (1.714, 1.714, 2.667)$, so $f = 1.714 = 12/7$. All the pool factors, in sevenths:

| pool | {1, 2} | {2, 4} | {4, 3} | {3, 1} | {1, 2, 4} | {2, 4, 3} | {4, 3, 1} | {3, 1, 2} |
|---|---|---|---|---|---|---|---|---|
| $7f_S$ | 16 | 12 | 12 | 16 | 20 | 20 | 20 | 24 |

The solution is $x = (8, 8, 8, 4)/7$, and $\theta = x\,t = (160, 320, 160, 640)/7$, which is $(0.5, 1, 0.5, 2)$ after scaling to mean 1. This is the truth: cell 4 is 4 times cell 1. The pools of size 2 alone would not be enough. On a ring of 4 they give the equations $x_1 + x_2$, $x_2 + x_4$, $x_4 + x_3$ and $x_3 + x_1$, and adding $(1, -1, 1, -1)$ in ring order changes none of these sums.

## Correctness

The [proof](proofs/correctness.md) shows that the method is exact when the counts of more than half of the genes are proportional to the true factors. Each such gene gives the pool ratio $\sum_{j \in S}x_j/\bar x$, so the median takes that value, every equation holds exactly, and the solution returns the true factors up to one constant. It also shows that the pool equations alone can fail to determine the factors. The pool matrices are circulant, and they share a null vector exactly when the number of cells $n$ divides $kw$ for every pool size $w$ and some $0 < k < n$. With the sizes of the paper this happens for every even $n$ and every multiple of 5. The weak equations of line L7 make the system positive definite, so the solution is always unique. With clusters, the method is exact when the condition holds inside each cluster and between each cluster and the reference. With real counts the factors carry noise, and the size of that error is measured, not proved.

## Complexity

On a [real RAM](/real-ram/), line L1 reads the matrix once in $O(mn)$ time. There are $qn$ pools for $q$ pool sizes. Each takes $O(mw)$ time for the sums and $O(m\log m)$ for the median, which gives $O(qnm(w + \log m))$ in all. Building the normal equations takes $O(qnw^2)$ time and solving them by elimination takes $O(n^3)$, with $O(n^2)$ space. scran solves the sparse system directly, which scales to many thousands of cells; the dense solve here is meant for small $n$.

## Properties

- **Robust to a minority of changed genes,** like median of ratios, but usable when most counts are 0.
- **Exact in the noiseless model,** for any choice of pools, as long as the weak equations are there.
- **Deterministic.** The ring and the pools depend only on the library sizes.
- **Scale free.** The factors are relative and have mean 1.
- **Local in the ring.** Each pool holds cells of similar library size, which keeps the noise of the pool sums balanced.

## Variants and improvements

- **Clustering first.** scran runs a quick clustering and normalizes each cluster on its own, which weakens the assumption to "most genes do not change inside a cluster".
- **Positive solutions.** Least squares can give negative factors for cells with very few counts. The paper discusses constrained solvers that keep the factors positive; removing such cells is the simple fix.
- **Pool sizes.** Larger pools give less noisy pool factors but fewer independent equations per cell. Sizes that share a factor with $n$ leave the pool system singular, and the weak equations then fix part of the answer.
- **Library size factors.** Plain division by the total count is the fast default in many pipelines. It is correct only when no large set of genes changes in one direction.
- **Spike-ins.** Factors from external spike-in RNA measure the total RNA of a cell, which is a different quantity from the factors here.

## When to use it

Use it for single-cell counts before log transformation, [highly variable gene selection](/highly-variable-gene-selection/) and clustering, when you expect real composition differences between cells, such as a few genes that take a large share in one cell type. It needs enough cells for the pools: at least as many as the largest pool size, per cluster. For bulk RNA-seq with few zeros use median of ratios or [TMM](/tmm-normalization/) directly.

## Pitfalls

- **Cells with very low counts** can get factors near 0 or negative. Filter low quality cells first.
- **Too few cells per cluster.** All pool sizes must fit in each cluster; smaller sizes help but give noisier pool factors.
- **Strong DE between all clusters.** The scaling between clusters still needs most genes to be stable between each cluster and the reference.
- **Genes with zero mean** carry no information and are skipped; filtering genes with a very low mean speeds up the computation and does not change the answer much.
- **Factors are not totals.** They have mean 1 and are relative; do not mix them with library sizes from another method.

## Implementations

## History

Before 2016, single-cell data were often normalized by the library size or by spike-in RNA, or with bulk methods that dropped most genes because of zeros. Lun, Bach and Marioni (2016) proposed pooling and deconvolution, with the ring of cells ordered by library size, the five window sizes and the weak single-cell equations. It became the default normalization of the scran package and of the Bioconductor workflows for single-cell data.

## References
