---
tag: 8C2NV0
kind: problem
slug: fill-reducing-ordering
name: Fill-reducing ordering
aliases:
- sparse matrix ordering
- minimum fill-in ordering
- minimum fill-in problem
- minimum triangulation
area: numerical/linear-systems
level: advanced
summary: Choose an elimination order for a sparse matrix that minimizes fill-in.
prereqs: [sparse-matrix, fill-in, cholesky-decomposition]
see_also: [minimum-degree-ordering, nested-dissection, fill-in, elimination-tree, bandwidth-reduction, reverse-cuthill-mckee, chordal-graph, treewidth]
sources:
  - paper: doi:10.1137/0602010
    title: Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 1981
    locator: pp. 77 to 79
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (minimum degree, nested dissection, column orderings for LU)
  - paper: doi:10.1137/S0895479894278952
    title: Patrick R. Amestoy, Timothy A. Davis and Iain S. Duff, An approximate minimum degree ordering algorithm, SIAM Journal on Matrix Analysis and Applications 17(4), 1996
    locator: pp. 886 to 905
  - paper: doi:10.1137/0716027
    title: Richard J. Lipton, Donald J. Rose and Robert Endre Tarjan, Generalized nested dissection, SIAM Journal on Numerical Analysis 16(2), 1979
    locator: pp. 346 to 358 (O(n log n) fill and O(n^(3/2)) flops for planar graphs)
  - paper: doi:10.1137/0710032
    title: Alan George, Nested dissection of a regular finite element mesh, SIAM Journal on Numerical Analysis 10(2), 1973
    locator: pp. 345 to 363
  - paper: doi:10.1137/S0097539798336073
    title: Assaf Natanzon, Ron Shamir and Roded Sharan, A polynomial approximation algorithm for the minimum fill-in problem, SIAM Journal on Computing 30(4), 2000
    locator: pp. 1067 to 1079 (fill at most 8 k^2 when the minimum is k)
  - paper: doi:10.1109/PROC.1967.6011
    title: W. F. Tinney and J. W. Walker, Direct solutions of sparse network equations by optimally ordered triangular factorization, Proceedings of the IEEE 55(11), 1967
    locator: pp. 1801 to 1809 (the minimum degree rule, scheme 2)
---

## In plain words

When a sparse matrix is factored, new nonzeros appear, and how many depends on the order in which the unknowns are eliminated. One order may keep the factor almost as sparse as the matrix, another may make it completely dense. The fill-reducing ordering problem asks for the order that creates the fewest new nonzeros. Finding the best order exactly is too hard for large matrices, but good orders are found quickly by greedy rules (eliminate the unknown with the fewest connections) or by divide and conquer (cut the problem in two, number the cut last).

## Definition

**Notation.** $A \in \mathbb{R}^{n \times n}$ symmetric positive definite (or symmetric in pattern with a stable diagonal), $G = (V, E)$ its graph with $m = |E|$ edges, $P$ a permutation, $L_P$ the Cholesky factor of $P A P^T$. The analysis is structural: no exact cancellation.

The **fill** of $P$ is $\operatorname{fill}(P) = \operatorname{nnz}(L_P + L_P^T) - \operatorname{nnz}(A)$, counted over strictly off-diagonal positions, so $\operatorname{nnz}(L_P) = \operatorname{nnz}(\operatorname{tril}(A)) + \operatorname{fill}(P)/2$.

**Input:** the pattern of $A$ as the graph $G$.
**Output:** a permutation $P$ minimizing $\operatorname{fill}(P)$.

In graph terms: eliminating vertices in the order $P$ produces a chordal supergraph $G^+_P \supseteq G$ (the filled graph), and every chordal supergraph arises this way. So the problem is the **minimum triangulation** problem: add the fewest edges to make $G$ chordal.

## Variants

- **Minimum operation count.** Minimize the flops $\sum_j c_j^2$, where $c_j$ is the number of nonzeros in column $j$ of $L_P$ below the diagonal (up to lower order terms the Cholesky flop count is $\sum_j c_j^2$). Orderings that minimize fill and flops differ, but the same heuristics serve both.
- **Minimum front size (treewidth).** Minimize the largest $c_j$, which is the [treewidth](/treewidth/) of $G$ when minimized over $P$; it bounds the size of the dense frontal matrices of a [multifrontal](/multifrontal-method/) solver. NP-hard as well (Arnborg, Corneil and Proskurowski 1987).
- **Unsymmetric LU.** For $P A Q = L U$ with pivoting for stability, choose $Q$ before the factorization so that the Cholesky factor of $Q^T A^T A Q$ is sparse, since it contains the patterns of $L$ and $U$ for every row pivoting (George and Ng). COLAMD approximates this without forming $A^T A$.
- **Orderings for parallelism.** Choose $P$ to make the [elimination tree](/elimination-tree/) short and bushy, so that independent subtrees can be factored at the same time.
- **Profile and bandwidth.** Confining fill to a band or envelope gives the [bandwidth reduction](/bandwidth-reduction/) problem.

## Examples

**The arrow matrix.** If vertex $1$ is joined to all others and there are no other edges, eliminating it first makes the remaining $n - 1$ vertices a clique: $\operatorname{fill} = (n - 1)(n - 2)$ off-diagonal positions. Eliminating it last gives $\operatorname{fill} = 0$, which is optimal. Here $G$ is a tree, hence chordal, and any order that eliminates leaves first is a perfect elimination ordering.

**The $3 \times 3$ grid.** For the 5-point Laplacian on $3 \times 3$ points, counting only one triangle, the natural row-by-row order creates $8$ fill entries in $L$. Nested dissection, with the middle row last and the middle points of the two outer rows before it, creates $5$. An exhaustive dynamic program over all subsets of eliminated vertices confirms that $5$ is the minimum.

**Larger grids.** On a $k \times k$ grid the natural order gives $(k - 1)^3$ fill entries in $L$ for $k = 3, 7, 15, 31$, and a simple recursive bisection gives $5, 155, 1627, 11971$; see [fill-in](/fill-in/). Asymptotically the band order has $\Theta(n^{3/2})$ entries in $L$ and nested dissection $\Theta(n \log n)$ for $n = k^2$.

## Known algorithms

| method | time | quality |
|---|---|---|
| [Minimum degree](/minimum-degree-ordering/) (Tinney and Walker 1967; MMD, Liu 1985) | $O(n m)$ worst case, fast in practice with quotient graphs | heuristic; the standard for 2D problems of moderate size |
| Approximate minimum degree, AMD (Amestoy, Davis and Duff 1996) | $O(n m)$ worst case, usually near $O(m)$ | heuristic; about as good as exact minimum degree, much faster |
| Minimum deficiency (minimum local fill) | more expensive per step | heuristic; often less fill than minimum degree |
| [Nested dissection](/nested-dissection/) (George 1973; Lipton, Rose and Tarjan 1979) | dominated by the separator search | provably $O(n \log n)$ fill and $O(n^{3/2})$ flops on planar graphs |
| Multilevel nested dissection (METIS, Scotch) | near $O(m)$ per level of the dissection | heuristic; best for large 2D and 3D meshes |
| [Reverse Cuthill-McKee](/reverse-cuthill-mckee/) | $O(m \log \Delta)$ | profile reduction; usually more fill than the above |
| Natanzon, Shamir and Sharan (2000) | polynomial | fill at most $8 k^2$ if the optimum is $k$ |
| Exact minimum triangulation (Kaplan, Shamir and Tarjan 1999; Fomin and Villanger 2012) | $O(16^k m)$; subexponential $2^{O(\sqrt{k} \log k)} + n^{O(1)}$ | exact, fixed parameter tractable in the fill $k$ |

## Bounds

- **NP-completeness (proved).** Deciding whether $\operatorname{fill}(P) \le k$ for some $P$ is NP-complete (Yannakakis 1981). Minimizing the front size (treewidth) is also NP-hard.
- **Planar graphs (proved).** Every planar graph has an $O(\sqrt n)$ separator, and generalized nested dissection gives $O(n \log n)$ fill and $O(n^{3/2})$ flops (Lipton, Rose and Tarjan 1979). For the $k \times k$ grid, every ordering needs $\Omega(n \log n)$ fill and $\Omega(n^{3/2})$ flops (Hoffman, Martin and Rose 1973), so nested dissection is optimal up to constants there.
- **3D meshes.** For a $k \times k \times k$ grid ($n = k^3$) separators have size $\Theta(n^{2/3})$; nested dissection gives $O(n^{4/3})$ fill and $O(n^2)$ flops, which is why direct methods lose to iterative ones on large 3D problems.
- **Chordal graphs (proved).** Zero fill is possible if and only if $G$ is chordal ([chordal graph](/chordal-graph/)), and such an ordering is found in $O(n + m)$ time by [lexicographic BFS](/lexicographic-bfs/) or maximum cardinality search.
- **Cost of evaluating an ordering.** Given $P$, the [elimination tree](/elimination-tree/) and the column counts of $L_P$, hence $\operatorname{fill}(P)$ and the flop count, are computed in nearly $O(m)$ time, without forming $L_P$.

## Reductions

- **Equivalent to minimum triangulation.** As stated in the definition, the problem is the same as adding the fewest edges to make $G$ chordal; Yannakakis reduces from optimal linear arrangement of bipartite graphs (via chain completion).
- **To graph partitioning.** Nested dissection reduces the ordering problem to repeated balanced vertex separator problems, which are solved by [graph partitioning](/graph-partitioning-problem/) heuristics.
- **From LU to Cholesky.** Column orderings for sparse LU with partial pivoting reduce to symmetric orderings of $A^T A$.
- **To bandwidth.** A banded ordering of half bandwidth $\beta$ is a feasible solution with $\operatorname{nnz}(L) \le n(\beta + 1)$, so bandwidth heuristics give upper bounds.

## Applications

- **Sparse direct solvers.** Every sparse Cholesky, $L D L^T$ and LU code (CHOLMOD, MUMPS, PARDISO, SuperLU, UMFPACK) starts with a fill-reducing ordering; it decides the memory, the flops and the parallelism.
- **Incomplete factorizations.** The ordering affects the quality of [ILU](/incomplete-lu-factorization/) and [IC](/incomplete-cholesky-factorization/) preconditioners as well as their fill.
- **Gaussian elimination on graphical models.** Variable elimination for inference in Bayesian networks and junction tree construction use the same orderings, since the cost is exponential in the largest clique.
- **Power networks and circuit simulation.** Tinney and Walker introduced minimum degree for power flow equations, still a main application.
- **Interior point methods.** Each iteration factors a matrix with a fixed pattern, so one ordering is reused hundreds of times.

## References
