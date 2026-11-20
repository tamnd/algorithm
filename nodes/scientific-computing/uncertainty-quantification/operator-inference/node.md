---
tag: 094ATM
kind: algorithm
slug: operator-inference
name: Operator inference
area: scientific-computing/uncertainty-quantification
level: research
summary: Learns the matrices of a polynomial reduced model by least squares on projected snapshot data, with no access to the full model code.
model: real-ram
complexity:
  vars: {n: the number of full unknowns, r: the reduced size, K: the total number of snapshots, C: the cost of one step of the full model}
  time: {offline: "O(n^2 K + n^3 + K C + K r^4)", online: "O(r^3)"}
  space: {extra: "O(n K + K r^2)"}
properties: {deterministic: true, exact: false, iterative: false, intrusive: false}
history:
  year: 2016
  people: [Benjamin Peherstorfer, Karen Willcox]
  note: Proposed as a non-intrusive way to obtain the projection-based reduced model of a system with polynomial terms. Re-projection, which recovers the intrusive reduced model exactly from data, followed in 2020.
prereqs: [pod-galerkin-reduced-model, least-squares-problem, qr-decomposition]
see_also: [dynamic-mode-decomposition, sindy, proper-generalized-decomposition, discrete-empirical-interpolation-method, tikhonov-regularization, burgers-equation, balanced-truncation]
sources:
  - paper: doi:10.1016/j.cma.2016.03.025
    title: Benjamin Peherstorfer and Karen Willcox, Data-driven operator inference for nonintrusive projection-based model reduction, Computer Methods in Applied Mechanics and Engineering 306, 2016, 196-215
    locator: the least squares problem for the reduced linear and quadratic operators, and the convergence of the learned operators to the intrusive ones
  - paper: doi:10.1137/19M1292448
    title: Benjamin Peherstorfer, Sampling low-dimensional Markovian dynamics for preasymptotically recovering reduced models from data with operator inference, SIAM Journal on Scientific Computing 42(5), 2020, A3489-A3515
    locator: the re-projection of trajectories and the exact recovery of the intrusive reduced model for time-discrete polynomial systems
  - paper: doi:10.1137/130932715
    title: Peter Benner, Serkan Gugercin and Karen Willcox, A survey of projection-based model reduction methods for parametric dynamical systems, SIAM Review 57(4), 2015, 483-531
    locator: projection-based reduced models and the intrusive construction that operator inference replaces
---

Operator inference (OpInf) builds a reduced model of a dynamical system from data, when the code of the full model cannot be changed or read. It assumes that the full model has a known polynomial form, for example a linear term and a quadratic term, as many discretized PDEs do. Then the [POD-Galerkin](/pod-galerkin-reduced-model/) reduced model has the same form, with small matrices $\hat{A}$ and $\hat{H}$. The intrusive way computes them as $V^T A V$ and a projected tensor, which needs the full matrices. OpInf computes a POD basis $V$ from snapshots, projects the snapshots to reduced states $\hat{a}_k = V^T x_k$, and fits $\hat{A}$ and $\hat{H}$ by linear [least squares](/least-squares-problem/) so that the reduced states follow the reduced model. With plain projected data, the fit includes a closure error, and the learned model differs from the intrusive one. With re-projected data, each reduced state is the projection of one full step from the lifted previous state, and then the least squares problem has the intrusive model as its exact solution, if the data matrix has full column rank.

[Dynamic mode decomposition](/dynamic-mode-decomposition/) also fits a matrix to projected snapshot pairs, but only a linear one, with no assumed structure. OpInf is the same kind of fit with the polynomial terms that the physics gives. [SINDy](/sindy/) chooses a few terms from a large library by sparse regression, often in the original variables, to discover the form of the equations. OpInf knows the form and fits all its terms in the reduced variables. The [proper generalized decomposition](/proper-generalized-decomposition/) is intrusive: it builds a separated solution from the operator itself and learns nothing from data.

## In plain words

You have a simulator that you can run but not open. You know that its equations have a linear part and a quadratic part. You run it, keep the states, and find a few patterns that describe them, by POD. Then you write each state as a mix of the patterns, and you ask: which small linear and quadratic rule moves one mix to the next? This is a least squares fit of a few numbers. The result is a small model of the same type that a code developer would get by projecting the equations, and with the right data it is exactly that model.

## The problem

The full model is a time-discrete system $x_{k+1} = f(x_k)$ with $x_k \in \mathbb{R}^n$ and

$$f(x) = A x + H (x \otimes x)$$

for unknown matrices $A$ and $H$. The user can only evaluate $f$. Given initial states and a reduced size $r$, the output is a reduced model

$$a_{k+1} = \hat{A} a_k + \hat{H} s(a_k), \qquad s(a) = (a_i a_j)_{1 \le i \le j \le r} \in \mathbb{R}^{r(r+1)/2},$$

where $\hat{A} \in \mathbb{R}^{r \times r}$, $\hat{H} \in \mathbb{R}^{r \times r(r+1)/2}$, and $V a_k$ approximates $x_k$ for an $n \times r$ basis $V$ with orthonormal columns. The intrusive reduced model, the reference, is the Galerkin projection $a_{k+1} = V^T f(V a_k)$. It has the same form, since $V^T f(V a)$ is a quadratic polynomial in $a$ with no constant term. The vector $s(a)$ keeps each product $a_i a_j$ once, so the coefficients of the quadratic part are unique.

**The model problem** of the example is the viscous [Burgers equation](/burgers-equation/) $u_t + (u^2/2)_x = \nu u_{xx}$ on $(0, 1)$ with $u = 0$ at both ends and $\nu = 0.05$, with central differences on $n = 32$ interior points ($h = 1/33$) and explicit Euler steps with $\Delta t = 0.002$. So $f(x) = x + \Delta t (L x + Q(x))$, where $L$ is the scaled second difference and $Q(x)_i = -(x_{i+1}^2 - x_{i-1}^2)/(4h)$.

## The algorithm

```pseudo id=main
OPERATOR-INFERENCE(black-box step f, initial states, K, r)
L1  V ← the r leading POD modes of the snapshots x_0..x_K of each trajectory
L2  â_k ← re-projected states: â_0 = V^T x_0, â_(k+1) = V^T f(V â_k); or projected states â_k = V^T x_k
L3  D ← the matrix with a row [â_k^T, s(â_k)^T] for each k < K of each trajectory
L4  R ← the matrix with the matching rows â_(k+1)^T
L5  O ← the minimizer of ‖D O - R‖_F, by a QR factorization of D
L6  [Â Ĥ] ← O^T
L7  return the reduced model a_(k+1) = Â a_k + Ĥ s(a_k)
```

Line L1 runs the full model and takes the POD basis of all snapshots, as for an intrusive reduced model. Line L2 has two choices. Projected states need no extra runs. Re-projected states need $K$ more calls of $f$ per trajectory, each started from the lifted reduced state $V \hat{a}_k$. Lines L3 and L4 set up a linear least squares problem with $r + r(r+1)/2$ unknowns per row of $O^T$; the $r$ columns of $O$ share the matrix $D$. Line L5 solves it with a QR factorization of $D$, here by modified [Gram-Schmidt](/qr-decomposition/) with two passes, which is more stable than the normal equations. The online stage, one step of the reduced model, costs $O(r^3)$.

## Example

**By hand.** Take $r = 1$ and a full model whose reduced step is $a_{k+1} = 0.5 a_k + 0.25 a_k^2$. The data $\hat{a}_0 = 1$, $\hat{a}_1 = 0.75$, $\hat{a}_2 = 0.515625$ give $D = \begin{pmatrix} 1 & 1 \\ 0.75 & 0.5625 \end{pmatrix}$ and $R = (0.75, 0.515625)^T$. $D$ is invertible ($\det D = -0.1875$), so the least squares solution is the solution of $D O = R$: $\hat{A} = 0.5$ and $\hat{H} = 0.25$, the model that made the data.

**Burgers.** Three trajectories of $K = 200$ steps start from $\sin(\pi x)$, $0.8 \sin(2\pi x) + 0.3 \sin(\pi x)$ and $2x(1 - x)(1 + x)$. The singular values of the 603 snapshots are 66.3, 33.6, 4.28, 2.77, 0.723 and 0.206. The table is a measurement from the test file and a scratch run. "Difference" is the largest entry of the learned $[\hat{A}, \hat{H}]$ minus the intrusive one. The errors are $\max_k \|x_k - V a_k\|_2 / \max_k \|x_k\|_2$ along the first training trajectory and along a test trajectory from $0.6 \sin(\pi x) + 0.4 \sin(3\pi x)$.

| $r$ | difference, re-projected | difference, projected | training error, re-projected | training error, projected | test error, re-projected | test error, projected |
|---|---|---|---|---|---|---|
| 3 | $5.1 \times 10^{-15}$ | $6.2 \times 10^{-3}$ | $5.63 \times 10^{-2}$ | $5.63 \times 10^{-2}$ | 0.124 | 0.168 |
| 4 | $5.8 \times 10^{-14}$ | $7.7 \times 10^{-3}$ | $1.13 \times 10^{-2}$ | $1.05 \times 10^{-2}$ | 0.102 | 0.558 |
| 5 | $3.8 \times 10^{-12}$ | $2.6 \times 10^{-2}$ | $3.52 \times 10^{-3}$ | $3.37 \times 10^{-3}$ | 0.0874 | overflow |
| 6 | $8.0 \times 10^{-11}$ | 0.27 | $2.25 \times 10^{-3}$ | $2.17 \times 10^{-3}$ | 0.0142 | 0.273 |

With re-projection the learned model is the intrusive model up to rounding, which grows with the condition number of $D$: $4.3 \times 10^4$ for $r = 4$ and $1.4 \times 10^8$ for $r = 6$. With projected data the fit is a little better on the training trajectory, because it fits that data, but on the test trajectory it is worse, and for $r = 5$ it blows up. With only the first trajectory, $D$ is numerically rank deficient for $r \ge 4$, and even re-projection does not recover the intrusive model: the difference is 6.9 for $r = 6$.

## Correctness

The proof file shows three facts, in exact arithmetic. First, the intrusive reduced step $V^T f(V a)$ equals $\hat{A}_{int} a + \hat{H}_{int} s(a)$ for unique matrices, because $f$ is a quadratic polynomial with $f(0) = 0$. Second, line L5 returns the unique minimizer of $\|D O - R\|_F$ when $D$ has full column rank, and the QR solution equals the solution of the normal equations. Third, the recovery theorem: if the states come from re-projection, then $R = D O_{int}$ with $O_{int}^T = [\hat{A}_{int}, \hat{H}_{int}]$, so the residual at $O_{int}$ is 0, and by uniqueness line L5 returns the intrusive model. With projected states, the row $k$ of $R$ is $V^T f(x_k)$, not $V^T f(V V^T x_k)$, so $R = D O_{int} + E$ with a closure error $E$ that is not 0 in general, and the learned model is the intrusive model plus $D^+ E$.

## Complexity

In the [real RAM](/real-ram/) model, the POD basis of $K$ snapshots costs $O(n^2 K)$ to form $S S^T$ and $O(n^3)$ per Jacobi sweep for its eigenvectors in the implementation; for $n > K$ the method of snapshots costs $O(n K^2 + K^3)$ instead. Re-projection costs $K$ calls of $f$ and $O(n r)$ per lift and projection. The data matrix has $K$ rows and $p = r + r(r+1)/2 = O(r^2)$ columns, so the QR factorization costs $O(K p^2) = O(K r^4)$, and the $r$ right sides cost $O(K r p)$. An online step costs $O(r p) = O(r^3)$ for $\hat{H} s(a)$. Memory is $O(n K)$ for the snapshots and $O(K r^2)$ for $D$.

## Properties

- **Non-intrusive.** It needs only evaluations of the full model, not its matrices.
- **Exact recovery.** With re-projected data and a data matrix of full column rank, the learned model is the intrusive POD-Galerkin model.
- **Structure from physics.** The reduced model has the polynomial form of the full model, so it can be analysed like an intrusive model.
- **Linear least squares.** The fit is a convex problem with a closed-form solution, unlike training a neural network.
- **No error bound.** The error of the reduced model is not certified; it is the error of the intrusive model at best.

## Variants and improvements

- **Continuous-time data.** For $\dot{x} = A x + H(x \otimes x)$, fit $\dot{\hat{a}} \approx \hat{A} \hat{a} + \hat{H} s(\hat{a})$, with time derivatives from finite differences of the reduced states. The derivative error then adds to the closure error.
- **Regularization.** Add a [Tikhonov](/tikhonov-regularization/) term $\lambda \|O\|_F^2$ to line L5 when $D$ is ill-conditioned or the data is noisy. This trades exact recovery for stability.
- **Inputs and constants.** Add columns for an input $u_k$ and for a constant term, so that the reduced model is $\hat{A} a + \hat{H} s(a) + \hat{B} u + \hat{c}$.
- **Lifting.** For a model that is not polynomial, change variables so that it becomes quadratic, then apply OpInf to the lifted variables.
- **Structure-preserving fits.** Constrain $\hat{A}$ to be symmetric or negative definite, or $\hat{H}$ to conserve energy, by a constrained least squares problem.

## When to use it

Use operator inference when the full model is a black box that you can run and that has a known polynomial form, and when you want a reduced model that behaves like a POD-Galerkin model, for example for control, design or [forward uncertainty propagation](/forward-uncertainty-propagation/). If you can also start the full model from chosen states, use re-projection. Use the intrusive projection when you can access the matrices. Use [DMD](/dynamic-mode-decomposition/) for a linear model with no known structure, [SINDy](/sindy/) to find which terms are in the equations, and [DEIM](/discrete-empirical-interpolation-method/) for a non-polynomial term in an intrusive model.

## Pitfalls

- **Rank-deficient data.** One trajectory that decays to a steady state gives nearly dependent rows, and the number of unknowns grows like $r^2$. Use several trajectories or inputs, and check the condition number of $D$.
- **The closure error.** With projected data, the learned model fits the truncated dynamics with an error that is not the intrusive error. It can fit the training data well and still be unstable, as in the example for $r = 5$.
- **Inconsistent time stepping.** If the data comes from an implicit or adaptive time integrator, the discrete map is not quadratic, and the assumed form is wrong. Fit the form that the data has.
- **Wrong polynomial degree.** A cubic term in the full model, or a non-polynomial one, is not in the model class. The fit then hides the error in the other terms.
- **Scaling.** The columns of $D$ for $a_i$ and for $a_i a_j$ can differ by orders of magnitude. Scale the states before the fit.

## Implementations

## History

Peherstorfer and Willcox introduced operator inference in 2016, for systems with polynomial terms, and showed that the learned operators converge to the intrusive ones as the projection error goes to 0. In 2020 Peherstorfer introduced re-projection and proved that, for time-discrete polynomial systems, it recovers the intrusive reduced model from data exactly under a rank condition. Later work added regularization, lifting transformations for models that are not polynomial, and structure-preserving fits.

## References
