---
tag: QQ5FA1
kind: concept
slug: ideal-formulation
name: Ideal formulation
aliases:
- sharp formulation
- tight formulation
- perfect formulation
- integral formulation
area: optimization/integer-programming
level: advanced
summary: A formulation whose LP relaxation has the integer hull as its feasible region.
prereqs: [lp-relaxation, integer-hull]
see_also: [integrality-gap, total-unimodularity, big-m-formulation, disjunctive-cut, matching-polytope, totally-dual-integrality, hoffman-kruskal-theorem, flow-integrality-theorem]
sources:
  - paper: "Juan Pablo Vielma, Mixed integer linear programming formulation techniques, SIAM Review 57(1) (2015), 3 to 57"
    locator: the sections on sharp and ideal formulations and on formulations for unions of polyhedra
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 4 (perfect formulations, extended formulations and unions of polyhedra)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (what is a good formulation, ideal formulations)
  - paper: "Egon Balas, Disjunctive programming: properties of the convex hull of feasible points, Discrete Applied Mathematics 89 (1998), 3 to 44"
    locator: the extended formulation of the convex hull of a union of polyhedra
  - paper: "Samuel Fiorini, Serge Massar, Sebastian Pokutta, Hans Raj Tiwary and Ronald de Wolf, Exponential lower bounds for polytopes in combinatorial optimization, Journal of the ACM 62(2) (2015)"
    locator: the lower bounds for the cut, stable set and traveling salesman polytopes
  - paper: "Thomas Rothvoss, The matching polytope has exponential extension complexity, Journal of the ACM 64(6) (2017)"
    locator: the main theorem
---

A formulation of a set $S$ of mixed-integer points is ideal when its [LP relaxation](/lp-relaxation/) is exactly the [integer hull](/integer-hull/) $\operatorname{conv}(S)$, or, in an extended space, when every vertex of the relaxation satisfies the integrality conditions. Then the [simplex method](/simplex-method/) returns an integer optimum for every objective, and the [integrality gap](/integrality-gap/) is 1. [Totally unimodular](/total-unimodularity/) systems, network flows and bipartite matching have ideal formulations of polynomial size. For NP-hard problems an ideal formulation of polynomial size is not expected, and for some polytopes it is proved not to exist, even with extra variables.

## In plain words

The same set of whole-number answers can be written down with different rules. Each set of rules, with the whole-number condition dropped, gives a region that contains all the answers. Some regions are loose and also contain many fractional points far from any answer. An ideal set of rules gives the tightest possible region, the one whose corners are all whole-number answers.

With an ideal formulation, a fast method for fractional problems always stops at a corner, so it gives a whole-number answer that is the best one. This is the best case for a modeler. Most hard problems do not have a short ideal formulation, but making a formulation closer to ideal almost always makes a solver faster.

## The idea

Let $S = \{x \in \mathbb{R}^n : Ax \le b,\ x_j \in \mathbb{Z} \text{ for } j \in I\}$ with rational data, and let $P = \{x : Ax \le b\}$.

**Definitions.**

- $P$ is an *ideal* (or *perfect*) formulation of $S$ if $P = \operatorname{conv}(S)$. When $P$ has vertices, this is the same as: each vertex of $P$ has $x_j \in \mathbb{Z}$ for $j \in I$.
- An *extended formulation* uses extra variables $w$: a polyhedron $Q \subseteq \mathbb{R}^{n} \times \mathbb{R}^{p}$ whose projection onto $x$ meets the integrality conditions in exactly $S$. Vielma (2015) calls $Q$ *sharp* if its projection is $\operatorname{conv}(S)$, and *ideal* if every vertex of $Q$ satisfies the integrality conditions on the variables that must be integer, which may include some of the $w$.

For a formulation without extra variables, sharp and ideal mean the same thing. With extra variables, ideal implies sharp when $Q$ has vertices, but a sharp $Q$ can have fractional vertices that project to points inside $\operatorname{conv}(S)$. The word "tight" is used for either, and sometimes only for "stronger than another formulation".

**Equivalent conditions.** For a rational polyhedron $P$ with $P \cap \mathbb{Z}^n \ne \emptyset$ in the pure integer case, the following are equivalent:

1. $P = P_I$.
2. Each nonempty face of $P$ contains an integer point.
3. $\max\{c^T x : x \in P\}$ is attained by an integer point for each $c$ for which it is finite.
4. $\max\{c^T x : x \in P\}$ is an integer for each integer $c$ for which it is finite.

The equivalence of 1 to 3 is direct: an optimal face of $c$ is a face of $P$, and each face is an optimal face of some $c$. Condition 4 is the theorem of Edmonds and Giles (1977). It is the bridge to [total dual integrality](/totally-dual-integrality/): if $Ax \le b$ is TDI and $b$ is integral, LP duality gives condition 4, so $P$ is integral.

**Sufficient conditions.** If $A$ is totally unimodular, then $\{x : Ax \le b\}$ is integral for each integral $b$, and the [Hoffman-Kruskal theorem](/hoffman-kruskal-theorem/) gives the converse for the system $Ax \le b$, $x \ge 0$. If $Ax \le b$ is TDI and $b$ is integral, then $P$ is integral. Both give ideal formulations for flows, matchings in bipartite graphs, interval scheduling and many other problems.

**Unions of polyhedra.** Let $S = P_1 \cup \cdots \cup P_k$ with $P_i = \{x : A^i x \le b^i\}$ nonempty polytopes. Balas's extended formulation

$$x = \sum_{i=1}^{k} x^i,\qquad A^i x^i \le b^i y_i,\qquad \sum_{i=1}^{k} y_i = 1,\qquad y \ge 0,$$

with $y_i \in \{0,1\}$, is ideal: its projection onto $x$ is $\operatorname{conv}(S)$, and each vertex has $y$ integral. It is the basis of [disjunctive cuts](/disjunctive-cut/) and of [lift-and-project](/lift-and-project/). The price is $k$ copies of the variables.

**Size limits.** An ideal formulation can have exponentially many inequalities, and extra variables sometimes help: the spanning tree polytope has an extended formulation with $O(n^3)$ variables and constraints, for a graph with $n$ vertices. They do not always help. Fiorini, Massar, Pokutta, Tiwary and de Wolf (2015) proved that each extended formulation of the traveling salesman polytope has $2^{\Omega(\sqrt{n})}$ inequalities, and Rothvoss (2017) proved $2^{\Omega(n)}$ for the [matching polytope](/matching-polytope/) of the complete graph, though matching is solvable in polynomial time.

## Examples

**A fixed charge.** Let $S = \{(x, y) : 0 \le x \le u y,\ y \in \{0, 1\}\}$ with $u = 4$: a quantity $x$ is allowed only if $y$ pays the fixed charge. The formulation $0 \le x \le 4y$, $0 \le y \le 1$ has the vertices $(0,0)$, $(0,1)$, $(4,1)$, so it is ideal. The [Big-M](/big-m-formulation/) version $x \le My$, $x \le 4$ with $M = 8$ has the extra vertex $(4, 1/2)$, and with $M = 40$ the extra vertex $(4, 1/10)$. A larger $M$ gives a weaker formulation, since the relaxation then pays only $4/M$ of the fixed charge.

**Disaggregation.** One facility $y \in \{0,1\}$ serves $k$ customers $x_j \in [0, 1]$, and $x_j > 0$ only if $y = 1$. The aggregated constraint $\sum_j x_j \le k y$ is a valid formulation. For $k = 3$, its relaxation has fractional vertices such as $y = 1/3$, $x = (1, 0, 0)$ and $y = 2/3$, $x = (1, 1, 0)$. The disaggregated constraints $x_j \le y$ for each $j$ give an ideal formulation: each row $x_j - y \le 0$ has one $+1$ and one $-1$, so with the bounds the matrix is totally unimodular, and every vertex is integral.

**Knapsack.** For $S = \{x \in \mathbb{Z}^2 : x \ge 0,\ 3x_1 + 5x_2 \le 16\}$, the formulation $x \ge 0$, $3x_1 + 5x_2 \le 16$ is not ideal, since $(16/3, 0)$ is a vertex. The ideal one is $x \ge 0$, $2x_1 + 3x_2 \le 10$, $x_1 + 2x_2 \le 6$, whose vertices are $(0,0)$, $(5,0)$, $(2,2)$, $(0,3)$.

**Matching.** For a [bipartite graph](/bipartite-graph/), the degree constraints $x(\delta(v)) \le 1$, $x \ge 0$ are ideal. For the triangle they are not: $x = (1/2, 1/2, 1/2)$ is a vertex. Adding Edmonds' odd set constraints gives an ideal formulation of the matching polytope for every graph.

## Where it is used

- **Modeling.** Disaggregated constraints, tight bounds instead of [Big-M](/big-m-formulation/), and Balas's union formulation are standard ways to move a model toward ideal, often at the cost of more rows or columns.
- **Polynomial algorithms.** Ideal formulations of polynomial size, or with a polynomial separation routine, turn combinatorial problems into linear programs: [bipartite matching](/bipartite-matching/), [maximum flow](/max-flow-problem/), [min-cost flow](/min-cost-flow-problem/), spanning trees and [matroid intersection](/matroid-intersection/).
- **Strong cutting planes.** Facets of $\operatorname{conv}(S)$ for small substructures, such as one knapsack row or one fixed-charge flow, give [cover](/cover-inequality/) and [flow cover](/flow-cover-inequality/) inequalities. Each is an ideal formulation of a relaxation of the full problem.
- **Extended formulations.** Lower bounds on the size of ideal extended formulations show that some polytopes cannot be written as small linear programs.

## References
