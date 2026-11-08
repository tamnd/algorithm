---
tag: XS4SMM
kind: algorithm
slug: gauss-legendre-runge-kutta
name: Gauss-Legendre Runge-Kutta methods
aliases:
- Gauss collocation methods
- Gauss methods
- Gauss-Legendre methods
- implicit midpoint rule (s = 1)
area: numerical/differential-equations
level: advanced
summary: "Implicit s-stage Runge-Kutta methods that collocate at the Gauss-Legendre nodes. Order 2s, the maximum for s stages; A-stable, symplectic, symmetric, and they conserve quadratic invariants."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", s: "the number of stages", d: "the dimension of y", K: "the number of simplified Newton iterations per step", C: "the cost of one evaluation of f"}
  time: {worst: "O(N (s^3 d^3 + K (s C + s^2 d^2)))"}
  space: {extra: "O(s^2 d^2)"}
  evaluations: {worst: "N (s (K + 1) + d + 1)"}
properties: {deterministic: true, implicit: true, one_step: true, order: "2s", stage_order: "s", a_stable: true, l_stable: false, symplectic: true, symmetric: true}
history:
  year: 1964
  people: [J. C. Butcher, J. Kuntzmann]
  note: Kuntzmann (1961) and Butcher (1964) found the implicit Runge-Kutta methods of order 2s based on Gauss quadrature; Ehle (1969) showed their stability functions are diagonal Padé approximations and hence A-stable, and Sanz-Serna, Lasagni and Suris (1988) proved they are symplectic.
prereqs: [implicit-runge-kutta-methods, gauss-legendre-quadrature, a-stability]
see_also: [radau-iia-methods, symplectic-integrators, collocation-method, hamiltonian-systems, pade-approximation, butcher-order-conditions, newton-method-for-systems, l-stability]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.7 (implicit Runge-Kutta methods, simplifying assumptions B, C, D, collocation methods, Gauss methods of order 2s, superconvergence via the nonlinear variation-of-constants formula)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.3 (A-stability, Padé approximations), Section IV.5 (Gauss, Radau and Lobatto methods), Section IV.8 (implementation of implicit Runge-Kutta methods, simplified Newton iteration), Section IV.12 (algebraic stability, B-stability)
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section IV.2 (conservation of quadratic invariants), Section VI.4 (symplectic Runge-Kutta methods, the condition b_i a_ij + b_j a_ji = b_i b_j), Chapter X (long-time energy behaviour)
  - paper: doi:10.1090/S0025-5718-1964-0159424-9
    title: J. C. Butcher, Implicit Runge-Kutta processes, Mathematics of Computation 18(85) (1964) 50-64
    locator: the methods of order 2s with Gauss-Legendre nodes
  - paper: doi:10.1007/BF01954907
    title: J. M. Sanz-Serna, Runge-Kutta schemes for Hamiltonian systems, BIT Numerical Mathematics 28(4) (1988) 877-883
    locator: Runge-Kutta methods with b_i a_ij + b_j a_ji - b_i b_j = 0 are symplectic; Gauss methods satisfy it
---

The Gauss-Legendre Runge-Kutta method with $s$ stages, or Gauss method, is the implicit [Runge-Kutta method](/implicit-runge-kutta-methods/) whose nodes $c_1, \ldots, c_s$ are the zeros of the shifted Legendre polynomial $P_s(2c - 1)$, the nodes of [Gauss-Legendre quadrature](/gauss-legendre-quadrature/) on $[0, 1]$, and whose coefficients make it the collocation method at those nodes. It has order $2s$, the highest possible for $s$ stages. Its stability function is the diagonal $(s, s)$ [Padé approximation](/pade-approximation/) of $e^z$, so it is [A-stable](/a-stability/) with $|R(iy)| = 1$ on the imaginary axis. It is symmetric and symplectic, and it conserves every quadratic first integral exactly. For $s = 1$ it is the implicit midpoint rule. The price is a nonlinear system of $sd$ equations per step.

## In plain words

Most step-by-step methods for differential equations look at the slope at a few points and combine them. The Gauss methods choose the few points inside each step with special care: they are the points that give the most accurate averages of smooth functions, the same ones used by the best numerical integration rules. The method then asks for a curve across the step whose slope matches the equation exactly at those points. Because the right slopes at future points are not known in advance, it has to solve a small system of equations at every step, which costs more than an explicit method. In return it is very accurate, it never blows up on rapidly decaying problems, and it keeps quantities like energy in an oscillator or the length of a spinning vector from drifting over very long simulations.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, smooth and Lipschitz in $y$ with constant $L$, an initial value $y_0$ and a step $h > 0$, approximate the solution of the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, on the grid $t_n = t_0 + nh$ (the last step shortened to end at $T$). The global error $e_n = y(t_n) - y_n$ should be $O(h^{2s})$ for smooth problems, the method should stay bounded on stiff linear problems with eigenvalues in the left half-plane, and for Hamiltonian or conservative problems it should respect the geometric structure. Cost is counted in evaluations of $f$, Jacobian evaluations and $sd \times sd$ linear solves per step.

## The algorithm

The tableau $(A, b, c)$ comes from Lagrange interpolation at the nodes: with $\ell_j$ the Lagrange basis polynomial for $c_j$, $a_{ij} = \int_0^{c_i}\ell_j(\tau)\,d\tau$ and $b_j = \int_0^1\ell_j(\tau)\,d\tau$. For $s = 1$: $c = \tfrac12$, $a = \tfrac12$, $b = 1$. For $s = 2$:

$$\begin{array}{c|cc} \tfrac12 - \tfrac{\sqrt3}{6} & \tfrac14 & \tfrac14 - \tfrac{\sqrt3}{6} \\ \tfrac12 + \tfrac{\sqrt3}{6} & \tfrac14 + \tfrac{\sqrt3}{6} & \tfrac14 \\ \hline & \tfrac12 & \tfrac12 \end{array}$$

One step solves for the stage increments $Z_i = Y_i - y_n$ in

$$Z_i = h\sum_{j=1}^s a_{ij}f(t_n + c_jh, y_n + Z_j), \qquad i = 1, \ldots, s,$$

and sets $y_{n+1} = y_n + h\sum_jb_jf(t_n + c_jh, y_n + Z_j)$. The implementation uses simplified Newton iteration with the Jacobian $J = \partial f/\partial y(t_n, y_n)$ frozen over the step, so the $sd \times sd$ matrix $I - hA \otimes J$ is formed once per step.

```pseudo id=main
GAUSS-LEGENDRE-RK(f, t0, y0, T, h, s)
L1  (A, b, c) ← Gauss tableau: c_i zeros of P_s(2c − 1), a_ij = ∫_0^(c_i) ℓ_j, b_j = ∫_0^1 ℓ_j
L2  N ← ⌈(T − t0)/h⌉, t ← t0, y ← y0
L3  for n ← 0 to N − 1 do                      ▷ last step k = T − t, others k = h
L4      J ← ∂f/∂y(t, y), M ← I − k A ⊗ J
L5      Z ← 0
L6      repeat ΔZ ← M^(−1)(−Z + k (A ⊗ I) F(Z)), Z ← Z + ΔZ until ‖ΔZ‖ ≤ tol
L7      y ← y + k Σ_j b_j f(t + c_j k, y + Z_j), t ← t + k
L8  return y
```

Here $F(Z)$ stacks $f(t + c_jk, y + Z_j)$ for $j = 1, \ldots, s$. Production codes factor $M$ once per step (or reuse it over several steps), transform $A$ to block-diagonal form to cut the cost of the linear algebra from $(sd)^3$ to about $s\,d^3$ complex operations, and avoid the last $s$ evaluations by $y_{n+1} = y_n + \sum_i(b^TA^{-1})_iZ_i$.

## Example

**Linear decay, one step.** For $y' = -y$, $y(0) = 1$ and $h = \tfrac12$ the methods reproduce their stability functions $R(z)$ at $z = -\tfrac12$:

| method | $R(z)$ | $y_1$ | error vs $e^{-1/2} = 0.6065307$ |
|---|---|---|---|
| $s = 1$ (implicit midpoint) | $\dfrac{1 + z/2}{1 - z/2}$ | $3/5 = 0.6$ | 6.5e-3 |
| $s = 2$ | $\dfrac{1 + z/2 + z^2/12}{1 - z/2 + z^2/12}$ | $37/61 = 0.6065574$ | 2.67e-5 |

**Observed order.** For $y' = \cos(t)\,y$, $y(0) = 1$, on $[0, 2]$ (exact $y(2) = e^{\sin 2}$):

| $s$ | $h$ | error | ratio |
|---|---|---|---|
| 1 | 0.2, 0.1, 0.05 | 9.27e-3, 2.31e-3, 5.76e-4 | 4.02, 4.00 |
| 2 | 0.2, 0.1, 0.05 | 3.17e-6, 1.97e-7, 1.23e-8 | 16.1, 16.0 |
| 3 | 0.5, 0.25, 0.125 | 7.86e-7, 1.22e-8, 1.91e-10 | 64.3, 64.0 |

The ratios $4, 16, 64$ are $2^{2s}$: orders 2, 4 and 6.

**Long-time conservation.** On the harmonic oscillator $q' = p$, $p' = -q$ with $s = 2$ and $h = 0.5$, after 2000 steps to $t = 1000$ the energy $q^2 + p^2$ differs from 1 by $7 \times 10^{-14}$, the Newton tolerance and rounding level; the phase error grows linearly, but the energy does not drift. For the free rigid body, $\|y\|^2$ is conserved in the same way.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the coefficients satisfy the simplifying assumptions $B(2s)$, $C(s)$ and $D(s)$; that the method is the collocation method at the Gauss nodes; that the collocation polynomial's defect vanishes at the nodes, which with the nonlinear variation-of-constants formula and the exactness of Gauss quadrature for degree $2s - 1$ gives local error $O(h^{2s+1})$ and global error $O(h^{2s})$; and that $b_ia_{ij} + b_ja_{ji} - b_ib_j = 0$, which with positive weights yields the energy identity behind A-stability, B-stability and exact conservation of quadratic invariants. Symplecticity follows from the same condition (Sanz-Serna 1988) and is cited.

## Complexity

Per step: one Jacobian ($d + 1$ evaluations of $f$ with forward differences, or one call to the Jacobian), forming and factoring the $sd \times sd$ matrix in $O(s^3d^3)$, and $K$ simplified Newton iterations, each with $s$ evaluations of $f$ and a solve. The implementation re-eliminates per iteration, $O(s^3d^3)$ each; with a stored factorization each solve is $O(s^2d^2)$. With $N$ steps the total is $O(N(s^3d^3 + K(sC + s^2d^2)))$ with a factorization reused, $N(s(K + 1) + d + 1)$ evaluations of $f$, and $O(s^2d^2)$ memory. With the tolerance $10^{-13}$ used in the tests, $K$ is between 2 (linear problems: one correction and one confirming iteration) and about 6. On nonstiff problems a Gauss method of order $2s$ is usually more expensive than an explicit method of the same order; its value lies in stability and structure preservation.

## Properties

- **Order $2s$**, the maximum for an $s$-stage Runge-Kutta method, with stage order $s$.
- **A-stable**: $|R(z)| \le 1$ for $\operatorname{Re} z \le 0$, with $|R(iy)| = 1$; but $|R(-\infty)| = 1$, so it is not [L-stable](/l-stability/) and does not damp stiff components.
- **Algebraically stable and B-stable**: contractive problems give contractive numerical solutions.
- **Symmetric**: stepping forward by $h$ and back by $-h$ returns the starting value.
- **Symplectic**: applied to a Hamiltonian system the step map is a symplectic map, which gives near-conservation of energy over exponentially long times (Hairer, Lubich and Wanner 2006, Chapter X).
- **Conserves quadratic invariants exactly**: if $y^TQf(t, y) = 0$ for all $t, y$ with symmetric $Q$, then $y_n^TQy_n$ is constant.

## Variants and improvements

- **Radau IIA and Lobatto IIIC methods** replace Gauss nodes by Radau or Lobatto nodes, giving order $2s - 1$ or $2s - 2$ but L-stability, better for stiff problems and DAEs (see [Radau IIA](/radau-iia-methods/)).
- **Lobatto IIIA-IIIB pairs** give symplectic partitioned methods with explicit stages for separable Hamiltonians.
- **Efficient implementations** transform $A^{-1}$ to real block-diagonal form, use extrapolated starting values from the previous step's collocation polynomial, and reuse the Jacobian over many steps.
- **Fixed-point iteration** instead of Newton for nonstiff problems; it is what many geometric integrators use, with compensated summation to keep roundoff from drifting.
- **Continuous output** from the collocation polynomial, of order $s$ (stage order).

## When to use it

Use Gauss methods for long-time integration of Hamiltonian systems and problems with quadratic invariants, such as celestial mechanics, molecular dynamics with implicit constraints, and rigid body motion, where symplecticity and exact quadratic conservation matter, and when high order with A-stability is needed for mildly stiff oscillatory problems. Continuous Galerkin time stepping is closely related to them. For strongly stiff dissipative problems prefer L-stable methods (Radau IIA, BDF); for cheap nonstiff integration prefer explicit pairs with error control; for separable Hamiltonians, explicit [symplectic integrators](/symplectic-integrators/) such as Störmer-Verlet are cheaper per step.

## Pitfalls

- **Stiff transients are not damped.** With $y' = -10^6(y - \cos t)$, $y(0) = 0$ and $h = 0.1$, both the 2- and 3-stage methods carry the initial error of size 1 through all 10 steps, ending near $-0.46$ instead of $\cos 1 = 0.54$, because $|R(z)| \approx 1$ for $z \to -\infty$. In the same way, $y' = -10^6y$ stays near magnitude 1.
- **Order reduction.** On stiff problems the observed order drops toward the stage order $s$ (or $s + 1$), not $2s$.
- **Newton failure for large steps.** Simplified Newton with a frozen Jacobian can diverge if $h$ is too large for the nonlinearity; reduce $h$ or update the Jacobian.
- **Loose iteration tolerances destroy structure.** Energy and symplecticity are only preserved up to the accuracy of the stage solution; stop the iteration at roundoff level for long runs.
- **Variable step sizes break symplecticity.** Changing $h$ adaptively destroys the long-time energy behaviour; use fixed steps or symmetric reversible step-size control.
- **Tableau coefficients in low precision.** Computing $A$ and $b$ from rounded nodes is fine, but typing truncated decimals loses order.

## Implementations

## History

Kuntzmann (1961) and Butcher (1964) introduced implicit Runge-Kutta methods of order $2s$ based on Gauss quadrature, and Butcher developed the theory of order conditions and simplifying assumptions around them. Ehle (1969) showed that their stability functions are the diagonal Padé approximations of $e^z$ and therefore A-stable. Burrage and Butcher (1979) and Crouzeix (1979) introduced algebraic stability, which Gauss methods satisfy. Cooper (1987) proved conservation of quadratic invariants, and Sanz-Serna (1988), Lasagni (1988) and Suris (1988) independently proved symplecticity, which made Gauss methods a standard tool of geometric numerical integration.

## References
