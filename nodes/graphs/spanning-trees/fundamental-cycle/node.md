---
tag: XEHWZ4
kind: concept
slug: fundamental-cycle
name: Fundamental cycle
aliases:
- fundamental cycle of a non-tree edge
area: graphs/spanning-trees
level: intro
summary: The cycle formed by adding one non-tree edge to a spanning tree.
prereqs: [spanning-tree, simple-cycle, tree]
see_also: [cycle-basis, cycle-property, mst-optimality-conditions, mst-verification, spanning-forest, low-stretch-spanning-tree, spanning-tree-enumeration, lowest-common-ancestor]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer Graduate Texts in Mathematics 173 (2017)
    locator: Section 1.9, Some linear algebra (fundamental cycles and fundamental cuts, and the theorem that they form bases of the cycle space and the cut space)
  - paper: doi:10.1016/j.cosrev.2009.08.001
    title: "Telikepalli Kavitha, Christian Liebchen, Kurt Mehlhorn, Dimitrios Michail, Romeo Rizzi, Torsten Ueckerdt and Katharina A. Zweig, Cycle bases in graphs: characterization, algorithms, complexity, and applications, Computer Science Review 3(4) (2009), 199-243"
    locator: the sections on fundamental cycle bases
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Prentice Hall (1993)
    locator: Chapter 13, Minimum Spanning Trees (the path optimality conditions)
---

A fundamental cycle is the one cycle that appears when one edge that is not in a [spanning tree](/spanning-tree/) $T$ is added to $T$: the edge itself together with the path in $T$ between its two ends. Each of the $m - n + 1$ non-tree edges of a connected graph gives one fundamental cycle, and together these cycles form a basis of the cycle space, the [cycle basis](/cycle-basis/) of $T$. Fundamental cycles are the objects that the [cycle property](/cycle-property/), the [MST optimality conditions](/mst-optimality-conditions/) and [MST verification](/mst-verification/) talk about.

## In plain words

A tree connects all the points of a network with no loop: between two points there is exactly one way to go along the tree. Now add one extra link that is not part of the tree. Its two ends were already connected by the tree, so the new link closes exactly one loop: the link, and the tree route between its ends. This loop is the fundamental cycle of the extra link.

Each extra link gives its own loop. Every other loop of the network can be built by combining these loops, in a way that keeps the links used an odd number of times and drops the links used an even number of times. So a tree and its extra links describe all the loops of a network.

## The idea

Let $G = (V, E)$ be an undirected graph and $T \subseteq E$ a spanning tree of $G$, so $G$ is connected. For a graph that is not connected, let $T$ be a [spanning forest](/spanning-forest/); everything below holds in each component.

**Definition.** For an edge $e = (u, v) \in E \setminus T$, let $P_T(u, v)$ be the path from $u$ to $v$ in $T$. The *fundamental cycle* of $e$ with respect to $T$ is

$$C_T(e) = P_T(u, v) \cup \{e\}.$$

If $e$ is a self-loop, $P_T(u, u)$ is empty and $C_T(e) = \{e\}$. If $e$ is parallel to a tree edge $f$, then $C_T(e) = \{e, f\}$, a cycle of length 2.

**It is the only cycle of $T \cup \{e\}$.** A tree has exactly one path between each two vertices. So $C_T(e)$ is a cycle. Let $C$ be any cycle of $T \cup \{e\}$. The tree $T$ has no cycle, so $C$ uses $e$. Then $C \setminus \{e\}$ is a path from $u$ to $v$ in $T$, and it is $P_T(u, v)$. So $C = C_T(e)$.

**The exchange.** For each tree edge $f \in C_T(e)$, the set $T - f + e$ is again a spanning tree: removing $f$ splits $T$ into two trees, $u$ and $v$ are on different sides because $f$ lies on their only path, and $e$ joins the sides. For a tree edge $f \notin C_T(e)$, the set $T - f + e$ has the cycle $C_T(e)$ and is not a tree. So the fundamental cycle of $e$ is exactly the set of tree edges that $e$ can replace. This is the move behind the [cut property](/cut-property/), the cycle property and the enumeration of spanning trees.

**The dual: fundamental cuts.** For a tree edge $f$, removing $f$ from $T$ leaves two trees with vertex sets $S$ and $V \setminus S$. The *fundamental cut* $D_T(f)$ is the set of edges of $G$ with one end in each side. For $e \notin T$ and $f \in T$,

$$f \in C_T(e) \iff e \in D_T(f),$$

because both sides say that the ends of $e$ are on different sides of $f$ in $T$.

**The cycle space.** Identify a set of edges with its indicator vector in $\mathbb{F}_2^E$, so that the sum of two sets is their symmetric difference. The *cycle space* of $G$ is the set of edge sets in which each vertex has even degree; it is spanned by the cycles of $G$.

**Theorem.** If $G$ is connected, with $n$ vertices and $m$ edges, the $m - n + 1$ fundamental cycles of $T$ form a basis of the cycle space. So its dimension, the *cyclomatic number*, is $m - n + 1$; for a graph with $c$ components it is $m - n + c$.

*Proof.* Independence: the cycle $C_T(e)$ is the only fundamental cycle that contains the non-tree edge $e$. So a sum of a nonempty set of fundamental cycles contains each of their non-tree edges and is not empty. Spanning: let $Z$ be an edge set in which each vertex has even degree, and let $Z' = Z + \sum_{e \in Z \setminus T} C_T(e)$. Each non-tree edge of $Z$ appears twice in this sum, so $Z' \subseteq T$. Each vertex has even degree in $Z'$, because the sum of two even-degree sets is an even-degree set. A nonempty edge set inside a forest has a vertex of degree 1 (a leaf of one of its trees), so $Z' = \emptyset$ and $Z = \sum_{e \in Z \setminus T} C_T(e)$. There are $m - (n - 1)$ non-tree edges, since $|T| = n - 1$. $\square$

**Computing one.** Root $T$ at a vertex and store the parent and the depth of each vertex. Then $P_T(u, v)$ is found by walking up from the deeper of $u$ and $v$, then from both at once, until they meet at their [lowest common ancestor](/lowest-common-ancestor/). This takes time proportional to the length of the cycle. With an LCA structure, the length $\mathrm{depth}(u) + \mathrm{depth}(v) - 2\,\mathrm{depth}(\mathrm{lca}(u, v)) + 1$ is known in $O(1)$ time after linear preprocessing.

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, with the minimum spanning tree $T = \{bc, bd, ef, ac, ce\}$. The graph has $m - n + 1 = 9 - 6 + 1 = 4$ non-tree edges.

| non-tree edge | tree path | fundamental cycle | length |
|---|---|---|---|
| $ab$ | $a, c, b$ | $\{ab, bc, ca\}$ | 3 |
| $cd$ | $c, b, d$ | $\{cd, db, bc\}$ | 3 |
| $de$ | $d, b, c, e$ | $\{de, ec, cb, bd\}$ | 4 |
| $df$ | $d, b, c, e, f$ | $\{df, fe, ec, cb, bd\}$ | 5 |

In each row, the non-tree edge is the heaviest edge of its cycle: $4 > 3, 1$; $4 > 2, 1$; $7 > 5, 2, 1$; $6 > 5, 2, 1$. This is the condition that makes $T$ a minimum spanning tree.

**A cycle as a sum.** The cycle $c, d, f, e$ has the edges $\{cd, df, fe, ec\}$. Its non-tree edges are $cd$ and $df$, so it is $C_T(cd) + C_T(df) = \{cd, db, bc\} + \{df, fe, ec, cb, bd\}$. The edges $bc$ and $bd$ appear twice and cancel, and the sum is $\{cd, df, fe, ec\}$.

**The complete graph.** The complete graph on $n$ vertices has $\binom{n}{2} - n + 1 = \binom{n-1}{2}$ fundamental cycles for each spanning tree. With the star centred at vertex 1 as $T$, each non-tree edge $(i, j)$ gives the triangle $\{1i, ij, j1\}$.

**Non-example.** A cycle of $G$ is not always a fundamental cycle of a given tree. In the example above, the cycle $\{cd, df, fe, ec\}$ contains two non-tree edges, so it is not $C_T(e)$ for any $e$. Each fundamental cycle has exactly one non-tree edge.

## Where it is used

- **Minimum spanning trees.** A spanning tree is minimum if and only if each non-tree edge is a heaviest edge of its fundamental cycle ([MST optimality conditions](/mst-optimality-conditions/)), and this is what [MST verification](/mst-verification/) checks. The [cycle property](/cycle-property/) and [second-best MST](/second-best-mst/) use the same cycles.
- **Cycle bases.** The fundamental cycles of a tree are a [cycle basis](/cycle-basis/); a basis of this kind is a *fundamental cycle basis*. Finding a fundamental basis of least total length is NP-hard, while a minimum cycle basis in general can be found in polynomial time (Kavitha et al., the sections on fundamental bases).
- **Electrical networks.** Kirchhoff's voltage law needs one equation for each fundamental cycle, and the [matrix-tree theorem](/matrix-tree-theorem/) comes from the same analysis.
- **Network simplex.** Each pivot of the [network simplex](/network-simplex/) method adds one non-tree arc to a spanning tree and sends flow around its fundamental cycle.
- **Low-stretch trees.** The stretch of an edge with respect to a tree is the length of its tree path, so the problem of [low-stretch spanning trees](/low-stretch-spanning-tree/) asks for short fundamental cycles on average.
- **Enumeration.** Each spanning tree is reached from each other one by a sequence of exchanges $T - f + e$ with $f \in C_T(e)$, so methods for [spanning tree enumeration](/spanning-tree-enumeration/) can walk from tree to tree by such exchanges.

## References
