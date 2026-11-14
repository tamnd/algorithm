---
tag: SR6DG7
kind: algorithm
slug: klu-solver
name: KLU
aliases:
- Clark Kent LU
- KLU sparse solver
area: eda/logic-and-circuit-simulation
level: advanced
summary: Davis and Palamadai Natarajan's sparse LU for circuit matrices, using block triangular form, AMD ordering of each block and Gilbert-Peierls factorization with fast refactoring.
model: word-ram
complexity:
  vars: {n: the order of the matrix, a: "the number of nonzeros of A", f: "the multiply and subtract operations of the block factorizations", s: "the number of nonzeros of the block factors"}
  time: {worst: "O(n a + f)"}
  space: {extra: "O(n + a + s)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 2010
  people: [Timothy A. Davis, Ekanathan Palamadai Natarajan]
  note: Davis and Palamadai Natarajan published KLU in 2010 as a solver for the matrices of circuit simulation. It became the default solver of the Xyce simulator.
prereqs: [gilbert-peierls-lu, dulmage-mendelsohn-decomposition, tarjan-scc, minimum-degree-ordering, bipartite-matching, modified-nodal-analysis]
see_also: [markowitz-pivoting, sparse-linear-systems, fill-in, sparse-matrix, strongly-connected-components, hopcroft-karp, dc-operating-point-analysis, transient-circuit-analysis]
sources:
  - paper: doi:10.1145/1824801.1824814
    title: Timothy A. Davis and Ekanathan Palamadai Natarajan, Algorithm 907, KLU, a direct sparse solver for circuit simulation problems, ACM Transactions on Mathematical Software 37(3), article 36, 2010
    locator: the whole paper (the BTF step, the ordering of each block, the factorization with threshold partial pivoting, refactorization, and the comparison with SuperLU, UMFPACK and Sparse 1.3 on circuit matrices)
  - paper: doi:10.1137/0909058
    title: John R. Gilbert and Tim Peierls, Sparse partial pivoting in time proportional to arithmetic operations, SIAM Journal on Scientific and Statistical Computing 9(5), 862 to 874, 1988
    locator: the factorization kernel used on each diagonal block
  - book: isbn:9780198508380
    title: Iain S. Duff, Albert M. Erisman and John K. Reid, Direct Methods for Sparse Matrices, second edition, Oxford University Press, 2017
    locator: the chapter on reduction to block triangular form (the transversal, the strong components and the uniqueness of the form)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: the chapter on fill-reducing orderings, with the maximum transversal and the block triangular form
---

KLU is a sparse direct solver for the matrices of circuit simulation, by Davis and Palamadai Natarajan (2010). It permutes the matrix to block upper triangular form, orders each diagonal block to reduce [fill-in](/fill-in/), factors only the diagonal blocks with [Gilbert-Peierls LU](/gilbert-peierls-lu/), and solves by block back substitution. When only the values change, as from one Newton iteration to the next, it refactors with the same pivots and patterns and skips all symbolic work. It belongs to the circuit simulation half of the logic and circuit simulation sub-area, where it solves the [modified nodal analysis](/modified-nodal-analysis/) systems of DC, transient and AC analysis.

## In plain words

A circuit often splits into parts where signals pass one way only. An amplifier stage drives the next stage, but the next stage does not change the first. The equations of such a circuit can be put in an order where each group of equations needs only the answers of the groups after it. Then the groups can be solved one at a time, from the last to the first, and each group is a small separate problem.

KLU finds this order automatically from the positions of the nonzero coefficients. It then solves each group with sparse elimination, in an order that keeps the work small. A simulator solves the same pattern thousands of times with new numbers, so KLU does the planning once and repeats only the arithmetic.

## The problem

Solve $Ax = b$ for a nonsingular sparse $n \times n$ matrix $A$, many times, where the pattern of $A$ stays fixed and the values change. In a circuit simulator $A$ is the MNA matrix $M$ of $Mx = z$ (or the Jacobian of the nonlinear MNA equations, or $G + j\omega C$ in AC analysis). Circuit matrices have few nonzeros per row, unsymmetric values and often unsymmetric patterns (controlled sources), zeros on the diagonal (rows of voltage sources and inductors), and little fill after a good ordering.

## The algorithm

The *graph* of a matrix $B$ with a zero-free diagonal has a node per index and an edge $i \to t$ for each off-diagonal nonzero $b_{it}$.

```pseudo id=main
KLU(A, b)
L1  Q ← a maximum transversal of A: AQ has a zero-free diagonal
L2  the strongly connected components of the graph of AQ, in reverse of Tarjan's output order, give a symmetric permutation P; T = P A Q Pᵀ is block upper triangular with blocks T_11, ..., T_mm
L3  inside each block, apply a symmetric fill-reducing order of the pattern of T_KK + T_KKᵀ
L4  for K ← 1 to m do
L5      P_K T_KK = L_K U_K by Gilbert-Peierls LU, threshold partial pivoting, diagonal preferred
L6  for K ← m downto 1 do
L7      c_K ← (P b)_K − Σ_{J > K} T_KJ y_J
L8      y_K ← U_K⁻¹ L_K⁻¹ P_K c_K
L9  return x ← Q Pᵀ y
```

Lines L1 to L3 are the symbolic analysis and depend only on the pattern. Line L1 is the transversal step of the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/), found with augmenting paths of [bipartite matching](/bipartite-matching/). Line L2 uses [Tarjan's algorithm](/tarjan-scc/). Lines L4 and L5 are the numerical factorization. *Refactorization* repeats lines L4 and L5 with the pivot rows fixed and no search for patterns. Lines L6 to L8 solve; a $1 \times 1$ block needs one division.

The real KLU orders each block with approximate minimum degree on $T_{KK} + T_{KK}^{\mathsf T}$, the alias of [minimum degree ordering](/minimum-degree-ordering/), or with COLAMD, and accepts the diagonal entry at line L5 when its magnitude is at least $10^{-3}$ times the largest candidate. The code of this page uses the exact minimum degree rule, which is slower on large blocks but has the same purpose.

## Example

Two stages joined by a voltage-controlled current source. Node 1 is held at $1$ V by a voltage source with current $j$. Conductances of $1$ S join node 1 to ground, nodes 1 and 2, node 2 to ground, node 3 to ground, nodes 3 and 4, and node 4 to ground. A source draws $2 e_2$ amperes out of node 3 to ground. With $x = (e_1, e_2, e_3, e_4, j)$ the MNA system is

$$\begin{pmatrix} 2 & -1 & 0 & 0 & 1 \\ -1 & 2 & 0 & 0 & 0 \\ 0 & 2 & 2 & -1 & 0 \\ 0 & 0 & -1 & 2 & 0 \\ 1 & 0 & 0 & 0 & 0 \end{pmatrix} x = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}.$$

| step | result |
|---|---|
| L1, transversal | row 5 (the source row) is matched to column $e_1$, row 1 to column $j$, rows 2, 3, 4 to their own columns |
| L2, components | $\{$rows 3, 4$\}$ (stage 2) is one component; rows 1, 2 and 5 are three singletons, because once row 5 owns $e_1$ the first stage has no cycle |
| L2, block order | rows $(3, 4 \mid 1 \mid 2 \mid 5)$, columns $(e_3, e_4 \mid j \mid e_2 \mid e_1)$ |
| L5, factor | only the $2 \times 2$ block of stage 2 needs elimination: $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ -\tfrac12 & 1 \end{pmatrix} \begin{pmatrix} 2 & -1 \\ 0 & \tfrac32 \end{pmatrix}$ |
| L6 to L8, block 4 | row 5: $e_1 = 1$ |
| block 3 | row 2: $2 e_2 = e_1$, so $e_2 = \tfrac12$ |
| block 2 | row 1: $j = -(2 e_1 - e_2) = -\tfrac32$ |
| block 1 | stage 2 with right side $(-2 e_2, 0) = (-1, 0)$: $e_3 = -\tfrac23$, $e_4 = -\tfrac13$ |

The coupling entry $2$ in row 3 lies in an off-diagonal block. It is used once, at line L7, and it never enters a factor. The determinant is the product of the block determinants with the signs of the permutations, here $-6$.

## Correctness

Line L1 finds a transversal of size $n$ whenever $A$ is nonsingular, because a nonzero determinant needs at least one nonzero product $\prod_i a_{i\sigma(i)}$. Tarjan's algorithm emits a component only after all components reachable from it, so the reversed order puts every nonzero at or above the diagonal blocks. For a block upper triangular matrix $\det T = \prod_K \det T_{KK}$, so each diagonal block is nonsingular, and the block rows solved from the last to the first give the exact solution. Each block factorization is correct by the theorem of Gilbert-Peierls LU. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Line L1 with depth-first augmenting paths costs $O(n \cdot a)$ in the worst case, where $a = \mathrm{nnz}(A)$, and is usually far faster on circuit matrices; [Hopcroft-Karp](/hopcroft-karp/) gives $O(a \sqrt n)$. Line L2 is $O(n + a)$. The ordering of line L3 has no useful worst case bound for the approximate minimum degree of the real KLU beyond $O(n a)$, and is close to linear in practice. Lines L4 and L5 cost $O(n + a + f)$, where $f$ is the arithmetic of the block factorizations, by the theorem of Gilbert-Peierls LU. A solve costs $O(n + a + s)$, where $s$ is the number of nonzeros of the block factors. Refactorization costs $O(n + a + f)$ with a smaller constant, because it does no search.

The gain from the block form is that fill and arithmetic stay inside the diagonal blocks. A chain of $k$ stages coupled one way, each a pair of nodes, gives $k$ blocks of size 2, and the factorization is linear in $k$. On a circuit with global feedback, or on a power grid, the whole matrix is one block and the block step gains nothing. Davis and Palamadai Natarajan report that the block step pays off on many of the circuit matrices of their test set, and that KLU was faster than SuperLU and UMFPACK on most of their circuit matrices; those are their measurements, not proved bounds.

## Properties

- **Built for refactorization.** The symbolic analysis is done once. Newton iterations and time steps then call only the numerical factorization, and most calls reuse the pivots.
- **No dense kernels.** KLU does not use supernodes or the BLAS. On circuit matrices, which have very little fill, dense kernels do not pay off.
- **Partial pivoting inside blocks.** Pivots are chosen only inside the diagonal blocks, which keeps the block form and limits the fill to the blocks.
- **Determinant and condition estimates.** The determinant is a product over the blocks; KLU also gives a cheap estimate of the [condition number](/condition-number/) and of the pivot growth, which a simulator can use to decide when to refactor with new pivots.

## Variants and improvements

- **Without the block step.** For matrices that are known to be irreducible, skip lines L1 and L2.
- **Ordering choices.** Approximate minimum degree on $T_{KK} + T_{KK}^{\mathsf T}$, COLAMD on $T_{KK}$, or an order supplied by the user.
- **Row scaling.** KLU can scale each row by its largest entry or by its sum before the threshold test, which makes the test independent of the units of each equation.

## When to use it

Use KLU for repeated solves of sparse circuit matrices in a SPICE-type simulator, for DC, transient and AC analysis, and for other matrices with the same features: very sparse, unsymmetric, with low fill. For large 2D or 3D mesh problems with high fill, supernodal or multifrontal solvers are faster. For a symmetric positive definite matrix, such as the conductance matrix of a resistor network or a power grid without sources, use [Cholesky](/cholesky-decomposition/).

## Pitfalls

- **Reusing pivots too long.** Refactorization does not check the pivot sizes against a threshold. If a pivot becomes small, the solution is inaccurate without an error. Check the growth or the condition estimate, and run a full factorization when it is bad.
- **Pattern changes.** A device model that drops a stamp entry when its value is zero changes the pattern, and the symbolic analysis becomes invalid. Keep explicit zeros in the pattern.
- **Structural singularity.** A floating node or a loop of voltage sources makes the matrix structurally singular, and line L1 fails. This is a fault in the netlist, not in the solver; [DC operating point analysis](/dc-operating-point-analysis/) codes usually add gmin conductances to avoid it.
- **Expecting gains on one block.** When the whole circuit is one strongly connected block, KLU is only a well-tuned Gilbert-Peierls LU with a fill-reducing order.

## Implementations

## History

Davis and Palamadai Natarajan developed KLU for circuit simulation and published it in 2010 as ACM TOMS Algorithm 907. It combines the block triangular form, whose algorithms Duff, Reid and others developed in the 1970s, with the factorization of Gilbert and Peierls (1988). It is the default solver of Xyce and is used in other simulators, among them NGSPICE, where it is an option that replaces the older Sparse 1.3 package.

## References
