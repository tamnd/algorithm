---
tag: X70A8S
kind: theorem
slug: nash-williams-tutte-theorem
name: Nash-Williams-Tutte theorem
aliases:
- tree packing theorem
- Tutte-Nash-Williams theorem
area: graphs/spanning-trees
level: advanced
summary: A graph has k edge-disjoint spanning trees iff every vertex partition has at least k(p-1) crossing edges.
prereqs: [spanning-tree, graphic-matroid, edge-connectivity, cut]
see_also: [spanning-tree-packing, nash-williams-arboricity-theorem, arboricity, spanning-tree-polytope, k-edge-connected-graph, matroid, menger-theorem, matroid-intersection-theorem]
sources:
  - paper: doi:10.1112/jlms/s1-36.1.445
    title: C. St. J. A. Nash-Williams, Edge-disjoint spanning trees of finite graphs, Journal of the London Mathematical Society 36 (1961), 445-450
    locator: the main theorem
  - paper: doi:10.1112/jlms/s1-36.1.221
    title: W. T. Tutte, On the problem of decomposing a graph into n connected factors, Journal of the London Mathematical Society 36 (1961), 221-230
    locator: the main theorem
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer Graduate Texts in Mathematics 173 (2017)
    locator: Chapter 2, Section 2.4, Tree-packing and arboricity (the tree-packing theorem with a graph-theoretic proof, and the corollary for 2k-edge-connected graphs)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer (2018)
    locator: Chapter 13, Matroids (the matroid union theorem) and Chapter 6, Spanning Trees and Arborescences (packing spanning trees)
---

The Nash-Williams-Tutte theorem says when a graph contains $k$ pairwise edge-disjoint [spanning trees](/spanning-tree/): exactly when, for every partition of the vertices into $p$ parts, at least $k(p - 1)$ edges join different parts. The condition is clearly necessary, since each spanning tree must use at least $p - 1$ edges between the parts, and the theorem says that it is also sufficient. Nash-Williams and Tutte proved it independently in 1961. A direct consequence is that every $2k$-edge-connected graph has $k$ edge-disjoint spanning trees.

## Statement

Let $G = (V, E)$ be a finite undirected multigraph with $n \ge 1$ vertices. Parallel edges are allowed and count as different edges; self-loops are allowed and play no role. For a partition $\mathcal{P}$ of $V$ into nonempty parts, let $\delta(\mathcal{P})$ be the set of edges whose ends lie in different parts, and let $|\mathcal{P}|$ be the number of parts.

**Theorem (Nash-Williams 1961, Tutte 1961).** For each integer $k \ge 1$, $G$ contains $k$ pairwise edge-disjoint spanning trees if and only if

$$|\delta(\mathcal{P})| \ge k\,(|\mathcal{P}| - 1) \quad \text{for every partition } \mathcal{P} \text{ of } V.$$

The condition for the partition into one part is empty. The condition for the partition into $n$ singletons says $m' \ge k(n - 1)$, where $m'$ is the number of edges that are not self-loops. For $k = 1$ the condition says that every partition into two or more parts has a crossing edge, which is [connectivity](/connected-graph/). So a graph that is not connected has no spanning tree and fails the condition for $k = 1$. Edge weights play no role, so ties do not arise.

## In plain words

You want to build several separate networks on the same set of points, each one connecting all the points, and no two networks may share a link.

Cut the points into groups in any way. Each network has to connect the groups to each other, so it needs at least one link fewer than the number of groups, among the links that run between groups. With $k$ networks you need $k$ times as many. The theorem says that this simple count is the only obstacle: if every way of cutting the points into groups leaves enough links between the groups, the $k$ separate networks exist.

## Proof

**Necessity.** Let $T_1, \ldots, T_k$ be edge-disjoint spanning trees and $\mathcal{P}$ a partition with $p$ parts. Contract each part to one vertex. Each $T_i$ becomes a connected graph on $p$ vertices whose edges are the edges of $T_i$ in $\delta(\mathcal{P})$, so $T_i$ has at least $p - 1$ edges in $\delta(\mathcal{P})$. The trees are disjoint, so $|\delta(\mathcal{P})| \ge k(p - 1)$.

**Sufficiency.** We use the matroid union theorem for the [graphic matroid](/graphic-matroid/) $M$ of $G$, whose independent sets are the forests and whose rank function is $r(F) = n - c(F)$, where $c(F)$ is the number of components of the graph $(V, F)$.

*Matroid union theorem* (Edmonds; Nash-Williams). For a matroid with rank function $r$ on a finite set $E$ and an integer $k \ge 1$, the largest size of a union $I_1 \cup \cdots \cup I_k$ of $k$ independent sets is
$$\min_{F \subseteq E} \big( |E \setminus F| + k\, r(F) \big).$$

The graph has $k$ edge-disjoint spanning trees if and only if some union of $k$ forests has $k(n - 1)$ edges. Indeed, a union of $k$ forests can be taken disjoint, by removing from each forest the edges already in earlier ones, and then it has $k(n - 1)$ edges only if each forest has $n - 1$ edges, that is, each is a spanning tree. So by the theorem it is enough to show

$$|E \setminus F| + k\, r(F) \ge k(n - 1) \quad \text{for each } F \subseteq E.$$

Fix $F$, and let $\mathcal{P}$ be the partition of $V$ into the vertex sets of the components of $(V, F)$, so $|\mathcal{P}| = c(F)$ and $r(F) = n - c(F)$. No edge of $F$ joins two different components, so $\delta(\mathcal{P}) \subseteq E \setminus F$. By the hypothesis,

$$|E \setminus F| \ge |\delta(\mathcal{P})| \ge k\,(c(F) - 1) = k(n - 1) - k\,(n - c(F)) = k(n - 1) - k\, r(F).$$

This is the inequality needed. $\blacksquare$

Diestel gives a proof by graph arguments only, which builds the $k$ trees by an exchange process on $k$ forests of largest total size.

## Consequences

- **Example.** The graph on $a$ to $f$ with the edges $ab, ac, bc, bd, cd, ce, de, df, ef$ has $n = 6$ and $m = 9 < 2 \cdot 5$, so it has no two edge-disjoint spanning trees; the partition into singletons is the witness. It is connected, so it has one.

- **Edge connectivity.** Every $2k$-edge-connected graph has $k$ edge-disjoint spanning trees. *Proof.* In a partition with $p \ge 2$ parts, each part has at least $2k$ edges leaving it, and each crossing edge leaves two parts, so $|\delta(\mathcal{P})| \ge 2k \cdot p / 2 = kp \ge k(p - 1)$. More generally, a $\lambda$-edge-connected graph has $\lfloor \lambda / 2 \rfloor$ edge-disjoint spanning trees.
- **Packing number.** The largest number of edge-disjoint spanning trees is $\min_{\mathcal{P}} \big\lfloor |\delta(\mathcal{P})| / (|\mathcal{P}| - 1) \big\rfloor$ over partitions with at least two parts ([spanning tree packing](/spanning-tree-packing/)).
- **Bounds by edge connectivity.** If $\lambda$ is the [edge connectivity](/edge-connectivity/), the packing number lies between $\lfloor \lambda / 2 \rfloor$ and $\lambda$, since each spanning tree crosses every cut.
- **Covering.** The dual result, the [Nash-Williams arboricity theorem](/nash-williams-arboricity-theorem/), says when the edges can be covered by $k$ forests; it has the same proof by matroid union.
- **Fractional form.** The largest fractional packing of spanning trees, a set of trees with nonnegative weights such that each edge has total weight at most 1, has value $\min_{\mathcal{P}} |\delta(\mathcal{P})| / (|\mathcal{P}| - 1)$ without the floor; this is the *strength* of the graph and relates to the [spanning tree polytope](/spanning-tree-polytope/).

## Tightness

**$2k$ cannot be lowered to $2k - 1$ in general.** The cycle $C_n$ with $n \ge 3$ is 2-edge-connected but has only $n < 2(n - 1)$ edges, so it has no two edge-disjoint spanning trees. More generally, for $k \ge 1$, take the cycle $C_n$ and replace each edge by $k$ parallel edges. The result is $2k$-edge-connected and has $kn$ edges. For the partition into singletons, the condition for $k + 1$ trees asks for $(k + 1)(n - 1)$ edges, which is more than $kn$ when $n > k + 1$. So this $2k$-edge-connected graph has exactly $k$ disjoint spanning trees, and the bound $\lfloor \lambda / 2 \rfloor$ is attained.

**All partitions are needed.** Checking only the partition into singletons, that is $m \ge k(n - 1)$, is not enough. Take two copies of $K_5$ joined by one edge: $n = 10$, $m = 21 \ge 2 \cdot 9 = 18$, yet the partition into the two copies has one crossing edge, fewer than $2 \cdot 1$, so there are no two disjoint spanning trees.

**Examples where it is exact.** $K_{2k}$ has $k(2k - 1)$ edges, exactly $k$ times $n - 1$, and it splits into $k$ edge-disjoint Hamiltonian paths, so it has $k$ disjoint spanning trees that use all its edges. For $K_4$, the paths $1, 2, 3, 4$ and $2, 4, 1, 3$ use all six edges.

## History

Nash-Williams and Tutte proved the theorem independently, and both papers appeared in the Journal of the London Mathematical Society in 1961. Edmonds (1965) and Nash-Williams (1966) put it in the frame of matroids with the matroid union and partition theorems, which also give polynomial-time algorithms. Nash-Williams proved the companion theorem on covering by forests in 1964.

## References
