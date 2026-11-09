---
tag: MYGDGH
kind: algorithm
slug: interior-point-method
name: Interior-point method
aliases:
- barrier method
- primal-dual interior point
- primal-dual interior-point method
- path-following method
- short-step path-following method
area: optimization/convex-optimization
level: advanced
summary: Follow the central path through the interior of the feasible region to the optimum, with one Newton step per iteration and O(n^(1/2) log(1/ε)) iterations for LP.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints, r: the ratio of the starting duality gap to the target gap}
  time: {worst: O(n^(1/2) log(r) (m^2 n + m^3))}
  space: {extra: O(m^2 + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1984
  people: [Narendra Karmarkar, James Renegar, Renato Monteiro, Ilan Adler, Masakazu Kojima, Yurii Nesterov, Arkadi Nemirovski]
  note: Karmarkar's 1984 projective method started the field. Renegar (1988) gave the first path-following method with O(n^(1/2) L) iterations, and Kojima, Mizuno and Yoshise and Monteiro and Adler (1989) gave the primal-dual version. Nesterov and Nemirovski (1994) extended the theory to all convex problems with a self-concordant barrier.
prereqs: [linear-programming-problem, lp-duality, central-path, newton-method-for-systems]
see_also: [barrier-method, self-concordant-function, karmarkar-algorithm, affine-scaling-method, simplex-method, ellipsoid-method, semidefinite-programming, kkt-conditions]
sources:
  - book: isbn:9780898713824
    title: Stephen J. Wright, Primal-Dual Interior-Point Methods, SIAM, 1997
    locator: Chapter 1 (the primal-dual framework and the central path), Chapter 5 (path-following algorithms, the short-step method with theta = 0.4 and sigma = 1 - 0.4/n^(1/2), and its O(n^(1/2) log(1/ε)) bound), Chapter 10 (practical issues)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 14, Interior-point methods for linear programming (primal-dual methods, the central path, a practical primal-dual algorithm with Mehrotra's predictor-corrector, other primal-dual algorithms)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 11, Interior-point methods (Section 11.5 complexity analysis via self-concordance, Section 11.7 primal-dual interior-point methods)
  - paper: doi:10.1007/BF01587075
    title: Renato D. C. Monteiro and Ilan Adler, Interior path following primal-dual algorithms. Part I, Linear programming, Mathematical Programming 44, 1989
    locator: pages 27 to 41
  - paper: doi:10.1007/BF01580724
    title: James Renegar, A polynomial-time algorithm, based on Newton's method, for linear programming, Mathematical Programming 40, 1988
    locator: pages 59 to 93
  - paper: doi:10.1137/0802028
    title: Sanjay Mehrotra, On the implementation of a primal-dual interior point method, SIAM Journal on Optimization 2(4), 1992
    locator: pages 575 to 601 (the predictor-corrector method)
  - book: isbn:9780898713190
    title: Yurii Nesterov and Arkadii Nemirovskii, Interior-Point Polynomial Algorithms in Convex Programming, SIAM, 1994
    locator: Chapters 2 and 3 (self-concordant barriers and path-following methods for general convex problems)
---

An interior-point method solves a [linear program](/linear-programming-problem/) or another convex problem by moving through the strict interior of the feasible set, close to the [central path](/central-path/), toward an optimal point. Each step is one [Newton step](/newton-method-for-systems/) on the optimality conditions with the complementarity products $x_i s_i$ pushed toward a target $\sigma\mu$ that shrinks at each step. The short-step primal-dual method of this page keeps its iterates in a fixed neighborhood of the path and cuts the [duality gap](/lp-duality/) by the factor $1 - 0.4/\sqrt{n}$ at each step, so it reaches gap $\varepsilon$ in $O(\sqrt{n}\log(n\mu_0/\varepsilon))$ steps. Methods of this family solve large linear, [second-order cone](/second-order-cone-programming/) and [semidefinite](/semidefinite-programming/) programs in practice, and they give polynomial-time bounds in theory.

## In plain words

The simplex method walks along the edges of the feasible region, from corner to corner. An interior-point method cuts through the inside. It keeps every variable strictly positive and moves along a smooth curve, the central path, that ends at an optimal point.

The method works on the primal program and the dual program together. The difference between their objective values, the duality gap, tells how far the current point is from optimal. At each step the method asks for a smaller gap, by a fixed factor, and makes one Newton step toward the point of the curve with that gap. If the steps are small enough, the points never leave a thin tube around the curve, so one Newton step is always enough. The number of steps grows like the square root of the number of variables, times the number of digits of accuracy.

## The problem

We use the notation of the optimization pages: $n$ variables, $m$ equality constraints, and an LP in [standard form](/lp-standard-form/) with data $A \in \mathbb{R}^{m \times n}$ of full row rank, $b \in \mathbb{R}^m$, $c \in \mathbb{R}^n$:

$$\text{(P)}\ \ \min\ c^\top x \ \text{ s.t. } Ax = b,\ x \ge 0, \qquad \text{(D)}\ \ \max\ b^\top y \ \text{ s.t. } A^\top y + s = c,\ s \ge 0.$$

For a primal feasible $x$ and a dual feasible $(y, s)$ the duality gap is $c^\top x - b^\top y = x^\top s \ge 0$, and both points are optimal if and only if the gap is $0$, that is, if and only if $x_i s_i = 0$ for each $i$ ([complementary slackness](/complementary-slackness/)). Write $X = \operatorname{diag}(x)$, $S = \operatorname{diag}(s)$, $e$ for the vector of ones and $\mu = x^\top s / n$. The central path is the set of points with $x > 0$, $s > 0$, both feasible, and $XSe = \mu e$. The method works in the neighborhood

$$\mathcal{N}_2(\theta) = \{(x, y, s) \text{ strictly feasible} : \|XSe - \mu e\|_2 \le \theta\mu\}, \qquad \theta = 0.4.$$

The input is $A$ and a start $(x^0, y^0, s^0) \in \mathcal{N}_2(0.4)$. The vectors $b = Ax^0$ and $c = A^\top y^0 + s^0$ are fixed by the start. The output is a primal-dual feasible pair with gap at most $\varepsilon$. So the primal objective is within $\varepsilon$ of $f^*$, and so is the dual objective.

## The algorithm

```pseudo id=main
SHORT-STEP-PATH-FOLLOWING(A, x, y, s, ε)     ▷ (x, y, s) ∈ N2(0.4)
L1  σ ← 1 − 0.4 / √n
L2  loop
L3      μ ← xᵀs / n
L4      if n·μ ≤ ε then return (x, y, s)       ▷ gap = cᵀx − bᵀy = n·μ
L5      r ← σμe − XSe                           ▷ the wanted change of the products x_i s_i
L6      solve (A D Aᵀ) Δy = −A S⁻¹ r, with D = X S⁻¹
L7      Δs ← −Aᵀ Δy
L8      Δx ← S⁻¹ (r − X Δs)
L9      (x, y, s) ← (x + Δx, y + Δy, s + Δs)    ▷ full step, no line search
```

Lines L6 to L8 solve the Newton system of the conditions $Ax = b$, $A^\top y + s = c$ and $XSe = \sigma\mu e$:

$$A\,\Delta x = 0, \qquad A^\top \Delta y + \Delta s = 0, \qquad S\,\Delta x + X\,\Delta s = \sigma\mu e - XSe.$$

The first two equations keep the iterate feasible. The third is the linear part of $(x_i + \Delta x_i)(s_i + \Delta s_i) = \sigma\mu$, with the product $\Delta x_i \Delta s_i$ dropped. Line L6 eliminates $\Delta x$ and $\Delta s$ and leaves the normal equations, an $m \times m$ positive definite system. The value $\sigma = 1 - 0.4/\sqrt{n}$ is the largest drop of $\mu$ for which the proof below keeps the full step inside $\mathcal{N}_2(0.4)$.

## Example

Take $n = 3$, $m = 1$, $A = [1\ 1\ 1]$, and the start $x^0 = (1, \tfrac12, \tfrac13)$, $y^0 = 0$, $s^0 = (1, 2, 3)$. Then $x^0_i s^0_i = 1$ for each $i$, so the start is on the central path with $\mu_0 = 1$, and it fixes $b = 11/6$ and $c = (1, 2, 3)$. The program is $\min x_1 + 2x_2 + 3x_3$ subject to $x_1 + x_2 + x_3 = 11/6$, $x \ge 0$. Its optimum is $x^* = (11/6, 0, 0)$ with $f^* = 11/6$, and the dual optimum is $y^* = 1$, $s^* = (0, 1, 2)$. Here $\sigma = 1 - 0.4/\sqrt{3} \approx 0.76906$. With $\varepsilon = 10^{-6}$:

| $k$ | gap $n\mu_k$ | $x^k$ | $s^k$ |
|---|---|---|---|
| 0 | 3 | (1.0000, 0.5000, 0.3333) | (1.0000, 2.0000, 3.0000) |
| 1 | 2.30718 | (1.0801, 0.4623, 0.2909) | (0.6889, 1.6889, 2.6889) |
| 2 | 1.77436 | (1.1839, 0.4070, 0.2424) | (0.4814, 1.4814, 2.4814) |
| 3 | 1.36459 | (1.2906, 0.3457, 0.1970) | (0.3408, 1.3408, 2.3408) |
| 10 | 0.217132 | (1.7281, 0.0697, 0.0355) | (0.0416, 1.0416, 2.0416) |
| 20 | 0.0157154 | (1.8255, 0.0052, 0.0026) | (0.0029, 1.0029, 2.0029) |
| 57 | 9.48 × 10⁻⁷ | (1.8333, 0.0000, 0.0000) | (0.0000, 1.0000, 2.0000) |

The gap is exactly $3 \cdot 0.76906^k$ at each step. The method stops after $57 = \lceil \ln(3 \cdot 10^6) / (-\ln 0.76906) \rceil$ steps. The cruder bound $\lceil (\sqrt{3}/0.4) \ln(3 \cdot 10^6) \rceil$ is $65$. The variables $x_2$ and $x_3$, which are $0$ at the optimum, go to $0$ at the same rate as the gap, and so do their partners $s_1$ in the dual.

## Correctness

The method keeps this invariant at line L3: the iterate is strictly feasible, it is in $\mathcal{N}_2(0.4)$, and $\mu_k = \sigma^k \mu_0$. The key facts are that $\Delta x^\top \Delta s = 0$, because $\Delta x$ is in the null space of $A$ and $\Delta s$ is in the range of $A^\top$, and that the new products are $x_i^+ s_i^+ = \sigma\mu + \Delta x_i \Delta s_i$. A lemma on products of two vectors with a nonnegative inner product bounds $\|\Delta X \Delta S e\|$ by $0.1886\,\mu$, and this is less than $\theta\mu^+ \ge 0.24\mu$. The same bound shows that no $x_i$ or $s_i$ can reach $0$ along the step. When the loop stops, the gap is at most $\varepsilon$, so by [weak duality](/weak-duality/) $c^\top x - f^* \le \varepsilon$. The full proof is below.

## Complexity

**Iterations.** Assume that $A$ has full row rank and that the start is in $\mathcal{N}_2(0.4)$. Then the method stops after at most

$$K = \left\lceil \frac{\ln(n\mu_0/\varepsilon)}{-\ln(1 - 0.4/\sqrt{n})} \right\rceil \le \left\lceil 2.5\sqrt{n}\, \ln\frac{n\mu_0}{\varepsilon} \right\rceil$$

iterations. This is a worst-case bound, proved, and the rate is linear (geometric) with ratio $1 - 0.4/\sqrt{n}$. The short-step method takes exactly this number of steps on each input: it never takes a longer step.

**One iteration.** Forming $A D A^\top$ costs $O(m^2 n)$ arithmetic operations for dense data, its Cholesky factorization costs $O(m^3)$, and the rest is $O(mn)$. For sparse data the cost is that of one sparse Cholesky factorization, and it depends on the fill-in. The extra space is $O(m^2 + n)$.

**Bit complexity.** For an LP with integer data of bit length $L$, a start of the form above can be built (for example by the homogeneous self-dual embedding of Ye, Todd and Mizuno, 1994), and a gap of $2^{-O(L)}$ can be rounded to an exact optimal vertex. This gives $O(\sqrt{n}\,L)$ iterations, as in Renegar (1988), and $O(n^{3.5} L)$ arithmetic operations with dense linear algebra. It is polynomial in $L$, not strongly polynomial: no strongly polynomial algorithm for LP is known.

**General convex problems.** For a problem in conic form with a $\nu$-[self-concordant](/self-concordant-function/) barrier, a short-step path-following method needs $O(\sqrt{\nu}\log(\nu/(t_0\varepsilon)))$ Newton steps (Nesterov and Nemirovski, 1994). The barrier $-\sum \ln x_i$ of the nonnegative orthant has $\nu = n$, which gives the bound above. For semidefinite programs with $p \times p$ matrices, $\nu = p$. See the [barrier method](/barrier-method/) for the primal version of this bound.

## Properties

- **Primal-dual.** Each iterate gives a primal point, a dual point and a certificate of accuracy, the gap $x^\top s$.
- **Feasible.** Each iterate satisfies $Ax = b$ and $A^\top y + s = c$ exactly in exact arithmetic. Infeasible-start variants drop this.
- **Not a vertex method.** The iterates stay strictly inside the feasible set, and they do not go to a vertex when the optimal face is larger than a point. If the example had $c = (1, 1, 1)$, each feasible point would be optimal, and the whole central path would be the single point $(11/18, 11/18, 11/18)$, which is not a vertex. A crossover step is needed to get a basic solution.
- **Deterministic and exact in its count.** The number of steps depends only on $n$, $\mu_0$ and $\varepsilon$.

## Variants and improvements

- **Long-step methods.** Use the wider neighborhood $\mathcal{N}_{-\infty}(\gamma) = \{x_i s_i \ge \gamma\mu\}$, a much smaller $\sigma$, and a line search that keeps the iterate in the neighborhood. The proved bound is worse, $O(n\log(1/\varepsilon))$ iterations, but in practice they are much faster.
- **Mehrotra's predictor-corrector.** First solve with $\sigma = 0$ (the affine-scaling direction, compare the [affine scaling method](/affine-scaling-method/)), choose $\sigma$ from how far that step gets, then solve again with the same matrix and a second-order correction. Most LP and conic solvers use this. It has no polynomial bound in its basic form.
- **Infeasible-start methods.** Start from any $x > 0$, $s > 0$ and reduce the residuals $Ax - b$ and $A^\top y + s - c$ together with $\mu$.
- **The homogeneous self-dual embedding.** Embed the LP in a larger LP with a known central start. It needs no phase one and it detects infeasibility and unboundedness.
- **Conic programs.** The same scheme works for [second-order cone](/second-order-cone-programming/) and [semidefinite](/semidefinite-programming/) programs with the Nesterov-Todd scaling of the products.
- **Potential reduction.** [Karmarkar's algorithm](/karmarkar-algorithm/) reduces a potential function by a constant at each step and needs $O(nL)$ steps.

## When to use it

Use an interior-point method for a large sparse LP, or for any SOCP or SDP of moderate size, when you want a high-accuracy answer in a predictable number of steps. Practical variants usually need a few tens of steps, and this number grows only slowly with the size. The [simplex method](/simplex-method/) is better when you need a vertex solution, when you solve many related LPs and can warm start from the last basis, and on small LPs. First-order methods such as [ADMM](/admm/) are better when one Newton system is too large to factor. The [ellipsoid method](/ellipsoid-method/) is a theoretical tool, not a practical solver.

## Pitfalls

- **A full step outside the neighborhood.** Line L9 takes the full step with no test. This is safe only because the start is in $\mathcal{N}_2(0.4)$ and $\sigma$ is the value of line L1. With a smaller $\sigma$, or a start far from the path, the full step can make some $x_i$ negative. Long-step and practical methods must cut the step to a fraction, for example $0.99$, of the largest step that keeps $x > 0$ and $s > 0$.
- **Stopping on the wrong measure.** Stop on the gap $n\mu$ of line L4, or on a relative gap, not on a small change of $c^\top x$. The gap is a certificate, and the change of the objective is not.
- **Ill-conditioned normal equations.** Near the end, $D_{jj} = x_j / s_j$ goes to $0$ or to infinity, so $A D A^\top$ in line L6 becomes badly conditioned. On a degenerate LP, where fewer than $m$ variables are positive at the optimum, a plain Gaussian elimination in double precision can meet an exact zero pivot when the gap is near $10^{-8}$. Solvers use a modified Cholesky factorization that handles tiny pivots, and they stop at a relative gap of about $10^{-8}$.
- **Rank-deficient $A$.** If $A$ does not have full row rank, $A D A^\top$ is singular. Remove the dependent rows in a presolve step.
- **Expecting a vertex.** A user who needs a basic solution, for example for sensitivity analysis, must add crossover.

## Implementations

## History

Frisch proposed the logarithmic barrier in 1955, and Fiacco and McCormick developed barrier methods for nonlinear programs in the 1960s. Interest in these methods for LP started in 1984, when Karmarkar published a projective method with a polynomial bound and good reported speed. Renegar (1988) gave a path-following method based on Newton's method with $O(\sqrt{n}L)$ iterations. In 1989 Kojima, Mizuno and Yoshise, and Monteiro and Adler, gave the primal-dual path-following methods of this page. Mehrotra's predictor-corrector method (1992) became the basis of most software. Nesterov and Nemirovski (1994) showed that the same bounds hold for every convex problem with a self-concordant barrier, which led to practical solvers for second-order cone and semidefinite programs.

## References
