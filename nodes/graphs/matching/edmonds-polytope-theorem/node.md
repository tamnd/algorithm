---
tag: N3PGEX
kind: theorem
slug: edmonds-polytope-theorem
name: Edmonds' matching polytope theorem
aliases:
- matching polytope characterization
area: graphs/matching
level: advanced
summary: The matching polytope of a graph is given by degree constraints plus odd-set constraints.
prereqs: [fractional-matching, convex-polytope]
see_also: [matching-polytope, maximum-weight-matching, minimum-weight-perfect-matching, totally-dual-integrality, separation-oracle, petersens-theorem, blossom, tutte-berge-formula]
sources:
  - paper: doi:10.6028/jres.069B.013
    title: Jack Edmonds, Maximum matching and a polyhedron with 0,1-vertices, Journal of Research of the National Bureau of Standards 69B, 125 to 130 (1965)
    locator: the whole paper (the theorem, proved through the weighted matching algorithm)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 25, The matching polytope (Theorem 25.1 on the perfect matching polytope and Corollary 25.1a on the matching polytope, with the contraction proof)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 11, Weighted Matching (the perfect matching polytope theorem)
---

Edmonds' matching polytope theorem says that the [convex hull](/convex-hull/) of the matchings of any graph, the [matching polytope](/matching-polytope/), is described by two families of linear inequalities: the degree constraints, which say that at most one unit of weight meets each vertex, and the odd-set constraints, which say that a set of $2k + 1$ vertices spans at most $k$ units. The graph is general, bipartite or not, and the theorem is about the polytope itself, so it serves every edge weighting at once. It turns [maximum weight matching](/maximum-weight-matching/) into a [linear program](/linear-programming-problem/) with exponentially many constraints but integer optimal vertices, and it is the polyhedral side of the weighted blossom algorithm.

## Statement

Let $G = (V, E)$ be a finite undirected graph. For $x \in \mathbb{R}^E$ and $F \subseteq E$ write $x(F) = \sum_{e \in F} x_e$; let $\delta(U)$ be the set of edges with exactly one end in $U \subseteq V$, $\delta(v) = \delta(\{v\})$, and $E[U]$ the set of edges with both ends in $U$. For a set of edges $F$, $\chi^F \in \{0, 1\}^E$ is its incidence vector.

**Theorem 1 (perfect matching polytope).** The convex hull of the incidence vectors of the [perfect matchings](/perfect-matching/) of $G$ is

$$Q(G) = \bigl\{ x \in \mathbb{R}^E : x \ge 0, \;\; x(\delta(v)) = 1 \;\; (v \in V), \;\; x(\delta(U)) \ge 1 \;\; (U \subseteq V, \; |U| \text{ odd}) \bigr\}.$$

**Theorem 2 (matching polytope).** The convex hull of the incidence vectors of the matchings of $G$ is

$$P(G) = \bigl\{ x \in \mathbb{R}^E : x \ge 0, \;\; x(\delta(v)) \le 1 \;\; (v \in V), \;\; x(E[U]) \le \tfrac{|U| - 1}{2} \;\; (U \subseteq V, \; |U| \text{ odd}) \bigr\}.$$

Without the odd-set constraints, $P(G)$ is the [fractional matching](/fractional-matching/) polytope. In a [bipartite graph](/bipartite-graph/) the odd-set constraints are implied by the degree constraints, since that polytope is already integral. When $x(\delta(v)) = 1$ for all $v \in U$, the two forms of the odd-set constraint agree: $\sum_{v \in U} x(\delta(v)) = 2x(E[U]) + x(\delta(U))$, so $x(\delta(U)) \ge 1$ if and only if $x(E[U]) \le \frac{|U| - 1}{2}$.

**Examples.** In the triangle, $x = (\frac12, \frac12, \frac12)$ satisfies the degree constraints with equality, but $x(E[V]) = \frac32 > 1$ and $x(\delta(V)) = 0 < 1$: it lies in neither polytope, and indeed the triangle has no perfect matching and its matching polytope is the simplex $x \ge 0$, $x_1 + x_2 + x_3 \le 1$. In the 4-cycle, a bipartite graph, $x = \frac12$ on every edge is the average of the two perfect matchings and lies in $Q$. For a graph with an odd number of vertices, $U = V$ gives $0 \ge 1$, so $Q(G) = \emptyset$, matching the absence of a perfect matching. With no edges, both polytopes are the single point of $\mathbb{R}^\emptyset$, the empty matching, and $Q(G)$ is empty unless $V = \emptyset$ too.

## In plain words

Write each pairing of a network as a row of zeros and ones, one entry per link. Blend these rows in every possible proportion, and you get a solid shape. The theorem gives a short list of rules that describe exactly this shape.

The first rule: the amounts on the links at a point add up to at most one. In a two-sided network that rule is enough. In a triangle it is not: half on each link obeys it but is not a blend of pairings, because a triangle holds only one pair. The second rule fixes this: any odd group of points holds inside it at most half as many units as it has points, rounded down. With both rules, every corner of the shape is a real pairing, so the best pairing for any link values can be found as a best corner.

## Proof

Every perfect matching satisfies the constraints of $Q(G)$: it has one edge at each vertex, and an odd set $U$ cannot be covered by edges inside $U$ alone, so some edge of the matching leaves $U$. So the convex hull lies in $Q(G)$. We prove the converse.

**Proof of Theorem 1.** Suppose the theorem fails, and take a counterexample $G$ with $|V| + |E|$ as small as possible, and a vertex $x$ of the [convex polytope](/convex-polytope/) $Q(G)$ that is not a convex combination of perfect matchings. All constraints have integer coefficients, so $x$ is rational.

*Step 1: $0 < x_e < 1$ for every edge.* If $x_e = 0$, then the restriction of $x$ to $G - e$ lies in $Q(G - e)$, since $\delta_{G - e}(U) = \delta_G(U) \setminus \{e\}$ loses nothing of weight; by minimality it is a convex combination of perfect matchings of $G - e$, which are perfect matchings of $G$. If $x_e = 1$ for $e = uv$, the degree constraints force every other edge at $u$ and $v$ to have value 0, and by the previous case there is none. Then $e$ is a component of $G$, the restriction of $x$ to $G - u - v$ lies in $Q(G - u - v)$, and adding $e$ to each matching of its convex combination gives one for $x$.

*Step 2: a tight nontrivial odd set exists.* By step 1 each vertex meets at least two edges, so $|E| \ge |V|$. If $|E| = |V|$, every vertex has degree 2 and $G$ is a disjoint union of cycles. On a cycle the degree equations force $x_e + x_{e'} = 1$ for consecutive edges, so $x$ alternates between some $a$ and $1 - a$. An odd cycle forces $a = \frac12$ and has $x(\delta(U)) = 0$ for its vertex set $U$, which is impossible; on an even cycle $x$ is $a$ times one perfect matching plus $1 - a$ times the other. Then $x$ is a convex combination of perfect matchings of $G$, a contradiction. So $|E| > |V|$. As a vertex of $Q(G)$, $x$ is the unique solution of $|E|$ linearly independent tight constraints. None is $x_e \ge 0$, and there are only $|V|$ degree equations, so some odd-set constraint $x(\delta(U)) = 1$ is tight with $U$ not a single vertex nor the complement of one, since those are degree equations, and $U \ne V$, since $x(\delta(V)) = 0$. So $3 \le |U| \le |V| - 3$.

*Step 3: contract both sides.* Let $G_1 = G / U$ be the graph with $U$ shrunk to one vertex $u^*$, keeping the edges of $\delta(U)$ and dropping $E[U]$, and $G_2 = G / (V \setminus U)$ with $V \setminus U$ shrunk to $w^*$. Let $x_1$ and $x_2$ be the restrictions of $x$ to their edges. Then $x_1 \in Q(G_1)$: the degree of $u^*$ is $x(\delta(U)) = 1$, and an odd set $W$ of $G_1$ that contains $u^*$ corresponds to the odd set $(W \setminus \{u^*\}) \cup U$ of $G$ with the same cut, since $|U|$ is odd. In the same way $x_2 \in Q(G_2)$. Both graphs are smaller than $G$, so by minimality, and since $x$ is rational, there is an integer $k$ and perfect matchings $M_1, \ldots, M_k$ of $G_1$ and $N_1, \ldots, N_k$ of $G_2$, repetitions allowed, with

$$x_1 = \tfrac1k \textstyle\sum_i \chi^{M_i}, \qquad x_2 = \tfrac1k \sum_i \chi^{N_i}.$$

Each $M_i$ contains exactly one edge of $\delta(U)$, the edge at $u^*$, and each edge $e \in \delta(U)$ lies in exactly $k x_e$ of the $M_i$; the same holds for the $N_i$. So the two lists can be renumbered so that $M_i$ and $N_i$ contain the same edge of $\delta(U)$. Then $M_i \cup N_i$ is a perfect matching of $G$: it covers $V \setminus U$ through $M_i$ and $U$ through $N_i$, and the shared edge of $\delta(U)$ is counted once. Now $x = \frac1k \sum_i \chi^{M_i \cup N_i}$, since each edge of $G$ lies in $E[U]$, in $E[V \setminus U]$ or in $\delta(U)$. This contradicts the choice of $G$. $\square$

**Proof of Theorem 2.** Every matching satisfies the constraints of $P(G)$, since a matching has at most $\frac{|U| - 1}{2}$ edges inside an odd set $U$. Conversely, let $x \in P(G)$. Build $\tilde G$ from two copies $G$ and $G'$ of the graph, with $v'$ the copy of $v$, and an edge $vv'$ for every $v \in V$. Define $\tilde x$ by $\tilde x_e = \tilde x_{e'} = x_e$ on both copies of each edge and $\tilde x_{vv'} = y_v = 1 - x(\delta(v)) \ge 0$. The degree equations of $\tilde G$ hold. Let $W = A \cup B'$ be an odd set of $\tilde G$, with $A, B \subseteq V$. Since $|A \setminus B| + |B \setminus A| \equiv |A| + |B|$ is odd, one of them is odd; by symmetry let $U = A \setminus B$ be odd. The cut $\delta(W)$ contains the edges $vv'$ for $v \in U$, the edges of $G$ from $U$ to $V \setminus A$, and the edges of $G'$ from $U'$ to $B'$. Since $(V \setminus A) \cup B = V \setminus U$, these give

$$\tilde x(\delta(W)) \ge \sum_{v \in U} y_v + x(\delta_G(U)) = |U| - 2x(E[U]) - x(\delta_G(U)) + x(\delta_G(U)) = |U| - 2x(E[U]) \ge 1,$$

using $\sum_{v \in U} x(\delta(v)) = 2x(E[U]) + x(\delta_G(U))$ and the odd-set constraint for $U$ (for $|U| = 1$, $E[U] = \emptyset$). So $\tilde x \in Q(\tilde G)$, and by Theorem 1 it is a convex combination of perfect matchings of $\tilde G$. Restricted to the edges of $G$, each of them is a matching of $G$, and the restricted combination is $x$. $\blacksquare$

## Consequences

- **Weighted matching is a linear program.** For any weights $w$, $\max \{ w^\top x : x \in P(G) \}$ is attained at a vertex, which is a matching. This is the base of Edmonds' primal-dual algorithms for [maximum weight matching](/maximum-weight-matching/) and [minimum-weight perfect matching](/minimum-weight-perfect-matching/), whose dual variables live on the vertices and on the odd sets that are current [blossoms](/blossom/). The algorithm itself was Edmonds' first proof.
- **Duality.** [LP duality](/lp-duality/) gives a min-max formula for the maximum weight of a matching. Cunningham and Marsh showed the system is [totally dual integral](/totally-dual-integrality/), so for integer weights the dual has an integer optimum; for unit weights this is the [Tutte-Berge formula](/tutte-berge-formula/).
- **Petersen's theorem, and more.** Let $G$ be cubic and bridgeless, and $x = \frac13$ on every edge. Each $v$ has $x(\delta(v)) = 1$. For odd $U$, $3|U| = 2|E[U]| + |\delta(U)|$, so $|\delta(U)|$ is odd; it is not 1 as $G$ has no bridge, so $|\delta(U)| \ge 3$ and $x(\delta(U)) \ge 1$. So $x \in Q(G)$: $G$ has a perfect matching, which is [Petersen's theorem](/petersens-theorem/), and since $x_e > 0$ every edge lies in some perfect matching.
- **Fractional edge colouring.** The fractional chromatic index, the least total weight of matchings covering every edge with weight 1, equals $\max \bigl( \Delta(G), \max_U \frac{2|E[U]|}{|U| - 1} \bigr)$ over odd $U$ with $|U| \ge 3$, by LP duality over $P(G)$. This bounds [edge colouring](/edge-coloring/) from below.
- **Separation and the ellipsoid method.** Padberg and Rao showed that a violated odd-set constraint can be found with a minimum odd cut, computable from a [Gomory-Hu tree](/gomory-hu-tree/). With a [separation oracle](/separation-oracle/), the [ellipsoid method](/ellipsoid-method/) optimizes over $P(G)$ in polynomial time without the combinatorial algorithm.

## Tightness

- **The odd-set constraints are needed.** The triangle shows that degree constraints alone allow fractional vertices; by half-integrality, the vertices of the fractional matching polytope that are not matchings carry $\frac12$ on disjoint odd cycles, and odd-set constraints cut each of them off.
- **Only odd sets.** For an even set $U$, the bound $x(E[U]) \le \frac{|U|}{2}$ follows from the degree constraints, so even sets add nothing.
- **Many constraints are facets.** Edmonds and Pulleyblank showed that the odd-set constraint of $U$ defines a facet of $P(G)$ when $G[U]$ is factor-critical and 2-connected, so in general no fixed polynomial subfamily suffices. In the complete graph $K_n$ every odd set with $|U| \ge 3$ gives a facet.
- **No compact extended formulation.** Rothvoss proved in 2014 that every polytope that projects onto the perfect matching polytope of $K_n$ has $2^{\Omega(n)}$ facets, so extra variables do not help either, although weighted matching is solvable in polynomial time.
- **Perfect matching version.** The equalities cannot be relaxed to $x(\delta(v)) \le 1$ in Theorem 1: then $x = 0$ would be in the set, and it is not a convex combination of perfect matchings when $V \ne \emptyset$.

## History

Jack Edmonds stated and proved the theorem in 1965, in a companion paper to "Paths, trees, and flowers", which gave the cardinality algorithm; his proof is algorithmic, through the weighted blossom algorithm and its dual solution. It was the first complete linear description of a polytope for a combinatorial problem beyond bipartite matching and network flows, and it started polyhedral combinatorics. Shorter non-algorithmic proofs followed, among them the contraction proof above, which appears in Schrijver's book; Cunningham and Marsh proved total dual integrality in 1978, and Rothvoss settled the extension complexity in 2014.

## References
