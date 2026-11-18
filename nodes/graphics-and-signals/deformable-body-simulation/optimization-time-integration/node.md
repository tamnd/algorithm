---
tag: VE7FP8
kind: technique
slug: optimization-time-integration
name: Optimization-based time integration
aliases:
- variational implicit Euler
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Write a backward Euler step as the minimization of inertia plus potential energy and solve it with Newton's method, a descent test and a line search, so the objective never rises in a step.
prereqs: [backward-euler-method, newton-method-for-systems, backtracking-line-search]
see_also: [projective-dynamics, vertex-block-descent, incremental-potential-contact, affine-body-dynamics, fast-mass-spring, wolfe-conditions, conjugate-gradient-method, convex-function]
sources:
  - paper: doi:10.1109/TVCG.2015.2459687
    title: "Theodore Gast, Craig Schroeder, Alexey Stomakhin, Chenfanfu Jiang and Joseph Teran, Optimization integrator for large time steps, IEEE Transactions on Visualization and Computer Graphics 21(10), 2015, 1103 to 1115"
    locator: "the minimization form of backward Euler and the safeguarded Newton method, extended to the material point method for snow (general locator)"
  - paper: doi:10.2312/sca.20141120
    title: "Theodore Gast and Craig Schroeder, Optimization integrator for large time steps, Proceedings of the ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA 2014), 31 to 40"
    locator: "Section 2 (backward Euler and the failure of plain Newton at large steps, Figures 3, 4 and 7), Section 2.1 (the objective E), Section 3.1 (the Newton steps, the descent test with kappa = 10^-2, the length clamp and the line search)"
---

Optimization time integration solves a [backward Euler](/backward-euler-method/) step as a minimization problem. The new positions are the minimizer of an objective $E$, the sum of an inertia term and the potential energy, so a nonlinear solve becomes the search for a minimum. Gast and Schroeder (2014), and Gast, Schroeder, Stomakhin, Jiang and Teran (2015), solve it with [Newton's method](/newton-method-for-systems/), a descent test and a [line search](/backtracking-line-search/). With these safeguards, $E$ cannot rise from one iteration to the next (proved), and in the tests below the solver reaches a lower $E$ at large time steps where plain Newton stalls or stops at a worse point (measured).

## In plain words

An implicit step asks where the objects must be at the end of the step so that the forces and the change of velocity agree. You can turn this question into a landscape: one hill pulls each point toward where it would go if nothing pushed it, and the stored energy of the springs adds hills and valleys. The answer is the bottom of a valley. Plain Newton jumps toward a point where the ground is flat, which can be the top of a hill or a saddle. The safeguarded method checks that each jump goes downhill, and it shortens the jump until the ground is really lower. So it always walks down, even with large steps.

## When it applies

- **Forces with a potential.** The method needs a potential energy $\Phi$ with $f = -\nabla\Phi$: elastic springs, [hyperelastic](/hyperelastic-material/) finite elements, gravity and barrier contact. Damping and friction have no potential in general and need extra terms.
- **Large time steps.** Backward Euler is stable for stiff systems, but each step is a nonlinear system. At large $\Delta t$ the start point is far from the solution, and plain Newton can fail (Section 2 of the 2014 paper shows this at $\Delta t = 1/24$ s).
- **A bounded objective.** The safeguards guarantee descent. They are useful when $E$ is bounded below, which is true for nonnegative elastic energies plus linear gravity (proved in [proofs/correctness.md](proofs/correctness.md)).
- **Inexact solves.** The minimization form gives a measure of progress. A solve can stop after a few iterations and still have a lower $E$ than its start point.

## The template

For a step from $(x_n, v_n)$ with mass matrix $M$:

$$E(z) = \frac{1}{2\Delta t^2}(z - \hat x)^T M (z - \hat x) + \Phi(z), \qquad \hat x = x_n + \Delta t\, v_n.$$

Its gradient is zero exactly at a backward Euler step $M(v_{n+1} - v_n) = \Delta t\, f(x_{n+1})$ with $v_{n+1} = (x_{n+1} - x_n)/\Delta t$ (proved).

```pseudo id=main
OTI-STEP(x, v, Δt)
L1  x̂ <- x + Δt v
L2  z <- x̂ + Δt² M⁻¹ f(x)                       ▷ the initial guess
L3  repeat up to max_iter times:
L4      g <- ∇E(z);  H <- ∇²E(z)
L5      if |g| < τ: stop
L6      d <- the solution of H d = -g
L7      if d·g ≥ -κ |d| |g|: d <- -d;  if still: d <- -g    ▷ κ = 10⁻²
L8      if |d| > ℓ: d <- ℓ d / |d|                  ▷ ℓ = 10³
L9      t <- a step length with E(z + t d) ≤ E(z) + c t d·g
L10     z <- z + t d
L11 v <- (z - x) / Δt;  x <- z
```

L7 to L9 are the safeguards of Section 3.1 of the 2014 paper. The paper solves L6 with [conjugate gradients](/conjugate-gradient-method/) and uses a line search with the strong [Wolfe conditions](/wolfe-conditions/). The code solves L6 with a dense Gaussian elimination and uses Armijo backtracking with $c = 10^{-4}$. It simulates a 2D chain of springs with gravity, with the first particle pinned. In floating point the code also stops when the predicted decrease $-t\, d \cdot g$ is below the rounding level of $E$.

The proofs are in [proofs/correctness.md](proofs/correctness.md). These are the claims:

1. A point with $\nabla E = 0$ is a backward Euler step (proved).
2. After L7 and L8 the direction goes downhill, $d \cdot g < 0$ (proved).
3. The line search ends, and $E$ does not rise from one iteration to the next (proved).
4. For a quadratic $\Phi$ with a well conditioned $H$, one iteration gives the exact step (proved). The test compares this with a direct linear solve.
5. For a [convex](/convex-function/) $\Phi$, the exact step loses at least $\frac12 |v_{n+1} - v_n|_M^2$ of total energy (proved). For a nonconvex $\Phi$ this is not guaranteed.
6. With gravity only, the step is the [symplectic Euler](/symplectic-euler-method/) step (proved).

## Classic examples

**A falling chain (measured).** A chain of 8 particles with spacing 0.1 m, stiffness $10^4$ and mass 0.1 starts horizontal at rest, hangs from its first particle and falls for 2 s, with $\tau = 10^{-6}$. The total energy $\frac12 v^T M v + \Phi$ starts at 0.

| $1/\Delta t$ | energy at 1 s | energy at 2 s | steps where the energy rose | largest iterations | mean iterations |
|---|---|---|---|---|---|
| 24 | -2.000 | -2.488 | 0 | 8 | 4.44 |
| 96 | -1.010 | -1.718 | 0 | 3 | 2.22 |
| 384 | -0.402 | -1.002 | 0 | 2 | 1.37 |

The energy falls more at larger $\Delta t$, which is the numerical damping of backward Euler. The springs have a nonconvex energy, so claim 5 does not cover this chain; the decay here is measured. For linear springs (rest length zero, stiffness 100) at $\Delta t = 1/24$ s, the smallest value of $(\mathcal E_n - \mathcal E_{n+1}) - \frac12|v_{n+1} - v_n|_M^2$ over 48 steps is $6.3 \times 10^{-6} \ge 0$, as claim 5 says.

**Crumpled start points (measured).** The same chain starts in a crumpled state: particle $i$ is at $(0.02 i + u, w)$ with $u, w$ uniform in $[-0.03, 0.03]$, with seeds 0 to 5, and at rest. One step is solved with the safeguards and with plain Newton (full steps, no tests). The table gives the iterations and the final $E$, and for plain Newton the number of iterations where $E$ rose.

| $\Delta t$ | seed | start $E$ | safeguarded | plain Newton |
|---|---|---|---|---|
| 1/24 | 0 | $3.6 \times 10^7$ | 15, 0.326 | 13, 0.326, 3 rises |
| 1/24 | 1 | $2.3 \times 10^7$ | 34, 0.438 | 100, 0.603, 47 rises, no convergence |
| 1/24 | 2 | $3.5 \times 10^7$ | 15, 0.219 | 69, 0.219, 32 rises |
| 1/24 | 3 | $1.6 \times 10^7$ | 22, 0.517 | 71, 1.592, 32 rises |
| 1/24 | 4 | $3.5 \times 10^7$ | 16, 0.272 | 15, 1.070, 7 rises |
| 1/24 | 5 | $2.8 \times 10^7$ | 43, 0.414 | 19, 0.849, 7 rises |
| 1 | 0 | $1.2 \times 10^{13}$ | 55, -2.679 | 5, 0.391, 2 rises |
| 1 | 1 | $7.7 \times 10^{12}$ | 48, -1.362 | 5, 0.787, 2 rises |
| 1 | 2 | $1.2 \times 10^{13}$ | 49, -0.977 | 5, 0.390, 2 rises |
| 1 | 3 | $5.2 \times 10^{12}$ | 48, -1.349 | 6, 0.985, 3 rises |
| 1 | 4 | $1.2 \times 10^{13}$ | 59, -2.684 | 7, -0.199, 3 rises |
| 1 | 5 | $9.3 \times 10^{12}$ | 62, -2.496 | 6, 1.585, 3 rises |

Plain Newton often converges to a stationary point with a higher $E$, and in one case it does not converge in 100 iterations. The safeguarded solver never raises $E$ and always ends at an $E$ at most as high. Its end points are not always minima: the Hessian there is not always positive definite, so the method guarantees descent, not a minimum. For seed 1 at $\Delta t = 1/24$ s it stopped at the rounding level with $|\nabla E| = 1.6 \times 10^{-6}$, just above $\tau$.

**Methods that minimize the same objective.** [Fast mass springs](/fast-mass-spring/) and [projective dynamics](/projective-dynamics/) minimize $E$ with a local step and a global linear solve. [Vertex block descent](/vertex-block-descent/) minimizes it one vertex at a time. [Incremental potential contact](/incremental-potential-contact/) adds a barrier on distances to $E$ and caps each step by a collision check, and [affine body dynamics](/affine-body-dynamics/) does the same for stiff bodies.

## Variations

- **Krylov solves.** For large systems L6 uses conjugate gradients with a tolerance tied to $|\nabla E|$, and on an indefinite $H$ it returns its last iterate (Section 3.1 of the 2014 paper).
- **Hessian projection.** Many codes project the Hessian of each element to a positive semidefinite matrix. Then $H$ is positive definite and the Newton direction always goes downhill (proved as for claim 4), so only the angle test of L7 can still reject it.
- **Quasi-Newton solvers.** [L-BFGS](/limited-memory-bfgs/) needs only gradients and works with the same line search.
- **Other integrators.** The implicit midpoint rule is also a minimization: its midpoint $y = (x_n + x_{n+1})/2$ minimizes $\frac{2}{\Delta t^2}|y - x_n - \frac{\Delta t}{2} v_n|_M^2 + \Phi(y)$ (proved by the same calculation as claim 1).
- **Constraints and contact.** Contact can enter the minimization as constraints, as penalty terms or as barrier terms. IPC uses a barrier.

## Pitfalls

- **A stationary point is not a minimum.** Plain Newton finds any point with $\nabla E = 0$, and at large steps this can be a saddle (the table). Do not take $\nabla E = 0$ as a proof that the state is good.
- **Rounding limits the tolerance.** When $|\nabla E|$ is small, the change of $E$ in a step can be below the rounding level of $E$, and the line search then cannot see a decrease. Choose $\tau$ relative to the scale of the forces, and stop when the predicted decrease is below rounding.
- **Nonsmooth energies.** A spring with a positive rest length has no gradient at length zero. A line search near such a point can stall.
- **Numerical damping.** Backward Euler removes energy, more at larger $\Delta t$ (the first table). The minimization form does not change this.
- **Forces without a potential.** Damping, friction and some follower forces have no potential. They need a separate treatment, often with lagged terms.

## Exercises

1. Show that $\nabla E(z) = 0$ is the same as $M(v_{n+1} - v_n) = \Delta t\, f(x_{n+1})$ with $v_{n+1} = (z - x_n)/\Delta t$.
2. For one particle of mass $m$ on a spring of stiffness $k$ and rest length $r$ to a pinned point, compute the step from $x_n > r$ at rest. Check with $m = 1$, $k = 100$, $r = 1$, $x_n = 1.5$ and $\Delta t = 0.1$ that $x_{n+1} = 1.25$.
3. Show that the direction $-g$ at L7 passes the test of L7 for every $\kappa < 1$.
4. Show that a Newton direction with a positive definite $H$ passes the test of L7 when the condition number of $H$ is smaller than $1/\kappa$.
5. Find a 1D potential $\Phi$ and a start point where a full Newton step raises $E$.
6. Prove that for a convex $\Phi$ the total energy does not rise in an exact backward Euler step.

## References
