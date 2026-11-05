---
tag: 7C5GE2
kind: problem
slug: graph-edit-distance
name: Graph edit distance
aliases:
- GED
area: graphs/graph-isomorphism
level: core
summary: Minimum total cost of vertex and edge insertions, deletions and substitutions that turn one graph into another; NP-hard, zero exactly for isomorphic graphs under positive costs.
model: word-ram
complexity:
  vars: {n: the number of vertices of the larger graph}
  time: {worst: O(n! n^2)}
prereqs: [graph-isomorphism-problem, edit-distance, assignment-problem]
see_also: [maximum-common-subgraph, subgraph-isomorphism, tree-edit-distance, hungarian-algorithm, vf2-algorithm, np-hard]
sources:
  - paper: doi:10.1109/TSMC.1983.6313167
    title: Alberto Sanfeliu and King-Sun Fu, A distance measure between attributed relational graphs for pattern recognition, IEEE Transactions on Systems, Man, and Cybernetics 13(3), 353 to 362 (1983)
    locator: the whole paper (edit operations on attributed graphs and the distance they define)
  - paper: doi:10.1016/S0167-8655(97)00060-3
    title: Horst Bunke, On a relation between graph edit distance and maximum common subgraph, Pattern Recognition Letters 18(8), 689 to 694 (1997)
    locator: the whole paper (for a particular cost function the edit distance is determined by the maximum common subgraph)
  - paper: doi:10.1016/j.imavis.2008.04.004
    title: Kaspar Riesen and Horst Bunke, Approximate graph edit distance computation by means of bipartite graph matching, Image and Vision Computing 27(7), 950 to 959 (2009)
    locator: the whole paper (the cost matrix and the assignment-based upper bound)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.4, Subgraph isomorphism and Largest common subgraph (the NP-complete problems that edit distance contains)
---

The graph edit distance between two graphs is the smallest total cost of a sequence of edit operations, inserting, deleting or relabeling vertices and edges, that turns the first graph into a graph isomorphic to the second. It is a distance on graphs up to isomorphism: with positive costs it is zero exactly for [isomorphic](/graph-isomorphism-problem/) graphs, and it grows as the graphs differ more. Computing it is [NP-hard](/np-hard/), since it contains [subgraph isomorphism](/subgraph-isomorphism/) and [maximum common subgraph](/maximum-common-subgraph/) as special cases, and exact methods are limited to a few dozen vertices. It is widely used in pattern recognition and chemistry, mostly through fast approximations by the [assignment problem](/assignment-problem/).

## In plain words

Think of two drawings of networks. You may change the first drawing step by step: add a point, remove a point, add a line, remove a line, or change the name tag on a point or line. Each kind of step has a price. The edit distance is the lowest total price to make the first drawing look exactly like the second, up to renaming the points. If the two drawings are the same network, the price is zero. The hard part is to find which point of one drawing should become which point of the other; once that is fixed, the price is easy to count.

## Definition

Graphs here are simple and undirected, with labels on vertices and edges from label sets $L_V$ and $L_E$; unlabeled graphs use one label. Directed graphs work the same way with arcs. An **edit operation** is one of:

- vertex insertion with label $a$, vertex deletion, vertex substitution of label $a$ by $b$;
- edge insertion with label $a$, edge deletion, edge substitution.

Each operation $o$ has a cost $c(o) \ge 0$; deleting a vertex requires deleting its edges first. An **edit path** from $G_1$ to $G_2$ is a sequence $o_1, \ldots, o_t$ that turns $G_1$ into a graph isomorphic to $G_2$.

**Graph edit distance.**
- Input: graphs $G_1$, $G_2$ and the cost function $c$.
- Output: $\mathrm{GED}(G_1, G_2) = \min \{ \sum_i c(o_i) : o_1, \ldots, o_t \text{ is an edit path from } G_1 \text{ to } G_2 \}$.

**Mapping form.** Every edit path of minimum cost corresponds to a partial injective map $\varphi$ from $V_1$ to $V_2$: mapped pairs are substituted, unmapped vertices of $G_1$ are deleted, unmapped vertices of $G_2$ are inserted, and edges follow their endpoints. So
$$\mathrm{GED}(G_1, G_2) = \min_{\varphi} \Big( \sum_{v \in \mathrm{dom}\,\varphi} c(v \to \varphi(v)) + \sum_{v \notin \mathrm{dom}\,\varphi} c(v \to \varepsilon) + \sum_{w \notin \mathrm{im}\,\varphi} c(\varepsilon \to w) + \text{edge costs induced by } \varphi \Big),$$
when the costs satisfy the triangle inequality, so that no detour through intermediate graphs is cheaper.

**Unit costs on unlabeled graphs.** Every insertion and deletion costs 1, substitutions are free. With the smaller graph padded by isolated dummy vertices to $n$ vertices,
$$\mathrm{GED}(G_1, G_2) = \big| |V_1| - |V_2| \big| + \min_{\pi} |\pi(E_1) \,\triangle\, E_2|,$$
over bijections $\pi$ of the padded vertex sets.

## Variants

- **Decision version.** Given $G_1$, $G_2$, $c$ and a bound $K$, is $\mathrm{GED}(G_1, G_2) \le K$? This is in NP and NP-complete.
- **Graph edit distance with only edge operations.** For graphs on the same vertex count, the unit-cost edge-only distance is the smallest number of edge flips that makes the graphs isomorphic.
- **Trees and strings.** On ordered trees the analogous [tree edit distance](/tree-edit-distance/) is polynomial ([Zhang-Shasha](/zhang-shasha-algorithm/)), and on strings it is the classical [edit distance](/edit-distance/). On unordered trees it is NP-hard.
- **Approximate and bounded versions.** Compute upper and lower bounds, or decide whether $\mathrm{GED} \le K$ for small $K$; similarity search in graph databases uses such filters.
- **Special cost functions.** Bunke (1997) showed that for a particular cost function the edit distance is a simple expression in $|V_1|$, $|V_2|$ and the size of a [maximum common subgraph](/maximum-common-subgraph/), so GED contains MCS.

## Examples

All examples use unit costs on unlabeled graphs, computed by a search over all bijections.

| $G_1$ | $G_2$ | GED | an optimal edit path |
|---|---|---|---|
| path $P_4$ | star $K_{1,3}$ | 2 | delete one end edge, insert an edge to the center |
| $C_6$ | $2K_3$ | 4 | delete 2 opposite edges, insert 2 edges to close two triangles |
| $K_3$ | $C_4$ | 4 | insert a vertex, delete one edge, insert two edges |
| $G$ | any relabeling of $G$ | 0 | none |

In the $C_6$ row, any bijection keeps at most 4 of the 6 cycle edges inside the two triangles, since the edges of $C_6$ that land in one triangle form a path of at most 2 edges. So at least 2 deletions and 2 insertions are needed.

## Known algorithms

| algorithm | output | time |
|---|---|---|
| search over all vertex maps | exact | $O(n! \cdot n^2)$ for equal sizes |
| A* and depth-first branch and bound over partial maps (Riesen and others) | exact | exponential; practical to about 10 to 20 vertices for A*, more with good bounds |
| mixed integer programming formulations | exact | exponential; practical on small labeled graphs |
| bipartite assignment (Riesen and Bunke 2009) | upper bound | $O(n^3)$ with the [Hungarian algorithm](/hungarian-algorithm/) |
| star and label-multiset bounds | lower bounds | polynomial |
| beam search, local search, neural predictors | upper bounds or estimates | polynomial per run |

The assignment method builds an $(n_1 + n_2) \times (n_1 + n_2)$ cost matrix: substituting $u$ by $v$ costs the vertex cost plus an optimal assignment of their incident edges, and the extra blocks hold deletion and insertion costs. An optimal assignment gives a vertex map, and the edit path it induces is an upper bound on GED.

## Bounds

- **NP-hard.** With costs that forbid substitution of different labels and charge 1 for every other operation, $\mathrm{GED}(H, G) = |V(G)| - |V(H)| + |E(G)| - |E(H)|$ exactly when $H$ is isomorphic to a subgraph of $G$, so deciding small edit distance decides [subgraph isomorphism](/subgraph-isomorphism/). The lower bound $|V(G)| - |V(H)| + |E(G)| - |E(H)|$ always holds, and it is reached only by an edit path made of insertions alone. Hence GED is NP-hard even for unlabeled graphs with unit costs.
- **Upper bound.** Exact computation in $O(n! \cdot n^2) = 2^{O(n \log n)}$ time by trying all vertex maps.
- **Graph isomorphism as the zero case.** With all costs positive, $\mathrm{GED} = 0$ exactly when $G_1 \cong G_2$, so deciding $\mathrm{GED} = 0$ is [graph isomorphism](/graph-isomorphism-problem/).
- **Metric.** If the cost function is a metric on the operations, GED is a metric on isomorphism classes.

## Reductions

- **From subgraph isomorphism**, as in the bounds above.
- **From maximum common subgraph** by Bunke's cost function.
- **To the quadratic assignment problem.** With the mapping form, GED is a quadratic assignment over the padded vertex sets: the vertex costs are linear in the assignment, and the edge costs depend on pairs of assignments.
- **Relaxation to linear assignment.** Dropping the pairwise edge terms, or folding local edge costs into vertex costs, gives the bipartite approximation.

## Applications

- Error-tolerant matching in pattern recognition: handwriting, fingerprints and shapes represented as attributed graphs.
- Similarity search for molecules in chemistry and for proteins in bioinformatics.
- Comparing business process models, program dependence graphs and software versions.
- Nearest-neighbor classification and clustering of graphs, and kernels built from edit distances.
- Measuring how much a network changes over time.

## References
