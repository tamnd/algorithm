---
tag: 1NTWAK
kind: algorithm
slug: generalized-alpha-method
name: Generalized-alpha method
aliases:
- Chung-Hulbert method
area: scientific-computing/finite-element-practice
level: advanced
summary: A second order implicit method for structural dynamics with set damping of high frequencies and little damping of low ones; it contains HHT-alpha.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {n: the number of unknowns, b: the half bandwidth of the effective matrix, m: the number of time steps}
  time: {worst: "Θ(n b^2 + m n b)"}
  space: {extra: "Θ(n b)"}
properties: {deterministic: true, one_step: true, implicit: true, order: 2, unconditionally_stable_linear: true, high_frequency_spectral_radius: "rho_inf in [0, 1], chosen by the user"}
history:
  year: 1993
  people: [Jintai Chung, Gregory M. Hulbert]
  note: Chung and Hulbert combined the HHT-alpha and WBZ-alpha shifts into one family with a single parameter rho_inf, the spectral radius at infinite step size.
prereqs: [newmark-beta-method, ode-initial-value-problem]
see_also: [newmark-beta-method, l-stability, a-stability, tr-bdf2, backward-differentiation-formulas, stiff-ode-problem, variational-multiscale-method, isogeometric-analysis]
sources:
  - paper: doi:10.1115/1.2900803
    title: J. Chung and G. M. Hulbert, A time integration algorithm for structural dynamics with improved numerical dissipation. The generalized-alpha method, Journal of Applied Mechanics 60(2) (1993) 371-375
    locator: the method, the parameter choice by rho_inf, the second order condition and the stability analysis
  - paper: doi:10.1002/eqe.4290050306
    title: H. M. Hilber, T. J. R. Hughes and R. L. Taylor, Improved numerical dissipation for time integration algorithms in structural dynamics, Earthquake Engineering and Structural Dynamics 5(3) (1977) 283-292
    locator: the HHT-alpha method
  - paper: doi:10.1002/nme.1620151011
    title: W. L. Wood, M. Bossak and O. C. Zienkiewicz, An alpha modification of Newmark's method, International Journal for Numerical Methods in Engineering 15(10) (1980) 1562-1566
    locator: the WBZ-alpha method
  - paper: doi:10.1016/S0045-7825(00)00203-6
    title: K. E. Jansen, C. H. Whiting and G. M. Hulbert, A generalized-alpha method for integrating the filtered Navier-Stokes equations with a stabilized finite element method, Computer Methods in Applied Mechanics and Engineering 190(3-4) (2000) 305-319
    locator: the generalized-alpha method for first order systems
  - book: isbn:9780486411811
    title: Thomas J. R. Hughes, The Finite Element Method, Linear Static and Dynamic Finite Element Analysis, Dover, 2000
    locator: Chapter 9 (Newmark and HHT-alpha methods, spectral radius, algorithmic damping and period error)
---

The generalized-alpha method is an implicit one-step integrator for the equations of structural dynamics $M\ddot d + C\dot d + K d = F(t)$. It keeps the displacement and velocity updates of the [Newmark-beta method](/newmark-beta-method/), but it enforces the equation of motion at two shifted points inside the step, one for the inertia term and one for the internal and external forces. One parameter $\rho_\infty \in [0, 1]$ sets the spectral radius of the step as $\omega\,dt \to \infty$. So the user picks how strongly the unresolved high modes of the mesh are damped, while the method stays second order and unconditionally stable for linear problems and damps the well resolved low modes very little. Newmark can damp the high modes only with $\gamma > \tfrac12$, which drops it to first order.

## In plain words

When a computer follows a vibrating structure in time, the mesh has many fast vibrations that are not real physics. They come only from the size of the elements. A good time stepper should remove these fast wiggles and leave the slow motion, which is the answer the engineer wants, almost untouched. The Newmark method can either keep everything, or remove the wiggles at the cost of a larger error on the slow motion. The generalized-alpha method moves the points inside the step where the forces are balanced. With one dial the user picks how much of a fast wiggle is left after each step, from all of it to none, and the slow motion keeps full accuracy.

## The problem

**Input.** Matrices $M$ (symmetric positive definite), $C$ and $K$ of size $n \times n$, a load $F(t)$, initial values $d_0$ and $v_0$, a time step $dt$, a number of steps $m$ and $\rho_\infty \in [0, 1]$. On finite element pages $h$ is the mesh size and $dt$ is the time step.

**Output.** Approximations $d_k \approx d(t_k)$ and $v_k \approx \dot d(t_k)$ for $t_k = k\,dt$, $k = 0, \ldots, m$, and an auxiliary acceleration $a_k$, such that the Newmark updates

$$d_{k+1} = d_k + dt\,v_k + dt^2\big((\tfrac12 - \beta) a_k + \beta a_{k+1}\big), \qquad v_{k+1} = v_k + dt\big((1 - \gamma) a_k + \gamma a_{k+1}\big)$$

hold, together with the balance at the shifted points

$$M a_{k+1-\alpha_m} + C v_{k+1-\alpha_f} + K d_{k+1-\alpha_f} = F(t_{k+1-\alpha_f}), \qquad x_{k+1-\alpha} = (1 - \alpha) x_{k+1} + \alpha x_k.$$

The parameters come from $\rho_\infty$:

$$\alpha_m = \frac{2\rho_\infty - 1}{\rho_\infty + 1}, \qquad \alpha_f = \frac{\rho_\infty}{\rho_\infty + 1}, \qquad \gamma = \tfrac12 - \alpha_m + \alpha_f, \qquad \beta = \tfrac14(1 - \alpha_m + \alpha_f)^2.$$

## The algorithm

```pseudo id=main
GENERALIZED-ALPHA(M, C, K, F, d_0, v_0, dt, m, alpha_m, alpha_f, beta, gamma)
L1  a_0 <- solve M a = F(0) - C v_0 - K d_0
L2  for k <- 0 to m - 1 do
L3      dp <- d_k + dt v_k + (dt^2 / 2)(1 - 2 beta) a_k
L4      vp <- v_k + (1 - gamma) dt a_k
L5      r <- F(t_k + (1 - alpha_f) dt) - alpha_m M a_k - C((1 - alpha_f) vp + alpha_f v_k) - K((1 - alpha_f) dp + alpha_f d_k)
L6      a_{k+1} <- solve ((1 - alpha_m) M + (1 - alpha_f)(gamma dt C + beta dt^2 K)) a = r
L7      d_{k+1} <- dp + beta dt^2 a_{k+1}
L8      v_{k+1} <- vp + gamma dt a_{k+1}
L9  return (d_k, v_k, a_k) for k = 0 .. m
```

Lines L3, L4, L7 and L8 are the Newmark predictor and corrector. Lines L5 and L6 are the balance at the shifted points, written as one linear system for $a_{k+1}$ after the Newmark updates are put in. The effective matrix of line L6 is the same for all steps when $dt$ is fixed, so a code factors it once. For a nonlinear internal force, line L6 becomes a [Newton iteration](/newton-method-for-systems/) with the effective tangent $(1 - \alpha_m) M + (1 - \alpha_f)(\gamma\,dt\,C + \beta\,dt^2 K_T)$.

**Members.**

| method | $\alpha_m$ | $\alpha_f$ | when |
|---|---|---|---|
| Newmark-beta | $0$ | $0$ | no shift |
| HHT-alpha (Hilber, Hughes and Taylor 1977) | $0$ | $\alpha \in [0, \tfrac13]$ | shift of the force terms only, $\rho_\infty = (1 - \alpha)/(1 + \alpha)$ |
| WBZ-alpha (Wood, Bossak and Zienkiewicz 1980) | $(\rho_\infty - 1)/(\rho_\infty + 1)$ | $0$ | shift of the inertia term only |
| Chung-Hulbert | as above | as above | both shifts, best ratio of high to low frequency damping |

In each case $\gamma = \tfrac12 - \alpha_m + \alpha_f$ and $\beta = \tfrac14(1 - \alpha_m + \alpha_f)^2$. The original HHT paper writes the parameter with the opposite sign, $\alpha_{\rm HHT} = -\alpha_f \in [-\tfrac13, 0]$.

## Example

**One step by hand.** Take $\ddot d + d = 0$, $d_0 = 1$, $v_0 = 0$, $dt = \tfrac12$ and $\rho_\infty = \tfrac12$. Then $\alpha_m = 0$, $\alpha_f = \tfrac13$, $\gamma = \tfrac56$ and $\beta = \tfrac49$. Line L1 gives $a_0 = -1$. Line L3 gives $\tilde d = 1 + \tfrac18(1 - \tfrac89)(-1) = \tfrac{71}{72}$ and line L4 gives $\tilde v = -\tfrac1{12}$. Line L6 solves $(1 + \tfrac23 \cdot \tfrac49 \cdot \tfrac14)\,a_1 = -\tfrac23 \cdot \tfrac{71}{72} - \tfrac13$, that is $\tfrac{29}{27} a_1 = -\tfrac{107}{108}$, so $a_1 = -\tfrac{107}{116}$. Then $d_1 = \tfrac{71}{72} - \tfrac19 \cdot \tfrac{107}{116} = \tfrac{205}{232} = 0.88362$ and $v_1 = -\tfrac1{12} - \tfrac5{12} \cdot \tfrac{107}{116} = -\tfrac{217}{464} = -0.46767$. The exact values are $0.87758$ and $-0.47943$. Note that $a_1 + d_1 = -\tfrac{9}{232}$ is not zero: the auxiliary $a_k$ does not satisfy the equation of motion at $t_k$. It approximates the acceleration at the earlier time $t_k - (\alpha_f - \alpha_m)\,dt$.

**Damping at the same $\rho_\infty$.** Fix $\rho_\infty = \tfrac{9}{11} = 0.818$ for all four methods: Newmark with $\gamma = 0.6$ and $\beta = 0.3025$, HHT with $\alpha = 0.1$, WBZ, and Chung-Hulbert. The table gives the algorithmic damping ratio $\bar\xi = -\ln|\lambda| / \arg\lambda$ of the principal eigenvalue $\lambda$ of one step, for an undamped oscillator. The values are measurements from the reference code.

| method | $\bar\xi$ at $\omega\,dt = 0.1$ | at $0.3$ | at $1$ | period error at $0.3$ | order |
|---|---|---|---|---|---|
| Newmark, $\gamma = 0.6$ | $4.99 \times 10^{-3}$ | $1.48 \times 10^{-2}$ | $4.31 \times 10^{-2}$ | 0.77 % | 1 |
| WBZ-alpha | $1.5 \times 10^{-5}$ | $3.87 \times 10^{-4}$ | $9.27 \times 10^{-3}$ | 0.97 % | 2 |
| HHT-alpha | $1.0 \times 10^{-5}$ | $2.62 \times 10^{-4}$ | $6.75 \times 10^{-3}$ | 0.93 % | 2 |
| Chung-Hulbert | $5.0 \times 10^{-7}$ | $1.33 \times 10^{-5}$ | $4.18 \times 10^{-4}$ | 0.78 % | 2 |

All four remove the same fraction of a very high mode per step. At $\omega\,dt = 0.1$, a mode resolved with about 60 steps per period, Newmark damps 10 000 times more than Chung-Hulbert. For the second order methods $\bar\xi$ falls like $(\omega\,dt)^3$.

## Correctness

The full arguments are in [the correctness proof](proofs/correctness.md).

- **Second order (theorem).** The auxiliary acceleration $a_k$ approximates $\ddot d(t_k - \delta\,dt)$ with $\delta = \alpha_f - \alpha_m$. With this shift the exact solution satisfies the balance of lines L5 and L6 up to $O(dt^2)$ and the displacement update up to $O(dt^3)$. The velocity update has the defect $(\tfrac12 + \delta - \gamma)\,dt^2\,\dddot d$, so the step has a local error of $O(dt^3)$ exactly when $\gamma = \tfrac12 - \alpha_m + \alpha_f$.
- **High frequency limit (theorem).** As $\omega\,dt \to \infty$ the step matrix of a mode converges to a matrix with eigenvalues $-\alpha_f/(1 - \alpha_f)$ and a pair with sum $2 - (\gamma + \tfrac12)/\beta$ and product $1 - (\gamma - \tfrac12)/\beta$. With the Chung-Hulbert parameters all three are equal to $-\rho_\infty$, so the spectral radius tends to $\rho_\infty$.
- **Stability (theorem, cited).** For a linear problem with $C = 0$, the method is unconditionally stable when $\alpha_m \le \alpha_f \le \tfrac12$ and $\beta \ge \tfrac14 + \tfrac12(\alpha_f - \alpha_m)$ (Chung and Hulbert 1993). The Chung-Hulbert parameters satisfy both conditions for every $\rho_\infty \in [0, 1]$.
- **The case $\rho_\infty = 1$ (theorem).** Then $\alpha_m = \alpha_f = \tfrac12$, $\beta = \tfrac14$ and $\gamma = \tfrac12$, and for a load that is zero or linear in $t$ the steps are those of the trapezoidal rule, which conserves the energy of a linear undamped system.

## Complexity

The cost is that of the [Newmark-beta method](/newmark-beta-method/): in the [real-RAM model](/real-ram/) a linear problem with banded matrices of half bandwidth $b$ and fixed $dt$ needs one factorization, $\Theta(n b^2)$, and then $\Theta(n b)$ per step, so $\Theta(n b^2 + m n b)$ in total and $\Theta(n b)$ memory. The shifted balance adds two vectors of storage and a few vector operations per step. A nonlinear problem costs one tangent assembly and one factorization per Newton iteration. The reference code uses dense Gaussian elimination and is meant only for small systems.

## Properties

- **One parameter for all the damping.** $\rho_\infty = 1$ gives no damping (the trapezoidal rule), $\rho_\infty = 0$ gives asymptotic annihilation: a mode with $\omega\,dt \to \infty$ is removed in one step, as with an [L-stable](/l-stability/) method.
- **Second order for every $\rho_\infty$**, and unconditionally stable for linear problems.
- **Small low frequency damping.** Among the second order three-stage schemes of this form, the Chung-Hulbert choice minimizes the low frequency damping for a given $\rho_\infty$ (Chung and Hulbert 1993). The measured ratios are in the example.
- **The auxiliary acceleration is not the physical one.** $a_k$ is a time-shifted value, so a code that reports accelerations, for example floor response spectra, must say so or recompute them from the equation of motion.

## Variants and improvements

- **HHT-alpha** ($\alpha_m = 0$) and **WBZ-alpha** ($\alpha_f = 0$): the two one-shift members. HHT-alpha is the usual implicit dynamics option of several commercial finite element codes.
- **First order systems (Jansen, Whiting and Hulbert 2000).** The same idea for $M\dot u + f(u) = 0$, with $\alpha_m = \tfrac12(3 - \rho_\infty)/(1 + \rho_\infty)$, $\alpha_f = 1/(1 + \rho_\infty)$ and $\gamma = \tfrac12 + \alpha_m - \alpha_f$ in their convention. It is used for stabilized finite element and [variational multiscale](/variational-multiscale-method/) flow solvers and in [isogeometric](/isogeometric-analysis/) fluid codes.
- **Nonlinear and constrained systems.** For multibody dynamics with constraints, Arnold and Bruls (2007) analyzed the method as an index-3 DAE integrator.
- **Energy-momentum and energy-decaying schemes.** For strongly nonlinear elastodynamics, generalized-alpha can still let the energy grow. Schemes based on discrete gradients bound the energy by construction.

## When to use it

Use it as the default implicit integrator for linear and nonlinear structural dynamics with a mesh that has unresolved high modes, for example after a sudden load or with contact, where the trapezoidal rule leaves high frequency noise in the stresses. A value $\rho_\infty$ between $0.5$ and $0.9$ is common. Use the trapezoidal rule ($\rho_\infty = 1$) when you need exact energy for a linear problem. Use the explicit central difference method for short wave and impact problems where the step is small anyway.

## Pitfalls

- **Wrong sign conventions.** Papers and codes use $\alpha$, $-\alpha$, $1 - \alpha$ for the same shift. A wrong sign gives a method that is first order or unstable. Check with the second order test and with the spectral radius at a large $\omega\,dt$.
- **Inconsistent initial acceleration.** Line L1 computes $a_0$ from the equation of motion, but strictly $a_0$ should approximate $\ddot d(-\delta\,dt)$. The difference is $O(dt)$ and is damped by the method, so it costs little in practice, but it shows up in the first steps of an error plot.
- **Load at the wrong time.** The load must be evaluated at $t_{k+1-\alpha_f}$ (or averaged as $(1 - \alpha_f)F_{k+1} + \alpha_f F_k$). Using $F(t_{k+1})$ makes the method first order for a time-dependent load.
- **Low frequency damping is not zero.** For $\rho_\infty < 1$ a long simulation of a resolved mode still loses some amplitude, about $\bar\xi\,\omega\,t$ in relative terms. For very long runs, use $\rho_\infty$ close to 1.
- **Nonlinear energy growth.** The linear stability proof does not cover nonlinear problems. Strongly nonlinear problems with large steps can still blow up.

## Implementations

## History

Hilber, Hughes and Taylor in 1977 shifted the stiffness and load terms of the Newmark balance and obtained second order with controllable high frequency damping. Wood, Bossak and Zienkiewicz in 1980 shifted the inertia term instead. Chung and Hulbert in 1993 used both shifts, related all parameters to the single high frequency spectral radius $\rho_\infty$, and showed that this choice gives the least low frequency damping for a given high frequency damping. Jansen, Whiting and Hulbert extended the method to first order systems in 2000, which made it a standard time integrator for stabilized flow solvers.

## References
