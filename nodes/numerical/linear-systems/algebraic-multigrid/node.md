---
tag: EZNBXD
kind: algorithm
slug: algebraic-multigrid
name: Algebraic multigrid
aliases:
- AMG
- classical AMG
- Ruge-Stüben AMG
area: numerical/linear-systems
level: research
summary: Multigrid that builds its coarse levels from the matrix alone, with no grid geometry.
model: floating-point-model
complexity:
  vars: {n: the order of A, z: the number of nonzeros of A, c: the operator complexity, ν: the number of smoothing sweeps per level}
  time: {per_cycle: O(ν c z)}
  space: {extra: O(c z)}
properties: {deterministic: true, in_place: false, recursive: true, iterative: true}
prereqs: [multigrid-method, gauss-seidel-method, positive-definite-matrix, sparse-matrix]
see_also: [multigrid-method, preconditioning, conjugate-gradient-method, domain-decomposition, poisson-equation, galerkin-method, laplacian-matrix, maximal-independent-set]
sources:
  - paper: "A. Brandt, S. F. McCormick and J. W. Ruge, Algebraic multigrid (AMG) for sparse matrix equations, in D. J. Evans (ed.), Sparsity and its Applications, Cambridge University Press, 1984"
    title: Algebraic multigrid (AMG) for sparse matrix equations
    locator: pp. 257 to 284
  - paper: "J. W. Ruge and K. Stüben, Algebraic multigrid, in S. F. McCormick (ed.), Multigrid Methods, Frontiers in Applied Mathematics 3, SIAM, 1987"
    title: Algebraic multigrid
    locator: pp. 73 to 130 (strength of connection, the C/F splitting heuristics, direct and standard interpolation, two-level theory for M-matrices)
  - paper: doi:10.1016/S0377-0427(00)00516-1
    title: K. Stüben, A review of algebraic multigrid, Journal of Computational and Applied Mathematics 128(1-2), 2001
    locator: pp. 281 to 309
  - book: isbn:9780898714623
    title: William L. Briggs, Van Emden Henson and Steve F. McCormick, A Multigrid Tutorial, second edition, SIAM, 2000
    locator: Chapter 8, Algebraic Multigrid (AMG)
  - book: isbn:9780127010700
    title: U. Trottenberg, C. W. Oosterlee and A. Schüller, Multigrid, Academic Press, 2001
    locator: Appendix A, An Introduction to Algebraic Multigrid, by K. Stüben (variational principle, smoothing property, interpolation and two-level convergence)
  - paper: doi:10.1017/S0962492917000083
    title: Jinchao Xu and Ludmil Zikatanov, Algebraic multigrid methods, Acta Numerica 26, 2017
    locator: pp. 591 to 721 (the convergence identity for symmetric multilevel methods)
  - paper: doi:10.1007/BF02238511
    title: P. Vaněk, J. Mandel and M. Brezina, Algebraic multigrid by smoothed aggregation for second and fourth order elliptic problems, Computing 56(3), 1996
    locator: pp. 179 to 196
  - paper: doi:10.1016/S0168-9274(01)00115-5
    title: Van Emden Henson and Ulrike Meier Yang, BoomerAMG, a parallel algebraic multigrid solver and preconditioner, Applied Numerical Mathematics 41(1), 2002
    locator: pp. 155 to 177
---

Algebraic multigrid solves a sparse linear system $A x = b$ the way [geometric multigrid](/multigrid-method/) does, by combining a cheap smoother, which removes the oscillatory part of the error, with a correction computed on a smaller problem, which removes the smooth part. The difference is that the coarse problems are built from the entries of $A$ alone. A setup phase decides which unknowns are strongly coupled, picks a subset $C$ of them as coarse unknowns, builds an interpolation $P$ from the coarse unknowns to all of them, and forms the coarse matrix $A_c = P^T A P$; this repeats until the problem is tiny. The solve phase is then the ordinary V-cycle. For symmetric positive definite $A$ with a convergent smoother the V-cycle always reduces the error in the energy norm (proved), and for the M-matrices of elliptic problems the reduction per cycle is typically a constant like $0.1$ to $0.2$ independent of the size, at a cost of $O(z)$ per cycle. That makes it a black-box solver of optimal complexity for unstructured meshes, where no grid hierarchy is at hand.

## In plain words

Simple iterations, such as sweeping through the equations and fixing each unknown in turn, quickly remove errors that zigzag between neighbouring unknowns, but are very slow on errors that vary smoothly over the whole problem. Multigrid fixes the smooth errors on a smaller version of the problem, where they look rough again. Algebraic multigrid builds that smaller version by reading the matrix: unknowns that strongly influence each other are grouped, a few representatives are kept, and the rest are filled in from their representatives. Repeating this gives a ladder of ever smaller problems, and one trip down and up the ladder costs about as much as a few sweeps.

## The problem

Solve $A x = b$ for $A \in \mathbb{R}^{n \times n}$ sparse, symmetric positive definite, typically an M-matrix or close to one (positive diagonal, nonpositive off-diagonals), such as a finite element or finite difference discretization of an elliptic equation on an arbitrary mesh, or a graph [Laplacian](/laplacian-matrix/).

**Notation.** $A_0 = A$, $A_l \in \mathbb{R}^{n_l \times n_l}$ the level $l$ matrix with $z_l$ nonzeros, $P_l \in \mathbb{R}^{n_l \times n_{l+1}}$ the interpolation, $A_{l+1} = P_l^T A_l P_l$. $x$ is the exact solution, $\hat x$ an iterate, $e = x - \hat x$ the error, $r = b - A \hat x$ the residual, $\|e\|_A = (e^T A e)^{1/2}$ the energy norm. $S_i = \{ j \ne i : -a_{ij} \ge \theta \max_{k \ne i} (-a_{ik}) \}$ is the set on which $i$ strongly depends, with threshold $\theta$ (here $0.25$). The operator complexity is $c = \sum_l z_l / z_0$ and the grid complexity $\sum_l n_l / n_0$. $\nu = \nu_1 + \nu_2$ is the number of Gauss-Seidel sweeps per level, here $1 + 1$. $u = 2^{-53}$.

## The algorithm

```pseudo id=main
AMG-VCYCLE(l, b, x)
L1  if l is the coarsest level then
L2      return A_l⁻¹ b by dense LU with partial pivoting
L3  x ← ν₁ forward Gauss-Seidel sweeps on A_l x = b, starting from x
L4  r ← b − A_l x
L5  r_c ← P_lᵀ r                                   (restriction)
L6  e_c ← AMG-VCYCLE(l + 1, r_c, 0)
L7  x ← x + P_l e_c                               (coarse correction)
L8  x ← ν₂ backward Gauss-Seidel sweeps on A_l x = b
L9  return x
AMG-SETUP(A, θ)
L10 A_0 ← A; l ← 0; while n_l is larger than the coarsest size do
L11     S ← the strong dependences S_i of A_l with threshold θ
L12     split the unknowns into C and F: pick a C point of largest weight λ_i = |{ j : i ∈ S_j }|, make the undecided points that depend on it F, raise λ of the points they depend on, repeat; then add C points so that strongly connected F points share a C point
L13     P_l ← identity on C; for i ∈ F, w_ij = −α_i a_ij / a_ii for j ∈ C ∩ S_i, with α_i = (Σ_{k≠i} a_ik⁻) / (Σ_{j∈C∩S_i} a_ij)
L14     A_{l+1} ← P_lᵀ A_l P_l; l ← l + 1
L15 return A_0, …, A_l and P_0, …, P_{l−1}
```

Line L12 is the Ruge-Stüben first pass, a greedy heuristic for a maximal set of C points that are not strongly dependent on each other, followed by the second pass that guarantees each F point can interpolate from the C points it depends on. Line L13 is direct interpolation: positive off-diagonal entries are added to the diagonal ($a_{ik}^-$ keeps only the negative entries), and the scaling $\alpha_i$ makes the weights of row $i$ sum to $-\sum_{k \ne i} a_{ik}^- / a_{ii}$, which is $1$ when row $i$ has zero sum. The stand-alone solver repeats AMG-VCYCLE on level $0$ until $\|r\|_2 \le \mathrm{tol}\, \|b\|_2$; as a [preconditioner](/preconditioning/) one V-cycle from $x = 0$ is applied to each residual inside [conjugate gradients](/conjugate-gradient-method/).

## Example

Take the 1D Laplacian $A = \operatorname{tridiag}(-1, 2, -1)$ of order $7$ and $b = e$, with solution $x_i = i(8 - i)/2 = (\frac72, 6, \frac{15}2, 8, \frac{15}2, 6, \frac72)$. Each point strongly depends on both neighbours. The weights are $\lambda = (1, 2, 2, 2, 2, 2, 1)$; point $2$ becomes C, so $1$ and $3$ become F and $\lambda_4$ rises to $3$; then $4$ is chosen, $5$ becomes F, then $6$, and $7$ becomes F. So $C = \{2, 4, 6\}$, the usual coarse grid, found from the matrix alone. Direct interpolation gives $w = \frac12$ from each C neighbour (and $\alpha_1 = \alpha_7 = 1$ with a single C neighbour, weight $\frac12$, since those rows do not have zero sum). Then
$$ A_1 = P^T A P = \begin{pmatrix} 1 & -\frac12 & 0 \\ -\frac12 & 1 & -\frac12 \\ 0 & -\frac12 & 1 \end{pmatrix}, $$
half the 1D Laplacian on the coarse grid. With the coarsest size set to $3$ there are two levels. One V-cycle from $\hat x = 0$:

| step | result |
|---|---|
| forward Gauss-Seidel | $\hat x = (\frac12, \frac34, \frac78, \frac{15}{16}, \frac{31}{32}, \frac{63}{64}, \frac{127}{128})$ |
| residual | $r = (\frac34, \frac78, \frac{15}{16}, \frac{31}{32}, \frac{63}{64}, \frac{127}{128}, 0)$ |
| restriction | $r_c = (\frac{55}{32}, \frac{247}{128}, \frac{95}{64})$ |
| coarse solve | $e_c = (\frac{21}4, \frac{113}{16}, \frac{321}{64})$ |
| correction | $\hat x = (\frac{25}8, 6, \frac{225}{32}, 8, \frac{897}{128}, 6, \frac72)$ |
| backward Gauss-Seidel | $\hat x = (\frac{27601}{8192}, \frac{23505}{4096}, \frac{15057}{2048}, \frac{7889}{1024}, \frac{3777}{512}, \frac{1473}{256}, \frac72)$ |

The energy norm of the error drops by the factor $(1952217/469762048)^{1/2} \approx 0.064$ in this first cycle, and by about $0.15$ per cycle afterwards, all in exact rational arithmetic.

## Correctness

The proofs are in `proofs/correctness.md`. Exact arithmetic, $A$ symmetric positive definite.

1. **The coarse problems are well posed (proved).** $P_l$ contains the identity on the C rows, so it has full column rank, and $A_{l+1} = P_l^T A_l P_l$ is symmetric positive definite.
2. **Coarse correction is an $A$-orthogonal projection (proved).** With an exact coarse solve, the error after line L7 is $(I - P A_c^{-1} P^T A) e$, the $A$-orthogonal projection of $e$ onto the complement of $\operatorname{range}(P)$; it never increases $\|e\|_A$ and removes the part of the error in $\operatorname{range}(P)$ exactly.
3. **Gauss-Seidel contracts (proved).** For symmetric positive definite $A$, one forward sweep satisfies $\|S e\|_A^2 = \|e\|_A^2 - \|D^{1/2} (D + L)^{-1} A e\|_2^2$, so $\|S\|_A < 1$; the backward sweep is its $A$-adjoint.
4. **The V-cycle converges (proved).** By induction over the levels, the error propagation operator $E$ of the V-cycle is $A$-self-adjoint with $\|E\|_A \le \|S\|_A^2 < 1$. So the stand-alone iteration converges for every symmetric positive definite $A$, whatever the splitting and interpolation, and one V-cycle from zero is a symmetric positive definite preconditioner, so conjugate gradients may use it.
5. **Rates independent of the size (proved only in special cases).** The bound of item 4 can be arbitrarily close to $1$. For symmetric M-matrices with direct interpolation, Ruge and Stüben prove a two-level rate depending only on $\theta$ and on how much of each row's couplings is interpolated, not on $n$; Xu and Zikatanov give the exact two-level and multilevel rate in terms of a stability constant of $P$. For the V-cycle, size independence is mostly **observed**.

**Observed in the tests.** For the 5-point Laplacian on $k \times k$ grids, $k = 8, 16, 32$ (and $48$ in a separate run), every hierarchy has operator complexity about $2.2$ and grid complexity about $1.7$, the residual reduction per cycle settles at $0.18$ to $0.19$, and $11$ V-cycles reach $\|r\|_2 \le 10^{-8} \|b\|_2$ for every size, against $7$ iterations of AMG-preconditioned CG. For the anisotropic problem $-\epsilon u_{xx} - u_{yy}$ with $\epsilon = 10^{-3}$ or $10^{-2}$, strength of connection coarsens only along the strong direction (the first coarse level has exactly half the points) and $11$ or $12$ cycles suffice; geometric multigrid with standard coarsening and point smoothing would need line smoothers here. On $500$ random diagonally dominant matrices the energy norm contraction of one V-cycle is always below $1$, the worst observed being below $0.9$.

**Floating point.** The smoother, residual, restriction and prolongation are sums of products with $O(z_l / n_l)$ terms per row, so each cycle introduces relative errors of order $u$ times the size of the iterate; the attainable residual is about $u \|A\| \|\hat x\|$, as for any stationary iteration, and the tests reach $10^{-8}$ without trouble. The coarsest solve uses partial pivoting and reports a singular or numerically singular coarsest matrix. AMG does not change the conditioning of the problem: the forward error is still bounded by $\kappa(A)$ times the backward error.

## Complexity

The proofs are in `proofs/complexity.md`.

- **Per V-cycle: $O(\nu c z)$ time (proved),** assuming the coarsest level has a bounded size. On level $l$ each Gauss-Seidel sweep costs $2 z_l - n_l$ flops, the residual $2 z_l$, restriction and prolongation $2 \operatorname{nnz}(P_l)$ each, and $\operatorname{nnz}(P_l) \le n_l + z_l$ because each F row uses only entries of its own row. Summing gives at most $(2\nu + 10) \sum_l z_l = (2\nu + 10)\, c z$ flops; with $\nu = 2$ and $c \approx 2.2$ that is about $30 z$, the price of $15$ sweeps.
- **Storage: $O(c z)$ (proved)** for the matrices and interpolations of all levels, plus $O(\sum_l n_l)$ for vectors.
- **Number of cycles.** $O(\log(1/\varepsilon))$ with a size independent rate when the method works well (observed); no general bound beyond item 4.
- **Setup.** Strength and interpolation are $O(z_l)$ per level, the splitting $O(z_l + n_l \log n_l)$ with a heap, and the Galerkin product costs $\sum_i \sum_{j \in \text{row } i} \operatorname{nnz}(P_j)$ multiplications, which is $O(z_l)$ only if the rows of $P$ have bounded length. The setup typically costs a few V-cycles; on 3D problems the coarse matrices can become dense ($c$ grows), which is the main motivation for aggressive coarsening and for truncating $P$.
- **Memory traffic.** Everything is sparse matrix-vector work with $O(1)$ flops per nonzero loaded, so on modern hardware the speed of a cycle is set by memory bandwidth, about $c$ passes over the matrix per sweep, not by the flop count.

## Properties

- **Black box**: only the matrix is needed, no grid, coordinates or geometry.
- **Optimal on its home ground**: $O(z)$ work per digit of accuracy for scalar elliptic M-matrix problems on unstructured meshes, with size independent iteration counts (observed).
- **Symmetric**: with symmetric smoothing and $R = P^T$ the V-cycle is a symmetric positive definite preconditioner (proved).
- **Adapts to anisotropy and coefficient jumps**, because strength of connection follows the matrix entries, not the mesh.
- **Not in place**: the hierarchy costs $c - 1$ times the storage of $A$ in addition.

## Variants and improvements

- **Smoothed aggregation** (Vaněk, Mandel and Brezina 1996). Coarse unknowns are aggregates of strongly connected points, the tentative piecewise constant interpolation is smoothed by one Jacobi step, and near null space vectors (rigid body modes) can be built in, which makes it the method of choice for elasticity. Used in ML and MueLu.
- **Standard, extended and multipass interpolation.** Interpolate also through strongly connected F points (Ruge and Stüben's standard interpolation, de Sterck, Falgout and others' extended interpolation) for better rates when the coarsening is aggressive.
- **Parallel coarsening.** The sequential greedy splitting is replaced by CLJP, Falgout, PMIS or HMIS coarsening, based on [maximal independent sets](/maximal-independent-set/) (Henson and Yang's BoomerAMG in hypre).
- **Aggressive coarsening and truncation.** Coarsen twice as fast and drop small interpolation weights to keep $c$ near $1.5$ on 3D problems.
- **Adaptive and bootstrap AMG.** Compute the smooth error from the matrix by relaxation on $A e = 0$ and fit the interpolation to it, for systems where the near null space is not the constant vector.
- **AMG for nonsymmetric and indefinite systems.** Use $R \ne P^T$ (Petrov-Galerkin) or apply AMG to a related positive definite matrix as a [preconditioner](/preconditioning/) inside GMRES; convergence theory is then much weaker.
- **Lean AMG for graph Laplacians.** Combinatorial coarsening based on low degree elimination and aggregation, related to the nearly linear Laplacian solvers.

## When to use it

Use it as a solver or, more often, as a preconditioner for conjugate gradients on large symmetric positive definite systems from scalar elliptic equations (diffusion, pressure Poisson equations in flow solvers, electrostatics, groundwater flow) on unstructured or adaptive meshes, where geometric multigrid would need a mesh hierarchy that does not exist, and where sparse direct factorization costs too much memory, typically in 3D. Prefer geometric multigrid on structured grids, where it is cheaper; prefer a sparse direct solver for moderate 2D problems or many right-hand sides; and prefer smoothed aggregation or system AMG for elasticity and other vector problems.

## Pitfalls

- **Positive off-diagonals and non-M-matrices.** Classical strength of connection looks at negative entries only, so a matrix with large positive couplings (higher order elements, the Hilbert matrix of the tests) may not coarsen at all, and AMG degenerates to a dense coarse solve or to plain Gauss-Seidel.
- **Systems of PDEs.** Treating the unknowns of elasticity or Stokes as one scalar problem couples displacement components incorrectly; use the unknown-based or nodal variants or smoothed aggregation with rigid body modes.
- **Indefinite problems.** For Helmholtz-type matrices the smoother amplifies some error components and the V-cycle can diverge; the tests check that a shifted Laplacian is reported as not converged.
- **Singular problems.** For a pure Neumann problem the coarsest matrix inherits the null space and is singular; the implementation raises an error, and a real code must project out the constant or fix one unknown.
- **Operator complexity blowup.** Galerkin products on 3D problems can make coarse matrices nearly dense; watch $c$ and use aggressive coarsening or truncation.
- **Nonsymmetric smoothing inside CG.** A V-cycle with forward Gauss-Seidel both before and after is not symmetric, and conjugate gradients may break down; use forward then backward sweeps, or symmetric Jacobi type smoothers.

## Implementations

## History

Multigrid was developed for grids by Fedorenko, Bakhvalov and Brandt in the 1960s and 1970s. Brandt, McCormick and Ruge (1982 to 1984) proposed building the hierarchy from the matrix itself, with Galerkin coarse operators and the strength of connection idea, and Ruge and Stüben's 1987 chapter fixed the classical algorithm and its two-level theory for M-matrices; their code AMG1R5 was the first general AMG solver. Smoothed aggregation followed in 1996 for elasticity. In the 2000s parallel coarsening made AMG scale to hundreds of thousands of processors in hypre's BoomerAMG, and AMG became the default preconditioner for elliptic problems in many simulation codes. Xu and Zikatanov's 2017 survey unified the theory around the abstract convergence identity.

## References
