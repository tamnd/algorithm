---
tag: QTKKXV
kind: data-structure
slug: laplacian-matrix
name: Laplacian matrix
aliases:
- graph Laplacian
- Kirchhoff matrix
area: graphs/graph-representation
level: advanced
summary: Degree matrix minus adjacency matrix; its spectrum encodes connectivity and structure.
implements: [graph]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [graph, adjacency-matrix, incidence-matrix, eigenvalue]
see_also: [incidence-matrix, adjacency-matrix, matrix-tree-theorem, spectral-clustering, cheeger-inequality, connected-components, conjugate-gradient-method, lanczos-algorithm]
sources:
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Graduate Texts in Mathematics 207, Springer, 2001
    locator: Chapter 13, the Laplacian of a graph, its quadratic form, the matrix-tree theorem and the algebraic connectivity
  - paper: doi:10.1145/1007352.1007372
    title: Daniel A. Spielman and Shang-Hua Teng, Nearly-linear time algorithms for graph partitioning, graph sparsification, and solving linear systems, STOC 2004
    locator: pages 81 to 90, the solver for symmetric diagonally dominant systems, which include Laplacian systems, in nearly linear time
---

The Laplacian matrix of an undirected [graph](/graph/) with $n$ vertices is the $n \times n$ matrix $L = D - A$, where $D$ is the diagonal matrix of the [degrees](/degree/) and $A$ is the [adjacency matrix](/adjacency-matrix/). With edge weights, $L = D - W$, where $W$ holds the weights and $D$ the weighted degrees. It is symmetric, each row sums to zero, and its quadratic form is $x^T L x = \sum_{\{u,v\} \in E} w(u,v) (x_u - x_v)^2$. So it is positive semidefinite, the number of zero eigenvalues is the number of [connected components](/connected-components/), and any cofactor counts the spanning trees (the [matrix-tree theorem](/matrix-tree-theorem/)). As a data structure it is stored sparse, with $\Theta(n + m)$ space, and its main operation is the product $Lx$.

## In plain words

Think of each vertex as a town with a temperature, and each edge as a pipe that carries heat between two towns. The Laplacian says how far each town is from the average of its neighbours: for town $u$ it is its own temperature times its number of pipes, minus the temperatures at the other ends. If all towns are equally warm, nothing flows and the answer is zero everywhere. The total tension of a setting is the sum, over the pipes, of the squared difference at the two ends. A setting with low tension changes slowly along the edges, so the settings of lowest tension show how the graph splits into loosely joined parts.

## The abstract type

The Laplacian stores an undirected, possibly weighted [multigraph](/multigraph/) on the vertices $0, \ldots, n - 1$, with positive weights and no [self-loops](/self-loop/). It supports `add-edge(L, u, v, w)`, `entry(L, u, v)`, `multiply(L, x) → Lx` and `quadratic-form(L, x) → x^T L x`. Linear algebra on top of these gives the rank, the spectrum and the cofactors.

## Representation

Two arrays: `deg[u]`, the weighted degree $D_{uu}$, and `adj[u]`, a list with one pair $(v, w)$ for each edge $\{u, v\}$ of weight $w$. This is a weighted [adjacency list](/adjacency-list/) with the diagonal kept apart; in [compressed sparse row](/compressed-sparse-row/) form it is what numerical solvers use.

**Invariant.** `deg[u]` is the sum of the weights of the edges at $u$, and `adj[u]` holds exactly one pair for each edge at $u$. Then the matrix is $L_{uu} = $ `deg[u]` and, for $u \ne v$, $L_{uv} = -\sum \{ w : (v, w) \in \texttt{adj}[u] \}$. Parallel edges add their weights. A self-loop would add $w$ to $D_{uu}$ and $w$ to $A_{uu}$, so it would not change $L$; the structure rejects it.

## Operations

```pseudo id=main
ADD-EDGE(L, u, v, w)                     ▷ u ≠ v, w > 0
L1  deg[u] ← deg[u] + w; deg[v] ← deg[v] + w
L2  append (v, w) to adj[u]
L3  append (u, w) to adj[v]

MULTIPLY(L, x)                           ▷ returns y = Lx
L4  for u ← 0 to n − 1 do
L5      y[u] ← deg[u] · x[u]
L6      for each (v, w) in adj[u] do
L7          y[u] ← y[u] − w · x[v]
L8  return y

QUADRATIC-FORM(L, x)                     ▷ returns x^T L x
L9  s ← 0
L10 for u ← 0 to n − 1 do
L11     for each (v, w) in adj[u] with u < v do
L12         s ← s + w · (x[u] − x[v])²
L13 return s
```

**Add.** Lines L1 to L3 update the two degrees and both lists, in $O(1)$ amortized time.

**Multiply.** Line L5 is the diagonal term and lines L6 and L7 subtract the weighted values of the neighbours. Each pair of each list is read once, so the time is $\Theta(n + m)$. This product is all that iterative methods such as the [conjugate gradient method](/conjugate-gradient-method/) and the [Lanczos algorithm](/lanczos-algorithm/) need.

**Quadratic form.** Each edge appears in two lists; the test $u < v$ of line L11 counts it once. The time is $\Theta(n + m)$.

**Entry.** $L_{uu}$ is `deg[u]` in $O(1)$; $L_{uv}$ scans `adj[u]` in $O(1 + d(u))$.

## Example

Take the vertices $0, 1, 2, 3$ and the edges $\{0,1\}, \{0,2\}, \{1,2\}, \{2,3\}$, all of weight 1: a triangle with a pendant vertex. After the four ADD-EDGE calls, `deg` is $(2, 2, 3, 1)$ and

$$L = \begin{pmatrix} 2 & -1 & -1 & 0 \\ -1 & 2 & -1 & 0 \\ -1 & -1 & 3 & -1 \\ 0 & 0 & -1 & 1 \end{pmatrix}.$$

| call | result |
|---|---|
| MULTIPLY$(L, (1,1,1,1))$ | $(0, 0, 0, 0)$ |
| MULTIPLY$(L, (1,0,0,0))$ | $(2, -1, -1, 0)$, the first column |
| QUADRATIC-FORM$(L, (1,1,0,0))$ | 2, the edges $\{0,2\}$ and $\{1,2\}$ |
| QUADRATIC-FORM$(L, (0,0,0,1))$ | 1, the edge $\{2,3\}$ |

The eigenvalues are $0, 1, 3, 4$. The eigenvalue 0 is simple, so the graph is connected. The eigenvector $(1, -1, 0, 0)$ has eigenvalue 3, and $(1, 1, 0, -2)$ has eigenvalue 1, the algebraic connectivity: its signs put vertex 3 apart from the triangle. Deleting row and column 0 leaves a matrix of determinant 3, the number of spanning trees, and $1 \cdot 3 \cdot 4 / n = 3$ as well.

## Correctness

ADD-EDGE keeps the invariant: line L1 adds $w$ to the degrees of both ends, and lines L2 and L3 add one pair to each end. MULTIPLY then computes $y_u = D_{uu} x_u - \sum_{v} W_{uv} x_v = (Lx)_u$. QUADRATIC-FORM computes $\sum_{\{u,v\} \in E} w (x_u - x_v)^2$, and expanding the square shows that this is $x^T L x$. From the identity:

- **Positive semidefinite.** $x^T L x \ge 0$ for each real $x$, so all eigenvalues are $\ge 0$.
- **Kernel.** $Lx = 0$ if and only if $x^T L x = 0$, if and only if $x_u = x_v$ for each edge, if and only if $x$ is constant on each component. So the multiplicity of the eigenvalue 0 is the number $c$ of components, and $\operatorname{rank} L = n - c$.
- **Factorization.** $L = B B^T$ for the signed [incidence matrix](/incidence-matrix/) $B$ of any orientation, with the column of $e$ scaled by $\sqrt{w(e)}$.

The full proof is in `proofs/correctness.md`. The cofactor formula is proved on the page of the [matrix-tree theorem](/matrix-tree-theorem/).

## Complexity

The model is the [word RAM](/word-ram/), with real arithmetic counted as one step.

| operation | time | dense $n \times n$ matrix |
|---|---|---|
| add-edge | $O(1)$ amortized | $O(1)$ |
| entry$(u, u)$ | $O(1)$ | $O(1)$ |
| entry$(u, v)$ | $O(1 + d(u))$ | $O(1)$ |
| multiply, quadratic form | $\Theta(n + m)$ | $\Theta(n^2)$ |
| rank, determinant (exact elimination) | $O(n^3)$ arithmetic steps | $O(n^3)$ |
| space | $\Theta(n + m)$ | $\Theta(n^2)$ |

Solving $Lx = b$ by Gaussian elimination takes $O(n^3)$ steps. Spielman and Teng gave a solver for Laplacian and symmetric diagonally dominant systems that runs in $m \log^{O(1)} n \log(1/\varepsilon)$ time for relative error $\varepsilon$.

## Variants

- **Normalized Laplacian** $\mathcal{L} = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}$, for graphs with no isolated vertex. Its eigenvalues lie in $[0, 2]$, and 2 is one of them exactly when some component is bipartite. It is the form used by the [Cheeger inequality](/cheeger-inequality/) and in [spectral clustering](/spectral-clustering/).
- **Random-walk Laplacian** $I - D^{-1} A$, which has the same eigenvalues as $\mathcal{L}$ and relates to the random walk with transition matrix $D^{-1}A$.
- **Signless Laplacian** $D + A = B B^T$ for the unsigned incidence matrix $B$.
- **Directed Laplacians** $D_{\text{out}} - A$, which are not symmetric; the matrix-tree theorem for directed graphs counts spanning arborescences with them.

## When to use it

Use the Laplacian when a question is about smoothness or cuts on a graph: counting spanning trees, testing connectivity by linear algebra, spectral partitioning and clustering, graph drawing by eigenvectors, electrical networks (the effective resistance between $u$ and $v$ is $(e_u - e_v)^T L^{+} (e_u - e_v)$ for the pseudoinverse $L^+$), and diffusion. Store it sparse and use only `multiply` with iterative solvers on large graphs. For plain traversals, the [adjacency list](/adjacency-list/) is enough and simpler.

## Pitfalls

- **Self-loops.** They cancel in $D - A$. If the input has them, decide whether to drop them or to use the signless or normalized forms, where they do count; do not let them change `deg` alone.
- **Singularity.** $L$ is never invertible: $L \mathbf{1} = 0$. Solve $Lx = b$ only when $b$ sums to zero on each component, fix one vertex per component, or use the pseudoinverse.
- **Floating-point rank.** Counting components by the number of eigenvalues near 0 needs a tolerance and fails for nearly disconnected graphs. Use exact arithmetic, as the implementation does, or a traversal.
- **Isolated vertices in the normalized form.** $D^{-1/2}$ is undefined at degree 0. Set the row to zero or remove the vertex first.

## Implementations

The Python class stores `deg` and `adj` as above and gives `add_edge`, `multiply`, `quadratic_form`, `entry` and `dense`. The helpers `components` and `spanning_tree_count` use exact Gaussian elimination over the rationals for $n - \operatorname{rank} L$ and the matrix-tree cofactor.

## History

Kirchhoff introduced the matrix in 1847 in his study of electrical networks, where he showed that the cofactors count the spanning trees; this is why it is also called the Kirchhoff matrix. Fiedler named the second smallest eigenvalue the algebraic connectivity in 1973 and showed that it is positive exactly when the graph is connected. Spectral partitioning with the corresponding eigenvector followed in the 1980s and 1990s, and Spielman and Teng's nearly linear time solver of 2004 made the Laplacian a basic tool of fast graph algorithms.

## References
