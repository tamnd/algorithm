---
tag: DYRABY
kind: technique
slug: operator-splitting
name: Operator splitting
aliases:
- Strang splitting
- fractional step method
- Lie-Trotter splitting
- splitting method
area: numerical/differential-equations
level: advanced
summary: "Solve y' = A(y) + B(y) by alternating sub-steps that each solve only y' = A(y) or y' = B(y). Lie splitting has order 1, symmetric Strang splitting order 2."
prereqs: [ode-initial-value-problem, order-of-accuracy, method-of-lines]
see_also: [symplectic-integrators, verlet-integration, symplectic-euler-method, adi-method, exponential-integrators, hamiltonian-systems, navier-stokes-equations, stiff-ode-problem]
sources:
  - paper: doi:10.1137/0705041
    title: Gilbert Strang, On the construction and comparison of difference schemes, SIAM Journal on Numerical Analysis 5 (1968) 506-517
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section II.5 (splitting methods), Section II.4 (composition methods, the triple jump) and Section III.5 (the Baker-Campbell-Hausdorff formula and order conditions of splitting methods)
  - paper: "Robert I. McLachlan and G. Reinout W. Quispel, Splitting methods, Acta Numerica 11 (2002) 341-434"
    locator: survey of splitting and composition methods, error analysis, applications
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 11 (fractional step methods for advection-reaction and advection-diffusion, splitting error)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 17 (fractional step methods for source terms) and Chapter 19 (dimensional splitting)
---

Operator splitting solves an evolution equation whose right side is a sum, $y' = f^{[A]}(y) + f^{[B]}(y)$, by solving the two parts one after the other within each step. If $\varphi_h^{A}$ and $\varphi_h^{B}$ are the exact (or accurate) flows of $y' = f^{[A]}(y)$ and $y' = f^{[B]}(y)$ over time $h$, Lie-Trotter splitting takes the step $y_{n+1} = \varphi_h^{B}(\varphi_h^{A}(y_n))$ and has order 1, and Strang splitting takes the symmetric step $y_{n+1} = \varphi_{h/2}^{A}(\varphi_h^{B}(\varphi_{h/2}^{A}(y_n)))$ and has order 2. The pieces are chosen so that each is easy: diffusion and reaction, advection in $x$ and in $y$, kinetic and potential energy, a stiff linear part and a nonstiff rest. For Hamiltonian systems the method gives the [symplectic Euler](/symplectic-euler-method/) and [Störmer-Verlet](/verlet-integration/) methods.

## In plain words

Some systems change for several reasons at once: a chemical spreads out and reacts, a planet moves and is pulled. Doing all of it together can be hard, but each reason alone is often easy, sometimes with an exact formula.

Splitting does the easy parts in turn: for a short time let only spreading happen, then only reaction, then spreading again. Because the parts do not quite take turns in reality, this makes a small error each step, which gets smaller as the steps get shorter. Doing half a step of the first part before and half after, in a mirror pattern, cancels the main part of that error for free.

## When it applies

- **A sum of simpler parts.** The right side of an [initial value problem](/ode-initial-value-problem/) $y' = f^{[A]}(y) + f^{[B]}(y)$, or a semi-discretised PDE $U' = F_A(U) + F_B(U)$ from the [method of lines](/method-of-lines/), where each part can be solved exactly or with a method suited to it.
- **Typical splits.** Diffusion plus reaction (implicit solve for the linear stiff diffusion, local ODE solves for the reaction); advection plus diffusion; dimension by dimension ([ADI](/adi-method/) and dimensional splitting for conservation laws); $H = T(p) + V(q)$ for [Hamiltonian systems](/hamiltonian-systems/); linear plus nonlinear parts in the nonlinear Schrödinger equation (split-step Fourier); the pressure projection in incompressible [Navier-Stokes](/navier-stokes-equations/) solvers.
- **When structure must be kept.** If each sub-flow is symplectic, volume preserving or positivity preserving, so is their composition.
- **Smooth enough solutions.** The order statements assume the commutators of the parts are bounded on the solution; for stiff parts or boundary conditions this can fail.

## The template

**Notation.** Steps $h$, grid $t_n$, approximations $y_n$; $\varphi_h^{A}$ and $\varphi_h^{B}$ are the flows of the parts. The cost is the cost of the sub-solves, counted in $f$ evaluations, linear solves or FFTs, times the number of steps.

```pseudo id=main
STRANG-SPLITTING(y0, t0, T, h, φ^A, φ^B)
L1  N ← ⌈(T − t0)/h⌉
L2  y ← y0
L3  for n ← 0 to N − 1 do
L4      h_n ← min(h, T − t0 − n h)
L5      y ← φ^A_{h_n/2}(y)            ▷ hole: solver for part A
L6      y ← φ^B_{h_n}(y)              ▷ hole: solver for part B
L7      y ← φ^A_{h_n/2}(y)
L8  return y
```

Lie-Trotter splitting replaces lines L5 to L7 by $y \leftarrow \varphi_{h_n}^{B}(\varphi_{h_n}^{A}(y))$. In Strang splitting, consecutive half steps L7 and L5 of part $A$ can be merged into one full step, so Strang costs the same as Lie except at the ends and at output times.

**Why the orders are 1 and 2.** For linear parts $f^{[A]}(y) = Ay$, $f^{[B]}(y) = By$, the flows are $e^{hA}$ and $e^{hB}$, and

$$e^{hB}e^{hA} = e^{h(A + B)} + \frac{h^2}{2}[B, A] + O(h^3), \qquad [B, A] = BA - AB,$$

by multiplying the series. So Lie splitting has local error $\frac{h^2}{2}[B, A]y + O(h^3)$, which is zero exactly when the parts commute, and, summed over $T/h$ steps with the stable flows, global error $O(h)$. Strang's product $e^{hA/2}e^{hB}e^{hA/2}$ is symmetric: replacing $h$ by $-h$ gives its inverse. A symmetric method has even order, and the $h^2$ terms cancel, so its local error is $O(h^3)$ and its order is 2. The leading error term involves the double commutators $[A, [A, B]]$ and $[B, [B, A]]$. For nonlinear flows the same holds with Lie brackets of vector fields (HLW, Section III.5). These statements are proved there for smooth nonstiff problems; with stiff parts the constants can depend on the stiffness.

**Higher order by composition.** With $\gamma_1 = 1/(2 - 2^{1/3}) = 1.35121$ and $\gamma_2 = 1 - 2\gamma_1 = -1.70241$, the triple jump $S_{\gamma_1 h}S_{\gamma_2 h}S_{\gamma_1 h}$ of a symmetric second order step $S_h$ has order 4 (Yoshida 1990, Suzuki 1990).

## Classic examples

**A non-commuting linear system.** $y' = (A + B)y$ with $A = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ (rotation), $B = \operatorname{diag}(-1, -0.1)$ (damping), $y_0 = (1, 0)$, $T = 1$, exact flows. Here $[A, B] \ne 0$. Max errors:

| $N$ | 10 | 20 | 40 | 80 | 160 |
|---|---|---|---|---|---|
| Lie | $2.29 \cdot 10^{-2}$ | $1.14 \cdot 10^{-2}$ | $5.68 \cdot 10^{-3}$ | $2.84 \cdot 10^{-3}$ | $1.42 \cdot 10^{-3}$ |
| Strang | $5.21 \cdot 10^{-4}$ | $1.30 \cdot 10^{-4}$ | $3.25 \cdot 10^{-5}$ | $8.13 \cdot 10^{-6}$ | $2.03 \cdot 10^{-6}$ |
| triple jump | $2.64 \cdot 10^{-6}$ | $1.65 \cdot 10^{-7}$ | $1.03 \cdot 10^{-8}$ | $6.43 \cdot 10^{-10}$ | |

The ratios are $2.00$, $4.00$ and $16.0$: observed orders 1, 2 and 4. If $B$ is replaced by a multiple of the identity, the parts commute and all three splittings are exact up to rounding.

**Hamiltonian systems.** For $H(q, p) = T(p) + V(q)$ the flow of $T$ moves $q$ with constant $p$, and the flow of $V$ changes $p$ with constant $q$. Lie splitting gives [symplectic Euler](/symplectic-euler-method/), and Strang splitting gives the Störmer-Verlet (leapfrog) method $p_{n+1/2} = p_n - \frac h2\nabla V(q_n)$, $q_{n+1} = q_n + hp_{n+1/2}$ (for $T = \frac12|p|^2$), $p_{n+1} = p_{n+1/2} - \frac h2\nabla V(q_{n+1})$. Both are [symplectic](/symplectic-integrators/), because each sub-flow is.

**Reaction-diffusion.** For $u_t = Du_{xx} + g(u)$, solve the diffusion with Crank-Nicolson or exactly in Fourier space, and the reaction pointwise, where $u' = g(u)$ is a scalar ODE at each grid point, often with a closed form. The coupled nonlinear implicit solve is avoided.

**Dimensional splitting.** For $u_t + au_x + bu_y = 0$, apply a one-dimensional scheme along rows and then along columns. With 1D schemes stable for their own Courant numbers, the split scheme is stable, and Strang ordering keeps second order (Strang 1968).

## Variations

- **Lie-Trotter, Strang, and symmetric compositions** of higher order with more stages (Yoshida, Suzuki, McLachlan); methods with processing, where a cheap change of variables raises the order.
- **Splitting with more than two parts.** $\varphi^A_{h/2}\varphi^B_{h/2}\varphi^C_h\varphi^B_{h/2}\varphi^A_{h/2}$ is again symmetric and of order 2.
- **Additive and IMEX methods.** Instead of composing flows, treat the parts with different coefficients inside one Runge-Kutta or multistep method; no splitting error in the same sense, but coupled stages.
- **Exponential integrators.** Treat a stiff linear part exactly through $\varphi$-functions of $hA$, without a splitting error of order 1.
- **Projection methods for incompressible flow.** Chorin's 1968 method advances velocity without the pressure, then projects onto divergence-free fields: a splitting of momentum and incompressibility.

## Pitfalls

- **Order reduction.** With stiff parts or non-periodic boundary conditions the intermediate values may not satisfy the boundary conditions, and Strang splitting can drop below order 2 in practice.
- **Steady states are not preserved.** If $f^{[A]}(y^*) + f^{[B]}(y^*) = 0$ but each part is nonzero at $y^*$, the split step moves away from $y^*$ and back, and the computed steady state carries an $O(h)$ or $O(h^2)$ error. This matters for source terms in conservation laws.
- **Negative steps above order 2.** Any splitting of order 3 or more with real coefficients needs a backward substep (Sheng 1989, Suzuki 1991), as $\gamma_2 < 0$ in the triple jump. Backward steps of diffusion are ill posed, so high order splitting is restricted to reversible parts or needs complex coefficients.
- **Inaccurate sub-solves.** The overall order is at most the order of the sub-solvers; a first-order sub-solver ruins Strang splitting.
- **Ordering at output times.** When Strang half steps are merged, the stored value between merged steps is not an approximation of second order at $t_n$; finish with the closing half step before output.

## Exercises

1. Show that $e^{hB}e^{hA} - e^{h(A + B)} = \frac{h^2}{2}(BA - AB) + O(h^3)$ by expanding both sides.
2. Show that Strang splitting is symmetric, and explain why a symmetric one-step method has even order.
3. Write Strang splitting for $H = \frac12p^2 + V(q)$ and check that it is the Störmer-Verlet method.
4. For $y' = -y + 1$ split as $f^{[A]} = -y$, $f^{[B]} = 1$, find the fixed point of the Lie step with exact flows and compare it with $y^* = 1$.

## References
