---
tag: MTE8PT
kind: algorithm
slug: mnn-batch-correction
name: Mutual nearest neighbors batch correction
aliases:
- MNN correction
area: biology/transcriptomics
level: advanced
summary: Pair cells across batches that are mutual nearest neighbors, average their difference vectors, and shift one batch onto the other.
solves: [batch-effect-correction]
model: real-ram
complexity:
  vars: {n: the number of cells per batch, q: the number of batches, d: the number of genes, k: the number of neighbors}
  time: {worst: O(q^2 n^2 (d + log n) + q k n^2 d)}
  space: {extra: O(q n d + k n d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Laleh Haghverdi, Aaron T. L. Lun, Michael D. Morgan, John C. Marioni]
  note: Haghverdi, Lun, Morgan and Marioni (2018) proposed matching mutual nearest neighbors across single-cell batches in Nature Biotechnology. It is the mnnCorrect and fastMNN functions of the R package batchelor.
prereqs: [k-nearest-neighbor-graph, euclidean-distance, cosine-similarity, single-cell-rna-sequencing]
see_also: [batch-effect-correction, combat, nearest-neighbor-graph, kernel-density-estimation, principal-component-analysis, shared-nearest-neighbor-clustering, umap, t-sne]
sources:
  - paper: doi:10.1038/nbt.4091
    title: Laleh Haghverdi, Aaron T. L. Lun, Michael D. Morgan and John C. Marioni, Batch effects in single-cell RNA-sequencing data are corrected by matching mutual nearest neighbors, Nature Biotechnology 36(5), 421 to 427 (2018)
    locator: the Results section on the MNN method and Figure 1, with the three assumptions, the cosine normalization, the pair vectors and the Gaussian kernel average
  - paper: doi:10.1016/j.cell.2019.05.031
    title: Tim Stuart et al., Comprehensive integration of single-cell data, Cell 177(7), 1888 to 1902 (2019)
    locator: the anchors between data sets, which are mutual nearest neighbors in a shared low dimensional space
  - paper: doi:10.1186/s13059-019-1850-9
    title: Hoa Thi Nhu Tran et al., A benchmark of batch-effect correction methods for single-cell RNA sequencing data, Genome Biology 21, article 12 (2020)
    locator: the comparison of 14 correction methods on several data sets, and the recommendation of Harmony, LIGER and Seurat 3
  - paper: doi:10.1038/s41592-019-0619-0
    title: Ilya Korsunsky et al., Fast, sensitive and accurate integration of single-cell data with Harmony, Nature Methods 16(12), 1289 to 1296 (2019)
    locator: the Harmony algorithm, which alternates soft clustering of all cells with a correction per cluster
---

Mutual nearest neighbors (MNN) batch correction removes batch effects from single-cell RNA-seq data by finding cells of the same type in two batches. A cell of one batch and a cell of the other are a pair when each is among the $k$ nearest neighbors of the other across the batches. The difference between the two cells of a pair estimates the batch effect at that place, and each cell of the second batch moves by a smoothed average of these differences. Haghverdi, Lun, Morgan and Marioni (2018) proposed it. Unlike [ComBat](/combat/), which removes one shift per gene and batch, it does not need the batches to hold the same mix of cell types, and the shift can change from one cell type to another. It solves the [batch effect correction](/batch-effect-correction/) problem for single cells, under the assumption that the batches share at least one cell type.

## In plain words

Two labs measured the same kinds of cells, but every cell from lab B looks a bit off in a certain direction. Find pairs of cells, one from each lab, that each pick the other as one of their closest matches in the other lab. Such pairs are most likely the same kind of cell, so the gap between them is the lab effect. Each cell of lab B then moves by the average gap of the pairs near it, with near pairs counting more. A kind of cell that only lab B has finds no partner, but it still moves with the pairs closest to it, so it is not pushed onto a different kind of cell.

## The problem

**Input.** Batches of cells, each cell a vector of log expression values over the same genes, a number of neighbors $k$ and a kernel width $\sigma$. The first batch is the reference.

**Output.** The batches in one space, with the batch effect removed.

**Assumptions** (Haghverdi et al. 2018): at least one cell population is present in both batches, the batch effect is almost orthogonal to the biological subspace, and the batch effect varies much less than the biology between cell types.

## The algorithm

```pseudo id=main
MNN-CORRECT(batches, k, σ)
L1  divide every cell by its Euclidean norm                     ▷ cosine normalization
L2  for the reference R and the next batch B: N_R(b) ← the k nearest cells of R to b; N_B(r) ← the k nearest cells of B to r
L3  P ← all pairs (r, b) with r ∈ N_R(b) and b ∈ N_B(r)
L4  v_p ← r - b for each pair p = (r, b)
L5  for each cell x of B: c(x) ← Σ_p w_p v_p / Σ_p w_p, with w_p = exp(-‖x - b_p‖² / σ²)
L6  replace each cell x of B by x + c(x)
L7  add the corrected B to R and go to L2 with the next batch
```

Line L1 is the cosine normalization of the paper. After it, cells that differ only by a factor in all genes are the same point, and the distance between two cells depends only on the [cosine similarity](/cosine-similarity/) of their profiles. Lines L2 and L3 find the mutual pairs with two neighbor searches across the batches. Line L4 gives one batch vector per pair. Line L5 averages them with a Gaussian kernel on the distance from $x$ to the cell of $B$ in each pair, so the correction of a cell comes mostly from pairs in its own part of the data; this is a kernel smoother of the kind used in [kernel density estimation](/kernel-density-estimation/). Line L7 merges the batches one at a time onto the reference.

## Example

Five reference cells and five cells of a second batch in two dimensions, with $k = 1$ and no cosine normalization. The reference has two cells of a type on the left and three of a type on the right. The second batch has three on the left, one on the right, and one cell of a type the reference does not have. The batch effect moved every cell of $B$ up by 3.

| reference $R$ | $(0, 0)$ | $(1, 0)$ | $(6, 0)$ | $(7, 0)$ | $(8, 0)$ |
|---|---|---|---|---|---|
| batch $B$ | $(0, 3)$ | $(1, 3)$ | $(2, 3)$ | $(7, 3)$ | $(3, 9)$ |

The nearest cell of $R$ to $(2, 3)$ is $(1, 0)$, but the nearest cell of $B$ to $(1, 0)$ is $(1, 3)$, so $(2, 3)$ has no pair. In the same way $(6, 0)$ and $(8, 0)$ pick $(7, 3)$, which picks $(7, 0)$. The mutual pairs are $(0, 0)$ with $(0, 3)$, $(1, 0)$ with $(1, 3)$, and $(7, 0)$ with $(7, 3)$. All three pair vectors are $(0, -3)$, so every cell of $B$ moves by $(0, -3)$: the left and right cells land on the reference line, and the new type goes to $(3, 6)$, away from both. Moving $B$ by the difference of the batch means would use $(1.8, -4.2)$, which is wrong, because the two batches have different mixes of the two types.

## Correctness

The [proof](proofs/correctness.md) shows that the correction of every cell is a weighted mean of the pair vectors with positive weights, so a batch effect that is the same for all pairs is removed exactly, and no cell moves further than the longest pair vector. It shows that with $k = 1$ a translation shorter than half of the smallest distance between reference cells gives only true pairs, so the second batch lands exactly on the reference. It also shows that cosine normalization removes a scale factor of each cell. When the batch effect is not constant, or pairs join cells of different types, the result is an estimate, and its error is measured, not proved.

## Complexity

With $q$ batches of $n$ cells and $d$ genes, the brute force neighbor searches for batch $i$ compare its cells with the $(i - 1)n$ cells corrected so far, which gives $O(q^2n^2(d + \log n))$ time in all. There are at most $kn$ pairs per batch, so line L5 takes $O(kn^2d)$ per batch. The space is $O(qnd)$ for the cells and $O(knd)$ for the pair vectors. fastMNN works in a space of principal components, which makes $d$ small, and real tools use approximate neighbor search.

## Properties

- **Local correction.** The shift can differ between cell types, because each cell uses the pairs near it.
- **Robust to different cell type mixes.** Cells without a partner do not change the pairs.
- **Bounded.** The correction is a convex combination of the pair vectors.
- **Order dependent.** With more than two batches the result depends on the order in which they are merged.
- **Changes the expression values.** The output is a corrected matrix, not a new embedding, so it can be used for clustering and display; using it for tests of differential expression is not advised.

## Variants and improvements

- **fastMNN.** Finds the pairs and corrects in a space of [principal components](/principal-component-analysis/) shared by the batches, which is much faster.
- **Seurat anchors.** Stuart and co-authors (2019) find mutual nearest neighbors in a shared space from [canonical correlation analysis](/canonical-correlation-analysis/), score them, and use them as anchors for the correction.
- **Harmony.** Korsunsky and co-authors (2019) cluster the cells of all batches together and remove the batch effect cluster by cluster in principal component space, in rounds.
- **Deep models.** [Variational autoencoders](/variational-autoencoder/) such as scVI learn a latent space that leaves out the batch.
- **ComBat.** [ComBat](/combat/) is simpler and works when each batch holds the same cell types.

## When to use it

Use it to put single-cell batches into one space before clustering, display on [UMAP](/umap/) or [t-SNE](/t-sne/), or trajectory inference, when the batches share some cell types but not necessarily in the same proportions. Merge the largest or most diverse batch first, as the reference. The benchmark of Tran and co-authors (2020) recommends Harmony, LIGER and Seurat 3 over the other methods it compared, so try more than one method.

## Pitfalls

- **No shared types.** If the batches share no cell type, every pair is wrong, and the method forces unrelated cells together.
- **Too large a $k$.** In the tests, with two cell types and $k = 10$, 2 of 222 pairs joined different types; with $k = 20$, 80 of 560 did.
- **Large batch effects** break the nearest neighbor search: if the effect is larger than the distances between types, the pairs are wrong.
- **Over-correction** of real biological differences between conditions, for example between a treated and a control batch.
- **Batch order.** With many batches, merge in a fixed and sensible order, and check the result.

## Implementations

## History

Before 2018, single-cell batches were often corrected with bulk methods such as ComBat or limma, which assume the same mix of cell types in each batch. Haghverdi, Lun, Morgan and Marioni (2018) proposed pairing mutual nearest neighbors across batches, which needs only one shared population. In 2019, the anchors of Seurat (Stuart et al.) built on mutual nearest neighbors, and Harmony (Korsunsky et al.) took another approach with clusters. The benchmark of Tran and co-authors (2020) compared 14 such methods.

## References
