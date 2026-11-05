---
tag: 6WFP89
kind: concept
slug: spanning-tree-polytope
name: Spanning tree polytope
area: graphs/spanning-trees
level: advanced
summary: The convex hull of the incidence vectors of spanning trees, described by subtour-style inequalities.
prereqs: [spanning-tree, convex-polytope, linear-programming-problem, minimum-spanning-tree]
see_also: [graphic-matroid, rado-edmonds-theorem, subtour-elimination-lp, held-karp-bound, separation-oracle, lp-duality, nash-williams-tutte-theorem, uniform-spanning-tree-sampling]
sources:
  - paper: doi:10.1007/BF01584082
    title: Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1 (1971), 127-136
    locator: the description of the polytope of independent sets and of bases of a matroid, and the proof by the greedy algorithm
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer (2018)
    locator: Chapter 6, Spanning Trees and Arborescences (the section on polyhedral descriptions of the spanning tree polytope)
---

The spanning tree polytope of a connected graph is the convex hull of the incidence vectors of its spanning trees, a polytope in $\mathbb{R}^E$ with one vertex for each spanning tree. Edmonds (1971) showed that it is exactly the set of nonnegative vectors whose total is $n - 1$ and that put at most $|S| - 1$ on the edges inside each vertex set $S$. So the [minimum spanning tree](/minimum-spanning-tree/) problem is a [linear program](/linear-programming-problem/) whose optimal vertices are always trees, even though the description has exponentially many inequalities. The polytope is the base polytope of the [graphic matroid](/graphic-matroid/), and it is a tool in TSP approximation, tree packing and network design.

## In plain words

Write a spanning tree as a list of zeros and ones, one entry for each link of the network: one if the tree uses the link, zero if not. Each tree is then a point in a space with one direction for each link. Fill in the shape spanned by all these points. That shape is the spanning tree polytope.

A point inside the shape is a "fractional tree": a weighted mix of trees. A short list of rules tells exactly which points are inside: the entries add up to one less than the number of points of the network, and no group of points gets more than one less than its size on the links inside the group. These rules say nothing about whole numbers, yet the corners of the shape are exactly the trees. That is why a cheapest tree can be found as a linear program.

## The idea

**Definition.** Let $G = (V, E)$ be a finite undirected graph with $n$ vertices and $m$ edges. For $F \subseteq E$, its *incidence vector* $\chi^F \in \{0, 1\}^E$ has $\chi^F_e = 1$ if and only if $e \in F$. The spanning tree polytope is

$$P_{\text{tree}}(G) = \operatorname{conv} \{ \chi^T : T \text{ a spanning tree of } G \}.$$

For $x \in \mathbb{R}^E$ and $F \subseteq E$ write $x(F) = \sum_{e \in F} x_e$, and for $S \subseteq V$ let $E(S)$ be the set of edges with both ends in $S$.

**Connectivity.** If $G$ is not connected, it has no spanning tree and $P_{\text{tree}}(G)$ is empty. The *forest polytope*, the convex hull of all forests, is never empty, and its maximal faces of the form $x(E) = n - c$, with $c$ the number of components, are the spanning forest polytopes. Self-loops are in no tree, so their coordinates are 0. Parallel edges are different coordinates.

**Edmonds' theorem.** For a connected graph $G$,

$$P_{\text{tree}}(G) = \Big\{ x \in \mathbb{R}^E :\ x \ge 0,\ \ x(E) = n - 1,\ \ x(E(S)) \le |S| - 1 \text{ for each nonempty } S \subseteq V \Big\}.$$

Each $\chi^T$ satisfies the inequalities: a tree has $n - 1$ edges, and its edges inside $S$ form a forest on $S$, with at most $|S| - 1$ edges. The hard direction is that every point of the right side is a mix of trees, that is, that every vertex of the right side is integral. The constraints for sets $S$ are *subtour-style*: they are the same as the constraints of the [subtour elimination LP](/subtour-elimination-lp/) for the TSP, which forbid the solution from closing a cycle inside $S$.

**Why the vertices are trees: the greedy proof.** It is enough to show that for every weight vector $w$, the linear program $\min \{ w^\top x : x \text{ in the right side} \}$ has an optimal solution $\chi^T$ with $T$ a spanning tree. Sort the edges as $w(e_1) \le \cdots \le w(e_m)$ and let $T$ be the tree of [Kruskal's algorithm](/kruskal/). For each $i$, let $\mathcal{P}_i$ be the components of $(V, \{e_1, \ldots, e_i\})$. The dual of the LP has a variable for each set $S$, and a dual solution built from the components $\mathcal{P}_i$, with values set by the gaps $w(e_{i+1}) - w(e_i)$, is feasible and has the same objective value as $\chi^T$. So $\chi^T$ is optimal by [LP duality](/lp-duality/). Since each weight vector has an optimal tree, each vertex of the right side is a tree. Edmonds proved this for the bases of any matroid; it is the polyhedral form of the [Rado-Edmonds theorem](/rado-edmonds-theorem/) that the greedy algorithm works on matroids.

**Ties.** With ties in $w$, the optimal face of the LP is the convex hull of all MSTs, which is larger than one vertex. With distinct weights, the optimal face is the single vertex $\chi^T$ of the unique MST.

**A form with partitions.** An equivalent description replaces the sets $S$ by partitions. For each partition $\mathcal{P}$ of $V$ into nonempty parts, let $\delta(\mathcal{P})$ be the set of edges between different parts. Then $P_{\text{tree}}(G) = \{ x \ge 0 : x(E) = n - 1,\ x(\delta(\mathcal{P})) \ge |\mathcal{P}| - 1 \text{ for each partition } \mathcal{P} \}$. This form says that the tree must connect the parts of every partition.

**Size and separation.** The description has $2^n - 1$ set constraints, but a [separation oracle](/separation-oracle/) runs in polynomial time: given $x$, find the set $S$ that maximizes $x(E(S)) - |S|$, which reduces to a polynomial number of [minimum cut](/min-cut-problem/) computations. So the [ellipsoid method](/ellipsoid-method/) can optimize over the polytope. There are also extended formulations with a polynomial number of variables and constraints, such as Martin's (1991), whose projection onto $\mathbb{R}^E$ is the polytope.

**Faces and edges.** Each vertex is a tree. Two vertices $\chi^T$ and $\chi^{T'}$ are joined by an edge of the polytope exactly when $T' = T - f + e$ for one exchange. This is a property of every matroid base polytope.

## Examples

**A triangle.** With edges $x, y, z$, the three trees give the points $(1, 1, 0)$, $(1, 0, 1)$ and $(0, 1, 1)$, and the polytope is the triangle that they span. It lies in the plane $x + y + z = 2$, with $0 \le x, y, z \le 1$. The constraint for $S = V$ is $x + y + z \le 2$, and for a pair $S = \{u, v\}$ it is $x_{uv} \le 1$. The point $(2/3, 2/3, 2/3)$, the average of the three trees, is in the polytope.

**A cycle.** In the cycle $C_4$ with edges $e_1, \ldots, e_4$, each tree leaves out one edge, so the four vertices are $(0, 1, 1, 1)$, $(1, 0, 1, 1)$, $(1, 1, 0, 1)$ and $(1, 1, 1, 0)$. Their average $(3/4, 3/4, 3/4, 3/4)$ is in the polytope, and so is $(1, 1, 1/2, 1/2)$, the average of the trees that leave out $e_3$ and $e_4$. The point $(1, 1, 1, 1)$ has total $4 > n - 1 = 3$, so it is not.

**A point that fails a set constraint.** Take two triangles $abc$ and $def$ joined by one edge $cd$, so $n = 6$. The point with $1$ on each of the six triangle edges and $0$ on $cd$ has total $6 \ne 5$. Lower it to $5/6$ on each triangle edge: the total is now 5, but the set $S = \{a, b, c\}$ has $x(E(S)) = 5/2 > 2 = |S| - 1$. So the point is not in the polytope; indeed every tree must use the [bridge](/bridge/) $cd$, and the partition form shows it: for $\mathcal{P} = \{\{a, b, c\}, \{d, e, f\}\}$ it requires $x_{cd} \ge 1$.

**Uniform tree marginals.** For a random spanning tree $T$ with any law, the vector $(\Pr[e \in T])_{e \in E}$ is a mix of trees, so it is in the polytope. For the [uniform spanning tree](/uniform-spanning-tree-sampling/) of the graph on $a$ to $f$ with the edges $ab, ac, bc, bd, cd, ce, de, df, ef$, it is

$$\tfrac{1}{55}\,(34, 34, 26, 31, 25, 31, 26, 34, 34),$$

whose total is $275/55 = 5 = n - 1$.

**Minimum weight.** With the weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$ on the same graph, the LP minimum over the polytope is 13, attained only at the vertex of the MST $\{ac, bc, bd, ce, ef\}$. The point of the uniform marginals has weight $\frac{1}{55}(34 \cdot 4 + 34 \cdot 3 + 26 + 31 \cdot 2 + 25 \cdot 4 + 31 \cdot 5 + 26 \cdot 7 + 34 \cdot 6 + 34 \cdot 2)$, which is $1035/55 = 207/11 \approx 18.8$, the mean weight of a uniform random tree, larger than 13.

## Where it is used

- **MST as a linear program.** The polytope shows that the MST problem is an LP, and Kruskal's algorithm is a primal-dual method for it. This is the model case of matroid optimization.
- **The Held-Karp bound for the TSP.** The [Held-Karp bound](/held-karp-bound/) uses 1-trees, spanning trees with one extra vertex, and Lagrangian weights; it equals the value of the subtour LP, whose feasible points, after scaling, lie in the spanning tree polytope.
- **TSP approximation.** The best approximation algorithms for asymmetric and symmetric TSP write a solution of the subtour LP as a point of the spanning tree polytope and sample a random tree with these marginals, then fix the degrees.
- **Tree packing.** The fractional number of disjoint spanning trees that fit in a graph is the largest $k$ such that $\mathbf{1}/k$ is above some point of the polytope. It equals $\min_{\mathcal{P}} |\delta(\mathcal{P})| / (|\mathcal{P}| - 1)$, the fractional form of the [Nash-Williams-Tutte theorem](/nash-williams-tutte-theorem/).
- **Constrained spanning trees.** For trees with degree bounds or other side constraints, an LP over the polytope with extra constraints gives lower bounds and the basis of rounding methods.
- **Graph strength and attack problems.** The partition form measures how many edges an attacker must cut to split the graph into many parts.

## References
