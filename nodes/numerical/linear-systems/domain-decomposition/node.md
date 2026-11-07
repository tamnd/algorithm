---
tag: M1A6HZ
kind: technique
slug: domain-decomposition
name: Domain decomposition
aliases:
- Schwarz methods
- additive Schwarz
- substructuring
area: numerical/linear-systems
level: research
summary: Split a problem into overlapping or non-overlapping subdomains solved and coupled iteratively.
prereqs: [preconditioning, schur-complement, conjugate-gradient-method]
see_also: [multigrid-method, algebraic-multigrid, schur-complement, preconditioning, conjugate-gradient-method, gmres, nested-dissection, poisson-equation]
sources:
  - book: isbn:9783540206965
    title: Andrea Toselli and Olof Widlund, Domain Decomposition Methods, Algorithms and Theory, Springer, 2005
    locator: Chapter 2, abstract Schwarz theory (Assumptions 2.2 to 2.4, Theorems 2.7 and 2.9); Chapter 3, two-level overlapping methods (the bound C (1 + H/delta)); Chapters 4 to 6, substructuring, FETI and BDDC
  - book: isbn:9780521495899
    title: Barry Smith, Petter Bjørstad and William Gropp, Domain Decomposition, Parallel Multilevel Methods for Elliptic Partial Differential Equations, Cambridge University Press, 1996
    locator: Chapter 1 (alternating, additive and multiplicative Schwarz); Chapter 5 (convergence theory)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 14, Domain Decomposition Methods (Section 14.3, Schwarz alternating procedures; Section 14.4, Schur complement approaches)
  - book: isbn:9781611974058
    title: Victorita Dolean, Pierre Jolivet and Frédéric Nataf, An Introduction to Domain Decomposition Methods, SIAM, 2015
    locator: Chapter 1 (Schwarz methods and the 1D contraction factor); Chapter 5 (coarse spaces); Chapter 7 (GenEO)
  - paper: "H. A. Schwarz, Über einen Grenzübergang durch alternierendes Verfahren, Vierteljahrsschrift der Naturforschenden Gesellschaft in Zürich 15, 1870"
    title: Über einen Grenzübergang durch alternierendes Verfahren
    locator: pp. 272 to 286 (the alternating method on a disk and a rectangle)
  - paper: "Xiao-Chuan Cai and Marcus Sarkis, A restricted additive Schwarz preconditioner for general sparse linear systems, SIAM Journal on Scientific Computing 21(2), 1999"
    title: A restricted additive Schwarz preconditioner for general sparse linear systems
    locator: pp. 792 to 797
  - paper: "Martin J. Gander, Optimized Schwarz methods, SIAM Journal on Numerical Analysis 44(2), 2006"
    title: Optimized Schwarz methods
    locator: pp. 699 to 731 (Robin transmission conditions)
---

Domain decomposition solves a large linear system $A x = b$, usually from an elliptic PDE, by splitting the unknowns into subdomains, solving the smaller subdomain problems independently, and coupling them by an outer iteration. In the overlapping (Schwarz) form, the preconditioner is $M^{-1} = \sum_i R_i^T A_i^{-1} R_i$, where $R_i$ restricts to subdomain $i$ and $A_i = R_i A R_i^T$. In the non-overlapping (substructuring) form, the interior unknowns are eliminated and the iteration runs on the [Schur complement](/schur-complement/) of the interfaces. With one level only, the condition number grows like $1/(H \delta)$ for subdomain size $H$ and overlap $\delta$, so the iteration count grows with the number of subdomains. Adding a coarse problem, as in [multigrid](/multigrid-method/), gives the proved bound $\kappa \le C(1 + H/\delta)$, independent of the mesh size and of the number of subdomains. That scalability, and the fact that each subdomain maps to one processor, make it the standard framework for parallel PDE solvers.

## In plain words

A big problem on a big region is hard to solve at once. Cut the region into pieces, give each piece to a different worker, and let each solve its own small problem using guesses for what happens at its edges. Then let neighbours exchange their answers along the edges and solve again. If the pieces overlap a little, the guesses improve each round. With many pieces, information travels slowly from one side to the other, so a small, coarse version of the whole problem is also solved each round to spread it quickly.

## When it applies

The technique applies to a sparse symmetric positive definite or nearly so system whose unknowns have a natural notion of locality, typically a finite element or [finite difference](/finite-difference-method/) discretization of an elliptic PDE such as the [Poisson equation](/poisson-equation/). It needs a partition of the unknowns (from a mesh partitioner or a [graph partitioning](/graph-partitioning-problem/) of $G(A)$), a solver for each subdomain matrix, and an outer Krylov method, usually [CG](/conjugate-gradient-method/) for symmetric $A$ and [GMRES](/gmres/) otherwise.

**Notation.** $A \in \mathbb{R}^{n \times n}$ SPD, $x_k$ and $r_k = b - A x_k$ the iterates and residuals. Subdomains are index sets $\Omega_1, \ldots, \Omega_N$ covering $\{1, \ldots, n\}$, possibly overlapping; $R_i \in \{0, 1\}^{n_i \times n}$ selects the rows in $\Omega_i$; $A_i = R_i A R_i^T$. A coarse space is given by $R_0^T \in \mathbb{R}^{n \times n_0}$ with $A_0 = R_0 A R_0^T$. For a PDE, $h$ is the mesh size, $H$ the subdomain diameter, and $\delta$ the width of the overlap. $\kappa(M^{-1} A)$ is the ratio of the extreme eigenvalues of the preconditioned operator, and the iteration matrix of a stationary method is $T = I - M^{-1} A$ with [spectral radius](/spectral-radius/) $\rho(T)$.

## The template

```pseudo id=main
SCHWARZ-PRECONDITIONER(r)                               ▷ returns z ≈ A⁻¹ r
L1  z ← 0
L2  if TWO-LEVEL then z ← R₀ᵀ A₀⁻¹ R₀ r                 ▷ hole: the coarse space R₀
L3  for i ← 1 to N do                                   ▷ in parallel for the additive form
L4      if MULTIPLICATIVE then rᵢ ← Rᵢ (r − A z) else rᵢ ← Rᵢ r
L5      zᵢ ← SOLVE(Aᵢ, rᵢ)                               ▷ hole: exact or inexact local solver
L6      z ← z + R̃ᵢᵀ zᵢ                                  ▷ hole: R̃ᵢ = Rᵢ, or a partition of unity (RAS)
L7  return z
OUTER(A, b)
L8  run CG (symmetric M) or GMRES with SCHWARZ-PRECONDITIONER, until ‖r_k‖ ≤ tol ‖b‖
```

The holes are the overlap of the $\Omega_i$, the coarse space $R_0$, the local solver at line L5, and the prolongation $\tilde R_i$ at line L6. With $\tilde R_i = R_i$ and the additive form, $M^{-1} = \sum_{i=0}^{N} R_i^T A_i^{-1} R_i$ is symmetric positive definite and CG applies. Restricted additive Schwarz (RAS, Cai and Sarkis 1999) uses $\tilde R_i$ that zeros the overlap, so each unknown is updated by only one subdomain; this is cheaper in communication and usually converges faster, but $M$ is not symmetric. The multiplicative form is a block [Gauss-Seidel](/gauss-seidel-method/) sweep over overlapping blocks, and as a stationary iteration it is Schwarz's alternating method.

**Why it works (proved, abstract Schwarz theory).** Write $P_i = R_i^T A_i^{-1} R_i A$, the $A$-orthogonal projection onto the range of $R_i^T$. Then $M^{-1} A = \sum_i P_i$. Suppose (i) every $v$ has a decomposition $v = \sum_{i=0}^N R_i^T v_i$ with $\sum_i v_i^T A_i v_i \le C_0^2\, v^T A v$ (stable decomposition), and (ii) each point lies in at most $N_c$ of the overlapping subdomains (finite covering). Then

$$C_0^{-2}\, v^T A v \le v^T A M^{-1} A v \le (N_c + 1)\, v^T A v,$$

so $\kappa(M^{-1} A) \le (N_c + 1) C_0^2$ (Toselli and Widlund, Theorem 2.7). For a second order elliptic PDE with a shape regular mesh and a coarse space from a coarse mesh of size $H$, one shows $C_0^2 \le C(1 + H/\delta)$ with $C$ independent of $h$, $H$ and $\delta$ (Dryja and Widlund; Toselli and Widlund, Theorem 3.13). Without the coarse space the best constant is $C_0^2 \approx C (1 + 1/(H \delta))$.

**Cost.** Per application: one solve with each $A_i$ (for sparse direct local solvers, the factorization is done once), one coarse solve, and one exchange of overlap data with neighbours. CG then needs $O(\sqrt{\kappa})$ iterations, so with a coarse space and fixed $H/\delta$ the iteration count is bounded independently of $n$ and $N$. On large machines the cost is dominated by communication and by the coarse solve, not by flops.

## Classic examples

**Two overlapping intervals.** Solve $-u'' = f$ on $(0, 1)$ with $u(0) = u(1) = 0$, by finite differences with $9$ interior points ($h = 1/10$). Take $\Omega_1 = \{1, \ldots, 6\}$ and $\Omega_2 = \{4, \ldots, 9\}$. The error is discrete harmonic, hence linear, in each subdomain, so one alternating sweep multiplies the error at the interface point $x_7$ by

$$\rho = \frac{\alpha (1 - \beta)}{\beta (1 - \alpha)}, \qquad \alpha = x_3 = 0.3, \quad \beta = x_7 = 0.7,$$

which gives $\rho = 9/49 \approx 0.18$. In exact arithmetic the interface errors are $9/49, (9/49)^2, (9/49)^3, \ldots$ when the initial error is $1$ at every point. With $\alpha = \beta$ (no overlap) $\rho = 1$ and the method stagnates; with a small overlap $\beta - \alpha = \delta$, $\rho \approx 1 - c\,\delta$, so convergence slows as the overlap shrinks.

**Many subdomains without a coarse space.** On the unit square with $N = H^{-2}$ subdomains in a row by row layout, the error from a source in one corner must cross about $1/H$ subdomains, one per iteration, so a one-level method needs at least $O(1/H)$ iterations; the bound $\kappa \lesssim 1/(H \delta)$ is attained up to constants. Adding the coarse space of piecewise linear functions on the subdomain mesh removes this growth.

**Non-overlapping substructuring.** Order the unknowns as interiors $I$ of all subdomains and interface $\Gamma$. Eliminating $I$, which is block diagonal and solved in parallel, leaves $S x_\Gamma = g$ with $S = A_{\Gamma\Gamma} - A_{\Gamma I} A_{II}^{-1} A_{I\Gamma}$. For second order elliptic problems $\kappa(A) = O(h^{-2})$ but $\kappa(S) = O(H^{-1} h^{-1})$. Neumann-Neumann, BDDC and FETI-DP preconditioners for $S$ reach $\kappa \le C (1 + \log(H/h))^2$ (proved, Mandel, Dohrmann and Tezaur 2005; Klawonn and Widlund), so the iteration count grows only logarithmically.

**Nested dissection as a direct analogue.** A [nested dissection](/nested-dissection/) ordering is a recursive non-overlapping decomposition solved exactly: interiors first, separators last.

## Variations

- **Optimized Schwarz.** Replace the Dirichlet transmission condition by a Robin condition $\partial_n u + p u$ with an optimized $p$. Without overlap this converges with rate $1 - O(h^{1/2})$ instead of stagnating (Gander 2006).
- **Spectral coarse spaces.** For highly heterogeneous coefficients the constant $C$ depends on the contrast. GenEO and related methods add local generalized eigenvectors to the coarse space and restore a bound independent of the contrast (Dolean, Jolivet and Nataf, Chapter 7).
- **Algebraic partitions.** Without a mesh, use a partition of $G(A)$ and grow the overlap by graph distance. PETSc's `PCASM` and `PCGASM` do this.
- **Inexact local solves.** Replace $A_i^{-1}$ by an [incomplete factorization](/incomplete-lu-factorization/) or a multigrid cycle; the abstract theory carries over with a constant that measures the local approximation.
- **Space-time and nonlinear decomposition.** Parareal decomposes in time; nonlinear preconditioners such as ASPIN apply the idea to Newton's method.

## Pitfalls

- **Additive Schwarz as a stationary iteration.** $x_{k+1} = x_k + M^{-1} r_k$ with $M^{-1} = \sum_i R_i^T A_i^{-1} R_i$ can diverge, because overlapping corrections are added twice: $\lambda_{\max}(M^{-1} A)$ can be as large as $N_c + 1$. Use it as a preconditioner for CG, or damp it.
- **No coarse space.** One-level methods do not scale: iteration counts grow with the number of subdomains. Weak scaling studies show this immediately.
- **RAS with CG.** The restricted variant is not symmetric; CG may fail or stagnate. Use GMRES or the symmetric form.
- **Too small an overlap.** With minimal overlap ($\delta = h$) the bound becomes $C(1 + H/h)$, which grows under mesh refinement at fixed $H$.
- **Heterogeneous coefficients.** The constants in the bounds depend on the coefficient contrast unless the subdomains are aligned with the jumps or a spectral coarse space is used.
- **Coarse solve bottleneck.** The coarse problem has size proportional to $N$ and is solved by every process or a subset; for tens of thousands of subdomains it needs its own parallel solver or a third level.

## Exercises

1. Derive the 1D contraction factor $\rho = \alpha(1 - \beta)/(\beta(1 - \alpha))$ for the alternating method on $(0, \beta)$ and $(\alpha, 1)$, and show it is less than $1$ exactly when $\alpha < \beta$.
2. Show that $P_i = R_i^T A_i^{-1} R_i A$ is an $A$-orthogonal projection, and that $\sum_i P_i$ is $A$-symmetric.
3. Prove the upper bound $\lambda_{\max}(M^{-1} A) \le N_c + 1$ from the finite covering assumption and the strengthened Cauchy-Schwarz inequality.
4. Show that the multiplicative Schwarz method with two non-overlapping blocks is block Gauss-Seidel and that its error propagation operator is $(I - P_2)(I - P_1)$.
5. For the 1D example, compute the condition number of the one-level additive Schwarz preconditioned matrix for $N = 2, 4, 8$ equal subdomains with overlap $2$, and observe its growth.
6. Show that if $A$ is ordered as interiors then interface, the Schur complement $S$ is SPD whenever $A$ is.

## References
