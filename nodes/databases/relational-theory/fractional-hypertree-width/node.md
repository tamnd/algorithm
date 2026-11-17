---
tag: TQRKBW
kind: definition
slug: fractional-hypertree-width
name: Fractional hypertree width
aliases:
- fractional hypertree decomposition
area: databases/relational-theory
level: research
summary: The width of a tree decomposition whose bags are covered by fractional edge covers; bounded width gives polynomial time join evaluation.
prereqs: [hypertree-width, edge-cover, linear-programming-problem]
see_also: [agm-bound, generic-join, leapfrog-triejoin, yannakakis-algorithm, fractional-matching, treewidth, acyclic-hypergraph, conjunctive-query]
sources:
  - paper: doi:10.1145/2636918
    title: Martin Grohe and Daniel Marx, Constraint solving via fractional edge covers, ACM Transactions on Algorithms 11(1), article 4 (2014); first in SODA 2006, 289 to 298
    locator: the definition of fractional hypertree width, the polynomial-time evaluation for bounded width when a decomposition is given, and classes where it is much smaller than hypertree width
  - paper: doi:10.1145/1721837.1721845
    title: Daniel Marx, Approximating fractional hypertree width, ACM Transactions on Algorithms 6(2), article 29 (2010); first in SODA 2009, 902 to 911
    locator: for fixed w, a decomposition of width O(w^3) in polynomial time for each hypergraph of fractional hypertree width at most w
  - paper: doi:10.1145/3196959.3196962
    title: Wolfgang Fischl, Georg Gottlob and Reinhard Pichler, General and fractional hypertree decompositions, hard and easy cases, Proceedings of the 37th ACM Symposium on Principles of Database Systems (PODS), 17 to 32 (2018)
    locator: deciding whether the fractional hypertree width is at most 2 is NP-complete
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Daniel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 1737 to 1767 (2013)
    locator: the bound on the size of a join by a fractional edge cover, used for each bag
  - paper: doi:10.1006/jcss.2001.1809
    title: Georg Gottlob, Nicola Leone and Francesco Scarcello, Hypertree decompositions and tractable queries, Journal of Computer and System Sciences 64(3), 579 to 627 (2002)
    locator: hypertree decompositions, which fractional hypertree decompositions generalize
---

Fractional hypertree width is a width measure of a [hypergraph](/hypergraph/) that is never larger than [hypertree width](/hypertree-width/) and is often much smaller. It uses a [tree decomposition](/tree-decomposition/), as hypertree width does, but it covers each bag by a fractional [edge cover](/edge-cover/), a weighting of the edges, instead of a set of edges. Grohe and Marx (2006, journal version 2014) defined it. If a [conjunctive query](/conjunctive-query/) has a decomposition of fractional width $w$, then by the [AGM bound](/agm-bound/) each bag has at most $N^w$ partial answers on a database with $N$ tuples per relation, and the query can be evaluated in polynomial time.

## Definition

Let $H = (V, E)$ be a hypergraph and $B \subseteq V$.

**Fractional edge cover.** A *fractional edge cover* of $B$ is a map $\gamma : E \to [0, \infty)$ with $\sum_{e \ni v} \gamma(e) \ge 1$ for each $v \in B$. Its *weight* is $\sum_{e \in E} \gamma(e)$. The *fractional edge cover number* $\rho^*_H(B)$ is the smallest weight of a fractional edge cover of $B$. It is the value of a [linear program](/linear-programming-problem/), so it can be computed in polynomial time, and by linear programming duality it equals the largest weight of a fractional independent set of $B$.

**Definition (Grohe and Marx 2006).** A *fractional hypertree decomposition* of $H$ is a triple $(T, \chi, \gamma)$, where $(T, \chi)$ is a tree decomposition of $H$ and $\gamma_p$ is a fractional edge cover of the bag $\chi(p)$ for each node $p$ of $T$. So:

1. for each edge $e \in E$ there is a node $p$ with $e \subseteq \chi(p)$;
2. for each vertex $v \in V$ the set $\{ p : v \in \chi(p) \}$ induces a connected subtree of $T$;
3. for each node $p$ and each $v \in \chi(p)$, $\sum_{e \ni v} \gamma_p(e) \ge 1$.

Its *width* is $\max_p \sum_e \gamma_p(e)$. The *fractional hypertree width* $\mathrm{fhw}(H)$ is the smallest width of a fractional hypertree decomposition. Equivalently,

$$\mathrm{fhw}(H) = \min_{(T, \chi)} \; \max_{p} \; \rho^*_H(\chi(p)),$$

over all tree decompositions $(T, \chi)$ of $H$. A decomposition with finitely many nodes is enough, so the minimum exists.

**Comparisons (theorems).** A set of $k$ edges that covers a bag is a fractional cover of weight $k$. So

$$\mathrm{fhw}(H) \le \mathrm{ghw}(H) \le \mathrm{hw}(H),$$

where $\mathrm{ghw}$ is the generalized hypertree width. One bag with all vertices gives $\mathrm{fhw}(H) \le \rho^*_H(V)$. Grohe and Marx showed that there are classes of hypergraphs of bounded fractional hypertree width and unbounded hypertree width, so the first inequality can be far from equality.

**Evaluation (theorem).** Let $Q$ be a conjunctive query whose hypergraph has a fractional hypertree decomposition of width $w$, given as part of the input, and let each relation have at most $N$ tuples. For each node $p$, let $R_p$ be the join of the projections $\pi_{e \cap \chi(p)}(R_e)$ over all edges $e$ that meet $\chi(p)$. The cover $\gamma_p$, restricted to these projections, gives $|R_p| \le \prod_e N^{\gamma_p(e)} \le N^w$ by the AGM bound, and a worst-case optimal join such as [Generic Join](/generic-join/) computes $R_p$ in about that time. The relations $R_p$ form an acyclic query along $T$ with the same answers as $Q$, and the [Yannakakis algorithm](/yannakakis-algorithm/) finishes in time polynomial in $N^w$, the size of $Q$ and the size of the output. This is combined complexity, and it is polynomial for each fixed $w$.

The bound $N^w$ is on each bag, not on the answer. The path query $Q(x, y, z) \mathbin{:\!-} R(x, y), S(y, z)$ is acyclic, so $\mathrm{fhw} = 1$, but with $R = \{(i, 0) : 1 \le i \le N\}$ and $S = \{(0, j) : 1 \le j \le N\}$ the answer has $N^2$ tuples.

**Computing the width (theorems).** Deciding $\mathrm{fhw}(H) \le 2$ is [NP-complete](/np-complete/) (Fischl, Gottlob and Pichler 2018). For each fixed $w$, Marx (2010) finds in polynomial time a fractional hypertree decomposition of width $O(w^3)$ for each hypergraph with $\mathrm{fhw}(H) \le w$. This approximation is enough for polynomial evaluation of queries of bounded fractional hypertree width when no decomposition is given.

## Examples and non-examples

- **Acyclic hypergraphs.** A join tree with $\gamma_p(e_p) = 1$ has width 1, so $\mathrm{fhw} = 1$. Each bag has at least one vertex that needs weight 1, so the width of a hypergraph with a nonempty edge is never less than 1.
- **The triangle.** The edges $AB$, $BC$, $CA$. One bag $\{A, B, C\}$ with weight $\tfrac12$ on each edge covers each vertex with weight 1, so $\mathrm{fhw} \le \tfrac32$. Any tree decomposition has a bag with all three vertices, since they form a clique of the primal graph, and each edge covers only two of them, so a fractional cover needs weight at least $\tfrac32$. So $\mathrm{fhw} = \tfrac32$, while $\mathrm{ghw} = \mathrm{hw} = 2$. On a database with $N$ tuples per relation, the triangle query has at most $N^{3/2}$ answers.
- **Complete graphs.** For $K_n$ read as a hypergraph with binary edges, some bag has all $n$ vertices, and weight $\tfrac{1}{n-1}$ on each of the $\binom{n}{2}$ edges covers them. Each edge covers 2 vertices, so $\mathrm{fhw}(K_n) = \tfrac{n}{2}$, while $\mathrm{ghw}(K_n) = \lceil n/2 \rceil$.
- **Longer cycles gain nothing.** Let $C_n$, $n \ge 4$, be the cycle of binary edges, of hypertree width 2 (see [hypertree width](/hypertree-width/)). The treewidth of a cycle is 2, so each tree decomposition has a bag with at least three vertices. Two of them are not adjacent, so no edge holds both, and each one needs weight 1 from its own edges. So each such bag needs weight 2, and $\mathrm{fhw}(C_n) = 2$. Among the cycles, only the triangle gains from fractional weights.
- **Non-example: one cover of the whole query.** $\rho^*_H(V)$ is only an upper bound. For the path $AB$, $BC$, $CD$, $DE$, vertex $A$ needs weight 1 on $AB$, vertex $E$ needs weight 1 on $DE$, and vertex $C$ needs weight 1 on $BC$ and $CD$ together, so $\rho^*_H(V) = 3$. But $\mathrm{fhw} = 1$, since the path is acyclic.

## Related definitions

- **AGM bound.** The [AGM bound](/agm-bound/) says that a join with a fractional edge cover of weight $w$ over all its variables has at most $N^w$ tuples. Fractional hypertree width applies the bound to each bag instead of to the whole query.
- **Hypertree width.** [Hypertree width](/hypertree-width/) uses integral covers and the special condition. It is at least the fractional hypertree width.
- **Worst-case optimal joins.** [Generic Join](/generic-join/) and [Leapfrog Triejoin](/leapfrog-triejoin/) meet the AGM bound and so compute each bag in time close to $N^{\rho^*}$.
- **Fractional matchings.** By duality, $\rho^*_H(B)$ equals the largest weight of a fractional independent set of $B$, the vertex version of a [fractional matching](/fractional-matching/).
- **Treewidth.** For graphs with binary edges, the cover number of a bag of $b$ vertices is at least $b / 2$ and at most $b$, so fractional hypertree width and [treewidth](/treewidth/) are within a factor of about 2. For hypergraphs with large edges the gap can be unbounded.

## References
