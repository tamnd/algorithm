---
tag: C6B46K
kind: algorithm
slug: multigrid-power-grid-analysis
name: Multigrid-like power grid analysis
aliases:
- Kozhaya-Nassif-Najm multigrid
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Kozhaya, Nassif and Najm's power grid solver that reduces the mesh to a coarse grid, solves it directly and maps the answer back once, with no smoothing, for DC and transient IR drop.
solves: [power-grid-analysis]
model: word-ram
complexity:
  vars: {N: the number of grid nodes, M: the number of nodes of the coarsest grid}
  time: {worst: "O(N + M^3)"}
  space: {extra: "O(N + M^2)"}
properties: {deterministic: true, exact: false, recursive: true}
history:
  year: 2001
  people: [Joseph N. Kozhaya, Sani R. Nassif, Farid N. Najm]
  note: Kozhaya, Nassif and Najm gave the method at ICCAD 2001 and in IEEE Transactions on Computer-Aided Design in 2002, as a fast approximate solver for the DC and transient analysis of large power grids, borrowing the coarse grid and interpolation of multigrid but not its iteration.
prereqs: [power-grid-analysis, multigrid-method]
see_also: [algebraic-multigrid, galerkin-method, gauss-seidel-method, conjugate-gradient-method, cholesky-decomposition, preconditioning, random-walk-power-grid-analysis, vectorless-power-grid-verification]
sources:
  - paper: "Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, A multigrid-like technique for power grid analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(10), 1148 to 1160, October 2002"
    title: Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, A multigrid-like technique for power grid analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(10), 1148 to 1160, October 2002
    locator: the grid reduction, the interpolation of the dropped nodes by their conductances, the coarse solve, the mapping back, the transient form, and the measured accuracy and speed on industrial grids
  - paper: "Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, Multigrid-like technique for power grid analysis, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 480 to 487, November 2001"
    title: Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, Multigrid-like technique for power grid analysis, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 480 to 487, November 2001
    locator: the conference version of the method
  - book: isbn:9780898714623
    title: William L. Briggs, Van Emden Henson and Steve F. McCormick, A Multigrid Tutorial, 2nd edition, SIAM, 2000
    locator: the chapters on the two-grid correction scheme, the variational properties of the Galerkin coarse operator, and the energy norm
---

The multigrid-like power grid analysis of Kozhaya, Nassif and Najm is a fast approximate solver for [power grid analysis](/power-grid-analysis/), the problem of finding the voltage drop at every node of an on-chip supply mesh. The drop $x$ solves $G x = i$, with $G$ the conductance matrix of the grid and $i$ the load currents. The method keeps every other row and every other column of the mesh, writes each dropped node as a weighted mean of its kept neighbors with the wire conductances as weights, and solves the much smaller coarse system with a direct method. It maps the coarse answer back to the fine grid once and stops. Unlike the [multigrid method](/multigrid-method/), it does no smoothing and no iteration, so its answer is not exact. This page proves what it does give: the best approximation in the energy norm among all vectors that the interpolation can produce.

## In plain words

A power grid on a chip is a mesh of wires with millions of crossing points. You want the voltage at each point, which means solving millions of linked equations.

This method throws away every other row and every other column of the mesh, so about a quarter of the points stay. It works out how the removed points would follow the kept ones: a removed point sits between kept points, and it follows the one it is wired to more strongly. It folds the loads of the removed points onto the kept ones, solves the small mesh exactly, and fills in the removed points from their neighbors.

It does this once. The answer is close on smooth parts of the grid and less close at sharp local peaks.

## The problem

The grid is an $n_x \times n_y$ mesh of nodes with wires of conductance $g_{jk}$ between neighbors, pads of conductance $g^{\mathrm{pad}}_k$ to the ideal supply at some nodes, and a load current $i_k \ge 0$ drawn at each node. The drop $x_k = V_{DD} - v_k$ solves

$$ A x = b, \qquad A = G = \mathcal{L} + \mathrm{diag}(g^{\mathrm{pad}}), \qquad b = i, $$

where $\mathcal{L}$ is the weighted [Laplacian](/laplacian-matrix/) of the wires. The [power grid analysis](/power-grid-analysis/) page shows that $A$ is a symmetric, [positive definite](/positive-definite-matrix/) M-matrix when every connected part has a pad. For a transient step with the [backward Euler method](/backward-euler-method/) and step $h$, the same form holds with $A = G + C/h$ and $b = i(t) + (C/h) x(t - h)$, by the [companion model](/companion-model/) of each capacitor. The output is $x$, or an approximation of it, at every node. The method fits no parameter of its own. The conductances, capacitances and loads come from layout extraction, foundry data and power estimates, as the power grid analysis page explains.

The energy norm of a vector $e$ is $\|e\|_A = \sqrt{e^T A e}$. For a drop error $e$ it is the power that the error currents would spend in the wires and pads.

## The algorithm

Number the node in row $r$ and column $c$ as $r n_x + c$. The kept lines are the even ones and the last one, in each direction. Each fine node is in one of four classes. A K node is on a kept row and a kept column, and it maps to itself. An H node is on a kept row between two K nodes, and its weights are its conductances to them, normalized to sum to 1. A V node is the same along a column. A C node is on two dropped lines, and it takes the normalized conductance weights of its four H and V neighbors, through their own rows of $P$.

```pseudo id=main
KNN-SOLVE(A, b, mesh, levels)
L1  if levels = 0 or the mesh is small then return the direct solution of A x = b
L2  P ← the interpolation from the kept nodes to all nodes (K, H, V and C rules)
L3  A_c ← Pᵀ A P;  b_c ← Pᵀ b
L4  x_c ← KNN-SOLVE(A_c, b_c, the coarse mesh, levels − 1)
L5  return P x_c                                   ▷ no smoothing

TWO-GRID-VARIANT(A, b, mesh, cycles)               ▷ not in the paper
L6  x ← KNN-SOLVE(A, b, mesh, 1)
L7  repeat cycles times
L8      one Gauss-Seidel sweep on A x = b
L9      r ← b − A x
L10     x ← x + P A_c⁻¹ Pᵀ r
L11     one Gauss-Seidel sweep on A x = b
```

Lines L1 to L5 are the method of the paper, applied over several levels. Lines L6 to L11 are a variant of this page: a standard two-grid cycle with [Gauss-Seidel](/gauss-seidel-method/) smoothing, which turns the one-pass answer into an iteration that converges to the exact drop. It is here to show what the missing smoothing would add.

## Example

Take a $5 \times 5$ mesh with every wire at 10 S, pads of 50 S at the four corners, and loads of 0.1 A at the center node 12 and 0.05 A at nodes 8 and 16. The kept lines are 0, 2 and 4 in each direction, so the coarse mesh is $3 \times 3$ with the nodes 0, 2, 4, 10, 12, 14, 20, 22 and 24. All wires are equal, so node 1 (an H node) gets the weights $(1/2, 1/2)$ on nodes 0 and 2, and node 6 (a C node) gets $1/4$ on each of the coarse nodes 0, 2, 10 and 12.

The drops in mV, exact on the left and after one pass on the right:

| row | exact | one pass |
|---|---|---|
| 0 | 0.919, 3.218, 4.250, 3.782, 1.081 | 0.900, 2.379, 3.857, 2.479, 1.100 |
| 1 | 3.218, 4.484, 5.750, 6.016, 3.782 | 2.379, 3.921, 5.464, 3.971, 2.479 |
| 2 | 4.250, 5.750, 8.250, 5.750, 4.250 | 3.857, 5.464, 7.071, 5.464, 3.857 |
| 3 | 3.782, 6.016, 5.750, 4.484, 3.218 | 2.479, 3.971, 5.464, 3.921, 2.379 |
| 4 | 1.081, 3.782, 4.250, 3.218, 0.919 | 1.100, 2.479, 3.857, 2.379, 0.900 |

The worst drop is $33/4000$ V $= 8.25$ mV at the center, and the one-pass answer gives 7.07 mV there. The largest error is at node 8, a C node with its own load: 3.97 mV against 6.02 mV, because line L3 spreads its load over four coarse nodes. The energy of the error is $3.22 \times 10^{-4}$ W against $x^T A x = 1.43 \times 10^{-3}$ W. The total current through the pads is 0.2 A in both answers. On this tiny grid with point loads the one-pass error is large. The variant of lines L6 to L11 brings the largest residual down to $6.51 \times 10^{-3}$, $3.94 \times 10^{-4}$, $2.47 \times 10^{-5}$, $3.81 \times 10^{-6}$, $4.46 \times 10^{-7}$ and $6.02 \times 10^{-8}$ in six cycles. These are runs of the code of this page on this toy grid, not benchmark results.

## Correctness

The [proof file](proofs/correctness.md) proves four facts. First, $A_c = P^T A P$ is symmetric and positive definite, because $P$ has full column rank: each kept node maps to itself. So line L4 is well defined at every level. Second, the one-pass answer $\hat{x} = P x_c$ satisfies the Galerkin condition $P^T A (x - \hat{x}) = 0$, so it is the vector of the form $P y$ closest to the exact $x$ in the energy norm, and with several levels the same holds for the product of the interpolations. Third, since the error is $A$-orthogonal to $\hat{x}$, the energies add up, $x^T A x = \hat{x}^T A \hat{x} + \|x - \hat{x}\|_A^2$, so the load-weighted drop $b^T \hat{x}$ is never above the exact $b^T x$. Fourth, the rows of $P$ sum to 1, so $P^T$ keeps the total load, and the pad currents of the coarse answer add up to the total load, as in the example.

The proofs say nothing about the error at a single node. In the example the one-pass answer is too low at most nodes and too high at the corners. The small errors that Kozhaya, Nassif and Najm report on their grids are measured, not proved.

For the variant, each Gauss-Seidel sweep and each coarse correction never increases the energy norm of the error, and Gauss-Seidel converges for a symmetric positive definite matrix, so the variant converges to the exact drop. Its rate on a given grid is measured, not proved here.

## Complexity

Each row of $P$ has at most 4 nonzeros, and the coarse matrices keep a bounded number of nonzeros per row, so lines L2 and L3 cost $O(N)$ on the fine grid, and each level has about a quarter of the nodes of the one above it. The total over all levels is $O(N)$, plus the direct solve on the coarsest grid with $M$ nodes, $O(M^3)$ by dense elimination and less by a sparse [Cholesky decomposition](/cholesky-decomposition/). The space is $O(N)$ for the matrices and $O(M^2)$ for a dense coarse factor. The code of this page uses dense matrices for clarity, so it is slower than these bounds. A transient run factors the coarse matrix once, when $h$ is fixed, and pays $O(N)$ plus two triangular solves per time step.

## Properties

- **Approximate.** The answer is exact only when the exact drop lies in the range of $P$, as for a uniform line of nodes with loads and pads only at kept nodes, where each dropped node is the mean of its two neighbors.
- **Best in energy, proved.** No vector of the form $P y$ is closer to the exact drop in the energy norm.
- **Low on average, proved.** The load-weighted drop of the answer is at most the exact one. A single node can be too high or too low.
- **Keeps the total current, proved.** The rows of $P$ sum to 1, so the total load is the same on every level.
- **Direct.** There is no iteration and no tolerance to set. The cost is fixed by the grid size and the number of levels.
- **Measured accuracy.** Kozhaya, Nassif and Najm report, for their industrial design C1 in a 0.18 µm process at 1.8 V, a drop error with a mean of $-0.0077\%$ and a standard deviation of $0.0333\%$, and a speedup of 16 to 20 times over their reference solver. These are measurements on their grids.

## Variants and improvements

- **Smoothing and iteration.** Lines L6 to L11 add Gauss-Seidel sweeps and repeated coarse corrections. With several levels this is the V-cycle of the [multigrid method](/multigrid-method/), and it converges to the exact answer, at the cost of several passes.
- **Algebraic coarsening.** [Algebraic multigrid](/algebraic-multigrid/) chooses the coarse nodes and the weights from the matrix alone, with no mesh. It fits grids with irregular wires, vias between layers and missing segments, where the row and column rule fails.
- **Multigrid as a preconditioner.** One V-cycle per step as a [preconditioner](/preconditioning/) of the [conjugate gradient method](/conjugate-gradient-method/) gives an exact solver whose number of steps grows slowly with the grid size. Many later power grid solvers use this form.
- **Other fast solvers.** The [random walk method](/random-walk-power-grid-analysis/) finds the drop at a few nodes without solving for the rest. [Vectorless verification](/vectorless-power-grid-verification/) bounds the worst drop over a set of possible loads.

## When to use it

Use it for a fast first look at the IR drop of a large, regular mesh, in early design or inside a loop that tries many grid sizes, where an error of a few percent of the drop is fine. Use a direct sparse solver or a preconditioned iterative solver for sign-off, and add the smoothing of the variant when the point loads matter.

## Pitfalls

- **Loads at dropped nodes.** Line L3 spreads the load of a dropped node over its kept neighbors, and line L5 cannot bring back the local peak. In the example the error is worst at the loaded C nodes. Keep nodes with large loads in the coarse grid, or smooth.
- **Irregular grids.** The rule of every other row and column assumes a full mesh. A missing wire or a via stack breaks it, and a node can end up with no kept neighbor. The code falls back to equal weights when the weights sum to 0, which is not a physical choice.
- **A part with no pad.** Then $A$ is singular, and so is $A_c$. Check that every connected part of the grid reaches a pad.
- **Taking the energy bound for a node bound.** The proofs bound an average error. The worst node, which is what sign-off needs, can be off by much more.

## Implementations

## History

Power grids grew to millions of nodes around 2000, and direct solvers ran out of memory. Kozhaya, Nassif and Najm (2001, 2002) borrowed the coarse grid and the interpolation of geometric multigrid, used one coarse solve without the smoothing loop, and showed small errors on industrial grids, both for DC and for transient analysis. Other fast methods followed within two years: the random walk solver of Qian, Nassif and Sapatnekar (2003), the vectorless bounds of Kouroussis and Najm (2003), and algebraic multigrid and preconditioned solvers for grids with irregular structure.

## References
