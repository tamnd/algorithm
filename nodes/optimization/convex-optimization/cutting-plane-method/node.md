---
tag: 6QC9VJ
kind: algorithm
slug: cutting-plane-method
name: Cutting-plane method
aliases:
- Kelley's cutting-plane method
- Kelley's method
- Cheney-Goldstein method
area: optimization/convex-optimization
level: advanced
summary: Iteratively add linear cuts that exclude infeasible or suboptimal regions.
model: real-ram
complexity:
  vars: {k: the number of iterations, n: the dimension, s: the cost of one oracle call, p: the cost of one linear program with n + 1 variables and at most k + 2n constraints}
  time: {worst: O(k (s + p))}
  space: {extra: O(k n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1960
  people: [James E. Kelley, Elliott W. Cheney, Allen A. Goldstein]
  note: Cheney and Goldstein (1959) and Kelley (1960) proposed the method independently. Center-of-gravity, ellipsoid and analytic-center methods later used cuts to shrink a region, which gave iteration bounds that are polynomial in the dimension.
prereqs: [subgradient, linear-programming-problem, separation-oracle]
see_also: [bundle-method, ellipsoid-method, cutting-plane-method-integer-programming, dantzig-wolfe-decomposition, benders-decomposition, column-generation, proximal-point-method, simplex-method]
sources:
  - paper: doi:10.1137/0108053
    title: James E. Kelley, The cutting-plane method for solving convex programs, Journal of the Society for Industrial and Applied Mathematics 8(4), 1960
    locator: pages 703 to 712
  - paper: doi:10.1007/BF01386389
    title: Elliott W. Cheney and Allen A. Goldstein, Newton's method for convex programming and Tchebycheff approximation, Numerische Mathematik 1, 1959
    locator: pages 253 to 268
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 3.3 (methods with complete data, Kelley's method and the example on which it is slow, and the level method)
  - paper: doi:10.1007/BF01585555
    title: Claude Lemaréchal, Arkadi Nemirovski and Yurii Nesterov, New variants of bundle methods, Mathematical Programming 69, 1995
    locator: pages 111 to 147 (the level method, which stabilizes the cutting-plane model)
  - paper: doi:10.2140/pjm.1960.10.1257
    title: Branko Grünbaum, Partitions of mass-distributions and of convex bodies by hyperplanes, Pacific Journal of Mathematics 10(4), 1960
    locator: pages 1257 to 1261 (each hyperplane through the centroid leaves at least the fraction (n/(n+1))^n of the volume on each side)
  - paper: doi:10.1007/BF02592216
    title: Pravin M. Vaidya, A new algorithm for minimizing convex functions over convex sets, Mathematical Programming 73(3), 1996
    locator: pages 291 to 341
  - paper: doi:10.1007/BF01585551
    title: David S. Atkinson and Pravin M. Vaidya, A cutting plane algorithm for convex programming that uses analytic centers, Mathematical Programming 69, 1995
    locator: pages 1 to 43
---

The cutting-plane method of Kelley minimizes a convex function $f$ over a box or a polytope when the only access to $f$ is an oracle that returns $f(x)$ and one [subgradient](/subgradient/) $g$ at a query point $x$. Each answer gives a linear lower bound $f(y) \ge f(x) + g^\top(y - x)$, called a cut. The method keeps all cuts, takes their maximum as a piecewise linear model of $f$, and queries next at a point where the model is lowest. That point comes from a small [linear program](/linear-programming-problem/). The minimum of the model is a lower bound $L$ on the optimum and the best value seen is an upper bound $U$, so the method always knows how far it is from optimal. It stops after at most $(1 + GD\sqrt{n}/\varepsilon)^n$ oracle calls when the subgradients have norm at most $G$ and the box has sides at most $D$, and it stops after finitely many calls with the exact optimum when $f$ is polyhedral.

## In plain words

You want the lowest point of a bowl, but you are blindfolded. At each place you touch, you learn the height and the slope there. From that you know the whole bowl lies above a certain flat plane through that place. Collect all these planes. Together they form a floor that is under the bowl everywhere. Go to the lowest point of this floor and touch the bowl there. If the bowl is close to the floor at that point, you are almost done, because nothing can be lower than the floor. If the bowl is much higher there, the new plane lifts the floor there, so you do not come back to the same place. The method can be slow in many dimensions and can jump far from good points.

## The problem

Minimize a convex $f: \mathbb{R}^n \to \mathbb{R}$ over the box $X = \{x : l \le x \le u\}$. The function is known only through a first-order oracle: for a query $x$, it returns $f(x)$ and a subgradient $g \in \partial f(x)$. The assumptions for the iteration bound are that each returned subgradient has $\|g\| \le G$ and that each side of the box has length at most $D$. The input is the oracle, $l$, $u$, a start $x_0 \in X$ and a tolerance $\varepsilon \ge 0$. The output is a point $x_{\text{best}}$ with $f(x_{\text{best}}) - \min_X f \le U - L \le \varepsilon$. A polytope $\{x : Cx \le d\}$ in place of the box needs only more rows in the linear program.

## The algorithm

```pseudo id=main
KELLEY(oracle, l, u, x, ε)
L1  B ← empty list of cuts;  U ← +∞
L2  repeat
L3      (f(x), g) ← oracle(x)
L4      append the cut  t ≥ f(x) + gᵀ(y − x)  to B
L5      if f(x) < U then U ← f(x); x_best ← x
L6      (x⁺, L) ← a minimizer of t over all (y, t) with l ≤ y ≤ u that satisfy every cut in B
L7      x ← x⁺
L8  until U − L ≤ ε
L9  return x_best, U, L
```

Line L6 is a linear program in the $n + 1$ variables $(y, t)$ with one row per cut and the box bounds. The value $L$ is the least value of the model $m(y) = \max_{\text{cuts}}\big(f(x_i) + g_i^\top(y - x_i)\big)$ over the box. The implementation solves it exactly with a dense simplex method and Bland's rule. With the substitution $y = l + w$ and $t = M - s$, where $M$ is the largest cut value at $l$, the slack basis is feasible, so no first phase is needed.

## Example

Minimize $f(x) = x^2$ over $[-1, 2]$, from $x_0 = 2$. The cut at $a$ is the tangent line $2ax - a^2$. Two tangents at $a$ and $b$ meet at $x = (a + b)/2$ with height $ab$, so after the second step each new query point is the mean of the last two. In exact arithmetic:

| $j$ | $x_j$ | $f(x_j)$ | $g_j$ | $U_j$ | $L_j$ | $x_{j+1}$ |
|---|---|---|---|---|---|---|
| 0 | 2 | 4 | 4 | 4 | -8 | -1 |
| 1 | -1 | 1 | -2 | 1 | -2 | 1/2 |
| 2 | 1/2 | 1/4 | 1 | 1/4 | -1/2 | -1/4 |
| 3 | -1/4 | 1/16 | -1/2 | 1/16 | -1/8 | 1/8 |
| 4 | 1/8 | 1/64 | 1/4 | 1/64 | -1/32 | -1/16 |

The first model is the single line $4x - 4$, whose minimum on the box is $-8$ at $x = -1$. After that the query points are $x_j = (-\tfrac12)^{j-1}$, and the certified gap is $U_j - L_j = 3 \cdot 4^{1-j}$. The bounds always enclose $f^* = 0$. In one dimension the method is fast. In higher dimensions the same model needs many more cuts.

## Correctness

Each cut lies below $f$ by the subgradient inequality, so the model lies below $f$ and its minimum $L$ is at most $f^* = \min_X f$. The upper bound $U$ is a value of $f$ at a point of $X$. So $L \le f^* \le U$ at every step, and when the method stops, $x_{\text{best}}$ is within $\varepsilon$ of optimal. For termination, the new point $x_{j+1}$ satisfies every old cut with value $L_j$, so for each earlier point $x_i$ we get $U_j - L_j \le f(x_i) - L_j \le -g_i^\top(x_{j+1} - x_i) \le G\|x_{j+1} - x_i\|$. While the gap is above $\varepsilon$, all query points are more than $\varepsilon/G$ apart, and only finitely many such points fit in the box. The full proof is below.

## Complexity

**Iterations.** Under the assumptions of the problem statement, for $\varepsilon > 0$ the method stops after at most

$$\Big(1 + \frac{GD\sqrt{n}}{\varepsilon}\Big)^n - 1$$

oracle calls. This bound is exponential in $n$, and the method can really be that slow: Nemirovski and Yudin gave functions on which the number of calls grows exponentially with $n$ for a fixed $\varepsilon$ (Nesterov 2018, Section 3.3). If $f$ is the maximum of $P$ affine pieces and the oracle returns the slope of an active piece, the method stops with $U = L = f^*$ after at most $P + 1$ calls, because each call that does not stop it adds a new piece to the model.

**One iteration.** One oracle call and one linear program with $n + 1$ variables and $k + 2n$ constraints at step $k$. Starting the simplex method from the last optimal basis makes each new linear program cheap in practice, but the number of constraints grows by one per step. The space is $O(kn)$ for the cuts.

## Properties

- **Certified gap.** $L \le f^* \le U$ at every step, with no constants to estimate.
- **Monotone bounds.** $L$ does not decrease, because the model only grows, and $U$ does not increase.
- **Unstable query points.** The minimizer of the model can jump from one corner of the box to another, even when the current point is nearly optimal. The function values $f(x_j)$ are not monotone.
- **Exact on polyhedral functions.** For a maximum of finitely many affine functions it stops with the exact optimum.
- **Growing subproblems.** The linear program gains one row per step. Dropping cuts is unsafe without care.

## Variants and improvements

- **Constraints.** For $\min f$ subject to a convex $h(x) \le 0$, add a cut $h(x) + s^\top(y - x) \le 0$ when $x$ violates the constraint. This is Kelley's original form. More generally, any [separation oracle](/separation-oracle/) for the feasible set gives cuts.
- **[Bundle methods](/bundle-method/).** Add a proximal term $\tfrac{1}{2t}\|y - \hat x\|^2$ to the model problem, or keep the query point in a level set of the model (the level method of Lemaréchal, Nemirovski and Nesterov, 1995). This stops the jumps and allows cuts to be dropped.
- **Localization methods.** Keep a region that must contain an optimum, query at its center, and cut it with the half-space $\{y : g^\top(y - x) \le 0\}$. Cutting through the centroid keeps at most $1 - (n/(n+1))^n \le 1 - 1/e$ of the volume (Grünbaum, 1960), which gives $O(n\log(1/\varepsilon))$ calls. The [ellipsoid method](/ellipsoid-method/) needs $O(n^2\log(1/\varepsilon))$ calls with cheap steps, and Vaidya's volumetric center method needs $O(n\log(1/\varepsilon))$ calls with polynomial work per step.
- **Decomposition.** [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/) and [column generation](/column-generation/) are Kelley's method applied to a Lagrangian dual, and [Benders decomposition](/benders-decomposition/) is Kelley's method on the value function of a subproblem.
- **Integer programming.** [Cutting planes for integer programs](/cutting-plane-method-integer-programming/), such as Gomory cuts, cut off fractional points rather than points of high cost. They share the name and the idea of a growing linear program.

## When to use it

Use Kelley's method when the function is nonsmooth, cheap linear programs are available, and the dimension is small, or when the function is polyhedral, where it is exact. In decomposition schemes the dimension is the number of coupling constraints, which is often small. For larger dimensions, prefer a [bundle method](/bundle-method/), which keeps the certified gap and is much more stable. If only a feasibility answer is needed for a set given by a separation oracle, use the [ellipsoid method](/ellipsoid-method/) or an analytic-center method.

## Pitfalls

- **An unbounded first model.** With no box, the first linear program is unbounded. Always bound the variables, or start with enough cuts.
- **Too many cuts.** The linear programs grow without limit. Removing inactive cuts can break convergence unless the method is stabilized, as in a bundle method.
- **Wrong subgradients.** A vector that is not a true subgradient gives a cut that can remove the optimum, and the lower bound becomes wrong. Check the oracle on test points.
- **Floating-point cuts.** Nearly parallel cuts make the linear program ill-conditioned. Use exact arithmetic or a robust LP solver, and stop on a relative gap.

## Implementations

## History

Cheney and Goldstein (1959) and Kelley (1960) proposed the method independently, for convex programs and for Chebyshev approximation. Dantzig and Wolfe (1960) built their decomposition method on the same idea applied to the dual. Levin and Newman proposed the center-of-gravity method in 1965, using Grünbaum's theorem on the volume cut off by a hyperplane through the centroid. The [ellipsoid method](/ellipsoid-method/) of Shor, Yudin and Nemirovski (1976 and 1977) made each cut cheap, and Khachiyan used it in 1979 to show that linear programming is solvable in polynomial time. Nemirovski and Yudin (1983) showed that Kelley's method can be exponentially slow in the dimension. The analytic-center methods of Atkinson and Vaidya and the volumetric center method of Vaidya (1989 to 1996) reached the best possible number of oracle calls up to constants.

## References
