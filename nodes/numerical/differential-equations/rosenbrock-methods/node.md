---
tag: B4P23E
kind: algorithm
slug: rosenbrock-methods
name: Rosenbrock methods
aliases:
- Rosenbrock-Wanner methods
- ROW methods
- linearly implicit Runge-Kutta methods
area: numerical/differential-equations
level: advanced
summary: "Linearly implicit Runge-Kutta methods for stiff ODEs: each step solves s linear systems with one matrix I - hγJ instead of a nonlinear system, so no Newton iteration is needed."
solves: [ode-initial-value-problem, stiff-ode-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", s: "the number of stages", d: "the dimension of y", C: "the cost of one evaluation of f"}
  time: {worst: "Θ(N (d^3 + s C + s d^2))"}
  space: {extra: "Θ(d^2 + s d)"}
  evaluations: {worst: "N s"}
properties: {deterministic: true, implicit: linear, one_step: true, order: "1 to 4 in common methods", a_stable: depends on γ, l_stable: "ROS2 and linearly implicit Euler", newton_free: true}
history:
  year: 1963
  people: [Howard H. Rosenbrock, Gerhard Wanner, Peter Kaps, Peter Rentrop, Trond Steihaug, Arne Wolfbrandt, Lawrence F. Shampine]
  note: Rosenbrock (1963) proposed replacing the Newton iteration of implicit Runge-Kutta methods by one linear solve per stage. Kaps, Rentrop and Wanner (1979 to 1981) built the modern ROW methods; Steihaug and Wolfbrandt (1979) introduced W-methods with inexact Jacobians.
prereqs: [runge-kutta-methods, stiff-ode-problem, newton-method-for-systems, l-stability]
see_also: [radau-iia-methods, backward-euler-method, backward-differentiation-formulas, exponential-integrators, implicit-runge-kutta-methods, embedded-runge-kutta-pairs, lu-decomposition, stability-region]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.7 (Rosenbrock-type methods, order conditions in Table 7.1, stability function, W-methods, the codes ROS4 and RODAS)
  - paper: "H. H. Rosenbrock, Some general implicit processes for the numerical solution of differential equations, The Computer Journal 5 (1963) 329-330"
    locator: the original linearly implicit methods; doi:10.1093/comjnl/5.4.329
  - paper: "P. Kaps and P. Rentrop, Generalized Runge-Kutta methods of order four with stepsize control for stiff ordinary differential equations, Numerische Mathematik 33 (1979) 55-68"
    locator: the GRK4 methods with embedded error estimates; doi:10.1007/BF01396495
  - paper: "T. Steihaug and A. Wolfbrandt, An attempt to avoid exact Jacobian and nonlinear equations in the numerical solution of stiff differential equations, Mathematics of Computation 33 (1979) 521-534"
    locator: W-methods, order conditions with an arbitrary matrix; doi:10.1090/S0025-5718-1979-0521273-8
  - paper: "J. G. Verwer, E. J. Spee, J. G. Blom and W. Hundsdorfer, A second-order Rosenbrock method applied to photochemical dispersion problems, SIAM Journal on Scientific Computing 20 (1999) 1456-1480"
    locator: the ROS2 method with γ = 1 + 1/√2 and its positivity behaviour; doi:10.1137/S1064827597326651
  - paper: "L. F. Shampine and M. W. Reichelt, The MATLAB ODE suite, SIAM Journal on Scientific Computing 18 (1997) 1-22"
    locator: ode23s, a modified Rosenbrock W-method of order 2 with an order 3 error estimate; doi:10.1137/S1064827594276424
---

Rosenbrock methods solve stiff initial value problems $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, with the stability of implicit methods but without nonlinear equations. An implicit Runge-Kutta step solves a nonlinear system by Newton's method; a Rosenbrock step takes the Jacobian $J = \partial f/\partial y$ into the formula itself, so each of its $s$ stages solves one linear system, always with the same matrix $I - h\gamma J$. One LU factorization and $s$ triangular solves per step replace the Newton iteration. Methods of order 2 to 4 with embedded error estimates are standard in stiff solvers, for example ode23s in MATLAB and RODAS in Hairer and Wanner's codes.

## In plain words

Stiff problems need implicit methods, which define the new value through an equation. Solving that equation exactly costs several rounds of Newton's method, each with a linear system.

Rosenbrock's idea is to do only the first Newton round, but to build the method so that this already gives the full accuracy. To make up for skipping the later rounds, the method uses several stages, each a small correction, and chooses the weights so that the errors cancel. Every stage solves a linear system with the same matrix, so the expensive factorization is done once per step. There is no loop that might fail to converge, but the method needs a good Jacobian.

## The problem

Given $f$, its Jacobian $J(t, y)$ and time derivative $f_t(t, y)$ (or finite differences), $t_0$, $y_0$, an end time $T \ge t_0$, a step size $h > 0$ and a method $(\alpha_{ij}, \gamma_{ij}, b_i, \gamma)$, compute $y_N \approx y(T)$. We assume $f$ is smooth and Lipschitz in $y$; in stiff problems the Lipschitz constant $L$ is huge but $J$ is dissipative. Costs are evaluations of $f$, Jacobian evaluations, LU factorizations of $d \times d$ matrices and linear solves. Errors are measured in the max norm.

## The algorithm

With $\alpha_i = \sum_{j<i}\alpha_{ij}$ and $\gamma_i = \gamma + \sum_{j<i}\gamma_{ij}$, one step of size $\tau$ computes, for $i = 1, \dots, s$,

$$(I - \tau\gamma J)\,k_i = \tau f\Big(t + \alpha_i\tau,\ y + \sum_{j<i}\alpha_{ij}k_j\Big) + \tau J\sum_{j<i}\gamma_{ij}k_j + \gamma_i\tau^2 f_t,$$

and then $y \leftarrow y + \sum_i b_i k_i$.

```pseudo id=main
ROSENBROCK(f, J, f_t, t0, y0, T, h, (α, Γ, b, γ))
L1  N ← ⌈(T − t0)/h − δ⌉; t ← t0, y ← y0           ▷ δ: relative slack 10^-9
L2  for n ← 0 to N − 1 do                           ▷ step τ = h, or T − t for the last step
L3      J ← ∂f/∂y(t, y); g ← ∂f/∂t(t, y); M ← LU(I − τγJ)
L4      for i ← 1 to s do
L5          F_i ← f(t + α_i τ, y + Σ_{j<i} α_ij k_j)
L6          solve M k_i = τ F_i + τ J Σ_{j<i} γ_ij k_j + γ_i τ^2 g
L7      y ← y + Σ_i b_i k_i
L8      t ← t + τ
    return (t, y)
```

The implementation provides four methods:

| method | $s$ | order | $\gamma$ | $R(\infty)$ | notes |
|---|---|---|---|---|---|
| linearly implicit Euler | 1 | 1 | 1 | 0 | $R(z) = 1/(1 - z)$ |
| ROS2 | 2 | 2 | $1 + 1/\sqrt2$ | 0 | L-stable W-method (Verwer et al. 1999) |
| ROS2, $\gamma = \frac12$ | 2 | 2 | $\frac12$ | $-1$ | $R$ equals the trapezoidal rule's $(1 + z/2)/(1 - z/2)$ |
| ROW3, $\gamma = \frac12$ | 3 | 3 | $\frac12$ | $-\frac13$ | A-stable; built here from the order conditions with Simpson weights $b = (\frac16, \frac23, \frac16)$, $\alpha_{21} = \frac12$, $\alpha_{31} = -1$, $\alpha_{32} = 2$, $\gamma_{32} = -3$ |

ROS2 has $\alpha_{21} = 1$, $\gamma_{21} = -2\gamma$ and $b = (\frac12, \frac12)$.

## Example

On the Robertson chemical kinetics problem ($d = 3$, rate constants $0.04$, $10^4$, $3 \times 10^7$, $y(0) = (1, 0, 0)$) the stiff initial layer needs short steps. With steps $10^{-5}$ up to $t = 10^{-3}$, $10^{-3}$ up to $t = 1$ and $0.1$ up to $t = 40$, 1489 steps in all, the maximum relative errors at $t = 40$ against the reference values $(0.7158270687, 9.185534764 \times 10^{-6}, 0.2841637457)$ are (observed):

| method | 1489 steps | all steps halved | halved again |
|---|---|---|---|
| linearly implicit Euler | 1.3e-3 | 6.5e-4 | 3.3e-4 |
| ROS2 | 3.4e-5 | 8.7e-6 | 2.2e-6 |
| ROW3, $\gamma = \frac12$ | 6.3e-8 | 1.3e-8 | 4.3e-9 |

No Newton iteration is involved, the sum $y_1 + y_2 + y_3 = 1$ is kept to rounding, while the explicit RKF45 code needs 7742 accepted steps just to reach $t = 10$ (see the [stiff problem page](/stiff-ode-problem/)), because $J$ has an eigenvalue of size $10^3$ to $10^4$ for most of the interval. On the nonstiff problem $y' = y\cos t$ the observed orders between $h = 0.025$ and $0.0125$ are 0.95, 2.06 and 2.98.

## Correctness

**Theorem (proved).** For $f \in C^{p+1}$ a Rosenbrock method has local error $O(h^{p+1})$, $p \le 3$, if and only if $\sum b_i = 1$ (order 1), $\sum b_i\beta_i' = \frac12 - \gamma$ (order 2), and $\sum b_i\alpha_i^2 = \frac13$, $\sum b_i\beta_{ik}\beta_k' = \frac16 - \gamma + \gamma^2$ (order 3), where $\beta_{ij} = \alpha_{ij} + \gamma_{ij}$, $\beta_i' = \sum_{j<i}\beta_{ij}$. Then the global error is $O(h^p)$.

The proof expands each stage in powers of $h$ and compares with the Taylor series of the solution; it also shows that the non-autonomous form is exactly the method applied to the autonomized system. If additionally $\sum b_i\alpha_i = \frac12$, order 2 holds with any matrix in place of $J$ (a W-method), which the tests confirm with $J = 0$ for ROS2. The stability function is $R(z) = 1 + zb^T(I - zB)^{-1}\mathbb{1}$ with $B = (\beta_{ij})$ and $\beta_{ii} = \gamma$, a rational function with denominator $(1 - \gamma z)^s$; the tests check it exactly with Fractions. Linear invariants $w^Ty$ are conserved exactly.

## Complexity

Per step: one Jacobian (or $d$ extra evaluations of $f$ by finite differences, plus one for $f_t$), one LU factorization, $\Theta(d^3)$ for a dense matrix, then $s$ evaluations of $f$, $s$ solves of $\Theta(d^2)$ each and up to $s$ Jacobian-vector products. The products are avoided in practice by the transformed variables $u_i = \sum_{j\le i}\gamma_{ij}k_j$ (HNW II, Section IV.7). Compared with an $s$-stage implicit Runge-Kutta method, which factors an $sd \times sd$ matrix (or a transformed equivalent) and iterates Newton, a Rosenbrock step costs one $d \times d$ factorization and exactly $s$ solves, which is predictable. Space is $\Theta(d^2)$ for the matrix plus $\Theta(sd)$ for the stages.

## Properties

- **Linearly implicit, one-step, no iteration**: the cost per step is fixed.
- **Order**: up to 4 in common codes (GRK4, ROS4, RODAS); the number of order conditions grows like for Runge-Kutta methods.
- **Stability**: $R(z) = P(z)/(1 - \gamma z)^s$, the same as for an SDIRK method with the same $\gamma$, order and $s = p$; $\gamma$ can be chosen for A- or L-stability.
- **Needs an accurate Jacobian** unless the method is a W-method. Errors in $J$ reduce the order of ordinary Rosenbrock methods.
- **Conserves linear invariants**, as all Runge-Kutta type methods do.
- **Easy to implement with step size control**: embedded methods share the stages.

## Variants and improvements

- **W-methods** (Steihaug and Wolfbrandt 1979) keep their order with any matrix, so the Jacobian can be reused over many steps or approximated.
- **Stiffly accurate methods** such as RODAS (Hairer and Wanner) have $y_{n+1}$ equal to the last internal stage and suit index 1 differential-algebraic equations.
- **Krylov-W methods** solve the linear systems with Krylov iterations for large sparse problems.
- **[Exponential integrators](/exponential-integrators/)** use $\varphi$-functions of $J$ instead of rational functions.
- **[Radau IIA](/radau-iia-methods/)** and other fully implicit methods iterate to convergence and keep their order for stiff problems where Rosenbrock methods suffer order reduction.

## When to use it

Use Rosenbrock methods for stiff problems of moderate size with an available or cheap Jacobian and moderate accuracy requirements, for example atmospheric chemistry, combustion kinetics and method-of-lines discretizations of reaction-diffusion equations. They avoid the convergence and tolerance logic of Newton iterations. For very large systems or tight tolerances, [BDF codes](/backward-differentiation-formulas/) or Radau IIA are usually preferred; for nonstiff problems an explicit method is cheaper.

## Pitfalls

- **Large first steps in a nonlinear initial layer.** On the Robertson problem, one fixed step of $h = 0.01$ from $t = 0$ uses the Jacobian at $y_2 = 0$, which misses the fastest reaction; ROS2 then lands on a state with negative concentrations and stays near a spurious equilibrium. Production codes start with tiny steps and control the error.
- **Overshooting internal stages.** With small $\gamma$ the first stage of a 2-stage method overshoots stiff components by a factor near $1/\gamma$. With fixed steps $h = 1$, $0.1$ and $0.01$ from $t = 0$ on Robertson, the 2-stage method with $\gamma = 1 - 1/\sqrt2$ overflowed, while $\gamma = 1 + 1/\sqrt2$ stayed bounded (though wrong). With the graded steps of the example both work, and the smaller $\gamma$ is more accurate ($3.2 \times 10^{-6}$ against $3.4 \times 10^{-5}$), so the choice is a trade between robustness and error constant.
- **Not L-stable.** With $\gamma = \frac12$ the 2-stage method has $R(-\infty) = -1$: on $y' = -50(y - \cos t)$ with $h = 0.4$ the error at $t = 1.2$ is $0.55$, against $0.031$ for ROS2.
- **Inexact Jacobians.** A finite-difference or outdated Jacobian lowers the order of methods that are not W-methods; ROW3 with $J$ replaced by 0 shows order about 1.9 instead of 3.
- **Order reduction** on very stiff problems and DAEs, as for other one-step methods with low stage order.

## Implementations

## History

Rosenbrock (1963) suggested methods that need only one linear solve per stage. Wanner and coauthors developed the general class in the 1970s and named it Rosenbrock-Wanner (ROW). Kaps and Rentrop (1979) gave fourth-order methods with embedded error estimators (GRK4), and Shampine (1982) and Hairer and Wanner (ROS4, RODAS) produced widely used codes. Steihaug and Wolfbrandt (1979) introduced W-methods that tolerate inexact Jacobians. Shampine and Reichelt's ode23s (1997) brought a Rosenbrock W-method into MATLAB, and Verwer, Spee, Blom and Hundsdorfer (1999) popularized ROS2 for atmospheric chemistry.

## References
