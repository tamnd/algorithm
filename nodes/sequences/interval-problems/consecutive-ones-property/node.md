---
tag: GP54BB
kind: definition
slug: consecutive-ones-property
name: Consecutive ones property
aliases:
- C1P
area: sequences/interval-problems
level: advanced
summary: A 0-1 matrix has it when the ones in each row are contiguous after some column permutation.
prereqs: [helly-property-intervals, total-order]
see_also: [pq-tree, total-unimodularity, hypergraph, lexicographic-bfs, chordal-graph, maximal-clique, interval-coloring-depth-theorem, k-machine-interval-scheduling]
sources:
  - paper: doi:10.1016/S0022-0000(76)80045-1
    title: "Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3) (1976), pages 335 to 379"
    locator: the PQ-tree, the linear time test for the consecutive ones property, and its use for interval graph recognition
  - paper: "Delbert R. Fulkerson and Oliver A. Gross, Incidence matrices and interval graphs, Pacific Journal of Mathematics 15(3) (1965), pages 835 to 855"
    locator: the characterization of interval graphs by the consecutive ones property of the clique matrix
  - paper: "Alan Tucker, A structure theorem for the consecutive 1's property, Journal of Combinatorial Theory, Series B 12 (1972), pages 153 to 162"
    locator: the characterization of the property by forbidden submatrices
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (the clique matrix and the Fulkerson and Gross theorem)
---

A 0-1 matrix has the consecutive ones property when its columns can be ordered so that in every row the ones form one contiguous block. In the language of sets, a family of subsets of a ground set has it when the elements can be placed on a line so that every set is an interval of that line. Fulkerson and Gross showed that a graph is an interval graph exactly when its clique matrix has the property, and Booth and Lueker test it in linear time with a [PQ-tree](/pq-tree/), which also describes all valid orders.

## Definition

Let $M$ be an $m \times n$ matrix with entries in $\{0, 1\}$, with rows $R_1, \ldots, R_m$ and columns $1, \ldots, n$. Identify row $R_i$ with the set $S_i = \{\, c : M_{ic} = 1 \,\}$ of its columns.

**Consecutive ones for rows.** $M$ has the *consecutive ones property* (for rows) if there is a permutation $\pi$ of the columns such that, in the matrix with columns in the order $\pi(1), \ldots, \pi(n)$, every row has the form $0 \cdots 0 \, 1 \cdots 1 \, 0 \cdots 0$, where any of the three blocks may be empty. Such a $\pi$ is a *consecutive ones order*. Equivalently, for each $i$, the positions $\{\, \pi^{-1}(c) : c \in S_i \,\}$ form a set of consecutive integers. If $\pi$ is the identity, $M$ is in *consecutive ones form*; such a matrix is also called an *interval matrix*.

**As a set system.** A family $\mathcal{S} = \{S_1, \ldots, S_m\}$ of subsets of a finite set $U$ has the property if there is a [total order](/total-order/) of $U$ in which every $S_i$ is an interval, a set of the form $\{\, u : x \le u \le y \,\}$. This is the same definition with $U$ the columns.

**For columns.** $M$ has the consecutive ones property *for columns* if its transpose has it for rows: the rows can be ordered so that the ones in each column are contiguous.

**Checking an order.** Given $\pi$, the property is checked in $O(m + n + f)$ time, where $f$ is the number of ones: for each row, the positions of its ones are consecutive if and only if their maximum minus their minimum equals their number minus one.

**The test.** Deciding whether some order exists is the hard part, since there are $n!$ orders. Booth and Lueker decide it, and produce an order, in $O(m + n + f)$ time with the [PQ-tree](/pq-tree/), which represents the set of all consecutive ones orders at once.

## Examples and non-examples

**A matrix with the property.** Take the rows $S_1 = \{1, 3\}$, $S_2 = \{2, 3, 4\}$, $S_3 = \{4, 5\}$, $S_4 = \{2, 4\}$ over the columns $1, \ldots, 5$:

| row | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $S_1$ | 1 | 0 | 1 | 0 | 0 |
| $S_2$ | 0 | 1 | 1 | 1 | 0 |
| $S_3$ | 0 | 0 | 0 | 1 | 1 |
| $S_4$ | 0 | 1 | 0 | 1 | 0 |

In the given order, $S_1$ and $S_4$ have a gap. In the order $1, 3, 2, 4, 5$:

| row | 1 | 3 | 2 | 4 | 5 |
|---|---|---|---|---|---|
| $S_1$ | 1 | 1 | 0 | 0 | 0 |
| $S_2$ | 0 | 1 | 1 | 1 | 0 |
| $S_3$ | 0 | 0 | 0 | 1 | 1 |
| $S_4$ | 0 | 0 | 1 | 1 | 0 |

every row is one block. A search over all $5! = 120$ orders shows that this order and its reverse $5, 4, 2, 3, 1$ are the only consecutive ones orders. The reason: $S_3$ and $S_4$ force 4 between 2 and 5, $S_2$ and $S_4$ then force 3 to the other side of 2, and $S_1$ forces 1 next to 3.

**Interval families.** If $I_1, \ldots, I_n$ are intervals of the line and $x_1 < \cdots < x_m$ are points, the matrix with $M_{ij} = 1$ when $x_i \in I_j$ has the property for columns in the given order of points: the points in an interval are consecutive. This holds for every type of interval, closed, half-open or open, since each is a convex set.

**The clique matrix of an interval graph.** Let $G$ be the interval graph of a family of closed intervals. The rows of its clique matrix are the [maximal cliques](/maximal-clique/) and the columns are the vertices. By the [Helly property](/helly-property-intervals/), each maximal clique is the set of intervals that contain some point, and sorting the cliques by that point puts the cliques that contain any one vertex in a contiguous run. So the clique matrix has the property for columns in that order. Fulkerson and Gross proved the converse: a graph whose clique matrix has the consecutive ones property for columns is an interval graph, with the interval of a vertex given by its run of cliques.

**Non-example: a triangle of pairs.** The sets $\{a, b\}, \{b, c\}, \{a, c\}$ over $\{a, b, c\}$ do not have the property. In any order $x, y, z$, the set $\{x, z\}$ is not an interval, and $\{x, z\}$ is one of the three sets.

**Non-example: a star of pairs.** The sets $\{a, b\}, \{a, c\}, \{a, d\}$ do not have it. A two-element set is an interval only when its elements are neighbours in the order, and $a$ has at most two neighbours on a line, but it would need three.

**Non-example: a cycle.** The clique matrix of a cycle of length 4, with maximal cliques the four edges, does not have the property for columns. Each vertex lies in two edges, which must be neighbours in the order of edges, so the four edges would form a cycle of neighbours, but a line has two ends. This matches the fact that a 4-cycle is not an interval graph, since it is not [chordal](/chordal-graph/).

**Edge cases.** A matrix with one row, or with rows that are all empty or all singletons, has the property for any order. A matrix with two rows has it, since any two sets can be placed as overlapping or disjoint blocks: list $S_1 \setminus S_2$, then $S_1 \cap S_2$, then $S_2 \setminus S_1$, then the rest.

## Related definitions

- **Circular ones property.** The ones of each row are contiguous on a circle, allowing a block that wraps from the last column to the first. Every matrix with the consecutive ones property has the circular one, but not conversely: the triangle of pairs above has it in the circular order $a, b, c$. It is the analogue of the property for arcs of a circle in place of intervals of a line.
- **Interval hypergraph.** A [hypergraph](/hypergraph/) whose edges are intervals of some order of its vertices, that is, whose incidence matrix has the property.
- **Tucker matrices.** Tucker characterized the property by a finite list of forbidden families of submatrices: a matrix has it if and only if no submatrix, after permuting rows and columns, is one of the Tucker matrices.
- **Total unimodularity.** A matrix in consecutive ones form is [totally unimodular](/total-unimodularity/). Every square submatrix keeps the form, since deleting rows and columns keeps each block of ones contiguous. Subtracting each column from the next one, from right to left, changes no determinant and turns each row into one with at most one $+1$ and one $-1$, the transpose of a submatrix of the incidence matrix of a directed graph, whose square submatrices have determinant $0$ or $\pm 1$. So linear programs over interval matrices, such as [k-machine interval scheduling](/k-machine-interval-scheduling/), have integral optima.
- **PQ-tree.** The [PQ-tree](/pq-tree/) of a family stores every consecutive ones order: P-nodes allow any order of their children and Q-nodes allow only the given order or its reverse.
- **Interval graph recognition.** Every interval graph is [chordal](/chordal-graph/), and a chordal graph has at most $n$ maximal cliques, which can be listed in linear time. Booth and Lueker list them and test the clique matrix for the property, which by Fulkerson and Gross recognizes interval graphs in linear time. Later methods use [lexicographic BFS](/lexicographic-bfs/) in place of the PQ-tree.

## References
