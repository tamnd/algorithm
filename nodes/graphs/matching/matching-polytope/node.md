---
tag: 2YQ3C5
kind: concept
slug: matching-polytope
name: Matching polytope
aliases:
- perfect matching polytope
area: graphs/matching
level: advanced
summary: Convex hull of the incidence vectors of all matchings of a graph.
prereqs: [convex-hull, linear-programming-problem, perfect-matching]
see_also: [edmonds-polytope-theorem, fractional-matching, birkhoff-von-neumann-decomposition, totally-dual-integrality, maximum-weight-matching, minimum-weight-perfect-matching, separation-oracle, tutte-berge-formula]
sources:
  - paper: doi:10.6028/jres.069B.013
    title: Jack Edmonds, Maximum matching and a polyhedron with 0,1-vertices, Journal of Research of the National Bureau of Standards 69B, 125 to 130 (1965)
    locator: the whole paper (the description of the matching polytope by odd-set constraints)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 18, Bipartite matching polytope, and Chapter 25, The matching polytope
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 11, Weighted Matching (the perfect matching polytope and its separation problem)
  - paper: "Manfred W. Padberg and M. R. Rao, Odd minimum cut-sets and b-matchings, Mathematics of Operations Research 7(1), 67 to 80 (1982)"
    locator: the whole paper (separation over the odd-set constraints in polynomial time)
  - paper: "Thomas Rothvoss, The matching polytope has exponential extension complexity, Journal of the ACM 64(6), article 41 (2017)"
    locator: the whole paper
---

The matching polytope of a graph is the [convex hull](/convex-hull/) of the incidence vectors of its matchings, a [convex polytope](/convex-polytope/) in $\mathbb{R}^E$. The perfect matching polytope is the convex hull of the perfect matchings only. Optimizing a linear function over either polytope is the same as finding a [maximum-weight matching](/maximum-weight-matching/) or a [minimum-weight perfect matching](/minimum-weight-perfect-matching/). For a [bipartite graph](/bipartite-graph/) the degree constraints alone describe the polytope. For a general graph, Edmonds showed in 1965 that one more family of inequalities, one for each odd set of vertices, is enough. This result is the base of the primal-dual algorithms for weighted matching.

## In plain words

Write a matching as a list of 0s and 1s, one entry for each edge, with a 1 for the edges in the matching. Each such list is a corner point in a space with one direction per edge. Fill in everything between these corners, and you get a solid shape, the matching polytope.

The aim is to describe this shape by simple rules, such as "the values on the edges at each vertex add up to at most 1". Then a best matching for any edge weights can be found as a best point of the shape, with the methods of linear programming. When the graph has two sides, the rule at each vertex is enough. When the graph has odd cycles, a few fractional points also obey that rule, and an extra rule for each odd group of vertices cuts them off.

## The idea

Let $G = (V, E)$ be a finite undirected graph without weights, bipartite or general. For $F \subseteq E$ let $\chi^F \in \{0, 1\}^E$ be its incidence vector. For $v \in V$ let $\delta(v)$ be the set of edges at $v$; for $U \subseteq V$ let $\delta(U)$ be the edges with one end in $U$ and $E[U]$ the edges with both ends in $U$; and let $x(F) = \sum_{e \in F} x_e$.

$$P_{\text{match}}(G) = \operatorname{conv}\{\chi^M : M \text{ a matching of } G\}, \qquad P_{\text{perf}}(G) = \operatorname{conv}\{\chi^M : M \text{ a perfect matching of } G\}.$$

**The degree constraints.** Every matching satisfies
$$x_e \ge 0 \;\; (e \in E), \qquad x(\delta(v)) \le 1 \;\; (v \in V). \tag{D}$$
The points that satisfy (D) form the *[fractional matching](/fractional-matching/) polytope*. It contains $P_{\text{match}}(G)$, and it is its [LP relaxation](/lp-relaxation/).

**Bipartite graphs.** If $G$ is bipartite, the constraints (D) describe $P_{\text{match}}(G)$ exactly, and (D) with equality at each vertex describes $P_{\text{perf}}(G)$. The reason is that the vertex-edge [incidence matrix](/incidence-matrix/) of a bipartite graph is totally unimodular: every square submatrix has determinant 0, 1 or $-1$. So every vertex of the polytope given by (D), which is the solution of a square subsystem, is an integer vector by Cramer's rule, and an integer vector in (D) is the incidence vector of a matching. For the complete bipartite graph $K_{k,k}$, $P_{\text{perf}}$ is the set of doubly stochastic matrices, and this is the [Birkhoff-von Neumann theorem](/birkhoff-von-neumann-decomposition/).

**General graphs.** In an odd cycle, (D) allows fractional points that are not convex combinations of matchings. For each set $U \subseteq V$ with $|U|$ odd and $|U| \ge 3$, a matching has at most $(|U| - 1)/2$ edges inside $U$, so it satisfies
$$x(E[U]) \le \tfrac{|U| - 1}{2}. \tag{O}$$

**Theorem (Edmonds, 1965).** For every graph $G$, $P_{\text{match}}(G) = \{x : x \text{ satisfies (D) and (O)}\}$, and
$$P_{\text{perf}}(G) = \{x \ge 0 : x(\delta(v)) = 1 \text{ for } v \in V, \;\; x(\delta(U)) \ge 1 \text{ for } U \subseteq V \text{ with } |U| \text{ odd}\}.$$

The proof is on the page [Edmonds' polytope theorem](/edmonds-polytope-theorem/). A constructive proof is Edmonds' weighted matching algorithm: for each weight vector, it finds a matching and a dual solution on (D) and (O) with the same value.

**Duality and integrality.** The system (D) and (O) is [totally dual integral](/totally-dual-integrality/), by Cunningham and Marsh (1978): for integer weights, the dual linear program has an optimal solution in integers. For unit weights the dual becomes the [Tutte-Berge formula](/tutte-berge-formula/): an optimal integer dual can be built from a set $S$ that attains the formula and from the components of $G - S$.

**Size and separation.** The number of odd-set constraints (O) is exponential in $|V|$, and none of them can be dropped in general: for $U$ odd and $G[U]$ factor-critical and 2-connected, the inequality of $U$ defines a facet. Still, a [separation oracle](/separation-oracle/) exists. Padberg and Rao showed that a most violated odd-set constraint is found by a minimum odd cut, computable from a [Gomory-Hu tree](/gomory-hu-tree/) in polynomial time. So the [ellipsoid method](/ellipsoid-method/) optimizes over the polytope in polynomial time, and [cutting plane methods](/cutting-plane-method/) use the same cuts in practice.

**No small extended formulation.** One could hope to write the polytope as a projection of a polytope with few constraints in more variables. Rothvoss proved in 2014 that this is impossible: every extended formulation of the perfect matching polytope of the complete graph $K_n$ has $2^{\Omega(n)}$ constraints. This holds although weighted matching is solvable in polynomial time.

**Adjacency of vertices.** Two vertices $\chi^M$ and $\chi^N$ of $P_{\text{match}}(G)$ are adjacent on the polytope if and only if $M \oplus N$ is a single path or a single cycle. This is why algorithms that move along edges of the polytope, such as augmenting along one path, fit the structure.

## Examples

**The triangle.** Let $G$ be the triangle with edges $e_1, e_2, e_3$. The matchings are $\emptyset$ and the three single edges, so $P_{\text{match}}$ is the simplex with vertices $0$, $(1,0,0)$, $(0,1,0)$, $(0,0,1)$, that is $x \ge 0$, $x_1 + x_2 + x_3 \le 1$. The point $x = (\frac12, \frac12, \frac12)$ satisfies (D), since each vertex has two edges with value $\frac12$, but $x_1 + x_2 + x_3 = \frac32 > 1$. The odd-set constraint (O) for $U = V$ is exactly $x_1 + x_2 + x_3 \le 1$, and it cuts the point off.

**No perfect matching.** For the triangle, $P_{\text{perf}}$ is empty. The equalities $x(\delta(v)) = 1$ alone have the solution $x = (\frac12, \frac12, \frac12)$, but $\delta(V) = \emptyset$ and the constraint $x(\delta(V)) \ge 1$ for the odd set $V$ fails. More generally, for $U = V$ with $|V|$ odd, the constraint says $0 \ge 1$, so the description is empty, as it should be.

**The 4-cycle.** The 4-cycle is bipartite. The point with $\frac12$ on every edge satisfies (D) with equality, and it is the average of the two perfect matchings. So (D) with equalities describes $P_{\text{perf}}$, which is the segment between the two perfect matchings.

**The 5-cycle.** The point with $\frac12$ on every edge satisfies (D), but the edges inside $U = V$ give $\frac52 > 2 = (5 - 1)/2$. In general the point $\frac12 \chi^E$ of an odd cycle is a vertex of the polytope (D), and the odd-set constraint of the cycle removes it. In fact the vertices of the fractional matching polytope are exactly the vectors with values in $\{0, \frac12, 1\}$ whose $\frac12$ entries form disjoint odd cycles.

**The empty graph.** With no edges, $\mathbb{R}^E$ is a point, and $P_{\text{match}}$ is that point, the empty matching. With no vertices, $P_{\text{perf}}$ is also that point.

## Where it is used

- **Weighted matching algorithms.** Edmonds' algorithm for [maximum-weight matching](/maximum-weight-matching/) and [minimum-weight perfect matching](/minimum-weight-perfect-matching/) keeps a dual solution on (D) and (O), with nonzero values only on the odd sets that are current blossoms, and uses [complementary slackness](/complementary-slackness/) to decide which edges may be used. The [Hungarian algorithm](/hungarian-algorithm/) is the bipartite case, where only (D) is needed.
- **Polyhedral combinatorics.** It was the first polytope of a combinatorial problem described completely, beyond the bipartite and network cases. It started the study of integral polyhedra and of total dual integrality.
- **Integer programming.** For the [traveling salesman problem](/traveling-salesman-problem/), the blossom inequalities, a generalization of (O), are standard cutting planes, separated in the Padberg-Rao way.
- **Lower bounds for linear programs.** Rothvoss's theorem shows that some problems in $\mathsf P$ have no polynomial-size linear program in any lifted form.

## References
