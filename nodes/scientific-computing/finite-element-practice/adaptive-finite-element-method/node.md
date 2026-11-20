---
tag: ZK2C1A
kind: algorithm
slug: adaptive-finite-element-method
name: Adaptive finite element method
aliases:
- AFEM
- solve-estimate-mark-refine loop
area: scientific-computing/finite-element-practice
level: core
summary: Repeats solve, estimate, mark and refine, so the mesh concentrates where the error indicator is large.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {M: the number of triangles of the final mesh, k: the number of steps, S: the total cost of the k linear solves}
  time: {average: "O(k M log M + S)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, nested_spaces: true, contraction_with_dorfler_marking: true, error_never_increases: true}
history:
  year: 1978
  people: [Ivo Babuska, Werner C. Rheinboldt, Willy Dorfler, Peter Binev, Wolfgang Dahmen, Ronald DeVore, Rob Stevenson, J. Manuel Cascon, Christian Kreuzer, Ricardo H. Nochetto, Kunibert G. Siebert]
  note: Babuska and Rheinboldt started a posteriori error estimation and adaptive refinement in 1978. Dorfler proved the first convergence result in 1996, and the papers of 2004 to 2008 proved optimal rates.
prereqs: [finite-element-method, residual-error-estimator, newest-vertex-bisection]
see_also: [dorfler-marking, afem-optimality-theorem, zienkiewicz-zhu-estimator, dual-weighted-residual-method, hp-finite-element-method, adaptive-mesh-refinement, berger-colella-amr, anisotropic-mesh-adaptation]
sources:
  - paper: doi:10.1137/0733054
    title: Willy Dorfler, A convergent adaptive algorithm for Poisson's equation, SIAM Journal on Numerical Analysis 33(3) (1996) 1106-1124
    locator: the bulk marking criterion and the first proof that the adaptive loop converges
  - paper: doi:10.1137/S0036142999360044
    title: Pedro Morin, Ricardo H. Nochetto and Kunibert G. Siebert, Data oscillation and convergence of adaptive FEM, SIAM Journal on Numerical Analysis 38(2) (2000) 466-488
    locator: convergence with oscillation marking and the interior node property
  - paper: doi:10.1137/07069047X
    title: J. Manuel Cascon, Christian Kreuzer, Ricardo H. Nochetto and Kunibert G. Siebert, Quasi-optimal convergence rate for an adaptive finite element method, SIAM Journal on Numerical Analysis 46(5) (2008) 2524-2550
    locator: the contraction of the error plus the scaled estimator, and the optimal rate
  - paper: doi:10.1007/978-3-642-03413-8_12
    title: "Ricardo H. Nochetto, Kunibert G. Siebert and Andreas Veeser, Theory of adaptive finite element methods: an introduction, in Multiscale, Nonlinear and Adaptive Approximation, Springer, 2009, 409-542"
    locator: the full theory of the loop for the model problem, with proofs
  - paper: doi:10.2478/cmam-2011-0026
    title: Stefan Funken, Dirk Praetorius and Philipp Wissgott, Efficient implementation of adaptive P1-FEM in Matlab, Computational Methods in Applied Mathematics 11(4) (2011) 460-490
    locator: the P1 solver, the residual estimator and the refinement in vectorized form
  - paper: doi:10.1016/j.camwa.2013.12.003
    title: Carsten Carstensen, Michael Feischl, Marcus Page and Dirk Praetorius, Axioms of adaptivity, Computers and Mathematics with Applications 67(6) (2014) 1195-1253
    locator: the four axioms (stability, reduction, discrete reliability, quasi-orthogonality) that give linear convergence and optimal rates
---

The adaptive finite element method (AFEM) repeats four steps: SOLVE the discrete problem on the current mesh, ESTIMATE the error on each element with an a posteriori [error estimator](/residual-error-estimator/), MARK the elements with large indicators, and REFINE them by [newest vertex bisection](/newest-vertex-bisection/). The mesh gets fine only where the solution needs it, for example near a reentrant corner, where the solution has a singularity that uniform refinement resolves slowly. With [Dorfler marking](/dorfler-marking/), an exact solve and the residual estimator, the error plus a multiple of the estimator shrinks by a fixed factor in each step, and the [AFEM optimality theorem](/afem-optimality-theorem/) shows that the error decays at the best rate that any sequence of such meshes can reach.

## In plain words

A uniform mesh spends the same effort everywhere, also where the solution is smooth and easy. The adaptive method starts with a coarse mesh and lets the computed solution show where the effort should go. After each solve, it measures for each triangle how badly the solution fails to satisfy the equation there. It refines the triangles with the largest values, solves again on the new mesh, and repeats. Near a corner where the solution is rough, the triangles get very small. Far from it, they stay large. For the same accuracy, the adaptive mesh can need far fewer unknowns than a uniform one.

## The problem

**Input.** A polygon $\Omega \subset \mathbb{R}^2$, the model problem $-\nabla\cdot(\kappa\nabla u) = f$ in $\Omega$ with $u = g$ on $\partial\Omega$ (the code takes $\kappa = 1$), a conforming initial triangulation $\mathcal{T}_0$ with refinement edges, a marking parameter $\theta \in (0, 1]$, and a stopping rule: a tolerance for the estimator, a maximum number of unknowns or a maximum number of steps.

**Output.** A sequence of nested triangulations $\mathcal{T}_0, \mathcal{T}_1, \ldots$ and continuous P1 Galerkin solutions $U_k$ with error indicators $\eta_k(K)$, where the last mesh meets the stopping rule. The aim is a small energy error $|||u - U_k||| = \|\nabla(u - U_k)\|$ for the number of unknowns $N_k$.

## The algorithm

The estimator is the residual estimator in the form of Cascon, Kreuzer, Nochetto and Siebert, with $h_K = |K|^{1/2}$:

$$\eta_k(K)^2 = h_K^2\|f\|_K^2 + h_K\sum_{E \subset \partial K \setminus \partial\Omega}\bigl\|[\![\partial_n U_k]\!]\bigr\|_E^2, \qquad \eta_k = \Bigl(\sum_{K}\eta_k(K)^2\Bigr)^{1/2}.$$

The jump $[\![\partial_n U_k]\!]$ of the normal derivative across an interior edge is constant on the edge for P1 functions. The element term has no $\Delta U_k$ because $U_k$ is linear on each triangle.

```pseudo id=main
AFEM(T0, f, g, theta, max_nodes, max_steps)
L1  for k <- 0, 1, ..., max_steps - 1 do        ▷ T <- T0 before the first pass
L2      U <- SOLVE(T, f, g)                      ▷ P1 Galerkin solution, conjugate gradients
L3      eta <- ESTIMATE(T, U, f)                 ▷ eta(K)^2 for every triangle K
L4      if the number of nodes of T > max_nodes then
L5          break
L6      M <- DORFLER(eta, theta)                 ▷ smallest set with sum of eta(K)^2 >= theta eta^2
L7      T <- REFINE(T, M)                        ▷ newest vertex bisection with closure
L8  return the list of (T, U, eta) of all passes
```

With $\theta = 1$ the code marks every triangle, and the loop becomes uniform refinement by bisection. This gives the comparison in the example below.

## Example

**One free node, by hand.** Take the unit square with $f = 1$ and $g = 0$, and refine the two initial triangles once, so that the mesh has four triangles of area $\tfrac14$ around the center $v_4 = (\tfrac12, \tfrac12)$. The only free node is $v_4$. Its hat function has gradient of length $2$ on each triangle, so the stiffness entry is $4 \cdot \tfrac14 \cdot 4 = 4$. The load is $4 \cdot \tfrac1{12} = \tfrac13$, so $U(v_4) = \tfrac1{12}$. The exact value of the solution at the center is about $0.0737$.

For the estimator, $h_K = \tfrac12$ and the element term is $h_K^2\|1\|_K^2 = \tfrac14\cdot\tfrac14 = \tfrac1{16}$. On the triangle with corners $(0,0)$, $(1,0)$, $v_4$ the solution is $U = \tfrac1{12}\cdot 2y$, and on its neighbor with corners $(0,0)$, $(0,1)$, $v_4$ it is $\tfrac1{12}\cdot 2x$. Across the shared half diagonal, with unit normal $(1, -1)/\sqrt2$, the jump of the normal derivative has size $\tfrac1{12}\cdot\tfrac{4}{\sqrt2} = \tfrac{\sqrt2}{6}$. The edge has length $\tfrac{\sqrt2}{2}$, so the edge term is $h_K\cdot\tfrac{\sqrt2}{2}\cdot\tfrac{2}{36} = \tfrac{\sqrt2}{72}$. Each triangle has two interior edges, so

$$\eta(K)^2 = \frac1{16} + \frac{\sqrt2}{36} \approx 0.10178, \qquad \eta = \sqrt{4 \cdot 0.10178} \approx 0.638.$$

All four indicators are equal. With $\theta = \tfrac12$, line L6 marks two triangles, because two of the four reach half of the sum. The test file checks these numbers.

**The L-shaped domain.** Take $\Omega = (-1, 1)^2 \setminus [0, 1) \times (-1, 0]$, $f = 0$ and $g$ equal to the exact solution $u = r^{2/3}\sin(2\phi/3)$ in polar coordinates. The gradient of $u$ is infinite at the reentrant corner, and $u$ is not in $H^2$. The initial mesh has six triangles. The reference code with max_nodes = 1200 gives the following energy errors, where $N$ is the number of free nodes.

| Method | Step | $N$ | $\lvert\lvert\lvert u - U\rvert\rvert\rvert$ | $\eta$ | $\eta / \lvert\lvert\lvert u - U\rvert\rvert\rvert$ |
|---|---|---|---|---|---|
| uniform | 3 | 17 | 0.2288 | 0.6896 | 3.01 |
| uniform | 6 | 161 | 0.1188 | 0.3667 | 3.09 |
| uniform | 9 | 1473 | 0.0606 | 0.1886 | 3.11 |
| adaptive, $\theta = 0.5$ | 5 | 14 | 0.1967 | 0.6767 | 3.44 |
| adaptive, $\theta = 0.5$ | 10 | 99 | 0.0866 | 0.3068 | 3.54 |
| adaptive, $\theta = 0.5$ | 13 | 266 | 0.0525 | 0.1888 | 3.60 |
| adaptive, $\theta = 0.5$ | 18 | 1376 | 0.0231 | 0.0847 | 3.67 |

A least squares fit of $\log$ error against $\log N$ for $N > 30$ gives the slope $-0.296$ for uniform refinement and $-0.484$ for the adaptive loop. The theory predicts $N^{-1/3}$ for uniform meshes, because $u$ is only in $H^{1 + 2/3 - \epsilon}$, and $N^{-1/2}$, the best rate of P1 elements in 2D, for the adaptive meshes. The uniform slope is still pre-asymptotic. To reach an error of $0.06$, the uniform mesh needs 1473 unknowns and the adaptive mesh needs about 200. The effectivity index stays between 2.6 and 3.7 over all steps of both runs. These are measurements on this problem, not bounds.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Each step is well defined because the P1 Galerkin matrix is symmetric positive definite, and NVB keeps the mesh conforming, so the spaces are nested. Galerkin orthogonality on nested spaces gives the Pythagoras identity $|||u - U_{k+1}|||^2 = |||u - U_k|||^2 - |||U_{k+1} - U_k|||^2$, so the error never grows. The estimator reduction lemma says that a bisection cuts $h_K^2$ at least in half, so the estimator of the old solution on the new mesh loses a fixed fraction of the marked part, up to a term in $|||U_{k+1} - U_k|||^2$. With Dorfler marking and the reliability bound $|||u - U_k||| \le C_{\mathrm{rel}}\eta_k$, these combine into the contraction

$$|||u - U_{k+1}|||^2 + \gamma\eta_{k+1}^2 \le \alpha^2\bigl(|||u - U_k|||^2 + \gamma\eta_k^2\bigr), \qquad 0 < \alpha < 1.$$

## Complexity

Count operations per step in the real-RAM model for a mesh of $M$ triangles. ESTIMATE costs $\Theta(M)$, with a hash map from edges to triangles. MARK costs $\Theta(M\log M)$ with a sort, or $\Theta(M)$ with a selection method (see [Dorfler marking](/dorfler-marking/)). REFINE costs $\Theta(M)$ expected time. SOLVE is the expensive step. The code uses unpreconditioned [conjugate gradients](/conjugate-gradient-method/), which costs $\Theta(M)$ per iteration, and the number of iterations grows with the condition number of the matrix, which grows as the mesh gets finer and more graded. A [multigrid](/multigrid-method/) or multilevel preconditioner adapted to the bisection hierarchy brings the cost of a solve close to $O(M)$. The memory is $\Theta(M)$.

Over $k$ steps the cost is the sum over the steps. In the L-shape run above the number of triangles grows by a factor of about 1.37 per step, so the sum is a small multiple of the cost of the last step. This growth factor is a measurement. With Dorfler marking alone there is no proved lower bound on the growth per step.

## Properties

- **Nested spaces.** NVB refinement gives $V_0 \subset V_1 \subset \cdots$, so the Galerkin error in the energy norm never increases with an exact solve.
- **Contraction.** With Dorfler marking, the quantity $|||u - U_k|||^2 + \gamma\eta_k^2$ decreases by the factor $\alpha^2 < 1$ in each step. The constants depend on $\theta$ and on the shapes of $\mathcal{T}_0$.
- **Optimal rate.** If $\theta$ is small enough and the marked set is nearly minimal, the error plus oscillation decays like $(\#\mathcal{T}_k)^{-s}$ for every $s$ for which the solution is in the approximation class $\mathbb{A}_s$. This is the [AFEM optimality theorem](/afem-optimality-theorem/).
- **Two-sided estimator.** The residual estimator is reliable, $|||u - U_k||| \le C_{\mathrm{rel}}\eta_k$, and efficient up to oscillation, $\eta_k \le C_{\mathrm{eff}}(|||u - U_k||| + \mathrm{osc}_k)$. So $\eta_k$ is a reliable stopping criterion up to the unknown constants.
- **No parameters from the solution.** The loop needs no knowledge of where the singularity is. The corner in the example is found by the indicators alone.

## Variants and improvements

- **Other marking rules.** The maximum strategy of Babuska and Vogelius marks every $K$ with $\eta(K) \ge \theta\max\eta$, and equidistribution marks indicators above the mean. They often work, but the optimal rate is proved only for bulk marking and some close relatives.
- **Other estimators.** The [Zienkiewicz-Zhu estimator](/zienkiewicz-zhu-estimator/) is cheaper to explain to engineers and is often used in practice. Equilibrated flux estimators give a guaranteed upper bound with constant 1. The convergence theory is cleanest for the residual estimator.
- **Goal-oriented adaptivity.** The [dual weighted residual method](/dual-weighted-residual-method/) marks by the error in a quantity of interest, using a dual solution.
- **hp adaptivity.** The [hp finite element method](/hp-finite-element-method/) chooses for each marked element between a smaller element and a higher degree, which can give exponential rates.
- **Coarsening.** Binev, Dahmen and DeVore added a coarsening step to prove optimal rates. Stevenson and Cascon, Kreuzer, Nochetto and Siebert showed it is not needed for the model problem. Coarsening is still useful for time dependent problems, where a feature moves.
- **Inexact solves.** Practical codes stop the iterative solver when its error is small compared to $\eta_k$. Later work extends the contraction and the rates to such loops.

## When to use it

Use AFEM when the solution has local features whose place is not known in advance: corner and crack singularities, point loads, jumps in the coefficients, interior and boundary layers. For a smooth solution on a convex domain, uniform refinement already gives the optimal rate, and adaptivity only adds cost. For time dependent problems with moving fronts, the static loop must be combined with coarsening or replaced by [block-structured AMR](/berger-colella-amr/) or the general [adaptive mesh refinement](/adaptive-mesh-refinement/) of finite volume codes. For strongly directional features such as boundary layers, isotropic bisection wastes unknowns; [anisotropic mesh adaptation](/anisotropic-mesh-adaptation/) stretches the elements.

## Pitfalls

- **Theta too large.** With $\theta$ close to 1, almost all triangles are marked, and the loop is close to uniform refinement. The rate theorem needs a small $\theta$; values from 0.25 to 0.6 are common. These values are a rule of thumb.
- **Counting the wrong size.** Plot the error against the number of unknowns $N$, not against the step number or the mesh size $h$, which is not uniform. The rate $N^{-1/2}$ for P1 in 2D corresponds to $h^1$ on uniform meshes.
- **Pre-asymptotic slopes.** The first steps on a coarse mesh do not show the final rate. Fit the slope only over the later steps, as in the example.
- **Unknown constants.** $\eta_k$ is an error bound only up to $C_{\mathrm{rel}}$, which the code does not know. In the example $\eta$ is about three times the error.
- **Loose solver tolerance.** If the iterative solver stops too early, the estimator measures the solver error, and the marking goes to the wrong places.
- **Inexact data.** A quadrature rule that is too weak for $f$ or $g$ adds an error that the estimator does not see. The data oscillation term must be small.
- **Boundary data on new nodes.** When a Dirichlet edge is bisected, the new node must get $g$ at the midpoint. Losing the boundary list during refinement gives a wrong problem, as the [NVB](/newest-vertex-bisection/) page warns.

## Implementations

## History

Ivo Babuska and Werner Rheinboldt introduced a posteriori error estimates and adaptive refinement for finite elements in 1978, and Babuska and Vogelius proved convergence of a feedback method in one dimension in 1984. For a long time the loop in 2D and 3D was used without a proof that it converges. Willy Dorfler gave the first proof in 1996 for Poisson's equation, with the bulk marking rule and a fine enough initial mesh. Pedro Morin, Ricardo Nochetto and Kunibert Siebert removed the condition on the initial mesh in 2000, with marking for the data oscillation and an interior node in each refined element. Peter Binev, Wolfgang Dahmen and Ronald DeVore proved optimal rates in 2004 with a coarsening step, Rob Stevenson removed the coarsening in 2007, and Manuel Cascon, Christian Kreuzer, Nochetto and Siebert gave the simple proof by contraction in 2008. Carsten Carstensen, Michael Feischl, Marcus Page and Dirk Praetorius collected the common structure of these proofs in the axioms of adaptivity in 2014.

## References
