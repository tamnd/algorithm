---
tag: N7GCD0
kind: algorithm
slug: admm
name: Alternating direction method of multipliers
aliases:
- ADMM
- alternating direction method
area: optimization/convex-optimization
level: advanced
summary: Split a problem into blocks and alternate minimization over each, updating multipliers.
solves: [quadratic-programming, linear-programming-problem]
model: real-ram
complexity:
  vars: {k: the number of iterations, m: the number of coupling constraints, n: the number of variables, s: the cost of the two subproblem solves of one iteration}
  time: {worst: O(k (s + m n))}
  space: {extra: O(m + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1975
  people: [Roland Glowinski, Americo Marrocco, Daniel Gabay, Bertrand Mercier]
  note: Glowinski and Marrocco (1975) and Gabay and Mercier (1976) introduced the method for problems from mechanics and partial differential equations. Gabay showed in 1983 that it is the Douglas-Rachford splitting applied to the dual. Boyd, Parikh, Chu, Peleato and Eckstein made it widely known in 2011.
prereqs: [augmented-lagrangian-method, dual-decomposition, proximal-operator]
see_also: [operator-splitting, proximal-point-method, proximal-gradient-method, dual-ascent, lasso-regression, basis-pursuit, compressed-sensing, quadratic-programming]
sources:
  - paper: doi:10.1561/2200000016
    title: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011
    locator: Section 3.1 (the algorithm and its scaled form), Section 3.2 (convergence), Section 3.3 (stopping criteria and the primal and dual residuals), Section 3.4.1 (varying the penalty), Appendix A (the proof with the Lyapunov function)
  - paper: doi:10.1051/m2an/197509R200411
    title: Roland Glowinski and Americo Marrocco, Sur l'approximation, par elements finis d'ordre un, et la resolution, par penalisation-dualite, d'une classe de problemes de Dirichlet non lineaires, RAIRO Analyse Numerique 9(R2), 1975
    locator: pages 41 to 76
  - paper: doi:10.1016/0898-1221(76)90003-1
    title: Daniel Gabay and Bertrand Mercier, A dual algorithm for the solution of nonlinear variational problems via finite element approximation, Computers and Mathematics with Applications 2(1), 1976
    locator: pages 17 to 40
  - paper: doi:10.1007/BF01581204
    title: Jonathan Eckstein and Dimitri P. Bertsekas, On the Douglas-Rachford splitting method and the proximal point algorithm for maximal monotone operators, Mathematical Programming 55, 1992
    locator: pages 293 to 318 (ADMM as Douglas-Rachford splitting, and convergence with inexact subproblems and relaxation)
  - paper: doi:10.1137/110836936
    title: Bingsheng He and Xiaoming Yuan, On the O(1/n) convergence rate of the Douglas-Rachford alternating direction method, SIAM Journal on Numerical Analysis 50(2), 2012
    locator: pages 700 to 709 (the ergodic O(1/k) rate)
  - paper: doi:10.1007/s10107-014-0826-5
    title: Caihua Chen, Bingsheng He, Yinyu Ye and Xiaoming Yuan, The direct extension of ADMM for multi-block convex minimization problems is not necessarily convergent, Mathematical Programming 155, 2016
    locator: pages 57 to 79
  - paper: doi:10.1007/s12532-020-00179-2
    title: Bartolomeo Stellato, Goran Banjac, Paul Goulart, Alberto Bemporad and Stephen Boyd, OSQP, an operator splitting solver for quadratic programs, Mathematical Programming Computation 12, 2020
    locator: pages 637 to 672
---

The alternating direction method of multipliers (ADMM) solves problems of the form $\min f(x) + g(z)$ subject to $Ax + Bz = c$, where $f$ and $g$ are convex and each is easy to handle alone. It is the [augmented Lagrangian method](/augmented-lagrangian-method/) with one change: instead of minimizing the augmented Lagrangian over $x$ and $z$ together, it does one pass, first over $x$ with $z$ fixed and then over $z$ with the new $x$ fixed, and then it updates the multiplier. Each step then uses only $f$ or only $g$, so a hard problem breaks into two easy ones. ADMM converges for each closed convex $f$ and $g$ whose Lagrangian has a saddle point and for each penalty $\rho > 0$, with no strong convexity. The averages of the first $K$ iterates are within $O(1/K)$ of optimal, both in objective and in constraint violation.

## In plain words

Two teams must agree on a shared plan, but each team only knows its own costs. Team one makes its best plan given the last plan of team two and a list of fines for each disagreement. Then team two does the same, using the new plan of team one. After both turns, a referee looks at how far apart the two plans are and raises the fines for the parts where they still disagree. The fines build up over the rounds, so the teams are pushed toward one plan that is best for both. No team ever needs to know the other team's costs. The method gets close to the answer quickly, but it can take many rounds to get the last few digits right.

## The problem

Minimize $f(x) + g(z)$ over vectors $x$ and $z$ subject to $Ax + Bz = c$, where $A$ and $B$ have $m$ rows, and $x$ and $z$ together have $n$ entries. The assumptions are:

- $f$ and $g$ are closed, proper and convex, and they can take the value $+\infty$, so constraints can be written as indicator functions;
- the Lagrangian $L_0 = f(x) + g(z) + y^\top(Ax + Bz - c)$ has a saddle point $(x^*, z^*, y^*)$;
- the two subproblems in lines L2 and L4 have minimizers, and there are routines to compute them.

The input is these two routines, $A$, $B$, $c$, a start $(z_0, u_0)$, a penalty $\rho > 0$ and a tolerance $\varepsilon$. The output is $(x, z)$ and a multiplier $y$.

## The algorithm

```pseudo id=main
ADMM(f, g, A, B, c, z, u, ρ, ε)
L1  repeat
L2      x ← argmin_x f(x) + (ρ/2)‖Ax + Bz − c + u‖²
L3      z_old ← z
L4      z ← argmin_z g(z) + (ρ/2)‖Ax + Bz − c + u‖²
L5      r ← Ax + Bz − c                       ▷ primal residual
L6      u ← u + r
L7      s ← ρ Aᵀ B (z − z_old)                ▷ dual residual
L8  until ‖r‖ ≤ ε and ‖s‖ ≤ ε
L9  return x, z, ρu
```

This is the scaled form: $u = y/\rho$ is the multiplier divided by the penalty, which makes lines L2 and L4 plain least squares terms. After line L6, $z$ minimizes the Lagrangian $L_0(x, \cdot, y)$ exactly, and $x$ minimizes $L_0(\cdot, z, y)$ up to the error $s$. So $r$ measures primal feasibility and $s$ measures dual feasibility, and together they bound the duality gap.

A common case is the split $x - z = 0$, with $A = I$, $B = -I$ and $c = 0$. Then line L4 is $z = \operatorname{prox}_{g/\rho}(x + u)$, a [proximal map](/proximal-operator/). For example, for a convex quadratic $f(x) = \tfrac12 x^\top Px + q^\top x$ and $g$ the indicator of a box, line L2 solves $(P + \rho I)x = -q + \rho(z - u)$, and line L4 clips $x + u$ to the box. For a standard form linear program $\min c^\top x$, $Ax = b$, $x \ge 0$, put $c^\top x$ and the equality constraints in $f$ and $x \ge 0$ in $g$. Then line L2 solves one fixed linear system and line L4 sets the negative entries of $x + u$ to zero.

## Example

Minimize $\tfrac12(x - 3)^2$ subject to $0 \le x \le 1$. Split it as $f(x) = \tfrac12(x - 3)^2$ and $g(z) = 0$ on $[0, 1]$ and $+\infty$ elsewhere, with $x - z = 0$. The answer is $x^* = z^* = 1$, with $p^* = 2$ and $y^* = -(x^* - 3) = 2$. Take $\rho = 1$, $z_0 = 1$ and $u_0 = 0$. Line L2 is $x = (3 + z - u)/2$, and line L4 is $z = \min(\max(x + u, 0), 1)$. In exact arithmetic:

| $k$ | $x_k$ | $z_k$ | $u_k$ | $r_k = x_k - z_k$ |
|---|---|---|---|---|
| 1 | 2 | 1 | 1 | 1 |
| 2 | 3/2 | 1 | 3/2 | 1/2 |
| 3 | 5/4 | 1 | 7/4 | 1/4 |
| 4 | 9/8 | 1 | 15/8 | 1/8 |
| $k$ | $1 + 2^{1-k}$ | 1 | $2 - 2^{1-k}$ | $2^{1-k}$ |

The point $z_k$ is feasible from the first step, and $x_k$ is not, because $x$ sees the box only through the penalty. The multiplier $y_k = \rho u_k$ rises to $y^* = 2$, which is the slope of $f$ at the bound, and the residual halves at each step.

## Correctness

The proof has one key inequality. The two steps are exact minimizations, so their optimality conditions give a subgradient of $f$ at $x_{k+1}$ and a subgradient of $g$ at $z_{k+1}$. Put these into the subgradient inequality against any feasible point $(x, z)$ and any multiplier $\lambda$, and rewrite the cross terms with the identity $2(a - b)^\top(b - e) = \|a - e\|^2 - \|a - b\|^2 - \|b - e\|^2$. The result is a bound on the Lagrangian gap of step $k + 1$ by a drop in $\tfrac{1}{2\rho}\|\lambda - y\|^2 + \tfrac\rho2\|B(z - z^*)\|^2$, which telescopes. Averaging gives the ergodic rate. With $\lambda = y^*$ the same inequality shows that $V_k = \tfrac1\rho\|y_k - y^*\|^2 + \rho\|B(z_k - z^*)\|^2$ falls by at least $\rho(\|r_{k+1}\|^2 + \|B(z_{k+1} - z_k)\|^2)$, so the residuals go to zero. The full proof is below.

## Complexity

**Iterations.** Under the assumptions of the problem statement, for each $\rho > 0$ and each $K \ge 1$, the averages $\bar x_K$ and $\bar z_K$ of the first $K$ iterates satisfy

$$-\|y^*\|\,\|\bar r_K\| \le f(\bar x_K) + g(\bar z_K) - p^* \le \frac{1}{K}\Big(\frac{\|y_0\|^2}{2\rho} + \frac\rho2\|B(z_0 - z^*)\|^2\Big),$$

$$\|A\bar x_K + B\bar z_K - c\| \le \frac{1}{K}\Big(\frac{(\|y_0 - y^*\| + 1)^2}{2\rho} + \frac\rho2\|B(z_0 - z^*)\|^2\Big).$$

So $O(1/\varepsilon)$ iterations give an $\varepsilon$-accurate average. For the last iterate, $V_k$ does not increase and $\min_{j \le K+1}\|r_j\|^2 \le V_0/(\rho K)$. Under extra conditions, for example strong convexity and a Lipschitz gradient of one term together with rank conditions on $A$ and $B$, the rate is linear (Deng and Yin, 2016). In practice ADMM reaches modest accuracy in tens of iterations and then slows down.

**One iteration.** One $x$-minimization, one $z$-minimization, and $O(mn)$ for the residuals and the update. When line L2 is a linear system with a fixed matrix, such as $P + \rho I$ or $D^\top D + \rho I$, it is factored once and each later solve costs $O(n^2)$. The extra space is $O(m + n)$ plus that factorization.

## Properties

- **Robust.** It converges for each $\rho > 0$, with no strong convexity and no step-size rule. The value of $\rho$ changes only the speed.
- **Splits the work.** Each step uses only one of $f$ and $g$. With $g$ separable, line L4 splits into independent problems.
- **Primal and dual residuals.** $r$ and $s$ are cheap to compute and give a stopping test.
- **Order matters.** Swapping the roles of $x$ and $z$ gives a different method, with a different iterate sequence but the same guarantees.
- **Not more than two blocks.** The direct extension to three blocks $x$, $z$, $w$ can diverge, even for convex problems (Chen, He, Ye and Yuan, 2016).

## Variants and improvements

- **Over-relaxation.** Replace $Ax$ by $\alpha Ax - (1 - \alpha)(Bz - c)$ in lines L4 to L6, with $\alpha \in (1.5, 1.8)$ a common choice, to speed up convergence (Eckstein and Bertsekas, 1992).
- **Varying penalty.** Increase $\rho$ when $\|r\|$ is much larger than $\|s\|$ and decrease it in the other case, and rescale $u$ to keep $y = \rho u$.
- **Linearized and inexact ADMM.** Replace the $x$-step by one proximal gradient step on it, so that each step is a matrix-vector product and a proximal map.
- **Consensus and sharing.** For $\min\sum_i f_i(x)$, give each term its own copy $x_i$ and add $x_i - z = 0$. The $x$-steps then run in parallel, and the $z$-step is an average.
- **[Douglas-Rachford splitting](/operator-splitting/).** ADMM is Douglas-Rachford splitting applied to the dual problem, and it is also a [proximal point method](/proximal-point-method/) in a suitable metric.
- **Solvers built on ADMM.** OSQP solves [quadratic programs](/quadratic-programming/) with ADMM and one factored linear system, and SCS uses a related splitting for cone programs.

## When to use it

Use ADMM when the problem is a sum of two convex terms, each with a simple solver or [proximal map](/proximal-operator/), and medium accuracy is enough. Examples are the [lasso](/lasso-regression/), with $f(x) = \tfrac12\|Dx - b\|^2$ and $g(z) = \lambda\|z\|_1$, [basis pursuit](/basis-pursuit/), total variation denoising, and [quadratic programs](/quadratic-programming/) with box or cone constraints. It is also good for distributed problems where data stay on separate machines. For high accuracy on small or medium problems, an [interior-point method](/interior-point-method/) is usually faster. For problems with one smooth term and one simple term, the [proximal gradient method](/proximal-gradient-method/) is simpler.

## Pitfalls

- **A bad $\rho$.** The method converges for each $\rho$, but a $\rho$ that is too large or too small by a few orders of magnitude can make it very slow. Scale the problem, and adapt $\rho$.
- **Stopping on the primal residual only.** $r$ can be small while $s$ is large, and then $x$ is far from optimal. Check both.
- **Infeasible or unbounded problems.** Without a saddle point, the iterates diverge, and the residuals or the multipliers grow. The differences of successive iterates then tend to a certificate of infeasibility, and solvers such as OSQP test them.
- **Three or more blocks.** Updating three blocks in turn is not guaranteed to converge. Group the blocks into two, or use a convergent variant.
- **Expecting the last digits.** The rate is $O(1/K)$ at best in general. Do not plan on $10^{-8}$ accuracy.

## Implementations

## History

Glowinski and Marrocco (1975) and Gabay and Mercier (1976) introduced ADMM to solve nonlinear problems from mechanics and partial differential equations, as a cheaper form of the method of multipliers of Hestenes and Powell. Gabay (1983) showed that it is Douglas-Rachford splitting applied to the dual, and Eckstein and Bertsekas (1992) showed that this splitting is a proximal point method, which gave a convergence theory with inexact steps and relaxation. Boyd, Parikh, Chu, Peleato and Eckstein (2011) showed how many problems in statistics and machine learning fit the method, and it then became widely used. He and Yuan (2012) proved the ergodic $O(1/k)$ rate, and Chen, He, Ye and Yuan (2016) showed that the direct extension to three blocks can diverge.

## References
