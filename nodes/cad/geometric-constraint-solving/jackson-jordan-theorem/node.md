---
tag: QYX1EP
kind: theorem
slug: jackson-jordan-theorem
name: Jackson-Jordan global rigidity theorem
aliases:
- characterization of generic global rigidity in the plane
area: cad/geometric-constraint-solving
level: research
summary: A graph is generically globally rigid in the plane if and only if it is a complete graph on at most 3 vertices or it is 3-connected and redundantly rigid.
prereqs: [global-rigidity, laman-theorem, henneberg-construction, k-vertex-connected-graph]
see_also: [global-rigidity, generic-rigidity, laman-theorem, henneberg-construction, pebble-game-rigidity, vertex-connectivity, distance-based-formation-control, root-identification-problem]
sources:
  - paper: doi:10.1016/j.jctb.2004.11.002
    title: Bill Jackson and Tibor Jordán, Connected rigidity matroids and unique realizations of graphs, Journal of Combinatorial Theory, Series B 94(1), 1 to 29, 2005
    locator: the main theorem, the reduction of 3-connected M-connected graphs to K4 by inverse 1-extensions and edge deletions, and the corollary on 6-connected graphs (general locator)
  - paper: doi:10.1137/0221008
    title: Bruce Hendrickson, Conditions for unique graph realizations, SIAM Journal on Computing 21(1), 65 to 84, 1992
    locator: the necessity of (d + 1)-connectivity and of redundant rigidity, and the conjecture that they suffice in the plane
  - paper: doi:10.1007/s00454-004-1124-4
    title: Robert Connelly, Generic global rigidity, Discrete and Computational Geometry 33(4), 549 to 563, 2005
    locator: the stress matrix condition for global rigidity and the proof that 1-extensions keep it
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: the converse of Connelly's stress condition, in every dimension
  - paper: doi:10.1109/TMC.2006.174
    title: J. Aspnes, T. Eren, D. K. Goldenberg, A. S. Morse, W. Whiteley, Y. R. Yang, B. D. O. Anderson and P. N. Belhumeur, A theory of network localization, IEEE Transactions on Mobile Computing 5(12), 1663 to 1678, 2006
    locator: the use of the planar characterization for unique localization of sensor networks
---

The Jackson-Jordán theorem gives a combinatorial test for [global rigidity](/global-rigidity/) of generic frameworks in the plane. Hendrickson (1992) proved that a generically globally rigid graph on at least 4 vertices must be 3-connected and redundantly rigid, and asked whether these two conditions are also enough. Jackson and Jordán (2005) proved that they are, by combining a construction of these graphs from $K_4$ with Connelly's theorem that the construction steps keep global rigidity. The test runs in polynomial time and decides when the distances on the edges fix a generic planar shape uniquely.

## Statement

Let $G = (V, E)$ be a graph with $n$ vertices. $G$ is *generically globally rigid* in the plane if every generic framework $(G, p)$ in $\mathbb{R}^2$ is globally rigid: every framework $(G, q)$ in $\mathbb{R}^2$ with the same edge lengths is congruent to $(G, p)$. $G$ is *redundantly rigid* in the plane if $G - e$ is generically rigid for every edge $e$. $G$ is *3-connected* if $n \ge 4$ and removing any two vertices leaves a connected graph.

**Theorem (Jackson and Jordán 2005).** $G$ is generically globally rigid in the plane if and only if $G$ is a complete graph on at most 3 vertices, or $G$ is 3-connected and redundantly rigid.

## In plain words

Joints in general position in the plane are joined by rods of fixed length. The structure has only one possible shape, up to moving it around, exactly when two things hold. First, no two joints split it: if they did, one side could be flipped over the line through them. Second, every rod is spare: after taking any one rod out, the structure is still stiff. If some rod were needed, the structure without it could bend, and while it bends, the gap where that rod was can come back to its old length in a different shape. These two tests are the whole story, unless the structure has at most three joints, where it must have all its rods.

## Proof

The case $n \le 3$ is direct: $K_1$, $K_2$ and $K_3$ are globally rigid at every placement, since all distances are given. A graph on at most 3 vertices with a missing edge $uv$ is not even rigid: a vertex of degree at most 1 turns freely, and a path $u w v$ bends at $w$. So assume $n \ge 4$ from now on.

**Necessity of 3-connectivity (full proof).** Let $p$ be generic and suppose that a set $S$ of at most two vertices separates $G$ into sides $A$ and $B$, nonempty and with no edge between them. Choose a line $L$ through the points of $S$ and through no other point of $p$: if $|S| = 2$ it is the line through them, which holds no third point because $p$ is generic, and if $|S| \le 1$ there is a free choice. Let $\sigma$ be the reflection in $L$, and put $q_i = \sigma(p_i)$ for $i \in B$ and $q_i = p_i$ otherwise. Each edge lies inside $A \cup S$ or inside $B \cup S$, and $\sigma$ fixes the points of $S$, so each edge keeps its length. For $x \in A$ and $y \in B$, $|q_x - q_y| = |p_x - p_y|$ would put $p_x$ on the perpendicular bisector of $p_y$ and $\sigma(p_y)$, which is $L$, and no point of $A$ lies on $L$. So $(G, q)$ has the same edge lengths and is not congruent to $(G, p)$.

**Necessity of redundant rigidity (sketch).** This is Hendrickson's argument, in his paper of 1992, in the section on redundant rigidity. If $G$ is not rigid, it has non-congruent frameworks near $p$ with the same lengths. Otherwise, suppose $G - e$ is flexible for an edge $e = uv$. Adding edges to $G - e$ gives a graph $H$ whose generic frameworks have one degree of freedom, and the frameworks with the lengths of $(H, p)$, up to congruence, form a smooth closed curve through $p$. On this curve the length of $e$ is a smooth function, and at the generic point $p$ it is not stationary, because adding $e$ makes the framework rigid. So the function takes values above and below $|p_u - p_v|$ near $p$, and on a closed curve it must come back to $|p_u - p_v|$ at a second point $q$, which is not congruent to $p$. Then $(G, q)$ is equivalent to $(G, p)$ and not congruent to it.

**Sufficiency, step 1: the moves keep a stress certificate.** An *equilibrium stress* of $(G, p)$ is a weight $\omega_{ij}$ on each edge with $\sum_j \omega_{ij}(p_j - p_i) = 0$ at every vertex $i$, and its *stress matrix* $\Omega$ is the $n \times n$ matrix with $\Omega_{ij} = -\omega_{ij}$ for edges, 0 for other pairs, and row sums 0. Say that $G$ has property (S) if its generic frameworks have a stress whose stress matrix has rank $n - 3$. Connelly (2005) proved that a generic framework with such a stress is globally rigid. Two moves keep (S).

- *Edge addition.* Extend the stress by 0 on the new edge; $\Omega$ does not change.
- *1-extension* (an edge split of the [Henneberg construction](/henneberg-construction/)): remove an edge $xy$ and add a new vertex $v$ joined to $x$, $y$ and a third vertex $z$. Connelly proved that this keeps (S) when $G - xy$ is rigid. The idea is to place $v$ on the segment $xy$, give $vx$ and $vy$ the stress that $xy$ had, scaled so that $v$ is in equilibrium, give $vz$ the stress 0, and then move to a generic position while keeping the rank.

$K_4$ has (S): its generic frameworks have a one-dimensional space of stresses with all coefficients nonzero, and the stress matrix has rank $1 = n - 3$. Gortler, Healy and Thurston (2010) later proved that every generically globally rigid graph has (S), so the certificate is exact.

**Sufficiency, step 2: the construction (sketch).** Call $G$ *M-connected* if its edge set is connected in the generic rigidity matroid of the plane, that is, every two edges lie in a common circuit. Jackson and Jordán prove two things, in their paper of 2005:

1. A 3-connected, redundantly rigid graph is M-connected.
2. Every 3-connected M-connected graph other than $K_4$ has either an edge whose removal leaves a 3-connected M-connected graph, or a vertex of degree 3 with an inverse 1-extension that leaves a 3-connected M-connected graph. So every such graph is built from $K_4$ by edge additions and 1-extensions.

The proof of the second part uses ear decompositions of the rigidity matroid and a detailed study of the vertices of degree 3 and the 2-separations that an inverse 1-extension can create. The case of a matroid circuit was proved before by Berg and Jordán.

**Putting it together.** A 3-connected, redundantly rigid $G$ with $n \ge 4$ has a construction from $K_4$ by edge additions and 1-extensions, in which every intermediate graph is 3-connected and M-connected. An M-connected graph is redundantly rigid, so each 1-extension is made on an edge $xy$ with $G - xy$ rigid. $K_4$ has (S), each move keeps (S) by step 1, so $G$ has (S), and by Connelly's theorem every generic framework of $G$ is globally rigid. With the necessity part, this proves the theorem. $\square$

## Consequences

- **A polynomial test.** 3-connectivity takes linear time, and redundant rigidity can be tested with the [pebble game](/pebble-game-rigidity/): $G$ is redundantly rigid if and only if it is rigid and every edge lies in a circuit, which is the same as: for each edge $e$, the game on $G - e$ reaches rank $2n - 3$. With the $O(nm)$ game of that page this gives an $O(n m^2)$ test, and faster ones are known.
- **Generic global rigidity is a property of the graph.** In the plane it follows from the theorem: the answer does not depend on which generic placement is taken. Gortler, Healy and Thurston proved this in every dimension.
- **6-connected graphs.** Jackson and Jordán derived that every 6-connected graph is generically globally rigid in the plane.
- **Minimal globally rigid graphs.** A redundantly rigid graph has at least $2n - 2$ edges, and a 3-connected circuit of the rigidity matroid, such as a wheel, reaches this bound.
- **Localization and formations.** A planar sensor network with measured distances and at least three anchors in general position has unique positions, for generic positions, exactly when the graph with the anchors joined to each other is 3-connected and redundantly rigid. The same test tells whether a [formation](/distance-based-formation-control/) of robots that keeps distances has one shape or several.
- **CAD sketches.** A planar sketch of points and distances that is rigid but not globally rigid has several solutions, and the solver must choose one, the [root identification problem](/root-identification-problem/). A sketch whose graph passes the test has one solution at generic dimensions, but a sketch with $n \ge 4$ points and exactly $2n - 3$ independent distances is never redundantly rigid, so its solver always has the choice.

## Tightness

The rank claims below were checked with the pebble game.

- **3-connectivity alone is not enough.** $K_{3,3}$ and the triangular prism are 3-connected, but they have $2n - 3 = 9$ edges, so no edge is redundant. Their generic frameworks have a second, non-congruent realization.
- **Redundant rigidity alone is not enough.** Two copies of $K_4$ that share one edge have $n = 6$ and $11$ edges, and every $G - e$ has rank $9 = 2n - 3$, so the graph is redundantly rigid. The two shared vertices separate it, and reflecting one copy in the line through them gives a non-congruent framework.
- **Genericity is needed.** The wheel with hub $h$ and rim $r_0 r_1 r_2 r_3$ is 3-connected and redundantly rigid. Place $h$ at the origin and the rim at $(1, 0), (0, 1), (-1, 0), (0, -1)$. Move $r_2$ to $(1, 0)$ and $r_3$ to $(0, 1)$: all spokes keep length 1 and all rim edges keep length $\sqrt{2}$, but $r_0$ and $r_2$ now coincide. This framework is not globally rigid, though its graph is generically globally rigid.
- **The plane is needed.** In $\mathbb{R}^3$ the analogous conditions, 4-connectivity and redundant rigidity, are necessary but not sufficient: Connelly showed that $K_{5,5}$ satisfies them and is not generically globally rigid in space. No combinatorial characterization is known in dimension 3 or more.

## History

Hendrickson (1992) found the two necessary conditions in all dimensions, in his work on unique graph realization, motivated by the computation of molecular conformations from distances, and conjectured that they are sufficient in the plane. Connelly found that $K_{5,5}$ breaks the analogue in space, and his stress matrix condition, published in full in 2005, showed that 1-extensions keep global rigidity. Berg and Jordán (2003) proved the construction for circuits of the rigidity matroid, which settled the case of graphs with $2n - 2$ edges, and Jackson and Jordán (2005) extended it to all M-connected graphs and so proved Hendrickson's conjecture. Gortler, Healy and Thurston (2010) proved the converse of Connelly's condition, which makes generic global rigidity a property of the graph in every dimension.

## References
