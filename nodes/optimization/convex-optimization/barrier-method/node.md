---
tag: 0ZMXKV
kind: algorithm
slug: barrier-method
name: Barrier method
aliases:
- log-barrier method
- logarithmic barrier method
- sequential unconstrained minimization
- SUMT
area: optimization/convex-optimization
level: advanced
summary: Solve a sequence of unconstrained problems with a log barrier that grows in weight.
solves: [semidefinite-programming, linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, p: the size of the matrices in the constraint, r: the ratio p/(t_0 ε) of the first gap to the target gap}
  time: {worst: O(p^(1/2) log(r) (n p^3 + n^2 p^2 + n^3))}
  space: {extra: O(n p^2 + n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1955
  people: [Ragnar Frisch, Anthony Fiacco, Garth McCormick, Yurii Nesterov, Arkadi Nemirovski]
  note: Frisch proposed the logarithmic barrier in 1955. Fiacco and McCormick made the sequential unconstrained minimization technique a general method in the 1960s. Nesterov and Nemirovski (1994) proved a polynomial bound on the Newton steps for any self-concordant barrier.
prereqs: [convex-optimization-problem, kkt-conditions, newton-method-for-systems]
see_also: [interior-point-method, central-path, self-concordant-function, penalty-method, semidefinite-programming, lagrangian-duality, backtracking-line-search, karmarkar-algorithm]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.6 (self-concordance and the Newton step bound), Chapter 11 (Section 11.2 the logarithmic barrier and the central path, Section 11.3 the barrier method, Section 11.5 complexity analysis, Section 11.6 problems with generalized inequalities)
  - book: isbn:9780898712544
    title: Anthony V. Fiacco and Garth P. McCormick, Nonlinear Programming, Sequential Unconstrained Minimization Techniques, SIAM Classics edition, 1990
    locator: Chapter 3 (interior point unconstrained minimization techniques)
  - book: isbn:9780898713190
    title: Yurii Nesterov and Arkadii Nemirovskii, Interior-Point Polynomial Algorithms in Convex Programming, SIAM, 1994
    locator: Chapter 2 (self-concordant functions and barriers), Chapter 3 (path-following methods)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 19, Interior-point methods for nonlinear programming
  - paper: doi:10.1137/1038003
    title: Lieven Vandenberghe and Stephen Boyd, Semidefinite programming, SIAM Review 38(1), 1996
    locator: pages 49 to 95 (the barrier for the linear matrix inequality, the central path and the dual point F(x)^-1/t)
---

The barrier method solves a constrained convex problem by a sequence of unconstrained ones. It replaces the hard constraint by a logarithmic barrier term that goes to infinity at the boundary of the feasible set, minimizes $t\,c^\top x + \phi(x)$ with [Newton's method](/newton-method-for-systems/), multiplies $t$ by a factor $\mu$, and repeats from the last point. The minimizers form the [central path](/central-path/), and each of them gives a dual feasible point with [duality gap](/lagrangian-duality/) exactly $\nu/t$, where $\nu$ is the barrier parameter. So after $\lceil\log(\nu/(t_0\varepsilon))/\log\mu\rceil$ increases of $t$ the gap is at most $\varepsilon$. For a [self-concordant](/self-concordant-function/) barrier, each centering needs a number of Newton steps that does not depend on the data.

## In plain words

A wall is hard to handle with a method that follows the slope of a function. The barrier method replaces each wall with a smooth slope that rises to infinity just before the wall. Then the problem has no walls, and Newton's method can solve it.

The smooth slope pushes the answer away from the walls, so it is not the true answer. To fix this, the method gives more and more weight to the real objective and less to the slope. After each change it starts Newton's method again from the last answer, which is already close. The answers move along a curve to the true optimum. At each point of the curve there is an exact bound on the error, so the method knows when to stop.

## The problem

We state the method for the inequality form of a [semidefinite program](/semidefinite-programming/), which contains [linear programs](/linear-programming-problem/) as the diagonal case:

$$\min_{x \in \mathbb{R}^n}\ c^\top x \quad \text{s.t.} \quad F(x) = F_0 + x_1 F_1 + \cdots + x_n F_n \succeq 0,$$

with symmetric $p \times p$ matrices $F_i$. An LP $\min c^\top x$, $Ax \le b$ with $p$ rows is the case $F_0 = \operatorname{diag}(b)$ and $F_i = -\operatorname{diag}(A_{:,i})$. The dual program is

$$\max_{Z}\ -\operatorname{tr}(F_0 Z) \quad \text{s.t.} \quad \operatorname{tr}(F_i Z) = c_i\ (i = 1, \ldots, n), \quad Z \succeq 0.$$

The barrier is $\phi(x) = -\log\det F(x)$, defined where $F(x) \succ 0$, and its parameter is $\nu = p$. The input is the data, a strictly feasible start $x^0$ (with $F(x^0) \succ 0$), $t_0 > 0$, $\mu > 1$ and the target gap $\varepsilon$. The output is a strictly feasible $x$ and a dual feasible $Z$ whose gap is at most $\varepsilon$. We assume that $F_1, \ldots, F_n$ are linearly independent and that the feasible set is bounded, so that each centering problem has exactly one minimizer.

## The algorithm

```pseudo id=main
BARRIER-METHOD(c, F, x, t₀, μ, ε)          ▷ F(x) ≻ 0
L1  t ← t₀
L2  loop
L3      x ← CENTER(c, F, x, t)              ▷ minimize φ_t(x) = t·cᵀx − log det F(x)
L4      if p / t ≤ ε then exit loop         ▷ the gap of a central point is p/t
L5      t ← μ·t
L6  return x, Z = F(x)⁻¹ / t               ▷ Z is the dual point

CENTER(c, F, x, t)                          ▷ Newton's method with backtracking
L7      g_i ← t·c_i − tr(F⁻¹F_i),  H_ij ← tr(F⁻¹F_i F⁻¹F_j)   ▷ F = F(x)
L8      Δx ← −H⁻¹ g,  λ² ← −gᵀΔx
L9      if λ²/2 ≤ ε_nt then return x
L10     s ← 1; while φ_t(x + sΔx) > φ_t(x) − α·s·λ² do s ← β·s   ▷ φ_t = +∞ if F(x + sΔx) is not ≻ 0
L11     x ← x + sΔx; go to L7
```

Line L7 uses the derivatives of $-\log\det$: the gradient entry is $-\operatorname{tr}(F^{-1}F_i)$ and the Hessian entry is $\operatorname{tr}(F^{-1}F_iF^{-1}F_j)$. The line search of line L10, with $0 < \alpha < 1/2$ and $0 < \beta < 1$, keeps every iterate strictly feasible, because $\phi_t$ is $+\infty$ outside the open set $F(x) \succ 0$. The implementation uses $\alpha = 0.25$, $\beta = 0.5$ and $\varepsilon_{nt} = 10^{-12}$. Line L6 uses the zero gradient at the center: $t c_i = \operatorname{tr}(F^{-1}F_i)$ says that $Z = F^{-1}/t$ satisfies the dual equations.

## Example

Take $\min x$ subject to $0 \le x \le 1$. As a constraint of size $p = 2$ it is $F(x) = \operatorname{diag}(x, 1 - x) \succeq 0$, so $F_0 = \operatorname{diag}(0, 1)$ and $F_1 = \operatorname{diag}(1, -1)$. The barrier is $-\log x - \log(1 - x)$. The center solves $t - 1/x + 1/(1 - x) = 0$, that is, $t x^2 - (t + 2)x + 1 = 0$, so

$$x^*(t) = \frac{(t + 2) - \sqrt{t^2 + 4}}{2t}, \qquad Z = \frac{1}{t}\operatorname{diag}\Big(\frac{1}{x^*}, \frac{1}{1 - x^*}\Big).$$

The gap is $x^* + Z_{22} = 2/t$ for every $t$. With $x^0 = 1/2$, $t_0 = 1$, $\mu = 10$ and $\varepsilon = 10^{-6}$:

| centering | $t$ | $x^*(t)$ | gap $2/t$ | Newton steps |
|---|---|---|---|---|
| 1 | 1 | 0.381966 | 2 | 3 |
| 2 | 10 | 0.0900980 | 0.2 | 5 |
| 3 | 100 | 0.00990001 | 0.02 | 7 |
| 4 | 1000 | 0.000999000 | 0.002 | 6 |
| 5 to 7 | $10^4$ to $10^6$ | about $1/t$ | $2/t$ | 6 each |
| 8 | $10^7$ | $1.0 \times 10^{-7}$ | $2 \times 10^{-7}$ | 6 |

The first value is $(3 - \sqrt5)/2$. The method stops after $8 = \lceil\log_{10}(2 \cdot 10^6)\rceil + 1$ centerings and 45 Newton steps. The returned dual point is $Z \approx \operatorname{diag}(1, 10^{-7})$, which is close to the dual optimum $\operatorname{diag}(1, 0)$.

## Correctness

Three facts make the method correct. First, every iterate is strictly feasible, because the line search never accepts a point where $\phi_t = +\infty$. Second, at the exact center $x^*(t)$ the gradient is $0$, so $Z = F(x^*)^{-1}/t$ is positive definite and satisfies $\operatorname{tr}(F_i Z) = c_i$. Third, the gap of this pair is $c^\top x^* + \operatorname{tr}(F_0 Z) = \operatorname{tr}(F(x^*)Z) = \operatorname{tr}(I)/t = p/t$, and by [weak duality](/weak-duality/) this bounds $c^\top x^* - f^*$. When line L4 stops, the gap is at most $\varepsilon$. If the centering is not exact, the gap is $p/t + \sum_i x_i r_i$, where $r = g/t$ is the dual residual. The full proof is below.

## Complexity

**Outer iterations.** The method makes exactly $\lceil\log(p/(t_0\varepsilon))/\log\mu\rceil + 1$ centerings (or $1$ if $p/t_0 \le \varepsilon$).

**Newton steps per centering.** Assume that $F(x^0) \succ 0$, that the $F_i$ are linearly independent and that the feasible set is bounded. A centering that starts at the exact center for $t$ and ends at the center for $\mu t$ begins at most $p(\mu - 1 - \log\mu)$ above the minimum of $\phi_{\mu t}$. Since $\phi_t$ is self-concordant, Newton's method with backtracking needs at most

$$\frac{p(\mu - 1 - \log\mu)}{\gamma} + \log_2\log_2\frac{1}{\varepsilon_{nt}}, \qquad \gamma = \frac{\alpha\beta(1 - 2\alpha)^2}{20 - 8\alpha},$$

steps (Boyd and Vandenberghe, Section 11.5). With $\alpha = 1/4$ and $\beta = 1/2$, $\gamma = 1/288$, so this bound is very loose: it is 7721 for the example, where the actual count is at most 7. The first centering needs a separate bound in terms of $\phi_{t_0}(x^0) - \min\phi_{t_0}$.

**Total.** With the short-step choice $\mu = 1 + 1/\sqrt{p}$, each centering needs $O(1)$ Newton steps and there are $O(\sqrt{p}\log(p/(t_0\varepsilon)))$ centerings. With a fixed $\mu$ such as $10$, the bound is $O(p\log(p/(t_0\varepsilon)))$, but in practice the count of Newton steps per centering is almost constant, about 5 to 50.

**One Newton step.** Factoring $F(x)$ costs $O(p^3)$, the products $F^{-1}F_i$ cost $O(np^3)$, the Hessian costs $O(n^2p^2)$, and the Newton system costs $O(n^3)$. For an LP the matrices are diagonal, and the cost falls to $O(n^2 p + n^3)$. The extra space is $O(np^2 + n^2)$.

## Properties

- **Primal method with a dual certificate.** The iterates are primal points, and the dual point $F(x)^{-1}/t$ comes free at each center.
- **Feasible.** It needs a strictly feasible start, and every iterate stays strictly feasible.
- **Central, not vertex.** The limit is the analytic center of the optimal face. For $\min x_1$ over the unit square, $x_2^*(t) = 1/2$ for every $t$.
- **Generic.** The same method works for any convex problem with a self-concordant barrier: $-\sum\log(b_i - a_i^\top x)$ for an LP, $-\log(u^2 - \|v\|^2)$ for a second-order cone, $-\log\det$ for a semidefinite cone.

## Variants and improvements

- **Phase I.** To find a strictly feasible start, solve $\min s$ subject to $F(x) + sI \succeq 0$, which has the obvious strictly feasible start $s > -\lambda_{\min}(F(x))$. Stop as soon as $s < 0$.
- **Short-step path-following.** Take $\mu = 1 + c/\sqrt{\nu}$ and one Newton step per value of $t$. This is the version with the best proved bound.
- **Primal-dual methods.** The [interior-point method](/interior-point-method/) updates primal and dual variables together and does not need exact centering. It is the basis of practical solvers.
- **Inequality constraints in general form.** For $f_i(x) \le 0$ with convex $f_i$, use $\phi(x) = -\sum_i\log(-f_i(x))$, with gap $m/t$ for $m$ constraints.
- **Exterior relative.** The [penalty method](/penalty-method/) works from outside the feasible set with a penalty that grows, instead of from inside with a barrier that fades.

## When to use it

Use the barrier method when you need a high-accuracy solution of a small or medium convex problem, and you can write a self-concordant barrier for its constraints. It is easy to implement on top of a Newton solver. For large LPs and SDPs a primal-dual [interior-point method](/interior-point-method/) is faster and more robust. For very large problems where one Newton step is too expensive, use a first-order method.

## Pitfalls

- **No strictly feasible start.** The method cannot start on the boundary, and it cannot start outside. Run a phase I first.
- **Inexact dual point.** $F(x)^{-1}/t$ is dual feasible only at the exact center. Near the end of the run, $F(x)$ is nearly singular, and in double precision Newton's method cannot make the gradient small. The dual residual then grows with $t$. On some $2 \times 2$ problems the residual is about $10^{-8}$ at $t = 10^6$ and about $5 \times 10^{-5}$ at $t = 10^7$. Stop at a relative gap of about $10^{-6}$ to $10^{-8}$, and report the residual with the gap.
- **A stalled Newton loop.** With a tiny $\varepsilon_{nt}$ the test $\lambda^2/2 \le \varepsilon_{nt}$ can be out of reach in floating point. The implementation stops the centering when the step no longer changes $x$.
- **Too large $\mu$.** A large $\mu$ makes each centering start far from its center, so it needs more Newton steps. Values from $10$ to $100$ are common.
- **Equality constraints.** Eliminate them, or solve the Newton system with the KKT matrix. Do not put them in the barrier.

## Implementations

## History

Frisch proposed the logarithmic barrier for linear programs in 1955. Carroll (1961) used an inverse barrier, and Fiacco and McCormick developed the sequential unconstrained minimization technique (SUMT) for nonlinear programs in the 1960s and published their book in 1968. The method fell out of use in the 1970s because the Newton systems become ill-conditioned. Karmarkar's 1984 algorithm brought interior methods back, and Gill, Murray, Saunders, Tomlin and Wright (1986) showed that it is closely related to a barrier method. Nesterov and Nemirovski (1994) introduced self-concordant barriers and proved the $O(\sqrt{\nu}\log(\nu/\varepsilon))$ bound for all convex problems that have one.

## References
