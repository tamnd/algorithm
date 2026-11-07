---
tag: 0XWH5Q
kind: problem
slug: bandwidth-reduction
name: Bandwidth reduction
aliases:
- matrix bandwidth minimization
- graph bandwidth problem
- bandwidth minimization
area: numerical/linear-systems
level: advanced
summary: Permute rows and columns of a sparse symmetric matrix to shrink its bandwidth.
prereqs: [sparse-matrix, banded-matrix, breadth-first-search]
see_also: [cuthill-mckee, reverse-cuthill-mckee, fill-reducing-ordering, banded-matrix, fill-in, parameterized-bandwidth, graph-partitioning-problem, sparse-linear-systems]
sources:
  - paper: doi:10.1007/BF02280884
    title: Christos H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16(3), 1976
    locator: pp. 263 to 270
  - paper: doi:10.1137/0134037
    title: M. R. Garey, R. L. Graham, D. S. Johnson and D. E. Knuth, Complexity results for bandwidth minimization, SIAM Journal on Applied Mathematics 34(3), 1978
    locator: pp. 477 to 495 (NP-completeness for trees of maximum degree 3)
  - paper: doi:10.1137/0601042
    title: James B. Saxe, Dynamic-programming algorithms for recognizing small-bandwidth graphs in polynomial time, SIAM Journal on Algebraic and Discrete Methods 1(4), 1980
    locator: pp. 363 to 369 (an O(n^(k+1)) test for bandwidth at most k)
  - paper: doi:10.1145/800195.805928
    title: E. Cuthill and J. McKee, Reducing the bandwidth of sparse symmetric matrices, Proceedings of the 24th ACM National Conference, 1969
    locator: pp. 157 to 172
  - paper: doi:10.1137/0713023
    title: Norman E. Gibbs, William G. Poole and Paul K. Stockmeyer, An algorithm for reducing the bandwidth and profile of a sparse matrix, SIAM Journal on Numerical Analysis 13(2), 1976
    locator: pp. 236 to 250 (pseudo-peripheral endpoints and combined level structures)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (the section on bandwidth and profile reduction)
  - paper: doi:10.1137/0713020
    title: Wai-Hung Liu and Andrew H. Sherman, Comparative analysis of the Cuthill-McKee and the reverse Cuthill-McKee ordering algorithms for sparse matrices, SIAM Journal on Numerical Analysis 13(2), 1976
    locator: pp. 198 to 213 (reversal never increases the profile)
---

## In plain words

A sparse matrix is cheap to factor if all its nonzeros sit close to the diagonal, in a thin band. Renumbering the unknowns moves the nonzeros around without changing the problem. The bandwidth reduction problem asks for the numbering that makes the band as thin as possible. Think of the unknowns as people at a long table, with a line between any two who must talk: you want to seat them so that nobody has to talk to someone far down the table. Finding the very best seating is hard in general, but simple breadth first numberings do well in practice.

## Definition

**Notation.** $A \in \mathbb{R}^{n \times n}$ is symmetric in pattern ($a_{ij} \ne 0 \iff a_{ji} \ne 0$), and $G = G(A) = (V, E)$ is its graph, with $V = \{1, \ldots, n\}$ and an edge $\{i, j\}$ for each $a_{ij} \ne 0$, $i \ne j$. A numbering is a bijection $f: V \to \{1, \ldots, n\}$, equivalently a permutation matrix $P$ with $(P A P^T)_{f(i) f(j)} = a_{ij}$.

The **bandwidth** of $A$ is $\beta(A) = \max\{|i - j| : a_{ij} \ne 0\}$, and of a numbering $f$ of $G$ it is $\beta_f(G) = \max_{\{i,j\} \in E} |f(i) - f(j)|$.

**Input:** the pattern of $A$, given as $G$ with $m = |E|$ edges.
**Output:** a numbering $f$ minimizing $\beta_f(G)$. The minimum is the bandwidth of the graph, $\beta(G)$.

**Decision version:** given $G$ and $k$, is $\beta(G) \le k$?

## Variants

- **Profile (envelope) minimization.** With $f_i = \min\{j : a_{ij} \ne 0\}$ for row $i$ of $P A P^T$, minimize the profile $\sum_i (i - f_i)$. Envelope (skyline) solvers store exactly the entries between $f_i$ and $i$, and fill stays inside the envelope, so the profile is the storage of the factor. A small profile can coexist with a large bandwidth.
- **Unsymmetric bandwidth.** Minimize the lower and upper bandwidths of $P A Q$ with independent row and column permutations, or of $P A P^T$ for an unsymmetric pattern.
- **Fixed parameter version.** Decide $\beta(G) \le k$ for fixed $k$; see [parameterized bandwidth](/parameterized-bandwidth/).
- **Cyclic bandwidth and minimum linear arrangement.** Replace $|f(i) - f(j)|$ by its cyclic version, or the maximum by the sum $\sum_{E} |f(i) - f(j)|$.
- **Wavefront minimization.** Minimize the largest number of active rows at any step of a frontal method.

## Examples

**A path with a bad numbering.** For the path $v_1 - v_2 - v_3 - v_4 - v_5$ numbered $f = (1, 3, 5, 2, 4)$ along the path, the edges have label differences $2, 2, 3, 2$, so $\beta_f = 3$. Numbering in path order gives $\beta = 1$: a tridiagonal matrix.

**A star.** For $K_{1, n-1}$ (an arrow matrix), the centre has $n - 1$ neighbours, which need $n - 1$ distinct labels within distance $\beta$ of the centre's label, so $\beta \ge \lceil (n - 1)/2 \rceil$; placing the centre in the middle attains it.

**The grid.** For the 5-point grid graph on $k \times k$ points, row by row numbering gives $\beta = k$, and $k$ is optimal (Chvátalová 1975). Cuthill-McKee started at a corner numbers the grid by anti-diagonals, with bandwidth $k$ as well but a smaller profile.

**Two lower bounds (proved).** For any numbering, a vertex of degree $\Delta$ has $\Delta$ neighbours with distinct labels in an interval of length $2\beta$ around its own, so $\beta(G) \ge \lceil \Delta/2 \rceil$. The vertices labelled $1$ and $n$ in a connected graph are joined by a path of at most $D$ edges, $D$ the diameter, and each edge changes the label by at most $\beta$, so $\beta(G) \ge \lceil (n - 1)/D \rceil$.

## Known algorithms

| method | time | guarantee |
|---|---|---|
| [Cuthill-McKee](/cuthill-mckee/) (1969) | $O(m \log \Delta)$ after the start vertex | heuristic; $\beta_f \le 2 w - 1$ for level structure width $w$ |
| [Reverse Cuthill-McKee](/reverse-cuthill-mckee/) (George 1971) | same | same bandwidth as CM; profile never larger (Liu and Sherman 1976) |
| Gibbs-Poole-Stockmeyer (1976) | $O(m)$ per BFS, a few BFS passes | heuristic; often a smaller bandwidth than RCM with a faster start vertex search |
| Spectral ordering | an eigenvector of the graph Laplacian | heuristic; sort by the Fiedler vector; good for profile (Barnard, Pothen and Simon 1995) |
| Sloan (1986) | $O(m \log n)$ | heuristic for the profile and wavefront |
| Saxe (1980) dynamic programming | $O(n^{k+1})$ | exact test of $\beta(G) \le k$ |
| Exact branch and bound | exponential | exact for small $n$ |

All the heuristics start a [breadth-first search](/breadth-first-search/) from a pseudo-peripheral vertex, one of nearly maximal eccentricity, because the BFS levels then form many narrow layers and edges join only adjacent layers.

## Bounds

- **NP-hardness (proved).** The decision version is NP-complete (Papadimitriou 1976), even for trees of maximum degree $3$ (Garey, Graham, Johnson and Knuth 1978).
- **Polynomial for fixed $k$ (proved).** Saxe (1980): $O(n^{k+1})$ time. It is W[t]-hard for every $t$ when parameterized by $k$ (Bodlaender, Fellows and Hallett 1994), so an $f(k) n^{O(1)}$ algorithm is not expected.
- **Approximation (proved).** No constant factor approximation exists unless P = NP, even for caterpillars (Dubey, Feige and Unger 2011); Feige (2000) gave a polylogarithmic approximation by volume respecting embeddings.
- **Polynomial classes.** Some special classes, such as interval graphs and caterpillars with short hairs, are solvable exactly in polynomial time.
- **What a good bandwidth buys.** A banded Cholesky factorization of half bandwidth $\beta$ costs $n \beta^2 + O(n \beta)$ flops and $n(\beta + 1)$ storage, since all fill stays inside the band ([banded matrix](/banded-matrix/)). For 2D meshes with $n$ unknowns the best possible bandwidth is $\Theta(\sqrt n)$, giving $\Theta(n^2)$ flops, while a nested dissection [fill-reducing ordering](/fill-reducing-ordering/) gives $\Theta(n^{3/2})$.

## Reductions

- **From NP-complete problems.** Papadimitriou's proof reduces from 3-partition; the tree result of Garey et al. also starts from 3-partition.
- **To fill reduction.** A numbering of bandwidth $\beta$ confines the [fill-in](/fill-in/) of Cholesky to the band, so $\operatorname{nnz}(L) \le n(\beta + 1)$. A bandwidth or profile ordering is thus a fill-reducing ordering, usually a weaker one than minimum degree or nested dissection.
- **Relation to treewidth and pathwidth.** The pathwidth of $G$ is at most $\beta(G)$, and the [treewidth](/treewidth/) is at most the pathwidth, so a small bandwidth implies small separators.
- **Reverse numbering.** $f$ and $n + 1 - f$ have the same bandwidth; this is why reversing Cuthill-McKee changes only the profile.

## Applications

- **Banded and envelope solvers** for finite element and [finite difference](/finite-difference-method/) systems, especially on small or long thin domains, and in out-of-core codes where the band is streamed.
- **Cache locality of sparse matrix-vector products.** RCM ordering places the entries of $x$ used by nearby rows close in memory, which reduces cache misses in CG and other Krylov methods.
- **Preconditioners.** The quality of [ILU](/incomplete-lu-factorization/) depends on the ordering, and RCM often improves it compared with the natural or a random order.
- **Graph layouts and VLSI.** Minimizing the length of the longest wire in a linear layout is the same problem.
- **Bioinformatics and seriation.** Ordering items so that similar ones are close (the matrix of similarities becomes nearly banded).

## References
