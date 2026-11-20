---
tag: FTZTDM
kind: algorithm
slug: incremental-4d-var
name: Incremental 4D-Var
area: scientific-computing/data-assimilation
level: advanced
summary: Solves 4D-Var by outer loops that relinearize the model and inner loops that minimize a quadratic cost for the increment at lower resolution.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, K: the number of model steps in the window, p: the total number of observations, k: the number of outer loops, m: the number of conjugate gradient steps per outer loop, c: the cost of one full model step, s: the cost of one step of the inner linear model}
  time: {worst: "Θ(n^3 + k (K c + m (K s + n^2 + n p)))"}
  space: {extra: "Θ(K n + n^2)"}
properties: {deterministic: true, outer_loop: Gauss-Newton step with the exact tangent linear model, exact_for_linear_model: one outer loop with an exact inner solve, inner_solver: conjugate gradient, inexact_inner_model: changes the fixed point}
history:
  year: 1994
  people: [Philippe Courtier, Jean-Noël Thépaut, Anthony Hollingsworth]
  note: Courtier, Thépaut and Hollingsworth proposed the incremental form in 1994 to make 4D-Var affordable, and Lawless, Gratton and Nichols showed in 2005 that it is a Gauss-Newton method.
prereqs: [four-dimensional-variational-assimilation, gauss-newton-algorithm]
see_also: [adjoint-model, conjugate-gradient-method, three-dimensional-variational-assimilation, weak-constraint-4d-var, control-variable-transform, nonlinear-least-squares, preconditioning, four-dimensional-ensemble-variational]
sources:
  - paper: doi:10.1002/qj.49712051912
    title: P. Courtier, J.-N. Thépaut and A. Hollingsworth, A strategy for operational implementation of 4D-Var, using an incremental approach, Quarterly Journal of the Royal Meteorological Society 120(519) (1994) 1367-1387
    locator: the outer and inner loops, the increment at low resolution and the simplified linear model
  - paper: doi:10.1256/qj.04.20
    title: A. S. Lawless, S. Gratton and N. K. Nichols, An investigation of incremental 4D-Var using non-tangent linear models, Quarterly Journal of the Royal Meteorological Society 131(606) (2005) 459-476
    locator: incremental 4D-Var as a Gauss-Newton method, and the effect of an inexact linear model on the fixed point
  - paper: doi:10.1002/qj.49712656415
    title: F. Rabier, H. Järvinen, E. Klinker, J.-F. Mahfouf and A. Simmons, The ECMWF operational implementation of four-dimensional variational assimilation. I, Experimental results with simplified physics, Quarterly Journal of the Royal Meteorological Society 126(564) (2000) 1143-1170
    locator: the operational incremental system with simplified physics in the inner loop
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Section 5.6 (methods with an evolving forecast error covariance, 4D-Var and the Kalman filter)
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Incremental 4D-Var solves the [4D-Var](/four-dimensional-variational-assimilation/) problem as a sequence of quadratic problems. An outer loop runs the full nonlinear model from the current initial state and computes the departures of the observations from that trajectory. An inner loop then finds the increment $\delta x_0$ that minimizes a quadratic cost in which the change of the trajectory is given by a linear model along the stored trajectory, the tangent linear model or a cheaper simplified version of it, usually at a lower resolution. The increment updates the initial state, and the next outer loop relinearizes. With the exact tangent linear model each outer loop is one step of the [Gauss-Newton algorithm](/gauss-newton-algorithm/) for the 4D-Var cost (Lawless, Gratton and Nichols 2005), and for a linear model one outer loop is enough. This is the form in which every operational 4D-Var system runs.

## In plain words

Searching directly for the best start state with the full weather model is too expensive, because every trial needs a full model run. The incremental method splits the work. It runs the full model once and records how far each measurement is from that run. Then it works only with a simpler linear version of the model, which says how a small change of the start state moves the run. With this simple version the best small change is the answer to a single quadratic problem, which a cheap iterative method solves. The method adds the change to the start state, runs the full model again, and repeats a few times.

## The problem

**Input.** As for [4D-Var](/four-dimensional-variational-assimilation/): a background $x^b$ with error covariance $B$, the full model steps $M_k$, a linear inner model along a trajectory with its exact transpose, and observations $y_k$ with operators $H_k$ and error covariances $R_k$ at the times $k \in T$ of the window $0, \ldots, K$. Notation of Ide, Courtier, Ghil and Lorenc (1997).

**Output.** The initial state $x_0^a$ after the outer loops. With the exact tangent linear model it is a stationary point of the 4D-Var cost

$$J(x_0) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k \in T} \tfrac12 d_k^\top R_k^{-1} d_k, \qquad d_k = y_k - H_k M_{0 \to k}(x_0).$$

The inner cost of one outer loop, with $L_k$ the linear inner model from time $0$ to time $k$, is

$$\tilde J(\delta x_0) = \tfrac12 (x_0 + \delta x_0 - x^b)^\top B^{-1}(x_0 + \delta x_0 - x^b) + \sum_{k \in T} \tfrac12 (d_k - H_k L_k \delta x_0)^\top R_k^{-1}(d_k - H_k L_k \delta x_0).$$

## The algorithm

```pseudo id=main
INCREMENTAL-4DVAR(x^b, B, {y_k, H_k, R_k}, M, L, L^T)
L1  x_0 <- x^b
L2  for outer <- 1 to max_outer do
L3      run the full model from x_0 and store x_1, ..., x_K
L4      d_k <- y_k - H_k x_k for k in T                     ▷ departures from the full model
L5      b <- -B^-1 (x_0 - x^b) + sum_k L_k^T H_k^T R_k^-1 d_k   ▷ one adjoint run
L6      A v = B^-1 v + sum_k L_k^T H_k^T R_k^-1 H_k L_k v   ▷ one linear run and one adjoint run
L7      dx_0 <- solve A dx_0 = b by conjugate gradients     ▷ the inner loop
L8      x_0 <- x_0 + dx_0
L9      if |dx_0| <= tol (1 + |x_0|) then break
L10 return x_0
```

Line L6 never forms $A$: a product $Av$ runs the linear model forward from $v$, applies $H_k^\top R_k^{-1} H_k$ at each observation time, and runs the adjoint backward, the template of the [adjoint model](/adjoint-model/) page. With the exact tangent linear model, $b$ of line L5 is minus the gradient of $J$ and $A$ is the Gauss-Newton matrix. In operational systems the increment lives on a coarser grid than the full model, the inner linear model has simplified physics, and the inner loop minimizes over a [control variable](/control-variable-transform/) $v$ with $\delta x_0 = Uv$, which replaces $B^{-1}$ by the identity.

## Example

**A square model.** Take $x_1 = x_0^2$ ($K = 1$), $x^b = 1$, $B = 1$, and one observation $y_1 = 2$ with $H = R = 1$. The full cost is $J(x_0) = \tfrac12 (x_0 - 1)^2 + \tfrac12 (2 - x_0^2)^2$, and $J'(x_0) = 2x_0^3 - 3x_0 - 1 = (x_0 + 1)(2x_0^2 - 2x_0 - 1)$, so the minimizer is $(1 + \sqrt 3)/2 = 1.3660254$.

Outer loop 1 at $x_0 = 1$: $x_1 = 1$, $d_1 = 1$, and the tangent linear model is multiplication by $2x_0 = 2$. The inner cost is $\tfrac12 \delta^2 + \tfrac12 (1 - 2\delta)^2$, with minimizer $\delta = 2/5$, so $x_0 = 1.4$.

Outer loop 2 at $x_0 = 1.4$: $x_1 = 1.96$, $d_1 = 0.04$, and the tangent linear model is multiplication by $2.8$. The inner cost $\tfrac12 (0.4 + \delta)^2 + \tfrac12 (0.04 - 2.8\delta)^2$ has the minimizer $\delta = -0.288/8.84$, so $x_0 = 1.3674208$.

The reference code continues:

| outer loop | $x_0$ | $J(x_0)$ | error |
|---|---|---|---|
| 0 | 1.0000000 | 0.5000000 | 3.7e-1 |
| 1 | 1.4000000 | 0.0808000 | 3.4e-2 |
| 2 | 1.3674208 | 0.0759699 | 1.4e-3 |
| 3 | 1.3660701 | 0.0759619 | 4.5e-5 |
| 4 | 1.3660268 | 0.0759619 | 1.4e-6 |
| 5 | 1.3660254 | 0.0759619 | 4.5e-8 |

The error falls by a factor of about 0.032 per outer loop: Gauss-Newton converges only linearly here, because the residual $2 - x_1 = 0.134$ at the minimum is not zero.

**An inexact inner model.** On a Lorenz-63 window of 20 forward Euler steps with $\Delta t = 0.01$, the exact tangent linear model converges in 8 outer loops to a point where the full gradient is below $10^{-8}$. With the tangent linear model scaled by 0.9 and its own transpose, the loop still converges, in 43 outer loops, but to a point 0.21 away, where the full gradient has a component of 1.15 and the cost is 3.77 instead of 3.64 (a measurement). This is the effect that Lawless, Gratton and Nichols (2005) analyze.

## Correctness

The [proof](proofs/correctness.md) shows that $A$ is symmetric positive definite, so each inner problem has a unique minimizer, and that with the exact tangent linear model $b = -\nabla J(x_0)$ and $A$ is the Gauss-Newton matrix of the 4D-Var least squares problem (a theorem). So each outer loop is a Gauss-Newton step and a descent direction for $J$. For a linear model the inner cost equals the full cost, and the first outer loop returns the 4D-Var minimizer, which is the Kalman smoother estimate. With an inexact inner model, a fixed point solves a different equation and is in general not a stationary point of $J$. The tests check the outer iterates against a Gauss-Newton step built with a finite difference Jacobian, the linear case against a Kalman filter and smoother to $10^{-8}$, and the inner sweeps with the dot product test.

## Complexity

An outer loop costs one full model run, $Kc$, and the inner loop costs one linear run and one adjoint run per conjugate gradient step, $\Theta(Ks)$ with $s$ the cost of one step of the inner linear model, and the dense operators of the reference code add $\Theta(n^2 + np)$. With $k$ outer loops of $m$ inner steps the time is $\Theta(n^3 + k(Kc + m(Ks + n^2 + np)))$, where $n^3$ is the Cholesky factorization of $B$. The saving over plain 4D-Var comes from $s$: an inner model at a coarser resolution and with simplified physics costs a small fraction of the full model. Operational systems use 2 to 4 outer loops and some tens of inner steps each (a rule of thumb, not a bound). The memory is the stored trajectory, $\Theta(Kn)$.

## Properties

- **Gauss-Newton.** With the exact tangent linear model the outer loop is the Gauss-Newton method for the 4D-Var cost (a theorem). It converges fast when the residuals at the minimum are small and the model is close to linear over the window, and only linearly otherwise.
- **Exact for linear models.** One outer loop with an exact inner solve gives the 4D-Var minimizer (a theorem).
- **Inner problems are convex.** Each inner cost is a strictly convex quadratic, so the conjugate gradient method is the natural solver, and it can be stopped early.
- **The inner model changes the answer.** With a simplified or lower resolution inner model the fixed point moves (a theorem for the fixed point equation; the size of the shift is a measurement).
- **No global convergence guarantee.** Full Gauss-Newton steps can increase $J$ far from the minimum. Operational systems rely on a good background and a short window instead of a line search.

## Variants and improvements

- **Multi-incremental 4D-Var.** Use a coarse inner grid in the first outer loop and finer grids in later ones.
- **Truncated inner loops.** Stop the conjugate gradient method after a fixed number of steps. This is a truncated Gauss-Newton method, and its convergence depends on the inner accuracy (Gratton, Lawless and Nichols 2007).
- **Lanczos inner solvers.** A [Lanczos](/lanczos-algorithm/) form of the conjugate gradient method also gives eigenvalue estimates of the inner Hessian, used to precondition later outer loops and to estimate the analysis error variances.
- **Dual form.** Solve the inner problem in observation space, with $p$ unknowns instead of $n$, as in the physical space analysis system and the [representer method](/representer-method/).
- **Weak constraint and ensembles.** The same outer and inner structure carries over to [weak-constraint 4D-Var](/weak-constraint-4d-var/) and to [4DEnVar](/four-dimensional-ensemble-variational/), where an ensemble replaces the linear model.

## When to use it

Use the incremental form whenever 4D-Var runs with a large model: it is the practical way to do 4D-Var, and the same structure suits 3D-Var with a nonlinear observation operator. Choose the resolution and physics of the inner model as a trade-off between cost and the shift of the solution that an inexact inner model causes. If the model is strongly nonlinear over the window, add outer loops or shorten the window.

## Pitfalls

- **Departures from the linear model (line L4).** The departures must come from the full nonlinear model at the current $x_0$. Computing them with the linear model removes the nonlinearity that the outer loop is there to capture.
- **An adjoint that is not the transpose of the inner model (lines L5 and L6).** Then $A$ is not symmetric, and the conjugate gradient method fails or converges to a wrong point. Check the transpose with the dot product test for the inner model actually used.
- **Inner and outer resolutions.** The increment must be interpolated from the coarse grid to the full grid, and the full departures must be passed to the coarse grid in a consistent way, or the outer loop does not converge.
- **Too few outer loops for a nonlinear problem.** One outer loop gives the right answer only for a linear model. For nonlinear observation operators, such as for clouds and precipitation, the result after one loop can be far from the minimum.
- **Stopping the inner loop too early (line L7).** The increment is then not the inner minimizer, and the outer loop is not a full Gauss-Newton step.

## Implementations

## History

Courtier, Thépaut and Hollingsworth proposed the incremental approach in 1994 as a way to make 4D-Var affordable for a global weather model: the increment is found at a lower resolution, with a simplified linear model, inside outer loops that use the full model. ECMWF started operational 4D-Var in this form in November 1997, with simplified physics in the inner loop (Rabier et al. 2000). Lawless, Gratton and Nichols showed in 2005 that incremental 4D-Var is a Gauss-Newton method and studied the effect of non-tangent linear inner models, and Gratton, Lawless and Nichols gave the convergence theory of the truncated form in 2007.

## References
