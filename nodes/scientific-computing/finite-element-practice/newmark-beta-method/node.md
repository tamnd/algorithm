---
tag: DKETH0
kind: algorithm
slug: newmark-beta-method
name: Newmark-beta method
aliases:
- Newmark method
area: scientific-computing/finite-element-practice
level: core
summary: Steps M a + C v + K d = F in time with parameters beta and gamma. beta = 1/4, gamma = 1/2 is second order and unconditionally stable for linear problems only.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {n: the number of unknowns, b: the half bandwidth of the effective matrix, m: the number of time steps}
  time: {worst: "Θ(n b^2 + m n b)"}
  space: {extra: "Θ(n b)"}
properties: {deterministic: true, one_step: true, implicit: "for beta > 0", order: "2 if gamma = 1/2, else 1", unconditionally_stable_linear: "for 2 beta >= gamma >= 1/2", conserves_linear_energy: "for beta = 1/4 and gamma = 1/2"}
history:
  year: 1959
  people: [Nathan M. Newmark]
  note: Newmark published the two-parameter family in 1959 for the dynamic response of structures to blast and earthquake loads.
prereqs: [finite-element-method, ode-initial-value-problem, mass-lumping]
see_also: [generalized-alpha-method, crank-nicolson-method, trapezoidal-rule, verlet-integration, a-stability, stiff-ode-problem, wave-equation, newton-method-for-systems]
sources:
  - paper: doi:10.1061/JMCEA3.0000098
    title: N. M. Newmark, A method of computation for structural dynamics, Journal of the Engineering Mechanics Division (ASCE) 85(3) (1959) 67-94
    locator: the two-parameter step for displacement and velocity, with the stability limits
  - book: isbn:9780486411811
    title: Thomas J. R. Hughes, The Finite Element Method, Linear Static and Dynamic Finite Element Analysis, Dover, 2000
    locator: Chapter 9 (the Newmark method, its stability and accuracy analysis, numerical dissipation and dispersion)
  - paper: doi:10.1016/0045-7949(76)90007-9
    title: T. J. R. Hughes, Stability, convergence and growth and decay of energy of the average acceleration method in nonlinear structural dynamics, Computers and Structures 6(4-5) (1976) 313-324
    locator: energy of the average acceleration method for nonlinear problems
  - paper: doi:10.1007/BF00913408
    title: J. C. Simo and N. Tarnow, The discrete energy-momentum method. Conserving algorithms for nonlinear elastodynamics, Zeitschrift fur angewandte Mathematik und Physik 43(5) (1992) 757-792
    locator: loss of stability of the trapezoidal rule in nonlinear elastodynamics, and energy-momentum conserving schemes
---

The Newmark-beta method is a one-step time integrator for the second order equations of structural dynamics $M\ddot d + C\dot d + K d = F(t)$, which come from a [finite element](/finite-element-method/) discretization in space. It advances displacement $d$, velocity $v$ and acceleration $a$ with two parameters $\beta$ and $\gamma$: $\gamma = \tfrac12$ gives second order accuracy, $\beta = 0$ gives the explicit central difference method, and $\beta = \tfrac14$, $\gamma = \tfrac12$ gives the implicit average acceleration rule, which is unconditionally stable and conserves the energy exactly for linear undamped problems. Unconditional stability is a property of linear problems: for nonlinear problems the same rule can let the energy grow. Graphics simulators of cloth and soft bodies often step with backward Euler, which is stable but damps every motion strongly, and Newmark with $\beta = \tfrac14$ adds second order accuracy and no artificial damping at the price of the same one linear solve per step.

## In plain words

A vibrating structure moves, so its position, its speed and its rate of change of speed change at every instant. A computer can only look at the structure at separate moments, a small time apart. The Newmark method gets the next position and speed from the current ones and from a guess about how the speed changes during the step. One setting assumes that the rate of change of speed is the average of its values at the start and the end of the step. This setting never blows up for a linear structure, whatever the size of the step, and it keeps the energy of a free vibration exactly. Another setting uses only the start values. That one is cheap, but it fails when the step is too long compared with the fastest vibration.

## The problem

**Input.** A symmetric positive definite mass matrix $M$, a damping matrix $C$ and a stiffness matrix $K$, all $n \times n$, a load $F(t)$, initial values $d_0$ and $v_0$, a time step $dt$ and a number of steps $m$. On finite element pages $h$ is the mesh size, so the time step is $dt$ here.

**Output.** Approximations $d_k \approx d(t_k)$, $v_k \approx \dot d(t_k)$ and $a_k \approx \ddot d(t_k)$ at $t_k = k\,dt$ for $k = 0, \ldots, m$, such that $M a_k + C v_k + K d_k = F(t_k)$ holds at every step and

$$d_{k+1} = d_k + dt\, v_k + \frac{dt^2}{2}\big((1 - 2\beta) a_k + 2\beta a_{k+1}\big), \qquad v_{k+1} = v_k + dt\big((1 - \gamma) a_k + \gamma a_{k+1}\big).$$

## The algorithm

The step first forms predictors $\tilde d$ and $\tilde v$ from the old values, then solves one linear system for the new acceleration, then corrects.

```pseudo id=main
NEWMARK(M, C, K, F, d_0, v_0, dt, m, beta, gamma)
L1  a_0 <- solve M a = F(0) - C v_0 - K d_0
L2  for k <- 0 to m - 1 do
L3      dp <- d_k + dt v_k + (dt^2 / 2)(1 - 2 beta) a_k        ▷ displacement predictor
L4      vp <- v_k + (1 - gamma) dt a_k                         ▷ velocity predictor
L5      a_{k+1} <- solve (M + gamma dt C + beta dt^2 K) a = F(t_{k+1}) - C vp - K dp
L6      d_{k+1} <- dp + beta dt^2 a_{k+1}
L7      v_{k+1} <- vp + gamma dt a_{k+1}
L8  return (d_k, v_k, a_k) for k = 0 .. m
```

The matrix $M^* = M + \gamma\,dt\,C + \beta\,dt^2 K$ of line L5 does not change when $dt$ is fixed, so a code factors it once. With $\beta = 0$, $C = 0$ and a diagonal (lumped) $M$, line L5 is a division per unknown and the method is explicit.

**Nonlinear problems.** For an internal force $f_{\rm int}(d)$ in place of $K d$, line L5 becomes the nonlinear equation $M a + C(\tilde v + \gamma\,dt\,a) + f_{\rm int}(\tilde d + \beta\,dt^2 a) = F(t_{k+1})$. A [Newton iteration](/newton-method-for-systems/) solves it with the matrix $M + \gamma\,dt\,C + \beta\,dt^2 K_T(d)$, where $K_T = \partial f_{\rm int}/\partial d$ is the tangent stiffness at the current iterate. The reference code does this in `newmark_nonlinear`.

**Common members of the family.**

| name | $\beta$ | $\gamma$ | type | order | stable for $\omega\,dt$ (undamped) |
|---|---|---|---|---|---|
| central difference | $0$ | $\tfrac12$ | explicit with lumped $M$ | 2 | $\le 2$ |
| Fox-Goodwin | $\tfrac1{12}$ | $\tfrac12$ | implicit | 2 | $\le \sqrt6 = 2.449$ |
| linear acceleration | $\tfrac16$ | $\tfrac12$ | implicit | 2 | $\le \sqrt{12} = 3.464$ |
| average acceleration (trapezoidal rule) | $\tfrac14$ | $\tfrac12$ | implicit | 2 | all |
| damped Newmark | $\tfrac14(\gamma + \tfrac12)^2$ | $> \tfrac12$ | implicit | 1 | all |

Here $\omega$ is the highest natural frequency of the mesh, the square root of the largest eigenvalue of $K x = \omega^2 M x$. The table holds for $C = 0$. The limit for $\gamma \ge \tfrac12$ and $2\beta < \gamma$ is $\omega\,dt \le (\gamma/2 - \beta)^{-1/2}$.

## Example

**One step by hand.** Take $m = k = 1$ (so $\omega = 1$), no damping, no load, $d_0 = 1$, $v_0 = 0$, $dt = \tfrac12$, and the average acceleration rule. Line L1 gives $a_0 = -1$. Line L3 gives $\tilde d = 1 + 0 + \tfrac18 \cdot \tfrac12 \cdot (-1) = \tfrac{15}{16}$ and line L4 gives $\tilde v = -\tfrac14$. Line L5 solves $(1 + \tfrac14 \cdot \tfrac14)\,a_1 = -\tfrac{15}{16}$, so $a_1 = -\tfrac{15}{17}$. Then $d_1 = \tfrac{15}{16} - \tfrac1{16}\cdot\tfrac{15}{17} = \tfrac{15}{17}$ and $v_1 = -\tfrac14 - \tfrac14 \cdot \tfrac{15}{17} = -\tfrac{8}{17}$. The energy $\tfrac12(v_1^2 + d_1^2) = \tfrac12 \cdot \tfrac{64 + 225}{289} = \tfrac12$ is the initial energy. The exact values are $\cos\tfrac12 = 0.87758$ and $-\sin\tfrac12 = -0.47943$.

| $k$ | $d_k$ | $v_k$ | exact $\cos t_k$ | exact $-\sin t_k$ |
|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 0 |
| 1 | 15/17 = 0.88235 | -8/17 = -0.47059 | 0.87758 | -0.47943 |
| 2 | 161/289 = 0.55709 | -240/289 = -0.83045 | 0.54030 | -0.84147 |
| 3 | 495/4913 = 0.10075 | -4888/4913 = -0.99491 | 0.07074 | -0.99749 |
| 4 | -0.37929 | -0.92528 | -0.41615 | -0.90930 |

The discrete solution is $d_k = \cos(k\theta)$, $v_k = -\sin(k\theta)$ with $\theta = 2\arctan(\omega\,dt/2) = 0.48996$ per step in place of $0.5$. The amplitude is exact and the phase lags: the period grows by the factor $\omega\,dt / (2\arctan(\omega\,dt/2))$, which is $1.0205$ for $\omega\,dt = \tfrac12$, $1.0784$ for $\omega\,dt = 1$ and $1.2732$ for $\omega\,dt = 2$. For small steps the relative period error is about $(\omega\,dt)^2/12$.

**Other members on the same problem.** After 4 steps of $dt = \tfrac12$ (at $t = 2$, exact $d = -0.41615$) the central difference method gives $d_4 = -0.43555$, Fox-Goodwin $-0.41639$ and linear acceleration $-0.39764$. Fox-Goodwin is the most accurate of the four here, but it is only conditionally stable.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). Three facts carry the method.

- **Consistency and order.** Insert the exact solution into the two update formulas. The velocity formula has a residual $(\tfrac12 - \gamma)\,dt^2\,\dddot d + O(dt^3)$ and the displacement formula $(\tfrac16 - \beta)\,dt^3\,\dddot d + O(dt^4)$. So the [local truncation error](/local-truncation-error/) per unit time is $O(dt)$ unless $\gamma = \tfrac12$, and $O(dt^2)$ when $\gamma = \tfrac12$. For the average acceleration rule the proof bounds the [global error](/global-error/) in the energy norm by $C\,T\,dt^2$ directly. For the other stable members the global error has the order of the local one by the usual stability argument (Hughes 2000, Chapter 9), and the reference tests measure orders 2 and 1.
- **Stability for linear problems.** For one mode $\ddot d + \omega^2 d = 0$, the displacements satisfy the three-term recurrence $(1 + \beta\Omega^2) d_{k+1} - (2 - (\tfrac12 - 2\beta + \gamma)\Omega^2) d_k + (1 + (\tfrac12 + \beta - \gamma)\Omega^2) d_{k-1} = 0$ with $\Omega = \omega\,dt$. For $\Omega > 0$ the steps stay bounded exactly when $\gamma \ge \tfrac12$ and either $2\beta \ge \gamma$ or $\Omega^2 \le 2/(\gamma - 2\beta)$, with strict inequality when $\gamma = \tfrac12$. The modes of $K x = \omega^2 M x$ with $C = 0$ decouple, so the same holds for the full system.
- **Energy.** For $\beta = \tfrac14$, $\gamma = \tfrac12$, $C = 0$ and $F = 0$, the quantity $\tfrac12 v_k^\top M v_k + \tfrac12 d_k^\top K d_k$ is the same at every step, for any $dt$, by a two-line identity.

## Complexity

In the [real-RAM model](/real-ram/), for a linear problem with fixed $dt$, the effective matrix is factored once. For a banded matrix with half bandwidth $b$, as from a finite element mesh with a good node order, the Cholesky factorization costs $\Theta(n b^2)$ and each step costs $\Theta(n b)$ for the matrix-vector products and the two triangular solves. The total for $m$ steps is $\Theta(n b^2 + m n b)$, and the memory is $\Theta(n b)$ for the factor. The explicit case ($\beta = 0$, lumped $M$, $C$ diagonal or zero) needs no factorization, and a step costs one product with $K$, $\Theta(\text{nnz}(K))$, but $dt$ must stay below $2/\omega_{\max}$, and $\omega_{\max}$ grows like $1/h$ for a mesh of size $h$. A nonlinear step costs one tangent assembly and one factorization per Newton iteration. Newton converges locally and quadratically when the tangent is exact and the predictor is close enough; the number of iterations is a measurement (at most 2 corrections per step to a residual of $10^{-12}$ for the Duffing test of the reference code, with 50 to 200 steps). The reference code uses dense Gaussian elimination from `scimat`, so it costs $\Theta(n^3)$ per step and is meant only for small systems.

## Properties

- **Second order exactly when $\gamma = \tfrac12$.** Any $\gamma > \tfrac12$ adds numerical damping and drops the order to 1.
- **No amplitude error for the trapezoidal rule.** Both roots have modulus 1 for every $\Omega$, so the method neither damps nor amplifies a linear mode. The price is that high, unresolved modes of a coarse mesh also keep their full amplitude.
- **Equivalent forms.** With $\beta = \tfrac14$, $\gamma = \tfrac12$ the method is the [trapezoidal rule](/trapezoidal-rule/) applied to the first order system $\dot d = v$, $M\dot v = F - C v - K d$. With $\beta = 0$, $\gamma = \tfrac12$ the displacements satisfy $M(d_{k+1} - 2d_k + d_{k-1})/dt^2 + K d_k = F_k$ when $C = 0$, the central difference method, which for $M = I$ is the position form of [Verlet integration](/verlet-integration/).
- **Not L-stable.** The trapezoidal rule has spectral radius 1 as $\Omega \to \infty$, so it is [A-stable](/a-stability/) but does not damp stiff modes, in contrast with [backward Euler](/backward-euler-method/).
- **Symplectic members.** For $\gamma = \tfrac12$ the method conserves a modified quadratic energy for linear problems. For $\beta = 0$ it is the symplectic Stormer-Verlet scheme also for nonlinear forces.

## Variants and improvements

- **[Generalized-alpha method](/generalized-alpha-method/).** Evaluate the equation of motion at shifted times inside the step. This keeps second order and gives a chosen amount of damping of the high modes, which Newmark can only get with $\gamma > \tfrac12$ and first order.
- **HHT-alpha and WBZ-alpha.** The two special cases of the generalized-alpha family, which shift only the stiffness and damping terms (Hilber, Hughes and Taylor) or only the inertia term (Wood, Bossak and Zienkiewicz).
- **d-form and v-form.** Solve for $d_{k+1}$ or $v_{k+1}$ in place of $a_{k+1}$. The three forms give the same values in exact arithmetic. The d-form is common in nonlinear codes, because the tangent acts on the displacement.
- **Explicit predictor-corrector.** Use the predictors as the new values and the old acceleration in the force evaluation. This is explicit for any $\beta$ but has a step limit.
- **Energy-momentum methods.** For nonlinear elastodynamics, replace the trapezoidal force average by a discrete gradient so that energy, linear momentum and angular momentum are all conserved (Simo and Tarnow 1992).

## When to use it

Use the average acceleration rule for linear and mildly nonlinear structural dynamics where the response of interest is in the low modes and you want no artificial damping, for example the response of a building to an earthquake record. Use the central difference member with a lumped mass matrix for short events such as impact, crash and wave propagation, where the step must be small anyway to resolve the physics. When the mesh has spurious high modes that must be damped, or when a nonlinear problem shows energy growth, use the [generalized-alpha method](/generalized-alpha-method/) in place of $\gamma > \tfrac12$.

## Pitfalls

- **Unconditional stability is only for linear problems.** For nonlinear problems the energy of the trapezoidal rule can grow without bound for large steps (Hughes 1976, Simo and Tarnow 1992). A large step that works for the linearized problem can fail on the nonlinear one.
- **Damping by $\gamma > \tfrac12$.** It damps the high modes, but it also loses second order for all modes. The error then grows linearly in $dt$.
- **The explicit limit uses the highest frequency.** The limit $dt \le 2/\omega_{\max}$ comes from the stiffest element of the mesh, not from the physics. One small or very stiff element limits the whole model. The consistent mass matrix gives a larger $\omega_{\max}$ than the lumped one, so it gives a smaller stable step.
- **Initial acceleration.** Line L1 must solve the equation of motion for $a_0$. Setting $a_0 = 0$ for a loaded or displaced start gives a first order error that persists.
- **Undamped high modes with the trapezoidal rule.** A sudden load excites mesh modes that the trapezoidal rule never damps, so the computed velocities and stresses show noise of high frequency that a finer step does not remove.
- **Period error.** The method has no amplitude error but has a phase error. Over many periods the phase error dominates. For the trapezoidal rule the period error is about $(\omega\,dt)^2/12$, so to keep it below 1 percent, use at least about 20 steps per period of the highest mode of interest.

## Implementations

## History

Nathan Newmark published the method in 1959, in a paper on computing the response of structures to blast and earthquake loads, and gave the two parameters, the choice $\gamma = \tfrac12$ for no artificial damping and the stability limits for the linear oscillator. The finite element community made it the standard integrator for structural dynamics in the 1970s. Hughes showed in 1976 that the energy argument for the average acceleration rule fails for nonlinear problems. Hilber, Hughes and Taylor in 1977 and Chung and Hulbert in 1993 added controlled numerical damping without the loss of order. Simo and Tarnow in 1992 gave schemes that conserve energy and momentum for nonlinear elastodynamics.

## References
