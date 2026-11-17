---
tag: C9281K
kind: problem
slug: trajectory-inference
name: Trajectory inference
aliases:
- pseudotime inference
- pseudotime ordering
area: biology/transcriptomics
level: advanced
summary: Order cells along a continuous process such as differentiation, and find its branches, from a snapshot of single-cell profiles.
prereqs: [single-cell-rna-sequencing, nearest-neighbor-graph, principal-component-analysis]
see_also: [mst-pseudotime, diffusion-pseudotime, rna-velocity, diffusion-maps, variational-autoencoder, minimum-spanning-tree, umap, t-sne]
sources:
  - paper: doi:10.1038/s41587-019-0071-9
    title: Wouter Saelens, Robrecht Cannoodt, Helena Todorov and Yvan Saeys, A comparison of single-cell trajectory inference methods, Nature Biotechnology 37(5), 547 to 554 (2019)
    locator: the types of trajectory, the benchmark of methods on real and synthetic data, and the guidelines for choosing a method
  - paper: doi:10.1038/nbt.2859
    title: Cole Trapnell et al., The dynamics and regulators of cell fate decisions are revealed by pseudotemporal ordering of single cells, Nature Biotechnology 32(4), 381 to 386 (2014)
    locator: the idea of pseudotime and the ordering of cells along a minimum spanning tree
  - paper: doi:10.1038/nmeth.3971
    title: Laleh Haghverdi, Maren Büttner, F. Alexander Wolf, Florian Buettner and Fabian J. Theis, Diffusion pseudotime robustly reconstructs lineage branching, Nature Methods 13(10), 845 to 848 (2016)
    locator: the ordering of cells by a random-walk distance and the detection of branches
  - paper: doi:10.1038/s41586-018-0414-6
    title: Gioele La Manno et al., RNA velocity of single cells, Nature 560(7719), 494 to 498 (2018)
    locator: the direction of change of each cell from unspliced and spliced counts
---

Trajectory inference orders single cells along a continuous process, such as the differentiation of stem cells into mature types, from one snapshot of many cells. Each cell is measured once, at one moment, but a population that changes all the time holds cells at every stage. A method finds a graph through the cells, often a path or a tree, assigns each cell to a place on it, and gives each cell a pseudotime: its position along the process from a chosen start. The known methods build a tree or graph through the cells and an order on it, and there is no general guarantee that the order is the real one. Saelens and co-authors (2019) compared many methods and found that the best choice depends on the shape of the trajectory.

## In plain words

Imagine one photo of a long road race, taken from above. Each runner is a cell, and you see where each is, but not when they started. Runners who are close on the road are at a similar stage. Join the runners along the road and you can order them from the start to the finish, even though you only have one photo. Where the road forks, the runners split into groups. The photo does not tell you which end is the start, or how fast the runners move; you must know that from somewhere else.

## Definition

**Input.** Cells $x_1, \dots, x_n$ in a space of expression, usually reduced by [principal component analysis](/principal-component-analysis/), and often a start cell or start cluster.

**Output.** A graph $G$ whose edges are the paths of the process, a place on $G$ for each cell, and a pseudotime $\tau_i$ for each cell, the distance along $G$ from the start. Branch points of $G$ are where one cell fate splits into several.

**Types of trajectory.** Saelens and co-authors group them into types such as linear, cycle, bifurcation, tree, graph and disconnected.

**What a snapshot cannot give (a theorem).** Let the cells be states $c(t_i)$ on a curve $c$ at unknown times $t_i$. For any strictly increasing function $h$, the curve $c \circ h^{-1}$ at the times $h(t_i)$ gives exactly the same cells. So the data fix at most the order of the cells along the curve, and its reverse, but not the real time or the speed of the process. *Proof.* $c(h^{-1}(h(t_i))) = c(t_i)$ for every $i$, and the set of cells is all that is measured. $\square$ The direction needs a known start or a different kind of data, such as [RNA velocity](/rna-velocity/), and a time scale needs cells sampled at known times.

## Variants

- **Linear or branched.** A single path, or a tree with branch points.
- **With or without a root.** Most methods need the start cell; some find it from the data with extra assumptions.
- **Cycles.** The cell cycle is a closed loop, which a tree cannot represent.
- **Disconnected.** Several separate processes in one data set.
- **With direction.** Use unspliced and spliced counts to give each cell a direction.

## Examples

**A small Y.** The eight cells of the example on the [minimum spanning tree pseudotime](/mst-pseudotime/) page form a stem of three cells and two arms. The tree finds the branch point, and with the start cell at the base of the stem the two arms get the same pseudotimes at the same depth. Without a given start, the longest path of the tree runs from one arm tip to the other, so the default start is a tip, which shows why the start must be given.

**A curve that comes back.** On the [diffusion pseudotime](/diffusion-pseudotime/) page, cells on an arc whose two ends are close in space get the right order from the random-walk distance, with a rank correlation of 0.998 with the true time in the tests, while the straight distance from the start cell gives only 0.618.

## Known algorithms

- **[Minimum spanning tree pseudotime](/mst-pseudotime/).** A [minimum spanning tree](/minimum-spanning-tree/) on the cells (Monocle 1, Trapnell et al. 2014) or on cluster centers (TSCAN), and the distance along the tree. The tree is exact; it is sensitive to noise when built on cells.
- **[Diffusion pseudotime](/diffusion-pseudotime/)** (Haghverdi et al. 2016). A distance from a random walk on the cells that adds up the walk over all numbers of steps. It needs no tree, and it has an exact formula in the eigenvectors of the walk. It differs from a [diffusion map](/diffusion-maps/), which gives coordinates at one chosen number of steps and is used for display.
- **Cluster graphs.** Methods such as Slingshot and PAGA build a graph on clusters and then order the cells on it.
- **Principal curves and graphs.** Fit a smooth curve or a graph through the cells, as in later versions of Monocle.
- **[RNA velocity](/rna-velocity/)** (La Manno et al. 2018). It does not order the cells by itself; it gives each cell a local direction from a model of splicing, which can choose the start and the direction of a trajectory found by another method.
- **Learned spaces.** A [variational autoencoder](/variational-autoencoder/) learns a low dimensional space of the cells. It does not give an order; a trajectory method is then run in that space.

## Bounds

There is no general guarantee: by the theorem above, a snapshot does not fix the time, the speed or the direction, and noise can change the graph. Some results are exact under strong assumptions: on the MST page, if the distance between two cells grows strictly with the gap between their times, the tree is the path of consecutive cells and the pseudotime gives the true order. Everything else is measured on simulated and real data with known order, as in the benchmark of Saelens and co-authors. Display methods such as [t-SNE](/t-sne/) and [UMAP](/umap/) do not keep distances between groups, so a path seen on such a drawing is not evidence of a trajectory.

## Reductions

- To a spanning tree: order by distance along a minimum spanning tree of cells or clusters.
- To a random walk: order by a distance between rows of the accumulated transition matrix of a walk on a neighbor graph.
- To clustering and a graph on clusters: cluster first, then find the graph of clusters and place the cells on its edges.
- From dynamics: with spliced and unspliced counts, a model of each gene gives local directions that can orient any of the above.

## Applications

- Finding the order of states in the differentiation of stem cells, such as blood cells from their precursors.
- Finding genes that change along a process, by testing expression against pseudotime.
- Finding branch points where cells choose between fates, and the genes that change near them.
- Studying responses to a stimulus over a continuum of cell states.

## References
