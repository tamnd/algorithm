---
tag: NRVHTE
kind: algorithm
slug: backward-differentiation-formulas
name: Backward differentiation formulas
aliases:
- BDF methods
- Gear's methods
- BDF
area: numerical/differential-equations
level: core
summary: Implicit multistep methods that set the derivative of the polynomial through the new and last k values equal to f at the new point. Order k, zero-stable for k <= 6; the standard stiff method.
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", k: "the order", d: "the dimension of y", m: "the number of Newton iterations per step"}
  time: {worst: "Θ(N (k d + m d^3))"}
  space: {extra: "Θ(k d + d^2)"}
  evaluations: {worst: "Θ(N m d)"}
properties: {deterministic: true, explicit: false, multistep: true, order: "k", zero_stable: "k <= 6", a_stable: "k <= 2", stiff: true, self_starting: false}
history:
  year: 1952
  people: [Charles F. Curtiss, Joseph O. Hirschfelder, C. William Gear]
  note: Curtiss and Hirschfelder (1952) introduced the formulas for stiff chemical kinetics; Gear's DIFSUB (1971) made variable-order BDF the standard stiff solver.
prereqs: [backward-euler-method, zero-stability]
see_also: [stiff-ode-problem, a-stability, l-stability, dahlquist-barrier, linear-multistep-methods, adams-moulton-methods, radau-iia-methods, newton-method-for-systems]
sources:
  - paper: doi:10.1073/pnas.38.3.235
    title: C. F. Curtiss and J. O. Hirschfelder, Integration of stiff equations, Proceedings of the National Academy of Sciences 38 (1952) 235-243
    locator: the backward differentiation formulas and their use for stiff problems
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section V.1 (stability of BDF, A(alpha)-stability angles, stiff decay), Section V.2 (order stars and the second Dahlquist barrier), Section VI.2 (implementation of BDF)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.1 (backward differentiation formulas), Section III.3 (stability of BDF, zero-stable for k <= 6)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 2, Section 2.3 (backward differentiation formulae) and Chapter 4, Section 4.4 (A-stability of multistep methods)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 5 (linear multistep methods; BDF and their implementation)
  - book: "C. W. Gear, Numerical Initial Value Problems in Ordinary Differential Equations, Prentice-Hall, 1971"
    locator: the variable-order BDF code DIFSUB
  - paper: "C. W. Cryer, On the instability of high order backward-difference multistep methods, BIT 12 (1972) 17-25"
    locator: BDF of order k >= 7 is not zero-stable
---

The backward differentiation formulas (BDF) are implicit [linear multistep methods](/linear-multistep-methods/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. The $k$-step formula fits the polynomial of degree $k$ through the unknown $y_{n+1}$ and the known values $y_n, \dots, y_{n+1-k}$, and asks that its derivative at $t_{n+1}$ equal $f(t_{n+1}, y_{n+1})$. BDF1 is [backward Euler](/backward-euler-method/). The method of order $k$ is [zero-stable](/zero-stability/) exactly for $k \le 6$, A-stable for $k \le 2$ and A($\alpha$)-stable with large $\alpha$ up to $k = 5$, and it damps very stiff components almost completely. With one Newton solve of size $d$ per step, it is the method behind most general-purpose [stiff](/stiff-ode-problem/) solvers: DIFSUB, LSODE, VODE, DASSL, CVODE and MATLAB's ode15s.

## In plain words

Instead of guessing how the slope will change, the method looks at the path drawn through the last few computed points and the new point it is looking for. It requires that the slope of that path at the new point agree with the slope the differential equation demands there. Finding a new point that satisfies this means solving an equation in every step. The reward is that the method stays calm on problems where some parts of the solution die out extremely fast: it simply lets those parts vanish, even with steps far longer than their lifetime. Using more past points makes it more accurate, but beyond six points the method itself becomes unstable and useless.

## The problem

**Notation.** As on all differential-equations pages: $y' = f(t, y)$ on $[t_0, T]$, $y \in \mathbb{R}^d$, step $h$, $t_n = t_0 + nh$, $y_n \approx y(t_n)$; $e_n = y(t_n) - y_n$; order $p$; $z = h\lambda$; $\rho$, $\sigma$ the polynomials of the method; $\nabla y_{n+1} = y_{n+1} - y_n$ the backward difference.

The $k$-step BDF is
$$\sum_{j=1}^{k}\frac{1}{j}\nabla^jy_{n+1} = hf(t_{n+1}, y_{n+1}),$$
so $\sigma(\zeta) = \zeta^k$. Written as $\sum_{i=0}^k\alpha_iy_{n+1-i} = hf_{n+1}$, the coefficients are:

| $k$ | $\alpha_0, \alpha_1, \dots, \alpha_k$ | error constant | A($\alpha$) angle |
|---|---|---|---|
| 1 | $1, -1$ | $-1/2$ | $90°$ (A-stable) |
| 2 | $\tfrac32, -2, \tfrac12$ | $-1/3$ | $90°$ (A-stable) |
| 3 | $\tfrac{11}{6}, -3, \tfrac32, -\tfrac13$ | $-1/4$ | $86.03°$ |
| 4 | $\tfrac{25}{12}, -4, 3, -\tfrac43, \tfrac14$ | $-1/5$ | $73.35°$ |
| 5 | $\tfrac{137}{60}, -5, 5, -\tfrac{10}{3}, \tfrac54, -\tfrac15$ | $-1/6$ | $51.84°$ |
| 6 | $\tfrac{49}{20}, -6, \tfrac{15}{2}, -\tfrac{20}{3}, \tfrac{15}{4}, -\tfrac65, \tfrac16$ | $-1/7$ | $17.84°$ |

The error constant is that of the local error $-\frac{1}{k+1}h^{k+1}y^{(k+1)}$ in this normalization, and $\alpha_0 = \sum_{j=1}^k 1/j$. The angles were computed from the boundary locus $z(\theta) = \sum_{j=1}^k\frac1j(1 - e^{-i\theta})^j$ and agree with the values in Hairer and Wanner, Section V.1.

## The algorithm

```pseudo id=main
BDF(f, t0, y0, T, h, k)                              ▷ 1 ≤ k ≤ 6
L1  N ← ⌈(T − t0)/h⌉; if N = 0 return (t0, y0); h ← (T − t0)/N
L2  α_i ← coefficient of y_{n+1−i} in Σ_{j=1}^{k} ∇^j y_{n+1} / j, exactly
L3  y_0 ← y0
L4  for n = 0 to min(k − 1, N) − 1 do y_{n+1} ← one step of the 3-stage Gauss method   ▷ starting values
L5  for n = k − 1 to N − 1 do
L6      g ← −Σ_{i=1}^{k} (α_i / α_0) y_{n+1−i}
L7      x ← y_n                                    ▷ initial guess
L8      solve x = g + (h/α_0) f(t_{n+1}, x) by Newton: (I − (h/α_0) J) δ = g + (h/α_0) f(t_{n+1}, x) − x, x ← x + δ
L9      y_{n+1} ← x
L10 return (t_n, y_n) for n = 0, …, N
```

$J$ is $\partial f/\partial y$ at the iterate, from the caller or by forward differences. The starting values come from the 3-stage Gauss method, which is implicit, A-stable and of order 6, so that starting does not spoil the order or the stiff stability. Unlike Adams methods, BDF stores past values of $y$, not of $f$. Line L1 shrinks the step to fit the interval.

## Example

**A nonlinear step.** $y' = -2ty^2$, $y(0) = 1$, $k = 2$, $h = 0.1$. The Gauss step gives $y_1 = 0.99009901$ (exact $1/1.01$ to nine digits). Then $y_2$ solves $\tfrac32y_2 - 2y_1 + \tfrac12y_0 = 0.1 \cdot (-0.4y_2^2)$, a quadratic; Newton gives $y_2 = 0.9621143$, against the exact $0.9615385$. On $[0, 2]$ the observed orders at the last halving of $h$ (from $h = 0.0125$ to $0.00625$) are $0.99, 2.00, 2.93, 3.99, 4.82, 5.96$ for $k = 1, \dots, 6$.

**A stiff linear problem.** $y' = -1000(y - \cos t) - \sin t$, $y(0) = 1$, exact $y = \cos t$, with $h = 0.1$, so $z = -100$. Every explicit method in this collection explodes at this step. BDF gives errors at $t = 1$ of $2.8 \cdot 10^{-5}$, $2.7 \cdot 10^{-6}$, $1.6 \cdot 10^{-7}$, $1.5 \cdot 10^{-8}$, $1.2 \cdot 10^{-9}$ and $4.6 \cdot 10^{-10}$ for $k = 1, \dots, 6$.

**Robertson's chemical kinetics problem.** $y_1' = -0.04y_1 + 10^4y_2y_3$, $y_2' = 0.04y_1 - 10^4y_2y_3 - 3\cdot10^7y_2^2$, $y_3' = 3\cdot10^7y_2^2$, $y(0) = (1, 0, 0)$, with eigenvalues of the Jacobian down to about $-10^4$. BDF2 with the fixed step $h = 0.04$ (1000 steps) gives at $t = 40$ the values $y_1 = 0.7158261$ and $y_2 = 9.18550 \cdot 10^{-6}$, against the reference $0.7158271$ and $9.18553 \cdot 10^{-6}$. The total $y_1 + y_2 + y_3$ stays equal to 1 within $10^{-13}$: every linear multistep method preserves linear invariants exactly, up to rounding and the Newton tolerance.

## Correctness

The proofs are in `proofs/correctness.md`. In summary:

1. **Order $k$.** If $y \in C^{k+1}$, the local truncation error $\sum_j\frac1j\nabla^jy(t_{n+1}) - hy'(t_{n+1})$ equals $-\frac{1}{k+1}h^{k+1}y^{(k+1)}(\xi)$ for scalar $y$ and is bounded by $\frac{1}{k+1}M_{k+1}h^{k+1}$ in general. The tests check $C_0 = \dots = C_k = 0$ and $C_{k+1} = -1/(k+1)$ exactly with fractions for $k \le 7$.
2. **Zero-stability.** The roots of $\rho$ other than 1 have modulus at most $0.3333, 0.4264, 0.5609, 0.7087, 0.8634$ for $k = 2, \dots, 6$ (computed), so BDF$k$ is zero-stable for $k \le 6$; for $k = 7$ a root of modulus $1.0222$ appears, and Cryer (1972) proved instability for all $k \ge 7$ (cited, not reproved). With consistency, Dahlquist's [equivalence theorem](/dahlquist-equivalence-theorem/) gives convergence of order $k$ on non-stiff problems for $k \le 6$.
3. **A-stability of BDF2** is proved directly: the boundary locus satisfies $\operatorname{Re}z(\theta) = (1 - \cos\theta)^2 \ge 0$. BDF$k$ for $k \ge 3$ cannot be A-stable, by the [second Dahlquist barrier](/dahlquist-barrier/).
4. **Stiff decay.** As $z \to \infty$, the roots of $\rho(\zeta) - z\sigma(\zeta)$ tend to those of $\sigma(\zeta) = \zeta^k$, which are all 0, so very stiff components are damped completely in one step, as for an [L-stable](/l-stability/) one-step method.

## Complexity

The cost model counts evaluations of $f$, Jacobians and linear solves. Each step costs $m$ Newton iterations, each with one evaluation of $f$, one Jacobian (or $d$ evaluations by differences) and one LU solve of size $d$, $\Theta(d^3)$ for dense $J$. Production codes keep $J$ and the LU factors of $I - (h/\alpha_0)J$ over many steps (modified Newton), so the typical cost per step is one or two evaluations and back-substitutions, and a refactorization only when $h$, $k$ or $J$ change much. The memory is $k$ past vectors plus the matrix. In this implementation the start costs $k - 1$ Gauss steps, each solving a system of size $3d$.

## Properties

- **Implicit, order $k$, $1 \le k \le 6$.** Error constants $-1/(k+1)$ in the normalization above, larger than those of Adams-Moulton of the same order.
- **A-stable for $k \le 2$, A($\alpha$)-stable for $k \le 6$** with the angles in the table, and the stability regions contain a disc around $-\infty$ in each case (stiffly stable in Gear's sense).
- **Stiff decay**: $R(\infty)$-type damping, all roots tend to 0 as $z \to -\infty$.
- **BDF2 is G-stable** (Dahlquist 1978), which gives contractivity for nonlinear problems with a one-sided Lipschitz constant $\le 0$ in a suitable norm.
- **Not suitable for oscillatory stiff problems** with eigenvalues near the imaginary axis when $k \ge 3$, because of the reduced angle $\alpha$.

## Variants and improvements

- **Variable step size and order.** Codes use fixed-leading-coefficient or Nordsieck forms to change $h$ and $k$; step size control uses the predictor-corrector difference as an error estimate.
- **Numerical differentiation formulas (NDF).** Klopfenstein's and Shampine's modification adds a term $\kappa\gamma_k\nabla^{k+1}y_{n+1}$ that improves the error constant at a small cost in stability angle; ode15s uses NDF1 to NDF5 (Shampine and Reichelt 1997).
- **DAEs.** BDF applies directly to implicit systems $F(t, y, y') = 0$ by replacing $y'$ with the BDF difference quotient (DASSL, IDA).
- **Alternatives for stiff problems.** [Radau IIA](/radau-iia-methods/) methods (order $2s - 1$, L-stable for every order), Rosenbrock methods, and [Gauss methods](/gauss-legendre-runge-kutta/) for stiff oscillatory problems.

## When to use it

Use BDF for stiff problems: chemical kinetics, circuit simulation, the [method of lines](/method-of-lines/) for parabolic PDEs, control systems with fast modes, and DAEs of index 1. Orders 1 to 5 are common; order 6 is rarely used because of its small angle. For non-stiff problems Adams methods are more accurate per step, and for stiff problems with eigenvalues close to the imaginary axis A-stable one-step methods are safer.

## Pitfalls

- **Fixed-point iteration instead of Newton.** Iterating $x \leftarrow g + (h/\alpha_0)f(x)$ converges only if $hL/\alpha_0 < 1$, which throws away all the stiff stability.
- **Starting with an explicit method.** A stiff problem makes RK4 starting steps blow up; the starting method must itself be stable for stiff problems, as Gauss or lower-order BDF with small steps are.
- **Order 7 and above.** Not zero-stable: errors grow like $1.0222^n$ even for $h \to 0$, and the implementation refuses $k = 7$.
- **Oscillatory stiff components.** BDF3 to BDF6 are unstable for $z$ near the imaginary axis with large modulus, such as lightly damped mechanical vibrations.
- **Changing $h$ in a fixed-coefficient code** without interpolating the history makes the method inconsistent; variable-step BDF also loses zero-stability if the step ratio changes too fast.

## Implementations

## History

Curtiss and Hirschfelder introduced the formulas in 1952, in the same paper that named stiff equations, to integrate chemical kinetics. Dahlquist's 1963 barrier showed that no linear multistep method beyond order 2 could be A-stable, which made BDF's near A-stability valuable. Gear's book and code DIFSUB (1971) introduced automatic variable step and variable order BDF with Newton iteration, the design of all later stiff multistep codes. Cryer (1972) proved that BDF of order 7 and above is not zero-stable.

## References
