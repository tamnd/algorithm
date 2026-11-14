---
tag: 6ASGQ9
kind: algorithm
slug: gilbert-peierls-lu
name: Gilbert-Peierls sparse LU
aliases:
- left-looking sparse LU
- Gilbert-Peierls algorithm
area: eda/logic-and-circuit-simulation
level: advanced
summary: Sparse LU with partial pivoting that builds each column of L and U from the earlier columns, finding its pattern by depth-first search, in time proportional to the arithmetic.
model: word-ram
complexity:
  vars: {n: the order of the matrix, a: "the number of nonzeros of A", f: "the number of multiply and subtract operations of the factorization", s: "the number of nonzeros of L and U"}
  time: {worst: "O(n + a + f)"}
  space: {extra: "O(n + s)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1988
  people: [John R. Gilbert, Tim Peierls]
  note: Gilbert and Peierls published the column-by-column method with a depth-first search for the pattern in 1988. KLU, from 2010, uses it as the factorization kernel for circuit matrices.
prereqs: [lu-decomposition, partial-pivoting, sparse-matrix, fill-in, depth-first-search, topological-sort, triangular-system-solving, modified-nodal-analysis]
see_also: [markowitz-pivoting, klu-solver, minimum-degree-ordering, elimination-tree, multifrontal-method, back-substitution, sparse-linear-systems, growth-factor]
sources:
  - paper: doi:10.1137/0909058
    title: John R. Gilbert and Tim Peierls, Sparse partial pivoting in time proportional to arithmetic operations, SIAM Journal on Scientific and Statistical Computing 9(5), 862 to 874, 1988
    locator: the column algorithm, the reach of the column pattern by depth-first search, and the time bound
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: the chapter on solving triangular systems (the sparse triangular solve with a sparse right-hand side) and the chapter on LU factorization (the column method with partial pivoting)
  - paper: doi:10.1145/1824801.1824814
    title: Timothy A. Davis and Ekanathan Palamadai Natarajan, Algorithm 907, KLU, a direct sparse solver for circuit simulation problems, ACM Transactions on Mathematical Software 37(3), article 36, 2010
    locator: the use of the method on the diagonal blocks of circuit matrices and the symmetric pruning of Eisenstat and Liu
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 3, solution of linear algebraic circuit equations (LU factorization, pivoting and sparse matrices)
---

Gilbert-Peierls LU is a [sparse LU factorization](/lu-decomposition/) with [partial pivoting](/partial-pivoting/). It computes the factors one column at a time: column $k$ of $L$ and $U$ is the solution of one sparse triangular system with the columns of $L$ already found. Before the arithmetic it finds the nonzero pattern of that solution by a [depth-first search](/depth-first-search/) in the graph of $L$, so the total time is proportional to the number of arithmetic operations plus the size of the matrix. It is a general method of sparse linear algebra; on this page it is framed for the circuit simulation half of the logic and circuit simulation sub-area, where it factors the [modified nodal analysis](/modified-nodal-analysis/) matrices of [KLU](/klu-solver/).

## In plain words

Elimination on a matrix that is almost all zeros wastes time if it looks at the zeros. This method builds the answer column by column. For each new column it first works out which positions can become nonzero, by following links from the known nonzeros through the part of the factor already built. Then it does arithmetic only on those positions, in an order where every value is final before it is used.

The search costs no more than the arithmetic it prepares. So the method never spends much time on bookkeeping, even when each column has only a few nonzeros, which is the usual case for circuits. It also swaps rows during the work to keep the numbers stable.

## The problem

Given a nonsingular $n \times n$ [sparse matrix](/sparse-matrix/) $A$, find a row permutation $P$, a unit lower triangular $L$ and an upper triangular $U$ with $PA = LU$, and use them to solve $Ax = b$. In a circuit simulator $A$ is the MNA matrix $M$ of the system $Mx = z$, or the Jacobian of the nonlinear MNA equations at one Newton iteration. The column order is fixed in advance by a fill-reducing order such as [minimum degree](/minimum-degree-ordering/); the row order is chosen during the factorization.

## The algorithm

Write $\pi(j)$ for the row of $A$ chosen as pivot $j$. A row is *pivotal* once it is some $\pi(j)$. The graph of $L$ has the rows as nodes and an edge $\pi(j) \to r$ for each nonzero $L(r, j)$.

```pseudo id=main
GP-LU(A)
L1  for k ← 1 to n do
L2      X ← REACH(L, rows of the nonzeros of A(:, k))       ▷ in topological order
L3      x ← A(:, k), scattered on the rows of X (zero where A has no entry)
L4      for each row i in X, in order do
L5          if i = π(j) for some j < k then
L6              for each r with L(r, j) ≠ 0 do x_r ← x_r − L(r, j) · x_i
L7      p ← the non-pivotal row of X with the largest |x_p|; if x_p = 0 then return "singular"
L8      U(π(j), k) ← x_π(j) for the pivotal rows of X; U(k, k) ← x_p; L(r, k) ← x_r / x_p for the other non-pivotal rows of X
L9      π(k) ← p
L10 return π, L, U

REACH(L, B)
R1  for each s in B not yet marked do DFS(s)
R2  DFS(i): mark i; if i = π(j) then for each r with L(r, j) ≠ 0, r not marked do DFS(r)
R3      append i to the postorder
R4  return the postorder reversed
```

Lines L3 to L6 are a column-oriented [triangular solve](/triangular-system-solving/) $L x = A(:, k)$ that touches only the rows in $X$. The reverse postorder of the search is a [topological order](/topological-sort/) of the graph of $L$, so each $x_{\pi(j)}$ is final before line L6 uses it. To solve $Ax = b$, run forward substitution with $L$ on $Pb$ and [back substitution](/back-substitution/) with $U$.

## Example

Take the matrix below. It has a zero in each position where a new nonzero will appear, so the trace shows both pivoting and [fill-in](/fill-in/).

$$A = \begin{pmatrix} 1 & 0 & 0 & 2 \\ 4 & 2 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & -1 & 1 \end{pmatrix}$$

Rows are numbered 1 to 4.

| column $k$ | start rows $B$ | reach $X$ (in order) | values after line L6 | pivot | new $L(:, k)$ | new $U(:, k)$ |
|---|---|---|---|---|---|---|
| 1 | 1, 2 | 1, 2 | $x_1 = 1$, $x_2 = 4$ | row 2 | $L(1,1) = 1/4$ | $U(1,1) = 4$ |
| 2 | 2, 3 | 2, 1, 3 | $x_2 = 2$, $x_1 = 0 - \tfrac14 \cdot 2 = -\tfrac12$, $x_3 = 1$ | row 3 | $L(1,2) = -\tfrac12$ | $U(1,2) = 2$, $U(2,2) = 1$ |
| 3 | 3, 4 | 3, 1, 4 | $x_3 = 1$, $x_1 = 0 + \tfrac12 \cdot 1 = \tfrac12$, $x_4 = -1$ | row 4 | $L(1,3) = -\tfrac12$ | $U(2,3) = 1$, $U(3,3) = -1$ |
| 4 | 1, 4 | 4, 1 | $x_4 = 1$, $x_1 = 2 + \tfrac12 \cdot 1 = \tfrac52$ | row 1 | none | $U(3,4) = 1$, $U(4,4) = \tfrac52$ |

In column 2 the search goes from row 2, which is pivot 1, along the edge to row 1, because $L(1, 1) \ne 0$. Row 1 has a zero in $A(:, 2)$, so $L(1, 2)$ is a fill entry, found by the search before any arithmetic. In column 4 the search starts at rows 1 and 4, follows the edge from row 4 (pivot 3) to row 1, and never visits rows 2 and 3, because no path leads there. The pivot order is $\pi = (2, 3, 4, 1)$. The factorization does 3 multiply and subtract operations, and the four searches visit 10 nodes and traverse 3 edges. With $b = (3, 6, 2, 0)$ the solution is $x = (1, 1, 1, 1)$.

## Correctness

The column solve of lines L3 to L6 is forward substitution with the columns of $L$ found so far, and it is correct when each pivotal row is visited before every row it updates. The search gives that order: along each edge of the graph of $L$ the pivot step grows, so the graph has no cycle, and the reverse postorder of a depth-first search of a graph with no cycle is a topological order. The rows where $x$ is structurally nonzero are exactly the rows reachable from the nonzeros of $A(:, k)$, so the search misses no nonzero. The patterns of $L$ and $U$ equal those of symbolic Gaussian elimination on $PA$. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**Theorem.** In step $k$ the search traverses exactly $f_k$ edges and visits at most $|B| + f_k$ nodes, where $f_k$ is the number of multiply and subtract operations of line L6 and $|B|$ the number of nonzeros of $A(:, k)$. The whole factorization takes $O(n + \mathrm{nnz}(A) + f)$ time, where $f = \sum_k f_k$.

The proof is short: the out-edges of row $\pi(j)$ are the nonzeros of $L(:, j)$, and line L6 does one operation for each of them. This is the result of the title of the 1988 paper. Earlier sparse codes with partial pivoting either scanned a dense work vector of length $n$ per column, which costs $\Theta(n^2)$ in total even for a diagonal matrix, or needed a symbolic analysis that assumed a fixed pivot order. Space is $O(n)$ for the work vector and the marks plus the storage of $L$ and $U$.

The bound does not say that $f$ is small. $f$ depends on the column order and on the pivots. With a poor column order, $f$ grows fast: on the nodal matrices of $k \times k$ resistor grids in row-major order (a conductance of $1/10$ S to ground at every node, floats, the code of this page), the measured counts are:

| grid | $n$ | $\mathrm{nnz}(A)$ | $f$ | nodes visited | edges traversed |
|---|---|---|---|---|---|
| $10 \times 10$ | 100 | 460 | 8769 | 1918 | 8769 |
| $20 \times 20$ | 400 | 1920 | 149739 | 15638 | 149739 |
| $30 \times 30$ | 900 | 4380 | 774909 | 53158 | 774909 |

The edge count equals $f$, as the theorem says. For an $n \times n$ tridiagonal matrix the measured counts are $f = n - 1$ and $3n - 2$ visited nodes, so the total work is linear. These are toy inputs, not benchmark results.

## Properties

- **Exact patterns, no symbolic phase.** The pattern of each column is found during the factorization, so partial pivoting can choose any row. No estimate of the fill is needed in advance.
- **Stable as partial pivoting.** Every multiplier has $|L(r, k)| \le 1$, so the backward error bound is that of dense partial pivoting.
- **Column by column.** Each step reads only the columns of $L$ already built and writes one new column of $L$ and of $U$. Memory can grow as the factorization proceeds.
- **Good for very sparse matrices.** Circuit matrices have few nonzeros per column and little fill after ordering, so the dense kernels of supernodal and [multifrontal](/multifrontal-method/) codes have little work to speed up. This method has no dense kernel and no overhead per column beyond the search.

## Variants and improvements

- **Symmetric pruning.** Eisenstat and Liu showed that edges of the graph of $L$ can be removed without changing the reach sets, once a symmetric pair $L(r, j) \ne 0$ and $U(j, r) \ne 0$ is found. This makes the searches faster. KLU uses it (Davis and Palamadai Natarajan 2010).
- **Threshold pivoting with a preferred diagonal.** Accept the planned diagonal entry when $|x_{\text{diag}}| \ge u \max |x_r|$, which keeps the fill-reducing order. KLU does this with $u = 10^{-3}$ by default.
- **Refactorization.** When only the values change, as in Newton iterations, keep $\pi$ and the patterns and repeat lines L3 to L8 without the search and without pivot choice.
- **Sparse right-hand side.** The same search solves $Lx = b$ for a sparse $b$ in time proportional to the arithmetic, which is useful for a few entries of $A^{-1}$ or for the adjoint solves of [noise analysis](/circuit-noise-analysis/).
- **Supernodes.** SuperLU groups columns with the same pattern to use dense kernels; this pays off when fill is high, which is rare for circuits.

## When to use it

Use it to factor sparse unsymmetric matrices with low fill after ordering, such as circuit matrices, when partial pivoting is needed for stability. Combine it with a fill-reducing column order and, for circuits, with the block triangular form of KLU. For matrices from 2D and 3D meshes, where the factors become dense, supernodal or multifrontal codes are faster. For symmetric positive definite matrices, use [Cholesky](/cholesky-decomposition/) with an [elimination tree](/elimination-tree/), which needs no pivoting.

## Pitfalls

- **Scanning the work vector.** Clearing or scanning a dense vector of length $n$ in each column brings back the $\Theta(n^2)$ term that the method avoids. Clear only the rows in $X$.
- **Recursive search.** A recursive depth-first search can overflow the stack on a long path in the graph of $L$. Use an explicit stack, as the code of this page does.
- **Wrong visiting order.** Visiting the rows of $X$ in index order instead of topological order uses values that are not final. The result is wrong without any error message.
- **No column order.** The method does not reduce fill by itself. Without a fill-reducing column order, the arithmetic $f$ can be much larger than needed.
- **Structural versus numerical zeros.** An entry that cancels to zero still lies in the pattern. A code that drops it changes the graph of $L$, which is allowed, but it must then drop it consistently in the later searches.

## Implementations

## History

Gilbert and Peierls published the method in 1988, with the title result that sparse partial pivoting can run in time proportional to the arithmetic. Davis gave a compact implementation in the CSparse package and in his 2006 book. Davis and Palamadai Natarajan built KLU on it for circuit simulation, and KLU became the default sparse solver of the Xyce circuit simulator (Davis and Palamadai Natarajan 2010).

## References
