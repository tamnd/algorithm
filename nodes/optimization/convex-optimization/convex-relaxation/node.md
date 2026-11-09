---
tag: DNEBN9
kind: technique
slug: convex-relaxation
name: Convex relaxation
aliases:
- relaxation to a convex problem
- SDP relaxation
- Shor relaxation
area: optimization/convex-optimization
level: advanced
summary: Replace a hard nonconvex problem with a convex one that bounds or approximates it.
prereqs: [convex-optimization-problem, semidefinite-programming, lp-relaxation]
see_also: [lp-relaxation, integrality-gap, maximum-cut, lovasz-theta-function, basis-pursuit, convex-envelope, lagrangian-relaxation, lift-and-project]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 5 (Lagrange duality, with the two-way partitioning problem and its semidefinite bound)
  - paper: doi:10.1145/227683.227684
    title: Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42(6), 1995
    locator: pages 1115 to 1145
  - paper: doi:10.1109/TIT.1979.1055985
    title: László Lovász, On the Shannon capacity of a graph, IEEE Transactions on Information Theory 25(1), 1979
    locator: pages 1 to 7
  - paper: doi:10.1007/BF01580665
    title: Garth P. McCormick, Computability of global solutions to factorable nonconvex programs, Part I, Convex underestimating problems, Mathematical Programming 10, 1976
    locator: pages 147 to 175
  - paper: doi:10.1007/bfb0120690
    title: Arthur M. Geoffrion, Lagrangean relaxation for integer programming, Mathematical Programming Study 2, 1974
    locator: pages 82 to 114
  - paper: doi:10.1109/TIT.2005.858979
    title: Emmanuel J. Candès and Terence Tao, Decoding by linear programming, IEEE Transactions on Information Theory 51(12), 2005
    locator: pages 4203 to 4215
  - paper: doi:10.1137/070697835
    title: Benjamin Recht, Maryam Fazel and Pablo A. Parrilo, Guaranteed minimum-rank solutions of linear matrix equations via nuclear norm minimization, SIAM Review 52(3), 2010
    locator: pages 471 to 501
  - paper: doi:10.1137/S1052623400366802
    title: Jean B. Lasserre, Global optimization with polynomials and the problem of moments, SIAM Journal on Optimization 11(3), 2001
    locator: pages 796 to 817
---

A convex relaxation replaces a hard problem, $\min f(x)$ over a set $S$, by a [convex problem](/convex-optimization-problem/) over a larger set with an objective that is not larger than $f$ on $S$. The convex problem can be solved to global optimality in polynomial time, and its optimal value is a lower bound on the original one. If the relaxed solution happens to lie in $S$ with the same value, it is optimal for the original problem. If not, a rounding step turns it into a feasible point, and the bound tells how far that point can be from the optimum. The common relaxations drop integrality ([LP relaxation](/lp-relaxation/)), replace a product $xx^\top$ by a [positive semidefinite](/positive-definite-matrix/) matrix ([semidefinite relaxation](/semidefinite-programming/)), or replace a function by its [convex envelope](/convex-envelope/), as $\|x\|_1$ does for the number of nonzero entries.

## In plain words

Some problems are hard because the choices are yes or no, or because the cost surface has many valleys. A relaxation makes the rules looser: it allows halfway choices, or it smooths the surface into one bowl. The looser problem is easy, and its best value can only be as good as or better than the best value of the real problem, so it gives a limit that no real answer can pass. Sometimes the easy answer is also a real answer, and then the work is done. Other times the easy answer is a blend, and you turn it into a real answer by rounding. The limit then tells you how good the rounded answer is.

## When it applies

- The problem is $\min f(x)$ over $x \in S$, where $S$ or $f$ is not convex: integer variables, $x_i \in \{-1, 1\}$, products of variables, rank or cardinality constraints.
- A global optimum, or at least a bound on it, is needed, so a local method is not enough.
- There is a convex set $\hat S \supseteq S$ and a convex $\hat f$ with $\hat f \le f$ on $S$ that are small enough to solve: a linear program, a [second-order cone program](/second-order-cone-programming/) or a semidefinite program.
- You need a lower bound for branch and bound, a certificate that a candidate is optimal, or a starting point for rounding with a provable ratio.

## The template

```pseudo id=main
CONVEX-RELAXATION(f, S)
L1  choose a convex set Ŝ ⊇ S and a convex f̂ with f̂(x) ≤ f(x) for x ∈ S   ▷ hole: the relaxation
L2  x̂ ← argmin over x ∈ Ŝ of f̂(x);  lower ← f̂(x̂)                         ▷ a convex problem
L3  if x̂ ∈ S and f(x̂) = lower then return x̂                               ▷ the relaxation is tight
L4  x̃ ← ROUND(x̂)                                                          ▷ hole: a map into S
L5  return x̃ and the error bound f(x̃) − lower
```

**The holes.** For line L1, typical choices are: replace $x_i \in \{0, 1\}$ by $0 \le x_i \le 1$; lift $x \in \{-1, 1\}^n$ to a matrix $X = xx^\top$ and keep only the convex facts $X \succeq 0$ and $X_{ii} = 1$ (the Shor relaxation); replace a nonconvex term by its convex envelope on a box, such as the McCormick inequalities for a product $w = xy$; or take the [Lagrangian dual](/lagrangian-duality/), which is always convex. For line L4, typical choices are thresholds, [randomized rounding](/randomized-rounding/), the random hyperplane, or the best rank-one part of $X$.

**The analysis.** Let $p^* = \inf_{x \in S} f(x)$ and $\hat p = \inf_{x \in \hat S} \hat f(x)$.

1. *Lower bound.* Each $x \in S$ is in $\hat S$ with $\hat f(x) \le f(x)$, so $\hat p \le p^*$.
2. *Tightness.* If $\hat x \in S$ and $f(\hat x) = \hat p$, then $f(\hat x) \le p^*$, so $\hat x$ is optimal. More generally, every feasible $\tilde x$ has $f(\tilde x) - p^* \le f(\tilde x) - \hat p$, a bound that the method computes.
3. *Approximation ratio.* For a minimization with $f \ge 0$, if the rounding gives $\mathbb{E}f(\tilde x) \le \rho\,\hat p$, then $\mathbb{E}f(\tilde x) \le \rho\,p^*$, so the method is a $\rho$-approximation. The ratio $p^*/\hat p$ over all inputs, the [integrality gap](/integrality-gap/), is the best $\rho$ that this argument can prove.
4. *The best relaxation is exact but hard.* Let $S$ be compact, $f$ continuous, $\hat S = \operatorname{conv}(S)$ and $\hat f$ the convex envelope of $f$ on $S$, the largest convex function below $f$ on $S$. The constant function $p^*$ is convex and below $f$ on $S$, so $\hat f \ge p^*$, and $\hat p \ge p^*$. With fact 1, $\hat p = p^*$. So each relaxation is an outer approximation of the convex hull, and the work is to find one that is both tight and small.
5. *Relaxation and duality.* The Lagrangian dual of a problem is a convex relaxation. For an integer program with the rows $Ax \le b$ relaxed, the best Lagrangian bound equals the minimum of $c^\top x$ subject to $Ax \le b$ over the convex hull of the integer points that satisfy the other rows (Geoffrion, 1974). For $\min x^\top Qx$ over $\{-1, 1\}^n$, the dual of the Shor relaxation is $\max \sum_iz_i$ subject to $Q - \operatorname{Diag}(z) \succeq 0$, which is the Lagrangian dual of the constraints $x_i^2 = 1$.

### A worked example

Find a [maximum cut](/maximum-cut/) of the triangle $K_3$: split the three nodes into two sides to cut the most edges. With $x_i \in \{-1, 1\}$ for the side of node $i$, the problem is

$$\max\ \sum_{ij \in E}\frac{1 - x_ix_j}{2} \quad\text{over } x \in \{-1, 1\}^3.$$

Two nodes are always on the same side, so the answer is $p^* = 2$. The Shor relaxation replaces $x_ix_j$ by $X_{ij}$ and asks for $X \succeq 0$ with $X_{ii} = 1$. It is a maximization, so it gives an upper bound:

- *The bound $\tfrac94$.* The matrix with $X_{ii} = 1$ and $X_{ij} = -\tfrac12$ is $\tfrac32I - \tfrac12J$, with the eigenvalues $0, \tfrac32, \tfrac32$, so it is feasible. Its value is $3 \cdot \tfrac{1 + 1/2}{2} = \tfrac94$. These are three unit vectors in a plane, at $120°$ to each other.
- *The certificate.* The dual is $\min\sum_iz_i$ subject to $\operatorname{Diag}(z) - \tfrac14L \succeq 0$, where $L = 3I - J$ is the Laplacian of $K_3$. The point $z = (\tfrac34, \tfrac34, \tfrac34)$ gives $\operatorname{Diag}(z) - \tfrac14L = \tfrac14J \succeq 0$, with value $\tfrac94$. So $\tfrac94$ is the exact optimal value of the relaxation.
- *The rounding.* Cut the three vectors with a random line through the origin. An edge is cut with the probability $\arccos(-\tfrac12)/\pi = \tfrac23$, so the expected cut is $3 \cdot \tfrac23 = 2 = p^*$, and each outcome is a cut with $2$ edges.

The simplest bound, each term at most $1$, gives $3$. The relaxation gives $\tfrac94$, and $p^*/\hat p = \tfrac89$. Goemans and Williamson (1995) proved that the random hyperplane gives at least $0.878$ times the SDP bound on every graph.

## Classic examples

- **[LP relaxation](/lp-relaxation/) of integer programs.** Replace $x \in \{0, 1\}^n$ by $[0, 1]^n$. For [vertex cover](/vertex-cover/), rounding every $x_i \ge \tfrac12$ up gives a [2-approximation](/lp-rounding-vertex-cover/). When the constraint matrix is [totally unimodular](/total-unimodularity/), the relaxation is exact.
- **The Goemans-Williamson SDP relaxation of [max-cut](/maximum-cut/).** The worked example above, with the ratio $0.878$, which is the best possible if the [unique games conjecture](/unique-games-conjecture/) holds.
- **The [Lovász theta function](/lovasz-theta-function/).** An SDP relaxation of the independence number. It lies between the independence number and the clique cover number, so it computes both exactly for perfect graphs.
- **$\ell_1$ for sparsity.** On the box $\|x\|_\infty \le 1$, the convex envelope of the number of nonzero entries is $\|x\|_1$. [Basis pursuit](/basis-pursuit/) and the [lasso](/lasso-regression/) use it, and in [compressed sensing](/compressed-sensing/) the relaxation is exact under the restricted isometry property (Candès and Tao, 2005).
- **The nuclear norm for rank.** The sum of the singular values is the convex envelope of the rank on the unit ball of the spectral norm. It gives exact low-rank matrix recovery under similar conditions (Recht, Fazel and Parrilo, 2010), and the PhaseLift method for [phase retrieval](/phase-retrieval/).
- **McCormick envelopes.** For $w = xy$ with $x \in [x_L, x_U]$ and $y \in [y_L, y_U]$, the four inequalities such as $w \ge x_Ly + xy_L - x_Ly_L$ describe the convex hull of the graph of $xy$ on the box. Global solvers for factorable nonconvex programs use them in spatial branch and bound (McCormick, 1976).
- **[Lagrangian relaxation](/lagrangian-relaxation/).** The dual bound of fact 5, computed by subgradient or [bundle](/bundle-method/) methods.

## Variations

- **Hierarchies.** Add more lifted variables to get a sequence of tighter relaxations: Sherali and Adams for LPs, the [lift-and-project](/lift-and-project/) method of Lovász and Schrijver, and the moment or sum-of-squares hierarchy of Lasserre (2001) for polynomial problems. Level $n$ is exact for $n$ binary variables, but the size grows fast.
- **Weaker but cheaper relaxations.** An SDP relaxation can be relaxed again to an SOCP or an LP, for example by requiring only that each $2 \times 2$ principal minor of $X$ is positive semidefinite.
- **Tightening with cuts.** Add valid inequalities of $S$ to $\hat S$, such as the triangle inequalities $X_{ij} + X_{jk} + X_{ik} \ge -1$ for max-cut, or the cuts of [branch and cut](/branch-and-cut/).
- **Rank-one recovery.** If the SDP solution has rank $1$, $X = xx^\top$, then $x$ is optimal. For a quadratic problem with one quadratic constraint, such as the trust-region subproblem, the Shor relaxation is exact when a strictly feasible point exists, by the S-lemma.

## Pitfalls

- **The direction of the bound.** For a minimization the relaxation gives a lower bound, for a maximization an upper bound. A relaxed value says nothing about the quality of a rounded point unless the point is also evaluated in the original objective.
- **Exactness to a tolerance.** Numerical SDP solvers return a matrix that is rank one only up to their tolerance, and an LP solver returns $x_i = 0.9999999$. Round, check that the point is in $S$, and compare its true value with the bound.
- **Size.** The Shor relaxation has $n(n + 1)/2$ variables and a matrix constraint of order $n$. For large $n$, use first-order SDP methods, low-rank factorizations of $X$, or a weaker LP or SOCP relaxation.
- **A weak relaxation.** A relaxation can be valid and still useless, for example the LP relaxation of a big-M model, whose bound gets weaker as M grows. Check the integrality gap on small cases before building on it.

## Exercises

1. For vertex cover on the triangle, show that the LP relaxation has the optimal value $\tfrac32$ at $(\tfrac12, \tfrac12, \tfrac12)$, while every cover has size $2$. What does the threshold rounding return, and how does its size compare with $2 \cdot \tfrac32$?
2. Show that the Shor relaxation of max-cut on the $4$-cycle is exact: find a feasible $X$ of rank $1$ and a dual $z$ with the same value.
3. Prove that the convex envelope of the function $[x \ne 0]$ on $[-1, 1]$ is $|x|$. Then show that the convex envelope of the number of nonzero entries on the box $\|x\|_\infty \le 1$ is $\|x\|_1$.

## References
