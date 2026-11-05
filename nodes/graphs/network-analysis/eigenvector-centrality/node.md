---
tag: RR3G64
kind: definition
slug: eigenvector-centrality
name: Eigenvector centrality
aliases:
- Bonacich centrality
area: graphs/network-analysis
level: core
summary: The centrality of a vertex is proportional to the sum of the centralities of its neighbours, the leading eigenvector of the adjacency matrix.
prereqs: [centrality, adjacency-matrix, eigenvector, perron-frobenius-theorem]
see_also: [katz-centrality, pagerank, hits-algorithm, power-iteration, degree-centrality, spectral-radius]
sources:
  - paper: doi:10.1080/0022250X.1972.9989806
    title: Phillip Bonacich, Factoring and weighting approaches to status scores and clique identification, Journal of Mathematical Sociology 2(1), 113 to 120 (1972)
    locator: the whole paper (status as the first eigenvector of the adjacency matrix)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the sections on eigenvector centrality and on Katz centrality, with the problems of directed and acyclic networks)
  - book: isbn:9780898714548
    title: Carl D. Meyer, Matrix Analysis and Applied Linear Algebra, SIAM, 2000
    locator: Chapter 8, Perron-Frobenius theory of nonnegative matrices (irreducible and primitive matrices)
---

Eigenvector centrality gives each [vertex](/vertex/) a score proportional to the sum of the scores of its neighbours, so a vertex is central when it is joined to other central vertices. The scores form the [eigenvector](/eigenvector/) of the [adjacency matrix](/adjacency-matrix/) for its largest [eigenvalue](/eigenvalue/), which the [Perron-Frobenius theorem](/perron-frobenius-theorem/) makes unique and positive on a connected graph. Bonacich proposed it as a status score in 1972. [Katz centrality](/katz-centrality/), [PageRank](/pagerank/) and [HITS](/hits-algorithm/) are variants that fix its problems on directed and disconnected graphs.

## Definition

Let $G = (V, E)$ be an undirected graph with $V = \{1, \ldots, n\}$ and adjacency matrix $A$, so $A_{ij} = 1$ if $\{i, j\} \in E$ and 0 otherwise. We want scores $x_i \ge 0$, not all 0, with

$$x_i = \frac{1}{\lambda} \sum_{j} A_{ij}\, x_j \quad \text{for all } i, \qquad \text{that is,} \qquad A x = \lambda x.$$

The **eigenvector centrality** is the solution with $\lambda = \lambda_1$, the largest eigenvalue of $A$, which equals the [spectral radius](/spectral-radius/) $\rho(A)$ since $A$ is nonnegative. The vector is fixed only up to a positive factor, so it is reported normalized, for example with $\max_i x_i = 1$, with $\sum_i x_i = 1$ or with $\|x\|_2 = 1$. The ranking does not depend on this choice.

**Why the largest eigenvalue.** Let $G$ be connected with $n \ge 2$. Then $A$ is irreducible, and the Perron-Frobenius theorem gives three facts: $\lambda_1 > 0$ is a simple eigenvalue, it has an eigenvector with all entries positive, and no other eigenvalue has a nonnegative eigenvector. So $\lambda_1$ is the only choice that gives scores $x \ge 0$, and with it the scores are unique up to the factor and all positive.

**Weighted graphs.** With weights $w_{ij} = w_{ji} \ge 0$, use $A_{ij} = w_{ij}$. A weight here is the strength of a tie: a larger weight passes more score.

**Directed graphs.** In a directed graph, the usual choice is that $i$ is central when central vertices point to it: $x_i = \frac{1}{\lambda} \sum_j A_{ji} x_j$, that is $A^\top x = \lambda x$. The Perron-Frobenius argument now needs the graph to be strongly connected. A vertex with no in-arc gets the score 0, and so does each vertex that only such vertices point to. On a [directed acyclic graph](/directed-acyclic-graph/), $A$ is nilpotent, $\lambda_1 = 0$, and the definition gives no useful scores. [Katz centrality](/katz-centrality/) and [PageRank](/pagerank/) add a constant to each score to fix this.

**Disconnected graphs.** If $G$ has several components, $A$ is block diagonal, and $\lambda_1$ is the largest of the leading eigenvalues of the components. Each vertex of a component with a smaller leading eigenvalue gets the score 0. If two components share the largest value, the eigenspace has dimension at least 2 and the scores are not unique. A common fix is to compute the scores of each component on its own, but then the scores of different components cannot be compared.

**Ties.** The scores of two vertices that a symmetry of the graph exchanges are equal, since the eigenvector is unique. In floating point, two equal scores can differ in the last digits, so a ranking should compare with a tolerance and then apply a fixed tie rule.

**Computation.** [Power iteration](/power-iteration/) starts with $x^{(0)} = (1, \ldots, 1)$ and repeats $x^{(t+1)} = A x^{(t)} / \|A x^{(t)}\|$. On a connected graph that is not [bipartite](/bipartite-graph/), it converges to the eigenvector, and the error falls like $(|\lambda_2| / \lambda_1)^t$, where $\lambda_2$ is the eigenvalue of second largest absolute value. On a bipartite graph, $-\lambda_1$ is also an eigenvalue and the iteration can oscillate between two vectors; iterating with $A + I$ in place of $A$ fixes this without changing the eigenvectors. Each step costs $O(n + m)$ time with adjacency lists.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, a dense group and a triangle joined by the edge $\{3, 4\}$. It has triangles, so it is not bipartite, and power iteration with $A$ converges. The table scales each iterate so that its largest entry is 1.

| step $t$ | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0.667 | 1 | 1 | 1 | 1 | 0.667 | 0.667 |
| 2 | 0.667 | 0.889 | 0.889 | 1 | 0.778 | 0.556 | 0.556 |
| 3 | 0.696 | 1 | 1 | 1 | 0.826 | 0.522 | 0.522 |
| 10 | 0.738 | 1 | 1 | 0.982 | 0.651 | 0.389 | 0.389 |
| 30 | 0.738 | 1 | 1 | 0.971 | 0.631 | 0.369 | 0.369 |

Step 1 is the degree, divided by 3. The limit has $\lambda_1 \approx 2.7093$, the largest root of the characteristic polynomial $t^7 - 9t^5 - 6t^4 + 19t^3 + 24t^2 + 5t - 2$. Vertices 3 and 4 both have degree 3, but $x_4 \approx 0.631$ is much less than $x_3 \approx 0.971$, because the neighbours 5 and 6 of vertex 4 are weak.

**A star.** In $K_{1,k}$ with centre $c$, the vector with $x_c = \sqrt{k}$ and $x_\ell = 1$ for each leaf $\ell$ satisfies $A x = \sqrt{k}\, x$: a leaf sees $x_c = \sqrt{k} \cdot 1$, and the centre sees $k \cdot 1 = \sqrt{k} \cdot \sqrt{k}$. So $\lambda_1 = \sqrt{k}$. The star is bipartite, so plain power iteration from the all-ones vector swaps between two vectors and does not converge.

**A disconnected graph.** For a triangle plus a separate edge, the triangle has leading eigenvalue 2 and the edge has 1. So $\lambda_1 = 2$, the scores are $1, 1, 1$ on the triangle and $0, 0$ on the edge, although the vertices of the edge have degree 1.

**Non-examples.**

- The degree is not the eigenvector centrality, but it is the first step of power iteration from the all-ones vector. The two agree for a [regular graph](/regular-graph/), where the all-ones vector is the eigenvector.
- On the directed path $a \to b \to c$, the matrix is nilpotent and $\lambda_1 = 0$. There is no positive eigenvector, so eigenvector centrality is not defined in a useful way here.
- The eigenvector of the second largest eigenvalue is not a centrality: it has positive and negative entries. Its signs are used to split a graph in two, see [spectral clustering](/spectral-clustering/).

## Related definitions

- [Katz centrality](/katz-centrality/): $x = \alpha A x + \beta \mathbf{1}$, which works on any directed graph when $\alpha < 1/\lambda_1$.
- [PageRank](/pagerank/): the stationary distribution of a random walk with jumps.
- [HITS](/hits-algorithm/): hub and authority scores, the leading eigenvectors of $A A^\top$ and $A^\top A$.
- [Power iteration](/power-iteration/): the standard way to compute the scores.
- [Perron-Frobenius theorem](/perron-frobenius-theorem/): the reason why the scores are positive and unique.

## References
