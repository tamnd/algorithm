---
tag: 0RVW5J
kind: algorithm
slug: diffusion-pseudotime
name: Diffusion pseudotime
aliases:
- DPT
area: biology/transcriptomics
level: advanced
summary: Order cells by a distance between their random-walk transition vectors in a diffusion map, measured from a chosen root cell.
solves: [trajectory-inference]
model: real-ram
complexity:
  vars: {n: the number of cells, d: the number of dimensions}
  time: {worst: O(n^2 d + n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Laleh Haghverdi, Maren Büttner, F. Alexander Wolf, Florian Buettner, Fabian J. Theis]
  note: Haghverdi and co-authors (2016) defined diffusion pseudotime in Nature Methods, one year after they applied diffusion maps to single-cell data.
prereqs: [diffusion-maps, markov-chain, transition-matrix, stationary-distribution, eigenvalue, single-cell-rna-sequencing]
see_also: [trajectory-inference, mst-pseudotime, rna-velocity, laplacian-matrix, spectral-clustering, nearest-neighbor-graph, principal-component-analysis, power-iteration]
sources:
  - paper: doi:10.1038/nmeth.3971
    title: Laleh Haghverdi, Maren Büttner, F. Alexander Wolf, Florian Buettner and Fabian J. Theis, Diffusion pseudotime robustly reconstructs lineage branching, Nature Methods 13(10), 845 to 848 (2016)
    locator: the definition of the accumulated transition matrix and of the diffusion pseudotime distance from a root cell
  - paper: doi:10.1093/bioinformatics/btv325
    title: Laleh Haghverdi, Florian Buettner and Fabian J. Theis, Diffusion maps for high-dimensional single-cell analysis of differentiation data, Bioinformatics 31(18), 2989 to 2998 (2015)
    locator: the diffusion map of single cells with a Gaussian kernel and its eigenvectors as coordinates
  - paper: doi:10.1016/j.acha.2006.04.006
    title: Ronald R. Coifman and Stéphane Lafon, Diffusion maps, Applied and Computational Harmonic Analysis 21(1), 5 to 30 (2006)
    locator: the normalization of the kernel by the density with the parameter alpha, and the diffusion distance
  - paper: doi:10.1038/s41587-019-0071-9
    title: Wouter Saelens, Robrecht Cannoodt, Helena Todorov and Yvan Saeys, A comparison of single-cell trajectory inference methods, Nature Biotechnology 37(5), 547 to 554 (2019)
    locator: the benchmark of trajectory inference methods on real and synthetic data
---

Diffusion pseudotime (DPT) orders single cells along a process such as differentiation. It builds a random walk on the cells, where a step goes mostly to near cells, and it adds up the walks of all lengths into one matrix. The pseudotime of a cell is the distance between its row of that matrix and the row of a root cell. Haghverdi and co-authors (2016) defined it. It answers the [trajectory inference](/trajectory-inference/) problem with no tree to build and no time scale to choose. The distance is defined exactly and has a formula in the eigenvectors of the walk; the claim that it follows the real order of the process is a heuristic.

## In plain words

Think of the cells as stepping stones. A walker on one stone jumps to a near stone more often than to a far one. Start a walker at every stone and record where it is likely to be after one jump, two jumps, and so on, and add all of these up. Two stones whose records look alike are close along the path that the stones make, even if a straight line between them would go across empty space. The pseudotime of a cell is how different its record is from the record of the start cell.

## The problem

**Input.** Cells $x_1, \dots, x_n$ in $\mathbb{R}^d$, usually the first principal components of the log expression values, a kernel width $\sigma > 0$ and a root cell $r$.

**Output.** A pseudotime $\tau_i \ge 0$ for each cell, with $\tau_r = 0$.

## The algorithm

```pseudo id=main
DPT(x_1..x_n, σ, r)
L1  K_ij ← exp(-‖x_i - x_j‖² / (2σ²)) for i ≠ j; K_ii ← 0
L2  q_i ← Σ_j K_ij; K_ij ← K_ij / (q_i q_j)                 ▷ remove the effect of density
L3  z_i ← Σ_j K_ij; T_s ← Z^(-1/2) K Z^(-1/2)               ▷ symmetric form of the walk
L4  ψ_0 ← √z / ‖√z‖                                        ▷ top eigenvector, eigenvalue 1
L5  M ← (I - T_s + ψ_0 ψ_0ᵀ)^(-1) - I                      ▷ = Σ_{t ≥ 1} (T_s^t - ψ_0 ψ_0ᵀ)
L6  τ_i ← ‖M(r, ·) - M(i, ·)‖ for every cell i
```

Line L1 is a Gaussian kernel. Line L2 divides by the density at both cells, which is the normalization of Coifman and Lafon (2006) with $\alpha = 1$. Line L3 gives a symmetric matrix that has the same eigenvalues as the walk $T = Z^{-1}K$ whose rows sum to 1. Line L4 is the eigenvector of the eigenvalue 1. Line L5 adds the walk over all numbers of steps, with the part that does not depend on the start removed; the inverse is computed by Gauss-Jordan elimination. Line L6 is the distance from the root. The paper writes the sum with the walk $T$; this page uses the symmetric form, which gives the exact eigen formula below.

## Example

Five cells on a line at $0, 1, 2, 3, 4$, with $\sigma = 1$ and root cell 0. Line L3 gives a walk where cell 0 sends most of its weight to cell 1 ($T_s$ entry 0.7038) and cell 1 sends weight to both sides (0.7038 to cell 0, 0.3312 to cell 2). Lines L5 and L6 give:

| cell | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $\tau$ | 0 | 0.5877 | 1.0140 | 1.9329 | 1.9833 |

The order is correct. The steps are not even: the last two cells are close in pseudotime, because the walk treats the two ends of the line alike.

## Correctness

The [proof](proofs/correctness.md) shows that the walk has a simple eigenvalue 1 and that all its other eigenvalues $\lambda_l$ lie strictly between $-1$ and 1 when $n \ge 3$. So the matrix of line L5 exists and equals $\sum_{t \ge 1}(T_s^t - \psi_0\psi_0^\top)$, and the pseudotime has the exact formula $\tau(x, y)^2 = \sum_{l \ge 1}(\lambda_l/(1 - \lambda_l))^2(\psi_l(x) - \psi_l(y))^2$. It is a pseudometric, and it does not change when the cells are moved, rotated or renumbered. The order of noisy cells is a measurement: in the tests, 80 cells near a line in five dimensions give a rank correlation of 0.998 with the true time at $\sigma = 0.2$. For 80 cells on an arc of $1.7\pi$, whose two ends are close in space, the pseudotime gives 0.998 and the straight distance from the root gives only 0.618.

## Complexity

The kernel takes $O(n^2d)$ time and the inverse $O(n^3)$, with $O(n^2)$ space for the dense matrices. Real tools use a sparse [nearest neighbor graph](/nearest-neighbor-graph/) as the kernel and compute only a few eigenvectors, which makes the formula of the proof cheap for many cells.

## Properties

- **No time scale.** The sum over all steps removes the number of steps $t$ that a [diffusion map](/diffusion-maps/) needs.
- **Follows the shape.** The distance runs along the cells, not across empty space.
- **Exact formula.** The pseudotime is a weighted distance in the eigenvectors of the walk.
- **Needs a root.** The data do not say where the process starts.
- **Depends on $\sigma$.** In the tests, $\sigma = 0.1$ gives 0.982 on the line and 0.961 on the arc, against 0.998 at $\sigma = 0.2$.

## Variants and improvements

- **Diffusion maps.** Use the eigenvectors $\lambda_l^t\psi_l$ for a fixed $t$ as coordinates for display (Haghverdi, Buettner and Theis 2015). DPT is not a set of coordinates but a distance that adds all $t$.
- **Branches.** The paper also finds branches by comparing the pseudotimes from several end cells; this page leaves that out.
- **Width per cell.** A kernel width that changes with the local density of cells, in place of one $\sigma$.
- **Sparse graph.** A kernel on a k-nearest-neighbor graph, as in the scanpy package, to scale to many cells.
- **Other approaches.** [Minimum spanning tree pseudotime](/mst-pseudotime/) builds a tree, and [RNA velocity](/rna-velocity/) gives a direction from spliced and unspliced counts, which can help to choose the root.

## When to use it

Use it when the cells form a continuous path or a tree and you can name a start cell. It handles curved paths that a straight distance gets wrong. The benchmark of Saelens and co-authors (2019) found that the best method depends on the shape of the trajectory, so check the result against a second method.

## Pitfalls

- **Wrong root.** A root in the middle of the path gives cells on both sides the same pseudotimes.
- **Too small $\sigma$** splits the walk into parts that almost do not touch, and the eigenvalues come near 1.
- **Too large $\sigma$** joins cells across gaps and makes the walk ignore the shape.
- **Separate groups.** Cells of a different type far from the path get large but meaningless pseudotimes; remove them first.
- **Pseudotime is not time.** It is a distance in the walk, not hours or days, and its steps need not be even, as the example shows.

## Implementations

## History

Coifman and Lafon (2006) introduced diffusion maps and the normalization of the kernel by density. Haghverdi, Buettner and Theis (2015) applied diffusion maps to single-cell differentiation data. Haghverdi and co-authors (2016) defined diffusion pseudotime and used it to find branch points. The benchmark of Saelens and co-authors (2019) compared it with many other trajectory inference methods.

## References
