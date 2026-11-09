---
tag: V38187
kind: algorithm
slug: benson-algorithm
name: Benson's outer approximation algorithm
aliases:
- Benson algorithm
- Benson outer approximation
- Benson's algorithm for MOLP
- primal Benson algorithm
area: optimization/multi-objective
level: research
summary: Computes the set of extreme nondominated points of a multi-objective LP by outer approximation of the upper image.
solves: [multi-objective-linear-programming]
model: real-ram
complexity:
  vars: {K: the number of cuts, N: the number of vertices of all outer approximations, L: the cost of one linear program, E: the cost of one vertex update, p: the number of objectives}
  time: {worst: O(N L + K E)}
  space: {extra: O(p N)}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1998
  people: [Harold P. Benson]
  note: Benson gave the outer approximation of the outcome set in 1998. Ehrgott, Löhne and Shao gave a dual variant in 2012, and Hamel, Löhne and Rudloff gave the form with one linear program per vertex used here in 2014.
prereqs: [multi-objective-linear-programming, lp-duality, supporting-hyperplane, vertex-enumeration]
see_also: [pareto-front, weighted-sum-method, simplex-method, convex-polytope, normal-boundary-intersection, separating-hyperplane-theorem, parametric-linear-programming]
sources:
  - paper: doi:10.1023/A:1008215702611
    title: Harold P. Benson, An outer approximation algorithm for generating all efficient extreme points in the outcome set of a multiple objective linear programming problem, Journal of Global Optimization 13(1), 1998
    locator: pages 1 to 24 (the outer approximation of the outcome set by cutting planes)
  - paper: doi:10.1007/s10898-013-0098-2
    title: Andreas H. Hamel, Andreas Löhne and Birgit Rudloff, Benson type algorithms for linear vector optimization and applications, Journal of Global Optimization 59(4), 2014
    locator: pages 811 to 836 (the primal algorithm with the linear programs P2(t) and D2(t), and its correctness and finiteness)
  - paper: doi:10.1007/s10898-011-9709-y
    title: Matthias Ehrgott, Andreas Löhne and Lizhen Shao, A dual variant of Benson's outer approximation algorithm for multiple objective linear programming, Journal of Global Optimization 52(4), 2012
    locator: pages 757 to 778 (the dual algorithm and the geometric duality between the upper image and a lower image)
  - book: isbn:9783642183508
    title: Andreas Löhne, Vector Optimization with Infimum and Supremum, Springer, 2011
    locator: Chapter 5 (Benson type algorithms for linear vector optimization)
---

Benson's algorithm computes the extreme points of the [Pareto front](/pareto-front/) of a [multi-objective linear program](/multi-objective-linear-programming/) by working in the objective space, not in the decision space. It keeps a polyhedron $\mathcal{T}$ that contains the upper image $\mathcal{P} = C[X] + \mathbb{R}^p_+$, starts with the [ideal point](/ideal-point/) plus the nonnegative orthant, and cuts $\mathcal{T}$ with supporting half-spaces of $\mathcal{P}$ until each vertex of $\mathcal{T}$ lies in $\mathcal{P}$. Then $\mathcal{T} = \mathcal{P}$, and its vertices are the extreme nondominated points. Each step solves one linear program. The objective space usually has far fewer dimensions than the decision space, which is why the method beats multi-objective simplex methods on large problems.

## In plain words

You want the corners of a shape, but you can only ask one kind of question: "here is a point; how far is it from the shape, and what is a flat wall that touches the shape and keeps this point out?"

Start with a big box that surely holds the shape. Look at a corner of the box. If the corner is in the shape, it is a true corner. If it is outside, the answer gives a wall; cut the box along the wall. The cut makes new corners. Go on until every corner is in the shape. Then the box and the shape are the same, and its corners are the answer.

## The problem

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p$, and $y = f(x)$ is the image of $x$.

The input is a multi-objective linear program

$$\min\ C x \quad \text{subject to} \quad x \in X = \{x \in \mathbb{R}^n : A x \geqq b\},$$

with $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$ and $C \in \mathbb{R}^{p \times n}$, so $f(x) = C x$. Assume that $X$ is not empty and that each objective $c_i^\top x$ is bounded below on $X$. The *upper image* is

$$\mathcal{P} = C[X] + \mathbb{R}^p_+ = \{y \in \mathbb{R}^p : y \geqq C x \text{ for some } x \in X\}.$$

It is a polyhedron with the recession cone $\mathbb{R}^p_+$. Its vertices are the extreme points of the nondominated set $Y_N$, and its nondominated points are $Y_N$. The output is the list of vertices of $\mathcal{P}$ and a list of inequalities that describe $\mathcal{P}$.

## The algorithm

Let $e = (1, \ldots, 1)$. For a point $t \in \mathbb{R}^p$, the linear program

$$\mathrm{P}_2(t): \quad \min\ z \quad \text{subject to} \quad A x \geqq b, \quad C x - z e \leqq t$$

finds the least $z$ such that $t + z e \in \mathcal{P}$. Its dual is

$$\mathrm{D}_2(t): \quad \max\ b^\top v - t^\top u \quad \text{subject to} \quad A^\top v = C^\top u, \quad e^\top u = 1, \quad u \geqq 0, \quad v \geqq 0.$$

The feasible set of $\mathrm{D}_2(t)$ does not depend on $t$. If the optimal value $z$ is positive, then $t \notin \mathcal{P}$, and an optimal $(u, v)$ gives the half-space $u^\top y \ge b^\top v$, which contains $\mathcal{P}$, touches it, and does not contain $t$.

```pseudo id=main
BENSON(A, b, C)               ▷ minimize Cx over X = {x : Ax ≥ b}; X ≠ ∅, each objective bounded below
L1  for i ← 1 to p do y^I_i ← min { c_i^T x : x ∈ X }
L2  𝒯 ← { y : y_i ≥ y^I_i for i = 1, ..., p }                ▷ kept as a list of inequalities
L3  loop
L4      V ← the vertices of 𝒯
L5      for each t ∈ V do
L6          solve D2(t); let z be its value and (u, v) an optimal basic solution
L7          if z > 0 then add u^T y ≥ b^T v to the inequalities of 𝒯 and go to L4
L8      return V and the inequalities of 𝒯                       ▷ now 𝒯 = 𝒫
```

Line L1 solves $p$ linear programs. Line L4 is a vertex enumeration. Practical codes update the vertices after each cut instead of starting again, by the double description method, and they remember which vertices have already been checked in line L6. The implementation here enumerates the vertices by brute force over all $p$-subsets of the inequalities, which is enough for small tests.

## Example

Minimize $(x_1, x_2)$ over $X = \{x : x_1 \ge 0,\ x_2 \ge 0,\ x_1 + 2 x_2 \ge 4,\ 3 x_1 + x_2 \ge 6\}$. Here $C$ is the identity, so $\mathcal{P} = X$, and the answer is known: the vertices are $(0, 6)$, $(8/5, 6/5)$ and $(4, 0)$. The cuts are written with $u$ scaled so that $u_1 + u_2 = 1$.

| round | vertices $V$ of $\mathcal{T}$ | $t$ checked | value $z$ of $\mathrm{D}_2(t)$ | cut added |
|---|---|---|---|---|
| 1 | $(0, 0)$ | $(0, 0)$ | $3/2$ | $\tfrac34 y_1 + \tfrac14 y_2 \ge \tfrac32$, that is, $3 y_1 + y_2 \ge 6$ |
| 2 | $(0, 6)$, $(2, 0)$ | $(0, 6)$ | $0$ | none |
| | | $(2, 0)$ | $2/3$ | $\tfrac13 y_1 + \tfrac23 y_2 \ge \tfrac43$, that is, $y_1 + 2 y_2 \ge 4$ |
| 3 | $(0, 6)$, $(8/5, 6/5)$, $(4, 0)$ | each | $0$ | none: stop |

Line L1 gives the ideal point $(0, 0)$. In round 1, the least $z$ with $(z, z) \in \mathcal{P}$ is $3/2$, where $3 z + z \ge 6$ is the tight constraint, and the cut is that constraint. In round 2, the point $(2, 0) + z e$ needs $(2 + z) + 2 z \ge 4$, so $z = 2/3$. After two cuts, $\mathcal{T} = \mathcal{P}$.

## Correctness

The proof has four steps. First, linear programming duality shows that the value of $\mathrm{D}_2(t)$ is the least $z$ with $t + z e \in \mathcal{P}$, so $t \in \mathcal{P}$ exactly when the value is at most 0. Second, every feasible $(u, v)$ gives a valid inequality: for $y \geqq C x$ with $x \in X$, $u^\top y \ge u^\top C x = v^\top A x \ge v^\top b$. An optimal one cuts off $t$, because $u^\top t = b^\top v - z < b^\top v$, and it supports $\mathcal{P}$. So $\mathcal{T} \supseteq \mathcal{P}$ at all times. Third, each cut comes from a vertex of the feasible set of $\mathrm{D}_2$, which has finitely many vertices, and no cut is added twice, so the loop ends. Fourth, at the end every vertex of $\mathcal{T}$ is in $\mathcal{P}$, and $\mathcal{T}$ is the convex hull of its vertices plus $\mathbb{R}^p_+$, so $\mathcal{T} \subseteq \mathcal{P}$. The full proof is below.

## Complexity

Let $K$ be the number of cuts and $N$ the number of vertices that appear in any $\mathcal{T}$. If each vertex is checked once, the algorithm solves $p + N$ linear programs and $K$ vertex updates, so the time is $O(N L + K E)$, where $L$ is the cost of one linear program and $E$ the cost of one update of the vertex list. The number $K$ is at most the number of vertices of the feasible set of $\mathrm{D}_2$, a polyhedron with $m + p$ variables, because no cut is added twice. Each $\mathcal{T}$ is cut out by $K + p$ inequalities, so it has at most $\binom{K + p}{p}$ vertices. Both numbers can be exponential in the input size, because the front itself can have exponentially many vertices.

The linear programs have $n + 1$ variables in the primal form. The vertex enumeration works in $\mathbb{R}^p$. When $p$ is small and $n$ is large, as in most applications, the linear programs dominate the time, and the number of rounds depends on the size of the answer, not on the number of vertices of $X$. A method in the decision space, such as a multi-objective simplex method, must move between bases of $X$, and many bases can map to the same point of the front.

The implementation recomputes all vertices by brute force in each round. It takes time exponential in the number of cuts, and serves only as a reference.

## Properties

- **Exact.** With exact arithmetic it returns all vertices of $\mathcal{P}$ and an inequality description, without tolerance.
- **Objective space.** The work outside the linear programs is in $\mathbb{R}^p$, so the cost depends on the shape of the front, not on the degeneracy of $X$.
- **Outer and inner approximations.** At each round, $\mathcal{T}$ is an outer approximation of $\mathcal{P}$, and the vertices found in $\mathcal{P}$ span an inner approximation. Stopping when every vertex has $z \le \varepsilon$ gives an $\varepsilon$-approximation of the front.
- **Supported points only.** All points of the front of a linear program are supported, so the vertices and the facets describe the whole front.
- **No preimages by default.** The algorithm returns points of the objective space. A preimage $x$ of each vertex comes from the primal solution of $\mathrm{P}_2(t)$ in the last round.

## Variants and improvements

- **Benson's original version (1998).** It works with a bounded part of the outcome set, uses a fixed interior point, and finds the boundary point on the segment from each vertex $t$ to this interior point before it solves a second linear program for the cut. The direction $e$ used here replaces the interior point, so one linear program per vertex is enough (Hamel, Löhne and Rudloff, 2014).
- **Dual variant.** Ehrgott, Löhne and Shao (2012) approximate a lower image in the dual space, linked to $\mathcal{P}$ by geometric duality: the facets of one correspond to the vertices of the other. The dual variant needs only weighted sum problems, so it suits problems where weighted sums are easy, such as combinatorial problems with a linear relaxation.
- **Approximate versions.** Stop at a tolerance $\varepsilon > 0$, which also extends the method to convex problems, where the upper image is not a polyhedron and only approximations are possible.
- **Unbounded problems.** The general versions handle problems where some objectives are not bounded below, by computing the recession directions first.
- **Software.** The Bensolve program of Löhne and Weißing implements the primal and dual algorithms.

## When to use it

Use it to compute the whole front of a multi-objective linear program with a small number of objectives and any number of variables. For a front that is too large to list, or for a decision maker who wants one point, use an interactive method or one [scalarization](/scalarization/) instead. For $p = 2$, a dichotomic search with [weighted sums](/weighted-sum-method/) finds the same vertices with about $2 k$ linear programs for $k$ vertices, and needs no vertex enumeration.

## Pitfalls

- **Floating point.** The test $z > 0$ in line L7 must use a tolerance in floating point, and a wrong decision either misses a vertex or loops. Exact arithmetic avoids this, at a cost.
- **Degenerate vertex enumeration.** Several cuts can pass through one vertex. Brute-force or incremental enumeration must remove copies and handle the many tight inequalities.
- **Unbounded objectives.** If an objective is not bounded below on $X$, line L1 fails, and the simple version does not apply.
- **Confusing the outcome set with the upper image.** The vertices of $C[X]$ include dominated points. The algorithm works with $C[X] + \mathbb{R}^p_+$, whose vertices are all nondominated.

## Implementations

## History

Benson (1998) introduced the outer approximation of the outcome set of a multi-objective linear program, to avoid the large number of efficient bases that simplex-based methods visit. Later work by Shao and Ehrgott gave approximate versions, and extended the method to convex problems. Ehrgott, Löhne and Shao (2012) gave the dual variant based on geometric duality, and Hamel, Löhne and Rudloff (2014) gave the version with the linear programs $\mathrm{P}_2(t)$ and $\mathrm{D}_2(t)$, the treatment of unbounded problems, and applications in finance. Löhne's book (2011) gives the theory of solution concepts behind these methods.

## References
