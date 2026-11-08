---
tag: W7X2PW
kind: algorithm
slug: implicit-runge-kutta-methods
name: Implicit Runge-Kutta methods
aliases:
- IRK methods
- fully implicit Runge-Kutta methods
- Gauss, Radau and Lobatto methods
area: numerical/differential-equations
level: advanced
summary: "Runge-Kutta methods whose s stages are defined by a coupled system of s d equations, solved by simplified Newton. They reach order 2s, A- and L-stability, and symplecticity."
solves: [ode-initial-value-problem, stiff-ode-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps", d: "the dimension of y", s: "the number of stages", m: "the number of Newton iterations per step", C: "the cost of one evaluation of f", J: "the cost of one Jacobian"}
  time: {worst: "Θ(N (J + s^3 d^3 + m (s C + s^2 d^2)))"}
  space: {extra: "Θ(s^2 d^2)"}
  evaluations: {worst: "N m s"}
properties: {deterministic: true, implicit: true, one_step: true, order: "up to 2s", a_stable: "Gauss, Radau IIA, Lobatto IIIA and IIIC", l_stable: "Radau IIA, Lobatto IIIC", symplectic: "Gauss"}
history:
  year: 1964
  people: [John C. Butcher, Byron L. Ehle]
  note: Butcher introduced fully implicit Runge-Kutta methods in 1964, including the Gauss methods of order 2s. Ehle showed in 1969 that the Gauss and Radau IIA families are A-stable.
prereqs: [runge-kutta-methods, butcher-tableau, newton-method-for-systems, a-stability]
see_also: [gauss-legendre-runge-kutta, radau-iia-methods, l-stability, collocation-method, rosenbrock-methods, backward-euler-method, symplectic-integrators, butcher-order-conditions]
sources:
  - paper: doi:10.1090/S0025-5718-1964-0159424-9
    title: John C. Butcher, Implicit Runge-Kutta processes, Mathematics of Computation 18 (1964) 50-64
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.3 (stability function, A- and L-stability), Section IV.5 (construction of implicit Runge-Kutta methods, Gauss, Radau and Lobatto), Section IV.8 (implementation, simplified Newton iterations) and Section IV.15 (B-convergence)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.7 (implicit Runge-Kutta methods, existence of a solution, collocation)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (Runge-Kutta methods, implicit methods and their implementation)
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section VI.4 (symplectic Runge-Kutta methods)
  - paper: doi:10.1007/BF01954907
    title: J. M. Sanz-Serna, Runge-Kutta schemes for Hamiltonian systems, BIT 28 (1988) 877-883
---

An implicit Runge-Kutta method solves the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, with steps whose $s$ stage values depend on each other: the matrix $A$ of the [Butcher tableau](/butcher-tableau/) $(A, b, c)$ is not strictly lower triangular. Each step therefore solves a nonlinear system of $s d$ equations, in practice by a simplified Newton iteration with one Jacobian and one LU factorization per step. The reward is that such methods can be [A-stable](/a-stability/) and [L-stable](/l-stability/), which no explicit method can be, and can reach order $2s$ with $s$ stages. The main families are the [Gauss methods](/gauss-legendre-runge-kutta/) (order $2s$, symplectic), the [Radau IIA methods](/radau-iia-methods/) (order $2s - 1$, L-stable) and the Lobatto III methods.

## In plain words

An explicit method looks only at points it already knows when it takes a step. An implicit method asks for the slopes at several points inside the step, and those points themselves depend on the slopes. So each step is a small puzzle: find the inside points that are consistent with the equation. A computer solves the puzzle by repeated corrections, much as it finds the root of an equation.

Each step costs more, but the steps can be much longer on problems that mix very fast and very slow change. On such problems an explicit method must take tiny steps to avoid blowing up, while a good implicit method stays calm with long steps.

## The problem

Given $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, a start value $y_0$, $T \ge t_0$, a step size $h > 0$ and a tableau with $s$ stages, compute $y_N \approx y(T)$. We assume $f$ is continuous and Lipschitz in $y$ with constant $L$, and $C^1$ for the Newton iteration. The cost model counts evaluations of $f$, Jacobians $J = f_y$, LU factorizations and linear solves, and the number of steps. The method of interest is usually for [stiff problems](/stiff-ode-problem/), where $hL$ is large.

## The algorithm

One step from $(t_n, y_n)$ with step $h$ defines stage values $Y_i = y_n + Z_i$ by

$$Z_i = h \sum_{j=1}^{s} a_{ij}\, f(t_n + c_j h,\, y_n + Z_j) \qquad (i = 1, \dots, s),$$

and then $y_{n+1} = y_n + h \sum_i b_i f(t_n + c_i h, Y_i)$. When $A$ is nonsingular, the stage equations give $h F = (A^{-1} \otimes I) Z$, so $y_{n+1} = y_n + \sum_i d_i Z_i$ with $d^{T} = b^{T}A^{-1}$, which needs no further evaluations of $f$ and is better on stiff problems (HW II, Section IV.8).

```pseudo id=main
IRK(f, J, (A, b, c), t0, y0, T, h, tol)
L1  N ← ⌈(T − t0)/h − δ⌉                     ▷ δ: relative slack 10^-9 against rounding
L2  t ← t0, y ← y0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1) h
L5      k ← t_next − t
L6      Jn ← J(t, y)                          ▷ one Jacobian per step (or forward differences: d extra f)
L7      M ← LU factors of I − k (A ⊗ Jn)       ▷ size s d
L8      Z ← 0                                 ▷ Z = (Z_1, ..., Z_s)
L9      repeat (at most m_max times, else fail)
L10         F_i ← f(t + c_i k, y + Z_i) for i = 1..s
L11         ΔZ ← M^{-1} (−Z + k (A ⊗ I) F)
L12         Z ← Z + ΔZ
L13     until ‖ΔZ‖ ≤ tol · max(1, ‖y‖)
L14     y ← y + Σ d_i Z_i if A is nonsingular, else y + k Σ b_i f(t + c_i k, y + Z_i)
L15     t ← t_next
L16 return (t, y)
```

The grid is built as for [Euler's method](/euler-method/): $T = t_0$ gives no step, $h > T - t_0$ gives one step of length $T - t_0$, and the last step ends exactly at $T$. Line L11 is a Newton step for $G(Z) = Z - k (A \otimes I) F(Z) = 0$ with the exact derivative replaced by $I - k(A \otimes J_n)$, frozen for the step: the simplified Newton iteration.

**Tableaux used below.** Implicit midpoint (Gauss, $s = 1$): $A = (\frac12)$, $b = (1)$, $c = (\frac12)$. Two-stage Gauss, order 4:

$$c = \begin{pmatrix} \frac12 - \frac{\sqrt3}{6} \\ \frac12 + \frac{\sqrt3}{6} \end{pmatrix}, \quad A = \begin{pmatrix} \frac14 & \frac14 - \frac{\sqrt3}{6} \\ \frac14 + \frac{\sqrt3}{6} & \frac14 \end{pmatrix}, \quad b = \begin{pmatrix} \frac12 & \frac12 \end{pmatrix}.$$

Two-stage Radau IIA, order 3: $c = (\frac13, 1)$, $A = \begin{pmatrix} 5/12 & -1/12 \\ 3/4 & 1/4 \end{pmatrix}$, $b = (\frac34, \frac14)$. Three-stage Lobatto IIIA, order 4: $c = (0, \frac12, 1)$, rows of $A$: $(0, 0, 0)$, $(\frac{5}{24}, \frac13, -\frac{1}{24})$, $(\frac16, \frac23, \frac16)$, $b = (\frac16, \frac23, \frac16)$. Two-stage Lobatto IIIC, order 2: $A = \begin{pmatrix} 1/2 & -1/2 \\ 1/2 & 1/2 \end{pmatrix}$, $b = (\frac12, \frac12)$, $c = (0, 1)$.

## Example

Take $y' = -2ty^2$, $y(0) = 1$, with solution $1/(1 + t^2)$, $h = 0.2$, $T = 1$, the exact Jacobian $-4ty$ and $\text{tol} = 10^{-12}$:

| $t_n$ | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|
| $y(t_n)$ | 1.000000 | 0.961538 | 0.862069 | 0.735294 | 0.609756 | 0.500000 |
| Gauss, $s = 2$ | 1.000000 | 0.961534 | 0.862057 | 0.735281 | 0.609747 | 0.499994 |
| Radau IIA, $s = 2$ | 1.000000 | 0.961696 | 0.862323 | 0.735553 | 0.609953 | 0.500120 |

The final errors are $5.7 \cdot 10^{-6}$ and $-1.2 \cdot 10^{-4}$. The Gauss run used 37 Newton iterations, 74 evaluations of $f$, 5 Jacobians and 5 LU factorizations of size 2; [Heun's method](/heuns-method/) with the same $h$ has error $-3.3 \cdot 10^{-3}$ with 10 evaluations.

**Observed orders.** Errors at $T = 1$ for $N = 10, 20, 40, 80$ steps on the same problem, and $p_{\text{obs}} = \log_2$ of the last ratio:

| method | $N = 10$ | $N = 20$ | $N = 40$ | $N = 80$ | $p_{\text{obs}}$ | $p$ |
|---|---|---|---|---|---|---|
| backward Euler | $3.31 \cdot 10^{-3}$ | $1.72 \cdot 10^{-3}$ | $8.73 \cdot 10^{-4}$ | $4.40 \cdot 10^{-4}$ | 0.990 | 1 |
| implicit midpoint | $4.83 \cdot 10^{-4}$ | $1.21 \cdot 10^{-4}$ | $3.02 \cdot 10^{-5}$ | $7.55 \cdot 10^{-6}$ | 2.000 | 2 |
| Lobatto IIIC, $s = 2$ | $9.95 \cdot 10^{-4}$ | $2.46 \cdot 10^{-4}$ | $6.09 \cdot 10^{-5}$ | $1.52 \cdot 10^{-5}$ | 2.006 | 2 |
| Radau IIA, $s = 2$ | $1.64 \cdot 10^{-5}$ | $2.14 \cdot 10^{-6}$ | $2.73 \cdot 10^{-7}$ | $3.45 \cdot 10^{-8}$ | 2.984 | 3 |
| Lobatto IIIA, $s = 3$ | $8.70 \cdot 10^{-7}$ | $5.43 \cdot 10^{-8}$ | $3.39 \cdot 10^{-9}$ | $2.12 \cdot 10^{-10}$ | 4.000 | 4 |
| Gauss, $s = 2$ | $3.50 \cdot 10^{-7}$ | $2.17 \cdot 10^{-8}$ | $1.36 \cdot 10^{-9}$ | $8.48 \cdot 10^{-11}$ | 4.001 | 4 |

**A stiff problem.** $y' = -10^6 (y - \cos t) - \sin t$, $y(0) = 0$, with solution $\cos t - e^{-10^6 t}$. Errors $y_N - \cos 1$ at $T = 1$:

| method | $N = 10$ | $N = 20$ | $N = 40$ | $N = 80$ |
|---|---|---|---|---|
| explicit Euler (as a tableau) | $-1.0 \cdot 10^{50}$ | $-9.5 \cdot 10^{93}$ | $-8.3 \cdot 10^{175}$ | overflow |
| Gauss, $s = 2$ | $-0.9989$ | $-0.9952$ | $-0.9810$ | $-0.9261$ |
| Lobatto IIIA, $s = 3$ | $-0.9988$ | $-0.9952$ | $-0.9810$ | $-0.9261$ |
| Radau IIA, $s = 2$ | $9.09 \cdot 10^{-10}$ | $2.31 \cdot 10^{-10}$ | $5.80 \cdot 10^{-11}$ | $1.46 \cdot 10^{-11}$ |
| Lobatto IIIC, $s = 2$ | $-2.84 \cdot 10^{-8}$ | $-1.39 \cdot 10^{-8}$ | $-6.84 \cdot 10^{-9}$ | $-3.40 \cdot 10^{-9}$ |

With $h = 0.1$, explicit Euler multiplies the transient by $|1 - 10^5|$ per step. The A-stable but not L-stable Gauss and Lobatto IIIA methods have $|R(\infty)| = 1$, so the initial jump of size 1 is not damped. The L-stable Radau IIA and Lobatto IIIC methods damp it in one step. Radau IIA converges here with observed order 2, below its classical order 3: this is the order reduction of stiff problems (HW II, Section IV.15). Since the problem is linear and the Jacobian is exact, each step takes exactly 2 Newton iterations: the first solves the stage equations, the second confirms $\Delta Z = 0$.

## Correctness

Four facts make the algorithm correct; the proofs are in the correctness file.

1. **The stage equations have a unique solution for $h L \|A\|_\infty < 1$**, where $\|A\|_\infty = \max_i \sum_j |a_{ij}|$: the map $Z \mapsto h (A \otimes I) F(Z)$ is a contraction in the norm $\max_i \|Z_i\|$ (HNW I, Section II.7). This is a proved, non-asymptotic statement, but on stiff problems $hL$ is large and it says nothing; there existence follows from one-sided Lipschitz conditions and algebraic stability (HW II, Section IV.14).
2. **The simplified Newton iteration finds that solution.** If the iteration of line L11 converges, its limit solves the stage equations, because $M$ is invertible. Its iteration map has derivative $k\, M^{-1} (A \otimes (f_y(\cdot) - J_n))$, so it contracts when $k$ times the variation of $f_y$ near $(t_n, y_n)$ is small. For linear problems with constant Jacobian, one iteration solves the system exactly.
3. **The update of line L14 equals the Runge-Kutta formula.** If the stage equations hold and $A$ is nonsingular, $k \sum_i b_i F_i = \sum_i d_i Z_i$.
4. **Convergence of order $p$.** If the tableau satisfies the [Butcher order conditions](/butcher-order-conditions/) up to order $p$, the local error is $O(h^{p+1})$ (Butcher's theorem, HNW I, Section II.2, cited, not proved here). The step map is Lipschitz with constant $1 + h\Lambda$, $\Lambda = L\|b\|_1 / (1 - hL\|A\|_\infty)$, so the [Gronwall](/gronwall-inequality/) argument gives a global error $O(h^p)$ for nonstiff problems. For stiff problems, B-convergence results give orders that depend on the stage order (HW II, Section IV.15); these are proved for problems with a one-sided Lipschitz condition.

The tests check the order conditions with exact fractions for the rational tableaux, the stability functions exactly, and the observed orders by halving $h$.

## Complexity

Each step costs one Jacobian (or $d$ extra evaluations of $f$ for a difference Jacobian), one LU factorization of the $s d \times s d$ matrix in $\Theta(s^3 d^3)$, and per Newton iteration $s$ evaluations of $f$ and one solve in $\Theta(s^2 d^2)$. With $m$ iterations per step, the time is $\Theta(N (J + s^3 d^3 + m(sC + s^2 d^2)))$ and the extra space $\Theta(s^2 d^2)$ for the factors. For large $d$ the factorization dominates. Butcher's transformation diagonalizes $A^{-1}$ and splits the system into one real $d \times d$ system per real eigenvalue and one complex $d \times d$ system per complex pair, about $\Theta(s d^3)$ instead of $\Theta(s^3 d^3)$ (HW II, Section IV.8). Sparse or banded Jacobians, as from the [method of lines](/method-of-lines/), cut the cost further.

## Properties

- **Stability function.** $R(z) = 1 + z b^{T}(I - zA)^{-1}\mathbb{1} = \det(I - zA + z \mathbb{1} b^{T}) / \det(I - zA)$, rational of degree at most $s$. Gauss: diagonal Padé approximation $R_{s,s}$, so $|R(iy)| = 1$ and $R(\infty) = (-1)^s$. Radau IIA: $R_{s-1,s}$, so $R(\infty) = 0$. Lobatto IIIA: $R_{s-1,s-1}$. Lobatto IIIC: $R_{s-2,s}$. For the two-stage Radau IIA method $R(z) = (1 + z/3)/(1 - 2z/3 + z^2/6)$.
- **Order.** Gauss $2s$, the maximum for $s$ stages; Radau IIA $2s - 1$; Lobatto IIIA and IIIC $2s - 2$. These come from the simplifying assumptions $B(p)$, $C(q)$, $D(r)$ (HW II, Section IV.5).
- **Collocation.** The Gauss, Radau IIA and Lobatto IIIA methods are [collocation methods](/collocation-method/): the stage values are the values of a polynomial of degree $s$ that satisfies the equation at the nodes $t_n + c_i h$. The stage order of Gauss and Radau IIA is $s$.
- **Symplecticity.** A Runge-Kutta method is symplectic exactly when $b_i a_{ij} + b_j a_{ji} - b_i b_j = 0$ for all $i, j$ (Sanz-Serna 1988; HLW GNI, Section VI.4). The Gauss methods satisfy this, so they preserve every quadratic invariant: on the harmonic oscillator with $h = 0.5$, the two-stage Gauss method keeps $y_1^2 + y_2^2 = 1$ to $10^{-12}$ over 200 steps, while Radau IIA multiplies it by $|R(i/2)|^2$ per step, down to $0.71$.
- **Stiff accuracy.** Radau IIA and Lobatto IIIC have $a_{sj} = b_j$, so $y_{n+1} = Y_s$. This is the property that makes them L-stable and suits them to [differential-algebraic equations](/differential-algebraic-equations/).

## Variants and improvements

- **Diagonally implicit methods (DIRK, SDIRK).** $A$ lower triangular, so the stages are solved one at a time, each a $d$-dimensional system; with equal diagonal entries one LU serves all stages. The attainable order is lower than for fully implicit methods with the same $s$ (HW II, Section IV.6).
- **[Rosenbrock methods](/rosenbrock-methods/).** Replace the Newton iteration by a fixed number of linear solves with the exact Jacobian built into the formula.
- **Radau5.** The three-stage Radau IIA method of order 5 with step size control and the transformed Newton iteration, the classical code of HW II.
- **Starting values.** Extrapolating the collocation polynomial of the previous step gives a better $Z$ than zero in line L8 and saves iterations.
- **Reuse of the Jacobian.** Production codes keep $J$ and the LU over several steps and refactor only when the Newton iteration converges slowly or $h$ changes much.

## When to use it

Use an implicit Runge-Kutta method for stiff problems that need high accuracy, such as chemical kinetics, circuit equations and semi-discretized parabolic PDEs: Radau IIA is the standard choice, and it handles index-1 and index-2 [differential-algebraic equations](/differential-algebraic-equations/). Use the Gauss methods for long integrations of [Hamiltonian systems](/hamiltonian-systems/) where conserving invariants matters. For nonstiff problems, explicit methods such as [Dormand-Prince](/dormand-prince-method/) are much cheaper per unit of accuracy. For very large stiff systems, [BDF](/backward-differentiation-formulas/) codes are often cheaper per step.

## Pitfalls

- **Newton tolerance and failure.** A loose tolerance spoils the order and, for the Gauss method, the conservation of invariants. When the iteration diverges, the right response is to reduce $h$, not to accept the last iterate; the implementation raises an error.
- **Using $b$ instead of $d$ on stiff problems.** Evaluating $f$ at the stage values multiplies their small errors by the large Jacobian; the form $y_n + \sum d_i Z_i$ avoids this.
- **A-stable is not enough.** Gauss and trapezoidal-type methods keep fast transients alive with $|R| \approx 1$; use an L-stable method when the initial data or the forcing excite stiff components.
- **Order reduction.** On stiff problems the observed order can drop to about the stage order, as in the table above.
- **Difference Jacobians.** A forward difference with increment $\sqrt{\varepsilon}\,\max(1, |y_j|)$ costs $d$ evaluations and is accurate to about $\sqrt{\varepsilon}$, enough for simplified Newton but not for badly scaled problems.

## Implementations

## History

Butcher introduced fully implicit Runge-Kutta methods in 1964 and showed that the Gauss methods with $s$ stages have order $2s$. Ehle proved in 1969 that the Gauss and Radau IIA methods are A-stable and introduced L-stability. Butcher gave the transformation that makes the Newton iteration affordable in 1976, and Hairer and Wanner built it into the code Radau5 (HW II, Section IV.8). Sanz-Serna, Lasagni and Suris found in 1988 the condition for symplectic Runge-Kutta methods.

## References
