---
tag: VZDP45
kind: concept
slug: fractional-matching
name: Fractional matching
aliases:
- fractional perfect matching
area: graphs/matching
level: advanced
summary: Edge weights in [0,1] whose sum at each vertex is at most one; a linear-programming relaxation of matching.
prereqs: [bipartite-matching, lp-duality]
see_also: [edmonds-polytope-theorem, matching-polytope, total-unimodularity, lp-relaxation, vertex-cover, bipartite-double-cover, b-matching, tutte-berge-formula]
sources:
  - book: isbn:9780486485935
    title: Edward R. Scheinerman and Daniel H. Ullman, Fractional Graph Theory, Dover (2011 reprint of the 1997 edition)
    locator: Chapter 2, Fractional matching (half-integrality, the fractional Tutte theorem and the fractional matching number)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 18.1, The matching and the perfect matching polytope (bipartite case), and Chapter 30, 2-matchings, 2-covers, and 2-factors (the half-integral relaxation in general graphs)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 7, Matching and linear programming (fractional matchings and fractional vertex covers)
---

A fractional matching of a [graph](/graph/) puts a weight $x_e \ge 0$ on each edge so that the weights at every vertex sum to at most one. Ordinary matchings are the fractional matchings with weights 0 and 1, so the largest total weight $\nu_f(G)$ is at least the matching number $\nu(G)$. It is the [linear programming relaxation](/lp-relaxation/) of [maximum matching](/maximum-matching/): exact in [bipartite graphs](/bipartite-graph/), where $\nu_f = \nu$, and off by at most a factor $3/2$ in general graphs, where odd cycles can carry half weights. The definition is for graphs without edge weights; the weighted version maximizes $\sum_e w_e x_e$ over the same set.

## In plain words

A matching chooses some links of a network so that no point touches two chosen links. A fractional matching may choose part of a link: half of one link and half of another at the same point is allowed, as long as the parts at each point add up to at most one whole.

In a two-sided network splitting never helps: the best fractional choice is as large as the best ordinary one. In a triangle it does help. An ordinary matching takes one of the three links, but half of each link gives one and a half. The gap is the reason general matching needs more than linear programming with these simple constraints.

## The idea

**Definition.** Let $G = (V, E)$ be a finite undirected graph and $\delta(v)$ the set of edges at $v$. A vector $x \in \mathbb{R}^E$ is a *fractional matching* if

$$x_e \ge 0 \;\; (e \in E), \qquad x(\delta(v)) = \sum_{e \in \delta(v)} x_e \le 1 \;\; (v \in V).$$

Then $x_e \le 1$ follows. It is a *fractional perfect matching* if $x(\delta(v)) = 1$ for every $v$. Its size is $x(E) = \sum_e x_e$, and the *fractional matching number* is $\nu_f(G) = \max x(E)$. The set of fractional matchings is the *fractional matching polytope*; its integer points are the incidence vectors of matchings.

**Duality.** By [LP duality](/lp-duality/), $\nu_f(G)$ equals the minimum of $\sum_v y_v$ over $y \ge 0$ with $y_u + y_v \ge 1$ for every edge $uv$: a fractional [vertex cover](/vertex-cover/). With $\tau(G)$ the size of a smallest vertex cover,

$$\nu(G) \le \nu_f(G) = \tau_f(G) \le \tau(G).$$

**Bipartite graphs.** The constraint matrix is the vertex-edge incidence matrix of $G$. If $G$ is bipartite, this matrix is [totally unimodular](/total-unimodularity/), so every vertex of the polytope is integral and is a matching. Then all four numbers above are equal, which is [Kőnig's theorem](/konig-theorem/) read as LP duality. A fractional perfect matching of $K_{n,n}$ is a doubly stochastic matrix, and integrality is the Birkhoff and von Neumann theorem.

**General graphs: half-integrality.** Every vertex $x$ of the fractional matching polytope has entries in $\{0, \tfrac12, 1\}$; the edges with $x_e = 1$ form a matching, and the edges with $x_e = \tfrac12$ form vertex-disjoint odd cycles (Balinski). To see why, let $x$ be a vertex and $F = \{ e : 0 < x_e < 1 \}$. If $F$ contained an even cycle, or two odd cycles joined by a path, or a path whose ends are not saturated, adding $\pm\varepsilon$ alternately along it would write $x$ as the midpoint of two fractional matchings. So each component of $F$ is an odd cycle whose vertices are saturated by $F$, and then the equations $x_{e} + x_{e'} = 1$ around the cycle force $x_e = \tfrac12$.

**Consequences of half-integrality.**

- $\nu(G) \le \nu_f(G) \le \tfrac32 \nu(G)$. Take a half-integral optimum: an odd cycle of length $2k + 1$ carries $\tfrac{2k+1}{2} \le \tfrac32 k$ and contains a matching of $k$ edges. Disjoint triangles attain $\tfrac32$.
- $2\nu_f(G)$ is an integer: it is the largest size of a *2-matching*, an assignment of $0, 1, 2$ to edges with sum at most 2 at each vertex.
- *Fractional Tutte-Berge formula.* With $i(G - S)$ the number of isolated vertices of $G - S$,
  $$\nu_f(G) = \tfrac12 \Bigl( n - \max_{S \subseteq V} \bigl( i(G - S) - |S| \bigr) \Bigr).$$
  In particular $G$ has a fractional perfect matching if and only if $i(G - S) \le |S|$ for every $S$, the analogue of Tutte's condition with isolated vertices in place of odd components, and equivalently if and only if $G$ has a spanning subgraph whose components are single edges and odd cycles.
- *Odd-set constraints.* An odd set $U$ with $|U| = 2k + 1$ spans at most $k$ edges of any matching, but the triangle with $x \equiv \tfrac12$ has $x(E(U)) = \tfrac32 > 1$. Adding the constraints $x(E(U)) \le \lfloor |U|/2 \rfloor$ for every odd $U$ removes all fractional vertices: this is [Edmonds' matching polytope theorem](/edmonds-polytope-theorem/).

**Computing $\nu_f$.** Let $B(G)$ be the [bipartite double cover](/bipartite-double-cover/), with vertices $v'$ and $v''$ for each $v$ and edges $u'v''$ and $v'u''$ for each edge $uv$. A fractional matching $x$ of $G$ gives one of $B(G)$ of twice the size, by copying $x_{uv}$ to both copies of $uv$; conversely, averaging the two copies turns a matching of $B(G)$ into a fractional matching of $G$ of half the size. So $\nu_f(G) = \tfrac12 \nu(B(G))$, and a [Hopcroft-Karp](/hopcroft-karp/) run on $B(G)$ computes it in $O(m\sqrt n)$ time; averaging the two copies of a maximum matching of $B(G)$ gives an optimal fractional matching with entries in $\{0, \tfrac12, 1\}$.

## Examples

| graph | $\nu$ | $\nu_f$ | an optimal fractional matching |
|---|---|---|---|
| no edges | 0 | 0 | the empty vector |
| triangle $K_3$ | 1 | $\tfrac32$ | $\tfrac12$ on each edge |
| odd cycle $C_5$ | 2 | $\tfrac52$ | $\tfrac12$ on each edge |
| even cycle $C_6$ | 3 | 3 | a perfect matching, or $\tfrac12$ on each edge |
| star $K_{1,3}$ | 1 | 1 | 1 on one edge, or $\tfrac13$ on each |
| path $P_3$ | 1 | 1 | 1 on one edge |
| $K_4$ | 2 | 2 | a perfect matching |
| two disjoint triangles | 2 | 3 | $\tfrac12$ on all six edges |

**Not a vertex.** In $C_6$ the all-$\tfrac12$ vector is optimal but is not a vertex of the polytope: it is the average of the two perfect matchings. Half-integrality says that vertices carry halves only on odd cycles.

**No fractional perfect matching.** The star $K_{1,3}$ with $S$ the centre has $i(G - S) = 3 > 1 = |S|$, so it has no fractional perfect matching, and $\nu_f = \tfrac12 (4 - 2) = 1$. The triangle has a fractional perfect matching but no perfect matching, since it has an odd number of vertices.

**The gap in a bipartite graph.** For the bipartite graph $K_{2,3}$, $\nu = \nu_f = \tau = 2$, as total unimodularity predicts; the fractional vertex cover puts 1 on each vertex of the smaller side.

## Where it is used

- **LP methods for matching.** The fractional matching polytope is the starting point of the polyhedral theory of matching: it is the [matching polytope](/matching-polytope/) for bipartite graphs, and the odd-set constraints that close the gap in general graphs are the dual variables of the weighted blossom algorithm for [maximum weight matching](/maximum-weight-matching/).
- **Approximation.** The bound $\nu_f \le \tfrac32 \nu$ and the relation to fractional vertex cover underlie [LP rounding](/linear-programming-rounding/) for vertex cover; half-integrality of the fractional vertex cover gives the Nemhauser and Trotter reduction used in [LP-based kernelization](/lp-kernelization/).
- **Online and distributed matching.** Algorithms for [online bipartite matching](/online-bipartite-matching/), such as water-filling, and many distributed and streaming algorithms first maintain a fractional matching and then round it.
- **Assignment and economics.** Fractional perfect matchings of $K_{n,n}$ are doubly stochastic matrices; a [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) writes one as a lottery over perfect matchings, as in randomized assignment and switch scheduling.
- **Generalizations.** Fractional [b-matching](/b-matching/) replaces the bound 1 at $v$ by $b_v$; the fractional edge colouring number is the dual of a fractional matching problem.

## References
