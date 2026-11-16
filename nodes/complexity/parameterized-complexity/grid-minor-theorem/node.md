---
tag: 97F3FM
kind: theorem
slug: grid-minor-theorem
name: Grid minor theorem
aliases:
- Robertson-Seymour grid theorem
area: complexity/parameterized-complexity
level: research
summary: "Every graph of treewidth at least g(t) has the t x t grid as a minor. The best general g is polynomial in t, and on planar graphs g(t) = 9t/2 is enough."
prereqs: [treewidth, tree-decomposition, graph-minor]
see_also: [graph-minor-theorem, courcelle-theorem, bidimensionality-theory, irrelevant-vertex-technique, minor-testing, meta-theorems, planar-separator-theorem, menger-theorem]
sources:
  - paper: doi:10.1016/0095-8956(86)90030-4
    title: "Neil Robertson and Paul D. Seymour, Graph minors. V. Excluding a planar graph, Journal of Combinatorial Theory, Series B 41(1), 92-114 (1986)"
    locator: the main theorem, a minor-closed class has bounded treewidth if and only if it excludes some planar graph, through large grid minors
  - paper: doi:10.1006/jctb.1994.1073
    title: "Neil Robertson, Paul D. Seymour and Robin Thomas, Quickly excluding a planar graph, Journal of Combinatorial Theory, Series B 62(2), 323-348 (1994)"
    locator: "the explicit bound g(t) = 2^O(t^5), the lower bound of order t^2 log t, and the linear bound for planar graphs"
  - paper: doi:10.1145/2820609
    title: "Chandra Chekuri and Julia Chuzhoy, Polynomial bounds for the grid-minor theorem, Journal of the ACM 63(5), article 40 (2016)"
    locator: "the main theorem, g(t) = O(t^98 polylog t), with a randomized polynomial-time algorithm that finds the grid minor (conference version STOC 2014)"
  - paper: doi:10.1016/j.jctb.2020.09.010
    title: "Julia Chuzhoy and Zihan Tan, Towards tight(er) bounds for the excluded grid theorem, Journal of Combinatorial Theory, Series B 146, 219-265 (2021)"
    locator: "the main theorem, g(t) = O(t^9 polylog t) (conference version SODA 2019)"
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.7.1, Grid theorems (the treewidth of the grid, the general and planar bounds, the planar algorithm, and cycle packing as a win/win example)"
---

The grid minor theorem says that a graph has large [treewidth](/treewidth/) only if it contains a large grid as a [minor](/graph-minor/). Robertson and Seymour proved it in 1986 in Graph Minors V, with no explicit bound. Chekuri and Chuzhoy showed in 2014 that the bound is polynomial, and on planar graphs it is linear. The theorem is the large-treewidth half of most win/win arguments in parameterized algorithms. The easy direction is proved in full below, and the hard direction is given as a sketch.

## Statement

The $t \times t$ grid $\boxplus_t$ has the vertex set $\{1, \dots, t\} \times \{1, \dots, t\}$, and two vertices are adjacent when they differ by 1 in exactly one coordinate. A graph $H$ is a minor of $G$ if $H$ can be obtained from a subgraph of $G$ by edge contractions. Equivalently, there are disjoint connected vertex sets $B_h \subseteq V(G)$, one for each $h \in V(H)$ (the *branch sets*), such that for each edge $hh'$ of $H$ some edge of $G$ joins $B_h$ and $B_{h'}$.

**Theorem (Robertson and Seymour 1986).** There is a function $g$ such that for every $t \ge 1$, every graph of treewidth at least $g(t)$ contains $\boxplus_t$ as a minor.

**Converse (easy direction).** If $G$ contains $\boxplus_t$ as a minor, then $\mathrm{tw}(G) \ge \mathrm{tw}(\boxplus_t) = t$.

The known bounds on the smallest $g$:

| graphs | upper bound on $g(t)$ | source |
|---|---|---|
| all | exists, no explicit bound | Robertson and Seymour 1986 |
| all | $2^{O(t^5)}$ | Robertson, Seymour and Thomas 1994 |
| all | $O(t^{98} \operatorname{polylog} t)$ | Chekuri and Chuzhoy 2016 |
| all | $O(t^9 \operatorname{polylog} t)$ | Chuzhoy and Tan 2021 |
| planar | $9t/2$ | Gu and Tamaki, as stated in Cygan et al., Section 7.7.1 |

For general graphs, $g(t)$ must be $\Omega(t^2 \log t)$ (Robertson, Seymour and Thomas 1994). The parameter of the theorem is $t$. The theorem is a statement about graphs, not about an algorithm, but each bound above comes with an algorithm. On planar graphs, an $O(n^2)$ algorithm returns either a tree decomposition of width at most $(9/2 + \varepsilon) t$ or a minor model of $\boxplus_t$. For general graphs, the proof of Chekuri and Chuzhoy gives a randomized polynomial-time algorithm that finds the grid minor.

## In plain words

Treewidth measures how far a graph is from a tree. A square grid is the standard example of a graph that is far from a tree: a 10 by 10 grid has treewidth 10. The theorem says the reverse is also true in a weak form. If a graph is very far from a tree, then a large grid is hidden in it. You find the grid by deleting some vertices and edges and by merging connected groups of vertices into single vertices. The size of the hidden grid grows with the treewidth, but more slowly. For maps drawn in the plane, the grid side is a fixed fraction of the treewidth. For general graphs the best known link is a polynomial of degree about 9.

## Proof

The easy direction has two parts: treewidth does not grow when you take a minor, and the grid has large treewidth. The hard direction is a sketch.

### Treewidth does not grow under minors

Let $(T, \{X_x\})$ be a tree decomposition of $G$ of width $w$. Deleting a vertex $v$ from every bag, or deleting an edge, keeps the three conditions of a tree decomposition. Contracting an edge $uv$ into a new vertex $z$: replace $u$ and $v$ by $z$ in every bag. Each edge of the new graph is still inside some bag, because each edge at $z$ came from an edge at $u$ or at $v$. The bags that hold $z$ are the bags that held $u$ or $v$. These two subtrees are connected and they meet in a bag that holds the edge $uv$, so their union is a subtree. No bag grows. So the width stays at most $w$, and by induction on the number of operations $\mathrm{tw}(H) \le \mathrm{tw}(G)$ for every minor $H$ of $G$.

### The grid has treewidth at least t - 1

A *bramble* is a family of connected vertex sets that pairwise touch: two sets touch if they share a vertex or an edge joins them. Its *order* is the least size of a vertex set that meets every member.

*Lemma.* If $G$ has a bramble of order $p$, then every tree decomposition of $G$ has a bag of size at least $p$, so $\mathrm{tw}(G) \ge p - 1$.

*Proof.* Let $\mathcal{B}$ be the bramble and $(T, \{X_x\})$ a tree decomposition. For an edge $xy$ of $T$, the set $S = X_x \cap X_y$ separates the vertices of the bags on the $x$ side from those on the $y$ side. If $S$ meets every member of $\mathcal{B}$, then $|X_x| \ge |S| \ge p$ and we are done. Otherwise each member that $S$ misses is connected, so it lies on one side. Two such members on different sides could not touch, so they all lie on the same side. Point the edge $xy$ to that side. A tree has fewer edges than nodes, so some node $x$ has no edge pointing away from it. Suppose a member $C$ misses $X_x$. The bags that meet $C$ form a subtree, since $C$ is connected, and this subtree avoids $x$. So it lies behind one neighbor $y$ of $x$, and $C$ misses $X_x \cap X_y$. Then the edge $xy$ points to $y$, which is a contradiction. So $X_x$ meets every member and $|X_x| \ge p$. $\square$

In $\boxplus_t$, let the *cross* $C_{ij}$ be the union of row $i$ and column $j$. Each cross is connected, and two crosses $C_{ij}$ and $C_{i'j'}$ share the vertex $(i, j')$. A set of at most $t - 1$ vertices misses some row $i$ and some column $j$, so it misses $C_{ij}$. The crosses form a bramble of order at least $t$, so $\mathrm{tw}(\boxplus_t) \ge t - 1$. The exact value $\mathrm{tw}(\boxplus_t) = t$ needs a finer bramble (Cygan et al., Section 7.7.1). An exact treewidth computation by dynamic programming over vertex subsets gives 2, 3 and 4 for $t = 2, 3, 4$, and 3 for the 3 by 5 grid. So a graph with a $\boxplus_t$ minor has treewidth at least $t$.

### The hard direction (sketch)

The known proofs share an outline. The details differ from paper to paper and are left out here.

1. **A well-linked set.** If $\mathrm{tw}(G) \ge k$, then $G$ has a vertex set $W$ of size about $k$ that no small separator splits into two large parts. This step uses the duality between treewidth and brambles. Its proof is left out.
2. **Two families of disjoint paths.** By [Menger's theorem](/menger-theorem/), $W$ gives many vertex-disjoint paths between any two disjoint parts of $W$ of the same size. The proof builds a family of "horizontal" paths and a family of "vertical" paths such that each horizontal path meets many vertical paths.
3. **Cleaning.** Ramsey-type arguments and rerouting choose subfamilies whose intersections follow the grid pattern. Contracting the segments of the paths then gives $\boxplus_t$. This step is where the exponential bound $2^{O(t^5)}$ of Robertson, Seymour and Thomas comes from. Chekuri and Chuzhoy replace it with a chain of well-linked clusters (a "path-of-sets system"), and this gives the polynomial bound. These arguments are left out.

### Worked example

The Petersen graph has 10 vertices and treewidth 4 (exact computation). It has $\boxplus_3$ as a minor, and a search over branch-set labelings finds one. The minor needs a contraction: the Petersen graph is 3-regular, so it has no subgraph isomorphic to $\boxplus_3$, whose center has degree 4. It has no $\boxplus_4$ minor, because $\boxplus_4$ has 16 vertices. So treewidth 4 does not force a $4 \times 4$ grid, and $g(4) \ge 5$.

## Consequences

- **Excluding a planar graph.** Every planar graph is a minor of a large enough grid. So for every planar $H$, the graphs with no $H$ minor have treewidth bounded by a function of $H$. Robertson and Seymour proved that a minor-closed class has bounded treewidth if and only if it excludes some planar graph. This is a key step of the [graph minor theorem](/graph-minor-theorem/).
- **Win/win algorithms.** To decide a problem with parameter $k$, compute the treewidth. If it is small, use [Courcelle's theorem](/courcelle-theorem/) or a [dynamic program on a tree decomposition](/dp-on-tree-decompositions/). If it is large, the grid minor gives the answer directly. Cygan et al., Section 7.7.1, use this to show that cycle packing is FPT.
- **Subexponential algorithms on planar graphs.** With the linear planar bound, [bidimensionality theory](/bidimensionality-theory/) gives $2^{O(\sqrt{k})} n^{O(1)}$ algorithms for many planar problems.
- **Irrelevant vertices.** A large grid with no other structure contains vertices that no small solution needs. This is the base of the [irrelevant vertex technique](/irrelevant-vertex-technique/) used for [minor testing](/minor-testing/) and [disjoint paths](/parameterized-disjoint-paths/).
- **Planar treewidth.** From the planar bound, Cygan et al. derive that an $n$-vertex planar graph has treewidth less than $\frac{9}{2} \lceil \sqrt{n + 1} \rceil$. The [planar separator theorem](/planar-separator-theorem/) gives a bound of the same order by a different route.

## Tightness

- **Lower bound for general graphs.** Robertson, Seymour and Thomas showed that $g(t) = \Omega(t^2 \log t)$. So no linear bound holds for all graphs, and the gap to $O(t^9 \operatorname{polylog} t)$ is open.
- **Planar graphs.** The planar bound is linear, and it cannot be smaller than $t$: the grid $\boxplus_{t-1}$ is planar, has treewidth $t - 1$, and has too few vertices to contain $\boxplus_t$.
- **Minors, not topological minors.** The theorem gives a grid as a minor, not as a subdivision. The grid has vertices of degree 4, so a minor model of the grid need not give a subdivision of it. Because the wall (a grid with alternate vertical edges removed) has maximum degree 3, a large grid minor does give a large wall as a topological minor.
- **Constructive.** Unlike the graph minor theorem, the grid minor theorem is constructive: the known proofs give algorithms that find the grid minor.

## History

Robertson and Seymour proved the theorem in Graph Minors V (1986) as part of the proof of the graph minor theorem. Robertson, Seymour and Thomas (1994) gave the first explicit bound, $2^{O(t^5)}$, the lower bound $\Omega(t^2 \log t)$, and the linear bound $6t$ for planar graphs. Gu and Tamaki improved the planar constant to $9/2$. Chekuri and Chuzhoy (STOC 2014, JACM 2016) proved the first polynomial bound. Later work lowered the exponent through $t^{36}$ and $t^{19}$ to $O(t^9 \operatorname{polylog} t)$ (Chuzhoy and Tan, SODA 2019, JCTB 2021).

## References
