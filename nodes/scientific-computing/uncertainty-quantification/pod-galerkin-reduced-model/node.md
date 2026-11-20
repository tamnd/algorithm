---
tag: 9GPP7P
kind: algorithm
slug: pod-galerkin-reduced-model
name: POD-Galerkin reduced-order model
aliases:
- POD-Galerkin model
area: scientific-computing/uncertainty-quantification
level: core
summary: Projects the equations of a large model onto the leading proper orthogonal decomposition modes of its snapshots, which gives a small system of ODEs that runs fast.
model: real-ram
complexity:
  vars: {n: the state dimension, m: the number of snapshots, r: the size of the reduced basis, K: the number of time steps}
  time: {offline: "O(n m^2 + m^3 + n^2 r)", online: "O(r^3 + K r^2)", lift: "O(n r)"}
  space: {extra: O(n m + n r + r^2)}
properties: {deterministic: true, exact: false, iterative: false, intrusive: true}
history:
  year: 1987
  people: [John L. Lumley, Lawrence Sirovich, Philip Holmes, Gal Berkooz]
  note: Lumley brought the proper orthogonal decomposition to turbulence in 1967. Sirovich gave the method of snapshots in 1987. Galerkin models on POD modes of turbulent flows followed in the late 1980s.
prereqs: [singular-value-decomposition, galerkin-method, backward-euler-method]
see_also: [reduced-basis-method, discrete-empirical-interpolation-method, operator-inference, principal-component-analysis, dynamic-mode-decomposition, balanced-truncation, karhunen-loeve-theorem, heat-equation]
sources:
  - paper: doi:10.1090/qam/910462
    title: Lawrence Sirovich, Turbulence and the dynamics of coherent structures. I. Coherent structures, Quarterly of Applied Mathematics 45(3), 1987, 561-571
    locator: the method of snapshots (the eigenvalue problem of the m by m correlation matrix)
  - book: isbn:9781107008250
    title: Philip Holmes, John L. Lumley, Gal Berkooz and Clarence W. Rowley, Turbulence, Coherent Structures, Dynamical Systems and Symmetry, 2nd edition, Cambridge University Press, 2012
    locator: the chapters on the proper orthogonal decomposition and on Galerkin projection (the 1st edition of 1996 is by Holmes, Lumley and Berkooz)
  - book: isbn:9783319154305
    title: Alfio Quarteroni, Andrea Manzoni and Federico Negri, Reduced Basis Methods for Partial Differential Equations, An Introduction, UNITEXT 92, Springer, 2016
    locator: Chapter 6 (construction of reduced basis spaces by SVD-POD)
  - paper: doi:10.1137/130932715
    title: Peter Benner, Serkan Gugercin and Karen Willcox, A survey of projection-based model reduction methods for parametric dynamical systems, SIAM Review 57(4), 2015, 483-531
    locator: the sections on projection and on basis computation by POD
---

A POD-Galerkin reduced-order model replaces a large linear system of ODEs $x' = A x + f$ with $n$ unknowns by a system with $r$ unknowns, where $r$ is much smaller than $n$. It runs the full model once and stores the states as snapshots. It takes the $r$ leading proper orthogonal decomposition (POD) modes of the snapshots as an orthonormal basis $V$. Then it projects the equations onto that basis by a [Galerkin method](/galerkin-method/). The POD modes are the leading left singular vectors of the snapshot matrix $S$ (see [singular value decomposition](/singular-value-decomposition/)). They are the vectors that [principal component analysis](/principal-component-analysis/) finds when the snapshots are not centered. POD alone only compresses data. The Galerkin step makes a model that you can run again, for example with new initial values. [Dynamic mode decomposition](/dynamic-mode-decomposition/) fits a linear map to the snapshots and needs no equations, and its modes are not orthogonal. [Balanced truncation](/balanced-truncation/) also reduces linear systems, but it takes its basis from the Gramians of an input-output system and has an a priori error bound. POD uses only the states that it saw. The [reduced basis method](/reduced-basis-method/) uses the same projection for problems with parameters, with snapshots chosen by a [weak greedy search](/weak-greedy-reduced-basis/).

## In plain words

A heat simulation on a fine grid has thousands of numbers per time step, but the temperature profiles it goes through look alike. A few basic shapes, added with the right weights, describe each of them well. POD finds these shapes from a set of stored profiles: the first shape is the one that matches all the profiles best, the second one adds the most to the first, and so on.

Then the model changes its unknowns. It does not track the temperature at each grid point. It tracks only the weights of the few shapes. The equations are projected onto the shapes, which gives a small system with $r$ unknowns instead of $n$. Each time step of the small system costs almost nothing. The price is a single run of the full model, plus the risk that the shapes do not fit states the model never saw.

## The problem

The full model is the linear system $x'(t) = A x(t) + f$ with a constant $n$ by $n$ matrix $A$, a constant vector $f$ and an initial value $x_0$. It is stepped with the [backward Euler method](/backward-euler-method/) with step $dt$:

$$(I - dt\, A)\, x_{k+1} = x_k + dt\, f, \qquad k = 0, \ldots, K - 1.$$

The snapshot matrix $S$ has $m$ columns $s_1, \ldots, s_m \in \mathbb{R}^n$, one per stored state; in the example they are the states $x_0, \ldots, x_K$ of a training run, so $m = K + 1$. For $r \le \operatorname{rank} S$, the POD basis of size $r$ is an $n$ by $r$ matrix $V$ with orthonormal columns that minimizes the projection error

$$E(V) = \sum_{j=1}^{m} \| s_j - V V^T s_j \|_2^2.$$

The output is the reduced trajectory $\tilde{x}_k = V z_k$, where $z_k \in \mathbb{R}^r$ solves the Galerkin reduced system: the full equation with $x = V z$, multiplied by $V^T$. This page writes $r$ for the reduced size and $n$ for the full size. The books of Hesthaven, Rozza and Stamm and of Quarteroni, Manzoni and Negri write $N$ for the reduced size and $N_h$ or $\mathcal{N}$ for the full size.

## The algorithm

```pseudo id=main
POD-GALERKIN(A, f, x_0, dt, K, S, r)
L1  C ← S^T S                                         ▷ m by m correlation matrix
L2  (λ_i, w_i) ← eigenpairs of C, λ_1 ≥ λ_2 ≥ ... ≥ λ_m ≥ 0, with orthonormal w_i
L3  v_i ← S w_i / sqrt(λ_i) for i = 1..r;  V ← [v_1 ... v_r]
L4  A_r ← V^T A V;  f_r ← V^T f;  z_0 ← V^T x_0          ▷ offline stage
L5  for k = 0 to K - 1 do                                 ▷ online stage
L6      z_(k+1) ← (I - dt A_r)^(-1) (z_k + dt f_r)
L7  return x̃_k = V z_k for k = 0..K
```

Lines L1 to L3 are the method of snapshots of Sirovich. They solve an eigenvalue problem of size $m$, not $n$, which is cheap when there are fewer snapshots than unknowns. Line L2 needs $\lambda_r > 0$; the implementation raises an error otherwise, and it finds the eigenpairs with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Line L3 maps each eigenvector of $C$ back to a mode in $\mathbb{R}^n$; the division by $\sqrt{\lambda_i}$ makes the mode a unit vector. Line L4 builds the reduced operators once. This is the offline stage, and it is the only part that touches vectors of length $n$ apart from the last line. Lines L5 and L6 are backward Euler on the reduced system; the implementation forms the $r$ by $r$ inverse once and reuses it. Line L7 lifts the reduced states back to the full space. For backward Euler on a linear system, it gives the same $z_k$ to project the ODE first and then step it, or to step it first and then project.

## Example

**A hand example.** Take $n = 3$, two snapshots $s_1 = (1, 1, 1)$ and $s_2 = (1, 1, -1)$, the matrix $A = 16 \operatorname{tridiag}(1, -2, 1)$ of the [heat equation](/heat-equation/) $u_t = u_{xx}$ on three interior points with $h = 1/4$, and $r = 1$.

| line | result |
|---|---|
| L1 | $C = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$ |
| L2 | $\lambda_1 = 4$, $w_1 = (1, 1)/\sqrt{2}$; $\lambda_2 = 2$, $w_2 = (1, -1)/\sqrt{2}$ |
| L3 | $v_1 = S w_1 / 2 = (2, 2, 0) / (2\sqrt{2}) = (1, 1, 0)/\sqrt{2}$ |
| L4 | $A v_1 = 16 (-1, -1, 1)/\sqrt{2}$, so $A_r = v_1^T A v_1 = -16$ |

The projection error with $r = 1$ is $\|s_1 - v_1 v_1^T s_1\|^2 + \|s_2 - v_1 v_1^T s_2\|^2 = \|(0, 0, 1)\|^2 + \|(0, 0, -1)\|^2 = 2$, which is $\lambda_2$, as the correctness section says. With $r = 2$ the second mode is $v_2 = S w_2 / \sqrt{2} = (0, 0, 1)$, the two modes span both snapshots, and the error is 0. One online step with $x_0 = s_1$, $f = 0$ and $dt = 1/16$ gives $z_0 = \sqrt{2}$ and $z_1 = \sqrt{2} / (1 + 16\, dt) = \sqrt{2}/2$, so $\tilde{x}_1 = (1/2, 1/2, 0)$. The full step gives $x_1 = (4/7, 5/7, 4/7)$; one mode cannot hold the third component.

**A measurement.** The full model is the heat equation on $(0, 1)$ with $u = 0$ at both ends and a source $f = 1$, on $n = 60$ interior points ($h = 1/61$), with $dt = 0.002$ and $K = 20$ steps. The initial value is 1 at the 12 grid points in $[0.2, 0.4]$ and 0 elsewhere. The snapshots are the 21 states of this run, and the reduced model then runs the same problem. The script is the test file of the implementation.

| $r$ | $\lambda_r$ | $\sum_{i > r} \lambda_i$ | measured $\sum_j \|s_j - V V^T s_j\|^2$ | $\max_k \|x_k - V z_k\|_2$ |
|---|---|---|---|---|
| 1 | 78.851 | 7.5391 | 7.5391 | 1.8074 |
| 2 | 6.5374 | 1.0016 | 1.0016 | 0.60535 |
| 3 | 0.85575 | 0.14589 | 0.14589 | 0.31229 |
| 4 | 0.13956 | $6.3318 \times 10^{-3}$ | $6.3318 \times 10^{-3}$ | $4.9508 \times 10^{-2}$ |
| 5 | $5.9171 \times 10^{-3}$ | $4.1472 \times 10^{-4}$ | $4.1472 \times 10^{-4}$ | $1.3277 \times 10^{-2}$ |
| 6 | $3.9203 \times 10^{-4}$ | $2.2684 \times 10^{-5}$ | $2.2684 \times 10^{-5}$ | $2.6899 \times 10^{-3}$ |
| 7 | $2.1838 \times 10^{-5}$ | $8.4650 \times 10^{-7}$ | $8.4650 \times 10^{-7}$ | $4.7749 \times 10^{-4}$ |

The third and fourth columns agree to all printed digits, which is the identity of Lemma 2 in the proof. The eigenvalues fall by a factor of 10 to 40 per mode, because diffusion damps the short waves fast. The largest error of the reduced model is at $k = 0$, where the step in the initial value is hardest to represent. Seven modes give an error of $4.8 \times 10^{-4}$ against $\|x_0\|_2 = 3.46$. This is the easy case: the reduced model runs the problem that made its snapshots.

## Correctness

The proof file shows four facts. First, the columns of $V$ from line L3 are orthonormal. Second, the projection error of the snapshots is exactly $\sum_{i > r} \lambda_i$, the sum of the discarded squared singular values of $S$. Third, if $A$ is symmetric and negative semidefinite, as for the heat equation, the matrix $I - dt\, A_r$ in line L6 is invertible for every $dt > 0$ and its inverse has norm at most 1. Fourth, with $\rho_k = x_k - V V^T x_k$, the error of the reduced model obeys

$$\|x_k - V z_k\|_2^2 = \|\rho_k\|_2^2 + \|V^T x_k - z_k\|_2^2, \qquad \|V^T x_K - z_K\|_2 \le dt \sum_{k=1}^{K} \|A \rho_k\|_2 .$$

So if every state of the run lies in the span of $V$, the reduced model reproduces the run exactly. The proof that $V$ minimizes $E(V)$ is the Schmidt-Eckart-Young theorem for the singular value decomposition, and the page cites it; the tests check the identity of the second fact and a random basis against POD. The bound has the factor $\|A \rho_k\|$, not $\|\rho_k\|$, so a small projection error can still give a large reduced model error when $A$ has a large norm. For nonlinear flows there is no such bound in general, and the reduced model can be unstable.

## Complexity

In the [real RAM](/real-ram/) model, line L1 costs $O(n m^2)$, an eigen solver for the symmetric $m$ by $m$ matrix costs $O(m^3)$ (each sweep of the Jacobi method costs $O(m^3)$, and a few sweeps are enough), and line L3 costs $O(n m r)$. Line L4 costs $O(n^2 r)$ for a dense $A$ and $O(n r^2)$ for a banded $A$ such as the heat matrix. The online stage costs $O(r^3)$ once for the inverse and $O(r^2)$ per step, so $O(r^3 + K r^2)$, with no dependence on $n$. Each lifted state $V z_k$ costs $O(n r)$, and a user who needs only a few outputs, such as a mean or a point value, can lift only those. The snapshot matrix takes $O(n m)$ memory and the basis $O(n r)$.

## Properties

- **Exact projection error.** The error of the snapshots is the sum of the discarded eigenvalues, so the user can pick $r$ before running the reduced model.
- **Optimal for the snapshots.** No other basis of size $r$ has a smaller error $E(V)$ (a theorem, Schmidt-Eckart-Young). It is optimal for the snapshots, not for the states of a new run.
- **Stable for symmetric dissipative systems.** If $A$ is symmetric and negative semidefinite, then so is $A_r$, and backward Euler on the reduced system does not grow (proved). If only $A + A^T \le 0$ holds, the same argument works for the symmetric part.
- **Intrusive.** Line L4 needs $A$ and $f$, not just the outputs of the full code. [Operator inference](/operator-inference/) learns $A_r$ from data instead.
- **Deterministic.** The basis depends on the snapshots only up to the sign of each mode.

## Variants and improvements

- **Direct SVD.** Compute the thin SVD of $S$ instead of the eigenpairs of $S^T S$. This avoids squaring the condition number and gives accurate modes for small singular values.
- **A weighted inner product.** For finite elements, the physical norm is $\|u\|_M^2 = u^T M u$ with the mass matrix $M$. Then line L1 is $C = S^T M S$, the modes are $M$-orthonormal and the projection is $V^T M$.
- **Mean subtraction.** Subtract the mean of the snapshots, or a lifting function that carries the boundary values, and find the modes of the rest.
- **Nonlinear terms.** For $x' = A x + g(x)$, the term $V^T g(V z)$ costs $O(n)$ per step. The [discrete empirical interpolation method](/discrete-empirical-interpolation-method/) evaluates $g$ at a few points only.
- **Parameters.** With snapshots at several parameter values, the same projection gives a parametric model; the [reduced basis method](/reduced-basis-method/) adds an a posteriori error bound and a greedy choice of the parameters.
- **Petrov-Galerkin projection.** A test basis $W \ne V$ in line L4 ($A_r = W^T A V$ with $W^T V = I$) can restore stability for convection problems.

## When to use it

Use a POD-Galerkin model when you must run the same large linear or mildly nonlinear model many times, at inputs close to those of the training runs, and you have access to the operators of the full code. The offline cost is one or more full runs, so the method pays only after many online runs. Use [balanced truncation](/balanced-truncation/) for a linear input-output system of moderate size where you want an error bound. Use [operator inference](/operator-inference/) or [dynamic mode decomposition](/dynamic-mode-decomposition/) when you have only the outputs of the code. Use the [reduced basis method](/reduced-basis-method/) when the problem has parameters and you need a certified error. Do not use POD-Galerkin for flows with moving fronts or shocks: the singular values of such snapshots decay slowly, and $r$ must be large.

## Pitfalls

- **A Galerkin model of a stable non-normal system can be unstable.** Line L4 does not keep the stability of $A$ unless $A + A^T \le 0$. For $A = \begin{pmatrix} -1 & 4 \\ 0 & -1 \end{pmatrix}$, with both eigenvalues equal to $-1$, and $v = (1, 1)/\sqrt{2}$, the reduced matrix is $v^T A v = 1 > 0$, and the reduced model grows.
- **Small eigenvalues in line L3.** If $\lambda_i$ is at the level of rounding, $S w_i / \sqrt{\lambda_i}$ is mostly noise and is not orthogonal to the other modes. Choose $r$ below the numerical rank, or use the SVD of $S$.
- **The energy rule is a rule.** Choosing $r$ so that $\sum_{i \le r} \lambda_i / \sum_i \lambda_i \ge 99.9\%$ is a common rule of thumb, not a bound on the error of the reduced model. The bound depends on $\|A \rho_k\|$ (see the correctness section).
- **An online stage that depends on $n$.** If $A$ depends on a parameter or the model has a nonlinear term, and line L4 is done again at each step, the online cost is $O(n)$ or more, and the reduced model is not faster. Use an affine decomposition or DEIM.
- **Extrapolation.** The snapshots come from one run. A new initial value or source with shapes that the run did not contain gives a large error, with no warning.
- **The wrong inner product in line L1.** On a non-uniform mesh, the Euclidean product weights small cells too little. The modes are then optimal in the wrong norm.

## Implementations

## History

The proper orthogonal decomposition is the discrete form of the [Karhunen-Loeve expansion](/karhunen-loeve-theorem/) of the 1940s (Kosambi, Loeve and Karhunen). Lumley brought it to turbulence in 1967 as a way to define coherent structures. Sirovich gave the method of snapshots in 1987, which made POD practical for large simulations. Aubry, Holmes, Lumley and Stone built a Galerkin model of the turbulent wall layer on POD modes in 1988. Holmes, Lumley and Berkooz wrote the standard book in 1996, and its second edition of 2012 adds Rowley. In the 2000s, POD-Galerkin models became one of the main tools of projection-based model reduction, next to balanced truncation and the reduced basis method, as the survey of Benner, Gugercin and Willcox describes.

## References
