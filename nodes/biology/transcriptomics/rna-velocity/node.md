---
tag: MT9F81
kind: algorithm
slug: rna-velocity
name: RNA velocity
aliases:
- scVelo dynamical model
area: biology/transcriptomics
level: research
summary: Estimate the time derivative of expression of each gene from unspliced and spliced counts with a model of splicing and degradation.
solves: [trajectory-inference]
model: real-ram
complexity:
  vars: {n: the number of cells, g: the number of genes}
  time: {worst: O(g n log n)}
  space: {extra: O(g n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Gioele La Manno, Ruslan Soldatov, Sten Linnarsson, Peter V. Kharchenko]
  note: La Manno and co-authors (2018) introduced RNA velocity in Nature with the steady-state model. Bergen and co-authors (2020) fitted the full splicing kinetics of each gene in scVelo.
prereqs: [ode-initial-value-problem, ordinary-least-squares, single-cell-rna-sequencing, rna-sequencing]
see_also: [trajectory-inference, diffusion-pseudotime, mst-pseudotime, runge-kutta-methods, matrix-exponential, linear-regression, k-nearest-neighbor-graph, umap]
sources:
  - paper: doi:10.1038/s41586-018-0414-6
    title: Gioele La Manno et al., RNA velocity of single cells, Nature 560(7719), 494 to 498 (2018)
    locator: the model of transcription, splicing and degradation, the steady-state fit of the degradation ratio for each gene, and the extrapolation of the future state of a cell
  - paper: doi:10.1038/s41587-020-0591-3
    title: Volker Bergen, Marius Lange, Stefan Peidli, F. Alexander Wolf and Fabian J. Theis, Generalizing RNA velocity to transient cell states through dynamical modeling, Nature Biotechnology 38(12), 1408 to 1414 (2020)
    locator: the dynamical model fitted by expectation maximization, the latent time, and the comparison with the steady-state model
---

RNA velocity estimates, for each cell and each gene, how fast the amount of mature RNA is changing. A cell holds both newly made RNA that still has introns (unspliced) and mature RNA (spliced). If a gene was switched on recently, a cell has more unspliced RNA than its spliced RNA would need at balance, and if it was switched off, less. La Manno and co-authors (2018) turned this into a model with three rates and a velocity $v = u - \gamma s$ for each gene. The velocities of all genes point from the current state of the cell toward its state in the near future, which gives a direction to the [trajectory inference](/trajectory-inference/) problem. This page covers the steady-state model and states what it leaves out. The algebra of the model is proved; the claim that the fitted velocities follow the real process is a heuristic.

## In plain words

A cell makes copies of a gene's message as rough drafts. The drafts are cleaned into final copies, and the final copies wear out. When a gene has just turned on, there are many drafts and few final copies. When it has just turned off, there are few drafts but many old final copies. When nothing has changed for a long time, the two stay in a fixed proportion. Learn that proportion from the cells that seem settled. Then, for every cell, the gap between its drafts and the drafts that its final copies would need tells you whether the gene is going up or down, and how fast.

## The problem

**Input.** For $n$ cells and $g$ genes, the unspliced counts $u_{ig}$ and the spliced counts $s_{ig}$, usually from reads that fall in introns and in exons, normalized for library size. A fraction $q$ of cells to treat as near steady state at each end.

**Output.** A ratio $\hat\gamma_g$ for each gene and a velocity $v_{ig}$ for each cell and gene.

**Model.** For one gene, with transcription rate $\alpha$, splicing rate $\beta$ and degradation rate $\gamma$: $du/dt = \alpha - \beta u$ and $ds/dt = \beta u - \gamma s$. The steady-state model takes $\beta$ to be the same for every gene and measures time in units of it.

## The algorithm

```pseudo id=main
RNA-VELOCITY(u, s, q)
L1  for each gene g: C ← the ⌈qn⌉ cells with the smallest s_ig and the ⌈qn⌉ with the largest
L2  γ_g ← Σ_{i ∈ C} u_ig s_ig / Σ_{i ∈ C} s_ig²          ▷ least squares through the origin
L3  v_ig ← u_ig - γ_g s_ig for every cell i
L4  ŝ_i ← s_i + Δ v_i                                    ▷ the predicted state after a short time Δ
```

Line L1 takes the cells at the two ends of the spliced counts as the cells closest to the off and the on steady states. Line L2 fits the line $u = \gamma s$ through them by [ordinary least squares](/ordinary-least-squares/) with no intercept. Line L3 is the distance of each cell above or below that line, which is $ds/dt$ when $\gamma$ is right. Line L4 moves each cell a short way along its velocity. The real tools then compare $\hat s_i$ with the other cells to draw arrows on a [UMAP](/umap/) or other display.

## Example

One gene with $\alpha = 2$, $\beta = 1$ and $\gamma = 0.5$. The on steady state is $(u, s) = (2, 4)$. Ten cells: one off, four at times 0.5, 1, 2 and 10 after the gene is switched on, four at the same times after it is switched off from the on state, and one on.

| cell | off | on 0.5 | on 1 | on 2 | on 10 | off 0.5 | off 1 | off 2 | off 10 | on |
|---|---|---|---|---|---|---|---|---|---|---|
| $u$ | 0 | 0.787 | 1.264 | 1.729 | 2.000 | 1.213 | 0.736 | 0.271 | 0.000 | 2 |
| $s$ | 0 | 0.196 | 0.619 | 1.598 | 3.946 | 3.804 | 3.381 | 2.402 | 0.054 | 4 |
| $v$ | 0 | 0.689 | 0.955 | 0.930 | 0.027 | -0.689 | -0.955 | -0.930 | -0.027 | 0 |

With $q = 0.1$, line L1 picks the off cell and the on cell, and line L2 gives $\hat\gamma = 0.5$ exactly. The velocities are positive while the gene goes up and negative while it goes down, and the two phases mirror each other. With $q = 0.2$ the fit also uses the cells at times 10, and gives 0.503. With all cells it gives 0.413, because the cells that are still changing pull the line.

## Correctness

The [proof](proofs/correctness.md) gives the exact solution of the model, also for $\beta = \gamma$, and shows that every solution tends to a steady state on the line $u = (\gamma/\beta)s$. It shows that with the true ratio, the velocity is positive at all times after a gene is switched on from zero and negative at all times after it is switched off from its on state, and that the two phases mirror each other. The fit of line L2 is exact when the chosen cells lie on the line. The step of line L4 has an error of order $\Delta^2$. On noisy data the quality is a measurement: in the tests, with 20 genes, 300 cells over an on and an off phase and Gaussian noise of 10 percent, the median relative error of $\hat\gamma$ is 0.11 at $q = 0.1$, and 94 percent of the cells with a clear velocity get the right sign.

## Complexity

Line L1 sorts the cells for each gene in $O(n\log n)$ time, and lines L2 to L4 take $O(n)$ per gene, so the time is $O(gn\log n)$ and the space $O(gn)$. In real tools, the pooling of counts over neighbors and the projection onto a display cost more than this.

## Properties

- **Per gene.** Each gene is fitted on its own; no gene borrows strength from another.
- **Gives a direction.** Unlike a pseudotime, the velocity says which way a cell is moving, so it can choose the root of a trajectory.
- **Short horizon.** The velocity describes the near future of a cell, of the order of the lifetime of the mRNA.
- **Assumes steady states.** The fit needs cells near both steady states of each gene.
- **One splicing rate.** All genes share one $\beta$, so $\hat\gamma$ is a ratio, not a rate.

## Variants and improvements

- **Dynamical model.** Bergen and co-authors (2020) fit $\alpha$, $\beta$, $\gamma$ and a switching time for each gene, and a time for each cell, by expectation maximization on the solution of the model. This removes the need for cells at steady state and gives a latent time. It is not on this page.
- **Stochastic model.** Uses the second moments of the counts as well as the means.
- **Neighbor pooling.** Averages the counts of each cell over its nearest neighbors on a [k-nearest-neighbor graph](/k-nearest-neighbor-graph/) before the fit, to reduce noise; not on this page.
- **Velocity on a display.** Turns $\hat s_i$ into transition probabilities to the other cells and draws them as arrows; not on this page.
- **Pseudotime.** [Diffusion pseudotime](/diffusion-pseudotime/) and [minimum spanning tree pseudotime](/mst-pseudotime/) give an order but no direction; velocity can choose their root.

## When to use it

Use it when the data hold unspliced and spliced counts, the cells change during the time of the sample, and you want to know which way the cells move. Check the fit on a few genes with a plot of $u$ against $s$ before you trust the arrows.

## Pitfalls

- **No steady states.** If a gene never settles, the extreme cells are not on the line and $\hat\gamma$ is biased; the example shows how much the changing cells pull the line.
- **Different rates.** Genes with two transcription rates in two cell types, or a splicing rate that differs from the others, break the model.
- **Noise.** Unspliced counts are low; in the tests, cells with a velocity near 0 get the wrong sign often.
- **Arrows on a display.** The projection of high dimensional velocities onto a two dimensional display can show directions that are not in the data.
- **Normalization.** The counts must be normalized the same way for $u$ and $s$.

## Implementations

## History

The model of transcription, splicing and degradation of one gene is a pair of linear differential equations. La Manno and co-authors (2018) used it with the steady-state fit to give each single cell a velocity and a predicted future state, in the velocyto software. Bergen and co-authors (2020) fitted the full kinetics of each gene in scVelo and showed that this works also for genes that do not reach a steady state.

## References
