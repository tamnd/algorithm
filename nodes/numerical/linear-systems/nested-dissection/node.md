---
tag: F4FW9V
kind: algorithm
slug: nested-dissection
name: Nested dissection
aliases:
- recursive separator ordering
- ND ordering
- generalized nested dissection
area: numerical/linear-systems
level: research
summary: Order unknowns by recursive separators, giving low fill for planar-like sparse matrices.
solves: [fill-reducing-ordering]
model: word-ram
complexity:
  vars: {n: "the number of vertices (unknowns)", m: "the number of edges (off-diagonal pairs of A)"}
  time: {worst: O(n (n + m)), best: O((n + m) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, in_place: false, recursive: true}
prereqs: [fill-in, planar-separator-theorem, breadth-first-search]
see_also: [minimum-degree-ordering, reverse-cuthill-mckee, fill-reducing-ordering, elimination-tree, multifrontal-method, schur-complement, cholesky-decomposition, sparse-linear-systems]
sources:
  - paper: doi:10.1137/0710032
    title: Alan George, Nested dissection of a regular finite element mesh, SIAM Journal on Numerical Analysis 10(2), 1973
    locator: the cross-shaped dissection of the k by k grid and its storage and operation counts
  - paper: doi:10.1137/0716027
    title: Richard J. Lipton, Donald J. Rose and Robert Endre Tarjan, Generalized nested dissection, SIAM Journal on Numerical Analysis 16(2), 1979
    locator: O(n log n) fill and O(n^(3/2)) operations for graphs with square-root separators
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 1976
    locator: the path characterization of fill used in the correctness proof
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (nested dissection)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (the componentwise backward error bound)
---

Nested dissection orders the unknowns of a sparse symmetric matrix for [Cholesky factorization](/cholesky-decomposition/) by divide and conquer. It finds a small vertex separator $S$ whose removal splits the graph into parts, orders each part recursively, and numbers $S$ last. Since no path between two parts avoids $S$, elimination creates no [fill](/fill-in/) between the parts, and the matrix becomes block-arrowhead. The parts are independent subproblems, coupled only through a dense separator block. For the $k \times k$ grid, $n = k^2$, the factor has $O(n \log n)$ nonzeros and the factorization costs $O(n^{3/2})$ flops. Both orders are optimal for every ordering. Graphs with $O(\sqrt n)$ separators, including all planar graphs, get the same bounds. Bandwidth orderings need $\Theta(n^2)$ flops on the same grid. The separator tree is also the task tree of parallel sparse solvers.

## In plain words

To solve a large system that comes from a mesh, cut the mesh in two with a thin line of unknowns, solve the two halves as if the line were fixed, and deal with the line at the end. Each half is cut the same way, again and again, until the pieces are tiny. Because the two halves never touch except through the line, eliminating one half never spoils the other. The work then concentrates in the cut lines, which are short. The pieces at each level can also be handled at the same time on different processors.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ is symmetric positive definite, $G = (V, E)$ is its graph with $m = |E|$, and $P$ is the permutation of an ordering, with $P A P^T = L L^T$. A *vertex separator* of a vertex set $W$ is a set $S \subseteq W$ such that $G[W \setminus S]$ has at least two components $C_1, \ldots, C_t$. $|L|$ is the number of off-diagonal nonzeros of $L$, and flops are counted as $\sum_k c_k^2$, the leading term of Cholesky's cost, where $c_k$ is the number of nonzeros below the diagonal in column $k$ of $L$. For the numerical factorization: $u = 2^{-53}$, $\gamma_k = k u/(1 - k u)$, and $\kappa_2(A) = \|A\|_2\|A^{-1}\|_2$.

**Input.** The pattern of $A$ as the graph $G$; for the geometric variant, the coordinates of a grid.

**Output.** An ordering with small $|L|$ and small flops, the goal of the [fill-reducing ordering](/fill-reducing-ordering/) problem, whose exact solution is NP-hard. The dissection tree is a by-product: its nodes are separators and leaf blocks, and it describes which parts can be factored independently.

## The algorithm

```pseudo id=main
NESTED-DISSECTION(G, leaf)
L1  order ← empty list;  stack ← [SPLIT(V)]
L2  while stack is not empty do
L3      pop a task
L4      if task = EMIT(S) then append S to order;  continue
L5      W ← the task's vertices;  if G[W] is disconnected, push SPLIT of each component;  continue
L6      if |W| ≤ leaf or no separator is found, append W in minimum degree order;  continue
L7      S ← a small vertex separator of G[W], about balanced
L8      C_1, ..., C_t ← the components of G[W \ S]
L9      push EMIT(S), then SPLIT(C_t), ..., SPLIT(C_1)
L10 return order
```

The stack replaces recursion. EMIT(S) sits below the parts' tasks, so every part is numbered before its separator. The implementation finds $S$ at line L7 from a breadth-first level structure, the simplest form of George and Liu's automatic nested dissection:
- start at a pseudo-peripheral vertex;
- take the level $L_\mu$ where the cumulative count reaches $|W|/2$;
- keep only the vertices of $L_\mu$ with a neighbour in $L_{\mu+1}$.

The geometric version for a $k_1 \times k_2$ grid cuts the longer side at its middle line. George's original scheme cuts both ways at once with a cross. Production codes such as METIS and SCOTCH find separators by multilevel graph partitioning: they coarsen by matchings, partition the small graph, and refine with Kernighan-Lin or Fiduccia-Mattheyses moves on the way back.

## Example

**The $3 \times 3$ grid** (vertices $0, \ldots, 8$ row by row). The middle row $\{3, 4, 5\}$ separates the top row from the bottom row. Each of those rows is split by its middle vertex. The order is $(0, 2, 1, 6, 8, 7, 3, 4, 5)$:
- vertices 0 and 2, then their separator 1;
- vertices 6 and 8, then 7;
- finally the row $3, 4, 5$.

The factor has $|L| = 17$ off-diagonal nonzeros, 5 of them fill, and $\sum c_k^2 = 39$. The natural row-by-row order has $|L| = 20$ and 54 flops. Every fill entry lies inside a separator block or between a block and a later separator, never between the top and bottom rows.

**Growth on grids.** $|L|$ and flops for the $k \times k$ grid. Here "ND" is the level-structure version with leaf size 8, "grid ND" is the geometric bisection, AMD is approximate [minimum degree](/minimum-degree-ordering/), and RCM is [reverse Cuthill-McKee](/reverse-cuthill-mckee/). All numbers come from the implementations:

| $k$ | ND | grid ND | AMD | RCM |
|---|---|---|---|---|
| 16 | 2249, 26785 | 2390, 30472 | 1893, 20203 | 2840, 35240 |
| 32 | 12536, 257776 | 14812, 349600 | 11323, 240127 | 22320, 545104 |
| 48 | 33134, 939408 | 41547, 1373413 | 31611, 985095 | 74824, 2725624 |
| 64 | 68708, 2518240 | 84034, 3544912 | 66965, 3018469 | 176736, 8559264 |

Divided by $k^2 \log_2 k$ and $k^3$, the ND numbers at $k = 16, 32, 48, 64$ are $(2.2, 6.5)$, $(2.5, 7.9)$, $(2.6, 8.5)$ and $(2.8, 9.6)$. Both columns grow slowly toward constants, as the $O(n)$ lower-order terms fade. For RCM the flops divided by $k^3$ grow linearly in $k$: $8.6, 16.6, 24.7, 32.7$, that is, about $k^4/2 = n^2/2$. On these grid sizes, ND has the fewest flops for $k \ge 48$, and AMD has the fewest nonzeros. On large grids the asymptotic orders favour ND; the observed crossover depends on separator quality.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Permutation and termination.** The tasks on the stack, together with the vertices already appended, always partition $V$. Every split strictly shrinks its part, and a trimmed middle level of a breadth-first level structure is a nonempty separator.
- **Order (Lemma 2).** Every part is numbered before its separator, and all vertices of a part come before any ancestor separator that touches it.
- **No fill between parts (Theorem 1).** By the path theorem of Rose, Tarjan and Lueker, $l_{ij} \ne 0$ exactly when a path joins the two vertices through lower-numbered vertices. Every path between two parts passes through a later separator. So no entry of $L$ links two parts, and $P A P^T$ and $L$ have the block-arrowhead structure shown in the proof. The tests check this on random geometric graphs.
- **Bounds.** The fill and flop bounds on grids follow from the recurrences $F(k) = 4F(k/2) + O(k^3)$ and $|L|(k) = 4|L|(k/2) + O(k^2)$. The exact constants are cited from George (1973).

**Numerical stability.** The ordering does not affect backward stability for symmetric positive definite matrices. If Cholesky of $P A P^T$ runs to completion, $\hat L \hat L^T = P A P^T + \Delta A$ with $|\Delta A| \le \gamma_{n+1}|\hat L||\hat L^T|$ (Higham, Chapter 10), and then $\|\Delta A\|_2 \le n\gamma_{n+1}\|A\|_2$. The tests check this elementwise bound with exact rational residuals. The forward error of the solution is then of order $\kappa_2(A) u$ times a modest constant; this is proved, with a worst-case constant. The separator blocks are dense, and their factorization uses dense kernels with the usual rounding analysis. In inner products of length $c$, the bound sharpens to $\gamma_{c+1}$ entrywise.

## Complexity

**Fill and flops** (proved for grids, cited constants):

| problem | $\lvert L \rvert$ | flops | lower bound for any ordering |
|---|---|---|---|
| $k \times k$ grid, $n = k^2$ | $\tfrac{31}{4} k^2\log_2 k + O(k^2) = O(n \log n)$ | about $\tfrac{829}{84}k^3$ multiplications, $O(n^{3/2})$ | $\Omega(n\log n)$, $\Omega(n^{3/2})$ |
| graphs with $O(\sqrt n)$ separators (planar) | $O(n\log n)$ | $O(n^{3/2})$ | same order on grids |
| $k \times k \times k$ grid, $n = k^3$ | $O(n^{4/3})$ | $O(n^2)$ | same order |

The grid constants are from George (1973), and the lower bounds are from Hoffman, Martin and Rose (1973). The planar case is generalized nested dissection (Lipton, Rose and Tarjan, 1979), with separators from the [planar separator theorem](/planar-separator-theorem/). The 3D bounds use separators of size $O(n^{2/3})$. The separator blocks dominate: the top separator of the 2D grid alone is a dense block of order $k$, and the top 3D separator is a dense block of order $k^2$, costing $k^6/3 = n^2/3$ flops.

**Computing the order.** Each level of the dissection tree does breadth-first searches over disjoint parts, $O(n + m)$ per search. The pseudo-peripheral search repeats them a few times, and the tree has $O(\log n)$ levels when the separators are balanced. That gives $O((n + m)\log n)$ in that case. In the worst case, unbalanced splits make the depth $O(n)$, which gives $O(n(n + m))$. Extra space is $O(n + m)$ for the stack, the marks and one level structure. Multilevel partitioners run in near-linear time in practice.

**Memory traffic.** The factorization in this order is dominated by dense operations on separator blocks. Organized as dense blocks, as in the [multifrontal method](/multifrontal-method/), it runs at matrix-multiply speed and is compute-bound. The leaf blocks are small and memory-bound.

## Properties

- **Global and divide and conquer.** It is the opposite of the local greedy rule of minimum degree, and it has provable bounds where minimum degree has none.
- **Parallel.** The parts at each level are independent. The elimination tree is short, of height $O(\sqrt n)$ on 2D grids, against $\Theta(n)$ for banded orders.
- **Optimal order on grids and planar graphs**, up to constants.
- **Sensitive to separator quality.** Poor separators give much more fill, and on small problems minimum degree usually wins.
- **Structural.** Only the pattern is used.

## Variants and improvements

- **Generalized nested dissection** (Lipton, Rose and Tarjan, 1979). Any graph class with $O(n^\alpha)$ separators gets fill and work bounds. For $\alpha = 1/2$ these are $O(n\log n)$ and $O(n^{3/2})$.
- **Automatic nested dissection** (George and Liu). It finds separators from level structures, as in this implementation.
- **One-way dissection** (George). It uses one family of parallel separators instead of recursion, which needs less storage overhead for medium problems.
- **Multilevel partitioning** (METIS, SCOTCH). It gives high-quality edge or vertex separators, converted to vertex separators by a vertex cover on the cut edges.
- **Hybrid with minimum degree.** It switches to (constrained) minimum degree on small parts, as here at line L6, and on the separators themselves.
- **Spectral dissection.** Separators come from the Fiedler vector of the graph Laplacian.
- **Hierarchical (low-rank) solvers.** They compress the dense separator blocks, which in many PDE problems have low-rank off-diagonal structure, to reduce the $O(n^{3/2})$ or $O(n^2)$ cost.

## When to use it

Use nested dissection, through a multilevel partitioner, for large 2D and especially 3D finite element and finite difference problems solved by sparse direct methods. Use it when parallelism matters. Use it when the matrix comes from a mesh with good separators. For small and medium problems, or for matrices without geometric structure such as circuits, [AMD](/minimum-degree-ordering/) is usually as good and faster to compute. For band or envelope solvers, use [RCM](/reverse-cuthill-mckee/).

## Pitfalls

- **Unbalanced separators.** If one part is much larger than the other, the depth becomes linear and the bounds are lost. Balance and size must both be controlled.
- **Recursing to single vertices.** Very small parts create overhead and many tiny separators. Stop at a leaf size and use minimum degree there.
- **Wrong order of separator and parts.** The separator must be numbered after the parts it separates. Numbering it first destroys the block structure and creates dense fill.
- **Expecting gains on graphs without small separators.** Expander-like graphs have separators of size $\Theta(n)$, and every ordering then gives $\Theta(n^2)$ fill.
- **Deep recursion in implementations.** On unbalanced inputs the dissection can be deep. Use an explicit stack, as here.

## Implementations

## History

Alan George (1973) introduced nested dissection for the regular finite element mesh. He proved storage $O(n \log n)$ and work $O(n^{3/2})$, and Hoffman, Martin and Rose (1973) showed these orders are optimal. Rose, Tarjan and Lueker (1976) gave the path characterization of fill. Lipton and Tarjan (1979) proved the planar separator theorem. With Rose (1979), they turned it into generalized nested dissection for every planar graph. George and Liu developed automatic nested dissection and one-way dissection around 1978 to 1981. Multilevel partitioners, METIS by Karypis and Kumar in 1998, made nested dissection the standard ordering for large 3D problems.

## References
