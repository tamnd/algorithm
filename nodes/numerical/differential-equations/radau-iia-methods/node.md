---
tag: SBC09Y
kind: algorithm
slug: radau-iia-methods
name: Radau IIA methods
aliases:
- Radau methods
- Radau IIA
- RADAU5
area: numerical/differential-equations
level: advanced
summary: "Implicit Runge-Kutta methods that collocate at the right Radau points. s stages give order 2s - 1, L-stability and stiff accuracy, which makes them a standard choice for stiff ODEs and DAEs."
solves: [ode-initial-value-problem, stiff-ode-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", s: "the number of stages", d: "the dimension of y", k: "the number of Newton iterations per step", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (s^3 d^3 + k (s C + s^2 d^2)))"}
  space: {extra: "Θ(s^2 d^2)"}
  evaluations: {worst: "N s k"}
properties: {deterministic: true, implicit: true, one_step: true, order: "2s - 1", stage_order: "s", a_stable: true, l_stable: true, stiffly_accurate: true, symplectic: false}
history:
  year: 1969
  people: [John C. Butcher, Byron L. Ehle, Owe Axelsson, Ernst Hairer, Gerhard Wanner]
  note: Butcher (1964) built implicit Runge-Kutta methods on Radau quadrature. Ehle (1969) and Axelsson (1969) gave the IIA form and proved A-stability. Hairer and Wanner's RADAU5 code (1991) made the 3-stage method a standard stiff solver.
prereqs: [implicit-runge-kutta-methods, collocation-method, l-stability, stiff-ode-problem]
see_also: [gauss-legendre-runge-kutta, backward-euler-method, backward-differentiation-formulas, rosenbrock-methods, pade-approximation, butcher-order-conditions, newton-method-for-systems, differential-algebraic-equations]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.5 (construction of Radau IIA, simplifying assumptions, tableaus for s = 1, 2, 3), Section IV.4 (Pade approximations and A-stability), Section IV.8 (implementation of RADAU5, simplified Newton and transformation of the linear systems), Section IV.15 (order reduction, B-convergence)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.7 (implicit Runge-Kutta methods, collocation, superconvergence of collocation methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (implicit Runge-Kutta methods based on Radau quadrature, simplifying assumptions)
  - paper: "J. C. Butcher, Integration processes based on Radau quadrature formulas, Mathematics of Computation 18 (1964) 233-244"
    locator: the first methods based on Radau quadrature; doi:10.1090/S0025-5718-1964-0165693-1
  - paper: "O. Axelsson, A class of A-stable methods, BIT 9 (1969) 185-199"
    locator: A-stable methods of Radau type; doi:10.1007/BF01946812
  - paper: "E. Hairer and G. Wanner, Stiff differential equations solved by Radau methods, Journal of Computational and Applied Mathematics 111 (1999) 93-111"
    locator: implementation details and variable order; doi:10.1016/S0377-0427(99)00134-X
---

Radau IIA methods are [implicit Runge-Kutta methods](/implicit-runge-kutta-methods/) for $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, whose $s$ stages sit at the nodes of the right Radau quadrature rule, with the last node at the end of the step, $c_s = 1$. They are [collocation methods](/collocation-method/): one step fits a polynomial of degree $s$ that satisfies the differential equation exactly at the $s$ nodes. With $s$ stages they reach order $2s - 1$, one less than the maximum, and in exchange they are [L-stable](/l-stability/) and stiffly accurate: the new value is the last stage. This damps fast transients in one step, so Radau IIA with $s = 3$ (order 5) is one of the standard solvers for [stiff problems](/stiff-ode-problem/) and differential-algebraic equations. With $s = 1$ it is the [backward Euler method](/backward-euler-method/).

## In plain words

Some systems mix very fast and very slow processes. Explicit methods have to take tiny steps to follow the fast part even after it has died out. Implicit methods choose the next value so that the equation holds at the new point, which lets them take steps sized to the slow part.

Radau IIA methods do this with several checkpoints inside each step, the last one at the very end. They find a curve through the current value that obeys the equation at every checkpoint and take its end as the next value. Finding that curve means solving a set of equations at each step, usually with a few rounds of Newton's method. Fast components that should have vanished are wiped out completely in a single step, which is exactly the behaviour stiff problems need.

## The problem

Given $f$, its Jacobian $\partial f/\partial y$ (or finite differences of $f$), $t_0$, $y_0$, an end time $T \ge t_0$, a step $h > 0$ and a number of stages $s \ge 1$, compute $y_N \approx y(T)$. We assume $f$ is smooth and Lipschitz in $y$ with constant $L$; for the stiff analysis $L$ may be huge while the solution itself is smooth. The cost is counted as evaluations of $f$, Jacobian evaluations, LU factorizations and linear solves. Errors are measured in the max norm.

## The algorithm

The tableau $(A, b, c)$ comes from the nodes: $c_1 < \dots < c_s = 1$ are the zeros of $\frac{d^{s-1}}{dx^{s-1}}\big(x^{s-1}(x - 1)^s\big)$, $a_{ij} = \int_0^{c_i}\ell_j$ and $b_j = a_{sj}$, with $\ell_j$ the Lagrange basis polynomials. For $s = 2$:

$$c = (1/3, 1), \quad A = \begin{pmatrix} 5/12 & -1/12 \\ 3/4 & 1/4 \end{pmatrix}, \quad b = (3/4, 1/4).$$

For $s = 3$, $c = ((4 - \sqrt6)/10, (4 + \sqrt6)/10, 1)$. The step solves the stage equations for the increments $Z_i = Y_i - y_n$ by simplified Newton.

```pseudo id=main
RADAU-IIA(f, J, t0, y0, T, h, s)
L1  (A, b, c) ← Radau IIA tableau; N ← ⌈(T − t0)/h − δ⌉; t ← t0, y ← y0
L2  for n ← 0 to N − 1 do                       ▷ step τ = h, or T − t for the last step
L3      J ← ∂f/∂y(t, y); M ← LU(I − τ A ⊗ J)    ▷ one Jacobian and one LU per step
L4      Z ← 0                                    ▷ Z_i = Y_i − y, i = 1..s
L5      repeat
L6          G_i ← −Z_i + τ Σ_j a_ij f(t + c_j τ, y + Z_j)   for i = 1..s
L7          solve M ΔZ = G; Z ← Z + ΔZ
L8      until ‖ΔZ‖ ≤ tol (error if max_iter is reached)
L9      y ← y + Z_s                              ▷ stiffly accurate: b is the last row of A
L10     t ← t + τ
    return (t, y)
```

## Example

On the Curtiss-Hirschfelder equation $y' = -50(y - \cos t)$, $y(0) = 0$, with the exact solution of the [stiff problem page](/stiff-ode-problem/), the errors at $t = 1.2$ are (observed):

| $s$ (order) | $h = 0.1$ | $h = 0.2$ | $h = 0.4$ |
|---|---|---|---|
| 1 (1, backward Euler) | 4.29e-4 | 9.16e-4 | 2.16e-3 |
| 2 (3) | 9.22e-6 | 4.92e-5 | 5.79e-4 |
| 3 (5) | 2.26e-8 | 4.01e-7 | 2.44e-4 |

Here $z = -50h$ runs from $-5$ to $-20$, beyond the real stability limit $-2.785$ of classical RK4. Since the equation is linear, simplified Newton converges in one iteration (a second confirms it). On the nonstiff problem $y' = y\cos t$, $y(0) = 1$, the errors at $t = 2$ for $h = 0.4, 0.2, 0.1, 0.05$ with $s = 3$ are $5.9 \times 10^{-6}$, $1.8 \times 10^{-7}$, $5.5 \times 10^{-9}$, $1.7 \times 10^{-10}$, observed order 5.01; with $s = 2$ the observed order is 3.02 and with $s = 1$ it is 1.00.

## Correctness

**Theorem (proved).** If $f$ is $C^{2s}$ near the solution, the $s$-stage Radau IIA method has local error $O(h^{2s})$ and global error $O(h^{2s-1})$; its stability function is the $(s - 1, s)$ [Pade approximant](/pade-approximation/) of $e^z$, with $R(\infty) = 0$.

The proof shows that the nodes give a quadrature rule of order exactly $2s - 1$, that the method is collocation, and bounds the collocation error with the Alekseev-Grobner formula and that quadrature. The stability function is rational of degree $(s - 1, s)$ because $b$ is the last row of $A$, and order $2s - 1$ then forces it to be the unique Pade approximant. A-stability of these approximants is Ehle's theorem, cited rather than proved. For $s = 2$ the tests check the tableau, the conditions $B(3)$, $C(2)$, $D(1)$ and $R(z) = (1 + z/3)/(1 - 2z/3 + z^2/6)$ exactly with Fractions; for $s = 3, 4, 5$ they check $B(2s - 1)$, $C(s)$, $D(s - 1)$ and the Pade identity in floating point.

## Complexity

Each step evaluates one Jacobian (or $d$ extra evaluations of $f$ for finite differences), factors one $sd \times sd$ matrix, $\Theta(s^3 d^3)$ in this direct implementation, and runs $k$ Newton iterations, each with $s$ evaluations of $f$ and one solve, $\Theta(s^2 d^2)$. Production codes such as RADAU5 diagonalize $A^{-1}$: for $s = 3$ it has one real and a complex pair of eigenvalues, so the system splits into one real and one complex $d \times d$ system, about 5 times the cost of one real $d \times d$ LU instead of 27. They also keep the Jacobian over several steps and start Newton from the extrapolated collocation polynomial. Space is $\Theta(s^2 d^2)$ for the factored matrix.

## Properties

- **Order** $2s - 1$ and stage order $s$; order 1, 3, 5, 7 for $s = 1, 2, 3, 4$.
- **L-stable**: $R(z)$ is the $(s - 1, s)$ Pade approximant, $|R(z)| \le 1$ for $\operatorname{Re} z \le 0$ and $R(z) \to 0$ as $z \to \infty$.
- **Stiffly accurate**: $y_{n+1} = Y_s$, so the method can be applied directly to index 1, 2 and 3 differential-algebraic equations.
- **Algebraically stable and B-stable**: contractive for dissipative nonlinear problems (HNW II, Section IV.12).
- **Not symplectic, not symmetric**: on the oscillator $|R(ih)| < 1$, so the energy decays each step, as the tests check.
- **Order reduction** on very stiff problems: on the Prothero-Robinson problem $y' = \lambda(y - \sin t) + \cos t$ with $\lambda = -10^6$, the observed order drops to the stage order $s$ (2.02 for $s = 2$, 2.99 for $s = 3$), though the errors stay small ($10^{-10}$ to $10^{-13}$).

## Variants and improvements

- **Radau IA** uses the left Radau nodes ($c_1 = 0$); same order and stability function family but not stiffly accurate, rarely used.
- **Gauss-Legendre** methods ([Gauss-Legendre Runge-Kutta](/gauss-legendre-runge-kutta/)) reach order $2s$ and are symplectic, but $|R(\infty)| = 1$, so they do not damp stiff components.
- **Lobatto IIIC** methods are also L-stable, with order $2s - 2$.
- **Variable order Radau** (RADAU, Hairer and Wanner 1999) switches between 3, 5 and 7 stages.
- **[Rosenbrock methods](/rosenbrock-methods/)** replace the Newton iteration by a fixed number of linear solves; cheaper per step, but less robust at tight tolerances and on DAEs.
- **SDIRK** methods have a lower triangular $A$ with equal diagonal, so stages are solved one at a time with a single $d \times d$ LU, at the cost of stage order 1.

## When to use it

Use Radau IIA (in practice RADAU5) for stiff problems that need moderate to high accuracy, for problems with eigenvalues near the imaginary axis where [BDF](/backward-differentiation-formulas/) methods of high order are not stable, and for differential-algebraic equations of index up to 3. For nonstiff problems an explicit method is cheaper. For very large sparse systems at low accuracy, BDF codes with one $d \times d$ factorization are usually cheaper.

## Pitfalls

- **Newton failure.** Simplified Newton with a frozen Jacobian can diverge when the step is too large for the nonlinearity, as on the van der Pol problem with $\mu = 100$ and $h = 0.05$ during the fast jump; the implementation raises an error and production codes shrink the step.
- **Bad starting conditions.** On the Robertson problem a fixed step of $0.1$ from $t = 0$ overflows because the initial Jacobian misses the fast reaction; stiff codes need adaptive steps that start very small.
- **Stopping Newton too early or too late.** Codes stop at a tolerance tied to the local error tolerance; a tolerance near the rounding level, as here with $10^{-12}$, can stall on badly scaled problems.
- **Order reduction** means error estimates based on the classical order can be optimistic on very stiff problems.

## Implementations

## History

Butcher (1964) introduced implicit Runge-Kutta methods based on Radau quadrature. Ehle (1969) in his Waterloo thesis and Axelsson (1969) independently defined the IIA family and proved A-stability by the theory of Pade approximations. Hairer and Wanner's code RADAU5, published with their 1991 book on stiff problems, used the 3-stage method with a transformation that reduces the linear algebra to one real and one complex system, and made Radau IIA a standard tool.

## References
