---
tag: 54PG58
kind: theorem
slug: laman-theorem
name: Laman's theorem
aliases:
- Laman condition
- Geiringer-Laman theorem
area: cad/geometric-constraint-solving
level: core
summary: A graph with 2n - 3 edges is generically minimally rigid in the plane if and only if every subgraph on k >= 2 vertices has at most 2k - 3 edges.
prereqs: [generic-rigidity, infinitesimal-rigidity, maxwell-counting-rule]
see_also: [henneberg-construction, pebble-game-rigidity, maxwell-counting-rule, generic-rigidity, nash-williams-arboricity-theorem, spanning-tree-packing, distance-based-formation-control, jackson-jordan-theorem]
sources:
  - paper: doi:10.1007/BF01534980
    title: G. Laman, On graphs and rigidity of plane skeletal structures, Journal of Engineering Mathematics 4(4), 331 to 340, 1970
    locator: the main theorem on generic minimal rigidity in the plane and its proof by the two Henneberg moves
  - paper: doi:10.1002/zamm.19270070107
    title: Hilda Pollaczek-Geiringer, Über die Gliederung ebener Fachwerke, Zeitschrift für Angewandte Mathematik und Mechanik 7(1), 58 to 72, 1927
    locator: the earlier proof of the same characterization of plane trusses
  - book: "L. Henneberg, Die graphische Statik der starren Systeme, B. G. Teubner, Leipzig, 1911"
    locator: the construction of plane trusses by adding joints of degree two and three
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 4, Linear and Planar Rigidity
  - paper: doi:10.1137/0603009
    title: L. Lovász and Y. Yemini, On generic rigidity in the plane, SIAM Journal on Algebraic and Discrete Methods 3(1), 91 to 98, 1982
    locator: the matroid view, the rank formula, and the proof by doubling an edge and two spanning trees
  - paper: doi:10.1109/MCS.2008.929280
    title: B. D. O. Anderson, C. Yu, B. Fidan and J. M. Hendrickx, Rigid graph control architectures for autonomous formations, IEEE Control Systems Magazine 28(6), 48 to 63, 2008
    locator: Laman's theorem as the test of rigid formations in the plane
---

Laman's theorem gives a purely combinatorial test for [generic rigidity](/generic-rigidity/) in the plane. A graph with $n \ge 2$ vertices is generically minimally rigid, which means rigid at almost every placement but flexible after the removal of any edge, if and only if it has $2n - 3$ edges and every set of $k \ge 2$ vertices spans at most $2k - 3$ of them. The necessity of the counts is [Maxwell's counting rule](/maxwell-counting-rule/), and the theorem says that in the plane the counts are also sufficient. Pollaczek-Geiringer proved it in 1927, and Laman proved it again in 1970.

## Statement

Let $G = (V, E)$ be a graph with $n = |V| \ge 2$ and $m = |E|$. For $X \subseteq V$, let $i(X)$ be the number of edges with both ends in $X$. Call $G$ a *Laman graph* if
$$ m = 2n - 3 \quad \text{and} \quad i(X) \le 2|X| - 3 \ \text{ for every } X \subseteq V \text{ with } |X| \ge 2. $$
The two *Henneberg moves* add a new vertex $v$ to a graph: a *vertex addition* joins $v$ to two vertices $a \ne b$; an *edge split* removes an edge $ab$ and joins $v$ to $a$, $b$ and one more vertex $c$.

**Theorem (Pollaczek-Geiringer 1927, Laman 1970).** For a graph $G$ with $n \ge 2$ vertices, the following are equivalent.

1. $G$ is generically minimally rigid in the plane: at a generic placement $p$, the rows of the rigidity matrix $R(G, p)$ are linearly independent and have rank $2n - 3$.
2. $G$ is a Laman graph.
3. $G$ can be built from a single edge by a sequence of Henneberg moves.

**Corollary.** A graph is generically rigid in the plane if and only if it has a spanning subgraph that is a Laman graph, that is, $2n - 3$ edges on all $n$ vertices with at most $2k - 3$ of them on every $k \ge 2$ vertices.

**For robotics.** Let $n \ge 2$ robots, sensors or features in the plane, and let $E$ be the pairs whose distances are measured or controlled. For almost every shape of the group, the distances determine the shape locally, up to a translation and a rotation, if and only if $E$ contains $2n - 3$ pairs such that no $k \ge 2$ members carry more than $2k - 3$ of the chosen pairs. A formation that uses exactly such a set of $2n - 3$ links is minimally rigid: it keeps its shape, and the loss of any one link lets it deform. The [pebble game](/pebble-game-rigidity/) checks the condition in $O(n^2)$ time, and the [Henneberg construction](/henneberg-construction/) gives a way to add robots one at a time while keeping the formation rigid. The word "almost" matters: at special shapes, such as three robots on a line or $K_{3,3}$ on a conic, a Laman graph is infinitesimally flexible.

## In plain words

Think of points in the plane joined by rods, placed at random. The structure is stiff with no spare rod exactly when two things hold. First, the number of rods is twice the number of points, minus three. Second, no group of points has more rods among its own members than twice its size minus three. So stiffness at a random placement can be decided by counting alone, without any coordinates.

Every structure of this kind can also be grown from one rod. At each step you either add a point tied by two new rods, or you take out one rod and add a point tied by three new rods, two of them to the ends of the removed rod.

## Proof

The proof goes around the cycle $1 \Rightarrow 2 \Rightarrow 3 \Rightarrow 1$. Throughout, a set $X$ with $|X| \ge 2$ is *tight* in a graph if $i(X) = 2|X| - 3$.

**1 implies 2.** Let $p$ be generic. The rows of $R(G, p)$ are independent and the rank is $2n - 3$, so $m = 2n - 3$. For a set $X$ with $k \ge 2$ vertices, the rows of the edges inside $X$ are independent and form the rigidity matrix of $(G[X], p|_X)$, padded with zeros. The points $p|_X$ are distinct, so the two translations and the rotation restricted to $X$ are three independent infinitesimal motions in its kernel, and its rank is at most $2k - 3$. So $i(X) \le 2k - 3$.

**2 implies 3.** By induction on $n$. For $n = 2$ the only Laman graph is a single edge. Let $n \ge 3$ and let $G$ be a Laman graph.

*Low degree.* Every vertex $v$ has degree at least 2, because $X = V \setminus \{v\}$ gives $m - \deg v = i(X) \le 2(n - 1) - 3$, so $\deg v \ge 2$. The degrees add up to $2m = 4n - 6 < 4n$, so some vertex $v$ has degree 2 or 3.

*Degree 2.* Then $G - v$ has $2n - 5 = 2(n - 1) - 3$ edges, and its subsets are subsets of $G$, so $G - v$ is a Laman graph. By induction it has a Henneberg construction, and $G$ follows from $G - v$ by a vertex addition.

*Degree 3.* Let $a$, $b$, $c$ be the neighbors of $v$, and $H = G - v$, with $2(n - 1) - 4$ edges. For a pair $xy$ of neighbors, $H + xy$ is a Laman graph unless some set $X \ni x, y$ is tight in $H$: adding $xy$ raises $i(X)$ by 1 exactly for the sets that contain $x$ and $y$, and the other sets keep their counts. (If $xy$ is already an edge, then $\{x, y\}$ is tight.) Suppose that each of the three pairs lies in a tight set of $H$: $X_1 \supseteq \{a, b\}$, $X_2 \supseteq \{b, c\}$, $X_3 \supseteq \{a, c\}$. Two facts about tight sets give a contradiction.

- If $X$ and $Y$ are tight and $|X \cap Y| \ge 2$, then $X \cup Y$ is tight. Every edge inside $X$ or inside $Y$ is inside $X \cup Y$, and the edges inside both are inside $X \cap Y$, so
$$ i(X \cup Y) \ge i(X) + i(Y) - i(X \cap Y) \ge (2|X| - 3) + (2|Y| - 3) - (2|X \cap Y| - 3) = 2|X \cup Y| - 3, $$
and the Laman count gives equality.
- If $X_1 \cap X_2 = \{b\}$, $X_2 \cap X_3 = \{c\}$ and $X_1 \cap X_3 = \{a\}$, then $U = X_1 \cup X_2 \cup X_3$ is tight. The triple intersection is empty, so $|U| = |X_1| + |X_2| + |X_3| - 3$. An edge inside two of the sets would have both ends in a single vertex, so the edges inside the three sets are distinct, and
$$ i(U) \ge \sum_{t} (2|X_t| - 3) = 2(|U| + 3) - 9 = 2|U| - 3. $$

Each pairwise intersection contains one of $a$, $b$, $c$. If one of them has at least 2 vertices, the first fact makes the union of those two sets a tight set that contains $a$, $b$ and $c$. Otherwise the second fact does. In both cases a tight set $Y \subseteq V \setminus \{v\}$ of $H$ contains $a$, $b$, $c$, and then in $G$
$$ i(Y \cup \{v\}) = 2|Y| - 3 + 3 = 2|Y \cup \{v\}| - 2, $$
which breaks the Laman count. So some pair, say $ab$, is not an edge of $H$ and $H + ab$ is a Laman graph on $n - 1$ vertices. By induction it has a Henneberg construction, and $G$ follows from $H + ab$ by the edge split of $ab$ with the new vertex $v$ and the third neighbor $c$.

**3 implies 1.** By induction along the construction. A single edge at two distinct points has one nonzero row, of rank $1 = 2 \cdot 2 - 3$. The generic rank of a graph is at least its rank at any particular placement, so it suffices to show: if $G'$ has independent rows of rank $2n' - 3$ at a generic $p'$, then the graph $G$ after one move has independent rows at some placement $p$ that extends $p'$. The number of edges grows by 2 in both moves, so $m = 2n - 3$, and independence at one placement then gives rank $2n - 3$ at a generic placement of $G$.

*Vertex addition* with neighbors $a$, $b$. Put $p_v$ off the line through $p_a$ and $p_b$ (these points differ, since $p'$ is generic). The old rows are zero in the two columns of $v$, and the two new rows have $p_v - p_a$ and $p_v - p_b$ there, which are not parallel. So a dependence among the rows has zero weight on the new rows, and then zero weight on the old ones too.

*Edge split* of $ab$ with neighbors $a$, $b$, $c$. Put $p_v = p_a + t(p_b - p_a)$ with a real $t \ne 0, 1$, on the line through $p_a$ and $p_b$; $p_c$ is off this line, since $p'$ is generic. Let $w = p_b - p_a$. Suppose a combination of the rows of $G$ with weights $\omega$ is zero. In the columns of $v$ only the three new rows are nonzero:
$$ \omega_{va}\, t w + \omega_{vb}\, (t - 1) w + \omega_{vc}\, (p_v - p_c) = 0. $$
The vector $p_v - p_c$ is not parallel to $w$, so $\omega_{vc} = 0$ and $t\, \omega_{va} = (1 - t)\, \omega_{vb} =: \lambda$. The row of $va$ has $p_a - p_v = -t w$ in the columns of $a$, and the row of $vb$ has $p_b - p_v = (1 - t) w$ in the columns of $b$. So outside the columns of $v$, the two rows together contribute $-\lambda w$ at $a$ and $\lambda w$ at $b$, which is $\lambda$ times the row of $ab$ in $R(G', p')$. The other rows of $G$ are the rows of $G' - ab$. So the zero combination becomes a combination of the rows of $G'$ with weight $\lambda$ on $ab$, and independence in $G'$ gives $\lambda = 0$ and zero weights on all other rows. Since $t \ne 0, 1$, also $\omega_{va} = \omega_{vb} = 0$. So the rows of $G$ at $p$ are independent.

**The corollary.** If $G$ is generically rigid, choose $2n - 3$ independent rows of $R(G, p)$ at a generic $p$. Their edges form a spanning subgraph that satisfies statement 1, hence a Laman graph. Conversely, a spanning Laman subgraph has rank $2n - 3$ at a generic $p$, and adding edges cannot lower the rank. $\blacksquare$

## Consequences

- **The planar rigidity matroid is a count matroid.** The edge sets with $i(X) \le 2|X| - 3$ for all $|X| \ge 2$ are exactly the sets of independent rows at a generic placement, and they form a [matroid](/matroid/) on the edges of $K_n$ whose bases are the Laman graphs. The [matroid greedy algorithm](/matroid-greedy-algorithm/) therefore finds a largest independent set, and the [pebble game](/pebble-game-rigidity/) runs it in $O(n)$ time per edge.
- **Two spanning trees.** A graph $G$ with $2n - 3$ edges is a Laman graph if and only if, for every edge $e$, the [multigraph](/multigraph/) $G + e$ (with $e$ doubled) is the union of two edge-disjoint spanning trees. *Proof.* $G + e$ has $2n - 2$ edges. By the [Nash-Williams arboricity theorem](/nash-williams-arboricity-theorem/) its edges can be covered by two forests if and only if every set $X$ spans at most $2|X| - 2$ of them, and two forests with $2n - 2$ edges together are two spanning trees. If $G$ is Laman, a set spans at most $2|X| - 3 + 1$ edges of $G + e$. Conversely, a set $X$ with $|X| \ge 2$ that spans an edge $e$ of $G$ satisfies $i(X) + 1 \le 2|X| - 2$ in $G + e$, and a set that spans no edge satisfies the count trivially. This is the form used by Lovász and Yemini (1982) and by the algorithms based on [spanning tree packing](/spanning-tree-packing/).
- **Rank formula.** Lovász and Yemini (1982) showed that the generic rank of a graph in the plane is the minimum, over all families of vertex sets $X_1, \ldots, X_t$ with $|X_s| \ge 2$ such that every edge lies inside some $X_s$, of $\sum_s (2|X_s| - 3)$. They also proved that every 6-connected graph is generically rigid in the plane.
- **Polynomial tests.** The Laman count has exponentially many subsets, but it can be tested in polynomial time: by the pebble game in $O(n^2)$, or by $m$ tests for two spanning trees. Generic rigidity in the plane is thus decidable in polynomial time, while for rigidity at given coordinates one computes the rank of $R(G, p)$ directly.
- **Rigid components.** Every graph splits its edges into rigid components, the maximal vertex sets whose induced subgraph is generically rigid. Two of them share at most one vertex, and the pebble game finds them. In CAD they are the well-constrained clusters of a distance constraint graph, see [DR-plans](/dr-plan/) and [degrees of freedom analysis](/degrees-of-freedom-analysis/).
- **Global rigidity** needs more: a Laman graph with $n \ge 4$ vertices is never generically globally rigid, because it is not redundantly rigid ([Jackson-Jordán theorem](/jackson-jordan-theorem/)).

## Tightness

- **Generic placements are needed.** $K_{3,3}$ is a Laman graph. At six points on a conic, for example the rational points of the unit circle with parameters $t = 0, 1, 2$ and $t = -1, \tfrac{1}{2}, 3$, its rigidity matrix has rank 8 instead of 9. A triangle on a line has rank 2 instead of 3. So statement 2 says nothing about a particular placement.
- **The total count is not enough.** $K_4$ plus a vertex of degree 1 has $7 = 2 \cdot 5 - 3$ edges and rank 6: the $K_4$ breaks the subset count and the pendant vertex turns.
- **The subset count is needed only for $|X| \ge 2$.** For $|X| = 1$ the value $2 \cdot 1 - 3 = -1$ has no meaning, and every vertex spans 0 edges.
- **No analog in space.** The same statement with $3n - 6$ and $3k - 6$ is false in $\mathbb{R}^3$: the double banana has $n = 8$, $m = 18 = 3n - 6$, all subset counts hold, and its generic rank is 17. No combinatorial characterization of generic rigidity of bar-and-joint frameworks in three dimensions is known. For rigid bodies joined by bars, [Tay's theorem](/tay-theorem/) does give one.
- **Example of the induction.** The triangular prism with triangles $012$ and $345$ and the edges $03$, $14$, $25$ is a Laman graph with every degree equal to 3. At $v = 5$ the pair $34$ is an edge, so the proof tries the other pairs, and $H + 23$ is a Laman graph. In $H + 23$ the vertex 4 has degree 2, and so on. Read forward: start from the edge $01$, add 2 to $0, 1$, add 3 to $0, 2$, add 4 to $1, 3$, and split $23$ with the new vertex 5 and third neighbor 4. The result is the prism.

## History

Henneberg (1911) built plane trusses by the two moves and knew that they give stiff trusses. Pollaczek-Geiringer (1927) proved that the counts characterize the generic minimally rigid plane trusses, in a paper on the structure of plane trusses in ZAMM, and treated space trusses in 1932. Her work was forgotten, and Laman (1970) proved the theorem again, with the same induction by Henneberg moves. Asimow and Roth (1978) set the theory on the rigidity matrix at generic points. Lovász and Yemini (1982) gave the matroid view and the rank formula, and Jacobs and Hendrickson (1997) the [pebble game](/pebble-game-rigidity/). The name Geiringer-Laman theorem is now common.

## References
