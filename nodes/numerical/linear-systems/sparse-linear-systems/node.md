---
tag: J015T6
kind: problem
slug: sparse-linear-systems
name: Sparse linear systems
aliases:
- sparse linear system
- large sparse linear systems
area: numerical/linear-systems
level: core
summary: Solving systems of linear equations whose coefficient matrices have mostly zero entries, using methods that exploit sparsity to save time and memory.
model: floating-point-model
complexity:
  vars: {n: "the order of A", m: "the number of nonzeros of A"}
  time: {worst: Θ(n^3)}
prereqs: [sparse-matrix, linear-system-solving]
see_also: [fill-reducing-ordering, nested-dissection, multifrontal-method, cholesky-decomposition, conjugate-gradient-method, gmres, multigrid-method, preconditioning]
sources:
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 1, Introduction; Chapter 4, Cholesky factorization; Chapter 6, LU factorization; Chapter 7, Fill-reducing orderings
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 3, Sparse Matrices; Chapters 6 and 7, Krylov subspace methods; Chapters 9 and 10, preconditioning
  - paper: doi:10.1017/S0962492916000076
    title: Timothy A. Davis, Sivasankaran Rajamanickam and Wissam M. Sid-Lakhdar, A survey of direct methods for sparse linear systems, Acta Numerica 25, 2016
    locator: the survey of orderings, symbolic analysis, supernodal and multifrontal factorization and their software
  - paper: doi:10.1137/0710032
    title: Alan George, Nested dissection of a regular finite element mesh, SIAM Journal on Numerical Analysis 10(2), 1973
    locator: the O(n^(3/2)) operation count and O(n log n) fill for the k by k grid
  - paper: doi:10.1137/0602010
    title: Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 1981
    locator: the NP-completeness of choosing an elimination order with least fill
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (the backward error bound, which holds for every symmetric ordering)
---

A sparse linear system is $A x = b$ with $A \in \mathbb{R}^{n \times n}$ nonsingular and only $m \ll n^2$ nonzero entries, typically $m = O(n)$, and $n$ from thousands to billions. Dense [Gaussian elimination](/linear-system-solving/) would need $\tfrac23 n^3$ flops and $n^2$ words, so the methods instead exploit the [sparse matrix](/sparse-matrix/) structure: sparse direct factorizations that reorder $A$ to limit [fill-in](/fill-in/), and iterative methods that touch $A$ only through products $A v$. On the 2D model problem the best direct methods take $\Theta(n^{3/2})$ flops and the best iterative ones, multigrid, take $O(n)$.

## In plain words

In big simulations each unknown, such as the temperature at a point, depends only on a few nearby unknowns, so almost every coefficient in the equations is zero. Solving such systems by the school method would treat all those zeros as numbers and would never finish. Two families do better. Direct methods still eliminate unknowns, but choose a clever order so that few new nonzeros appear. Iterative methods never change the matrix at all: they guess, see how wrong the guess is by multiplying with the matrix, and improve, which needs memory only for a handful of vectors.

## Definition

**Notation.** $A \in \mathbb{R}^{n \times n}$ with $m = \mathrm{nnz}(A)$, $b \in \mathbb{R}^n$, exact solution $x$, computed $\hat x$, residual $r = b - A \hat x$, $\kappa(A) = \|A\|_2 \|A^{-1}\|_2$, $u = 2^{-53}$, $\gamma_n = n u/(1 - n u)$. For a direct method, $P$ and $Q$ are permutations and $L$, $U$ (or $R = L^T$) the factors, with $|L| + |U|$ having $\mathrm{nnz}(L + U)$ entries, the fill being $\mathrm{nnz}(L + U) - m$. For an iterative method, $x_k$, $r_k = b - A x_k$ and $\mathcal{K}_k(A, r_0) = \mathrm{span}\{r_0, A r_0, \ldots, A^{k-1} r_0\}$.

**Input.** $A$ in a sparse format, and $b$.

**Output.** $\hat x$ with a small backward error, $\|r\| \le \varepsilon(\|A\|\|\hat x\| + \|b\|)$ for $\varepsilon$ a modest multiple of $u$ (direct methods), or with $\|r\|_2 \le \mathrm{tol}\cdot\|b\|_2$ for a user tolerance (iterative methods). Then $\|\hat x - x\|/\|x\| \lesssim \kappa(A)$ times the relative backward error.

**Cost model.** Flops (leading term), the number of nonzeros stored, and for iterative methods the number of products with $A$ and with the preconditioner. On current machines a sparse product does about one flop per 6 bytes moved, so for iterative methods and for the sparse parts of direct methods memory traffic, not flops, dominates the time.

## Variants

- **By structure of $A$:** symmetric positive definite (sparse [Cholesky](/cholesky-decomposition/), [conjugate gradients](/conjugate-gradient-method/)); symmetric indefinite ($L D L^T$ with $1 \times 1$ and $2 \times 2$ pivots, [MINRES](/minres/)); unsymmetric (sparse LU with threshold pivoting, [GMRES](/gmres/), [BiCGSTAB](/bicgstab/)).
- **Banded and tridiagonal** systems, solved by band elimination in $O(n w^2)$ flops for half-bandwidth $w$; the [Thomas algorithm](/thomas-algorithm/) is the case $w = 1$.
- **Many right-hand sides** or a sequence of matrices with one pattern: factor once, or reuse the symbolic analysis, which favours direct methods.
- **Sparse least squares** $\min \|A x - b\|_2$ with $A$ rectangular, by sparse QR or by CG on the normal equations.
- **Saddle point (KKT) systems** $\begin{pmatrix} H & B^T \\ B & 0 \end{pmatrix}$ from optimization and incompressible flow, which are indefinite and need special orderings or block preconditioners.

## Examples

**Order matters: the arrow matrix.** Let $A$ have $a_{11} = n$, $a_{ii} = 1$ for $i \ge 2$, and $a_{1i} = a_{i1} = 1$; it is symmetric positive definite with $m = 3n - 2$. Eliminating $x_1$ first creates the Schur complement $I - \tfrac1n \mathbf{1}\mathbf{1}^T$, which is completely full: the Cholesky factor has $n(n+1)/2$ nonzeros and costs about $n^3/3$ flops. Numbering $x_1$ last instead gives a factor with the pattern of the lower triangle of $A$, $2n - 1$ nonzeros, and $O(n)$ flops. The two orderings solve the same system; only the order of elimination differs.

**The 2D model problem.** The 5-point [Poisson](/poisson-equation/) matrix on a $k \times k$ grid has $n = k^2$ and $m \approx 5n$. Known costs to reach discretization accuracy:

| method | flops | storage | status |
|---|---|---|---|
| dense LU | $\tfrac23 n^3$ | $n^2$ | |
| band Cholesky, natural order ($w = k$) | about $n w^2 = n^2$ | $n^{3/2}$ | count to leading order |
| sparse Cholesky, [nested dissection](/nested-dissection/) | $O(n^{3/2})$ | $O(n \log n)$ | proved, optimal for every ordering |
| [Jacobi](/jacobi-method/) or [Gauss-Seidel](/gauss-seidel-method/) | $O(n^2 \log n)$ | $O(n)$ | proved, $O(n \log n)$ sweeps |
| optimal [SOR](/successive-over-relaxation/) | $O(n^{3/2} \log n)$ | $O(n)$ | proved |
| CG, unpreconditioned | $O(n^{3/2} \log n)$ | $O(n)$ | bound proved, $O(\sqrt{\kappa}) = O(k)$ steps per digit |
| [multigrid](/multigrid-method/) | $O(n)$ | $O(n)$ | proved for the model problem |

In 3D on a $k \times k \times k$ grid, $n = k^3$, nested dissection needs $O(n^2)$ flops and $O(n^{4/3})$ fill, which is why iterative methods dominate for large 3D problems.

## Known algorithms

- **Sparse direct methods.** Four phases (Davis, 2006): a fill-reducing ordering ([minimum degree](/minimum-degree-ordering/), [nested dissection](/nested-dissection/), [reverse Cuthill-McKee](/reverse-cuthill-mckee/) for band and profile methods); symbolic analysis with the [elimination tree](/elimination-tree/) and column counts, in time nearly linear in $m$; numeric factorization by left-looking, supernodal or [multifrontal](/multifrontal-method/) methods that run dense kernels on blocks; and triangular solves. Unsymmetric LU must balance sparsity and stability, using threshold partial pivoting, static pivoting with [iterative refinement](/iterative-refinement/), or a fixed ordering of $A^T A$.
- **Krylov subspace methods.** [CG](/conjugate-gradient-method/) for SPD $A$, [MINRES](/minres/) for symmetric indefinite $A$, [GMRES](/gmres/) and [BiCGSTAB](/bicgstab/) for general $A$, each needing one product with $A$ per step plus $O(n)$ work.
- **[Preconditioning](/preconditioning/).** Incomplete factorizations, sparse approximate inverses, [algebraic multigrid](/algebraic-multigrid/) and [domain decomposition](/domain-decomposition/) make the Krylov iteration counts small.
- **Multigrid.** Smoothing plus coarse-grid correction, optimal $O(n)$ for elliptic problems on grids.
- **Stationary iterations.** [Jacobi](/jacobi-method/), [Gauss-Seidel](/gauss-seidel-method/) and [SOR](/successive-over-relaxation/), now used mainly as smoothers and preconditioners.

## Bounds

- **Reading the input.** Every method needs $\Omega(m)$ time; multigrid on the model problem meets it.
- **Minimum fill is hard.** Finding a symmetric ordering with the least fill is NP-complete (Yannakakis, 1981), so practical orderings are heuristics; nested dissection on graphs with good separators comes within known factors of optimal.
- **Grid lower bounds (proved).** For the $k \times k$ grid every ordering gives $\Omega(n \log n)$ fill and $\Omega(n^{3/2})$ flops for Cholesky, so George's nested dissection (1973) is optimal up to constants; Lipton, Rose and Tarjan (1979) extend the upper bounds to all planar graphs.
- **Stability of sparse Cholesky (proved).** For SPD $A$ and any symmetric permutation, if Cholesky runs to completion the computed solution satisfies $(A + \Delta A)\hat x = b$ with $|\Delta A| \le \gamma_{3n+1} |\hat R^T||\hat R|$ (Higham, Chapter 10); the ordering is free to be chosen for sparsity alone. The dimension in $\gamma$ can be replaced by the length of the longest inner product, which is bounded by the largest row count of $R$.
- **Sparse LU (worst case).** Pivoting for sparsity can raise the growth factor; threshold pivoting with parameter $\tau \in (0, 1]$ bounds the multipliers by $1/\tau$, and the backward error is then bounded through the growth factor as in the dense case, with growth observed to be small.
- **Iterative methods (proved, exact arithmetic).** CG satisfies $\|x - x_k\|_A \le 2\big((\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)\big)^k \|x - x_0\|_A$; in floating point the residual of a converged run levels off near $u\,\|A\|\,\|x\|$ times a modest factor (observed and analyzed by Greenbaum).

## Reductions

- **Sparse elimination to graph problems.** Eliminating unknown $v$ joins all its neighbours into a clique in the graph of $A$ (Parter, Rose); fill-in, orderings and the elimination tree are therefore graph computations, and the minimum fill problem is the minimum chordal completion problem.
- **To dense subproblems.** Supernodal and multifrontal methods turn the factorization into a tree of dense factorizations of frontal matrices, so almost all flops run in dense BLAS 3 kernels.
- **Least squares to square systems.** Sparse $\min\|A x - b\|_2$ reduces to the [normal equations](/normal-equations/) $A^T A x = A^T b$, which squares $\kappa$, or to the augmented system $\begin{pmatrix} I & A \\ A^T & 0 \end{pmatrix}\begin{pmatrix} r \\ x \end{pmatrix} = \begin{pmatrix} b \\ 0 \end{pmatrix}$, which keeps it sparse and does not.

## Applications

- Discretized partial differential equations by finite differences, finite elements and finite volumes, the largest source of sparse systems.
- Circuit simulation (very unsymmetric, sparse LU), power networks, and structural analysis.
- Interior point methods for linear and quadratic programming, where each step solves a sparse KKT system.
- Markov chains and PageRank, bundle adjustment in computer vision, and graph Laplacian systems in data analysis.

## References
