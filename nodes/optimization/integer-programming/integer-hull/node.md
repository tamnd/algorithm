---
tag: T70Z1A
kind: concept
slug: integer-hull
name: Integer hull
aliases:
- convex hull of integer points
- integral hull
- P_I
area: optimization/integer-programming
level: advanced
summary: Convex hull of the integer points of a polyhedron; it is itself a polyhedron.
prereqs: [polyhedron, lp-relaxation, minkowski-weyl-theorem]
see_also: [ideal-formulation, chvatal-closure, chvatal-gomory-finite-convergence, total-unimodularity, matching-polytope, integrality-gap, lift-and-project, mixed-integer-programming]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 16 (the integer hull of a polyhedron) and Chapter 17 (estimates in integer linear programming)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 4 (perfect formulations, with Meyer's theorem)
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part I, Chapter 4 (polyhedral theory)
  - paper: "Robert R. Meyer, On the existence of optimal solutions to integer and mixed-integer programming problems, Mathematical Programming 7 (1974), 223 to 235"
    locator: the main theorem
  - paper: "William Cook, Mark Hartmann, Ravi Kannan and Colin McDiarmid, On integer points in polyhedra, Combinatorica 12 (1992), 27 to 37"
    locator: the bound on the number of vertices of the integer hull in fixed dimension
---

The integer hull of a [polyhedron](/polyhedron/) $P \subseteq \mathbb{R}^n$ is the convex hull of its integer points, written $P_I = \operatorname{conv}(P \cap \mathbb{Z}^n)$. Maximizing a linear function over the integer points of $P$ is the same as maximizing it over $P_I$, so an [integer program](/mixed-integer-programming/) is a linear program over $P_I$. Meyer's theorem says that $P_I$ is again a polyhedron when $P$ is rational. The catch is that a description of $P_I$ by inequalities is usually not known, can have exponentially many facets, and is hard to compute.

## In plain words

Draw a region on squared paper and mark the corners of the squares that lie inside it. Now stretch a rubber band around the marked points. The shape inside the band is the integer hull.

It is a smaller region with straight sides, and each of its corners is a marked point. A linear goal, such as "go as far right as you can", reaches its best value at a corner. So the best whole-number answer and the best answer over the smaller region are the same. If we knew the sides of the hull, a fast method for fractional problems would also solve the whole-number problem. The hard part is to find those sides.

## The idea

**Definition.** For $P \subseteq \mathbb{R}^n$, let $P_I = \operatorname{conv}(P \cap \mathbb{Z}^n)$. For a mixed-integer set with integer variables $I$, the same name is used for $\operatorname{conv}\{x \in P : x_j \in \mathbb{Z} \text{ for } j \in I\}$.

**Why it matters.** A linear function has the same supremum on a set and on its convex hull. So for each $c$,

$$\max\{c^T x : x \in P,\ x \in \mathbb{Z}^n\} = \max\{c^T x : x \in P_I\},$$

and each vertex of $P_I$ is an integer point. When $P_I$ is a polyhedron, the [simplex method](/simplex-method/) applied to a description of $P_I$ returns an integer optimum. A formulation with $P = P_I$ is [ideal](/ideal-formulation/), and [total unimodularity](/total-unimodularity/) is the classic reason for $P = P_I$.

**Meyer's theorem.** If $P$ is a rational polyhedron, then $P_I$ is a rational polyhedron. If $P_I \ne \emptyset$, then $P_I$ and $P$ have the same recession cone.

*Proof.* By the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), $P = \operatorname{conv}(V) + \operatorname{cone}(R)$ for finite sets $V$ and $R$. Since $P$ is rational, we can scale each $r \in R$ to an integer vector. Let

$$B = \operatorname{conv}(V) + \Big\{\sum_{r \in R} \lambda_r r : 0 \le \lambda_r \le 1\Big\}.$$

This set is bounded, so $B \cap \mathbb{Z}^n$ is finite. Let $x \in P \cap \mathbb{Z}^n$, and write $x = v + \sum_r \lambda_r r$ with $v \in \operatorname{conv}(V)$ and $\lambda \ge 0$. Then $y = x - \sum_r \lfloor \lambda_r \rfloor r$ is an integer vector, because each $r$ is integral, and $y = v + \sum_r (\lambda_r - \lfloor \lambda_r \rfloor) r$ lies in $B$. So

$$P \cap \mathbb{Z}^n = (B \cap \mathbb{Z}^n) + \Big\{\sum_r \mu_r r : \mu_r \in \mathbb{Z},\ \mu_r \ge 0\Big\},$$

where the inclusion from right to left holds because $B \subseteq P$ and $\operatorname{cone}(R)$ is the recession cone of $P$. We show that $P_I = \operatorname{conv}(B \cap \mathbb{Z}^n) + \operatorname{cone}(R)$. The inclusion $\subseteq$ follows from the equation, since the right side is convex. For $\supseteq$, let $y \in \operatorname{conv}(B \cap \mathbb{Z}^n)$, $r \in R$ and $\alpha \ge 0$. For an integer $N \ge \alpha$, the point $y + N r$ lies in $P_I$ by the equation, and

$$y + \alpha r = \big(1 - \tfrac{\alpha}{N}\big)\, y + \tfrac{\alpha}{N}\,(y + N r)$$

is a convex combination of two points of $P_I$. Repeating this for each $r$ gives the inclusion. So $P_I$ is the sum of a polytope with integer vertices and a rational cone, which is a rational polyhedron by Minkowski-Weyl. If $P_I \ne \emptyset$, its recession cone is $\operatorname{cone}(R)$, which is that of $P$. $\square$

The same proof, with the integer vectors replaced by vectors that are integral in the coordinates $I$, gives the mixed-integer version.

**Irrational data.** For $P = \{x \in \mathbb{R}^2 : 0 \le x_2 \le \sqrt{2}\, x_1\}$, the only integer point on the line $x_2 = \sqrt{2}\, x_1$ is the origin, but integer points $(p, q)$ with $q/p$ below $\sqrt{2}$ and as close as we like to it exist. So $P_I = \{0\} \cup \{x : x_1 > 0,\ 0 \le x_2 < \sqrt{2}\, x_1\}$, which is not closed, and so it is not a polyhedron.

**Size.** The vertices of $P_I$ are integer points whose size, in bits, is bounded by a polynomial in $n$ and the size of the inequalities of $P$. So each facet of $P_I$ also has a description of polynomial size. The number of facets and vertices is another matter. In a fixed dimension $n$, Cook, Hartmann, Kannan and McDiarmid (1992) bound the number of vertices of $P_I$ by a polynomial in $m$ and the input size, where $m$ is the number of inequalities. In a variable dimension it can be exponential. For NP-hard problems such as the [traveling salesman problem](/traveling-salesman-problem/), unless NP = coNP, there is no family of inequalities that describes $P_I$ and whose validity has short proofs. Separation over $P_I$ is as hard as optimization over it, by the equivalence of separation and optimization of Grötschel, Lovász and Schrijver.

**Approaching it.** Cutting planes produce a sequence $P \supseteq P' \supseteq P'' \supseteq \cdots \supseteq P_I$. The [Chvátal closure](/chvatal-closure/) reaches $P_I$ after finitely many rounds for rational $P$, by the [finite convergence theorem](/chvatal-gomory-finite-convergence/). The [lift-and-project](/lift-and-project/) and [disjunctive](/disjunctive-cut/) closures reach the hull of a 0/1 set in at most $n$ rounds.

## Examples

**The running example.** For $P = \{x \ge 0 : 3x_1 + 2x_2 \le 6,\ -3x_1 + 2x_2 \le 0\}$, with vertices $(0,0)$, $(2,0)$ and $(1, 3/2)$, the integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$. So

$$P_I = \operatorname{conv}\{(0,0),\ (2,0),\ (1,1)\} = \{x : x_2 \ge 0,\ x_2 \le x_1,\ x_1 + x_2 \le 2\}.$$

Each of the last two facets is a [Chvátal-Gomory cut](/chvatal-gomory-cut/) of $P$.

**A knapsack set.** For $P = \{x \ge 0 : 3x_1 + 5x_2 \le 16\}$, the LP vertices are $(0,0)$, $(16/3, 0)$ and $(0, 16/5)$. The 14 integer points have the hull with vertices $(0,0)$, $(5,0)$, $(2,2)$, $(0,3)$, so

$$P_I = \{x \ge 0 : 2x_1 + 3x_2 \le 10,\ x_1 + 2x_2 \le 6\}.$$

One knapsack row gave two new facets, with coefficients that do not appear in the original row.

**A thin triangle.** For $P_t = \operatorname{conv}\{(0,0), (0,1), (t, 1/2)\}$ with an integer $t \ge 1$, the only integer points are $(0,0)$ and $(0,1)$. So $P_I$ is the segment $\{0\} \times [0,1]$, though $P_t$ reaches $x_1 = t$. The Chvátal closure needs $2t$ rounds to reach it.

**Matching.** For the degree constraints of a graph, $P = \{x \ge 0 : x(\delta(v)) \le 1 \text{ for each vertex } v\}$, the integer hull is the [matching polytope](/matching-polytope/). Edmonds showed that it is described by $P$ and the odd set inequalities $x(E(S)) \le (|S| - 1)/2$ for each odd vertex set $S$. These are exponentially many, but they can be separated in polynomial time. For a [bipartite graph](/bipartite-graph/), $P = P_I$, since the [incidence matrix](/incidence-matrix/) is totally unimodular.

## Where it is used

- **Polyhedral combinatorics.** The study of the facets of $P_I$ for a combinatorial problem, such as matching, the traveling salesman problem or knapsack, gives the strong valid inequalities used in [branch and cut](/branch-and-cut/).
- **Cutting-plane theory.** Every cut family, from [Chvátal-Gomory cuts](/chvatal-gomory-cut/) to [cover inequalities](/cover-inequality/), approximates $P_I$, and its closure is compared with $P_I$.
- **Existence of optima.** Meyer's theorem gives part 4 of the proposition on the [LP relaxation](/lp-relaxation/) page: for rational data, an integer program whose relaxation is unbounded is itself unbounded or infeasible, and a bounded feasible integer program has an optimal solution.
- **Duality.** Since $P_I$ is a polyhedron, LP duality applies to it, and [subadditive duality](/subadditive-duality/) gives a closed form of its dual.
- **Integer programming in fixed dimension.** The polynomial bound on the number of vertices of $P_I$ is one route to algorithms for a fixed number of variables, with [Lenstra's algorithm](/lenstra-algorithm/) the classic one.

## References
