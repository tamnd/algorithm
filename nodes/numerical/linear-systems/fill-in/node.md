---
tag: T7DGE5
kind: concept
slug: fill-in
name: Fill-in
aliases:
- fill
- fill-in entries
area: numerical/linear-systems
level: advanced
summary: Entries that become nonzero during factorization of a sparse matrix.
prereqs: [sparse-matrix, gaussian-elimination, cholesky-decomposition]
see_also: [fill-reducing-ordering, elimination-tree, minimum-degree-ordering, nested-dissection, reverse-cuthill-mckee, incomplete-lu-factorization, sparse-linear-systems, multifrontal-method]
sources:
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 4, Cholesky factorization (elimination tree, sparse triangular solves, row and column counts); Chapter 7, Fill-reducing orderings
  - paper: doi:10.1016/0022-247X(70)90282-9
    title: Donald J. Rose, Triangulated graphs and the elimination process, Journal of Mathematical Analysis and Applications 32(3), 1970
    locator: pp. 597 to 609 (elimination graphs, perfect elimination orderings and chordal graphs)
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 1976
    locator: pp. 266 to 283 (the fill path lemma and lexicographic breadth first search)
  - paper: doi:10.1137/0602010
    title: Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 1981
    locator: pp. 77 to 79
  - paper: doi:10.1137/0710032
    title: Alan George, Nested dissection of a regular finite element mesh, SIAM Journal on Numerical Analysis 10(2), 1973
    locator: pp. 345 to 363 (O(n log n) fill and O(n^(3/2)) flops on a k by k grid)
  - paper: doi:10.1137/1003021
    title: Seymour Parter, The use of linear graphs in Gauss elimination, SIAM Review 3(2), 1961
    locator: pp. 119 to 130 (the graph model of elimination)
---

Fill-in is the set of positions that are zero in a sparse matrix $A$ but nonzero in its factors. In the Cholesky factorization $A = L L^T$ of a symmetric positive definite matrix, an entry $l_{ij}$ with $a_{ij} = 0$ is fill. How much fill appears depends on the order in which the unknowns are eliminated, and the difference is dramatic: the arrow matrix fills completely in one order and not at all in the reverse order, and on a $k \times k$ grid the natural order gives $\Theta(k^3)$ fill against $\Theta(k^2 \log k)$ for [nested dissection](/nested-dissection/). Fill decides the memory and the flops of every sparse direct solver, which is why the choice of a [fill-reducing ordering](/fill-reducing-ordering/) comes before any arithmetic.

## In plain words

A sparse matrix is mostly zeros, which is what makes it cheap to store. When you eliminate one unknown, every equation that mentioned it now mentions all the other unknowns from that equation too, so new nonzeros appear. Those new nonzeros are the fill. Eliminate a hub that touches everything first and the whole matrix becomes dense. Eliminate the quiet corners first and almost nothing new appears. So the order of elimination can make the difference between a factorization that fits in memory and one that does not.

## The idea

**Notation.** $A \in \mathbb{R}^{n \times n}$ symmetric with a zero-free diagonal, $G(A)$ its graph on vertices $1, \ldots, n$ with an edge $\{i, j\}$ for each $a_{ij} \ne 0$, $i \ne j$. $L$ is the Cholesky factor in the given order, $\operatorname{nnz}(\cdot)$ counts nonzeros, and the filled graph $G^+(A)$ is the graph of $L + L^T$. The analysis is structural: it assumes no entry becomes zero by exact numerical cancellation, which is the generic case.

**The elimination game (Parter 1961, Rose 1970).** Eliminating vertex $1$ replaces the trailing matrix by the Schur complement $A_{2:n,2:n} - a_{2:n,1} a_{1,2:n} / a_{11}$, whose pattern is that of $A_{2:n,2:n}$ plus all pairs of neighbours of vertex $1$. In graph terms: delete vertex $1$ and make its neighbours a clique. Every new edge is fill. Repeating this for vertices $2, 3, \ldots$ yields $G^+(A)$.

**The fill path theorem (Rose, Tarjan and Lueker 1976, proved).** For $i > j$, $l_{ij} \ne 0$ structurally if and only if there is a path from $i$ to $j$ in $G(A)$ whose interior vertices are all numbered less than $j$. So fill is a reachability property, and it can be computed without simulating elimination. The [elimination tree](/elimination-tree/) compresses this information: the pattern of row $i$ of $L$ is the set of vertices on the tree paths from the nonzeros of row $i$ of $A$ up to $i$.

**Chordal graphs.** An ordering produces no fill exactly when every vertex's higher numbered neighbours form a clique, a perfect elimination ordering. Rose (1970) showed that such an ordering exists if and only if $G(A)$ is chordal, and $G^+(A)$ is always chordal. So minimizing fill is the same as finding a chordal supergraph with fewest added edges, which is NP-complete (Yannakakis 1981).

**Unsymmetric and pivoted factorizations.** For $P A = L U$ with partial pivoting the pattern depends on the pivots, but it is contained in the pattern of the Cholesky factor of $A^T A$ (George and Ng), so column orderings for LU are chosen on $A^T A$ or its approximations (COLAMD).

## Examples

**The arrow matrix.** Let $A$ have nonzeros on the diagonal, in the first row and in the first column. Eliminating vertex $1$ first connects all other vertices, so $L$ is dense: $(n - 1)(n - 2)/2$ fill entries, $\operatorname{nnz}(L) = n(n+1)/2$, and $\Theta(n^3)$ flops. Reverse the order so the hub comes last: every other vertex has the single neighbour $n$, no clique is created, the fill is $0$, $\operatorname{nnz}(L) = 2n - 1$, and the factorization costs $O(n)$ flops.

**Tridiagonal and banded matrices.** A tridiagonal matrix has no fill in the natural order. A [banded matrix](/banded-matrix/) of half bandwidth $p$ fills only inside the band, so $\operatorname{nnz}(L) \le (p + 1) n$.

**The 5-point grid.** For the Laplacian on a $k \times k$ grid ($n = k^2$) in the natural row-by-row order, the half bandwidth is $k$ and the band fills in. Counting the fill exactly with the elimination game gave the numbers below; for the natural order they equal $(k - 1)^3$ for these $k$, and nested dissection, using middle rows and columns as separators recursively, gives much less.

| $k$ | $n$ | fill, natural order | fill, nested dissection |
|---|---|---|---|
| 3 | 9 | 8 | 5 |
| 7 | 49 | 216 | 155 |
| 15 | 225 | 2744 | 1627 |
| 31 | 961 | 27000 | 11971 |

George (1973) proved that nested dissection gives $\operatorname{nnz}(L) = O(n \log n)$ and $O(n^{3/2})$ flops on this grid, against $\Theta(n^{3/2})$ entries and $\Theta(n^2)$ flops for a band ordering, and Hoffman, Martin and Rose (1973) proved that $\Omega(n^{3/2})$ flops are needed by every ordering.

**Numerical cancellation.** For $A = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{pmatrix}$, $a_{23} = 1$ and eliminating vertex $1$ gives $a_{23}^{(2)} = 1 - 1 = 0$: an entry that is structurally nonzero is numerically zero. Sparse codes ignore such cancellation because it depends on values and is rare; the structural pattern is an upper bound.

**Incomplete factorizations.** [ILU(0)](/incomplete-lu-factorization/) and [IC(0)](/incomplete-cholesky-factorization/) discard all fill; ILU($p$) keeps fill of level at most $p$, where an original entry has level $0$ and fill created from entries of levels $a$ and $b$ has level $a + b + 1$.

## Where it is used

- **Orderings.** [Minimum degree](/minimum-degree-ordering/) eliminates the vertex creating the fewest new edges, greedily; [nested dissection](/nested-dissection/) eliminates separators last; [reverse Cuthill-McKee](/reverse-cuthill-mckee/) confines fill to a narrow profile. All aim to reduce fill.
- **Symbolic factorization.** Before any arithmetic, a sparse Cholesky code computes the [elimination tree](/elimination-tree/) and the column counts of $L$ in nearly $O(\operatorname{nnz}(A))$ time, then allocates exactly $\operatorname{nnz}(L)$ storage.
- **Supernodal and [multifrontal](/multifrontal-method/) methods.** Columns of $L$ with nested patterns are grouped into dense blocks, so most flops become dense matrix operations.
- **Choosing direct or iterative.** If the predicted $\operatorname{nnz}(L)$ is too large, as for 3D meshes where it is $\Theta(n^{4/3})$ with nested dissection, one uses an iterative method with an incomplete factorization or [multigrid](/multigrid-method/) instead.
- **Pivoting in sparse LU.** Threshold pivoting chooses among numerically acceptable pivots the one with the smallest Markowitz count $(r_i - 1)(c_j - 1)$, a bound on the fill it creates.

## References
