---
tag: NGK7EM
kind: concept
slug: equitable-partition
name: Equitable partition
aliases:
- stable partition
- equitable coloring of vertices
area: graphs/graph-isomorphism
level: core
summary: A vertex partition where each vertex has the same number of neighbors in every cell as all other vertices of its own cell.
prereqs: [equivalence-relation, degree, adjacency-matrix]
see_also: [weisfeiler-leman, partition-refinement, automorphism-orbit, individualization-refinement, regular-graph, eigenvalue, graph-automorphism-group]
sources:
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer, Graduate Texts in Mathematics 207, 2001
    locator: Chapter 9, Interlacing (the sections on equitable partitions and quotient matrices)
  - paper: "Brendan D. McKay, Practical graph isomorphism, Congressus Numerantium 30, 45 to 87 (1981)"
    locator: Section 2 (equitable partitions and the refinement procedure)
  - book: isbn:9781107014527
    title: Martin Grohe, Descriptive Complexity, Canonisation, and Definable Graph Structure Theory, Cambridge University Press, 2017
    locator: Chapter 3 (stable colorings computed by color refinement)
---

An equitable partition of a graph is a partition of its vertices into cells such that, for any two cells $X$ and $Y$, every vertex of $X$ has the same number of neighbors in $Y$. The stable colorings that [color refinement](/weisfeiler-leman/) computes are exactly the coarsest equitable partitions, and the orbits of any group of [automorphisms](/graph-automorphism-group/) form an equitable partition. Equitable partitions give a small quotient matrix whose eigenvalues are eigenvalues of the graph, and they are the nodes of the search trees in [nauty](/nauty/) and related tools.

## In plain words

Sort the points of a network into groups. The grouping is fair, or equitable, when every point of a group sees the other groups in the same way: each point of one group has the same number of links into each group, including its own. Then you can describe the whole network roughly by one small table: for each pair of groups, how many links a point of the first group has into the second. Points that a symmetry can swap always end up in the same group of the coarsest fair grouping. The reverse need not hold: points in the same group need not be swappable.

## The idea

Let $G = (V, E)$ be a simple undirected graph and $\pi = (V_1, \ldots, V_r)$ a partition of $V$ into non-empty cells. Write $\deg_Y(v) = |N(v) \cap Y|$ for the number of neighbors of $v$ in a set $Y$.

**Definition.** $\pi$ is **equitable** when for all $i, j$ there is a number $b_{ij}$ with $\deg_{V_j}(v) = b_{ij}$ for every $v \in V_i$.

The $r \times r$ matrix $B = (b_{ij})$ is the **quotient matrix**. Let $P$ be the $n \times r$ characteristic matrix, with $P_{vi} = 1$ when $v \in V_i$. Then $\pi$ is equitable exactly when
$$A P = P B,$$
where $A$ is the [adjacency matrix](/adjacency-matrix/). Three consequences follow.

- **Eigenvalues.** If $B x = \lambda x$ with $x \ne 0$, then $A (P x) = \lambda (P x)$ and $P x \ne 0$, so every eigenvalue of $B$ is an [eigenvalue](/eigenvalue/) of $A$.
- **Coarsest refinement.** Among the equitable partitions that refine a given partition $\pi_0$, there is a unique coarsest one. It is the stable partition of color refinement started from $\pi_0$, and any order of splitting cells reaches it (see [partition refinement](/partition-refinement/)).
- **Orbits.** If $\Gamma \le \mathrm{Aut}(G)$, the [orbits](/automorphism-orbit/) of $\Gamma$ form an equitable partition: an automorphism mapping $u$ to $v$ maps the neighbors of $u$ in an orbit $Y$ bijectively onto the neighbors of $v$ in $Y$. So the orbit partition of $\mathrm{Aut}(G)$ refines the coarsest equitable partition.

The same notions apply to directed graphs, where each vertex must have the same numbers of out-neighbors and of in-neighbors in each cell, and to vertex-colored graphs, where the partition must refine the colors. Edge labels split $b_{ij}$ by label.

## Examples

**The trivial partition.** The partition with one cell $\{V\}$ is equitable exactly when $G$ is [regular](/regular-graph/); then $B = (d)$ and $d$ is the degree. The discrete partition, with every vertex in its own cell, is always equitable.

**The path on 4 vertices.** For $0 - 1 - 2 - 3$, the partition $\{0, 3\}, \{1, 2\}$ is equitable with
$$B = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}.$$
The eigenvalues of $B$ are $(1 \pm \sqrt 5)/2 \approx 1.618$ and $-0.618$, and the eigenvalues of the path are $\pm 1.618$ and $\pm 0.618$. The partition $\{0, 1\}, \{2, 3\}$ is not equitable: $\deg_{\{2,3\}}(1) = 1$ but $\deg_{\{2,3\}}(0) = 0$.

**The star $K_{1,3}$.** The partition into the center and the leaves is equitable with $B = \begin{pmatrix} 0 & 3 \\ 1 & 0 \end{pmatrix}$, whose eigenvalues $\pm \sqrt 3 \approx \pm 1.732$ are the largest and smallest eigenvalues of the star.

**Equitable but not an orbit partition.** The Frucht graph is 3-regular with 12 vertices, so $\{V\}$ is equitable. Its automorphism group is trivial, so its orbits are the 12 singletons. Color refinement stops at once with one cell and learns nothing about this graph.

**Two graphs with the same quotient.** The 6-cycle and two disjoint triangles both have the equitable partition $\{V\}$ with $B = (2)$. Graphs with a common equitable partition and quotient matrix are the pairs that color refinement cannot separate.

## Where it is used

- **[Color refinement](/weisfeiler-leman/)** computes the coarsest equitable partition that refines a given coloring, and decides non-isomorphism by comparing cell sizes and quotient matrices.
- **[Individualization-refinement](/individualization-refinement/)** in [nauty](/nauty/), Traces and [bliss](/bliss/): each node of the search tree is an equitable partition, obtained by fixing a vertex and refining again.
- **Spectral graph theory**: quotient matrices give eigenvalues and interlacing bounds, for example on independence numbers; the largest eigenvalue of a graph equals that of the quotient of any equitable partition when the graph is connected.
- **Symmetry reduction** in integer programming and SAT: the coarsest equitable partition is a cheap over-approximation of the orbit partition, used to find candidate symmetries (see [orbital branching](/orbital-branching/)).
- **Lumping of Markov chains and bisimulation**: a partition of states with equal transition counts into each block is the same idea for weighted directed graphs.
- **Fractional isomorphism**: two graphs have a common coarsest equitable partition with the same quotient exactly when they are fractionally isomorphic.

## References
